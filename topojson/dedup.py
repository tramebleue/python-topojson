# coding: utf-8

import numpy as np
from collections import defaultdict

def dedup(coordinates, lines, rings):

    arc_index = defaultdict(list)
    arcs = list()

    def minimum_offset(arc):

        mid = arc.a
        minimum = mid
        minimum_point = coordinates[mid]

        while mid < arc.b-1:
            mid += 1
            point = coordinates[mid]
            if point[0] < minimum_point[0] or point[0] == minimum_point[0] and point[1] < minimum_point[1]:
                minimum = mid
                minimum_point = point

        return minimum - arc.a

    def equal_line(x, y):

        n = x.b - x.a
        if n != (y.b - y.a):
            return False

        return np.all([ coordinates[ x.a + i ] == coordinates[ y.a + i ] for i in range(n+1) ])

    def equal_line_reverse(x, y):

        n = x.b - x.a
        if n != (y.b - y.a):
            return False

        return np.all([ coordinates[ x.a + i ] == coordinates[ y.b - i ]
                     for i in range(n+1) ])

    def equal_ring(x, y):

        n = x.b - x.a
        if n != (y.b - y.a):
            return False

        offset_x = minimum_offset(x)
        offset_y = minimum_offset(y)

        return np.all([ coordinates[ x.a + ((i + offset_x) % n) ] == coordinates[ y.a + ((i + offset_y) % n) ]
                     for i in range(n+1) ])

    def equal_ring_reverse(x, y):

        n = x.b - x.a
        if n != (y.b - y.a):
            return False

        offset_x = minimum_offset(x)
        offset_y = n - minimum_offset(y)

        return np.all([ coordinates[ x.a + ((i + offset_x) % n) ] == coordinates[ y.b - ((i + offset_y) % n) ]
                     for i in range(n+1) ])

    def dedup_line(arc):

        for other_arc in arc_index[tuple(coordinates[arc.a])]:
            if equal_line(arc, other_arc):
                arc.a = other_arc.a
                arc.b = other_arc.b
                return

        for other_arc in arc_index[tuple(coordinates[arc.b])]:
            if equal_line_reverse(arc, other_arc):
                arc.a = other_arc.b
                arc.b = other_arc.a
                return

        arc_index[tuple(coordinates[arc.a])].append(arc)
        arc_index[tuple(coordinates[arc.b])].append(arc)
        
        arcs.append(arc)

    def dedup_ring(arc):

        for other_arc in arc_index[tuple(coordinates[arc.a])]:
            if equal_line(arc, other_arc):
                arc.a = other_arc.a
                arc.b = other_arc.b
                return
            if equal_line_reverse(arc, other_arc):
                arc.a = other_arc.b
                arc.b = other_arc.a
                return

        offset = minimum_offset(arc)

        for other_arc in arc_index[tuple(coordinates[arc.a + offset])]:
            if equal_ring(arc, other_arc):
                arc.a = other_arc.a
                arc.b = other_arc.b
                return
            if equal_ring_reverse(arc, other_arc):
                arc.a = other_arc.b
                arc.b = other_arc.a
                return
            
        arc_index[tuple(coordinates[arc.a + offset])].append(arc)

        arcs.append(arc)

    for line in lines:
        while line:
            dedup_line(line)
            line = line.next

    for ring in rings:
        if ring.next:
            while ring:
                dedup_line(ring)
                ring = ring.next
        else:
            dedup_ring(ring)

    return arcs