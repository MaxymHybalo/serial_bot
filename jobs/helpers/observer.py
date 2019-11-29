import math
from processes.move import Move
from processes.wait import Wait
from shapes.window import Window

OBSERVE_Y = 0
OBSERVE_Y_INV = 1
OBSERVE_X = 2
OBSERVE_Y_INV = 3
DELTA = 3
OBSERVE_DELAY = 0.05

class Observer:

    def __init__(self, checker, direction=0):
        self.move = Move()
        self.direction = direction
        self.checker = checker
        self.window = Window().center()


    def observe(self, navigate=None):
        x, y = self.window
        dx, dy = x, y
        self.move.moveTo(x,y)
        self.move.pressRight()
        check = self.checker()
        while check is not None:
            speed = math.floor(int(check / 10))
            if speed == 0:
                speed = 1

            for i in range(speed):
                self.move.move(self._apply_direction())
                Wait(OBSERVE_DELAY).delay()
            check = self.checker()
        self.move.releaseRight()


    def _apply_direction(self):
        if self.direction is OBSERVE_Y:
            return 'Y'
        elif self.direction is OBSERVE_Y_INV:
            return 'U'
        elif self.direction is OBSERVE_X:
            return 'X'
        else:
            return 'Z'