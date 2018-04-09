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
        self.start, _ = self.__find_grid_entry()
        self.inventory_region = self.__inventory_region()
        self.matix_rects = self.generate_rectangles(self.start)

    def slice_inventory(self, start, end):
        start_line = self.matix_rects[start[1] - 1][start[0] - 1:self.col]
        end_line = self.matix_rects[end[1] - 1][:end[0]]
        body = self.matix_rects[start[1]:end[1]-1]
        print(body)
        body.append(start_line)
        body.append(end_line)
        self.__visualize_rect_matrix(body)
        # utils.log_image(**{'rect': body, 'multi':'rect'})
        return None

    def get_center_of(self, col, row):
        """
        :param col: column of item
        :param row: row of item
        :return: center coordinates of item cell
        """
        item = self.matix_rects[row - 1][col - 1]
        return int(item[0] + item[2] / 2), int(item[1] + item[3] / 2)

    def get_region_of(self, col, row):
        """
        :param col: column of item position
        :param row: row of item position
        :return: rectangle of item area
        """
        return self.matix_rects[row - 1][col - 1]

    def find_position(self, target):
        """
        :param target: path to item image
        :return: col and row of found
        """
        self.log.debug('Find target at inventory')
        rect = Recognizer(target, region=self.inventory_region).recognize()
        target_col = (rect[0] - self.start[0] - self.col + 2)/ITEM_WIDTH
        target_row = (rect[1] - self.start[1] - self.row)/(ITEM_HEIGHT + 2)
        startless = [int(target_col) + 1, int(target_row) + 1]
        self.log.debug('Found target at position: {0}'.format(startless))
        return startless

    def generate_rectangles(self, start):
        self.log.debug('Try generate rectangles: {0}, {1}'.format(self.col, self.row))
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

    def __inventory_region(self):
        return [self.start[0], self.start[1], self.col * (ITEM_WIDTH + 1) + self.col,
         self.row * (ITEM_HEIGHT + 2) + self.row]

    def __visualize_rect_matrix(self, matrix):
        self.log.debug('Start visualizing')
        rects = []
        for row in matrix:
            rects += row
        utils.log_image(**{'rect': rects, 'multi': 'rect'})
        self.log.debug('Visualization ended')
