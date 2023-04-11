import logging
import discord
import dotenv
from discord.commands import Option
from os import getenv, listdir
from os.path import isfile, join
from typing import List

logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/bot.log", "a"), logging.StreamHandler()],
)
dotenv.load_dotenv("config/.env")
logger = logging.getLogger(__name__)

# Load sound options into list
soundFileNames: List[str] = []
soundOpts: List[List[str]] = []
for file in listdir("resources"):
    if isfile(join("resources/", file)):
        if len(soundFileNames) < 25:
            soundFileNames.append(file[:-4])
        else:
            soundOpts.append(soundFileNames.copy())
            soundFileNames.clear()
soundOpts.append(soundFileNames)
logger.info(f"soundOpts: {soundOpts}")

bot = discord.AutoShardedBot(intents=discord.Intents.all())
logger.info("Starting bot")


@bot.slash_command()
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")


@bot.slash_command()
async def sound(
    ctx: discord.ApplicationContext,
    selection: Option(str, "Sound to be played", choices=soundOpts[0], required=True),
):
    await playAudio(ctx, selection)


@bot.slash_command()
async def sound_ext(
    ctx: discord.ApplicationContext,
    selection: Option(str, "Sound to be played", choices=soundOpts[1], required=True),
):
    await playAudio(ctx, selection)


async def playAudio(ctx: discord.ApplicationContext, soundSelection: str):
    vc = ctx.voice_client
    if not vc:
        vc = await ctx.author.voice.channel.connect()

    if ctx.author.voice.channel.id != vc.channel.id:
        return await ctx.respond("You must be in the same voice channel as the bot")

    logger.info(f"{ctx.author.display_name} has chosen to play {soundSelection}")
    vc.play(
        discord.FFmpegPCMAudio(
            source=f"C:/Users/Zach/Code/Python/discord-bot-v3/resources/{soundSelection}.mp3"
        )
    )
    await ctx.respond(f"{ctx.author.display_name} has instructed iBot to play {soundSelection}!")
    await vc.disconnect()


@bot.slash_command()
async def shutup(ctx: discord.ApplicationContext):
    vc = ctx.voice_client
    if not vc:
        vc = await ctx.author.voice.channel.connect()

    if ctx.author.voice.channel.id != vc.channel.id:
        return await ctx.respond("You must be in the same voice channel as the bot")

    logger.info(f"VC is connected? {vc.is_connected()}")
    await vc.disconnect(force=True)
    await ctx.respond(f"{ctx.author.display_name} has told iBot to shut up 😔")


@bot.event
async def on_ready():
    logger.info("Bot is ready")


bot.run(getenv("TOKEN"))
