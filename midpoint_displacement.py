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
from Tkinter import *

# global variables
# algorithm variables
iterations = 1
roughness = 1.0

# tk variables
canvas_width = 300
canvas_height = 200
canvas = 0

def draw_lines(c, points):
    """
    Draw lines on a Tk canvas
     c - Tk canvas
     points - list of (x,y) pairs (sorted)
    """
    # make sure we start with a clean slate
    c.delete(ALL)

    # get width and height scalings
    w = canvas_width
    h = get_scaled_height(canvas_height, points)

    # now draw them
    for i in xrange(len(points) - 1):
        c.create_line(w * points[i][0],     canvas_height - h * points[i][1],
                      w * points[i + 1][0], canvas_height - h * points[i + 1][1])

def get_scaled_height(original_height, points):
    """
    Returns a scaled height (/multiplier) given an original height
    and a list of (x,y) pairs
     original_height - max possible height
     points - (x,y) pairs
     returns a scalar such that scalar * max(points)  == original_height
    """
    # sort the values
    sorted_points = sorted(points, key=lambda point: point[1])

    # get last item
    max_height = sorted_points[-1][1]

    # make sure we aren't overzealous
    if (max_height < 1.0):
        max_height = 1.0

    return original_height / max_height

def update_iterations(iters):
    """
    Tk Scale callback that updates the number of iterations
     iters - number of iterations (in string format)
    """
    global iterations
    iterations = int(iters)

    # update canvas
    points = midpoint_displacement()
    draw_lines(canvas, points)

def update_roughness(rough):
    """
    Tk Scale callback that updates the roughness
     rough - roughness (in string format)
    """
    global roughness
    roughness = float(rough)

    # update canvas
    points = midpoint_displacement()
    draw_lines(canvas, points)

def midpoint_displacement():
    """
    Generate a midpoint displacement line based on parameters set via Tk
     returns a list of (x,y) pairs
    """
    # clamp x values at [0.0 and 1.0]
    begin_points = [[0.0, 0.0],[1.0, 0.0]]
    return midpoint_displacement_recurse(iterations, begin_points, 1.0, roughness)

def midpoint_displacement_recurse(it, points, rand_range, r):
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
    return midpoint_displacement_recurse(it-1, new_points, rand_range * (2**-r), r)

if __name__ == '__main__':
    # set up window
    root = Tk()
    root.wm_title("Midpoint Displacement")

    # add canvas (to draw lines on)
    canvas = Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    # add scales for roughness and num iterations
    roughness_scale = Scale(root, from_ = 0.0, to = 1.0, resolution = .05,
                            orient = HORIZONTAL, length = 300, command=update_roughness)
    roughness_scale.set(roughness)
    roughness_scale.pack()
    iterations_scale = Scale(root, from_ = 0, to = 10, orient = HORIZONTAL,
                             length = 300, command=update_iterations)
    iterations_scale.set(iterations)
    iterations_scale.pack()

    # add quit button
    button = Button(root, text="Quit", command=quit)
    button.pack()

    # start Tk main loop
    root.mainloop()
