# coding: utf-8

import numpy as np
from functools import partial
import json

from common import Arc
from extract import extract
from dedup import dedup
from visvalingam import simplify
from delta import delta_encode

def index(coordinates):

    coordinates_map = dict()
    indexes = np.full(len(coordinates), -1, dtype=np.int32)

    for i in xrange(len(coordinates)):

        c = tuple(coordinates[i])
        if coordinates_map.has_key(c):
            indexes[i] = coordinates_map[c]
        else:
            indexes[i] = i
            coordinates_map[c] = i

    del coordinates_map

    return indexes

def junction(coordinates, lines, rings):

    n = len(coordinates)

    indexes = index(coordinates)
    visited = np.full(n, -1, dtype=np.int32)
    left = np.full(n, -1, dtype=np.int32)
    right = np.full(n, -1, dtype=np.int32)
    junctions = np.zeros(n, dtype=np.int16)
    junction_count = 0

    def sequence(i, previous_index, current_index, next_index):

        if visited[current_index] == i:
            return 0

        visited[current_index] = i
        left_index = left[current_index]
        count = 0

        if left_index >= 0:

            right_index = right[current_index]

            if (left_index != previous_index or right_index != next_index) and \
               (left_index != next_index or right_index != previous_index):

               junctions[current_index] = 1
               count += 1

        else:

            left[current_index] = previous_index
            right[current_index] = next_index

        return count

    for i, line in enumerate(lines):

        start = line.a
        end = line.b

        if start == end: continue

        current_index = indexes[start]
        next_index = indexes[start + 1]

        start += 1
        junctions[current_index] = 1
        junction_count += 1

        while start < end:

            start += 1
            previous_index = current_index
            current_index = next_index
            next_index = indexes[start]
            junction_count += sequence(i, previous_index, current_index, next_index)

        junctions[next_index] = 1
        junction_count += 1

    visited = np.full(n, -1, dtype=np.int32)

    for i, ring in enumerate(rings):

        start = ring.a
        end = ring.b

        if start == end: continue

        previous_index = indexes[end - 1]
        current_index = indexes[start]
        next_index = indexes[start + 1]

        start += 1
        junction_count += sequence(i, previous_index, current_index, next_index)

        while start < end:

            start += 1
            previous_index = current_index
            current_index = next_index
            next_index = indexes[start]
            junction_count += sequence(i, previous_index, current_index, next_index)

    # del visited
    # del left
    # del right

    junction_set = { tuple(coordinates[indexes[i]])
                     for i in range(n)
                     if junctions[indexes[i]] == 1 }

    # junction_set = set()
    # for i in range(n):

    #     j = indexes[i]
    #     if junctions[j] == 1:
    #         junction_set.add(coordinates[j])

    # del indexes
    # del junctions

    return junction_set

def rotate(x, start, mid, end):

    # ABCDE -> EDCBA -> CDEAB
    # x[ start:end+1 ] = np.flip(x[ start:end+1 ], 0)
    # x[ start:mid ] = np.flip(x[ start:mid ], 0)
    # x[ mid:end+1 ] = np.flip(x[ mid:end+1 ], 0)

    x[ start:end+1 ] = np.roll(x[ start:end+1 ], end-mid+1, 0)

def cut(coordinates, lines, rings):

    junctions = junction(coordinates, lines, rings)

    for line in lines:

        start = mid = line.a
        end = line.b

        while mid < end-1:
            mid += 1
            if tuple(coordinates[mid]) in junctions:
                line.b = mid
                line.next = Arc(mid, end)
                line = line.next

    for ring in rings:

        start = mid = ring.a
        end = ring.b
        ring_fixed = (tuple(coordinates[start]) in junctions)

        while mid < end-1:
            mid += 1
            if tuple(coordinates[mid]) in junctions:
                if ring_fixed:
                    ring.b = mid
                    ring.next = Arc(mid, end)
                    ring = ring.next
                else:
                    rotate(coordinates, start, mid, end-1)
                    coordinates[end] = coordinates[start]
                    ring_fixed = True
                    mid = start

def count_lines(lines):

    count = 0

    for i in range(len(lines)):

        line = lines[i]
        while line.next:
            line = line.next
            count += 1
        count += 1

    return count



def arc_geometry(coordinates, arc):

    a = arc.a
    b = arc.b

    if a > b:
        return np.flip(coordinates[b:a+1], 0).tolist()
    else:
        return coordinates[a:b+1].tolist()


def component_geometry(coordinates, component):

    coords = list()
    arc = component
    
    while arc:

        geom = arc_geometry(coordinates, arc.a, arc.b)
        last_point = geom[-1]
        coords.extend(geom[:-1])
        arc = arc.next

    coords.append(last_point)

    return coords

def map_geometries(arc_index, objects, coordinates):

    def map_arc(arc):

        arcs = list()
        current = arc

        while current:

            start = current.a
            end   = current.b

            if start > end:
                index = -arc_index[(end, start)]-1
            else:
                index = arc_index[(start, end)]

            arcs.append(index)
            current = current.next

        return arcs

    def component_arcs(component):

        component_type = component['type']

        if component_type is 'None':
            pass

        elif component_type == 'Point':
            component['coordinates'] = coordinates[component['coordinates']].tolist()

        elif component_type == 'LineString':
            component['arcs'] = map_arc(component['arcs'])

        elif component_type == 'Polygon':
            component['arcs'] = map(map_arc, component['arcs'])

        elif component_type == 'MultiPoint':
            component['coordinates'] = [ coordinates[pt].tolist() for pt in component['coordinates']]

        elif component_type == 'MultiLineString':
            component['arcs'] = map(map_arc, component['arcs'])

        elif component_type == 'MultiPolygon':
            component['arcs'] = [ map(map_arc, polygon) for polygon in component['arcs'] ]

        elif component_type == 'GeometryCollection' or component_type == 'FeatureCollection':
            for geometry in component['geometries']:
                component_arcs(geometry)

        elif component_type == 'Feature':
            component_arcs(component['geometry'])

        return component

    if objects.has_key('type'):
        
        component_arcs(objects)

    else:

        return { key: component_arcs(obj) for key, obj in objects.items() }

    return objects


def topology(geojson, quantization=1e6, simplification=0):
    """
    Convert GeoJSON to TopoJSON.

    Parameters
    ----------

    geojson: dict-like
        plain GeoJSON object
        or dictionary of named GeoJSON objects

    quantization: number, > 1
        size of the grid used to round-off coordinates.
        If <= 1, no quantization is used.

    Returns
    -------

    topojson: dict-like TopoJSON object

    Notes
    -----

    [1] Bostock, Mike (2013) How To Infer Topology
        https://bost.ocks.org/mike/topology/

    [2] Bostock's Nodejs reference implementation
        https://github.com/topojson/topojson-server/tree/6c1709b/src
        BSD-3 Licensed
    """

    coordinates, lines, rings, objects = extract(geojson)

    if len(coordinates) > 0:

        minx = np.min(coordinates[:, 0])
        miny = np.min(coordinates[:, 1])
        maxx = np.max(coordinates[:, 0])
        maxy = np.max(coordinates[:, 1])

        if quantization > 1:
            kx = (minx == maxx) and 1 or 2.0*(maxx - minx)
            ky = (miny == maxy) and 1 or 2.0*(maxy - miny)
            quantized = np.int32(np.round((coordinates - (minx, miny)) / (kx, ky) * quantization))
        else:
            kx = ky = 1
            quantized = coordinates

    else:

        minx = miny = maxx = maxy = 0.0
        kx = ky = 1
        quantized = coordinates

    cut(quantized, lines, rings)
    arcs = dedup(quantized, lines, rings)
    arc_index = { (arc.a, arc.b): i for i, arc in enumerate(arcs) }

    if simplification > 0:

        arcs = map(delta_encode, simplify(map(partial(arc_geometry, quantized), arcs), simplification))

    elif quantization > 1:

        arcs = map(delta_encode, map(partial(arc_geometry, quantized), arcs))

    else:

        arcs = map(partial(arc_geometry, quantized), arcs)

    topo = {
        'arcs': arcs,
        'objects': map_geometries(arc_index, objects, quantized),
        'bbox': [ minx, miny, maxx, maxy ],
        'type': 'Topology'
    }

    if quantization > 1:

        topo['transform'] = {
            'scale': [ kx / quantization, ky / quantization ],
            'translate': [ minx, miny ]
        }

    return topo



def test_geom():
    import shapely.geometry
    return shapely.geometry.MultiPolygon([
            [[ (0,0), (1,0), (1,1), (0,1) ], []],
            [[ (1,0), (2,0), (2,1), (1,1) ], []]
        ])


