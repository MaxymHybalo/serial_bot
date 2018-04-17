import logging
import utils.cv2_utils as utils


class Drawer:

    def __init__(self, *shapes):
        self.shapes = shapes
        self.log = logging.getLogger('drawer')

    def draw(self):
        image = utils.make_image()
        for s in self.shapes:
            s.draw(image)
        utils.show(image)
