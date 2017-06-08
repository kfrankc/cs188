import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.color import rgb2gray

import json
from random import randint

debug = True

def generate_mask(img, r, c):
	[rowMax, colMax] = img.shape
	if (r < rowMax-1 and c < colMax-1 and r > 0 and c > 0):
		if debug:
			print "inside generate_mask: r: %i, c: %i" %(r, c)
		return np.array([[img[r-1][c-1], img[r-1][c], img[r-1][c+1]],
						  [img[r][c-1], img[r][c], img[r][c+1]],
						  [img[r+1][c-1], img[r+1][c], img[r+1][c+1]]
						 ])

def next_pixel(pixel_matrix):
	# returns the next likely pixel offset 
	# (-1, -1) (-1, 0) (-1, +1)
	# (0, -1)  (0, 0)  (0, +1)
	# (+1, -1) (+1, 0) (+1, +1)
 	# if none, found, return plain (0, 0)
 	[rowMax, colMax] = np.shape(pixel_matrix)
 	if debug:
 		print pixel_matrix
 	for r in xrange(0, 3, 1):
 		for c in xrange(0, 3, 1):
 			if (r == 1 and c == 1):
 				continue
 			if (pixel_matrix[r][c] == 1):
 				if debug:
 					print "Found in next_pixel! (%i, %i)" %(r, c)
 				return [r-1, c-1]
 	return [0, 0]

    #  ```````````::hdydmmyosys/.``````````````     
    #  ````````-odNNNhhhymNNNNNMNh:````````````     
    #  ``````odmy:.``   `-+hNNNNMMMNs.`````````     
    #  ````hdNy.            -+ymNMNMMm+````````     
    #  ```+Nh-                `/mNMNMMMh.``````     
    #  `-dMN-`                 .dNNNNMMMy``````     
    #  `oMMs.`           ``.   `+dNMNMMMm``````     
    #  `yMh-+oso.        -:+os+---sNNNMMN:`````     
    #  `od:so+ohs+-  `/ydmNNNNMNmy./shNNMdd.```     
    # `sdNMMMNMMMMMNNNNNNNNNddNMmmysyshNmmy````     
    #  hNMMMNMMMMMMh/sMMNNNNmmmNm+-`+my/so.````     
    #  `/NMMMMMMMMy`  /mMMNNNNmm.   .+/`.`.````     
    #  ``+NMMMMMNy`    `:oyhydy.   `.-`. -`````     
    #  ``::yyoo/..`    .`         `.-.:.:d+````     
    #  ``-:`    -+hoo+o+/`       ``.:yooNmhh```     
    #  ```+.```.-:odysso+:.`     ``.:NNMMMhy```     
    #  ```.+...-sd+:--/+++h+` ``...:yNMMMMms```     
    #  ````oh/:hdho:--``.:+-```..-:sNMMMMNMd:``     
    #  ````-y/:::+syhdhs/-` ``..-+sNNNMMMMd+s:`     
    #  `````:+-/:-:/:/.`  `````./smNdNMMMMmy.-`     
    #  ``````.+os////:+/...-/yhs/``y`/mNMd`-o+`     
    #  ````````:hmmNMMMMNNNMNy-````/+.ssy+:+-``     
    #  ``````````-oydmmmmds+-``````````````````
def mask_off(img, r, c):
	img[r-1][c-1] = 0
	img[r-1][c] = 0
	img[r-1][c+1] = 0
	img[r][c-1] = 0
	img[r][c] = 0
	img[r][c+1] = 0
	img[r+1][c-1] = 0
	img[r+1][c] = 0
	img[r+1][c+1] = 0
	return img

def search(search_list, img, r, c):
	[rowMax, colMax] = img.shape
	# takes in (r, c), recursively returns list
	if debug:
		print "search_list length: %i" %(len(search_list))
	# look for neighbors and their pixel intensity
	pixel_matrix = generate_mask(img, r, c)
	[r_offset, c_offset] = next_pixel(pixel_matrix)
	if debug:
		print "r_offset: %i, c_offset: %i" %(r_offset, c_offset)
	img = mask_off(img, r, c)
	new_r = r + r_offset
	new_c = c + c_offset
	# stopping condition: offsets are zero OR goes out of bound
	if ((r_offset == 0 and c_offset == 0) or (new_r >= rowMax - 1) or (new_c >= colMax - 1)):
		return search_list
	if debug:
		print "new_r: %i, new_c: %i" %(new_r, new_c)
	search_list.append((new_r, new_c))
	return search(search_list, img, new_r, new_c)


def find_path(img_gray):
	# return array of tuples, containing (in order) the (x, y) coordinates of the skeletonization path

	path_list = []
	search_list = []

	# start at (rowMax, 0)
	# move to (rowMax, colMax), then move to (rowMax -1, 0)...
	# stop at (0, colMax)
	fin = False
	[rowMax, colMax] = img_gray.shape
	for r in xrange(rowMax-2, 1, -1):
		for c in xrange(2, colMax-2, 1):
			if img_gray[r][c] == 1:
				path_list.append((r, c))
				# check neighbors for next white pixel
				if debug:
					print "inside find_path double for loop: r: %i, c: %i" %(r, c)
				path_list = path_list + search(search_list, img_gray, r, c)
				fin = True
				break
		if (fin):
			break
	return [path_list, img_gray]

skel = imread('skel3.png')
# greyscale the image
img_gray = rgb2gray(skel)
path_list = []
path_exist = True
while path_exist:
	[path, img_gray] = find_path(img_gray)
	if not path:
		path_exist = False
	path_list.append(path)

fig = plt.figure(frameon=False)
plt.imshow(img_gray, interpolation='nearest')
plt.pause(0)
plt.draw()

# # Save as json
# with open('test.json', 'wb') as outfile:
#     json.dump(path_list, outfile)

im = rgb2gray(skel)

# visualize list on top of original file
I = np.dstack([im, im, im])
for path in path_list:
	color = [randint(0,1), randint(0,1), randint(0,1)]
	for tup in path:
		I[tup[0], tup[1], :] = color
plt.imshow(I, interpolation='nearest')
plt.pause(0)
plt.draw()