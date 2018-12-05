import io
import os
import re
from setuptools import setup, find_packages


def read(path, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()


def get_install_requirements(path):
    content = read(path)
    return [
        req
        for req in content.split("\n")
        if req != '' and not req.startswith('#')
    ]


def version(path):
    """Obtain the packge version from a python file e.g. pkg/__init__.py
    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(path)
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


DESCRIPTION = "Python implementation of TopoJSON"
LONG_DESCRIPTION = """
Python port of Mike Bostock's TopoJSON.
TopoJSON is an extension of GeoJSON that encodes topology.
Rather than representing geometries discretely,
geometries in TopoJSON files are stitched together from shared line segments called arcs.
"""
NAME = "topojson"
AUTHOR = "Christophe Rousson"
MAINTAINER = "Christophe Rousson"
URL = 'https://github.com/tramebleue/python-topojson'
LICENSE = 'BSD'
PACKAGES = find_packages()
VERSION = version('topojson/__init__.py')
DEV_REQUIRES = get_install_requirements("requirements-dev.txt")

setup(
    name=NAME,
    version=VERSION,
    license=LICENSE,
    packages=PACKAGES,
    # extras_requires={
    #     'dev': DEV_REQUIRES
    # },
    test_suite="tests",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    maintainer=MAINTAINER,
    # maintainer_email=MAINTAINER_EMAIL,
    # url=URL
    entry_points='''
        [console_scripts]
        geo2topo=topojson.cli.geo2topo:geo2topo
    '''
)