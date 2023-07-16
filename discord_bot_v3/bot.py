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
async def jarrod(ctx, name: str = None):
    await ctx.respond("A cool guy who will always have your back. Jarrod's are nice, funny, and fun to be around. Jarrod's tend to be the friend to the chicks, usually not by choice, but when the chicks realize all other guys are dipshits, they come back to the Jarrod, usually because they always treated them right and they have a nice penis. Jarrod's can keep up with any conversation and are usually well rounded in terms of music taste and movie knowledge. Almost always a jack of all trades, they will try anything and generally be successful at whatever they try. For example, Jarrods may not be the all-state quarterback, but they will make all region at whatever position they play. They may not be the unholy manifestation of skills at Modern Warefare, but they'll play well with a good kill/death ratio. Jarrod's usually dont like to fight, but if the shit goes down a Jarrod will punch faces like a coked out Chuck Norris in the middle of a ninja convention. Overall, Jarrod's are good to have around. They won't let you down")


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
    await ctx.respond(f"{ctx.author.display_name} has instructed iBot to play {soundSelection}! 🎵 🔊")


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
async def on_message(self, message: discord.Message):
    if message.author == self.user:
        return
    logger.info(f"{message.author.display_name} said {message.content}")


@bot.event
async def on_presence_update(self, before: discord.Member, after: discord.Member):
    logger.info(f"Before status: {before.status.value}")
    logger.info(f"Before activity: {before.activity}")
    logger.info(f"After status: {after.status.value}")
    logger.info(f"After activity: {after.activity}")


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    logger.info(f"{member.display_name} voice state update")
    logger.info(f"Before: {before}")
    logger.info(f"After: {after.channel}")


@bot.event
async def on_ready():
    logger.info("Bot is ready")


bot.run(getenv("TOKEN"))
