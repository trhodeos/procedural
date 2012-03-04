#!/usr/bin/env python
"""
Interpolation techniques, such as linear and cosine, and utilities to apply these
interpolation functions to 1d and 2d data sets
"""

import math

def xfrange(start, stop=None, step=None):
    """
    a floating point version of xrange
    start - start point
    stop - end point (exclusive)
    step - step size
    returns a list of floats from [start, stop)
    """
    if stop is None:
        stop = float(start)
        start = 0.0

    if step is None:
        step = 1.0

    cur = float(start)

    while cur < stop:
        yield cur
        cur += step

def linear(t, y1, y2):
    """
    A method for linear interpolation.
    t - value from [0.0, 1.0]
    y1 - value of function at 0.0
    y2 - value of function at 1.0
    returns value of function at t
    """
    assert(t >= 0)
    assert(t <= 1)
    return y1 * (1 - t) + y2 * t

def cosine(t, y1, y2):
    """
    A method for cosine interpolation.
    t - value from [0.0, 1.0]
    y1 - value of function at 0.0
    y2 - value of function at 1.0
    returns value of function at t
    """
    assert(t >= 0)
    assert(t <= 1)
    new_t = (1 - math.cos(math.pi * t)) / 2
    return y1 * (1 - new_t) + y2 * new_t

def interpolate_1d(points, interp = cosine, step = .1):
    """
    Apply an interpolation function to a 1d set of points
    points - a list of (x,y) pairs (sorted by x value)
    interp - interpolation function of form:
    func(t, y1, y2)
    step - step size
    returns an interpolated list of points
    """
    if len(points) < 2:
        print "Cannot interpolate on less than 2 points."
        return

    new_points = []

    # step through pairs of points, and apply interpolation 1/step times
    for i in xrange(len(points) - 1):
        r = points[i + 1][0] - points[i][0] # total range of x values
        new_points.extend([
                [points[i][0] + r * t, # x
                 interp(t, points[i][1], points[i + 1][1])] # y
                for t in xfrange(0.0, 1.0, step)])
    new_points.append(points[-1]) # make sure we add the last item back
    return new_points

