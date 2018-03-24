import cv2


def get_image(imagepath):
    return cv2.imread(imagepath)


def draw_corners(image, corners, color=255):
    if type(image) is str:
        image = get_image(image)
    for c in corners:
        if type(c) not in [tuple, list]:
            x, y = c.ravel()
        else:
            x, y = c
        cv2.circle(image, (x, y), 2, color, 2)
    return image


def draw_rect(image, point, w, h):
    cv2.rectangle(image, tuple(point), (point[0] + w, point[1] + h), (0, 255, 179), 2);
    return image


def show(image, name='image'):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
