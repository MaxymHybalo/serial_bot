import logging

import cv2

from enhancer.cell import Cell
from enhancer.grid_identifier import GridIdentifier
from enhancer.helpers import Finder
from utils.configurator import Configurator
import utils.cv2_utils as utils # used for drawing images


FILE = 'assets/enhancer/inventory.png'
class Enhancer:

    def __init__(self, config):
        self.log = logging.getLogger('enhancer-v2')
        self.log.info('Created new enhancer instance')
        self.log.info('Config, {0}'.format(config))
        self.config = Configurator(config['enhancer']).from_yaml()
        self.fnd = Finder()
        self.open_source()
        self.grid = GridIdentifier(self.source)
        self.set_params()

        # import pdb; pdb.set_trace()
        # utils.show_image(self.grid.cells[self.cube_id].source)
        # utils.show_image(self.grid.source)


    def open_source(self):
        self.source = cv2.imread(FILE)
        self.log.info('Loaded source screen')
        # utils.show_image(self.source)

    def set_params(self):
        self.cube = self.config['enhancement']['cube']
        cube_col, cube_row = self.cube
        self.cube_id = self.fnd.by_id(int(cube_col) - 1, int(cube_row) - 1)
        print(self.cube)