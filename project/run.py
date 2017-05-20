#! /usr/bin/env python
from __future__ import print_function
import sys

import dicom
# import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')       # See: http://stackoverflow.com/questions/4931376/generating-matplotlib-graphs-without-a-running-x-server
import matplotlib.pyplot as plt
# from PIL import Image

from skimage.color import rgb2gray
from skimage.filters import threshold_mean
from skimage import util
from skimage.filters.rank import median
from skimage.morphology import disk
from skimage.morphology import skeletonize

if (len(sys.argv)) < 3:
    print("Missing argument")
    print("Usage: {} <path_to_dicom> <output_directory>".format(sys.argv[0]))
    exit(1)
dicom_file = sys.argv[1]
output_dir = sys.argv[2]

ds = dicom.read_file(dicom_file)
i = 1
for frame in ds.pixel_array:

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
	print(thresh)
	binary = img_gray > thresh
	binary_invert = util.invert(binary)

	# median filter
	med = median(binary_invert, disk(5))

	# skeletonize
	med[med == 255] = 1
	skeleton = skeletonize(med)
	final_img = skeleton

	# Display
	# Save; note: convert -delay 20 -loop 0 *png skeleton.gif converts to gif
	fig = plt.gcf()
	fig.savefig(output_dir + '/' + str(i) + '.png')
	plt.imshow(skeleton, cmap=plt.cm.bone)
	plt.pause(.1)
	plt.draw()
	i = i + 1

