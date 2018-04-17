from shapes.shape import Shape
import cv2


DEFAULT_COLOR = [0, 200, 100]
DEFAULT_THINKNESS = 1


class Rect(Shape):

    def __init__(self, rect, shape=None):
        self.rect = rect
        if shape is None:
            super().__init__(DEFAULT_COLOR, DEFAULT_THINKNESS)
        else:
            super().__init__(shape.color, shape.color)

    def draw(self, image):
        x, y, w, h = self.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), self.color, self.thinkness)
