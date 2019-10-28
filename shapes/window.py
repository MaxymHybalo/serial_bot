import pyautogui as ui
import matplotlib.pyplot as plt
import numpy as np
from utils.configurator import Configurator

class Window:

    def __init__(self):
        self.config = Configurator('config.yml').from_yaml()['window']
        self.width, self.height = self.config['width'], self.config['height']
        self.windowHead = ui.locateOnScreen(self.config['marker'])
        self.x = self.windowHead[0]
        self.y = self.windowHead[1] + self.windowHead[3]
        self.screen = ui.screenshot(region=(self.x,self.y, self.width, self.height))

    def center(self):
        return self.x + self.width / 2, self.y + self.height / 2
