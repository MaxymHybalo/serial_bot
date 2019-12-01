import math

from processes.move import Move
from processes.wait import Wait

from shapes.window import Window
from shapes.rect import Rect

from jobs.helpers.navigator import get_guild_and_npc

OBSERVE_Y = 0
OBSERVE_Y_INV = 1
OBSERVE_X = 2
OBSERVE_X_INV = 3
DELTA = 3
OBSERVE_DELAY = 0.05

# start point camera position reqiuirement
CAMERA_HEIGHT = 300
ANGLE_WIDTH = 20

def observe_height():
    titleRoi, guildRoi = get_guild_and_npc()
    height = camera_height(titleRoi, guildRoi)
    if height > CAMERA_HEIGHT:
        return None
    return CAMERA_HEIGHT - height

def observe_angle():
    titleRoi, guildRoi = get_guild_and_npc()
    width = camera_angle_width(titleRoi, guildRoi)
    if abs(width) <= ANGLE_WIDTH:
        return None
    return width

def camera_height(npc, guild):
    npcC, gC = _centers(npc, guild)
    return gC[1] - npcC[1]

def camera_angle_width(npc, guild):
    npcC, gC = _centers(npc, guild)
    return npcC[0] - gC[0]

def _centers(rect1, rect2):
    c1 = Rect(rect1).center()
    c2 = Rect(rect2).center()
    return c1, c2

class Observer:

    def __init__(self, xChecker, yChecker):
        self.move = Move()
        self.xChecker = xChecker
        self.yChecker = yChecker
        self.window = Window().center()


    def observe(self):
        xCheck = self.xChecker()
        yCheck = self.yChecker()
        if yCheck:
            self.direction = OBSERVE_Y
            self.round(yCheck, self.yChecker)
        if xCheck:
            self.direction = OBSERVE_X if xCheck > 0 else OBSERVE_X_INV
            self.round(xCheck, self.xChecker)

    def round(self, initial, checker):
        x, y = self.window
        dx, dy = x, y
        self.move.moveTo(x,y)
        self.move.pressRight()
        check = abs(initial)
        while check is not None:
            speed = math.floor(int(check / 10))
            if speed == 0:
                speed = 1
            for i in range(speed):
                self.move.move(self._apply_direction())
                Wait(OBSERVE_DELAY).delay()
            check = checker()
            check = abs(check) if check is not None else None
        self.move.releaseRight()

    def _apply_direction(self):
        if self.direction is OBSERVE_Y:
            return 'Y'
        elif self.direction is OBSERVE_Y_INV:
            return 'U'
        elif self.direction is OBSERVE_X:
            return 'X'
        elif self.direction is OBSERVE_X_INV:
            return 'Z'
        else: None