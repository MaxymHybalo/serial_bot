import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils.cv2_utils import show_image

class Extruder:

    def __init__(self, image):

        # if not isinstance(image, np.ndarray):
        #     image = np.array(image)
        #     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # self.image = image
        self.set_image(image)
        # plt.imshow(self.filtredImgByColor())
        # plt.show()

    def set_image(self, image):
        if not isinstance(image, np.ndarray):
            image = np.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        self.image = image

    def filtredImgByColor(self, config):
        return self.filterByColor(self.image, config)

    def filterByColor(self, image, colorSpace):
        # color space object with light and dark tupels
        # image as bgr color scheme
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = tuple(colorSpace.light)
        upper = tuple(colorSpace.dark)
        print(lower,upper)
        mask = cv2.inRange(hsv, lower, upper)
        filtered = cv2.bitwise_and(image, image, mask=mask)
        return filtered
    
    def get_template_rect(self, config):
        filtered = self.filtredImgByColor(config)
        template = cv2.imread(config.template)
        return self.match_by_template(template, image=filtered, roi=config.roi)
    
    def match_by_template(self, template, image=None, roi=None, method='minmax'):
        if image is None:
            image = self.image
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        if roi:
            x,y,w,h = roi
            image = image[y:y+h,x:x+w]
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(grayImage, template, cv2.TM_CCOEFF_NORMED)
        h, w = template.shape
        dx, dy = self._min_max_match(res) if method is 'minmax' else self._threshold_match(res) 
        if roi:
            dx += x
            dy += y
        return (dx, dy, w, h)
    
    def threshold(self, config):
        x,y,w,h = config.roi
        gray = self.image[y:y+h,x:x+w]
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        result = gray

        # TODO move 30 to config
        _, result = cv2.threshold(gray, 49, 255, cv2.THRESH_BINARY)
        # show_image(cv2.cvtColor(result,cv2.COLOR_GRAY2RGB))

        return result

    def _min_max_match(self, res):
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return max_loc

    def _threshold_match(self, res):
        threshold = 0.8
        loc = np.where( res >= threshold)
        loc = list(zip(*loc[::-1]))
        if not len(loc):
            return None
        return loc[0]

    def clear(self, image, kernel=(2,2)):
        kernel = np.ones(kernel, np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        return cv2.erode(image, kernel, iterations=1)

    def corners(self, image):
        result = np.float32(image)
        corners = cv2.goodFeaturesToTrack(result, 100, 0.01, 20)
        if corners is None:
            return None
        corners = np.int0(corners)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
        return corners
        # for c in corners:
            # x,y = c.ravel()
            # cv2.circle(result, (x,y), 3, 255, -1)
        # show_image(result)
    
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