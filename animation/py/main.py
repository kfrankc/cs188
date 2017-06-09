#! /usr/bin/env python
from __future__ import print_function
import json
from pprint import pprint


# Input: point= [x,y]
# output: [y,x]
def transpose_x_y(point):
    return (point[1], point[0])

# Input:
#  array of [x,y]
# Output: array of [y,x]
def transpose_points(path_array):
    return map(transpose_x_y, path_array)

# Input: array of points
# output: array of vectors to the next point
def get_vectors(path_array):
    vectors = []
    for i in range(len(path_array)):
        if i == len(path_array) - 1: # check for last pixel
            vectors.append((0,0))     # segment ended. vector to nowhere...
        else:
            x1, y1 = path_array[i]
            x2, y2 = path_array[i+1]
            vectors.append((x2-x1, y2-y1))
    return vectors


with open('path.json') as f:    
    path_array = json.load(f)
    path_array = transpose_points(path_array)
    vectors = get_vectors(path_array)

    width  = 1024
    height = 1024
    vec_field = []

    for x in range(width):
        vec_field.append([])
        for y in range(height):
            vec_field.append((0,0))

    pprint(vec_field)



            

    #pprint(get_vectors(path_array))
