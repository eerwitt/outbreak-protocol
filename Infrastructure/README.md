# Architectual Diagram
                +--------------------+
                |                    |
                |   Discord Server💽 |
                |                    |
                +--------------------+
                        |
                        | Player sends a message 📨
                        v
            +---------------------------+
            |                           |
            | Amazon EKS (Discord Bot)  |
            |                           |
            +---------------------------+
                        |
                        | Matches session and connects to
                        | AWS GameLift game server via IP/port
                        v
    +-----------------------------------------------+
    |                                               |
    | AWS GameLift (Dedicated Game Server)          |
    | - Sends private IP (game_host) and port       |
    | - Uploads level info to S3                    |
    |                                               |
    +-----------------------------------------------+
                        |
                        | Uploads game-level data
                        v
            +---------------------------+
            |                           |
            |     Amazon S3 Bucket      |
            |                           |
            +---------------------------+
                        |
                        | S3 bucket change triggers
                        v
            +---------------------------+
            |                           |
            |    AWS Lambda Function    |
            | - Syncs data to Bedrock   |
            |   Knowledge Base          |
            +---------------------------+
                        |
                        | Updates Bedrock Knowledge Base
                        v
            +---------------------------+
            |                           |
            |   Amazon Bedrock          |
            | - Processes live context  |
            | - Suggests actions        |
            +---------------------------+
                        ^
                        | 🤖Bot queries Bedrock with context
                        | and possible actions
                        |
            +---------------------------+
            |                           |
            | Amazon EKS (Discord Bot)  |
            | - Receives actions        |
            | - Sends commands to Game  |
            |   Server                  |
            +---------------------------+
                        |
                        | Sends action commands
                        v
    +-----------------------------------------------+
    | AWS GameLift (Dedicated Game Server) 🐻       |
    | - Executes the commands in the live session   |
    +-----------------------------------------------+

## Instructions

Most steps are taken care of via a combination of Terraform and kubectl for deploying the bot.

Sadly, to create the knowledge base, it requires editing the console and creating with the specific name used throughout `game-knowledge-base`.