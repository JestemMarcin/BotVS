import time
from Boss import Boss


class BossTimer:

  def __init__(self):
    self.bosses = []
    self.ctime = 3  #time correction in minutes
    self.time_to_remind = 10  #time to remind in minutes

  def setCtime(self, correction_time: int):
    self.ctime = correction_time

  def set_time_to_remind(self, remind_time: int):
    self.time_to_remind = remind_time

  def textWall(self):
    text = ""
    for boss in self.bosses:
      text += (boss.name + "\t<t:" + str(boss.respawn_time) + ":R> \t" +
               boss.command + "\n")
    return text

  def addBoss(self, boss_name, command, time_to_reset):
    self.bosses.append(Boss(boss_name, command, time_to_reset, 0))

  def resetTime(self, boss_command):
    for boss in self.bosses:
      if boss.command == boss_command:
        boss.respawn_time = int(time.time() - self.ctime * 60) + 60 * boss.time
        boss.reminded = False

  async def check_remaining_time(self, reminder_sender):
    for boss in self.bosses:
      if not boss.reminded:
        remaining_time_seconds = boss.respawn_time - time.time()
        if remaining_time_seconds <= 0:
          boss.reminded = True
          await reminder_sender.send_reminders(boss.name, "Boss respawned!")
        else:
          remaining_time_minutes = int(remaining_time_seconds / 60)
          if remaining_time_minutes <= self.time_to_remind:
            boss.reminded = True
            await reminder_sender.send_reminders(boss.name,
                                                 str(remaining_time_minutes))
