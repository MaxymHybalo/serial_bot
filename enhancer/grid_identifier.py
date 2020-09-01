import logging
import pyautogui as ui

import cv2

import utils.cv2_utils as utils

from enhancer.cell import Cell
from processes.recognizer import Recognizer
from jobs.helpers.extruder import Extruder

X_SHIFT = 1 # X_SHIFT and Y_SHIFT used to calibrate actual inventory grid position of found inventory feature
Y_SHIFT = 1
ITEM_WIDTH = 33
ITEM_HEIGHT = 33
MARGIN = 1
SIZE = [9, 11]
GRID_ENTRY = 'assets/enhancer/grid_identifier.png'
GRID_ENTRY_2 = 'assets/enhancer/inventory_shop_active.png'
# todo change debug to image log, decorate it
# include size into class
# add option use image instead path
class GridIdentifier:

    def __init__(self, source, debug=False):
        self.debug = debug
        self.source = source
        self.log = logging.getLogger('grid-identifier')
        self.identifier = cv2.imread(GRID_ENTRY)
        # utils.show_image(self.identifier)
        self.col, self.row = SIZE
        self.entry = self._find_grid_entry()
        # utils.show_image(utils.circle(self.source, (*self.entry, 2), thickness=3))
        self.inventory_region = self._inventory_region()
        self.log.debug('Inventory region {0}'.format(self.inventory_region))
        # utils.show_image(utils.rect(self.source, self.inventory_region))

        self.matix_rects = self.generate_rectangles(self.entry)
        # log cells
        # for c in self.matix_rects:
        #     self.source = utils.rect(self.source, c.rect())
        # utils.show_image(self.source)

    def slice_inventory(self, start, end):
        self.log.debug('Try slice scope {0}:{1}'.format(start, end))
        slice = list()
        start_line = self.matix_rects[start[1] - 1][start[0] - 1:self.col]
        slice.append(start_line)
        center = []
        if end:
            end_line = self.matix_rects[end[1]][:end[0]]
            center = self.matix_rects[start[1]:end[1]]
            slice.append(end_line)
        else:
            center = self.matix_rects[start[1]:11]
        for c in center:
            slice.append(c)
        self.write_2nd_rects(slice, 'testslice.png')
        return slice

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
        insertion = Recognizer(target, self.inventory_region, wait=0).recognize(once=True)
        if insertion is None:
            return None
        rect = list(insertion)
        rect[0], rect[1], rect[2], rect[3] = rect[0] - 1, rect[1] - 2, ITEM_WIDTH + 1, ITEM_HEIGHT + 1
        for row in self.matix_rects:
            if rect in row:
                x, y = row.index(list(rect)), self.matix_rects.index(row)
        self.log.debug('Found target at position: {0}'.format([x, y]))
        if self.debug:
            self.write_2nd_rects(self.matix_rects[y][x], 'log/eoi.png', single_rect=True)
        return x, y

    def generate_rectangles(self, start):
        self.log.debug('Try generate rectangles: {0}, {1}'.format(self.col, self.row))
        x, y = start
        cells = []
        for col in range(self.col):
            for row in range(self.row):
                dx = x + (ITEM_WIDTH + MARGIN) * col + col
                dy = y + (ITEM_HEIGHT + MARGIN + 1) * row + row
                config = {
                    "col": col,
                    "row": row,
                    "x": dx,
                    "y": dy
                }
                cells.append(Cell(**config))
        # import pdb; pdb.set_trace()
        self.log.debug('Cells generated')

        return cells

    def _find_grid_entry(self):
        self.log.debug('Grid anchor: {0}'.format(self.identifier.shape))
        grid_entry = Extruder(self.source).match_by_template(self.identifier, method='minmax')
        x, y, _, h = grid_entry
        self.log.debug('Found grid entry at: {0}'.format(grid_entry))
        return x + X_SHIFT, y + h + Y_SHIFT

    def _inventory_region(self):
        self.log.debug('Find inventory region')
        region = [self.entry[0] - 1, self.entry[1] - 1, self.col * (ITEM_WIDTH + 1) + self.col + 1,
                  self.row * (ITEM_HEIGHT + 2) + self.row + 1]
        return region
