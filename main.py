import time
import os
from skimage.io import imread, imsave
from soil_capture_RGB import *

# IMAGE_SOIL = 'sample_day1_soil.jpeg'
# IMAGE_SOIL_SPROUTED = 'sample.jpeg'
# IMAGE_SOIL_CROPPED_SPROUTED = 'sample_cropped.jpeg'
# IMAGE_SAND_SPROUTED = 'sample_sand.jpeg'
# IMAGE_SAND = 'day1_sand.jpeg'
# IMAGE_SAND_CROPPED_SPROUTED = 'sample_sand_cropped.jpeg'
# IMAGE_TEST = 'rgb_20220403_125355.jpeg'
# IMAGE_TEST_2 = 'C:\\Users\\randm\\Desktop\\Realsense_Data\\20220405\\6\\rgb_20220405_131505.jpeg'
# IMAGE_TEST_3 = 'C:\\Users\\randm\\Desktop\\Realsense_Data\\20220405\\7\\rgb_20220405_132154.jpeg'
SOURCE_DIR = 'source'
DEST_DIR = 'result'
if __name__ == "__main__":
    total_time = 0
    if not os.path.exists(DEST_DIR):
        os.mkdir(DEST_DIR)
    num_file = 0
    g = os.walk(SOURCE_DIR)

    for path, dir_list, file_list in g:
        num_file = len(file_list)
        file_processed = 0
        print("已处理：{}/{}".format(file_processed, num_file))
        for file in file_list:
            start_time = time.time()
            output_path = os.path.join(DEST_DIR, '{}_cropped.jpeg'.format(os.path.basename(file)))
            image = imread(os.path.join(SOURCE_DIR, file))
            masked_im = soilCapture(image)
            imsave(output_path, masked_im, quality=100)
            file_processed += 1
            terminal_time = time.time()
            total_time += terminal_time - start_time
            print("已处理：{}/{}，用时{:.3f}s.".format(file_processed, num_file, terminal_time - start_time))

    print("完成！共{}个文件，平均用时{:.3f}秒".format(num_file, total_time / num_file))

    # plot_image(image, 'Original')
    # # f, (ax1, ax2, ax3) = pylab.subplots(1, 3)
    # # ax1.imshow(color_diff[0], cmap='gray')
    # # ax1.set_title('R-G', fontsize=title_size)
    # # ax2.imshow(color_diff[1], cmap='gray')
    # # ax2.set_title('R-B', fontsize=title_size)
    # # ax3.imshow(color_diff[2], cmap='gray')
    # # ax3.set_title('G-B', fontsize=title_size)
    # # f, ax = pylab.subplots(1, 1)
    # # ax.imshow(color_diff[3], cmap='gray')
    # # ax.set_title('green diff = 2G-B-R', fontsize=title_size)
    # plot_image(masked_im, 'Masked Image')
    # plt.show()
