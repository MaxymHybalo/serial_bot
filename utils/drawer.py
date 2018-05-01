import logging
import utils.cv2_utils as utils
import cv2
from shapes.shape import Shape
from shapes.rect import Rect


class Drawer:

    def __init__(self, shapes, file=None, region=None):
        self.shapes = shapes
        self.log = logging.getLogger('drawer')
        self.image = None
        self.file = file
        self.region = region

    def draw(self):
        self.image = utils.make_image()
        for s in self.shapes:
            s.draw(self.image)
        if self.region:
            x, y, w, h = self.region
            self.image = self.image[y:y+h, x:x+w]
        utils.show(self.image)

    def save(self):
        self.log.debug('Save image to {0}'.format(self.file))
        cv2.imwrite(self.file, self.image)


def draw_state(cube, eoi, scope, roi):
    logging.debug('Draw global picture')
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
