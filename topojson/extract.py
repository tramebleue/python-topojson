# coding: utf-8

import numpy as np
from common import Arc, copy_key

def extract(geojson):
    """
    [1] GeoJSON Specification
        https://tools.ietf.org/html/rfc7946
    """

    coordinates = list()
    lines = list()
    rings = list()

    def extract_point(coords):

        coordinates.append(tuple(coords))
        return len(coordinates)-1

    def extract_line(line_coords):

        a = len(coordinates)
        coordinates.extend(map(tuple, line_coords))
        b = len(coordinates) - 1

        arc = Arc(a, b)
        lines.append(arc)

        return arc

    def extract_ring(line_coords):

        a = len(coordinates)
        coordinates.extend(map(tuple, line_coords))
        b = len(coordinates) - 1

        arc = Arc(a, b)
        rings.append(arc)

        return arc

    def extract_geometry(component):

        # TODO encode bbox, id fields

        if component is None:
            return { 'type': None }

        component_type = component['type']

        if component_type == 'Point':
            return {
                'coordinates': extract_point(component['coordinates']),
                'type': component_type
            }

        elif component_type == 'LineString':
            return {
                'arcs': extract_line(component['coordinates']),
                'type': component_type
            }

        elif component_type == 'Polygon':
            return {
                'arcs': map(extract_ring, component['coordinates']),
                'type': component_type
            }

        elif component_type == 'MultiPoint':
            return {
                'coordinates': [ extract_point(pt) for pt in component['coordinates'] ],
                'type': component_type
            }

        elif component_type == 'MultiLineString':
            return {
                'arcs': map(extract_line, component['coordinates']),
                'type': component_type
            }

        elif component_type == 'MultiPolygon':
            return {
                'arcs': [ map(extract_ring, polygon) for polygon in component['coordinates'] ],
                'type': component_type
            }

        elif component_type == 'GeometryCollection':
            return {
                'geometries': map(extract_geometry, component['geometries']),
                'type': component_type
            }

        elif component_type == 'Feature':
            geometry = extract_geometry(component['geometry'])
            copy_key(component, geometry, 'id', 'properties')
            return geometry

        elif component_type == 'FeatureCollection':
            return {
                'geometries': map(extract_geometry, component['features']),
                'type': component_type
            }

        else:

            raise ValueError('Unexpected type %s' % component_type)

    def extract_object(obj):
        o = extract_geometry(obj)
        copy_key(obj, o, 'bbox', 'crs')
        return o

    if geojson.has_key('type'):

        objects = extract_object(geojson)
    else:
        objects = { key: extract_object(obj) for key, obj in geojson.items() }

    return np.array(coordinates), lines, rings, objects