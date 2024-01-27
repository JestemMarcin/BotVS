# bot.py
import os
from discord.utils import get
import discord
from dotenv import load_dotenv
from discord.ext import commands
from BossTimer.py import BossTimer

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = '!',intents=discord.Intents.all())
boss_timer = BossTimer()

@bot.command(name='chimera')
async def resetTime(ctx):
    print(ctx)
    response = "s"
    await ctx.send(response)

@bot.command(name='init')
async def initBot(ctx):
    guild = ctx.message.guild
    channel_exist = False
    for channel in guild.channels:
        print(channel.name)
        if channel.name == 'bosstimer-by-o120d6': 
            channel_exist = True
    if channel_exist:
        CHANNEL_MAIN = channel
        channel.send("inicjalizacja pomyślna")
    else:
        CHANNEL_MAIN = await guild.create_text_channel('bosstimer-by-o120d6')

@bot.command(name='reset', help='Use it like that "reset chimera"')
async def resetBoss(ctx, boss_command: str):
    boss_timer.resetTime(boss_command)

@bot.command(name='addBoss', help='Use it like that "add chimera timetoresetinminutes"')
async def addBoss(ctx, boss_command: str, ):
    boss_timer.addBoss(boss_command)

@bot.command(name="display")
async def displayBossTime(ctx, boss_command: str):
    CHANNEL_MAIN.edit(0,boss_timer.textWall())


bot.run(TOKEN)