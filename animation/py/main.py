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

def create_vector(x,y):
    return {
        "x": x,
        "y": y,
        }

# Input: array of points
# output: array of vectors to the next point # TODO
def get_vectors(path_array):
    vectors = []
    for i in range(len(path_array)):
        if i == len(path_array) - 1: # check for last pixel
            #vectors.append((0,0))     # segment ended. vector to nowhere...

            vectors.append({
                "x": 0,
                "y": 0,
            })

        else:
            x1, y1 = path_array[i]
            x2, y2 = path_array[i+1]
            vectors.append(create_vector(x2-x1, y2-y1))

            #vectors.append((x2-x1, y2-y1))   # tuple/array representation
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
            vec_field[x].append(create_vector(0,0))

    for i, (x, y) in enumerate(path_array):
        vec_field[x][y] = vectors[i]

    #print(json.dumps(vectors, indent=2))
    #print(vec_field[357][1022])
    print(json.dumps(vec_field, indent=2))


    # Valid
    #print(json.dumps(path_array, indent=2))

