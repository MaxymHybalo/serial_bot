import logging
import utils.cv2_utils as utils
import cv2


class Drawer:

    def __init__(self, shapes, file=None):
        self.shapes = shapes
        self.log = logging.getLogger('drawer')
        self.image = None
        self.file = file

    def draw(self):
        self.image = utils.make_image()
        for s in self.shapes:
            s.draw(self.image)
        utils.show(self.image)

    def save(self):
        self.log.debug('Save image to {0}'.format(self.file))
        cv2.imwrite(self.file, self.image)
