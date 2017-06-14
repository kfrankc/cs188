#! /usr/bin/env python
from __future__ import print_function
import json
import dicom
from pprint import pprint
from scipy import misc
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec

from skimage.color import rgb2gray
from skimage.filters import threshold_mean
from skimage import util
from skimage.filters.rank import median
from skimage.filters import rank
from skimage.morphology import disk, skeletonize, binary_dilation, binary_erosion, binary_closing
from scipy import ndimage

frames = dicom.read_file("2d_angiogram_1.dcm").pixel_array

def threshold_percentile(image, percentile):
    """
    input: image: np 2d array
           percentile: float
    """
    values = np.sort(image.ravel())
    index = int(percentile*len(values))
    return values[index]

fig1 = plt.figure(frameon=False)
ax1 = plt.Axes(fig1, [0., 0., 1., 1.])
fig1.set_size_inches(5.12, 5.12)
ax1.set_axis_off()
fig1.add_axes(ax1)

for i, image in enumerate(frames):
    print(i)

    fig, ax = plt.subplots(1, 3, figsize=(12, 6))
    fig.subplots_adjust(hspace=.5)
    fig.tight_layout(pad=1.5, w_pad=4, h_pad=4)

    # fig = plt.figure(figsize=(12, 6)) 
    # gs = gridspec.GridSpec(1, 3) 
    # ax0 = plt.subplot(gs[0])
    # ax1 = plt.subplot(gs[1])
    # ax2 = plt.subplot(gs[2])

    # greyscale the image
    image = rgb2gray(image)

    a = ax[0]
    a.imshow(image, cmap=plt.cm.gray)
    a.set_title('Grayscale of Original')
    a.axis('off')


    # percentile threshold
    threshold = min(600, threshold_percentile(image, 0.050))  #  hardcode 600
    filtered = image > threshold
    a = ax[2]
    a.imshow(filtered, cmap=plt.cm.gray)
    a.set_title("Filtered Image")
    a.axis('off')


    # historgram
    a = ax[1]
    a.hist(image.ravel(), bins=256)
    a.axvline(threshold, color='r')
    a.set_title("Intensity Histogram")

    fig.savefig('out/{}.png'.format(i))
    plt.close(fig)

    binary_invert = util.invert(filtered)
    med = median(binary_invert, selem=np.ones((18, 18)))
    med[med == 255] = 1
    skeleton = skeletonize(med)

    plt.axis('off')
    plt.imshow(skeleton, cmap=plt.cm.gray, aspect='auto')
    fig1.savefig('out' + '/skel' + str(i) + '.png', transparent=True)
    plt.pause(.1)
    plt.draw()