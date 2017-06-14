import math # 'math' needed for 'sqrt'
from sys import maxint

def euclidean_dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
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

def get_new_endpt_dict(seg, new_endpt_dict, roots):
	# return dictionary of endpoints as keys and segments_key as value
	if seg.seg_id in roots:
		new_endpt_dict[seg.path[0]] = seg.seg_id
	if seg.children is None:
		new_endpt_dict[seg.path[-1]] = seg.seg_id
		return
	else:
		for child in seg.children:
			get_new_endpt_dict(child, new_endpt_dict, roots)

def get_endpt_dict(segments, roots, endpt_dict):
	for root in roots:
		get_new_endpt_dict(segments[root], endpt_dict, roots)

def endpt_compare(new_endpt_dict, endpt_dict):
	# return the value in new_endpt_dict that has the closest euclidean distance
	min_dist = maxint
	ret_id = -1
	for p1, new_seg_id in new_endpt_dict.iteritems():
		for p2, seg_id in endpt_dict.iteritems():
			dist = euclidean_dist(p1, p2)
			if dist < min_dist:
				min_dist = dist
				ret_id = new_seg_id
	return ret_id

def reverse_path(segments, parent, seg, key, roots):
	# reverse path
	if (seg.children is None) or (parent in seg.children):
		seg.parent = parent
		seg.path = seg.path[::-1]
		seg.children = None
		return
	else:
		parent = seg.parent
		seg.add_to_children(segments[parent.seg_id])
		for child in parent.children:
			if child.seg_id == seg.seg_id:
				continue
			else:
				seg.add_to_children(segments[child.seg_id])
		# add junction to seg from seg's parent
		seg.add_junction(parent.junction)
		seg.parent = parent
		for child in seg.children:
			reverse_path(segments, seg, child, child.seg_id, roots)

def change_orientation(segments, roots, seg, new_root_key):
	# update root key in roots
	[new_root_key if root==seg.seg_id else root for root in roots]

	# perform reverse on the segment path graph, starting from new root
	seg = segments[new_root_key]
	seg.path = seg.path[::-1]
	# if no parent, this is the right choice already, so do nothing
	if seg.parent is None:
		return
	# add seg's parent and seg's siblings to seg's children
	parent = seg.parent
	seg.add_to_children(segments[parent.seg_id])
	for child in parent.children:
		if child.seg_id == seg.seg_id:
			continue
		else:
			seg.add_to_children(segments[child.seg_id])
	# add junction to seg from seg's parent
	seg.add_junction(parent.junction)
	seg.parent = None
	for child in seg.children:
		reverse_path(segments, seg, child, child.seg_id, roots)

def check_direction(segments, roots, seg):
	# get the segment endpts from root seg that needs to be checked
	# format: {
	#			(r, c): segments_key
	#			...
	#		  }
	new_endpt_dict = {}
	get_new_endpt_dict(seg, new_endpt_dict, roots)

	# roots[:-1] everything except last root in roots list
	endpt_dict = {}
	get_endpt_dict(segments, roots[:-1], endpt_dict)

	# new_root_key: integer
	new_root_key = endpt_compare(new_endpt_dict, endpt_dict)
	if (new_root_key == -1 or new_root_key == roots[-1]):
		print "new root key and old root key are the same"
		return
	print "new root key: %i" %(new_root_key)

	# update segments and roots with correct orientation
	change_orientation(segments, roots, seg, new_root_key)