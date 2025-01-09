'''
Entrypoint for connecting to discord and managing the communication back and forth.
'''
import base64
import discord

from outbreak.client import UE5RemoteControlClient


class Bot(discord.Client):
    '''
    Connects discord to business logic via handling event callbacks from discord.py.
    '''

    def __init__(self, game_host: str, game_port: int, channel_name: str) -> None:
        intents = discord.Intents.default()
        intents.guilds = True
        intents.messages = True
        intents.message_content = True

        super().__init__(intents=intents)

        self.channel_name = channel_name

        self.backend = UE5RemoteControlClient(
            hostname=game_host,
            port=game_port
        )

    async def on_ready(self) -> None:
        '''
        Callback to do initial setup and gather information on the server connected to.
        '''
        print(f'We have logged in as {self.user}')
        for guild in self.guilds:
            for channel in guild.channels:
                print(f'Guild: {guild} Channel: {channel}')
        await self.backend.connect()

    async def on_message(self, message: discord.Message) -> None:
        '''
        Callback to handle messages sent to the bot.
        '''
        print(message)
        if not message.author == self.user \
                and not message.author.bot \
                and message.channel.type == discord.ChannelType.text \
                and message.channel.name == "bottest":
            direct_response = await message.author.send('Test')

            timeout = 5.0
            response = await self.backend.get_object_thumbnail(object_path="/Game/ParagonBoris/Characters/Heroes/Boris/BorisPlayerCharacter.BorisPlayerCharacter", timeout=timeout)
            with open("thumbnail.png", "wb") as f:
                f.write(base64.b64decode(response["ResponseBody"]))

            embed = discord.Embed(
                title="Misha the Menace", description="Mountain of muscle and fur, his thick, shaggy coat a patchwork of scars from battles long won.", color=discord.Color.blue())
            file = discord.File("./thumbnail.png", filename="image.png")
            embed.set_image(url="attachment://image.png")
            content = """The bear was prowling the meadows, minding its own business, when the player, like a clueless tourist on a bad vacation, wandered too close. The moment their eyes met, it was on. The player bolted for the pond, a desperate sprint fueled by sheer terror, while the bear, clearly unimpressed by the effort, charged after him like a freight train with claws. A gunshot echoed—brave, sure, but about as effective as throwing a pebble at a tank. The bear didn’t even flinch. Within moments, the beast caught up, and with one swift, merciless swipe, the player’s grand escape turned into a final escape."""

            await message.channel.send(content=content, file=file, embed=embed)
