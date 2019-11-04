from processes.click import Click
from shapes.window import Window

Y_OFFSET_FROM_START_POSITION = 70

class Navigator:

    @staticmethod
    def move_to_npc(npc_roi):
        npc_x, npc_y = calc_nav_point(npc_roi)
        wx, wy = Window().position()
        Click(wx + npc_x, wy + npc_y, process='dclick').make_click()

def calc_nav_point(roi):
    x,y,w,h = roi
    center = int(x + w/2)
    return (center, y + h + Y_OFFSET_FROM_START_POSITION)
