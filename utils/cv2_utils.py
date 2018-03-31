import cv2
import pyautogui as ui
import numpy as np


def get_image(imagepath):
    if type(imagepath) is str:
        return cv2.imread(imagepath)
    if type(imagepath) in [list, tuple]:
        image = ui.screenshot(region=imagepath)
        # convert to cv2 format
        image = np.asarray(image)
        # image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
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


def draw_rect(image, point, w, h):
    point = np.array(point)
    cv2.rectangle(image, tuple(point.tolist()), (point[0] + w, point[1] + h), (0, 255, 179), 2);
    return image


def show(image, name='image'):
    image = get_image(image)
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
