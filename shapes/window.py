import logging
import pyautogui as ui
import matplotlib.pyplot as plt
import numpy as np
from utils.configurator import Configurator
from utils.singleton import Singleton

class Window(metaclass=Singleton):

    def __init__(self):
        self.log = logging.getLogger('window')
        self.config = Configurator('config.yml').from_yaml()['window']
        self.width, self.height = self.config['width'], self.config['height']
        self.locate_window()
        if self.windowHead is None:
            self.log.error('Window has not initiated!')
            return
        self.x = self.windowHead[0]
        self.y = self.windowHead[1] + self.windowHead[3]
        self.screen = ui.screenshot(region=(self.x,self.y, self.width, self.height))
        self.rect = (self.x, self.y, self.width, self.height)

    def position(self):
        return self.x, self.y

    def locate_window(self):
        if not hasattr(self, 'windowHead'):
            self.windowHead = ui.locateOnScreen(self.config['marker'])
            self.log.info('Located game window on screen')
        else:
            print('window already inited: ', self.windowHead)
    
    def center(self):
        return self.x + int(self.width / 2), self.y + int(self.height / 2)

    def relative_center(self):
        return int(self.width / 2), int(self.height / 2)

    def relative(self, point):
        x, y = point
        return self.x + x, self.y + y