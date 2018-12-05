import numpy as np
import json

from delta import delta_decode

def unpack(topojson):
    """
    Convert TopoJSON object to GeoJSON. 
    """

    if not (topojson.has_key('type') and topojson['type'] == 'Topology'):
        raise KeyError('Not a valid TopoJSON object')

    geojson = dict()

    arcs = [ delta_decode(arc) for arc in topojson['arcs'] ]

    if topojson.has_key('transform'):
        sx, sy = topojson['transform']['scale']
        tx, ty = topojson['transform']['translate']
        arcs = [ (np.array(arc) * (sx, sy)) + (tx, ty) for arc in arcs ]
    else:
        arcs = [ np.array(arc) for arc in arcs ]

    def unpack_linestring(geometry):

        coordinates = list()

        for index in geometry:

            if index < 0:
                arc = np.flip(arcs[-index-1], 0).tolist()
            else:
                arc = arcs[index-1].tolist()

            last_point = arc[-1]
            coordinates.extend(arc[:-1])

        coordinates.append(last_point)

        return coordinates

    def unpack_ring(geometry):

        ring = unpack_linestring(geometry)
        if tuple(ring[0]) != tuple(ring[-1]): print ring
        assert(tuple(ring[0]) == tuple(ring[-1]))
        return ring

    def unpack_geometry(component):

        component_type = component['type']

        if component.has_key('properties'):
            feature = {
                'geometry': unpack_geometry({ 'arcs': component['arcs'], 'type': component_type }),
                'type': 'Feature'
            }
            copy_key(component, feature, 'id', 'bbox', 'properties')
            return feature

        elif component_type == 'Point':
            return {
                'coordinates': component['coordinates'],
                'type': component_type
            }

        elif component_type == 'LineString':
            return {
                'coordinates': unpack_linestring(component['arcs']),
                'type': component_type
            }
            

        elif component_type == 'Polygon':
            return {
                'coordinates': map(unpack_ring, component['arcs']),
                'type': component_type
            }

        elif component_type == 'MultiPoint':
            return {
                'coordinates': component['coordinates'],
                'type': component_type
            }

        elif component_type == 'MultiLineString':
            return {
                'coordinates': map(unpack_linestring, component['arcs']),
                'type': component_type
            }

        elif component_type == 'MultiPolygon':
            return {
                'coordinates': [ map(unpack_ring, polygon) for polygon in component['arcs'] ],
                'type': component_type
            }

        elif component_type == 'GeometryCollection':
            return {
                'geometries': [ unpack_geometry(geometry) for geometry in component['geometries'] ],
                'type': component_type
            }

        elif component_type == 'FeatureCollection':
            return {
                'features': [ unpack_geometry(geometry) for geometry in component['geometries'] ],
                'type': component_type
            }
            
        else:

            raise ValueError('Unexpected type %s' % component_type)

    def unpack_object(obj):

        o = unpack_geometry(obj)
        copy_key(obj, o, 'id', 'bbox', 'crs')
        return o

    if topojson['objects'].has_key('type'):

        geojson = unpack_object(topojson['objects'])

    else:

        geojson = { key: unpack_object(obj)
                    for key, obj in topojson['objects'].items() }

    return geojson