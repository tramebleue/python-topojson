# coding: utf-8

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the BSD-3-Clause license.                              *
*                                                                         *
***************************************************************************
"""

from heapq import heappop, heappush, heapify
from functools import total_ordering

def triangle_area(a, b, c):

    return abs((a.x - c.x) * (b.y - a.y) - (a.x - b.x) * (c.y - a.y)) / 2

class Point(object):

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        # do not store z, we don't need it
        # self.z = z

    def __repr__(self):
        return '(%.1f, %.1f)' % (self.x, self.y)

class Triangle(object):

    def __init__(self, index, a, b, c):
        self.a = Point(*a)
        self.b = Point(*b)
        self.c = Point(*c)
        # Store original b for later output
        # quite not sure b is actually modified in the process
        # self.bo = b
        self.weight = self.area
        self.entry = None
        self.index = index
        self.previous = index - 1
        self.next = index + 1

    @property
    def area(self):
        return triangle_area(self.a, self.b, self.c)

    def __repr__(self):
        return 'A%s B%s C%s' % (self.a, self.b, self.c)

@total_ordering
class QueueEntry(object):

    def __init__(self, triangle):
        self.triangle = triangle
        self.removed = False
        triangle.entry = self

    def __lt__(self, other):
        return self.triangle.weight < other.triangle.weight

    def __eq__(self, other):
        return self.triangle.weight == other.triangle.weight


def pre_simplify(linestring):
    """
    Visvalingam's non-destructive line simplification

    [1] Visvalingam, M. and J. D. Whyatt. (1992)
        Line Generalisation By Repeated Elimination of Smallest Area.
        Cartographic Information Systems Research Group, University of Hull.

    [2] https://bost.ocks.org/mike/simplify/

    [3] https://github.com/topojson/topojson-simplify/blob/9c893b2/src/presimplify.js
        BSD-3 Licensed
    """

    if len(linestring) <= 2:

        return zip(linestring, [float('inf')] * len(linestring))

    triangles = [
        Triangle(k, a, b, c)
        for k, (a, b, c)
        in enumerate(zip(linestring[:-2], linestring[1:-1], linestring[2:]))
    ]

    heap = [QueueEntry(t) for t in triangles]
    heapify(heap)
    max_weight = 0

    while heap:

        entry = heappop(heap)
        if entry.removed:
            continue

        triangle = entry.triangle
        weight = triangle.weight

        if weight < max_weight:
            triangle.weight = max_weight
        else:
            max_weight = weight

        if triangle.previous > 0:

            t = triangles[triangle.previous]
            t.next = triangle.next
            t.c = triangle.c
            t.weight = t.area
            t.entry.removed = True

            heappush(heap, QueueEntry(t))

        if triangle.next < len(triangles)-1:

            t = triangles[triangle.next]
            t.previous = triangle.previous
            t.a = triangle.a
            t.weight = t.area
            t.entry.removed = True

            heappush(heap, QueueEntry(t))

    start = (linestring[0], float('inf'))
    end = (linestring[-1], float('inf'))
    return [start] + [(t.b, t.weight) for t in triangles] + [end]

def simplify(linestring, min_weight):

    return [
        p for p, weight in pre_simplify(linestring)
        if weight >= min_weight
    ]
