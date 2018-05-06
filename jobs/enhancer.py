import logging
import time
import numpy as np
import pyautogui as ui
from utils.configurator import Configurator
from jobs.grid_layout import Grid
import utils.cv2_utils as utils
from utils.drawer import draw_state
from processes.click import Click
from shapes.rect import Rect


class Enhancer:

    def __init__(self, configpath):
        self.log = logging.getLogger('enhancer')
        self.config = Configurator(configpath).from_yaml()
        self.serial = None
        self.cube = None
        self.grid = None

    def write_state(state):
        def wrapper(self):
            scope, eoi = state(self)
            cube_roi = self.grid.get_region_of(self.cube[0], self.cube[1])
            eoi_roi = self.grid.get_region_of(eoi[0] + 1, eoi[1] + 1) if eoi else None
            draw_state(cube_roi, eoi_roi, scope, self.grid.inventory_region)
            self.log.debug('Draw state')
            return scope, eoi
        return wrapper

    def process(self, serial):
        self.serial = serial
        self.enhance()
        self.log.debug('End Enhancer process')


    @write_state
    def state(self):
        self.log.debug('Getting inventory state')
        grid_image = self._image_path(self.config['recognize']['grid']['image'])
        self.grid = Grid(grid_image, self.config['recognize']['grid']['size'])
        # EOI: End Of Inventory
        eoi = self.grid.find_position(self._image_path(self.config['recognize']['grid']['eoi']))
        self.cube = self.config['enhancement']['cube']
        scope = self.grid.slice_inventory([self.cube[0] + 1, self.cube[1]], eoi)
        self.log.debug('Inventory state proceed')
        return scope, eoi

    def enhance(self):
        scope, eoi = self.state()
        self._click_at_target(self.config['recognize']['enhance']['menu'])
        before = self.__fetch_scope_mask(scope)
        points = self.base_clicks()
        self.do_flow(scope, points['make'], points['slot'])
        scope, eoi = self.state()
        after = self.__fetch_scope_mask(scope)
        broken = find_subtraction(before, after)
        self.log.debug('Broken items: {0}'.format(broken))
        broken = list(map(lambda e: scope[e[0]][e[1]], broken))
        if broken:
            self._click_at_target(self.config['recognize']['enhance']['close'])
            self._remove_broken(broken)

        # TODO move to some decorator
        cube_roi = self.grid.get_region_of(self.cube[0], self.cube[1])
        eoi_roi = self.grid.get_region_of(eoi[0] + 1, eoi[1] + 1) if eoi else None
        draw_state(cube_roi, eoi_roi, scope, self.grid.inventory_region, broken=broken)
        print(broken)

    def do_flow(self, scope, make, main_slot):
        self.log.debug('End base point init')
        self.log.info('Start enhancing from {0}'.format(len(scope)))
        for row_id, row in enumerate(scope):
            for col_id, col in enumerate(row):
                self.log.info('Row: {0}/{1}, Col: {2}/{3}'.format(row_id, len(scope), col_id, len(row)))
                item = Rect(col).click()
                item.make_click(self.serial)
                cube = Rect(self.grid.get_region_of(self.cube[0], self.cube[1])).click()
                cube.make_click(self.serial)
                make.make_click(self.serial)
                main_slot.make_click(self.serial)

    def _remove_broken(self, broken):
        self._click_at_target(self.config['recognize']['remove']['menu'])
        for i, b in enumerate(broken):
            c = Rect(b).click()
            c.make_click(self.serial)
            if i % 25:
                self.log.debug('Remove partially')
                self._click_at_target(self.config['recognize']['remove']['clear'])
        # self._click_at_target(self.config['recognize']['remove']['confirm'])

    def base_clicks(self):
        main_slot = ui.locateCenterOnScreen(self._image_path(self.config['recognize']['enhance']['slot']))
        main_slot = Click(main_slot[0], main_slot[1], process='dclick')
        make = ui.locateCenterOnScreen(self._image_path(self.config['recognize']['enhance']['make']))
        make = Click(make[0], make[1], delay=2)
        return {
            'make': make,
            'slot': main_slot
        }

    def _click_at_target(self, target):
        click = ui.locateCenterOnScreen(self._image_path(target))
        click = Click(click[0], click[1])
        click.make_click(self.serial)
        self.log.debug('Click at {0}'.format(target))

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


def find_subtraction(before, after):
    changed = []
    for row_id, row in enumerate(before):
        for col_id, col in enumerate(row):
            if not np.array_equal(after[row_id][col_id], col):
                changed.append([row_id, col_id])
    return changed
