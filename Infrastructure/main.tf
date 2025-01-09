# Terraform and Provider Versions
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.82.2"
    }
    awscc = {
      source  = "hashicorp/awscc"
      version = "~> 1.0"
    }
  }
  required_version = "~> 1.10"
}

variable "build_bucket_name" {
  description = "Name of the S3 bucket containing the game server build"
  type        = string
}

variable "build_key_path" {
  description = "Path to the build files in the S3 bucket"
  type        = string
  default     = "path/to/build/files"
}

provider "aws" {
  profile = "default"
  region = "eu-west-3"  # Paris Region
}

# ECR Repository
resource "aws_ecr_repository" "game_containers" {
  name                 = "outbreak-protocol-containers"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# VPC Configuration
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "outbreak-protocol-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["eu-west-3a", "eu-west-3b", "eu-west-3c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway     = true
  single_nat_gateway     = true
  enable_dns_hostnames   = true
  enable_dns_support     = true
}

# IAM Role for GameLift
resource "aws_iam_role" "gamelift_role" {
  name = "outbreak-protocol-gamelift-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "gamelift.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "gamelift_policy" {
  role       = aws_iam_role.gamelift_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGameLiftServiceRole"
}

# GameLift Fleet
resource "aws_gamelift_build" "game_server" {
  name             = "outbreak-protocol-build"
  operating_system = "AMAZON_LINUX_2023"

  storage_location {
    bucket   = var.build_bucket_name
    key      = var.build_key_path
    role_arn = aws_iam_role.gamelift_role.arn
  }
}

resource "aws_gamelift_fleet" "game_fleet" {
  name              = "outbreak-protocol-fleet"
  build_id          = aws_gamelift_build.game_server.id
  ec2_instance_type = "c5.large"

  fleet_type = "ON_DEMAND"
  
  runtime_configuration {
    game_session_activation_timeout_seconds = 300
    server_process {
      launch_path = "/srv/OutbreakProtocolServer"
      parameters  = "-game"
      concurrent_executions = 1
    }
  }

  ec2_inbound_permission {
    from_port = 7777
    to_port   = 7779
    ip_range  = "10.0.0.0/16"  # VPC CIDR
    protocol  = "UDP"
  }

  depends_on = [aws_iam_role_policy_attachment.gamelift_policy]
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "outbreak-protocol-cluster"
  cluster_version = "1.31"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  enable_irsa = true

  eks_managed_node_groups = {
    main = {
      desired_size = 1
      min_size     = 1
      max_size     = 3

      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"
    }
  }
}

# Security Group for EKS to GameLift Communication
resource "aws_security_group" "eks_to_gamelift" {
  name_prefix = "eks-to-gamelift"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port = 30020
    to_port   = 30020
    protocol  = "tcp"
    self      = true
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "eks-to-gamelift-sg"
  }
}

# IAM Role for Bedrock access from EKS
resource "aws_iam_role" "eks_bedrock_role" {
  name = "eks-bedrock-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRoleWithWebIdentity"
        Effect = "Allow"
        Principal = {
          Federated = module.eks.oidc_provider_arn
        }
        Condition = {
          StringEquals = {
            "${module.eks.oidc_provider}:aud" : "sts.amazonaws.com",
            "${module.eks.oidc_provider}:sub" : "system:serviceaccount:default:bedrock-bot-sa"
          }
        }
      }
    ]
  })
}

# IAM Policy for Bedrock access
resource "aws_iam_policy" "bedrock_access_policy" {
  name = "bedrock-access-policy"
  path = "/"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:ListFoundationModels",
          "bedrock:ListCustomModels",
          "bedrock:GetFoundationModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = "*"
      }
    ]
  })
}

# Attach the Bedrock policy to the role
resource "aws_iam_role_policy_attachment" "bedrock_policy_attachment" {
  policy_arn = aws_iam_policy.bedrock_access_policy.arn
  role       = aws_iam_role.eks_bedrock_role.name
}

# Kubernetes Service Account
resource "kubernetes_service_account" "bedrock_bot_sa" {
  metadata {
    name      = "bedrock-bot-sa"
    namespace = "default"
    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.eks_bedrock_role.arn
    }
  }
  depends_on = [module.eks]
}

# IAM Role for ECR access from EKS
resource "aws_iam_role_policy_attachment" "eks_ecr" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = module.eks.cluster_iam_role_name
}

# S3 Bucket for Game-Level Data
resource "aws_s3_bucket" "game_level_data" {
  bucket = "game-level-data-bucket"

  tags = {
    Name        = "Game-Level-Data-Bucket"
    Environment = "Production"
  }
}

# S3 Bucket Notification Configuration
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.game_level_data.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.s3_change_lambda.arn
    events              = ["s3:ObjectCreated:*", "s3:ObjectRemoved:*"] # Trigger for any object change
  }

  depends_on = [aws_lambda_permission.allow_bucket_notification]
}

# Lambda Execution Role
resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Lambda Role Policy for S3 Access and Logging
resource "aws_iam_policy" "lambda_policy" {
  name        = "lambda_policy"
  description = "Policy for Lambda to access S3 and CloudWatch logs"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject", "s3:ListBucket"]
        Resource = [
          aws_s3_bucket.game_level_data.arn,
          "${aws_s3_bucket.game_level_data.arn}/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Attach the IAM Policy to the Lambda Execution Role
resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# Lambda Function Deployment
resource "aws_lambda_function" "s3_change_lambda" {
  function_name = "sync_knowledge_base"
  runtime       = "python3.12"
  role          = aws_iam_role.lambda_execution_role.arn
  handler       = "sync_knowledge_base.lambda_handler"

  # ZIP deploy of sync lambda
  filename = "sync_knowledge_base.zip"
  source_code_hash = filebase64sha256("sync_knowledge_base.zip")

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.game_level_data.id
    }
  }
}

# Allow S3 Bucket to Trigger the Lambda
resource "aws_lambda_permission" "allow_bucket_notification" {
  statement_id  = "AllowS3BucketNotification"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.s3_change_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.game_level_data.arn
}

# Create Bedrock Knowledge Base (Placeholder)
resource "aws_bedrock_knowledge_base" "game_data_knowledge_base" {
  name        = "GameDataKnowledgeBase"
  description = "Knowledge base linked to S3 for game-level data"
  source_type = "S3"
  s3_bucket   = aws_s3_bucket.game_level_data.id
  region      = "eu-west-3"

  depends_on = [aws_s3_bucket.game_level_data]
}


# Outputs
output "ecr_repository_url" {
  value = aws_ecr_repository.game_containers.repository_url
}

output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "gamelift_fleet_id" {
  value = aws_gamelift_fleet.game_fleet.id
}
