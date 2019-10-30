import cv2
import numpy as np
import matplotlib.pyplot as plt

# Support classes
class CharTitleConfig:
    light = (11, 140, 0)
    dark = (18, 255, 255)

class Extruder:

    def __init__(self, image):
        self.image = image
        # plt.imshow(self.filtredImgByColor())
        # plt.show()

    def filtredImgByColor(self):
        return self.filterByColor(self.image, CharTitleConfig)

    def filterByColor(self, image, colorSpace):
        # color space object with light and dark tupels
        # image as bgr color scheme
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, colorSpace.light, colorSpace.dark)
        filtered = cv2.bitwise_and(image, image, mask=mask)
        return filtered
    
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