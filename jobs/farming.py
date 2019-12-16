import time
from utils.config import Config
from processes.key import Key
from processes.move import Move
from shapes.window import Window

class Farming:
    # TODO invistigate asyncio

    actions = {
        'one': 2.4,
        'two': 0.4,
        'three': 0.4,
        'four': 80,
        'turn': 6
    }

    actionsState = {
        'one': 0,
        'two': 0,
        'three': 0,
        'four': 0,
        'turn': 0
    }

    def __init__(self):
        self.config = Config()
        self.config.enable()
        self.roundFrequency = 10
        self.actionsState = self.init_actions_time(self.actionsState)

        # self.window = Window()
        # self.roundStart = self.window.center()
        # self.rountEnd =  self.roundStart[0] + 100, self.roundStart[1]

    def run(self):
        startTime = time.time()
        while self.config.isWorks():
            print('[While iteration]')
            for a in self.actionsState:
                itime = time.time()
                if itime > self.actionsState[a]:
                    f = getattr(self, a)
                    f()
                    self.actionsState[a] = itime + self.actions[a]
    
    def init_actions_time(self, actions):
        itime = time.time()
        for a in actions:
            actions[a] = itime
        return actions

    def one(self):
        print('1')
        Key('1').press()
        return None

    def two(self):
        print('2')
        Key('2').press()
        return None

    def three(self):
        print('3')
        Key('3').press()
        return None

    def four(self):
        print('4')
        Key('4').press()
        return None

    def turn(self):
        print('turn')
        # Move().fromTo(self.roundStart, self.rountEnd)
        return None
