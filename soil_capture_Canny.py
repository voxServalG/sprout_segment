import numpy as np
from scipy import signal, misc, ndimage
from skimage import filters, feature, img_as_float
from skimage.io import imread
from skimage.color import rgb2gray
from PIL import Image, ImageFilter
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
from scipy.ndimage.morphology import binary_fill_holes


IMAGE_SOIL = 'sample_day1_soil.jpeg'
IMAGE_SOIL_SPROUTED = 'sample.jpeg'
IMAGE_SAND = 'sample_sand.jpeg'
im_original = imread(IMAGE_SOIL)
im = rgb2gray(im_original)
height, width = im.shape[:2]  # height is row and width is column
mask = np.empty([height, width], dtype=bool)
for i in range(height):
    for j in range(width):
        if 140 <= i <= 600 and 282 <= j <= 1000:
            mask[i, j] = True
        else:
            mask[i, j] = False

im_gsm = ndimage.gaussian_filter(im, 5)
im_gsm += 0.05 * np.random.random(im_gsm.shape)
edges1 = feature.canny(im, sigma=4, mask=mask)
filled_edges1 = binary_fill_holes(edges1)


res = im_original.copy()
for i in range(height):
    for j in range(width):
        if filled_edges1[i, j] == 0:
            res[i, j, :] = 0
        else:
            pass


fig, ax0 = pylab.subplots(1, 1)
ax0.imshow(im_original)
fig, ax1 = pylab.subplots(1, 1)
ax1.imshow(im_gsm, cmap=pylab.cm.gray)
fig, ax2 = pylab.subplots(1, 1)
ax2.imshow(edges1, cmap=pylab.cm.gray)
ax2.set_title('edges1', fontsize=10)
fig, ax3 = pylab.subplots(1, 1)
ax3.imshow(filled_edges1, cmap=pylab.cm.gray)
ax3.set_title('filled edge', fontsize=10)
fig, ax4 = pylab.subplots(1, 1)
ax4.imshow(res)
pylab.show()
