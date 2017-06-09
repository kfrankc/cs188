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

 # Input: (x,y)
 # Output: {"x": x, "y":y}
def tuple_to_dict(val):
    x,y = val
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


def write_to_json(vector_field, starting_points=None, filename="data.json", indent=None):
    """
    output:
        {
            "starting_points": [{"x": 1, "y":1}, {"x": 2, "y":2}],    # these are coordinates
            "starting_points": "ALL",
            "vector_field": [
                                [{"x": 1, "y":1}, {"x": 2, "y":2}],   # these are vectors
                                [{"x": 1, "y":1}, {"x": 2, "y":2}]
                            ]
        }
    """

    if starting_points != "ALL":
        starting_points = map(tuple_to_dict, starting_points)
    data = {
        "vector_field": vector_field,
        "starting_points": starting_points,
    }

    with open(filename, "w") as output:
        output.write(json.dumps(data, indent=indent))


def run():
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


        write_to_json(vec_field, path_array, indent=1)

        # Valid
        #print(json.dumps(path_array, indent=2))

def test_data():
    n = 150
    vector_field = []
    for x in range(n):
        vector_field.append([])
        for y in range(n):
            vector_field[x].append(create_vector(1,1))

    starting_points = []
    for x in range(n):
        for y in range(n):
            starting_points.append((x,y))

    #write_to_json(vector_field, starting_points, filename="test.json", indent=1)
    write_to_json(vector_field, "ALL", filename="test-all.json", indent=1)

    
test_data()
#run()


