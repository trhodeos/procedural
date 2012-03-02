#!/usr/bin/env python

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

def draw_heightmap(c, map):
    """
    Draw the double array given onto a canvas (using grayscale)
     c - Tk Canvas to draw on
     map - a 2d list of floats (0.0-1.0)
    """
    # make sure we start from scratch
    c.delete(ALL)

    # make sure we fit the heightmap inside the canvas
    scale_x = canvas_width / len(map[0])
    scale_y = canvas_height / len(map)

    for j in xrange(len(map)):
        start_y = j * scale_y
        end_y = start_y + scale_y
        for i in xrange(len(map[0])):
            start_x = i * scale_x
            end_x = start_x + scale_x

            # color computation
            hex_color = hex(int(map[j][i] * 15))[2:] # hex, minus the '0x'
            color = "#" + 3 * str(hex_color) # grayscale value, hence '3 *'
            c.create_rectangle(start_x, start_y,
                               end_x, end_y,
                               fill = color, width = 0)

if __name__ == '__main__':
    # set up window
    root = Tk()
    root.wm_title("Square-Diamond")

    # add canvas (to draw lines on)
    canvas = Canvas(root, width = canvas_width, height = canvas_height)
    canvas.grid(row=0, columnspan = 2)

    # add labels/scales for roughness and num iterations
    roughness = DoubleVar()
    roughness_label = Label(root, text = "Roughness: ")
    roughness_label.grid(row = 1, column = 0, sticky = S)
    roughness_scale = Scale(root, from_ = 0.0, to = 1.0, resolution = .05,
                            orient = HORIZONTAL, variable = roughness,
                            length = canvas_width - 100)
    roughness_scale.set(1.0)
    roughness_scale.grid(row = 1, column = 1)

    iterations = IntVar()
    iterations_label = Label(root, text = "Iterations: ")
    iterations_label.grid(row = 3, column = 0, sticky = S)
    iterations_scale = Scale(root, from_ = 0, to = 4,
                             orient = HORIZONTAL, variable = iterations,
                             length = canvas_width - 100)
    iterations_scale.set(0)
    iterations_scale.grid(row = 3, column = 1)

    # add quit button
    button = Button(root, text="Quit", command = quit)
    button.grid(row = 4, columnspan = 2)

    # testing grid draw-er
    map = []
    for j in xrange(0, 10):
        map.append([])
        for i in xrange(0, 10):
            map[j].append(random.uniform(0.0,1.0))

    draw_heightmap(canvas, map)

    # start Tk main loop
    root.mainloop()
