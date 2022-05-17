import numpy as np


def pixel_contains_soil(pixel_value, min_threshold_list, max_threshold_list):
    """

    :param pixel_value:         A list containing (R-G, R-B, G-B) value of current pixel.

    :param min_threshold_list:  A list containing minimum threshold of (R-G, R-B, G-B) value.
                                Any pixel with any item in its (R-G, R-B, G-B) LOWER THAN corresponding item in
                                min_threshold will not be considered as 'soil'.

    :param max_threshold_list:  A list containing maximum threshold of (R-G, R-B, G-B) value.
                                Any pixel with any item in its (R-G, R-B, G-B) GREATER THAN corresponding item in
                                max_threshold will not be considered as 'soil'.

    :return:                    Boolean. Tells if current pixel 'belongs to soil'.
    """
    result = True
    for i in range(len(pixel_value)):
        if not min_threshold_list[i] <= pixel_value[i] <= max_threshold_list[i]:
            result = False
            break
    return result


def pixel_contains_sprout(pixel_value, min_threshold, max_threshold=None):
    """

    :param pixel_value:     A single value containing 2G-R-B value of current pixel.

    :param min_threshold:   A single value containing minimum threshold of 2G-R-B value.
                            Any pixel with a 2G-R-B value LOWER THAN this parameter will not be considered as 'sprout'

    :param max_threshold:   A single value containing maximum threshold of 2G-R-B value. 255 by default. Modify when
                            necessary.

    :return:                Boolean. Tells if current pixel 'belongs to sprout'.
    """
    if max_threshold is None:
        max_threshold = 255
    return min_threshold <= pixel_value <= max_threshold


def get_color_diff(im):
    """
    
    :param im:  A 3-dimensional array (e.g. RGB image).
    :return:    A tuple like (R-G, R-B, G-B, 2G-R-B) containing four 2-dimensional arrays, each telling a color
                difference of :parameter im.
    这个函数获取原图im的R-G, R-B, G-B, 2R-G-B数据，返回4个720*1280矩阵。
    """
    R_minus_G = im[:, :, 0] - im[:, :, 1]
    R_minus_B = im[:, :, 0] - im[:, :, 2]
    G_minus_B = im[:, :, 1] - im[:, :, 2]
    green_diff = 2 * im[:, :, 1] - im[:, :, 0] - im[:, :, 2]
    return R_minus_G, R_minus_B, G_minus_B, green_diff


def get_mask(im, min_threshold, max_threshold, ratio=None):
    """

    :param im:              A 3-dimensional array (e.g. RGB image).
    :param min_threshold:   A list containing minimum threshold of (R-G, R-B, G-B, 2R-G-B) value.
    :param max_threshold:   A list containing maximum threshold of (R-G, R-B, G-B, 2R-G-B) value.
    :param ratio:           A float value. Check get_processed_mask().

    :return:                A rectangular 2-dimensional array , equivalently, a rectangular 'mask'. Will be used to
                            crop an image.
    """
    if ratio is None:
        ratio = 0.39
    color_diff = get_color_diff(im)
    height, width = color_diff[0].shape[:2]
    mask = np.zeros((height, width))
    upper_row, lower_row, left_col, right_col = (0, 0, 0, 0)
    for i in range(height):
        pixel_contains_soil_or_sprout = 0
        for j in range(width):
            pixel_val = [color_diff[0][i, j], color_diff[1][i, j], color_diff[2][i, j]]
            green_val = color_diff[3][i, j]
            if pixel_contains_soil(pixel_val, min_threshold[0:3], max_threshold[0:3]) or pixel_contains_sprout(
                    green_val, min_threshold[3], max_threshold[3]):
                pixel_contains_soil_or_sprout += 1
        if (pixel_contains_soil_or_sprout / width) > ratio:a
            upper_row = i
            break

    for i in reversed(range(height)):
        pixel_contains_soil_or_sprout = 0
        for j in range(width):
            pixel_val = [color_diff[0][i, j], color_diff[1][i, j], color_diff[2][i, j]]
            green_val = color_diff[3][i, j]
            if pixel_contains_soil(pixel_val, min_threshold[0:3], max_threshold[0:3]) or pixel_contains_sprout(
                    green_val, min_threshold[3], max_threshold[3]):
                pixel_contains_soil_or_sprout += 1
        if pixel_contains_soil_or_sprout / width > ratio:
            lower_row = i
            break

    for i in range(width):
        pixel_contains_soil_or_sprout = 0
        for j in range(upper_row, lower_row + 1):
            pixel_val = [color_diff[0][j, i], color_diff[1][j, i], color_diff[2][j, i]]
            green_val = color_diff[3][j, i]
            if pixel_contains_soil(pixel_val, min_threshold[0:3], max_threshold[0:3]) or pixel_contains_sprout(
                    green_val, min_threshold[3], max_threshold[3]):
                pixel_contains_soil_or_sprout += 1
        if pixel_contains_soil_or_sprout / height > ratio:
            left_col = i
            break

    for i in reversed(range(width)):
        pixel_contains_soil_or_sprout = 0
        for j in range(upper_row, lower_row + 1):
            pixel_val = [color_diff[0][j, i], color_diff[1][j, i], color_diff[2][j, i]]
            green_val = color_diff[3][j, i]
            if pixel_contains_soil(pixel_val, min_threshold[0:3], max_threshold[0:3]) or pixel_contains_sprout(
                    green_val, min_threshold[3], max_threshold[3]):
                pixel_contains_soil_or_sprout += 1
        if pixel_contains_soil_or_sprout / height > ratio:
            right_col = i
            break

    mask[upper_row:lower_row + 1, left_col:right_col + 1] = 1
    # filled_mask = binary_fill_holes(mask)

    # '''调试1'''
    # f, ax = pylab.subplots(nrows=1, ncols=1)
    # ax.imshow(mask)
    # ax.set_title('Initial Filled Mask', fontsize=10)
    # pylab.show()
    # print('调试1完成')
    # '''调试1'''

    return mask

    # '''调试2'''
    # x_row = np.arange(0, len(row_sums))
    # f, ax = pylab.subplots(1, 1)
    # ax.plot(x_row, row_sums)
    # ax.axhline(y=(len(column_sums) + 1) * ratio, lw=1)
    # ax.text(1, (len(column_sums) + 1) * ratio + 5, 'sum={:.3f}'.format((len(column_sums) + 1) * ratio))
    # pylab.xlabel('index of row')
    #
    # diff_scale = 1
    # x_row_diff = np.arange(0, len(row_sums) - diff_scale)
    # row_diff = np.diff(row_sums, diff_scale)
    # ax.plot(x_row_diff, row_diff)
    # ax.set_title('Row-sum and its {} difference'.format(diff_scale))
    #
    # x_column = np.arange(0, len(column_sums))
    # f, ax = pylab.subplots(1, 1)
    # ax.plot(x_column, column_sums)
    # ax.axhline(y=((len(row_sums) + 1) * ratio), lw=1)
    # ax.text(1, (len(row_sums) + 1) * ratio, 'sum={}'.format((len(row_sums) + 1) * ratio))
    # pylab.xlabel('index of column')
    #
    # x_column_diff = np.arange(0, len(column_sums) - diff_scale)
    # column_diff = np.diff(column_sums, diff_scale)
    # ax.plot(x_column_diff, column_diff)
    # ax.set_title('Column-sum and its {} difference'.format(diff_scale))
    # print("调试2完成")
    # '''调试2'''


# def get_processed_mask(mask, ratio):
#     """
#
#     :param mask:    A 2-dimensional array.
#     :param ratio:   A float value. Any row/column of :parameter mask containing 'True' value at a ratio less than
#                     :parameter ratio will be marked as 'False'.
#     :return:        A 2-dimensional array.
#     """
#     height, width = mask.shape[:2]
#     result = np.zeros((height, width), dtype=bool)
#     row_sums = np.sum(mask, axis=1)
#     column_sums = np.sum(mask, axis=0)
#     row_sum_threshold = (len(column_sums) + 1) * ratio
#     column_sum_threshold = (len(row_sums) + 1) * ratio
#     height_min, height_max, width_min, width_max = (height, 0, width, 0)
#
#     index_row = 0
#     for i in range(0, len(row_sums)):
#         if row_sums[i] >= row_sum_threshold and i < height_min:
#             height_min = i
#             index_row += 1
#             break
#         index_row += 1
#     for i in range(index_row, len(row_sums)):
#         if row_sums[i] >= row_sum_threshold and i > height_max:
#             height_max = i
#
#     index_column = 0
#     for i in range(0, len(column_sums)):
#         if column_sums[i] >= column_sum_threshold and i < width_min:
#             width_min = i
#             index_column += 1
#             break
#         index_column += 1
#     for i in range(index_column, len(column_sums)):
#         if column_sums[i] >= column_sum_threshold and i > width_max:
#             width_max = i
#
#     result[height_min:height_max + 1, width_min:width_max + 1] = True
#     # '''调试3'''
#     # f, ax = pylab.subplots(nrows=1, ncols=1)
#     # ax.imshow(processed_filled_mask)
#     # ax.set_title('Processed Filled Mask', fontsize=10)
#     # print('调试3完成')
#     # '''调试3'''
#     return result


def get_masked_image(im, mask):
    """

    :param im:
    :param mask:
    :return:
    原图im是720*1280*3的矩阵，这个矩阵记录了原图的色彩信息。
    滤镜mask是720*1080的boolean矩阵（它的元素只有True和False）
    将mask套用在im上：如果mask的i行j列是False，那么就把im的第i行第j列设成黑色。
                    如果mask的i行j列是True，那么就保留im的第i行第j列，让其不变。
    """
    height, width = im.shape[:2]  # height is row and width is column
    # masked_image = im.copy()
    for i in range(height):
        for j in range(width):
            if mask[i, j] == 0:
                im[i, j, :] = 0
            else:
                pass
    return im


def get_soilpart_of_image(im, min_thresh=None, max_thresh=None):
    if max_thresh is None:
        max_thresh = [40, 70, 35, 110]  # 设定R-G, R-B, G-B, 2R-G-B的最大阈值。若某个像素的四个指标的任何一个超过对应阈值，它都不会被认为是泥土或者幼芽
    if min_thresh is None:
        min_thresh = [20, 35, 15, 70]  # 设定R-G, R-B, G-B, 2R-G-B的最小阈值。若某个像素的四个指标的任何一个小于对应阈值，它都不会被认为是泥土或者幼芽
    # im_blurred = cv2.blur(im, (7, 7))
    return get_masked_image(im, get_mask(im, min_thresh, max_thresh, ratio=0.20))  # 先获取mask，再将mask套用在原图上得到处理结果并返回。

# def plot_image(im, title):
#     f, ax = pylab.subplots(nrows=1, ncols=1)
#     ax.imshow(im)
#     ax.set_title(title, fontsize=10)
