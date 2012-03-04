#!/usr/bin/env python
"""
Different interpolation techniques
"""

import math

def xfrange(start, stop=None, step=None):
    """
    a floating point version of xrange
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
    return y1 * (1 - t) + y2 * t

def cosine(t, y1, y2):
    new_t = (1 - math.cos(math.pi * t)) / 2
    return y1 * (1 - new_t) + y2 * new_t

def interpolate_1d(points, interp = cosine, step = .1):
    if len(points) < 2:
        print "Cannot interpolate on less than 2 points."
        return

    new_points = []
    for i in xrange(len(points) - 1):
        r = points[i + 1][0] - points[i][0]
        new_points.extend(
            [[points[i][0] + r * t, interp(t, points[i][1], points[i + 1][1])]
             for t in xfrange(0.0, 1.0, step)])
    new_points.append(points[-1]) # make sure we add the last item back
    return new_points

