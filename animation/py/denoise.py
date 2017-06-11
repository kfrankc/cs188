#! /usr/bin/env python
from __future__ import print_function
import json
import dicom
from pprint import pprint
from scipy import misc
import numpy as np
from matplotlib import pyplot as plt

from skimage.color import rgb2gray
from skimage.filters import threshold_mean
from skimage import util
from skimage.filters.rank import median
from skimage.filters import rank
from skimage.morphology import disk, skeletonize, binary_dilation, binary_erosion, binary_closing
from scipy import ndimage

frames = dicom.read_file("2d_angiogram_1.dcm").pixel_array

#frames = []
#for i in range(19,19+1):
#for i in range(1,24):
    #frames.append(misc.imread('img/' + str(i) + '.png'))

def threshold_percentile(image, percentile):
    """
    input: image: np 2d array
           percentile: float
    """
    values = np.sort(image.ravel())
    index = int(percentile*len(values))
    return values[index]

total = np.zeros(shape=(1024,1024))

for i, image in enumerate(frames):
        #misc.imsave('out/{}-gray.png'.format(i), img_gray)
        print(i)
        #if i != 7:
            #continue


        fig, ax = plt.subplots(3, 3)
        fig.tight_layout()



	# greyscale the image
	image = rgb2gray(image)
        # denoise
        image = ndimage.median_filter(image, 3)

        a = ax[0, 0]
        a.imshow(image, cmap=plt.cm.gray)
        a.set_title('Grayscale of Original')
        a.axis('off')


        


        # mean threshold
	threshold = threshold_mean(image) - 100
	mean = image > threshold
        a = ax[0, 2]
        a.imshow(mean, cmap=plt.cm.gray)
        a.set_title('mean thresh - 100')
        a.axis('off')


        # percentile threshold
        per_thresh = threshold_percentile(image, 0.040)
        per_thresh = min(per_thresh, 600)
	percentile = image > per_thresh
        a = ax[1, 0]
        a.imshow(percentile, cmap=plt.cm.gray)
        a.set_title('percentile - ' + str(per_thresh))
        a.axis('off')


        med = median(percentile, disk(3))
        a = ax[1, 1]
        a.imshow(med, cmap=plt.cm.gray)
        a.set_title('Median Filter')
        a.axis('off')






        total += med








	#binary = median > 0
	##binary = util.invert(binary)
	#skeleton = skeletonize(binary)
        #a = ax[2, 1]
        #a.imshow(skeleton, cmap=plt.cm.gray)
        #a.set_title('skeleton')
        #a.axis('off')




	#img_gray = rgb2gray(image)
	#thresh = threshold_mean(img_gray) - 100
	#binary = img_gray > thresh
	#binary_invert = util.invert(binary)
	#med = median(binary_invert, disk(10))
	#med[med == 255] = 1
	#test = skeletonize(med)
        #a = ax[2, 0]
        #a.imshow(test, cmap=plt.cm.gray)
        #a.set_title('test')
        #a.axis('off')


        #print(type(image.ravel()), len(image.ravel()))
        #for j in len(image.ravel()):



        # historgram
        a = ax[0, 1]
        a.hist(image.ravel(), bins=256)
        a.axvline(threshold, color='r')
        a.axvline(per_thresh, color='g')
        a.set_title('hist of intense - ' + str(int(threshold)))
        a.set_yticklabels([])






	#fig.savefig('out/{}.png'.format(i), transparent=True)
	fig.savefig('out/{}.png'.format(i))

        #plt.show()
        plt.close(fig)
        continue








	thresh = threshold_mean(img_gray)
	binary = img_gray > thresh
        misc.imsave('thresh/{}-thresh.png'.format(i), image)
	#plt.imshow(binary, cmap=plt.cm.gray)
        #plt.show()
        continue


####################


        # denoise
        denoised = ndimage.median_filter(image, 10)
        a = ax[0, 1]
        a.imshow(denoised, cmap=plt.cm.gray)
        a.set_title('denoised')
        a.axis('off')




#threshold_percentile(image, 0.99)
total = total > 6000
print(total)
plt.imshow(total, cmap = plt.get_cmap('gray'))
plt.axis('off')
plt.savefig("out/total.png")
#plt.show()

with open("total.json", "w") as output:
    output.write(json.dumps(total, indent=2))




