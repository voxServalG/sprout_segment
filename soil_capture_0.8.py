import numpy as np
from scipy import ndimage
from skimage.io import imread
import matplotlib.pylab as pylab
from scipy.ndimage.morphology import binary_fill_holes
from PIL import Image, ImageFilter
import cv2
import time


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
    :return: [R_minus_G, R_minus_B, G_minus_B, green_diff]
    """
    R_minus_G = im[:, :, 0] - im[:, :, 1]
    R_minus_B = im[:, :, 0] - im[:, :, 2]
    G_minus_B = im[:, :, 1] - im[:, :, 2]
    green_diff = 2 * im[:, :, 1] - im[:, :, 0] - im[:, :, 2]
    return R_minus_G, R_minus_B, G_minus_B, green_diff


def get_mask(color_diff, min_threshold, max_threshold):
    height, width = color_diff[0].shape[:2]
    mask = np.zeros((height, width))
    height_min, height_max, width_min, width_max = (1280, 0, 1280, 0)
    for i in range(height):
        for j in range(width):
            pixel_val = [color_diff[0][i, j], color_diff[1][i, j], color_diff[2][i, j]]
            green_val = color_diff[3][i, j]
            if pixel_contains_soil(pixel_val, min_threshold[0:3], max_threshold[0:3]) or pixel_contains_sprout(
                    green_val, min_threshold[3], max_threshold[3]):
                mask[i, j] = 1
                if i < height_min:
                    height_min = i
                if i > height_max:
                    height_max = i
                if j < width_min:
                    width_min = j
                if j > width_max:
                    width_max = j

    for i in range(height):
        for j in range(width):
            if height_min <= i <= height_max and width_min <= j <= width_max:
                mask[i, j] = 1

    print("处理过程中，height介于{}和{}之间，width介于{}和{}之间".format(height_min, height_max, width_min, width_max))
    return mask


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


def soilCapture(im, min_thresh, max_thresh):
    im_blurred = cv2.blur(im, (7, 7))
    color_diff = get_color_diff(im_blurred)
    mask = get_mask(color_diff, min_thresh, max_thresh)
    masked_image = get_masked_image(im, mask)
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
    image = imread(IMAGE_SAND_CROPPED_SPROUTED)
    title_size = 10
    min_thresh = [20, 35, 15, 70]
    # R-G, R-B, G-B, 2G - R - B
    max_thresh = [40, 70, 35, 110]

    pylab.imsave('result.jpeg', soilCapture(image, min_thresh, max_thresh), format='jpeg')
    terminal_time = time.time()
    print("完成！用时{}秒".format(terminal_time - start_time))
