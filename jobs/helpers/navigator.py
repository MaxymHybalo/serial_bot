from processes.click import Click
from shapes.window import Window
from utils.cv2_utils import screenshot
from jobs.helpers.extruder import Extruder, CharTitleConfig, GuildIconConfig, StartPointConfig
from processes.wait import Wait
from processes.move import Move
from shapes.rect import Rect

Y_OFFSET_FROM_START_POSITION = 70
TURN_AROUND_DISTANCE = 500

window = Window()

class Navigator:

    @staticmethod
    def move_to_npc(npc_roi):
        npc_x, npc_y = circus_npc_point(npc_roi)
        wx, wy = Window().position()
        Click(wx + npc_x - 40, wy + npc_y, process='dclick').make_click()

    @staticmethod
    def click_at_npc(npc_roi):
        npc_x, npc_y = circus_npc_point(npc_roi)
        wx, wy = Window().position()
        Click(wx + npc_x, wy + npc_y - int(Y_OFFSET_FROM_START_POSITION / 2), process='dclick').make_click()
    
    @staticmethod
    def touch_circus_npc():
        title = get_tempalate_roi(CharTitleConfig)
        Navigator.move_to_npc(title)
        Wait(3).delay()
        title, guild = get_guild_and_npc()
        while not is_near_npc(title, guild):
            title, guild = get_guild_and_npc()
            print(title, guild)
            Wait(1).delay()
        title, guild = get_guild_and_npc()
        Navigator.click_at_npc(title)
        return title

    @staticmethod
    def turn_around(start):
        wx, wy = Window().position()
        x, y, _, _ = start
        Move().fromTo((wx + x, wy + y), (wx + x + TURN_AROUND_DISTANCE, wy + y))

    @staticmethod
    def go_to_start():
        start = get_tempalate_roi(StartPointConfig)
        x, y = window.relative(start_point(start))
        Click(x,y).make_click()
        return start
    
    @staticmethod
    def drag_camera(start, end):
        x,y = window.position()
        sx, sy = start
        ex, ey = end
        Move().fromTo((x + sx, y + sy), (x + ex, y + ey))


def get_guild_and_npc():
    rect = window.rect
    image = screenshot(rect)
    titleCenter = get_tempalate_roi(CharTitleConfig, image)
    guildCenter = get_tempalate_roi(GuildIconConfig, image)
    return titleCenter, guildCenter

def get_tempalate_roi(config, image=None):
    rect = Window().rect
    if not image:
        image = screenshot(rect)

    extruder = Extruder(image)
    
    # roi = extruder.get_template_rect(config)
    # import cv2
    # from utils.cv2_utils import show_image
    # import numpy as np
    # rected = np.array(image)
    # rected = cv2.cvtColor(rected, cv2.COLOR_RGB2BGR)
    # rected = cv2.rectangle(rected, roi[:2], (roi[0] + roi[2], roi[1] + roi[3]), 255,2)
    # show_image(rected)
    
    return extruder.get_template_rect(config)
    
def distance(point1, point2):
    import math
    x1,y1 = point1
    x2, y2 = point2
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def is_near_npc(npc, guild, near=120):
    # accept 2 rects
    npc = Rect(npc).center()
    guild = Rect(guild).center()
    d = distance(npc, guild)
    print('distance', d)
    return d <= near

def circus_npc_point(roi):
    x,y,w,h = roi
    center = int(x + w/2)
    return (center, y + h + Y_OFFSET_FROM_START_POSITION)

def start_point(roi):
    x, y, w, h = roi
    right = x + w
    middle =  int(y + h / 2)
    return (right, middle)