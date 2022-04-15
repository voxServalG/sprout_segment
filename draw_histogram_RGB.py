import numpy as np
import matplotlib.pyplot as plt
import skimage


FILE_NAME = '.\\sample.jpeg'
img = skimage.io.imread(FILE_NAME)
img_red, img_green, img_blue = img[:, :, 0], img[:, :, 1], img[:, :, 2]

fig, ax = plt.subplots(2, 3)
ax[0, 0].imshow(img_red, cmap='gray')
ax[0, 1].imshow(img_green, cmap='gray')
ax[0, 2].imshow(img_blue, cmap='gray')

bins = np.arange(-0.5, 255+1, 1)
ax[1, 0].hist(img_red.flatten(), bins=bins, color='r')
ax[1, 1].hist(img_green.flatten(), bins=bins, color='g')
ax[1, 2].hist(img_blue.flatten(), bins=bins, color='b')

plt.show()
