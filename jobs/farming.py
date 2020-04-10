import time
from utils.config import Config
from processes.key import Key
from processes.move import Move
from processes.wait import Wait
from shapes.window import Window

class Farming:
    # TODO invistigate asyncio
    frequences = [
        2,
        0.3,
        0.3,
        15,
        15,
        40,
        40,
        40,
        5
    ]

    action_params = [
        '1',
        ['c', '6'],
        ['c', '7'],
        ['s', '2'],
        ['s', '3'],
        ['a', '5'], # alt + 1
        ['a', '4'],
        ['a', '1'],
        '_'
    ]

    # frequences = [
    #     0.5,

    #     2
    # ]
    # action_params = [
    #     '1',
    #     '_'
    # ]

    def __init__(self, actions, timings):
        print(actions, timings)
        self.action_params = actions
        self.frequences = timings
        self.config = Config()
        self.config.enable()
        self.roundFrequency = 10
        
        self.generate_actions()
        self.window = Window()
        self.roundStart = self.window.center()
        self.rountEnd =  self.roundStart[0] + 100, self.roundStart[1]

    def run(self):
        startTime = time.time()
        while self.config.isWorks():
            # print('[While iteration]')
            for i, a in enumerate(self.actions):
                itime = time.time()
                if itime > self.skills_state[i]:
                    f = getattr(self, a)
                    f(self.action_params[i])
                    print(a, self.frequences[i])
                    self.skills_state[i] = itime + self.frequences[i]
    
    def init_actions_time(self):
        itime = time.time()
        for a in range(len(self.actions)):
            self.skills_state[a] = itime
    
    def generate_actions(self):
        self.actions = ['key'] * (len(self.action_params) - 1)
        self.actions.append('turn')
        self.skills_state = [0] * len(self.frequences)
        self.init_actions_time()

    def key(self, params):
        if type(params) == list:
            print('list key call')
            Key(params[1], pressed=params[0]).combination()

        else:
            Key(params).press()
        Wait(0.4).delay()

    def turn(self, _):
        print('turn')
        Move().fromTo(self.roundStart, self.rountEnd)
        return None
