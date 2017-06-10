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

def create_point(x,y):
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

def get_starting_points(vec_field):
    """
    """
    
    starting_points = []
    for x in range(len(vec_field)):
        for y in range(len(vec_field[x])):
            vec = vec_field[x][y]
            x = vec['x']
            y = vec['y']
            if x==0 and y==0:
                continue
            else:
                starting_points.append(create_point(x,y))

    return starting_points


def shift_points(points, x_delta, y_delta):
    """
        Input: array of points: [{x:x, y:y},{}]
        x: amount to shift
        y: amount to shift
    """
    
    coordinates = []
    for point in points:
        x = get_x(point)
        y = get_y(point)
        coordinates.append(create_point(x + x_delta, y + y_delta))

    return coordinates


def format_to_file(vector_field, starting_points=None, filename="data.json", indent=None):
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


def write_to_json(data, filename, indent=None):
    with open(filename, "w") as output:
        output.write(json.dumps(data, indent=indent))


def add_to_vec_field(coordinates, vectors, vec_field):
    """
    Input:
        coordinates:  array of coords - [{x,y}, {x,y}, ...]
        vectors:  array of vectors - [{x,y}, {x,y}, ...]
        vec_field:  [[{}],
                     [],
                    ]
    Coordinates should correspond to vector at same index
    """

    # Add in the path to the vec field
    for i, point in enumerate(coordinates):
        x = get_x(point)
        y = get_y(point)
        vec_field[x][y] = vectors[i]


def run():
    with open('path.json') as f:
        path_array = json.load(f)
        path_array = convert_frank_to_arvin(path_array)
        vectors = get_vectors(path_array)


        width  = 1024 # TODO: this is set manually for now...
        height = 1024


        # Init vec field with all (0,0)
        vec_field = init_vec_field(width,height)
        add_to_vec_field(path_array, vectors, vec_field)

        #format_to_file(vec_field, path_array, filename="data-paths.json", indent=1)
        format_to_file(vec_field, get_starting_points(vec_field), filename="data-paths.json", indent=1)
        format_to_file(vec_field, "ALL", filename="data-all.json", indent=1)



        # left
        #for i in range(5):
            #new_path = shift_points(path_array, -1*i, 0)
            #add_to_vec_field(new_path, get_vectors(new_path), vec_field)
        # right
        #for i in range(5):
            #new_path = shift_points(path_array, i, 0)
            #add_to_vec_field(new_path, get_vectors(new_path), vec_field)
        # up
        #for i in range(10):
            #new_path = shift_points(path_array, 0, -i+1)
            #add_to_vec_field(new_path, get_vectors(new_path), vec_field)


        #write_to_json(path_array, "corrected-path.json", indent=2)
        #write_to_json(get_vectors(shift_points(path_array, -1, -1)), "corrected-path.shifted.json", indent=2)
        #write_to_json(shift_points(path_array, -1, -1), "corrected-path.shifted.json", indent=2)

def test_data():
    n = 150
    vector_field = []
    for x in range(n):
        vector_field.append([])
        for y in range(n):
            vector_field[x].append(create_vector(1,1))

    starting_points = []
    for x in range(n):
        starting_points.append(create_vector(x, n-x))

    format_to_file(vector_field, starting_points, filename="test-paths.json", indent=1)
    #format_to_file(vector_field, "ALL", filename="test-all.json", indent=1)

    
#test_data()
run()

