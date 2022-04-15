import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from skimage.io import imread
import matplotlib.pylab as pylab
from scipy.ndimage.morphology import binary_fill_holes
from PIL import Image, ImageFilter
import cv2
import time


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
    for i in range(len(pixel_value)):
        if not min_threshold_list[i] <= pixel_value[i] <= max_threshold_list[i]:
            result = False
            break
    return result


def pixel_contains_sprout(pixel_value, min_threshold, max_threshold=255):
    return min_threshold <= pixel_value <= max_threshold


def get_color_diff(im):
    """
    :param im: image with form of RGB
    :return: [R_minus_G, R_minus_B, G_minus_B]
    """
    R_minus_G = im[:, :, 0] - im[:, :, 1]
    R_minus_B = im[:, :, 0] - im[:, :, 2]
    G_minus_B = im[:, :, 1] - im[:, :, 2]
    green_diff = 2 * im[:, :, 1] - im[:, :, 0] - im[:, :, 2]
    return R_minus_G, R_minus_B, G_minus_B, green_diff


def get_mask(color_diff, min_threshold, max_threshold):
    mask = np.zeros((height, width))
    height_min, height_max, width_min, width_max = (1280, 0, 1280, 0)
    for i in range(height):
        for j in range(width):
            pixel_val = [color_diff[0][i, j], color_diff[1][i, j], color_diff[2][i, j]]
            green_val = color_diff[3][i, j]
            if pixel_contains_soil(pixel_val, min_threshold[0:3], max_threshold[0:3]) or pixel_contains_sprout(
                    green_val, min_threshold[3], max_threshold[3]):
                mask[i, j] = 1
                # if i < height_min:
                #     height_min = i
                # if i > height_max:
                #     height_max = i
                # if j < width_min:
                #     width_min = j
                # if j > width_max:
                #     width_max = j

    for i in range(height):
        for j in range(width):
            if height_min <= i <= height_max and width_min <= j <= width_max:
                mask[i, j] = 1

    print("处理过程中，height介于{}和{}之间，width介于{}和{}之间".format(height_min, height_max, width_min, width_max))
    return mask


# def get_rectangle_mask(mask):


def get_masked_image(im, mask):
    """

    :param im:
    :param mask:
    :return:
    """
    height, width = im.shape[:2]  # height is row and width is column
    masked_image = im.copy()
    for i in range(height):
        for j in range(width):
            if mask[i, j] == 0:
                masked_image[i, j, :] = 0
            else:
                pass
    return masked_image


IMAGE_SOIL = 'sample_day1_soil.jpeg'
IMAGE_SOIL_SPROUTED = 'sample.jpeg'
IMAGE_SOIL_CROPPED_SPROUTED = 'sample_cropped.jpeg'
IMAGE_SAND_SPROUTED = 'sample_sand.jpeg'
IMAGE_SAND = 'day1_sand.jpeg'
IMAGE_SAND_CROPPED_SPROUTED = 'sample_sand_cropped.jpeg'
IMAGE_TEST = 'rgb_20220403_125355.jpeg'
if __name__ == "__main__":
    start_time = time.time()
    im0 = imread(IMAGE_SOIL)
    im = cv2.blur(im0, (7, 7))
    height, width = im.shape[:2]  # height is row and width is column
    title_size = 10
    min_thresh = [20, 35, 15, 70]
    # R-G, R-B, G-B, 2G - R - B
    max_thresh = [40, 70, 35, 110]

    color_diff = get_color_diff(im)
    mask = get_mask(color_diff, min_thresh, max_thresh)
    filled_mask = binary_fill_holes(mask)
    masked_im = get_masked_image(im0, filled_mask)
    pylab.imsave('result.jpeg', masked_im)

    row_sum = np.sum(mask, axis=1)
    column_sum = np.sum(mask, axis=0)
    '''调试'''
    x_row = np.arange(0, len(row_sum))
    f, ax = pylab.subplots(1, 1)
    ax.plot(x_row, row_sum)
    ax.axhline(y=((len(column_sum) + 1) / 2), lw=1)
    ax.text(1, (len(column_sum) + 1) / 2, 'sum={}'.format((len(column_sum) + 1) / 2))
    pylab.xlabel('index of row')

    x_row_diff = np.arange(0, len(row_sum) - 1)
    row_diff = np.diff(row_sum)
    ax.plot(x_row_diff, row_diff)
    ax.set_title('Row-sum and its one scale difference')

    x_column = np.arange(0, len(column_sum))
    f, ax = pylab.subplots(1, 1)
    ax.plot(x_column, column_sum)
    ax.axhline(y=((len(row_sum) + 1) / 2), lw=1)
    ax.text(1, (len(row_sum) + 1) / 2, 'sum={}'.format((len(row_sum) + 1) / 2))
    pylab.xlabel('index of column')

    x_column_diff = np.arange(0, len(column_sum) - 1)
    column_diff = np.diff(column_sum)
    ax.plot(x_column_diff, column_diff)
    ax.set_title('Column-sum and its one scale difference')
    '''调试'''

    f, ax = pylab.subplots(nrows=1, ncols=1)
    ax.imshow(im)
    ax.set_title('Original', fontsize=title_size)
    # f, (ax1, ax2, ax3) = pylab.subplots(1, 3)
    # ax1.imshow(color_diff[0], cmap='gray')
    # ax1.set_title('R-G', fontsize=title_size)
    # ax2.imshow(color_diff[1], cmap='gray')
    # ax2.set_title('R-B', fontsize=title_size)
    # ax3.imshow(color_diff[2], cmap='gray')
    # ax3.set_title('G-B', fontsize=title_size)
    # f, ax = pylab.subplots(1, 1)
    # ax.imshow(color_diff[3], cmap='gray')
    # ax.set_title('green diff = 2G-B-R', fontsize=title_size)
    f, (ax1, ax2) = pylab.subplots(1, 2)
    ax1.imshow(mask)
    ax2.imshow(filled_mask)
    ax1.set_title('mask', fontsize=title_size)
    ax2.set_title('filled mask', fontsize=title_size)
    f, ax = pylab.subplots(1, 1)
    ax.imshow(masked_im)
    ax.set_title('Masked Image', fontsize=title_size)
    pylab.show()

    terminal_time = time.time()
    print("完成！用时{}秒".format(terminal_time - start_time))
