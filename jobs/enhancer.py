import logging
from utils.configurator import Configurator
from jobs.grid_layout import Grid
import utils.cv2_utils as utils


class Enhancer:

    def __init__(self, configpath):
        self.log = logging.getLogger('enhancer')
        self.config = Configurator(configpath).from_yaml()
        # TODO think to make decorator for this option
        self.debug = self.config['debug']
        print(self.debug)

    def process(self):
        grid_image = self._image_path(self.config['recognize']['grid']['image'])
        grid = Grid(grid_image, self.config['recognize']['grid']['size'], debug=self.debug)
        # End of inventory
        # TODO: In case when not exist any EOI
        eoi = grid.find_position(self._image_path(self.config['recognize']['grid']['eoi']))
        cube = self.config['enhancement']['cube']
        scope = grid.slice_inventory([cube[0] + 1, cube[1]], eoi)
        self.__fetch_scope_mask(scope)
        self.log.debug('End Enhancer process')

    def __fetch_scope_mask(self, scope):
        self.log.debug('Start fetching a images')
        # TODO try get region of all inventory and then split to parts
        result = list(map(lambda col: list(map(lambda cell: utils.make_image(region=cell), col)), scope))
        self.log.debug('End fetching a images')

    def _image_path(self, image):
        path = self.config['recognize']['prefix']['path']
        prefix = self.config['recognize']['prefix']['image_suffix']
        full_path = path + image + prefix
        self.log.debug('Grid identifier: {0}'.format(full_path))
        return full_path

