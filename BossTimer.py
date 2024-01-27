import time
from Boss.py import Boss

class BossTimer:
    def __init__(self):
        self.bosses=[]

    def textWall():
        text = ""
        for boss in bosses:
            text += (boss.name + "\t<c:".boss.last_reset_time+60*boss.time+":R> \t"+boss.command+"\n")
        return  text
    
    def addBoss(boss_name, command, time):
        bosses.append(Boss(boss_name, command, time, int(time.time())))

    def resetTime(boss_command):
        for boss in bosses:
            if boss.command == boss_command:
                boss.last_reset_time = int(time.time())
        