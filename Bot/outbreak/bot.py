"""
Entrypoint for connecting to discord and managing the communication back and forth.
"""
import asyncio
import base64
import datetime
import discord
import json
import logging

from discord.ext import tasks

from outbreak.client import UE5RemoteControlClient, add_uepie_prefix
from outbreak.prompts import RAGPromptGenerator
from outbreak.rag import BedrockRAGClient
from outbreak.models import RAGRequestPayload, Message, MessageContent, GameState, GameContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Bot(discord.Client):
    """
    Connects discord to business logic via handling event callbacks from discord.py.

    TODO: make a cog for UE5 remote and RAG requests
    """

    def __init__(self, game_host: str, game_port: int, channel_name: str) -> None:
        intents = discord.Intents.default()
        intents.guilds = True
        intents.messages = True
        intents.message_content = True
        self.request_running = False

        super().__init__(intents=intents)

        self.channel_name = channel_name

        self.backend = UE5RemoteControlClient(
            hostname=game_host,
            port=game_port
        )

        self.prompt_generator = RAGPromptGenerator()

        self.rag = BedrockRAGClient(region_name="us-east-1")

    @tasks.loop(seconds=30)
    async def periodic_task(self):
        if not self.request_running:
            self.prompt_generator.clear_chat_messages()

            await self.do_some_stuff()


    @periodic_task.before_loop
    async def before_periodic_task(self):
        logger.info("Waiting for the bot to get ready...")
        await self.wait_until_ready()  # Ensures the bot is ready before starting the task

    async def on_ready(self) -> None:
        """
        Callback to do initial setup and gather information on the server connected to.
        """
        logging.info(f"We have logged in as {self.user}")
        for guild in self.guilds:
            for channel in guild.channels:
                print(f"Guild: {guild} Channel: {channel}")
        await self.backend.connect()
        await self.periodic_task.start()

    async def find_available_actions(self):
        # NOTE: disabling due to description not loading well for all the function names
        available_actions = await self.backend.get_remote_preset("SurvivalManagerPreset")

    async def update_latest_game_state(self):
        remote_object_path = add_uepie_prefix("/Game/LBG/Maps/L_LBG_Medow.L_LBG_Medow:PersistentLevel.B_RemoteCaller_C_1")
        ue_response = await self.backend.call_object_function(remote_object_path, "GameState", {})

        if ue_response.ResponseCode == 200:
            self.prompt_generator.clear_contexts()
            game_state = GameState.from_dict(ue_response.ResponseBody)
            for bear_name, location in game_state.BearLocations.items():
                self.prompt_generator.add_context(GameContext(context={"Bear": {"NameOrPath": bear_name, "Location": location}}))

            for location_name in game_state.LocationNames:
                self.prompt_generator.add_context(GameContext(context={"Location": location_name}))

            self.prompt_generator.add_context(GameContext(context={"PlayerLocation": game_state.PlayerLocation}))
            self.prompt_generator.add_context(GameContext(context={"PlayerAmmo": game_state.PlayerAmmo}))
            self.prompt_generator.add_context(GameContext(context={"PlayerGrenades": game_state.PlayerGrenades}))
            self.prompt_generator.add_context(GameContext(context={"PlayerHealth": game_state.PlayerHealth}))
        else:
            logger.error(f"Unable to load game state! {ue_response}")

    async def generate_content_with_thumbnail(self, object_path: str, title: str, image_alt: str):
        timeout = 5.0
        response = await self.backend.get_object_thumbnail(object_path=object_path, timeout=timeout)
        with open("thumbnail.png", "wb") as f:
            f.write(base64.b64decode(response["ResponseBody"]))

        embed = discord.Embed(title=title, description=image_alt, color=discord.Color.blue())
        file = discord.File("./thumbnail.png", filename="image.png")
        embed.set_image(url="attachment://image.png")

        return (file, embed)

    async def do_some_stuff(self):
        self.request_running = True

        await self.find_available_actions()
        await self.update_latest_game_state()

        prompt = self.prompt_generator.generate_prompt()

        model_id = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
        rag_request_payload = RAGRequestPayload(
            anthropic_version="bedrock-2023-05-31",
            max_tokens=2048,
            top_k=250,
            temperature=0.5,
            top_p=0.7,
            messages=[
                Message(
                    role="user",
                    content=[
                        MessageContent(
                            type="text",
                            text=prompt
                        )
                    ]
                )
            ]
        )

        response = self.rag.make_rag_request(model_id=model_id, rag_request_payload=rag_request_payload)
        notes = list()
        for content in response.content:
            if content.type == "text":
                parsed = json.loads(content.text)
                if parsed["Header"]["Notes"]:
                    notes.append(parsed["Header"]["Notes"])

                remote_object_path = add_uepie_prefix("/Game/LBG/Maps/L_LBG_Medow.L_LBG_Medow:PersistentLevel.B_RemoteCaller_C_1")

                for action in parsed["Actions"]:
                    logger.info(action)
                    ue_response = None
                    if action["Name"] == "Chat":
                        self.prompt_generator.add_previous_message(action["Arg1"])
                        ue_response = await self.backend.call_object_function(remote_object_path, "Chat", {"Arg1": action["Arg1"]})
                    elif action["Name"] == "Spawn":
                        ue_response = await self.backend.call_object_function(
                            remote_object_path,
                            "Spawn",
                            {"Arg1": action["Arg1"], "Arg2": action["Arg2"]})
                    elif action["Name"] == "TeleportPlayer":
                        ue_response = await self.backend.call_object_function(
                            remote_object_path,
                            "TeleportPlayer",
                            {"Arg1": action["Arg1"], "Arg2": action["Arg2"]})
                    elif action["Name"] == "MoveTo":
                        ue_response = await self.backend.call_object_function(
                            remote_object_path,
                            "MoveTo",
                            {"Arg1": action["Arg1"], "Arg2": action["Arg2"]})
                    elif action["Name"] == "Wait":
                        wait_time = action["Arg1"]
                        if type(wait_time) is str:
                            wait_time = float(wait_time)

                        await asyncio.sleep(wait_time)
                    
                    if ue_response and not ue_response.ResponseCode == 200:
                        logger.error(f"Failed to call function in UE: {ue_response}")
                        notes.append(ue_response)



        self.request_running = False
        return notes

    async def on_message(self, message: discord.Message) -> None:
        """
        Callback to handle messages sent to the bot.
        """
        if not message.author == self.user \
                and not message.author.bot \
                and message.channel.type == discord.ChannelType.text \
                and message.channel.name == "bottest":

            self.prompt_generator.add_chat_message(message.clean_content, message.created_at)
            notes = await self.do_some_stuff()

            if notes:
                await message.channel.send(" ".join(notes))
