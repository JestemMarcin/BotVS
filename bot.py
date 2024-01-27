import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from BossTimer import BossTimer

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
boss_timer = BossTimer()

@bot.event
async def on_ready():
    print('Bot jest gotowy!')

@bot.event
async def on_message(message):
    if message.channel.name == 'bosstimer-by-o120d6':
        if message.author != bot.user and message.content.startswith('!'):
            await message.delete()
        else:
            await bot.process_commands(message)
    else:
        await bot.process_commands(message)

@bot.command(name='init')
async def init_bot(ctx):
    channel_name = 'bosstimer-by-o120d6'
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    if channel:
        await clear_channel(channel)
    else:
        channel = await ctx.guild.create_text_channel(channel_name)
        await channel.send(f"Inicjalizacja pomyślna na kanale {channel_name}")
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)  # Ustawienie uprawnień

async def clear_channel(channel):
    async for message in channel.history():
        await message.delete()

@bot.command(name='reset', help='Użycie: !reset chimera')
async def reset_boss(ctx, boss_command: str):
    for boss in boss_timer.bosses:
        if boss.command == boss_command:
            boss_timer.resetTime(boss_command)
            await ctx.send(f"Czas bossa {boss.name} został zresetowany.")

@bot.command(name='addBoss', help='Użycie: !addBoss Bigchimera chimera timetoresetinminutes')
async def add_boss(ctx, boss_name: str, boss_command: str, boss_time: int):
    boss_timer.addBoss(boss_name, boss_command, boss_time)
    await ctx.send(f"Dodano nowego bossa: {boss_name}")

@bot.command(name='display')
async def display_boss_time(ctx):
    channel_name = 'bosstimer-by-o120d6'
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    if channel:
        async for message in channel.history(limit=1):
            try:
                await message.delete()
            except discord.errors.Forbidden:
                pass
        await channel.send(boss_timer.textWall())
    else:
        await ctx.send(f"Nie znaleziono kanału o nazwie {channel_name}.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Nieznana komenda!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Brakujący argument!")
    else:
        await ctx.send(f"Wystąpił błąd: {error}")

bot.run(TOKEN)