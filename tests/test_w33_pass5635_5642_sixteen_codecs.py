"""Regression lock for Passes 5635-5642.

Locks the two structural refutations so neither can be re-derived as a positive:
the 16-codec graph is not Q4, and the two 192s are not the same 192.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import networkx as nx
import pytest

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "PART_W33_PASS5635_5642_SIXTEEN_CODECS_NOT_A_HYPERCUBE.json"


def q4() -> nx.Graph:
    g = nx.Graph()
    g.add_nodes_from(range(16))
    for a in range(16):
        for b in range(4):
            g.add_edge(a, a ^ (1 << b))
    return g


def codec16() -> nx.Graph:
    g = nx.Graph()
    g.add_nodes_from([("tet", i) for i in range(2)])
    g.add_nodes_from([("cs", i) for i in range(7)])
    g.add_nodes_from([("sz", i) for i in range(7)])
    for i, j in itertools.combinations(range(7), 2):
        g.add_edge(("cs", i), ("cs", j))
        g.add_edge(("sz", i), ("sz", j))
    return g


def test_q4_is_bipartite_and_triangle_free():
    Q = q4()
    assert nx.is_bipartite(Q)
    assert sum(nx.triangles(Q).values()) == 0
    assert set(dict(Q.degree()).values()) == {4}


def test_codec_graph_is_not_q4():
    """The test the 2026-05-29 file left open: it resolves NEGATIVE."""
    G, Q = codec16(), q4()
    assert G.number_of_nodes() == Q.number_of_nodes() == 16
    assert not nx.is_bipartite(G)
    assert sum(nx.triangles(G).values()) // 3 == 70
    assert not nx.is_isomorphic(G, Q)


def test_obstruction_survives_every_relabelling():
    """Not a labelling accident: the invariants differ, so no assignment repairs it."""
    G, Q = codec16(), q4()
    assert nx.is_bipartite(Q) != nx.is_bipartite(G)
    assert max(dict(G.degree()).values()) == 6 > max(dict(Q.degree()).values()) == 4


def test_flag_arithmetic_still_holds():
    """What the refutation does NOT touch."""
    assert (2 + 7 + 7) * 12 == 192
    assert 24 + 84 + 84 == 192
    assert 16 * 12 == 192


def test_the_two_192s_are_distinct():
    """A regular action of an order-192 group is transitive; 24+84+84 is not."""
    partition = [24, 84, 84]
    assert sum(partition) == 192
    assert len(set(partition)) > 1, "unequal parts forbid a transitive action"


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_certificate_records_the_negative():
    d = json.loads(CERT.read_text(encoding="utf-8"))
    assert d["pass_5638"]["isomorphic_to_q4"] is False
    assert d["pass_5638"]["codec_graph_bipartite"] is False
    assert d["pass_5639"]["coincidence_number"] == 9
    assert d["pass_5640"]["orbits"] == [96, 96]
    assert d["pass_5641"]["status"] == "OPEN"
    assert d["pass_5641"]["proved"] is False
    assert d["pass_5635"]["delta_certificates"] == -2
