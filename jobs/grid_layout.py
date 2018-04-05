from processes.recognizer import Recognizer
from utils import cv2_utils as utils

class Grid:

    def __init__(self, identifier):
        self.identifier = identifier
        start = self.__find_grid_entry()
        image = utils.make_image()
        image = utils.draw_rect(image, start)
        utils.show(image)

    def __find_grid_entry(self):
        return Recognizer(self.identifier, None).recognize()
