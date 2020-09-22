import utils.cv2_utils as utils

class Enhancer:

    def __init__(self, config, inventory):
        self.config = config
        self.inventory = inventory;

        print(self.config, self.inventory)
        # self.proceed(int(self.config['options']['cycles']))
        self.show_state()

    def proceed(self, loops):
        for l in range(loops):
            self.stage(l)

    def stage(self, cycle):
        print(cycle)

    def show_state(self):
        img = self.inventory.grid.cells_image()
        img = utils.rect(img, self.inventory.cube.rect(), 3, 3)
        img = utils.rect(img, self.inventory.cube.rect(), (244,0,0), 3)
        for c in self.inventory.working_cells:
            img = utils.rect(img, c.rect(), (199,200,0), 3)
        img = utils.rect(img, self.inventory.eoi.rect(), (30,100, 20), 3)
        print(self.inventory.main_slot)
        img = utils.rect(img, self.inventory.main_slot, (0, 200, 0),1)
        img = utils.rect(img, self.inventory.make, (100, 200, 0), 2)
        utils.show_image(img)