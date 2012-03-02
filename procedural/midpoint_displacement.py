#!/usr/bin/env python
"""
An example of midpoint displacement procedural generation.
The algorithm is fairly simple:
for number iterations:
  for each line segment:
     add new point at midpoint (+ random_val in y position)
  divide random_val by (2 * 'roughness')
"""

import random

def run(iterations, roughness):
    """
    Generate a midpoint displacement line based on arguments
     iterations - number of iterations to run
     roughness - constant that controls 'roughness'
       NOTE: 1.0 is less rough, 0.0 is more rough
     returns a list of (x,y) pairs
    """
    # clamp x values at [0.0 and 1.0]
    begin_points = [[0.0, 0.0],[1.0, 0.0]]
    return __midpoint_displacement_recurse(iterations, begin_points, 1.0, roughness)

def __midpoint_displacement_recurse(it, points, rand_range, r):
    """
    One iteration of midpoint displacement.
     it - number of iterations left
     points - current list of (x,y) points
     rand_range - current possible range of randomness
     r - 'roughness' [constant]
     returns a generated list of (x,y) pairs based on parameters
      note: for the (x,y) pairs, 0 <= x <= 1.0 and 0 <= y
    """
    # base case of recursion
    if it == 0:
        return points

    # iterate through all of the line segments
    new_points = [points[0]]
    for i in xrange(len(points)-1):
        # calculate a new point
        avg_x = (points[i][0] + points[i+1][0])/2
        avg_y = (points[i][1] + points[i+1][1])/2
        calc_point = [avg_x,
                      avg_y +
                      random.uniform(-rand_range, rand_range)]

        # clamp the y value to be >= 0
        calc_point[1] = max(calc_point[1], 0)

        # add the new point to the list (as well as the old point
        new_points.append(calc_point)
        new_points.append(points[i+1])

    # recurse and return
    return __midpoint_displacement_recurse(it-1, new_points, rand_range * (2**-r), r)
