import time

from utils.config import Config
from processes.key import Key
from processes.move import Move
from shapes.window import Window

class Taming:

    def __init__(self):
        self.config = Config()
        self.config.enable()
        self.roundFrequency = 30
        self.window = Window()
        self.roundStart = self.window.center()
        self.rountEnd = self.roundStart[0] + 100, self.roundStart[1]

    def run(self):
        startTime = time.time()

        while self.config.isWorks():
            Key('2').press()
            time.sleep(3)
            Key('1').press()
            time.sleep(13)
            currentTime = time.time()
            if startTime + self.roundFrequency < currentTime:
                startTime = currentTime
                Move().fromTo(self.roundStart, self.rountEnd)