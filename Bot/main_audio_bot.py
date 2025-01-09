"""
Initial prototype for playing the game with audio feedback. Not actively used in the hackathon project.
"""
import boto3
import discord
import argparse
import asyncio
import wave
import os
import time
import logging
import requests
from io import BytesIO
from discord.ext import commands

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_vocabulary(transcribe_client: boto3.client, vocabulary_name: str) -> str:
    """
    Check if a vocabulary exists within the specified timeout.

    Args:
        transcribe_client: Boto3 Transcribe client.
        vocabulary_name: Name of the vocabulary to check.
        timeout: Timeout in seconds to wait for the vocabulary.

    Returns:
        str: Status of the vocabulary.
    """
    try:
        response = transcribe_client.get_vocabulary(VocabularyName=vocabulary_name)
        status = response["VocabularyState"]
        logger.info(f"Vocabulary {vocabulary_name} exists with a status of {status}.")
        return status
    except transcribe_client.exceptions.BadRequestException:
        logger.info("No vocabulary exists.")
        return "NONE"

def create_vocabulary(transcribe_client: boto3.client, vocabulary_name: str, timeout: int = 120) -> None:
    """
    Create a new vocabulary.

    Args:
        transcribe_client: Boto3 Transcribe client.
        vocabulary_name: Name of the vocabulary to create.
        timeout: Timeout in seconds to wait for the vocabulary to be ready.
    """
    logger.info(f"Creating vocabulary {vocabulary_name}...")
    transcribe_client.create_vocabulary(
        VocabularyName=vocabulary_name,
        LanguageCode="en-US",
        Phrases=["Outbreak", "Protocol", "Zombie", "Bear"]
    )

    # Wait for the vocabulary to be ready
    start_time = time.time()
    while True:
        status = check_vocabulary(transcribe_client, vocabulary_name)
        if status == "READY":
            logger.info(f"Vocabulary {vocabulary_name} is ready.")
            break
        elif status == "FAILED":
            raise Exception("Vocabulary creation failed.")
        elif status == "NONE":
            raise Exception("Vocabulary doesn't exist.")
        elif status == "TIMEOUT":
            raise Exception("Timeout checking vocabulary.")
        elif time.time() - start_time > timeout:
            raise Exception(f"Timeout waiting for vocabulary {vocabulary_name} to be ready.")
        else:
            logging.debug("Waiting for ready state of vocabulary.")
        time.sleep(5)

def check_or_create_vocabulary(transcribe_client: boto3.client, vocabulary_name: str) -> None:
    """
    Ensure that the vocabulary exists, creating it if necessary.

    Args:
        transcribe_client: Boto3 Transcribe client.
        vocabulary_name: Name of the vocabulary to check or create.
    """
    if not check_vocabulary(transcribe_client, vocabulary_name):
        create_vocabulary(transcribe_client, vocabulary_name)

def transcribe_audio(s3_client: boto3.client, transcribe_client: boto3.client, bucket_name: str, vocabulary_name: str, file_name: str, timeout: int = 300) -> str:
    """
    Transcribe an audio file using Amazon Transcribe.

    Args:
        s3_client: Boto3 S3 client.
        transcribe_client: Boto3 Transcribe client.
        bucket_name: Name of the S3 bucket.
        vocabulary_name: Name of the vocabulary to use.
        file_name: Name of the file to transcribe.
        timeout: Timeout in seconds to wait for the transcription job to complete.

    Returns:
        str: Transcription text.
    """
    job_name = f"transcription-{int(time.time())}"
    file_uri = f"s3://{bucket_name}/{file_name}"

    logger.info(f"Starting transcription job {job_name} for file {file_name}...")
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": file_uri},
        MediaFormat="wav",
        LanguageCode="en-US",
        Settings={"VocabularyName": vocabulary_name}
    )

    start_time = time.time()
    while True:
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        status = job["TranscriptionJob"]["TranscriptionJobStatus"]
        if status == "COMPLETED":
            transcript_uri = job["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            logger.info(f"Transcription job {job_name} completed successfully.")
            response = requests.get(transcript_uri)
            return response.json()["results"]["transcripts"][0]["transcript"]
        elif status == "FAILED":
            raise Exception("Transcription job failed.")
        if time.time() - start_time > timeout:
            raise Exception(f"Timeout waiting for transcription job {job_name} to complete.")
        time.sleep(5)

class TranscribeCog(commands.Cog):
    def __init__(self, bot: commands.Bot, s3_client: boto3.client, transcribe_client: boto3.client, bucket_name: str, vocabulary_name: str):
        """
        Initialize the bot with required clients and configurations.

        Args:
            bot: the Discord bot to attach to
            intents: Discord intents for the bot.
            s3_client: Boto3 S3 client.
            transcribe_client: Boto3 Transcribe client.
            bucket_name: Name of the S3 bucket.
            vocabulary_name: Name of the vocabulary to use.
        """
        self.bot = bot
        self.audio_buffer = BytesIO()
        self.recording = False
        self.s3_client = s3_client
        self.transcribe_client = transcribe_client
        self.bucket_name = bucket_name
        self.vocabulary_name = vocabulary_name


    def create_vocabulary(self) -> None:
        check_or_create_vocabulary(
            self.transcribe_client,
            self.vocabulary_name)

    async def record_audio(self, voice_client: discord.VoiceClient) -> None:
        """
        Record audio from a voice client (NOT the voice but the media playing).

        Args:
            voice_client: Discord voice client.
        """
        while self.recording:
            pcm_audio = await voice_client.source()  # Receive PCM audio
            self.audio_buffer.write(pcm_audio)  # Append audio to buffer
            await asyncio.sleep(0.1)

    async def save_and_transcribe(self) -> str:
        """
        Save audio to a file and transcribe it.

        Returns:
            str: Transcription text.
        """
        self.audio_buffer.seek(0, os.SEEK_END)
        buffer_size = self.audio_buffer.tell()
        self.audio_buffer.seek(max(0, buffer_size - (6 * 16000 * 2)))  # 6 seconds * 16kHz * 2 bytes/sample

        with wave.open("temp.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(self.audio_buffer.read())

        self.s3_client.upload_file("temp.wav", self.bucket_name, "temp.wav")
        transcription = transcribe_audio(self.s3_client, self.transcribe_client, self.bucket_name, self.vocabulary_name, "temp.wav")
        os.remove("temp.wav")
        return transcription

    @commands.command()
    async def join(self, ctx: commands.Context) -> None:
        """
        Join the voice channel of the command issuer.

        Args:
            ctx: The command context.
        """
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()
            self.recording = True
            asyncio.create_task(self.record_audio(voice_client))

    @commands.command()
    async def leave(self, ctx: commands.Context) -> None:
        """
        Leave the voice channel.

        Args:
            ctx: The command context.
        """
        self.recording = False
        if ctx.voice_client:
            await ctx.voice_client.disconnect()

    @commands.command()
    async def transcribe(self, ctx: commands.Context) -> None:
        """
        Transcribe the recorded audio and send the result.

        Args:
            ctx: The command context.
        """
        transcription = await self.save_and_transcribe()
        await ctx.send(f"Transcription: {transcription}")

    @transcribe.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def run(discord_token: str, s3_bucket_name: str, vocabulary_name: str) -> None:
    """
    Run the bot with the provided configurations.

    Args:
        discord_token: Discord bot token.
        s3_bucket_name: S3 bucket name for storing audio files.
        vocabulary_name: Amazon Transcribe vocabulary name.
    """
    intents = discord.Intents.default()
    intents.guilds = True
    intents.messages = True
    intents.message_content = True

    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or("!"), 
        intents=intents
    )

    transcribe_cog = TranscribeCog(
        bot,
        s3_client=boto3.client("s3", region_name="eu-west-3"),
        transcribe_client=boto3.client("transcribe", region_name="eu-west-3"),
        bucket_name=s3_bucket_name,
        vocabulary_name=vocabulary_name)
    transcribe_cog.create_vocabulary()

    @bot.event
    async def on_ready() -> None:
        """Log when the bot is ready."""
        logger.info(f"Logged in as {bot.user}")

    async def main():
        async with bot:
            await bot.add_cog(transcribe_cog)
            await bot.start(discord_token)

    asyncio.run(main())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the TranscribeBot")
    parser.add_argument("--discord-token", required=True, help="The Discord bot token")
    parser.add_argument("--s3-bucket-name", required=True, help="The S3 bucket name")
    parser.add_argument("--vocabulary-name", required=True, help="The Amazon Transcribe vocabulary name")
    args = parser.parse_args()

    run(args.discord_token, args.s3_bucket_name, args.vocabulary_name)
