import cv2
import numpy as np

from utils.cv2_utils import screenshot, draw_rect, show_image
from jobs.helpers.extruder import Extruder

class Detector:

    def __init__(self, observable, window):
        self.window = window
        # import pdb; pdb.set_trace()
        self.observable = observable
        if type(observable) is str:
            self.observable = cv2.imread(observable)

    def detect(self):
        # move method head to once detection method if could be needed
        frame = screenshot(self.window.rect)
        e = Extruder(frame)
        match = e.match_by_template(self.observable, method='threshold')
        while not match:
            image = screenshot(self.window.rect)
            image = np.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            match = e.match_by_template(self.observable, image=image, method='threshold')
            frame = image
        return match