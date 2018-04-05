import cv2
import pyautogui as ui
import numpy as np

COLOR = (0, 255, 0)
THINKNESS = 2

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


def draw_rect(image, rect):
    x, y, w, h = rect
    cv2.rectangle(image, (x, y), (x + w, y + h), COLOR, THINKNESS)
    return image

def draw_circle(image, circle):
    x, y, r = circle
    cv2.circle(image, (x,y), r, COLOR, THINKNESS)

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
    for key, value in kwargs:
        if key is 'rect':
            image = draw_rect(image, value)
        if key is 'circle':
            image = draw_circle
    show(image)