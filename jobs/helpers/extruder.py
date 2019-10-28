import cv2
import matplotlib.pyplot as plt
class Extruder:

    def __init__(self, roi):
        self.roi = roi
        
        print(self.roi)
        hsvRoi = cv2.cvtColor(self.roi, cv2.COLOR_BGR2HSV)
        dark_orange, light_orange = (16, 255, 244), (9, 166, 63)
        # (9, 166, 63)
        # light_orange = (1, 190, 200)
        # dark_orange = (18, 255, 255)
        mask = cv2.inRange(hsvRoi, light_orange, dark_orange)
        filtered = cv2.bitwise_and(self.roi, self.roi, mask=mask)
        plt.imshow(as_rgb(filtered))
        plt.show()
    
def as_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)