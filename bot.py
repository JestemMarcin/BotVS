import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from BossTimer import BossTimer
import asyncio
from ReminderSender import ReminderSender

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
boss_timer = BossTimer()
reminder_sender = ReminderSender()
MESSAGE = None


@bot.event
async def on_ready():
  print('Bot jest gotowy!')


@bot.command(name='set_ctime',
             help='Correction time in minutes to boss respawn')
async def set_ctime(ctx, correction_time: str):
  boss_timer.setCtime(int(correction_time))


@bot.command(name='set_rtime', help='Time to remind via pw')
async def set_rtime(ctx, remind_time: str):
  boss_timer.set_time_to_remind(int(remind_time))


@bot.command(name='init')
async def init_bot(ctx):
  global MESSAGE
  channel = discord.utils.get(ctx.guild.channels, name='bosstimer-by-o120d6')
  if channel:
    await clear_channel(channel)
  else:
    channel = await ctx.guild.create_text_channel('bosstimer-by-o120d6')
    await channel.set_permissions(ctx.guild.default_role,
                                  send_messages=False)  # Ustawienie uprawnień
  MESSAGE = await channel.send(
      f"Initialization successful on channel {channel.name}")


async def clear_channel(channel):
  async for message in channel.history():
    await message.delete()


@bot.command(name='reset', help='!reset bossname')
async def reset_boss(ctx, boss_command: str):
  for boss in boss_timer.bosses:
    if boss.command == boss_command:
      boss_timer.resetTime(boss_command)
      await ctx.send(f"{boss.name} time has been reset.")
      await display_boss_time(ctx)


@bot.command(name='resetall', help='!resetall')
async def resetall_boss(ctx):
  for boss in boss_timer.bosses:
    boss_timer.resetTime(boss.command)
  await display_boss_time(ctx)


@bot.command(
    name='addBoss',
    help='!addBoss Boss_description boss_name time_to_reset_in_minutes')
async def add_boss(ctx, boss_name: str, boss_command: str, boss_time: int):
  boss_timer.addBoss(boss_name, boss_command, boss_time)
  await ctx.send(f"Dodano nowego bossa: {boss_name.lower()}")


@bot.command(name='display')
async def display_boss_time(ctx):
  global MESSAGE
  await MESSAGE.edit(content=boss_timer.textWall() +
                     "\nCorrection time set to: " + str(boss_timer.ctime) +
                     " minutes\nReminder time set to: " +
                     str(boss_timer.time_to_remind) + " minutes")


@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send("Don't know that command.")
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Missing argument.")
  else:
    await ctx.send(f"Error: {error}")


@bot.command(name='deleteBoss', help='!deleteBoss boss_name')
async def delete_boss(ctx, boss_name: str):
  for boss in boss_timer.bosses:
    if boss.command.lower() == boss_name.lower():
      boss_timer.bosses.remove(boss)
      await ctx.send(f"Deleted boss: {boss_name}")
      await display_boss_time(ctx)
  await ctx.send(f"There is no boss named: {boss_name}")


@bot.command(name='addReminders', help='!addReminders')
async def add_reminders(ctx):
  await reminder_sender.add_user(ctx.author)


@bot.command(name='removeReminders', help='!removeReminders')
async def remove_reminders(ctx):
  await reminder_sender.remove_user(ctx.author)


async def time_loop():
  while True:
    print("loop1")
    await boss_timer.check_remaining_time(reminder_sender)
    #await reminder_sender.send_reminders("boss name", 99)
    print("loop")
    await asyncio.sleep(40)


async def main():
  task = asyncio.create_task(time_loop())
  await asyncio.gather(bot.start(TOKEN), task)


if __name__ == "__main__":
  asyncio.run(main())
