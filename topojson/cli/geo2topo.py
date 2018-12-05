#!/usr/bin/env python
# coding: utf-8

from topojson.topology import topology
import json
import click
import sys, os

@click.command()
@click.argument('files', nargs=-1, type=click.Path(readable=True, exists=True))
@click.option('--out', type=click.Path(writable=True),
	help='Specify the output TopoJSON file name. Defaults to "-" for stdout.')
@click.option('--quantization', type=click.FLOAT, default=1e6,
	help='Coordinates quantization factor, ie. number of differentiable positions in each axis direction. 0 disables quantization')
@click.option('--simplification', type=click.FLOAT, default=0.0,
	help='Simplify topology arcs using given tolerance (area) in squared map units')
def geo2topo(files, out, quantization, simplification):
	"""
	Converts one or more GeoJSON objects to an output topology.
	
	See https://github.com/topojson/topojson-server/blob/master/README.md#geo2topo
	"""

	geojson = dict()

	for file in files:
		with open(file) as fp:
			geojson[os.path.basename(file)] = json.load(fp)

	topojson = topology(geojson, quantization, simplification)

	if out is None or out == '-':
		json.dump(topojson, sys.stdout)
	else:
		with open(out, 'w') as fp:
			json.dump(topojson, fp)