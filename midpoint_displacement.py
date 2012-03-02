#!/usr/bin/env python

from Tkinter import *

import random

iterations = 0
roughness = 0.0

canvas_width = 300
canvas_height = 200

canvas = 0

def draw_lines(c, points):
    # make sure we start with a clean slate
    c.delete(ALL)

    # now draw them
    global canvas_width
    w = canvas_width

    global canvas_height
    max_height = canvas_height
    for i in points:
        if i[1] * canvas_height > max_height:
            max_height = i[1] * canvas_height
    h = canvas_height * canvas_height / max_height

    for i in xrange(len(points) - 1):
        c.create_line(w * points[i][0],     canvas_height - h * points[i][1],
                      w * points[i + 1][0], canvas_height - h * points[i + 1][1])

def update_iterations(iters):
    global iterations
    iterations = int(iters)
    global canvas
    generate_horizon(canvas)

def update_roughness(rough):
    global roughness
    roughness = float(rough)
    global canvas
    generate_horizon(canvas)

def generate_horizon(c):
    begin_points = [[0.0, 0.0],[1.0, 0.0]]
    points = generate(iterations, begin_points, 1.0)
    draw_lines(c, points)

def generate(it, points, rand_range):
    if it == 0:
        return points
#    sorted(points, key=lambda point: point[0])

    new_points = [points[0]]
    for i in xrange(len(points)-1):
        calc_point = [(points[i+1][0] + points[i][0])/2,
                      (points[i+1][1] + points[i][1])/2 +
                      random.uniform(0, rand_range)]

        new_points.append(calc_point)
        new_points.append(points[i+1])

    global roughness
    r = roughness

    return generate(it-1, new_points, rand_range * (2**-r))

if __name__ == '__main__':
    root = Tk()

    canvas = Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    roughness_scale = Scale(root, from_ = 0.0, to = 1.0, resolution = .05,
                            orient = HORIZONTAL, length = 300, command=update_roughness)
    roughness_scale.pack()

    iterations_scale = Scale(root, from_ = 0, to = 10, orient = HORIZONTAL,
                             length = 300, command=update_iterations)
    iterations_scale.pack()
    button = Button(root, text="Quit", command=quit)
    button.pack()

    root.mainloop()
