#! /usr/bin/env python

# import dicom
import mudicom
# import cv2
import numpy as np
from matplotlib import pyplot as plt
# from PIL import Image

from skimage.color import rgb2gray
from skimage.filters import threshold_mean
from skimage import util
from skimage.filters.rank import median
from skimage.morphology import disk
from skimage.morphology import skeletonize
from skimage.morphology import binary_dilation
from skimage.morphology import binary_erosion
from skimage.morphology import binary_closing

from skimage.transform import probabilistic_hough_line

# ds = dicom.read_file("2d_angiogram_2.dcm")
mu = mudicom.load("2d_angiogram_1.dcm")
mu_out = mu.image
pixel_array = mu_out.numpy
i = 1
fig2, ax = plt.subplots(2, 2, figsize=(10, 8))
for frame in pixel_array:

	# OUTDATED - kept for future reference
	# kernel = np.ones((25, 25), np.float32)/25
	# dst = cv2.filter2D(frame, -1, kernel)
	# th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
	# img = Image.fromarray(frame).convert('RGB')
	# npimg = np.array(img)
	# open_cv_img = npimg[:, :, ::-1].copy() 
	# imgrey = cv2.cvtColor(npimg, cv2.COLOR_BGR2GRAY)

	# greyscale the image
	img_gray = rgb2gray(frame)
	# Reference: http://scikit-image.org/docs/dev/auto_examples/xx_applications/plot_thresholding.html
	thresh = threshold_mean(img_gray) - 100
	print thresh
	binary = img_gray > thresh
	binary_invert = util.invert(binary)

	# median filter
	med = median(binary_invert, disk(10))

	# skeletonize
	med[med == 255] = 1
	skeleton = skeletonize(med)

	kernel = np.ones((20,20), np.uint8)  # note this is a HORIZONTAL kernel
	dilate = binary_dilation(skeleton, kernel)
	erode = binary_erosion(dilate, kernel) 

	closed = binary_closing(erode)
	skel = skeletonize(closed)
	final_img = skel

	# # Display
	# # Save; note: convert -delay 20 -loop 0 *png skeleton.gif converts to gif
	# fig = plt.gcf()
	# plt.axis('off')
	# plt.imshow(final_img, cmap=plt.cm.bone, bbox_inches=0)
	# # fig.savefig('./img/' + str(i) + '.png')
	# plt.pause(.1)
	# plt.draw()

	ax[0,0].imshow(frame, cmap=plt.cm.bone)
	ax[0,0].set_title('Input image')
	ax[0,0].axis('image')
	ax[0,1].imshow(dilate, cmap=plt.cm.bone)
	ax[0,1].set_title('Dilation')
	ax[0,1].axis('image')
	ax[1,0].imshow(closed, cmap=plt.cm.bone)
	ax[1,0].set_title('Closing')
	ax[1,0].axis('image')
	ax[1,1].imshow(final_img, cmap=plt.cm.bone)
	ax[1,1].set_title('Final Image')
	ax[1,1].axis('image')
	# fig2.savefig('./img/' + str(i) + '.png')
	plt.pause(.1)
	plt.draw()
	i = i + 1

