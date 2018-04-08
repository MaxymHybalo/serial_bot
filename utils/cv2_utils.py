import cv2
import pyautogui as ui
import numpy as np

COLOR = (0, 255, 0)
THICKNESS = 1


def get_image(imagepath):
    if type(imagepath) is str:
        return cv2.imread(imagepath)
    if type(imagepath) in [list, tuple]:
        image = ui.screenshot(region=imagepath)
        image = np.asarray(image)
        return image
    return imagepath


def draw_corners(image, corners, color=255):
    image = get_image(image)
    for c in corners:
        if type(c) not in [tuple, list]:
            x, y = c.ravel()
        else:
            x, y = c
        cv2.circle(image, (x, y), 2, color, 2)
    return image


# def _draw(image, shape, value):
#     image = shape(image, value)
#     return image

# def draw_rect(image, rect):
#     if type(rect) in ITERABLE_TYPES:
#         for r in rect:
#             x, y, w, h = r
#             cv2.rectangle(image, (x, y), (x + w, y + h), COLOR, THINKNESS)
#     else:
#         x, y, w, h = rect
#         cv2.rectangle(image, (x, y), (x + w, y + h), COLOR, THINKNESS)
#     return image

# def draw_circle(image, circle):
#     if type(circle) in ITERABLE_TYPES:
#         for c in circle:
#             x, y, r = c
#             cv2.circle(image, (x,y), r, COLOR, THINKNESS)
#     else:
#         x, y, r = circle
#         cv2.circle(image, (x,y), r, COLOR, THINKNESS)
#     return image


def _rect(image, rect, iterate):
    if iterate is 'rect':
        for r in rect:
            x, y, w, h = r
            cv2.rectangle(image, (x, y), (x + w, y + h), COLOR, THICKNESS)
    else:
        x, y, w, h = rect
        cv2.rectangle(image, (x, y), (x+w, y+h), COLOR, THICKNESS)


def _circle(image, circle, iterate):
    if iterate is 'circle':
        for c in circle:
            x, y, r = c
            cv2.circle(image, (x, y), r, COLOR, THICKNESS)
    else:
        x, y, r = circle
        cv2.circle(image, (x, y), r, COLOR, THICKNESS)


def make_image(region=None):
    if region is None:
        image = ui.screenshot('test.png')
        return np.array(image)[:, :, ::-1].copy()


def show(image, name='image'):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def log_image(**kwargs):
    image = make_image()
    if 'multi' in kwargs:
        iterate = kwargs['multi']
        print('iterate', iterate)
    else:
        iterate = None
    for key, value in kwargs.items():
        if key is 'rect':
            _rect(image, value, iterate)
        if key is 'circle':
            _circle(image, value, iterate)
    show(image)
