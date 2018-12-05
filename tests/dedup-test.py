# coding: utf-8

import unittest
import nose2
from nose2.tools import such
from topojson.topology import cut, extract, dedup
from collections import OrderedDict

def repr_arc(arc):

  o = { 0: arc.a, 1: arc.b }
  if arc.next is not None:
    o['next'] = repr_arc(arc.next)

  return o

def do_dedup(geojson):

  # items = [ (key, val) for key, val in geojson.items() ]
  # items.sort(key=lambda x: x[0])
  # ordered = OrderedDict(items)

  coordinates, lines, rings, objects = extract(geojson)
  cut(coordinates, lines, rings)
  arcs = dedup(coordinates, lines, rings)
  arc_index = { (arc.a, arc.b): i for i, arc in enumerate(arcs) }

  for key, obj in objects.items():

    component_type = obj['type']

    if component_type == 'LineString':
      obj['arcs'] = repr_arc(obj['arcs'])
    elif component_type == 'Polygon':
      obj['arcs'] = [ repr_arc(arc) for arc in obj['arcs'] ]
    else:
      raise ValueError('Unexpected type %s' % component_type)

  return objects

with such.A('deduplication function `dedup`') as it:

  @it.should("dedup exact duplicate lines ABC & ABC share an arc")
  def test_dedup_abc_abc(case):

    objects = do_dedup({
      'abc': {'type': 'LineString', 'coordinates': [[0, 0], [1, 0], [2, 0]]},
      'abc2': {'type': 'LineString', 'coordinates': [[0, 0], [1, 0], [2, 0]]}
    })

    case.assertDictEqual(objects, {
      'abc': {'type': "LineString", 'arcs': {0: 0, 1: 2}},
      'abc2': {'type': "LineString", 'arcs': {0: 0, 1: 2}}
    })

  @it.should("dedup reversed duplicate lines ABC & CBA share an arc")
  def test_dedup_abc_cba(case):

    objects = do_dedup({
      'abc': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0]]},
      'cba': {'type': "LineString", 'coordinates': [[2, 0], [1, 0], [0, 0]]}
    })

    case.assertDictEqual(objects, {
      'abc': {'type': "LineString", 'arcs': {0: 0, 1: 2}},
      'cba': {'type': "LineString", 'arcs': {0: 2, 1: 0}}
    })

  @it.should("dedup exact duplicate rings ABCA & ABCA share an arc")
  def test_dedup_abca_abca(case):

    objects = do_dedup({
      'abca': {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [2, 0], [0, 0]]]},
      'abca2': {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [2, 0], [0, 0]]]}
    })

    case.assertDictEqual(objects, {
      'abca': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]},
      'abca2': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]}
    })

  @it.should("dedup reversed duplicate rings ACBA & ABCA share an arc")
  def test_dedup_acba_abca(case):

    objects = do_dedup(OrderedDict([
      ('abca', {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [2, 0], [0, 0]]]}),
      ('acba', {'type': "Polygon", 'coordinates': [[[0, 0], [2, 0], [1, 0], [0, 0]]]})
    ]))

    case.assertDictEqual(objects, {
      'abca': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]},
      'acba': {'type': "Polygon", 'arcs': [{0: 3, 1: 0}]}
    })

  @it.should("dedup rotated duplicate rings BCAB & ABCA share an arc")
  def test_dedup_bcab_abca(case):

    objects = do_dedup({
      'abca': {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [2, 0], [0, 0]]]},
      'bcab': {'type': "Polygon", 'coordinates': [[[1, 0], [2, 0], [0, 0], [1, 0]]]}
    })

    case.assertDictEqual(objects, {
      'abca': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]},
      'bcab': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]}
    })

  @it.should("dedup ring ABCA & line ABCA have no cuts")
  def test_dedup_ring_abca_line_abca(case):

    objects = do_dedup(OrderedDict([
      ('abcaLine', {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0], [0, 0]]}),
      ('abcaPolygon', {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [2, 0], [0, 0]]]})
    ]))

    case.assertDictEqual(objects, {
      'abcaLine': {'type': "LineString", 'arcs': {0: 0, 1: 3}},
      'abcaPolygon': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]}
    })

  @it.should("dedup ring BCAB & line ABCA have no cuts")
  def test_dedup_ring_bcab_line_abca(case):

    objects = do_dedup(OrderedDict([
      ('abcaLine', {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0], [0, 0]]}),
      ('bcabPolygon', {'type': "Polygon", 'coordinates': [[[1, 0], [2, 0], [0, 0], [1, 0]]]})
    ]))

    case.assertDictEqual(objects, {
      'abcaLine': {'type': "LineString", 'arcs': {0: 0, 1: 3}},
      'bcabPolygon': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]}
    })

  @it.should("dedup ring ABCA & line BCAB have no cuts")
  def test_dedup_ring_abca_line_bcab(case):

    objects = do_dedup(OrderedDict([
      ('bcabLine', {'type': "LineString", 'coordinates': [[1, 0], [2, 0], [0, 0], [1, 0]]}),
      ('abcaPolygon', {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [2, 0], [0, 0]]]}) # rotated to BCAB
    ]))

    case.assertDictEqual(objects, {
      'bcabLine': {'type': "LineString", 'arcs': {0: 0, 1: 3}},
      'abcaPolygon': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]}
    })

  @it.should("dedup when an old arc ABC extends a new arc AB, ABC is cut into AB-BC")
  def test_dedup_ab_extends_abc(case):

    objects = do_dedup({
      'abc': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0]]},
      'ab': {'type': "LineString", 'coordinates': [[0, 0], [1, 0]]}
    })

    case.assertDictEqual(objects, {
      'abc': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 1, 1: 2}}},
      'ab': {'type': "LineString", 'arcs': {0: 0, 1: 1}}
    })

  @it.should("dedup when a reversed old arc CBA extends a new arc AB, CBA is cut into CB-BA")
  def test_dedup_cba_extends_ab(case):

    objects = do_dedup({
      'cba': {'type': "LineString", 'coordinates': [[2, 0], [1, 0], [0, 0]]},
      'ab': {'type': "LineString", 'coordinates': [[0, 0], [1, 0]]}
    })

    case.assertDictEqual(objects, {
      'cba': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 1, 1: 2}}},
      'ab': {'type': "LineString", 'arcs': {0: 2, 1: 1}}
    })

  @it.should("dedup when a new arc ADE shares its start with an old arc ABC, there are no cuts")
  def test_dedup_ade_extends_abc(case):

    objects = do_dedup({
      'ade': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0]]},
      'abc': {'type': "LineString", 'coordinates': [[0, 0], [1, 1], [2, 1]]}
    })

    case.assertDictEqual(objects, {
      'ade': {'type': "LineString", 'arcs': {0: 0, 1: 2}},
      'abc': {'type': "LineString", 'arcs': {0: 3, 1: 5}}
    })

  @it.should("dedup ring ABA has no cuts")
  def test_dedup_ring_aba(case):

    objects = do_dedup({
      'aba': {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [0, 0]]]},
    })

    case.assertDictEqual(objects, {
      'aba': {'type': "Polygon", 'arcs': [{0: 0, 1: 2}]}
    })

  @it.should("dedup ring AA has no cuts")
  def test_dedup_ring_aa(case):

    objects = do_dedup({
      'aa': {'type': "Polygon", 'coordinates': [[[0, 0], [0, 0]]]},
    })

    case.assertDictEqual(objects, {
    'aa': {'type': "Polygon", 'arcs': [{0: 0, 1: 1}]}
  })

  @it.should("dedup degenerate ring A has no cuts")
  def test_dedup_ring_a(case):

    objects = do_dedup({
      'a': {'type': "Polygon", 'coordinates': [[[0, 0]]]},
    })

    case.assertDictEqual(objects, {
      'a': {'type': "Polygon", 'arcs': [{0: 0, 1: 0}]}
    })

  @it.should("dedup when a new line DEC shares its end with an old line ABC, there are no cuts")
  def test_dedup_dec_extends_abc(case):

    objects = do_dedup({
      'abc': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0]]},
      'dec': {'type': "LineString", 'coordinates': [[0, 1], [1, 1], [2, 0]]}
    })

    case.assertDictEqual(objects, {
      'abc': {'type': "LineString", 'arcs': {0: 0, 1: 2}},
      'dec': {'type': "LineString", 'arcs': {0: 3, 1: 5}}
    })

  @it.should("dedup when a new line ABC extends an old line AB, ABC is cut into AB-BC")
  def test_dedup_abc_extends_ab(case):

    objects = do_dedup({
    'ab': {'type': "LineString", 'coordinates': [[0, 0], [1, 0]]},
    'abc': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0]]}
  })

    case.assertDictEqual(objects, {
    'ab': {'type': "LineString", 'arcs': {0: 0, 1: 1}},
    'abc': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 3, 1: 4}}}
  })

  @it.should("dedup when a new line ABC extends a reversed old line BA, ABC is cut into AB-BC")
  def test_dedup_abc_extends_ba(case):

    objects = do_dedup(OrderedDict([
      ('ba', {'type': "LineString", 'coordinates': [[1, 0], [0, 0]]}),
      ('abc', {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0]]})
    ]))

    case.assertDictEqual(objects, {
      'ba': {'type': "LineString", 'arcs': {0: 0, 1: 1}},
      'abc': {'type': "LineString", 'arcs': {0: 1, 1: 0, 'next': {0: 3, 1: 4}}}
    })

  @it.should("dedup when a new line starts BC in the middle of an old line ABC, ABC is cut into AB-BC")
  def test_dedup_bc_joins_abc(case):

    objects = do_dedup({
      'abc': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0]]},
      'bc': {'type': "LineString", 'coordinates': [[1, 0], [2, 0]]}
    })

    case.assertDictEqual(objects, {
      'abc': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 1, 1: 2}}},
      'bc': {'type': "LineString", 'arcs': {0: 1, 1: 2}}
    })

  @it.should("dedup when a new line BC starts in the middle of a reversed old line CBA, CBA is cut into CB-BA")
  def test_dedup_bc_joins_cba(case):

    objects = do_dedup({
      'cba': {'type': "LineString", 'coordinates': [[2, 0], [1, 0], [0, 0]]},
      'bc': {'type': "LineString", 'coordinates': [[1, 0], [2, 0]]}
    })

    case.assertDictEqual(objects, {
      'cba': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 1, 1: 2}}},
      'bc': {'type': "LineString", 'arcs': {0: 1, 1: 0}}
    })

  @it.should("dedup when a new line ABD deviates from an old line ABC, ABD is cut into AB-BD and ABC is cut into AB-BC")
  def test_dedup_abc_deviates_from_abc(case):

    objects = do_dedup({
      'abc': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0]]},
      'abd': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [3, 0]]}
    })

    case.assertDictEqual(objects, {
      'abc': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 1, 1: 2}}},
      'abd': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 4, 1: 5}}}
    })

  @it.should("dedup when a new line ABD deviates from a reversed old line CBA, CBA is cut into CB-BA and ABD is cut into AB-BD")
  def test_dedup_abc_deviates_from_cba(case):

    objects = do_dedup({
      'cba': {'type': "LineString", 'coordinates': [[2, 0], [1, 0], [0, 0]]},
      'abd': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [3, 0]]}
    })

    case.assertDictEqual(objects, {
      'cba': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 1, 1: 2}}},
      'abd': {'type': "LineString", 'arcs': {0: 2, 1: 1, 'next': {0: 4, 1: 5}}}
    })

  @it.should("dedup when a new line DBC merges into an old line ABC, DBC is cut into DB-BC and ABC is cut into AB-BC")
  def test_dedup_dbc_merges_abc(case):

    objects = do_dedup(OrderedDict([
      ('abc', {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0]]}),
      ('dbc', {'type': "LineString", 'coordinates': [[3, 0], [1, 0], [2, 0]]})
    ]))

    case.assertDictEqual(objects, {
      'abc': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 1, 1: 2}}},
      'dbc': {'type': "LineString", 'arcs': {0: 3, 1: 4, 'next': {0: 1, 1: 2}}}
    })


  @it.should("dedup when a new line DBC merges into a reversed old line CBA, DBC is cut into DB-BC and CBA is cut into CB-BA")
  def test_dedup_dbc_merges_cba(case):

    objects = do_dedup(OrderedDict([
      ('cba', {'type': "LineString", 'coordinates': [[2, 0], [1, 0], [0, 0]]}),
      ('dbc', {'type': "LineString", 'coordinates': [[3, 0], [1, 0], [2, 0]]})
    ]))

    case.assertDictEqual(objects, {
      'cba': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 1, 1: 2}}},
      'dbc': {'type': "LineString", 'arcs': {0: 3, 1: 4, 'next': {0: 1, 1: 0}}}
    })


  @it.should("dedup when a new line DBE shares a single midpoint with an old line ABC, DBE is cut into DB-BE and ABC is cut into AB-BC")
  def test_dedup_dbe_joins_abc(case):

    objects = do_dedup({
      'abc': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0]]},
      'dbe': {'type': "LineString", 'coordinates': [[0, 1], [1, 0], [2, 1]]}
    })

    case.assertDictEqual(objects, {
      'abc': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 1, 1: 2}}},
      'dbe': {'type': "LineString", 'arcs': {0: 3, 1: 4, 'next': {0: 4, 1: 5}}}
    })


  @it.should("dedup when a new line ABDE skips a point with an old line ABCDE, ABDE is cut into AB-BD-DE and ABCDE is cut into AB-BCD-DE")
  def test_dedup_abde_skips_c_in_abcde(case):

    objects = do_dedup(OrderedDict([
      ('abcde', {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]}),
      ('abde', {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [3, 0], [4, 0]]})
    ]))

    case.assertDictEqual(objects, {
      'abcde': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 1, 1: 3, 'next': {0: 3, 1: 4}}}},
      'abde': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 6, 1: 7, 'next': {0: 3, 1: 4}}}}
    })


  @it.should("dedup when a new line ABDE skips a point with a reversed old line EDCBA, ABDE is cut into AB-BD-DE and EDCBA is cut into ED-DCB-BA")
  def test_dedup_abde_skips_c_in_edcba(case):

    objects = do_dedup({
      'edcba': {'type': "LineString", 'coordinates': [[4, 0], [3, 0], [2, 0], [1, 0], [0, 0]]},
      'abde': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [3, 0], [4, 0]]}
    })

    case.assertDictEqual(objects, {
      'edcba': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 1, 1: 3, 'next': {0: 3, 1: 4}}}},
      'abde': {'type': "LineString", 'arcs': {0: 4, 1: 3, 'next': {0: 6, 1: 7, 'next': {0: 1, 1: 0}}}}
    })


  @it.should("dedup when a line ABCDBE self-intersects with its middle, it is not cut")
  def test_dedup_abcbe_self_intersects(case):

    objects = do_dedup({
      'abcdbe': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0], [3, 0], [1, 0], [4, 0]]}
    })

    case.assertDictEqual(objects, {
      'abcdbe': {'type': "LineString", 'arcs': {0: 0, 1: 5}}
    })


  @it.should("dedup when a line ABACD self-intersects with its start, it is cut into ABA-ACD")
  def test_dedup_abacd_self_intersects(case):

    objects = do_dedup({
      'abacd': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [0, 0], [3, 0], [4, 0]]}
    })

    case.assertDictEqual(objects, {
      'abacd': {'type': "LineString", 'arcs': {0: 0, 1: 2, 'next': {0: 2, 1: 4}}}
    })


  @it.should("dedup when a line ABDCD self-intersects with its end, it is cut into ABD-DCD")
  def test_dedup_abdcd_self_intersects(case):

    objects = do_dedup({
      'abdcd': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [4, 0], [3, 0], [4, 0]]}
    })

    case.assertDictEqual(objects, {
      'abdcd': {'type': "LineString", 'arcs': {0: 0, 1: 2, 'next': {0: 2, 1: 4}}}
    })


  @it.should("dedup when an old line ABCDBE self-intersects and shares a point B, ABCDBE is cut into AB-BCDB-BE and FBG is cut into FB-BG")
  def test_dedup_abcdbe_self_intersects(case):

    objects = do_dedup(OrderedDict([
      ('abcdbe', {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [2, 0], [3, 0], [1, 0], [4, 0]]}),
      ('fbg', {'type': "LineString", 'coordinates': [[0, 1], [1, 0], [2, 1]]})
    ]))

    case.assertDictEqual(objects, {
      'abcdbe': {'type': "LineString", 'arcs': {0: 0, 1: 1, 'next': {0: 1, 1: 4, 'next': {0: 4, 1: 5}}}},
      'fbg': {'type': "LineString", 'arcs': {0: 6, 1: 7, 'next': {0: 7, 1: 8}}}
    })


  @it.should("dedup when a line ABCA is closed, there are no cuts")
  def test_dedup_closed_line_abca(case):

    objects = do_dedup({
      'abca': {'type': "LineString", 'coordinates': [[0, 0], [1, 0], [0, 1], [0, 0]]}
    })

    case.assertDictEqual(objects, {
      'abca': {'type': "LineString", 'arcs': {0: 0, 1: 3}}
    })


  @it.should("dedup when a ring ABCA is closed, there are no cuts")
  def test_dedup_ring_abca(case):

    objects = do_dedup({
      'abca': {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [0, 1], [0, 0]]]}
    })

    case.assertDictEqual(objects, {
      'abca': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]}
    })


  @it.should("dedup exact duplicate rings ABCA & ABCA have no cuts")
  def test_dedup_rings_abca_abca(case):

    objects = do_dedup({
      'abca': {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [0, 1], [0, 0]]]},
      'abca2': {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [0, 1], [0, 0]]]}
    })

    case.assertDictEqual(objects, {
      'abca': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]},
      'abca2': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]}
    })


  @it.should("dedup reversed duplicate rings ABCA & ACBA have no cuts")
  def test_dedup_rings_abcs_acba(case):

    objects = do_dedup(OrderedDict([
      ('abca', {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [0, 1], [0, 0]]]}),
      ('acba', {'type': "Polygon", 'coordinates': [[[0, 0], [0, 1], [1, 0], [0, 0]]]})
    ]))

    case.assertDictEqual(objects, {
      'abca': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]},
      'acba': {'type': "Polygon", 'arcs': [{0: 3, 1: 0}]}
    })


  @it.should("dedup coincident rings ABCA & BCAB have no cuts")
  def test_dedup_rings_abcs_bcan(case):

    objects = do_dedup({
      'abca': {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [0, 1], [0, 0]]]},
      'bcab': {'type': "Polygon", 'coordinates': [[[1, 0], [0, 1], [0, 0], [1, 0]]]}
    })

    case.assertDictEqual(objects, {
      'abca': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]},
      'bcab': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]}
    })


  @it.should("dedup coincident reversed rings ABCA & BACB have no cuts")
  def test_dedup_rings_abcs_bacb(case):

    objects = do_dedup(OrderedDict([
      ('abca', {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [0, 1], [0, 0]]]}),
      ('bacb', {'type': "Polygon", 'coordinates': [[[1, 0], [0, 0], [0, 1], [1, 0]]]})
    ]))

    case.assertDictEqual(objects, {
      'abca': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]},
      'bacb': {'type': "Polygon", 'arcs': [{0: 3, 1: 0}]}
    })


  @it.should("dedup coincident rings ABCDA, EFAE & GHCG are cut into ABC-CDA, EFAE and GHCG")
  def test_dedup_abcda_efae_ghcg(case):

    objects = do_dedup(OrderedDict([
      ('abcda', {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]}),
      ('efae', {'type': "Polygon", 'coordinates': [[[0, -1], [1, -1], [0, 0], [0, -1]]]}),
      ('ghcg', {'type': "Polygon", 'coordinates': [[[0, 2], [1, 2], [1, 1], [0, 2]]]})
    ]))

    case.assertDictEqual(objects, {
      'abcda': {'type': "Polygon", 'arcs': [{0: 0, 1: 2, 'next': {0: 2, 1: 4}}]},
      'efae': {'type': "Polygon", 'arcs': [{0: 5, 1: 8}]},
      'ghcg': {'type': "Polygon", 'arcs': [{0: 9, 1: 12}]}
    })


  @it.should("dedup coincident rings ABCA & DBED have no cuts, but are rotated to share B")
  def test_dedup_abca_dbed(case):

    objects = do_dedup({
      'abca': {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [0, 1], [0, 0]]]},
      'dbed': {'type': "Polygon", 'coordinates': [[[2, 1], [1, 0], [2, 2], [2, 1]]]}
    })

    case.assertDictEqual(objects, {
      'abca': {'type': "Polygon", 'arcs': [{0: 0, 1: 3}]},
      'dbed': {'type': "Polygon", 'arcs': [{0: 4, 1: 7}]}
    })

#   test.deepEqual(topology.coordinates.slice(0, 4), [[1, 0], [0, 1], [0, 0], [1, 0]]);
#   test.deepEqual(topology.coordinates.slice(4, 8), [[1, 0], [2, 2], [2, 1], [1, 0]])


  @it.should("dedup overlapping rings ABCDA and BEFCB are cut into BC-CDAB and BEFC-CB")
  def test_dedup_rings_abcda_befcb(case):

    objects = do_dedup({
      'abcda': {'type': "Polygon", 'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]}, # rotated to BCDAB, cut BC-CDAB
      'befcb': {'type': "Polygon", 'coordinates': [[[1, 0], [2, 0], [2, 1], [1, 1], [1, 0]]]}
    })

    case.assertDictEqual(objects, {
      'abcda': {'type': "Polygon", 'arcs': [{0: 0, 1: 1, 'next': {0: 1, 1: 4}}]},
      'befcb': {'type': "Polygon", 'arcs': [{0: 5, 1: 8, 'next': {0: 1, 1: 0}}]}
    })


it.createTests(globals())

if __name__ == '__main__':
  nose2.main()