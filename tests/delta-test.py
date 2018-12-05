# coding: utf-8

import unittest
import nose2
from nose2.tools import such
from topojson.delta import delta_encode

with such.A('function delta_encode') as it:

  @it.should("convert arcs to delta encoding")
  def test_delta_encode(case):

    encoded = delta_encode([[0, 0], [9999, 0], [0, 9999], [0, 0]])

    case.assertListEqual(encoded, [[0, 0], [9999, 0], [-9999, 9999], [0, -9999]])

  @it.should("skip coincident points")
  def test_skip_coincident_point(case):

    encoded = delta_encode([[0, 0], [9999, 0], [9999, 0], [0, 9999], [0, 0]])

    case.assertListEqual(encoded, [[0, 0], [9999, 0], [-9999, 9999], [0, -9999]])

  @it.should("preserve at least two positions")
  def test_preverse_two_positions(case):

    encoded = delta_encode([[12345, 12345], [12345, 12345], [12345, 12345], [12345, 12345]])

    case.assertListEqual(encoded, [[12345, 12345], [0, 0]])

it.createTests(globals())

if __name__ == '__main__':
  nose2.main()