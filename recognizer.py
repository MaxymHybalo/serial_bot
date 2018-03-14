import pyautogui as ui
import time
import numpy as np
import cv2


class Recognizer:

    def __init__(self, image, region, wait=1, process="recognize", **kwargs):
        self.image = image
        self.region = region
        self.wait = wait
        self.process = process
        print(kwargs)

    def recognize(self):
        self.value = ui.locateOnScreen(str(self.image), region= self.region)
        while self.value is None:
            time.sleep(self.wait)
            self.value = ui.locateOnScreen(str(self.image), region=self.region)
        return self.value

    def center_of(self):
        return {
            'x': self.value[0] + self.value[2] / 2,
            'y': self.value[1] + self.value[3] / 2
        }

    def find(self):
        # convert to cv2 format
        if type(self.image) is str:
            self.image = cv2.imread(self.image)
        else:
            self.image = np.array(self.image)
            self.image = self.image[:, :, ::-1]
        self.image = self.image[0:480, 0:330]
        cv2.imshow('source', self.image)
        self.image = self._extract_color(self.image, [[0, 50, 50], [5, 255, 255]])
        self.image = cv2.cvtColor(self.image, cv2.COLOR_HSV2BGR)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        ret, self.image = cv2.threshold(self.image, 120, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        erode = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)
        cv2.imshow('image', self.image)
        cv2.imshow('ERODE', erode)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilate = cv2.dilate(erode, kernel, iterations=1)
        cv2.imshow('DILATE', dilate)

        dilate = np.float32(dilate)
        corners = cv2.goodFeaturesToTrack(dilate, 200, 0.01, 10)
        corners = np.int0(corners)
        dilate = cv2.cvtColor(dilate, cv2.COLOR_GRAY2BGR)
        for c in corners:
            x, y = c.ravel()
            cv2.circle(dilate, (x, y), 2, 255, -1)
        cv2.imshow('marks', dilate)

        # show options
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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