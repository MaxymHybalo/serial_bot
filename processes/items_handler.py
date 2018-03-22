import utils.cv2_utils as utils
import numpy as np

class ItemsHandler:

    def __init__(self, items_name, grid_name):
        self.items_name = items_name
        self.grid_name = grid_name
        self.items = None
        self.grid = None
        self.process = 'ItemsHandler'

    # image params used only to tracking, in future will be removed
    def handle(self):
        image = utils.draw_corners('assets/inventory.JPG', self.items, [255, 0, 100])
        start_point = self._find_grid_start_point()
        grid = self._make_items_grid()
        grid[:,0] += start_point[0]
        grid[:, 1] += start_point[1]
        print(grid)
        for g in grid:
            image = utils.draw_rect(image, g, 35, 36);
        # image = utils.draw_corners(image, grid, [0, 0, 255])
        utils.show(image)

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
