#! /usr/bin/env python
from __future__ import print_function
import json
from pprint import pprint


# Input: point= [x,y]
# output: [y,x]
def transpose_x_y(point):
    return (point[1], point[0])

 # Input: (x,y)
 # Output: {"x": x, "y":y}
def tuple_to_dict(val):
    x,y = val
    return {
        "x": x,
        "y": y,
    }

# Input:
#  Tuple/Array like [(y1,x1), (y2,x2), ...]
#  Output: array of [{'x':x1, 'y':y1}, {'x':x2,'y':y2}, ...]
"""
Frank:
      y
    +--->  
 x  |
    V
Arvin:
      x
    +--->  
 y  |
    V
"""
def convert_frank_to_arvin(path_array):
    transposed = map(transpose_x_y, path_array)
    return map(tuple_to_dict, transposed)

def create_vector(x,y):
    return {
        "x": x,
        "y": y,
    }

def get_x(point):
    """
    { x: x, y: y}
    """

    return point["x"]

def get_y(point):
    """
    { x: x, y: y}
    """

    return point["y"]


# Input: array of points
# output: array of vectors to the next point # TODO
def get_vectors(path_array):
    vectors = []
    for i in range(len(path_array)):
        # check for last pixel of segment
        # segment ended. vector to nowhere...
        if i == len(path_array) - 1: 
            vectors.append(create_vector(0,0))
        else:
            x1, y1 = get_x(path_array[i]), get_y(path_array[i])
            x2, y2 = get_x(path_array[i+1]), get_y(path_array[i+1])
            vectors.append(create_vector(x2-x1, y2-y1))
    return vectors

def init_vec_field(width, height):
    """
    Create a vector field matrix with all (0,0)
    """

    vec_field = []
    for x in range(width):
        vec_field.append([])
        for y in range(height):
            vec_field[x].append(create_vector(0,0))

    return vec_field


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

    data = {
        "vector_field": vector_field,
        "starting_points": starting_points,
    }

    with open(filename, "w") as output:
        output.write(json.dumps(data, indent=indent))


def run():
    with open('path.json') as f:
        path_array = json.load(f)
        path_array = convert_frank_to_arvin(path_array)
        vectors = get_vectors(path_array)

        width  = 1024 # TODO: this is set manually for now...
        height = 1024

        # Init vec field with all (0,0)
        vec_field = init_vec_field(width,height)

        # Add in the path to the vec field
        for i, point in enumerate(path_array):
            x = get_x(point)
            y = get_y(point)
            vec_field[x][y] = vectors[i]


        write_to_json(vec_field, path_array, filename="data-paths.json", indent=1)
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
        starting_points.append((x, n-x))

    #write_to_json(vector_field, starting_points, filename="test.json", indent=1)
    #write_to_json(vector_field, "ALL", filename="test-all.json", indent=1)

    
#test_data()
run()

