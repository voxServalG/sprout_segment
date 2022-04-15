import cv2
import numpy as np
import matplotlib.pyplot as plt

FILE_NAME = '.\\sample_cropped.jpeg'
img = cv2.imread(FILE_NAME)
cv2.imshow('initial', img)
# cv2.waitKey(0)

float_img = np.array(img, dtype=np.float32) / 255.0
(b, g, r) = cv2.split(float_img)
gray_img = 2 * g - b - r

(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray_img)
gray_u8 = np.array((gray_img - minVal) / (maxVal - minVal) * 255, dtype=np.uint8)
bin_img = cv2.adaptiveThreshold(gray_u8, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
cv2.imshow('binary_greenzone', bin_img)
# cv2.waitKey(0)

(b8, g8, r8) = cv2.split(img)
color_img = cv2.merge([b8 & bin_img, g8 & bin_img, r8 & bin_img])
cv2.imshow('result', color_img)

cv2.waitKey()
cv2.destroyAllWindows()