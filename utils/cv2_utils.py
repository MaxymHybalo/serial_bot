import logging
import cv2
import pyautogui as ui
import numpy as np

COLOR = (0, 255, 0)
THICKNESS = 1

log = logging.getLogger('image-utils')


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


def make_image(src=None, region=None):
    if region is None:
        image = ui.screenshot(src)
    else:
        if src is not None:
            image = ui.screenshot(src, region=region)
        else:
            image = ui.screenshot(region=region)
    return np.array(image)[:, :, ::-1].copy()


def show(image, name='image'):
    cv2.imshow(name, image)
    width, height = ui.size()
    cv2.moveWindow(name, int(width / 2), int(height / 2))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def log_image(**kwargs):
    """
    :param kwargs:
        file - flag save image to file, value is string with file name
    :return:
    """
    image = make_image()
    if 'multi' in kwargs:
        iterate = kwargs['multi']
        log.debug('Multiple {0}\'s'.format(iterate))
    else:
        iterate = None
    for key, value in kwargs.items():
        if key is 'rect':
            log.debug('Draw rectangle: {0}'.format(value))
            _rect(image, value, iterate)
        if key is 'circle':
            log.debug('Draw circle: {0}'.format(value))
            _circle(image, value, iterate)
    if 'file' in kwargs:
        log.debug('Save image to {0}'.format(kwargs['file']))
        cv2.imwrite(kwargs['file'], image)
    else:
        show(image)

def draw_rect(image, roi):
    return cv2.rectangle(image, roi[:2], (roi[0] + roi[2], roi[1] + roi[3]), 255,2)

def show_image(image):
    import matplotlib.pyplot as plt
    plt.imshow(image)
    plt.show()
