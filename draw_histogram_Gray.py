import numpy as np
import matplotlib.pyplot as plt
import skimage
from skimage.transform import (hough_line, hough_line_peaks, hough_circle,
                               hough_circle_peaks)
from skimage.draw import circle_perimeter
from skimage.feature import canny
from skimage.data import astronaut
from skimage.io import imread, imsave
from skimage.color import rgb2gray, gray2rgb, label2rgb
from skimage import img_as_float
from skimage.morphology import skeletonize
from skimage import data, img_as_float
from matplotlib import cm
from skimage.filters import sobel, threshold_otsu
from skimage.feature import canny
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
from skimage.segmentation import mark_boundaries, find_boundaries

FILE_NAME = '.\\sample_sand.jpeg'
# imread得到的二维矩阵元素全部介于0 1之间，使其扩增到0-256
img_gray = skimage.io.imread(FILE_NAME, as_gray=True) * 256


f, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot()
ax1.imshow(img_gray, cmap='gray')


edges = canny(img_gray, sigma=5)
ax2.plot()
ax2.imshow(edges, cmap=plt.cm.gray, interpolation='nearest')
ax2.axis('off'), plt.show()

plt.show()
