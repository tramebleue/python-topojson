# coding: utf-8

import unittest
import nose2
from nose2.tools import such
from topojson.topology import topology

with such.A('GeoJSON object converted to TopoJSON topology') as it:

    with it.having('Duplicate lines ABC & ABC'):

        @it.should('contain a shared arc ABC')
        def test_duplicate_abc(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 2, 0],
                    'arcs': [
                        [[0, 0], [1, 0], [2, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [0]
                        }
                    }
                })

    with it.having('Reversed duplicate lines ABC & CBA'):

        @it.should('contain a shared arc ABC')
        def test_reversed_duplicate_abc(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[2, 0], [1, 0], [0, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 2, 0],
                    'arcs': [
                        [[0, 0], [1, 0], [2, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [~0]
                        }
                    }
                })


    with it.having('an old arc ABC that extends a new arc AB'):

        @it.should("contain a shared arc AB")
        def test_shared_ab(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 2, 0],
                    'arcs': [
                          [[0, 0], [1, 0]],
                          [[1, 0], [2, 0]]
                    ],
                    'objects': {
                        'foo': {
                                'type': "LineString",
                                'arcs': [0, 1]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [0]
                        }
                    }
              })

    with it.having('an old arc CBA that extends a new arc AB'):

        @it.should("contain a shared arc BA")
        def test_cba_extends_ab(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[2, 0], [1, 0], [0, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 2, 0],
                    'arcs': [
                          [[2, 0], [1, 0]],
                          [[1, 0], [0, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0, 1]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [~1]
                        }
                    }
              })

    with it.having('a new arc ADE that shares its start with an old arc ABC'):

        @it.should("contain no shared arc")
        def test_ade_abc(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 1], [2, 1]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 2, 1],
                    'arcs': [
                          [[0, 0], [1, 0], [2, 0]],
                          [[0, 0], [1, 1], [2, 1]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [1]
                        }
                    }
              })

    with it.having('a new arc DEC that shares its start with an old arc ABC'):

        @it.should("contain no shared arc")
        def test_dec_abc(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 1], [2, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 2, 1],
                    'arcs': [
                          [[0, 0], [1, 0], [2, 0]],
                          [[0, 0], [1, 1], [2, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [1]
                        }
                    }
              })

    with it.having('a new arc ABC that extends an old arc AB'):

        @it.should("contain a shared arc AB")
        def test_abc_extends_ab(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 2, 0],
                    'arcs': [
                          [[0, 0], [1, 0]],
                          [[1, 0], [2, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [0, 1]
                        }
                    }
              })

    with it.having('a new arc ABC that extends a reversed old arc BA'):

        @it.should("contain a shared arc BA")
        def test_abc_extends_ba(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[1, 0], [0, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 2, 0],
                    'arcs': [
                          [[1, 0], [0, 0]],
                          [[1, 0], [2, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [~0, 1]
                        }
                    }
              })

    with it.having('a new arc that starts BC in the middle of an old arc ABC'):

        @it.should("contain a shared arc BC")
        def test_bc_extends_abc(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[1, 0], [2, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 2, 0],
                    'arcs': [
                          [[0, 0], [1, 0]],
                          [[1, 0], [2, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0, 1]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [1]
                        }
                    }
              })

    with it.having('a new arc BC that starts in the middle of a reversed old arc CBA'):

        @it.should("contain a shared arc CB")
        def test_bc_extends_cba(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[2, 0], [1, 0], [0, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[1, 0], [2, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 2, 0],
                    'arcs': [
                          [[2, 0], [1, 0]],
                          [[1, 0], [0, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0, 1]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [~0]
                        }
                    }
              })

    with it.having('a new arc ABD that deviates from an old arc ABC'):

        @it.should("contain a shared arc AB")
        def test_abd_extends_abc(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [3, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 3, 0],
                    'arcs': [
                          [[0, 0], [1, 0]],
                          [[1, 0], [2, 0]],
                          [[1, 0], [3, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0, 1]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [0, 2]
                        }
                    }
              })


    with it.having("a new arc ABD that deviates from a reversed old arc CBA"):

        @it.should("contain a shared arc CBA")
        def test_abd_extends_cba(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[2, 0], [1, 0], [0, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [3, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 3, 0],
                    'arcs': [
                          [[2, 0], [1, 0]],
                          [[1, 0], [0, 0]],
                          [[1, 0], [3, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0, 1]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [~1, 2]
                        }
                    }
              })

    with it.having("a new arc DBC that merges into an old arc ABC"):

        @it.should("contain a shared arc BC")
        def test_dbc_merges_abc(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[3, 0], [1, 0], [2, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 3, 0],
                    'arcs': [
                          [[0, 0], [1, 0]],
                          [[1, 0], [2, 0]],
                          [[3, 0], [1, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0, 1]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [2, 1]
                        }
                    }
              })

    with it.having("a new arc DBC that merges into a reversed old arc CBA"):

        @it.should("contain a shared arc CB")
        def test_dbc_merges_cba(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[2, 0], [1, 0], [0, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[3, 0], [1, 0], [2, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 3, 0],
                    'arcs': [
                          [[2, 0], [1, 0]],
                          [[1, 0], [0, 0]],
                          [[3, 0], [1, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0, 1]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [2, ~0]
                        }
                    }
              })

    with it.having("a new arc DBE that shares a single midpoint with an old arc ABC"):

        @it.should("contain no shared arc")
        def test_dbe_joins_abc(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 1], [1, 0], [2, 1]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 2, 1],
                    'arcs': [
                        [[0, 0], [1, 0]],
                        [[1, 0], [2, 0]],
                        [[0, 1], [1, 0]],
                        [[1, 0], [2, 1]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0, 1]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [2, 3]
                        }
                    }
              })

    with it.having("a new arc ABDE that skips a point with an old arc ABCDE, they share arcs AB and DE"):

        @it.should("contain two shared arcs AB and DE")
        def test_abde_skips_abcde(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [3, 0], [4, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 4, 0],
                    'arcs': [
                        [[0, 0], [1, 0]],
                        [[1, 0], [2, 0], [3, 0]],
                        [[3, 0], [4, 0]],
                        [[1, 0], [3, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0, 1, 2]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [0, 3, 2]
                        }
                    }
              })

    with it.having("a new arc ABDE that skips a point with a reversed old arc EDCBA"):

        @it.should("contain two shared arcs BA and ED")
        def test_abde_skips_edcba(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[4, 0], [3, 0], [2, 0], [1, 0], [0, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [3, 0], [4, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 4, 0],
                    'arcs': [
                        [[4, 0], [3, 0]],
                        [[3, 0], [2, 0], [1, 0]],
                        [[1, 0], [0, 0]],
                        [[1, 0], [3, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0, 1, 2]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [~2, 3, ~0]
                        }
                    }
              })

    with it.having("an arc ABCDBE that self-intersects"):

        @it.should("still contain one arc")
        def test_abcdbe(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0], [3, 0], [1, 0], [4, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 4, 0],
                    'arcs': [
                        [[0, 0], [1, 0], [2, 0], [3, 0], [1, 0], [4, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0]
                        }
                    }
              })


    with it.having("an old arc ABCDBE that self-intersects and shares a point B"):

        @it.should("split the old arc into multiple cuts")
        def test_abcdbe_joins_b(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [2, 0], [3, 0], [1, 0], [4, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 1], [1, 0], [2, 1]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 4, 1],
                    'arcs': [
                        [[0, 0], [1, 0]],
                        [[1, 0], [2, 0], [3, 0], [1, 0]],
                        [[1, 0], [4, 0]],
                        [[0, 1], [1, 0]],
                        [[1, 0], [2, 1]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0, 1, 2]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [3, 4]
                        }
                    }
              })

    with it.having("an arc ABCA that is closed"):

        @it.should("still produce one arc")
        def test_closed_abca(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates':  [[0, 0], [1, 0], [0, 1], [0, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 1, 1],
                    'arcs': [
                        [[0, 0], [1, 0], [0, 1], [0, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0]
                        }
                    }
              })

    with it.having("duplicate closed lines ABCA & ABCA that share the arc ABCA"):

        @it.should("produce one shared arc ABCA")
        def test_abca_abca(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [0, 1], [0, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [0, 1], [0, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 1, 1],
                    'arcs': [
                        [[0, 0], [1, 0], [0, 1], [0, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [0]
                        }
                    }
              })

    with it.having("reversed duplicate closed lines ABCA & ACBA that share the arc ABCA"):

        @it.should("produce one shared arc ABCA")
        def test_abca_acba(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 0], [0, 1], [0, 0]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [0, 1], [1, 0], [0, 0]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 1, 1],
                    'arcs': [
                        [[0, 0], [1, 0], [0, 1], [0, 0]]
                    ],
                    'objects': {
                        'foo': {
                            'type': "LineString",
                            'arcs': [0]
                        },
                        'bar': {
                            'type': "LineString",
                            'arcs': [~0]
                        }
                    }
              })


    with it.having("two coincident closed polygons ABCA & BCAB"):

        @it.should("produce one shared arc BCAB")
        def test_abca_bcab(case):

            geojson = {
                'abca': {
                    'type': "Polygon",
                    'coordinates': [[[0, 0], [1, 0], [0, 1], [0, 0]]]
                },
                'bcab': {
                    'type': "Polygon",
                    'coordinates': [[[1, 0], [0, 1], [0, 0], [1, 0]]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 1, 1],
                    'arcs': [
                        [[1, 0], [0, 1], [0, 0], [1, 0]]
                    ],
                    'objects': {
                        'abca': {
                            'type': "Polygon",
                            'arcs': [[0]]
                        },
                        'bcab': {
                            'type': "Polygon",
                            'arcs': [[0]]
                        }
                    }
              })

    with it.having("two coincident reversed closed polygons ABCA & BACB"):

        @it.should("produce one shared arc BCAB")
        def test_abca_bacb(case):

            geojson = {
                'abca': {
                    'type': "Polygon",
                    'coordinates': [[[0, 0], [1, 0], [0, 1], [0, 0]]]
                },
                'bacb': {
                    'type': "Polygon",
                    'coordinates': [[[1, 0], [0, 0], [0, 1], [1, 0]]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 1, 1],
                    'arcs': [
                        [[1, 0], [0, 0], [0, 1], [1, 0]]
                    ],
                    'objects': {
                        'abca': {
                            'type': "Polygon",
                            'arcs': [[~0]]
                        },
                        'bacb': {
                            'type': "Polygon",
                            'arcs': [[0]]
                        }
                    }
              })

    with it.having("two coincident closed polygons ABCA & DBED"):

        @it.should("produce a shared point B")
        def test_abca_dbed(case):

            geojson = {
                'abca': {
                    'type': "Polygon",
                    'coordinates': [[[0, 0], [1, 0], [0, 1], [0, 0]]]
                },
                'dbed': {
                    'type': "Polygon",
                    'coordinates': [[[2, 1], [1, 0], [2, 2], [2, 1]]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo,
                {
                    'type': "Topology",
                    'bbox': [0, 0, 2, 2],
                    'arcs': [
                        [[1, 0], [0, 1], [0, 0], [1, 0]],
                        [[1, 0], [2, 2], [2, 1], [1, 0]]
                    ],
                    'objects': {
                        'abca': {
                            'type': "Polygon",
                            'arcs': [[0]]
                        },
                        'dbed': {
                            'type': "Polygon",
                            'arcs': [[1]]
                        }
                    }
              })

    with it.having("two input objects"):

        # The topology `objects` is a map of geometry objects by name, allowing
        # multiple GeoJSON geometry objects to share the same topology. When you
        # pass multiple input files to bin/topojson, the basename of the file is
        # used as the key, but you're welcome to edit the file to change it.

        @it.should("map objects to topology.objects")
        def test_map_objects(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[.1, .2], [.3, .4]]
                },
                'bar': {
                    'type': "Polygon",
                    'coordinates': [[[.5, .6], [.7, .8]]]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertEqual(topo['objects']['foo']['type'], "LineString")
            case.assertEqual(topo['objects']['bar']['type'], "Polygon")

    with it.having("GeoJSON features"):

        # TopoJSON doesn't use features because you can represent the same
        # information more compactly just by using geometry objects.

        @it.should('map features to geometries')
        def test_map_features_to_geometries(case):

            geojson = {
                'foo': {
                    'type': "Feature",
                    'geometry': {
                        'type': "LineString",
                        'coordinates': [[.1, .2], [.3, .4]]
                    }
                },
                'bar': {
                    'type': "Feature",
                    'geometry': {
                        'type': "Polygon",
                        'coordinates': [[[.5, .6], [.7, .8]]]
                    }
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertEqual(topo['objects']['foo']['type'], "LineString")
            case.assertEqual(topo['objects']['bar']['type'], "Polygon")

    with it.having("GeoJSON Geometry Collection"):

        @it.should('map collection to geometries')
        def test_map_geometrycollection_to_geometries(case):

            geojson = {
                'collection': {
                    'type': "GeometryCollection",
                    'geometries': [
                        {
                            'type': "LineString",
                            'coordinates': [[.1, .2], [.3, .4]]
                        },
                        {
                            'type': "Polygon",
                            'coordinates': [[[.5, .6], [.7, .8]]]
                        }
                    ]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertEqual(topo['objects']['collection']['type'], "GeometryCollection")
            case.assertEqual(len(topo['objects']['collection']['geometries']), 2)
            case.assertEqual(topo['objects']['collection']['geometries'][0]['type'], "LineString")
            case.assertEqual(topo['objects']['collection']['geometries'][1]['type'], "Polygon")

    with it.having("GeoJSON Feature Collection"):

        @it.should('map features to geometries')
        def test_map_featurecollection_to_geometries(case):

            geojson = {
                'collection': {
                    'type': "FeatureCollection",
                    'features': [
                        {
                            'type': "Feature",
                            'geometry': {
                                'type': "LineString",
                                'coordinates': [[.1, .2], [.3, .4]]
                            }
                        },
                        {
                            'type': "Feature",
                            'geometry': {
                                'type': "Polygon",
                                'coordinates': [[[.5, .6], [.7, .8]]]
                            }
                        }
                    ]
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertEqual(topo['objects']['collection']['type'], "FeatureCollection")
            case.assertEqual(len(topo['objects']['collection']['geometries']), 2)
            case.assertEqual(topo['objects']['collection']['geometries'][0]['type'], "LineString")
            case.assertEqual(topo['objects']['collection']['geometries'][1]['type'], "Polygon")

    with it.having("nested geometry collections"):

        @it.should('preserve nested collections')
        def test_preserve_nested_geometry_collections(case):

            geojson = {
                'collection': {
                'type': "GeometryCollection",
                    'geometries': [
                        {
                            'type': "GeometryCollection",
                            'geometries': [
                                {'type': "LineString", 'coordinates': [[.1, .2], [.3, .4]]}
                            ]
                        },
                        {
                            'type': "Polygon",
                            'coordinates': [[[.5, .6], [.7, .8]]]}
                    ]
                }
            }

            topo = topology(geojson, quantization=0)
    
            case.assertEqual(len(topo['objects']['collection']['geometries'][0]['geometries'][0]['arcs']), 1);

    with it.having("null geometry objects in geometry collection"):

        @it.should('preserve null geometries')
        def preserve_null_geometries_in_geometrycollection(case):


            geojson = {
                'collection': {
                      'type': "GeometryCollection",
                      'geometries': [
                            None,
                            {
                                'type': "Polygon",
                                'coordinates': [[[.5, .6], [.7, .8]]]}
                      ]
                    }
                }

            topo = topology(geojson, quantization=0)

            case.assertEqual(topo['objects']['collection']['type'], "GeometryCollection")
            case.assertEqual(len(topo['objects']['collection']['geometries']), 2)
            case.assertEqual(topo['objects']['collection']['geometries'][0]['type'], None)
            case.assertEqual(topo['objects']['collection']['geometries'][1]['type'], "Polygon")

    with it.having("null geometry objects in feature collection"):

        @it.should('preserve null geometries')
        def preserve_null_geometries_in_featurecollection(case):


            geojson = {
                'collection': {
                      'type': "FeatureCollection",
                      'features': [
                            {
                                'type': "Feature",
                                'geometry': None
                            },
                            {
                                'type': "Feature",
                                'geometry': {
                                    'type': "Polygon",
                                    'coordinates': [[[.5, .6], [.7, .8]]]
                                }
                            }
                      ]
                    }
                }

            topo = topology(geojson, quantization=0)

            case.assertEqual(topo['objects']['collection']['type'], "FeatureCollection")
            case.assertEqual(len(topo['objects']['collection']['geometries']), 2)
            case.assertEqual(topo['objects']['collection']['geometries'][0]['type'], None)
            case.assertEqual(topo['objects']['collection']['geometries'][1]['type'], "Polygon")


    # with it.having("top-level features with null geometry objects"):

    #     @it.should('preserve null geometries')
    #     def preserve_toplevel_null_geometries(case):


    #         geojson = {
    #             'feature': {'type': "Feature", 'geometry': None}
    #         }

    #         topo = topology(geojson, quantization=0)

    #         case.assertDictEqual(topo['objects'],
    #             {
    #                 'feature': { 'type': None }
    #             })

    with it.having("a GeoJSON feature with an id"):

        # To know what a geometry object represents, specify an id. I prefer
        # numeric identifiers, such as ISO 3166-1 numeric, but strings work too.

        @it.should('report feature id')
        def test_preserve_feature_ids(case):

            geojson = {
                'foo': {
                    'type': "Feature",
                    'id': 42,
                    'properties': {},
                    'geometry': {
                        'type': "LineString",
                        'coordinates': [[.1, .2], [.3, .4]]
                    }
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertEqual(topo['objects']['foo']['type'], "LineString")
            case.assertEqual(topo['objects']['foo']['id'], 42)

    with it.having("a GeoJSON feature with a bbox"):

        # To know what a geometry object represents, specify an id. I prefer
        # numeric identifiers, such as ISO 3166-1 numeric, but strings work too.

        @it.should('report bbox')
        def test_preserve_feature_bbox(case):

            geojson = {
                'foo': {
                    'type': "Feature",
                    'bbox': [0, 0, 10, 10],
                    'properties': {},
                    'geometry': {
                        'type': "LineString",
                        'coordinates': [[.1, .2], [.3, .4]]
                    }
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertEqual(topo['objects']['foo']['type'], "LineString")
            case.assertListEqual(topo['objects']['foo']['bbox'], [0, 0, 10, 10])

    with it.having("a GeoJSON feature with properties"):

        # To know what a geometry object represents, specify an id. I prefer
        # numeric identifiers, such as ISO 3166-1 numeric, but strings work too.

        @it.should('preserce properties if not empty')
        def test_preserve_feature_properties(case):

            geojson = {
                'foo': {
                    'type': "Feature",
                    'id': 'Foo',
                    'properties': { "name": "Georges" },
                    'geometry': {
                        'type': "LineString",
                        'coordinates': [[.1, .2], [.3, .4]]
                    }
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertDictEqual(topo['objects']['foo']['properties'], { "name": "Georges" })

            geojson = {
                'foo': {
                    'type': "Feature",
                    'id': 'Foo',
                    'properties': { "name": "Georges" },
                    'geometry': {
                        'type': 'GeometryCollection',
                        'geometries': [
                            {
                                'type': "LineString",
                                'coordinates': [[.1, .2], [.3, .4]]
                            }
                        ]
                    }
                }
            }

            case.assertDictEqual(topo['objects']['foo']['properties'], { "name": "Georges" })

            geojson = {
                'foo': {
                    'type': "Feature",
                    'id': 'Foo',
                    'properties': {},
                    'geometry': {
                        'type': "LineString",
                        'coordinates': [[.1, .2], [.3, .4]]
                    }
                }
            }

            topo = topology(geojson, quantization=0)

            case.assertFalse('properties' in topo['objects']['foo'])

    with it.having("coordinates quantization"):

        # It's not required by the specification that the transform exactly
        # encompass the input geometry, but this is a good test that the reference
        # implementation is working correctly.

        @it.should("return a scale transform that exactly encompasses the input geometry")
        def test_exact_transform(case):

            geojson = {
                'foo': {
                    'type': "Feature",
                    'geometry': {
                        'type': "LineString",
                        'coordinates': [[1./8, 1./16], [1./2, 1./4]]
                    }
                }
            }

            topo = topology(geojson, quantization=2)

            case.assertDictEqual(topo['transform'], {'scale': [3./8, 3./16], 'translate': [1./8, 1./16]})

            geojson = {
                'foo': {
                    'type': "Polygon",
                    'coordinates': [[[1./8, 1./16], [1./2, 1./16], [1./2, 1./4], [1./8, 1./4], [1./8, 1./16]]]
                }
            }

            topo = topology(geojson, quantization=2)

            case.assertDictEqual(topo['transform'], {'scale': [3./8, 3./16], 'translate': [1./8, 1./16]})

        # TopoJSON uses integers with delta encoding to represent geometry
        # efficiently. (Quantization is necessary for simplification anyway, so
        # that we can identify which points are shared by contiguous geometry
        # objects.) The delta encoding works particularly well because line strings
        # are not random: most points are very close to their neighbors!

        @it.should('delta encode coordinates')
        def test_delta_encode(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[1./8, 1./16], [1./2, 1./16], [1./8, 1./4], [1./2, 1./4]]
                }
            }

            topo = topology(geojson, quantization=2)

            case.assertListEqual(topo['arcs'], [[[0, 0], [1, 0], [-1, 1], [1, 0]]])

            geojson = {
                'foo': {
                    'type': "Polygon",
                    'coordinates': [[[1./8, 1./16], [1./2, 1./16], [1./2, 1./4], [1./8, 1./4], [1./8, 1./16]]]
                }
            }

            topo = topology(geojson, quantization=2)

            case.assertListEqual(topo['arcs'][0], [[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]])

        # TopoJSON uses integers with for points, also. However, there’s no delta-
        # encoding, even for MultiPoints. And, unlike other geometry objects,
        # points are still defined with coordinates rather than arcs.

        @it.should('not delta encode points and mutlipoints')
        def test_points_not_encoded(case):

            geojson = {
                'foo': {
                    'type': "Point",
                    'coordinates': [1./8, 1./16]
                },
                'bar': {
                    'type': "Point",
                    'coordinates': [1./2, 1./4]
                }
            }

            topo = topology(geojson, quantization=2)

            print topo

            case.assertListEqual(topo['arcs'], [])
            case.assertDictEqual(topo['objects']['foo'], {'type': "Point", 'coordinates': [0, 0]})
            case.assertDictEqual(topo['objects']['bar'], {'type': "Point", 'coordinates': [1, 1]})

            geojson = {
                'foo': {
                    'type': "MultiPoint",
                    'coordinates': [[1./8, 1./16], [1./2, 1./4]]
                }
            }

            topo = topology(geojson, quantization=2)

            case.assertListEqual(topo['arcs'], [])
            case.assertDictEqual(topo['objects']['foo'], {'type': "MultiPoint", 'coordinates': [[0, 0], [1, 1]]})

        # // Rounding is more accurate than flooring.
        @it.should("round to the closest integer coordinate to minimize error")
        def test_use_rounding_rather_than_flooring(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0.0, 0.0], [0.5, 0.5], [1.6, 1.6], [3.0, 3.0], [4.1, 4.1], [4.9, 4.9], [5.9, 5.9], [6.5, 6.5], [7.0, 7.0], [8.4, 8.4], [8.5, 8.5], [10, 10]]
                }
            }

            topo = topology(geojson, quantization=11)

            case.assertListEqual(topo['arcs'], [[[0, 0], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]])
            case.assertDictEqual(topo['transform'], {'scale': [1, 1], 'translate': [0, 0]})
            # test.deepEqual(client.feature(topology, topology.objects.foo).geometry.coordinates, [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, 10]]);

# // When rounding, we must be careful not to exceed [±180°, ±90°]!
# tape("topology quantization precisely preserves minimum and maximum values", function(test) {
#   var topology = topojson.topology({foo: {type: "LineString", coordinates: [[-180, -90], [0, 0], [180, 90]]}}, 3);
#   test.deepEqual(client.feature(topology, topology.objects.foo).geometry.coordinates, [[-180, -90], [0, 0], [180, 90]]);
#   test.deepEqual(topology.arcs, [[[0, 0], [1, 1], [1, 1]]]);
#   test.deepEqual(topology.transform, {scale: [180, 90], translate: [-180, -90]});
#   test.end();
# });

        # GeoJSON inputs are in floating point format, so some error may creep in
        # that prevents you from using exact match to determine shared points. The
        # default quantization, 1e4, allows for 10,000 differentiable points in
        # both dimensions. If you're using TopoJSON to represent especially high-
        # precision geometry, you might want to increase the precision; however,
        # this necessarily increases the output size and the likelihood of seams
        # between contiguous geometry after simplification. The quantization factor
        # should be a power of ten for the most efficient representation, since
        # JSON uses base-ten encoding for numbers.
        @it.should("topology precision of quantization is configurable")
        def test_quantization_is_configurable(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[1./8, 1./16], [1./2, 1./16], [1./8, 1./4], [1./2, 1./4]]
                }
            }

            topo = topology(geojson, quantization=3)

            case.assertListEqual(topo['arcs'][0], [[0, 0], [2, 0], [-2, 2], [2, 0]])

            # geojson = {
            #     'foo': {
            #         'type': "Polygon",
            #         'coordinates': [[[1./8, 1./16], [1./2, 1./16], [1./2, 1./4], [1./8, 1./4], [1./8, 1./16]]]
            #     }
            # }

            # topo = topology(geojson, quantization=5)

            # case.assertListEqual(topo['arcs'][0], [[0, 0], [4, 0], [0, 4], [-4, 0], [0, -4]])

        # Quantization may introduce coincident points, so these are removed.
        @it.should("remove topology coincident points")
        def test_remove_coincident_points(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[1./8, 1./16], [1./8, 1./16], [1./2, 1./4], [1./2, 1./4]]
                }
            }

            topo = topology(geojson, quantization=2)

            case.assertListEqual(topo['arcs'], [[[0, 0], [1, 1]]])

            geojson = {
                'foo': {
                    'type': "Polygon",
                    'coordinates': [[[1./8, 1./16], [1./2, 1./16], [1./2, 1./16], [1./2, 1./4], [1./8, 1./4], [1./8, 1./4], [1./8, 1./16]]]
                }
            }

            topo = topology(geojson, quantization=2)

            case.assertListEqual(topo['arcs'][0], [[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]])


        # Quantization may introduce degenerate features which have collapsed onto a single point.
        @it.should("preserve topology collapsed lines")
        def test_preserve_collapsed_lines(case):

            geojson = {
                'foo': {
                    'type': "LineString",
                    'coordinates': [[0, 0], [1, 1], [2, 2]]
                },
                'bar': {
                    'type': "LineString",
                    'coordinates': [[-80, -80], [0, 0], [80, 80]]
                }
            }

            topo = topology(geojson, quantization=3)

            case.assertDictEqual(topo['objects']['foo'], {'type': "LineString", 'arcs': [0]})
            case.assertListEqual(topo['arcs'][0], [[1, 1], [0, 0]])


        @it.should("preserve topology collapsed lines in a MultiLineString")
        def test_preserve_collapsed_lines_in_multilinestring(case):

            geojson = {
                'foo': {
                    'type': "MultiLineString",
                    'coordinates': [[[1./8, 1./16], [1./2, 1./4]], [[1./8, 1./16], [1./8, 1./16]], [[1./2, 1./4], [1./8, 1./16]]]
                }
            }

            topo = topology(geojson, quantization=2)

            case.assertListEqual(topo['arcs'][0], [[0, 0], [1, 1]])
            case.assertListEqual(topo['arcs'][1], [[0, 0], [0, 0]])
            case.assertListEqual(topo['objects']['foo']['arcs'], [[0], [1], [~0]])


        @it.should("preserve topology collapsed polygons")
        def test_preserve_collapsed_polygons(case):


            geojson = {
                'foo': {
                    'type': "Polygon",
                    'coordinates': [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]
                },
                'bar': {
                    'type': "Polygon",
                    'coordinates': [[[0, 0], [0, 1], [1, 1], [0, 0]]]
                },
                'bazz': {
                    'type': "MultiPoint",
                    'coordinates': [[-80, -80], [0, 0], [80, 80]]
                }
            }

            topo = topology(geojson, quantization=3)

            case.assertDictEqual(topo['objects']['foo'], {'type': "Polygon", 'arcs': [[0]]})
            case.assertDictEqual(topo['objects']['bar'], {'type': "Polygon", 'arcs': [[0]]})
            case.assertListEqual(topo['arcs'][0], [[1, 1], [0, 0]])

        @it.should("preserve topology collapsed lines in a MultiPolygon")
        def test_preserve_collapsed_lines_in_multipolygons(case):

            geojson = {
                'foo': {
                    'type': "MultiPolygon",
                    'coordinates': [
                        [[[1./8, 1./16], [1./2, 1./16], [1./2, 1./4], [1./8, 1./4], [1./8, 1./16]]],
                        [[[1./8, 1./16], [1./8, 1./16], [1./8, 1./16], [1./8, 1./16]]],
                        [[[1./8, 1./16], [1./8, 1./4], [1./2, 1./4], [1./2, 1./16], [1./8, 1./16]]]
                    ]
                }
            }

            topo = topology(geojson, quantization=2)

            case.assertTrue(len(topo['arcs']) > 0)
            case.assertTrue(len(topo['arcs'][0]) >= 2)
            case.assertEqual(len(topo['objects']['foo']['arcs']), 3)

        @it.should("preserved topology collapsed geometries in a GeometryCollection")
        def test_preserve_collapsed_geometries_in_geometrycollection(case):

            geojson = {
                'collection': {
                    'type': "FeatureCollection",
                    'features': [{'type': "Feature", 'geometry': {'type': "MultiPolygon", 'coordinates': []}}]
                }
            }

            topo = topology(geojson, quantization=2)

            case.assertEqual(len(topo['arcs']), 0)
            case.assertDictEqual(topo['objects']['collection'], {'type': "FeatureCollection", 'geometries': [{'type': "MultiPolygon", 'arcs': []}]})

        # // If one of the top-level objects in the input is empty, however, it is
        # // still preserved in the output.
        @it.should("not remove topology empty geometries")
        def test_empty_geometries_are_not_removed(case):

            geojson = {
                'foo': {
                    'type': "MultiPolygon",
                    'coordinates': []
                }
            }

            topo = topology(geojson, quantization=2)

            case.assertEqual(len(topo['arcs']), 0)
            case.assertDictEqual(topo['objects']['foo'], {'type': "MultiPolygon", 'arcs': []})

        @it.should("not remove topology empty polygons")
        def test_empty_polygons_are_not_removed(case):

            geojson = {
                'foo': {
                    'type': "FeatureCollection",
                    'features': [{'type': "Feature", 'geometry': {'type': "MultiPolygon", 'coordinates': [[]]}}]
                },
                'bar': {'type': "Polygon", 'coordinates': []}
            }

            topo = topology(geojson, quantization=2)

            case.assertEqual(len(topo['arcs']), 0)
            case.assertDictEqual(topo['objects']['foo'], {'type': "FeatureCollection", 'geometries': [{'type': "MultiPolygon", 'arcs': [[]]}]})
            case.assertDictEqual(topo['objects']['bar'], {'type': "Polygon", 'arcs': []})


it.createTests(globals())

if __name__ == '__main__':
    nose2.main()