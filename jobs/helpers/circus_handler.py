from processes.wait import Wait
from processes.click import Click

from shapes.window import Window

from jobs.helpers.navigator import Navigator
from utils.config import Config
from jobs.helpers.observer import Observer, observe_angle, observe_height
from jobs.helpers.handle_npc import HandleNpc
from jobs.helpers.configs import QuestMenu, AcceptQuest

config = Config()
class CircusHandler:

    def __init__(self):
        self.window = Window()

    def get_quest(self):
        obs = Observer(observe_angle, observe_height)
        obs.observe()


        Navigator.touch_npc(config.CharTitleConfig)

        HandleNpc().select_menu(config.QuestMenu)
        Wait(0.3).delay()

        HandleNpc().select_menu(config.AcceptQuest)
        Wait(0.3).delay()

        Navigator.turn_around()
        Wait(0.3).delay()

        from shapes.rect import Rect

        center = Rect(config.StartPointConfig.roi).center()
        x, y = self.window.relative(center)
        Click(x, y).make_click()
        
        Wait(3).delay()
    
    def go_to_dungeon(self):
        Navigator.touch_npc(config.DungeonNpc)
        HandleNpc().select_menu(config.CircusDungeonMenu)
