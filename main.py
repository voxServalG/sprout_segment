import time
import os
from skimage.io import imread, imsave
from soil_capture_RGB import *


SOURCE_DIR = 'source'
DEST_DIR = 'result'
if __name__ == "__main__":
    total_time = 0
    if not os.path.exists(DEST_DIR):
        os.mkdir(DEST_DIR)
    num_file = 0

    '''
    遍历SOURCE_DIR
    '''
    g = os.walk(SOURCE_DIR)

    for path, dir_list, file_list in g:
        num_file = len(file_list)
        file_processed = 0
        print("已处理：{}/{}".format(file_processed, num_file))

        '''
        对SOURCE_DIR里的文件逐一处理
        '''
        for file in file_list:
            start_time = time.time()

            '''
            创建图片文件，处理结果存放在这个图片。这个图片后续会保存到DEST_DIR
            '''
            output_path = os.path.join(DEST_DIR, '{}_cropped.jpeg'.format(os.path.basename(file)))

            image = imread(os.path.join(SOURCE_DIR, file))  # 读取一个图片文件到image变量
            masked_im = get_soilpart_of_image(image)  # 将处理后的图片存到masked_im变量
            imsave(output_path, masked_im, quality=100)  # 保存图片到DEST_DIR中
            file_processed += 1
            terminal_time = time.time()
            total_time += terminal_time - start_time
            print("已处理：{}/{}，用时{:.3f}s.".format(file_processed, num_file, terminal_time - start_time))

    print("完成！共{}个文件，平均用时{:.3f}秒".format(num_file, total_time / num_file))

