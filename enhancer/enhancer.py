import logging

import cv2

from enhancer.cell import Cell
from enhancer.grid_identifier import GridIdentifier
import utils.cv2_utils as utils # used for drawing images

FILE = 'assets/enhancer/inventory.png'
class Enhancer:

    def __init__(self, config):
        self.log = logging.getLogger('enhancer-v2')
        self.log.info('Created new enhancer instance')
        self.log.info('Config, {0}'.format(config))
        self.open_source()
        GridIdentifier(self.source)

    def open_source(self):
        self.source = cv2.imread(FILE)
        self.log.info('Loaded source screen')
        # utils.show_image(self.source)