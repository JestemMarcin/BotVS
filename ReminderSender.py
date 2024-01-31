class ReminderSender:

  def __init__(self):
    self.user_list = []

  async def add_user(self, user_ctx):
    self.user_list.append(user_ctx)
    await user_ctx.send("Added to reminder list.")

  async def send_reminders(self, boss_name, remaining_time):
    for user in self.user_list:
      await user.send(boss_name+": "+ str(remaining_time) +
                      " minutes remaining till respawn.")

  async def remove_user(self, user_ctx):
    self.user_list.remove(user_ctx)
    await user_ctx.send("Removed from reminder list.")
