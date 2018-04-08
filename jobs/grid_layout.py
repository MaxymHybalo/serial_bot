import logging
from processes.recognizer import Recognizer
import utils.cv2_utils as utils

ITEM_WIDTH = 33
ITEM_HEIGHT = 33
MARGIN = 1


class Grid:

    def __init__(self, identifier, size):
        self.log = logging.getLogger('grid')
        self.identifier = identifier
        self.col, self.row = size
        self.matix_rects = self.generate_rectangles()
        self.__visualize_rect_matrix(self.matix_rects)

    def generate_rectangles(self):
        self.log.debug('Try generate rectangles: {0}, {1}'.format(self.col, self.row))
        start, _ = self.__find_grid_entry()
        start = [i + 1 for i in start]
        x, y, _ = start
        cols = [c for c in range(self.col)]
        rows = [r for r in range(self.row)]
        rectangles = list(
            map(lambda row: list(
                map(lambda col: [x + (ITEM_WIDTH + MARGIN) * col + col, y + (ITEM_HEIGHT + MARGIN + 1) * row + row,
                                 ITEM_WIDTH + 1, ITEM_HEIGHT + 1], cols)), rows))
        self.log.debug('Rectangles generated')
        return rectangles

    def __find_grid_entry(self):
        rect = Recognizer(self.identifier, None).recognize()
        start = (rect[0], rect[1] + rect[3], 3)
        end = (rect[0] + rect[2], rect[1] + rect[3], 3)
        self.log.debug('Found grid entry at: {0}'.format(start))
        return start, end

    def __visualize_rect_matrix(self, matrix):
        self.log.debug('Start visualizing')
        rects = []
        for row in matrix:
            rects += row
        utils.log_image(**{'rect': rects, 'multi': 'rect'})
        self.log.debug('Visualization ended')
