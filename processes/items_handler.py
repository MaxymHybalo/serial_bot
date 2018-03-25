import utils.cv2_utils as utils
import numpy as np

ITEM_WIDTH = 35
ITEM_HEIGHT = 36

class ItemsHandler:

    def __init__(self, items_name, grid_name):
        self.items_name = items_name
        self.grid_name = grid_name
        self.items = None
        self.grid = None
        self.process = 'ItemsHandler'

    # image params used only to tracking, in future will be removed
    def handle(self):
        image = utils.draw_corners('assets/i5.JPG', self.items, [255, 0, 100])
        start_point = self._find_grid_start_point()
        grid = self._make_items_grid()
        grid[:,0] += start_point[0]
        grid[:, 1] += start_point[1]
        self.grid = grid
        target = self.find_cells()
        for g in target:
            image = utils.draw_rect(image, g, 35, 36);
        utils.show(image)
        return target

    def find_cells(self):
        filled_cells = []
        for g in self.grid:
            in_dim = lambda d, point, accuracy: point < d < point + accuracy
            detected = list(filter(
                lambda x: in_dim(x[0], g[0], ITEM_WIDTH) and in_dim(x[1], g[1], ITEM_HEIGHT),
                self.items.squeeze().tolist()))
            if len(detected) > 0:
                filled_cells.append(g.tolist())
        return filled_cells

    def _find_grid_start_point(self):
        self.grid = self.grid.squeeze()
        self.grid.sort(axis=0)
        self.grid.squeeze()
        return self.grid[0:1].squeeze()

    def set_items(self, items):
        self.items = items

    def set_grid(self, grid):
        self.grid = grid

    @staticmethod
    def _make_items_grid():
        return np.array([[x*35, y*36] for x in range(0, 9) for y in range(0, 11)])
