import cv2


def draw_corners(image, corners, color=255):
    if type(image) is str:
        image = cv2.imread(image)
    for c in corners:
        x, y = c.ravel()
        cv2.circle(image, (x, y), 3, color, -1)
    return image


def show(image, name='image'):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
