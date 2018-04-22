import logging
from utils.configurator import Configurator
from jobs.grid_layout import Grid
import utils.cv2_utils as utils
from utils.drawer import Drawer
from shapes.shape import Shape
from shapes.rect import Rect


# todo make test for changes at inventory and highlight it
class Enhancer:

    def __init__(self, configpath):
        self.log = logging.getLogger('enhancer')
        self.config = Configurator(configpath).from_yaml()

    def write_state(state):
        def wrapper(self):
            draw = self.__draw_point
            grid, scope, cube, eoi = state(self)
            cube_roi = grid.get_region_of(cube[0], cube[1])
            eoi_roi = grid.get_region_of(eoi[0] + 1, eoi[1] + 1) if eoi else None
            draw(cube_roi, eoi_roi, scope, grid.inventory_region)
            self.log.debug('Draw state')
            return grid, scope, cube, eoi
        return wrapper

    def process(self):
        grid, scope, cube, eoi = self.state()
        items = self.__fetch_scope_mask(scope)
        self.log.debug('End Enhancer process')
        return grid, scope, cube, eoi

    @write_state
    def state(self):
        self.log.debug('Getting inventory state')
        grid_image = self._image_path(self.config['recognize']['grid']['image'])
        grid = Grid(grid_image, self.config['recognize']['grid']['size'])
        # EOI: End Of Inventory
        eoi = grid.find_position(self._image_path(self.config['recognize']['grid']['eoi']))
        cube = self.config['enhancement']['cube']
        scope = grid.slice_inventory([cube[0] + 1, cube[1]], eoi)
        self.log.debug('Inventory state proceed')
        return grid, scope, cube, eoi

    def __fetch_scope_mask(self, scope):
        self.log.debug('Start fetching a images')
        # TODO try get region of all inventory and then split to parts
        result = list(map(lambda col: list(map(lambda cell: utils.make_image(region=cell), col)), scope))
        self.log.debug('End fetching a images')
        return result

    def _image_path(self, image):
        path = self.config['recognize']['prefix']['path']
        prefix = self.config['recognize']['prefix']['image_suffix']
        full_path = path + image + prefix
        self.log.debug('Grid identifier: {0}'.format(full_path))
        return full_path

    def __draw_point(self, cube, eoi, scope, roi):
        self.log.debug('Draw global picture')
        cube = Rect(cube, Shape((41, 103, 248), 1))
        eoi = Rect(eoi, Shape((236, 221, 87), 1))
        body = []
        for row in scope:
            for cell in row:
                body.append(Rect(cell, Shape((115, 228, 95), 1)))
        body.append(cube)
        body.append(eoi)
        drawer = Drawer(body, 'log/all_in_one.png', roi)
        drawer.draw()
        drawer.save()

