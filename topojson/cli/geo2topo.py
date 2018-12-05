#!/usr/bin/env python
# coding: utf-8

from topojson.topology import topology
import json
import click

@click.command()
@click.argument('input', type=click.File('r'))
@click.argument('output', type=click.File('w'))
@click.option('--quantization', type=click.FLOAT, default=1e6, help='')
@click.option('--simplification', type=click.FLOAT, default=0, help='Simplify topology arcs using given tolerance')
def geo2topo(input, output, quantization, simplification):
	"""
	Description of geo2topo
	"""

	geojson = json.load(input)
	topojson = topology(geojson, quantization, simplification)
	json.dump(topojson, output)

if __name__ == '__main__':
	geo2topo()