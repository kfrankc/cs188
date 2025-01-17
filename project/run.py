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
from skimage.filters import median
from skimage.morphology import disk, skeletonize, binary_dilation, binary_erosion, binary_closing

# from skimage.exposure import equalize_adapthist

# ds = dicom.read_file("2d_angiogram_2.dcm")
img_id = 1
mu = mudicom.load("2d_angiogram_" + str(img_id) + ".dcm")
mu_out = mu.image
pixel_array = mu_out.numpy

# with open("pixel_array", "w") as f:
# 	np.save(f, pixel_array)
# exit()

i = 1

# fig2, ax = plt.subplots(2, 2, figsize=(10, 8))

fig = plt.figure(frameon=False)
ax = plt.Axes(fig, [0., 0., 1., 1.])
fig.set_size_inches(5.12, 5.12)
ax.set_axis_off()
fig.add_axes(ax)

for frame in pixel_array:

	# OUTDATED - kept for future reference
	# kernel = np.ones((25, 25), np.float32)/25
	# dst = cv2.filter2D(frame, -1, kernel)
	# th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
	# img = Image.fromarray(frame).convert('RGB')
	# npimg = np.array(img)
	# open_cv_img = npimg[:, :, ::-1].copy() 
	# imgrey = cv2.cvtColor(npimg, cv2.COLOR_BGR2GRAY)

	# thresh = equalize_adapthist(frame, kernel_size=None, clip_limit=0.01, nbins=256)

	# greyscale the image
	img_gray = rgb2gray(frame)
	thresh = threshold_mean(img_gray) - 100
	# Reference: http://scikit-image.org/docs/dev/auto_examples/xx_applications/plot_thresholding.html
	# thresh = threshold_mean(img_gray) - 100
	# print thresh

	# print np.shape(frame)
	binary = img_gray > thresh
	binary_invert = util.invert(binary)

	# diameter = 10
	# closed = binary_closing(binary_invert, np.ones((diameter, diameter)))

	# median filter
	med = median(binary_invert, selem=np.ones((18, 18)))
	# med = median(binary_invert, disk(10))
	# med = binary_invert

	# skeletonize
	med[med == 255] = 1
	skeleton = skeletonize(med)

	dkernel = np.ones((4,4), np.uint8)
	# ekernel = np.ones((18,18), np.uint8)
	dilate = binary_dilation(skeleton, dkernel)
	# erode = binary_erosion(dilate, ekernel) 

	# skel = skeletonize(erode)
	final_img = dilate

	# Display
	# Save; note: convert -delay 20 -loop 0 *png skeleton.gif converts to gif
	plt.axis('off')
	plt.imshow(med, cmap=plt.cm.bone, aspect='auto')
	fig.savefig('./img'+ str(img_id) + '/' + str(i) + '.png', transparent=True)
	plt.pause(.1)
	plt.draw()

	# ax[0,0].imshow(frame, cmap=plt.cm.bone)
	# ax[0,0].set_title('Input Image')
	# ax[0,0].axis('image')
	# ax[0,1].imshow(med, cmap=plt.cm.bone)
	# ax[0,1].set_title('Median Filter')
	# ax[0,1].axis('image')
	# ax[1,0].imshow(skeleton, cmap=plt.cm.bone)
	# ax[1,0].set_title('Skeletonization')
	# ax[1,0].axis('image')
	# ax[1,1].imshow(final_img, cmap=plt.cm.bone)
	# ax[1,1].set_title('Dilation')
	# ax[1,1].axis('image')
	# # fig2.savefig('./img'+ str(img_id) + '/' + str(i) + '.png')
	# plt.pause(.1)
	# plt.draw()

	i = i + 1

