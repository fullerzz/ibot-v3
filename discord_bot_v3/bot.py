import logging
import discord
import dotenv
from os import getenv
from time import sleep


logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot.log", "a"), logging.StreamHandler()],
)
dotenv.load_dotenv("config/.env")
logger = logging.getLogger(__name__)
bot = discord.Bot(intents=discord.Intents.all())
logger.info("Starting bot")


@bot.slash_command()
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")


@bot.user_command(name="Say Hello")
async def hi(ctx, user):
    await ctx.respond(f"{ctx.author.mention} says hello to {user.name}!")


sounds = bot.create_group("sounds", "Play sound in voice channel")


@sounds.command()
async def crab_rave(ctx):
    vc = ctx.voice_client

    if not vc:
        vc = await ctx.author.voice.channel.connect()

    if ctx.author.voice.channel.id != vc.channel.id:
        return await ctx.respond("You must be in the same voice channel as the bot")

    vc.play(
        discord.FFmpegPCMAudio(
            source="C:/Users/Zach/Code/Python/discord-bot-v3/resources/crab_rave.mp3"
        )
    )

    await ctx.message.delete()


@sounds.command()
async def duck_song(ctx):
    vc = ctx.voice_client

    if not vc:
        vc = await ctx.author.voice.channel.connect()

    if ctx.author.voice.channel.id != vc.channel.id:
        return await ctx.respond("You must be in the same voice channel as the bot")

    vc.play(
        discord.FFmpegPCMAudio(
            source="C:/Users/Zach/Code/Python/discord-bot-v3/resources/duck_song.mp3"
        )
    )

    await ctx.message.delete()


@bot.event
async def on_ready():
    logger.info("Bot is ready")


bot.run(getenv("TOKEN"))
