import logging
import discord
import dotenv
from discord.commands import Option
from os import getenv


logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/bot.log", "a"), logging.StreamHandler()],
)
dotenv.load_dotenv("config/.env")
logger = logging.getLogger(__name__)
bot = discord.AutoShardedBot(intents=discord.Intents.all())
logger.info("Starting bot")


@bot.slash_command()
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")


@bot.slash_command()
async def sound(
    ctx,
    opt: Option(
        str, "Sound to be played", choices=["Crab Rave", "Duck Song"], required=True
    ),
):
    vc = ctx.voice_client
    if not vc:
        vc = await ctx.author.voice.channel.connect()

    if ctx.author.voice.channel.id != vc.channel.id:
        return await ctx.respond("You must be in the same voice channel as the bot")

    # TODO: Select audio source based on opt parameter
    vc.play(
        discord.FFmpegPCMAudio(
            source="C:/Users/Zach/Code/Python/discord-bot-v3/resources/crab_rave.mp3"
        )
    )
    await ctx.message.delete()


@bot.event
async def on_ready():
    logger.info("Bot is ready")


bot.run(getenv("TOKEN"))
