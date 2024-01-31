class Boss:

  def __init__(self, name, command, time, respawn_time):
    self.name = name
    self.command = command
    self.time = time
    self.respawn_time = respawn_time
    self.reminded = False
