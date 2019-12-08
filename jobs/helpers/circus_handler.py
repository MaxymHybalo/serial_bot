from processes.wait import Wait
from processes.click import Click

from shapes.window import Window

from jobs.helpers.navigator import Navigator
from jobs.helpers.observer import Observer, observe_angle, observe_height
from jobs.helpers.handle_npc import HandleNpc
from jobs.helpers.configs import QuestMenu, AcceptQuest

class CircusHandler:

    def __init__(self):
        self.window = Window()

    # def get_quest(self):
    #     HandleNpc().select_menu(QuestMenu)
    #     HandleNpc().select_menu(AcceptQuest)


    def get_quest(self):
        obs = Observer(observe_angle, observe_height)
        obs.observe()

        npc_title = Navigator.touch_circus_npc()

        HandleNpc().select_menu(QuestMenu)
        HandleNpc().select_menu(AcceptQuest)

        Navigator.turn_around(npc_title)
        Wait(0.3).delay()

        from shapes.rect import Rect
        from jobs.helpers.extruder import StartPointConfig
        center = Rect(StartPointConfig.roi).center()
        x, y = self.window.relative(center)
        Click(x, y).make_click()
        