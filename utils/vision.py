import numpy as np
import cv2
import time

start = time.time() * 1000

img = cv2.imread('test1.png')

# make less size
img = img[360:560, 700:1200]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_orange = np.array([15, 0, 0])
upper_orange = np.array([16, 255, 255])
mask = cv2.inRange(hsv, lower_orange, upper_orange)
result = cv2.bitwise_and(img, img, mask=mask)
gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
ret, result = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

# make erosion

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 20))
closed = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
cv2.imshow('morph', closed)

kernel = np.ones((5,5))
closed = cv2.erode(closed, kernel, iterations=1)
cv2.imshow('erode', closed)

closed = cv2.dilate(closed, kernel, iterations=1)
cv2.imshow('dilte', closed)

closed = np.float32(closed)
corners = cv2.goodFeaturesToTrack(closed, 200, 0.01, 10)
corners = np.int0(corners)

for c in corners:
    x, y = c.ravel()
    cv2.circle(img, (x, y), 3, 255, -1)
print('exec time', time.time() * 1000 - start)

cv2.imshow('source', img)
cv2.imshow('hsv', hsv)
cv2.moveWindow('source', 100, 0)
cv2.waitKey(0)
cv2.destroyAllWindows()


# NOTICES
# HSV = H - 180, SV-255 probably max values

# Featured algo
# 1. Get screen
# 2. Get HSV
# 3. Highlight orange(like NPC name)
# 4. To gray color
# 5. Threshold

