#!/usr/bin/env python
"""
An example of midpoint displacement procedural generation.
The algorithm is fairly simple:
for number iterations:
  for each line segment:
     add new point at midpoint (+ random_val in y position)
  divide random_val by (2 * 'roughness')
"""

from procedural import midpoint_displacement, interpolation
from Tkinter import *

# global variables
# algorithm variables
iterations = 0
roughness = 0

# interpolation variables
step_size = 0

# tk variables
canvas_width = 300
canvas_height = 200
canvas = 0

# storage
points = []

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

def update_points(not_needed):
    """
    Updates the global set of points with values from the 'algorithmic' scales
    """
    # grab parameters from tk vars
    it = iterations.get()
    r = roughness.get()

    # update the global 'points' variable
    global points
    points = midpoint_displacement.run(it, r)

    # make sure to update the canvas
    update_canvas(not_needed)

def update_canvas(not_needed):
    """
    Interpolates the current set of points, and draws that to the canvas
     not_needed - just that
    """

    # grab tk var parameters
    s = step_size.get()

    # interpolate on the current points and draw
    p = interpolation.interpolate_1d(points, step = s)
    draw_lines(canvas, p)

if __name__ == '__main__':
    # set up window
    root = Tk()
    root.wm_title("Midpoint Displacement")

    # add canvas (to draw lines on)
    canvas = Canvas(root, width = canvas_width, height = canvas_height)
    canvas.grid(row=0, columnspan = 2)

    # add labels/scales for algorithmic variables
    algorithm_group = LabelFrame(root, text="Algorithmic",
                                 padx = 5, pady = 5)

    roughness = DoubleVar()
    roughness_label = Label(algorithm_group, text = "Roughness: ")
    roughness_label.grid(row = 0, column = 0, sticky = S)
    roughness_scale = Scale(algorithm_group, from_ = 0.0, to = 1.0, resolution = .05,
                            orient = HORIZONTAL, variable = roughness,
                            length = canvas_width - 100,
                            command = update_points)
    roughness_scale.set(1.0) # initial value
    roughness_scale.grid(row = 0, column = 1)

    iterations = IntVar()
    iterations_label = Label(algorithm_group, text = "Iterations: ")
    iterations_label.grid(row = 1, column = 0, sticky = S)
    iterations_scale = Scale(algorithm_group, from_ = 0, to = 10,
                             orient = HORIZONTAL, variable = iterations,
                             length = canvas_width - 100,
                             command = update_points)
    iterations_scale.set(1) # initial value
    iterations_scale.grid(row = 1, column = 1)

    algorithm_group.grid(row = 1, columnspan = 2, rowspan = 2)

    # add labels/scales for interpolation variables
    interp_group = LabelFrame(root, text="Interpolation",
                                 padx = 5, pady = 5)

    step_size = DoubleVar()
    step_label = Label(interp_group, text = "Step size: ")
    step_label.grid(row = 0, column = 0, sticky = S)
    step_scale = Scale(interp_group, from_ = 0.05, to = 1.0, resolution = 0.01,
                             orient = HORIZONTAL, variable = step_size,
                             length = canvas_width - 100,
                             command = update_canvas)
    step_scale.set(.1) # initial value
    step_scale.grid(row = 0, column = 1)

    interp_group.grid(row = 4, columnspan = 2, rowspan = 2)

    # add quit button
    button = Button(root, text="Quit", command = quit)
    button.grid(row = 6, columnspan = 2)

    # start Tk main loop
    root.mainloop()
