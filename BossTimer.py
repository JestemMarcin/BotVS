import time
from Boss import Boss

class BossTimer:
    def __init__(self):
        self.bosses=[]

    def textWall(self):
        text = ""
        for boss in self.bosses:
            text += (boss.name + "\t<t:"+str(boss.last_reset_time+60*boss.time)+":R> \t"+boss.command+"\n")
        return text
    
    def addBoss(self, boss_name, command, time_to_reset):
        self.bosses.append(Boss(boss_name, command, time_to_reset, 0))

    def resetTime(self, boss_command):
        for boss in self.bosses:
            if boss.command == boss_command:
                boss.last_reset_time = int(time.time())
        