import cv2
import numpy as np
import matplotlib.pyplot as plt

# Support classes
class CharTitleConfig:
    light = (11, 140, 0)
    dark = (18, 255, 255)

class Extruder:

    def __init__(self, image):

        if not isinstance(image, np.ndarray):
            image = np.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        self.image = image
        # plt.imshow(self.filtredImgByColor())
        # plt.show()

    def filtredImgByColor(self, config):
        return self.filterByColor(self.image, config)

    def filterByColor(self, image, colorSpace):
        # color space object with light and dark tupels
        # image as bgr color scheme
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, colorSpace.light, colorSpace.dark)
        filtered = cv2.bitwise_and(image, image, mask=mask)
        return filtered
    
    def match_by_template(self, template, image=None):
        if image is None:
            image = self.image
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(grayImage, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        h, w = template.shape
        return (top_left[0], top_left[1], w, h)
    
def as_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def draw_spectre():
    super_area = np.zeros((1,255,3), np.uint8)
    for k in range(255):
        for i in range(255):
            for j in range(255):
                hsv_area[i,j] = (i,j,k)
        super_area = cv2.vconcat([super_area, hsv_area])
        cv2.imwrite('test_hsv_spectre.png', super_area)

def test_extrude_by_channel(image):
    I = 14
    print(image.shape)
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    super_area = np.zeros((20, (I+1)*120, 3), np.uint8)
    dark = (255,255,255)

    for j in range(255):
        sub_row = np.zeros(image.shape, np.uint8)
        for i in range(I):
            # 9 29 93 124
            light = (i, 0, j)
            mask = cv2.inRange(hsvImage, light, dark)
            filtered = cv2.bitwise_and(image, image, mask=mask)
            filtered = cv2.putText(filtered, (str(i) + ' ' + str(j)), (0,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,255)
            sub_row = cv2.hconcat([sub_row, filtered])
        super_area = cv2.vconcat([super_area, sub_row])
    
    cv2.imwrite('test_hsv_channel_hv.png', super_area)