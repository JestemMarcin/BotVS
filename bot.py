# bot.py
import os
from discord.utils import get
import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
boss_tab={}
bot = commands.Bot(command_prefix = '!',intents=discord.Intents.all())

boss_tab['a']=21
@bot.command(name='init')
async def initBot(ctx):
    guild = ctx.message.guild
    channel_exist = False
    for channel in guild.channels:
        print(channel.name)
        if channel.name == 'world-boss-spawn-log': 
            channel_exist = True
    if channel_exist:
        CHANNEL_MAIN = channel
        await channel.send("inicjalizacja pomyślna")
    else:
        CHANNEL_MAIN = await guild.create_text_channel('world-boss-spawn-log')

@bot.command(name='adboss')
async def adBoss(ctx, boss_name: str, boss_time: int):
    boss_tab[boss_name] = boss_time

@bot.event
async def on_message(ctx):
    if ctx.channel.name == 'world-boss-spawn-log':
       print(ctx.content)
    for name in boss_tab:
        if name in ctx.content:
            content_string = (ctx.content+"bb")
            #await ctx.edit(content=content_string)
    print(boss_tab)



bot.run(TOKEN)