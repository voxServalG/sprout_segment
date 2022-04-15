import numpy as np
import skimage.color
from scipy import ndimage
from skimage.io import imread
from skimage.color import rgb2gray
from PIL import Image, ImageFilter
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def getZ(img, X, Y):
    gray = img[X, Y]
    return gray


def pixel_contains_soil(pixel_value, min_threshold_list, max_threshold_list):
    """

    :param pixel_value:         A list containing (R-G, R-B, G-B) value of current pixel.

    :param min_threshold_list:  A list containing minimum threshold of (R-G, R-B, G-B) value.
                                Any pixel with any (R-G, R-B, G-B) value BELOW corresponding min_threshold
                                will not be considered as 'soil'.

    :param max_threshold_list:  A list containing maximum threshold of (R-G, R-B, G-B) value.
                                Any pixel with any (R-G, R-B, G-B) value GREATER THAN corresponding max_threshold
                                will not be considered as 'soil'.\

    :return:                    Boolean. Tells if current pixel 'is soil'.
    """
    result = True
    for i in range(len(min_threshold_list)):
        if not min_threshold_list[i] <= pixel_value[i] <= max_threshold_list[i]:
            result = False
            break
    return result


im = imread('sample_day1_soil.jpeg')
# im = ndimage.gaussian_filter(im, 0.75)
height, width = im.shape[:2]  # height is row and width is column
title_size = 10
R_minus_G = im[:, :, 0] - im[:, :, 1]
R_minus_B = im[:, :, 0] - im[:, :, 2]
G_minus_B = im[:, :, 1] - im[:, :, 2]
min_thresh = [20, 35, 15]
max_thresh = [40, 70, 35]


def get_soil_mask(R_minus_G, R_minus_B, G_minus_B, min_threshold, max_threshold):
    """

    :param R_minus_G:
    :param R_minus_B:
    :param G_minus_B:
    :param min_threshold:
    :param max_threshold:
    :return:
    """
    mask = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            pixel_val = [R_minus_G[i, j], R_minus_B[i, j], G_minus_B[i, j]]
            if pixel_contains_soil(pixel_val, min_threshold, max_threshold):
                mask[i, j] = 1
    return mask


def get_masked_image(im, mask):
    """

    :param im:
    :param mask:
    :return:
    """
    masked_image = im.copy()
    for i in range(height):
        for j in range(width):
            if mask[i, j] == 0:
                masked_image[i, j, :] = 0
            else:
                pass
    return masked_image


# f, ax = pylab.subplots(1, 1)
# ax.imshow(mask, cmap='gray')
# pylab.show()
# print("done")



f, ax = pylab.subplots(nrows=1, ncols=1)
ax.imshow(im)
ax.set_title('Original', fontsize=title_size)
f, bx = pylab.subplots(nrows=1, ncols=1)
bx.imshow(R_minus_G, cmap='gray')  # R-G
bx.set_title('R minus G', fontsize=title_size)
f, cx = pylab.subplots(nrows=1, ncols=1)
cx.imshow(R_minus_B, cmap='gray')  # R-B
cx.set_title('R minus B', fontsize=title_size)
f, dx = pylab.subplots(nrows=1, ncols=1)
dx.imshow(G_minus_B, cmap='gray')  # G-B
dx.set_title('G minus B', fontsize=title_size)
# f2, bx = pylab.subplots(1, 1)
# bx.imshow(mask * R_minus_B, cmap='gray')
# bx.set_title('masked R_minus_B', fontsize=title_size)
f3, cx = pylab.subplots(1, 1)
cx.imshow(res, cmap='gray')
cx.set_title('masked im', fontsize=title_size)
pylab.show()

# f2, (bx1, bx2) = pylab.subplots(2, 1)
# bx1.imshow(mask * R_minus_B, cmap='gray')
# bx1.set_title('masked R_minus_B', fontsize=title_size)
# bx2.imshow(R_minus_B, cmap='gray')
# bx2.set_title('R_minus_B', fontsize=title_size)
# pylab.show()

# if __name__ == '__main__':
#     figure = pylab.figure()
#     # axes = Axes3D(figure)
#     # X = np.arange(0, height, 1)
#     # Y = np.arange(0, width, 1)
#     # X, Y = np.meshgrid(X, Y)
#     # axes.plot_surface(X, Y, getZ(R_minus_B, X, Y), cmap='rainbow')
#     # pylab.show()
#     xx, yy = np.mgrid[0:R_minus_B.shape[0], 0:R_minus_B.shape[1]]
#     ax = figure.gca(projection='3d')
#     ax.plot_surface(xx, yy, R_minus_B, cmap=pylab.cm.coolwarm, antialiased=False)
#     pylab.show()


