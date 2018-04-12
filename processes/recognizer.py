import logging
import pyautogui as ui
import time
import numpy as np
import cv2


class Recognizer:

    def __init__(self, image, region, wait=1, process="recognize", **kwargs):
        self.log = logging.getLogger('recognizer')
        self.image = image
        self.region = region
        self.wait = wait
        self.process = process
        self.properties = kwargs

    def recognize(self):
        self.log.debug('Try to recognize')
        if self.region is not None:
            value = ui.locateOnScreen(str(self.image), region=self.region)
        else:
            value = ui.locateOnScreen(str(self.image))
        while value is None:
            time.sleep(self.wait)
            if self.region is not None:
                value = ui.locateOnScreen(str(self.image), region=self.region)
            else:
                value = ui.locateOnScreen(str(self.image))
        self.log.debug('Recognized: {0}'.format(value))
        return value

    def recognize_all(self):
        if self.region is not None:
            return ui.locateAllOnScreen(self.image, region=self.region)
        return ui.locateAllOnScreen(self.image,)

    def center_of(self):
        location = self.recognize()
        center = ui.center(location)
        return {
            'x': center[0],
            'y': center[1]
        }

    # return array of found corners of objects filtered by specific color
    # predicted params image, roi, color, kernel
    def find(self):
        if type(self.image) is str:
            self.image = cv2.imread(self.image)
            if 'roi' in self.properties:
                x, y, w, h = self.properties['roi']
                self.image = self.image[y:y + h, x:x + w]  # think about how to pass different locations
        elif self.image is None:
            self.image = ui.screenshot(region=self.properties['roi'])
            # convert to cv2 format
            self.image = np.array(self.image)
            self.image = self.image[:, :, ::-1]
        # [[0, 50, 50], [1, 255, 255]] - red color example
        color = self.properties['color']
        self.image = self._extract_color(self.image, color)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_HSV2BGR)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        lower_threshold = self.properties['threshold_lower'] if 'threshold_lower' in self.properties else 100
        ret, self.image = cv2.threshold(self.image, lower_threshold, 255, cv2.THRESH_BINARY)
        # (2, 2) - example of kernel(form) instance
        if self.properties['kernel'] is not None:
            form = self.properties['kernel'] if 'kernel' in self.properties else (1, 1)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, form)
            self.image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)
        self.image = np.float32(self.image)
        corners = cv2.goodFeaturesToTrack(self.image, 200, 0.01, 15)
        corners = np.int0(corners)
        return corners

    # color is array from first vector is lower color component, second is upper color component
    @staticmethod
    def _extract_color(image, color):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array(color[0])
        upper = np.array(color[1])
        mask = cv2.inRange(image, lower, upper)
        image = cv2.bitwise_and(image, image, mask=mask)
        return cv2.cvtColor(image, cv2.COLOR_HSV2BGR)

    def __str__(self):
        return 'image: ' + self.image + ' region: ' + str(self.region)
