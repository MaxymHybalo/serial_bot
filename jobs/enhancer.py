import logging
from utils.configurator import Configurator
from jobs.grid_layout import Grid
import utils.cv2_utils as utils


class Enhancer:

    def __init__(self, configpath):
        self.log = logging.getLogger('enhancer')
        self.config = Configurator(configpath).from_yaml()

    def process(self):
        grid_image = self._image_path(self.config['recognize']['grid']['image'])
        grid = Grid(grid_image, self.config['recognize']['grid']['size'])
        # End of inventory
        # TODO: In case when not exist any EOI
        eoi = grid.find_position(self._image_path(self.config['recognize']['grid']['eoi']))
        # centerMock = grid.get_center_of(5, 5)
        # point = [centerMock[0], centerMock[1], 4]
        # utils.log_image(**{'circle': point})

    def _image_path(self, image):
        path = self.config['recognize']['prefix']['path']
        prefix = self.config['recognize']['prefix']['image_suffix']
        full_path = path + image+ prefix
        self.log.debug('Grid identifier: {0}'.format(full_path))
        return full_path

