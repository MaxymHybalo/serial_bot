import logging
from processes.recognizer import Recognizer
import utils.cv2_utils as utils

ITEM_WIDTH = 33
ITEM_HEIGHT = 33
MARGIN = 1


class Grid:

    def __init__(self, identifier, size, debug=False):
        self.debug = debug
        self.log = logging.getLogger('grid')
        self.identifier = identifier
        self.col, self.row = size
        self.start, _ = self.__find_grid_entry()
        self.inventory_region = self.__inventory_region()
        self.matix_rects = self.generate_rectangles(self.start)

    def slice_inventory(self, start, end):
        self.log.debug('Try slice scope {0}:{1}'.format(start, end))
        start_line = self.matix_rects[start[1] - 1][start[0] - 1:self.col]
        end_line = self.matix_rects[end[1]][:end[0]]
        body = list()
        body.append(start_line)
        center = self.matix_rects[start[1]:end[1]]
        for c in center:
            body.append(c)
        body.append(end_line)
        self.log.debug('Sliced scope')
        if self.debug:
            self.write_2nd_rects(body, 'log/scope_of_inventory.png')
        return body

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
        rect = list(Recognizer(target, self.inventory_region).recognize())
        rect[0], rect[1], rect[2], rect[3] = rect[0] - 2, rect[1] - 2, ITEM_WIDTH + 1, ITEM_HEIGHT + 1
        for row in self.matix_rects:
            if rect in row:
                x, y = row.index(list(rect)), self.matix_rects.index(row)
        self.log.debug('Found target at position: {0}'.format([x, y]))
        if self.debug:
            self.write_2nd_rects(self.matix_rects[y][x], 'log/eoi.png', singlerect=True)
        return x, y

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
        if self.debug:
            self.write_2nd_rects(rectangles, 'log/inventory_items_matrix.png')
        return rectangles

    def __find_grid_entry(self):
        rect = Recognizer(self.identifier, None).recognize()
        start = (rect[0], rect[1] + rect[3], 3)
        end = (rect[0] + rect[2], rect[1] + rect[3], 3)
        self.log.debug('Found grid entry at: {0}'.format(start))
        return start, end

    def __inventory_region(self):
        self.log.debug('Find inventory region')
        region = [self.start[0] - 1, self.start[1] - 1, self.col * (ITEM_WIDTH + 1) + self.col + 1,
                  self.row * (ITEM_HEIGHT + 2) + self.row + 1]
        if self.debug:
            utils.log_image(**{'rect': region, 'file': 'log/inventory_region.png'})
        return region

    def __visualize_rect_matrix(self, matrix):
        self.log.debug('Start visualizing')
        rects = []
        for row in matrix:
            rects += row
        utils.log_image(**{'rect': rects, 'multi': 'rect'})
        self.log.debug('Visualization ended')

    @staticmethod
    def write_2nd_rects(matrix, filename, singlerect=False):
        if singlerect:
            utils.log_image(**{'rect': matrix, 'file': filename})
        else:
            rects = []
            for r in matrix:
                rects += r
            utils.log_image(**{'rect': rects, 'multi': 'rect', 'file': filename})
