#! /usr/bin/env python
from __future__ import print_function
import json
from pprint import pprint
from copy import deepcopy

def write_to_json(data, filename, indent=None):
    with open(filename, "w") as output:
        output.write(json.dumps(data, indent=indent))


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

def create_vector(x,y,m=0):
    return {
        "x": x,
        "y": y,
        "m": m,
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
def get_vectors(path_array, m=1):
    vectors = []
    for i in range(len(path_array)):
        # check for last pixel of segment
        # segment ended. vector to nowhere...
        if i == len(path_array) - 1: 
            vectors.append(create_vector(0,0,0))
        else:
            x1, y1 = get_x(path_array[i]), get_y(path_array[i])
            x2, y2 = get_x(path_array[i+1]), get_y(path_array[i+1])
            vectors.append(create_vector(x2-x1, y2-y1, m))
    return vectors

def init_vec_field(width, height):
    """
    Create a vector field matrix with all (0,0)
    """

    vec_field = []
    for x in range(width):
        vec_field.append([])
        for y in range(height):
            vec_field[x].append(create_vector(0,0,1))

    return vec_field

def get_starting_points(vec_field):
    """
    """
    
    starting_points = []
    for x in range(len(vec_field)):
        for y in range(len(vec_field[x])):
            vec = vec_field[x][y]
            vecx = vec['x']
            vecy = vec['y']

            if vecx==0 and vecy==0:
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

def get_magnitude(i):
    # heuristic
    d = {
         0: 1,
         1: 1,
         2: 1,
         3: 1,
         4: 1,
         5: 1,
         6: 3,
         7: 2,
         8: 2,
         9: 2,
        10: 2,
        11: 2,
        12: 1,
        13: 1,
        14: 1,
        15: 1,
        16: 1,
        17: 2,
        18: 2,
        19: 2,
        20: 2,
        21: 2,
        22: 2,
        23: 1,
    }

    return d[i]

def truncate(x, y, boundx, boundy):
    """
    inclusive bound
    """

    if x < 0:
        x = 0
    if boundx < x:
        x = boundx
    if y < 0:
        y = 0
    if boundy < y:
        y = boundy

    return (x,y)

def get_points_to_explore(start_x, start_y, side_length, x_bound, y_bound):
    """
    input: 
        bound: inclusive

    print out values at side_length = 3 to understand


    unfinished
    doing spiral generator would probably be better
    """
    if side_length <= 0:
        raise Exception("side_length must be greater than 0")
    if side_length%2 == 0:
        raise Exception("side_length must be odd")

    if side_length == 1:
        return [(start_x, start_y)]

    points = []

    midx = int(side_length/2)  # mid point of rectangle placed at origin
    midy = int(side_length/2)
    shift_x = start_x - midx
    shift_y = start_y - midy

    # start at origin (bottom left). go up. stop before top left
    for i in range(side_length-1):
        points.append((0, i))
    # start at top left. go right. stop before top right
    for i in range(side_length-1):
        points.append((i, side_length-1))
    # start at top right. go down. stop before bottom right
    for i in range(side_length-1):
        points.append((side_length-1, side_length-1-i))
    # start at bottom right. go left. stop before origin (bottom left)
    for i in range(side_length-1):
        points.append((side_length-1-i, 0))

    # Shift from origin to start point
    points = map(lambda (x,y): (x + shift_x, y + shift_y), points)

    # Truncate values that go out of bounds
    points = map(lambda (x,y): truncate(x,y, x_bound, y_bound), points)

    # Remove duplicates
    points = list(set(points))
    return points

#print(get_points_to_explore(0,0, 5, 10, 10))

def predicate_fn(x, y, vector_field):
    if vector_field[x][y]['x'] == 0 and vector_field[x][y]['y'] == 0:
        return False
    else:
        return True


def find_nearest_neighbor(point_x, point_y, vector_field, predicate_fn):
    """
    unfinished
    """
    width = len(vector_field)
    height = len(vector_field[0])

    for i in range(1, 41, 2):  # hardcode
        points_to_explore = get_points_to_explore(point_x, point_y, i, width-1, height-1)
        for x,y in points_to_explore:
            if predicate_fn(x, y, vector_field) == True:
                return (x,y)

    return None



def run():
    width  = 1024 # TODO: this is set manually for now...
    height = 1024
    vec_field = init_vec_field(width,height)
    with open('video.json') as f:
        frames = json.load(f)
        #segments = frames[8]
        #for i in range(1):
        for i,segments in enumerate(frames):
            segments = map(convert_frank_to_arvin, segments)
            vectors_of_segments = map(get_vectors, segments)




            # Init vec field with all (0,0)
            for segment, vectors_of_segment in zip(segments, vectors_of_segments):
                add_to_vec_field(segment, vectors_of_segment, vec_field)
            #write_to_json(vec_field, "vec1.json", indent=2)


    print('here')
    vec_field = add_width(vec_field)


    #format_to_file(vec_field, path_array, filename="data-paths.json", indent=1)
    #format_to_file(vec_field, "ALL", filename="data-all.json", indent=1)
    format_to_file(vec_field, get_starting_points(vec_field), filename="data-paths.json", indent=1)




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


def add_width(truth_vec_field):
    write_to_json(truth_vec_field, "vec-no-width.json", indent=2)
    new_vec_field = deepcopy(truth_vec_field)
    count = 0
    num_found = 1

    with open('total.json') as total_file:
        # total.json is image binarized with 1 if there is a path there.  row column format
        total = json.load(total_file)
        for r in range(len(total)):
            for c in range(len(total)):
                x = c # translate coordinates in total.json
                y = r
                if total[r][c] == 0 and total[r][c] == 0:
                    continue
                count += 1
                if (count % 2000 == 0):
                    print("count: ", count)

                nearest_neighbor = find_nearest_neighbor(x,y, truth_vec_field, predicate_fn)
                if nearest_neighbor:
                    neighbor_x, neighbor_y = nearest_neighbor
                    copy_vec = deepcopy(truth_vec_field[neighbor_x][neighbor_y]) # deepcopy not needed?
                    new_vec_field[x][y] = copy_vec
                    #print("({},{})  |  ({},{})".format(x,y, truth_vec_field[x][y]['x'], truth_vec_field[x][y]['y']))
                else: # do nothing because it should already be 0, 0 there
                    pass

    write_to_json(new_vec_field, "vec-width.json", indent=2)
    return new_vec_field


    
run()

