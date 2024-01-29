import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from BossTimer import BossTimer

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
channel = 0
guild = 0
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
boss_timer = BossTimer()

@bot.event
async def on_ready():
    print('Bot jest gotowy!')

@bot.event
async def on_message(ctx):
    global channel
    global guild
    if ctx.channel == channel and ctx.author != bot.user:
        await ctx.delete()
    elif ctx.guild == guild and ctx.channel.name == 'world-boss-spawn-log':
        boss_command = ctx.content.replace(" ", "").lower()  # Usunięcie spacji
        for boss in boss_timer.bosses:
            if boss.command in boss_command:
                boss_timer.resetTime(boss_command)
                await display_boss_time(ctx)
                break
    else:
        await bot.process_commands(ctx)

@bot.command(name='init')
async def init_bot(ctx):
    global channel
    global guild
    channel = discord.utils.get(ctx.guild.channels, name='bosstimer-by-o120d6')
    guild = ctx.guild
    if channel:
        await clear_channel(channel)
    else:
        channel = await ctx.guild.create_text_channel('bosstimer-by-o120d6')
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)  # Ustawienie uprawnień
    await channel.send(f"Inicjalizacja pomyślna na kanale {channel.name}")

async def clear_channel(channel):
    async for message in channel.history():
        await message.delete()

@bot.command(name='reset', help='Użycie: !reset chimera')
async def reset_boss(ctx, boss_command: str):
    for boss in boss_timer.bosses:
        if boss.command == boss_command:
            boss_timer.resetTime(boss_command)
            await ctx.send(f"Czas bossa {boss.name} został zresetowany.")
            await display_boss_time()

@bot.command(name='resetall', help='Użycie: !resetall')
async def resetall_boss(ctx):
  for boss in boss_timer.bosses:
    boss_timer.resetTime(boss.command)
  await display_boss_time(ctx.channel)

@bot.command(name='addBoss', help='Użycie: !addBoss Bigchimera chimera timetoresetinminutes')
async def add_boss(ctx, boss_name: str, boss_command: str, boss_time: int):
    boss_timer.addBoss(boss_name, boss_command, boss_time)
    await ctx.send(f"Dodano nowego bossa: {boss_name.lower()}")

@bot.command(name='display')
async def display_boss_time(ctx):
    global channel
    if channel:
        async for message in channel.history(limit=1):
            try:
                await message.delete()
            except discord.errors.Forbidden:
                pass
        await channel.send(boss_timer.textWall())
    else:
        print(f"Nie znaleziono kanału.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Nieznana komenda!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Brakujący argument!")
    else:
        await ctx.send(f"Wystąpił błąd: {error}")

@bot.command(name='deleteBoss', help='Użycie: !deleteBoss boss_name')
async def delete_boss(ctx, boss_name: str):
    for boss in boss_timer.bosses:
        if boss.command.lower() == boss_name.lower():
            boss_timer.bosses.remove(boss)
            await ctx.send(f"Usunięto bossa: {boss_name}")
            await display_boss_time(ctx.channel)
            return
    await ctx.send(f"Nie znaleziono bossa o nazwie: {boss_name}")

@bot.command(name='hhelp')
async def delete_boss(ctx):
  await ctx.send("addBoss a a 1, deleteBoss a,reset a, display, resetall")

bot.run(TOKEN)