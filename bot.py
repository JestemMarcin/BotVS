# bot.py
import os
from discord.utils import get
import discord
from dotenv import load_dotenv
from discord.ext import commands
from BossTimer import BossTimer
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_MAIN = False
MESSAGE_MAIN = False
bot = commands.Bot(command_prefix = '!',intents=discord.Intents.all())
boss_timer = BossTimer()

@bot.event
async def on_message(message):
    if CHANNEL_MAIN != False:
    if message.channel == CHANNEL_MAIN:
    
        if not message.author.bot and not message.content.startswith('!'):
            await message.delete()

    await bot.process_commands(message)

@bot.command(name='chimera')
async def resetTime(ctx):
    print(ctx)
    response = "s"
    await ctx.send(response)

@bot.command(name='init')
async def initBot(ctx):
    global CHANNEL_MAIN
    guild = ctx.message.guild
    for channel in guild.channels:
        print(channel.name)
        if channel.name == 'bosstimer-by-o120d6': 
            CHANNEL_MAIN = channel
    if CHANNEL_MAIN == False:
        CHANNEL_MAIN = await guild.create_text_channel('bosstimer-by-o120d6')
        await CHANNEL_MAIN.send("inicjalizacja pomyślna "+CHANNEL_MAIN.name)
    else:
        await CHANNEL_MAIN.send("inicjalizacja pomyślna "+CHANNEL_MAIN.name)

@bot.command(name='reset', help='Use it like that "reset chimera"')
async def resetBoss(ctx, boss_command: str):
    boss_timer.resetTime(boss_command)

@bot.command(name='addBoss', help='Use it like that "add Bigchimera chimera timetoresetinminutes"')
async def addBoss(ctx, boss_name: str, boss_command: str, boss_time: int):
    
    boss_timer.addBoss(boss_name, boss_command, boss_time)

@bot.command(name="display")
async def displayBossTime(ctx):
    global CHANNEL_MAIN
    global MESSAGE_MAIN
    if MESSAGE_MAIN == False:
        async for message in CHANNEL_MAIN.history(limit=1):
            MESSAGE_MAIN = message
            break

    await MESSAGE_MAIN.edit(content = boss_timer.textWall())

# Cog error handler
async def cog_command_error(self, ctx, error):
    await ctx.send(f"An error occurred in the Test cog: {error}")


bot.run(TOKEN)