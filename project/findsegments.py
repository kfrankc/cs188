import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.color import rgb2gray
from collections import deque

import json
from random import randint

from segment import Segment
from tools import euclidean_dist, mask_off, get_new_endpt_dict, get_endpt_dict, endpt_compare, reverse_path, change_orientation, check_direction

# set to True for all debug statements to print
debug = False

def generate_mask(img, r, c):
	[rowMax, colMax] = img.shape
	if (r < rowMax-1 and c < colMax-1 and r > 0 and c > 0):
		if debug:
			print "inside generate_mask: r: %i, c: %i" %(r, c)
		return np.array([[img[r-1][c-1], img[r-1][c], img[r-1][c+1]],
						  [img[r][c-1], img[r][c], img[r][c+1]],
						  [img[r+1][c-1], img[r+1][c], img[r+1][c+1]]
						 ])

def next_pixel(pixel_matrix, seg, queue, row, col):
	# returns the next likely pixel offset 
	# (-1, -1) (-1, 0) (-1, +1)
	# (0, -1)  (0, 0)  (0, +1)
	# (+1, -1) (+1, 0) (+1, +1)
 	# if none, found, return plain (0, 0)
 	if debug:
 		print pixel_matrix
 	[rowMax, colMax] = np.shape(pixel_matrix)
 	forked_ctr = 0
 	coord_list = []
 	for r in xrange(0, 3, 1):
 		for c in xrange(0, 3, 1):
 			if (r == 1 and c == 1):
 				continue
 			if (pixel_matrix[r][c] == 1):
 				forked_ctr = forked_ctr + 1
 				coord_list.append((row+(r-1), col+(c-1)))
 				if debug:
 					print "Found in next_pixel! (%i, %i)" %(r, c)

 	if forked_ctr == 1:
 		return [coord_list[0][0], coord_list[0][1], False]
 	elif forked_ctr > 1:
 		seg.add_junction(coord_list[0])
 		for i in xrange(1, forked_ctr, 1):
	 		fork = {}
	 		# fork["id"] = seg.seg_id + i
			if debug:
				print "seg.seg_id in next_pixel: %i" %(seg.seg_id)
	 		fork["parent"] = seg.seg_id
	 		fork["point"] = (coord_list[i][0], coord_list[i][1])
	 		queue.append(fork)
	 	return [row, col, True]
 	else:
 		return [row, col, False]

def search(seg, img, queue, r, c):
	[rowMax, colMax] = img.shape
	forked = False
	# takes in (r, c), recursively returns list
	if debug:
		print "seg length: %i" %(len(seg.path))
	# look for neighbors and their pixel intensity
	pixel_matrix = generate_mask(img, r, c)

	# stopping condition: if pixel_matrix is None; return
	if pixel_matrix is None:
		if debug:
			print "Reach stopping condition in search b/c pixel_matrix is None"
		return

	[new_r, new_c, forked] = next_pixel(pixel_matrix, seg, queue, r, c)
	img = mask_off(img, r, c)
	if debug:
		print "in search: r: %i, c: %i" %(r, c)
		print "in search: new_r: %i, new_c: %i" %(new_r, new_c)
	# stopping condition: offsets are zero OR goes out of bound OR reaches forks
	if ((new_r == r and new_c == c) or (new_r >= rowMax - 1) or 
		(new_c >= colMax - 1) or (new_r <= 0) or (new_c <= 0) or forked):
		if debug:
			print "Reach stopping condition in search, seg's id: %i" %(seg.seg_id)
		return
	seg.add_to_path(new_r, new_c)
	if debug:
		print "seg length after add_to_path: %i" %(len(seg.path))
	return search(seg, img, queue, new_r, new_c)

def find_path(img, segments, roots, queue, seg_counter):
	# add Segments to segments list 
	# return 1 if successfully added Segment object to segments
	# return 0 if there are no more paths in the image
	# return -1 if no more Segment objects to be found
	[rowMax, colMax] = img.shape

	# initial seed heuristic to find start of blood vessels
	# start at (rowMax, 0)
	# move to (rowMax, colMax), then move to (rowMax -1, 0)...
	# stop at (0, colMax)
	if not queue:
		for r in xrange(rowMax-2, 1, -1):
			for c in xrange(2, colMax-2, 1):
				if img[r][c] == 1:
					roots.append(seg_counter)
					seg = Segment(seg_counter)
					seg.add_to_path(r, c)
					if debug:
						print "seg_counter: %i" %(seg_counter)
						print "inside find_path double for loop: r: %i, c: %i" %(r, c)
					# recursively add to seg until complete, erase paths from image
					search(seg, img, queue, r, c)
					if debug:
						print "size of seg: %i; seg.seg_id: %i" %(len(seg.path), seg.seg_id)
					segments[seg_counter] = seg
					seg_counter = seg_counter + 1
					return [1, seg_counter]
		return [0, seg_counter]
	else:
		# perform BFS by popping queue
		while (queue):
			fork = queue.popleft()
			if debug:
				print "Parent: %i" %(fork["parent"])
			seg = Segment(seg_counter)
			r = fork["point"][0]
			c = fork["point"][1]
			seg.add_to_path(r, c)
			seg.add_parent(segments[fork["parent"]])
			if debug:
				print "seg.seg_id in find_path: %i" %(seg.seg_id)
			if debug:
				print "fork['id'] in find_path: %i" %(fork["id"])
			search(seg, img, queue, r, c)

			# add children back to parent seg
			segments[fork["parent"]].add_to_children(seg)
			# add children's first coords to parent
			segments[fork["parent"]].add_to_path(r, c)
			# add current seg to segments dict
			segments[seg_counter] = seg
			seg_counter = seg_counter + 1
		return [-1, seg_counter]

def mat_nonimplication(cur_frame, prev_frame):
	[rowMax, colMax] = cur_frame.shape
	ret_frame = np.ones((rowMax, colMax))
	for r in xrange(rowMax):
		for c in xrange(colMax):
			if cur_frame[r][c] == 1 and prev_frame[r][c] == 0:
				print "point: (%i, %i)" %(r, c)
				ret_frame[r][c] = 1
			else:
				ret_frame[r][c] = 0
	return ret_frame

# MAIN SCRIPT 

seg_arrays = []
prev_frame = None
disp_vessels = False
for i in xrange(8, 9, 1):
	print "frame: %i" %(i)
	skel = imread('find_path_test_img/' + str(i) + '.png')
	# greyscale the image
	cur_frame = rgb2gray(skel)

	# perform abjunction (cite: https://www.wikiwand.com/en/Material_nonimplication)
	if (disp_vessels):
		print "got here"
		ret_frame = mat_nonimplication(cur_frame, prev_frame)
		cur_frame = np.copy(ret_frame)

	if prev_frame is not None:
		fig, ax = plt.subplots(1, 2, figsize=(10, 8))
		ax[0].imshow(cur_frame, cmap=plt.cm.bone)
		ax[0].set_title('Return Frame')
		ax[0].axis('image')
		ax[1].imshow(prev_frame, cmap=plt.cm.bone)
		ax[1].set_title('Prev Frame')
		ax[1].axis('image')
		plt.pause(0)
		plt.draw()

	prev_frame = np.copy(cur_frame)

	# array of Segment objects
	segments = {}
	roots = []
	path_exist = True
	seg_counter = 1
	queue = deque()
	while path_exist:
		[rc, seg_counter] = find_path(cur_frame, segments, roots, queue, seg_counter)
		if (rc == 1):
			disp_vessels = True
		if debug:
			print "returned rc: %i, seg_counter: %i" %(rc, seg_counter)
		if (rc == -1):
			# begin a new path, so re-initialize queue for BFS
			queue = deque()
			# check that path is pointing in the right direction
			# only want to check direction after adding initial segment (change later, since this approach is not robust)
			if (len(roots) > 1):
				seg = segments[roots[-1]]
				print "old root key: %i" %(roots[-1])
				check_direction(segments, roots, seg)
		elif (rc == 0):
			path_exist = False

	# Save as json
	seg_array = []
	# if debug:
	print "length of segments dict: %i" %(len(segments))
	print "length of root list: %i" %(len(roots))

	for seg_id, segment in segments.iteritems():
		seg_array.append(segment.path)
	seg_arrays.append(seg_array)

	im = rgb2gray(skel)

	# visualize list on top of original file
	fig = plt.figure(frameon=False)
	ax = plt.Axes(fig, [0., 0., 1., 1.])
	fig.set_size_inches(5.12, 5.12)
	ax.set_axis_off()
	fig.add_axes(ax)
	I = np.dstack([im, im, im])
	for seg_id, segment in segments.iteritems():
		color = [randint(0,1), randint(0,1), randint(0,1)]
		for tup in segment.path:
			I[tup[0], tup[1], :] = color
	plt.imshow(I, interpolation='nearest')
	plt.pause(0)
	plt.draw()

with open('test.json', 'wb') as outfile:
	json.dump(seg_arrays, outfile)