from processes.click import Click
from shapes.window import Window
from utils.cv2_utils import screenshot
from jobs.helpers.extruder import Extruder, CharTitleConfig, GuildIconConfig
from processes.wait import Wait
from processes.move import Move
from shapes.rect import Rect

Y_OFFSET_FROM_START_POSITION = 70
TURN_AROUND_DISTANCE = 500

class Navigator:

    @staticmethod
    def move_to_npc(npc_roi):
        npc_x, npc_y = calc_nav_point(npc_roi)
        wx, wy = Window().position()
        Click(wx + npc_x - 40, wy + npc_y, process='dclick').make_click()

    @staticmethod
    def click_at_npc(npc_roi):
        npc_x, npc_y = calc_nav_point(npc_roi)
        wx, wy = Window().position()
        Click(wx + npc_x, wy + npc_y - int(Y_OFFSET_FROM_START_POSITION / 2), process='dclick').make_click()
    
    @staticmethod
    def touch_circus_npc():
        rect = Window().rect
        image = screenshot(rect)
        extruder = Extruder(image)
        title = extruder.get_template_rect(CharTitleConfig)
        Navigator.move_to_npc(title)
        Wait(3).delay()
        title, guild = get_guild_and_npc(rect)
        while not is_near_npc(title, guild):
            title, guild = get_guild_and_npc(rect)
            print(title, guild)
            Wait(1).delay()
        title, guild = get_guild_and_npc(rect)
        Navigator.click_at_npc(title)
        return title

    @staticmethod
    def turn_around(start):
        wx, wy = Window().position()
        x, y, _, _ = start
        Move().fromTo((wx + x, wy + y), (wx + x + TURN_AROUND_DISTANCE, wy + y))

def get_guild_and_npc(rect):
    image = screenshot(rect)
    extruder = Extruder(image)
    titleCenter = extruder.get_template_rect(CharTitleConfig)
    guildCenter = extruder.get_template_rect(GuildIconConfig)
    return titleCenter, guildCenter

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

def calc_nav_point(roi):
    x,y,w,h = roi
    center = int(x + w/2)
    return (center, y + h + Y_OFFSET_FROM_START_POSITION)
