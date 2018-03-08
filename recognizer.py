import pyautogui as ui
import time

class Recognizer:

    def __init__(self, image, region, wait=1, process="center_on"):
        self.image = image
        self.region = region
        self.wait = wait
        self.process = process

    def recognize(self):
        self.value = ui.locateOnScreen(str(self.image), region= self.region)
        while self.value is None:
            time.sleep(self.wait)
            self.value = ui.locateOnScreen(str(self.image), region= self.region)
        return self.value

    def center_of(self):
        return {
            'x': self.value[0] + self.value[2] / 2,
            'y': self.value[1] + self.value[3] / 2
        }

    def __str__(self):
        return 'image: ' + self.image + ' region: ' + str(self.region)