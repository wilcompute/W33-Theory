"""Regression lock for Passes 5643-5650.

Locks the two 1152s apart and the bridge in place, so neither can be re-derived
from an order match.
"""

from __future__ import annotations

import collections
import itertools
import json
from pathlib import Path

import networkx as nx
import pytest

ROOT = Path(__file__).resolve().parents[1]
BT1413 = ROOT / "data" / "bt1413_q4_plaquette_tomotope_face_compiler.json"
CERT = ROOT / "data" / "PART_W33_PASS5643_5650_TOMOTOPE_W33_BRIDGE_IS_WF4_MOD_CENTRE.json"
FACE = "tomotope_face_label_from_q4_edge_pair"
EDGE = "tomotope_edge_label_from_q4_face_pair"


@pytest.fixture(scope="module")
def inc():
    if not BT1413.is_file():
        pytest.skip("bt1413 certificate absent")
    d = json.loads(BT1413.read_text(encoding="utf-8", errors="replace"))
    out = collections.defaultdict(set)
    for r in d["flag_rows"]:
        out[r[FACE]].add(r[EDGE])
    return out


def test_bt1413_carries_the_reye_configuration(inc):
    """16 faces of degree 3, 12 edges of degree 4 -- the 12_4 16_3 configuration."""
    rev = collections.defaultdict(set)
    for f, es in inc.items():
        for e in es:
            rev[e].add(f)
    assert len(inc) == 16
    assert len(rev) == 12
    assert {len(v) for v in inc.values()} == {3}
    assert {len(v) for v in rev.values()} == {4}


def test_the_sixteen_is_q4_edge_classes_not_vertices():
    """Q4 has 16 vertices AND 16 edge classes mod antipodal. Different 16s."""
    Q = nx.Graph()
    for a in range(16):
        for b in range(4):
            Q.add_edge(a, a ^ (1 << b))
    assert Q.number_of_nodes() == 16
    assert Q.number_of_edges() == 32
    ecls = {frozenset([frozenset(e), frozenset(x ^ 15 for x in e)]) for e in Q.edges()}
    assert len(ecls) == 16, "edge classes mod antipodal"
    fcls = set()
    for a in range(16):
        for i, j in itertools.combinations(range(4), 2):
            f = frozenset([a, a ^ (1 << i), a ^ (1 << j), a ^ (1 << i) ^ (1 << j)])
            fcls.add(frozenset([f, frozenset(x ^ 15 for x in f)]))
    assert len(fcls) == 12, "face classes mod antipodal"


def test_face_graph_is_the_rook_complement(inc):
    """Its Aut is S4 wr S2, order 1152 -- NOT W(F4). Coincidence ten."""
    faces = sorted(inc)
    G = nx.Graph()
    G.add_nodes_from(faces)
    for a, b in itertools.combinations(faces, 2):
        if inc[a] & inc[b]:
            G.add_edge(a, b)
    assert set(dict(G.degree()).values()) == {9}
    comp = nx.complement(G)
    assert set(dict(comp.degree()).values()) == {6}
    rook = nx.Graph()
    cells = list(itertools.product(range(4), repeat=2))
    for x, y in itertools.combinations(cells, 2):
        if x[0] == y[0] or x[1] == y[1]:
            rook.add_edge(x, y)
    assert nx.is_isomorphic(comp, rook), "complement is the 4x4 rook's graph"


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_certificate_separates_the_two_1152s():
    d = json.loads(CERT.read_text(encoding="utf-8"))
    p = d["pass_5644"]
    assert p["face_graph_aut"] == 1152
    assert p["face_aut_iso_wf4"] is False, "the decoy must stay killed"
    assert p["face_aut_iso_s4wrs2"] is True
    assert p["wf4_iso_s4wrs2"] is False, "1152 has two non-isomorphic realizations"
    assert p["coincidence_number"] == 10


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_certificate_records_the_bridge():
    d = json.loads(CERT.read_text(encoding="utf-8"))
    p = d["pass_5645"]
    assert p["levi_aut"] == 576
    assert p["wf4_mod_centre"] == 576
    assert p["levi_iso_wf4_mod_centre"] is True, "the bridge is by isomorphism"
    assert p["levi_structure"] == p["wf4_mod_centre_structure"] == "((A4 x A4) : C2) : C2"


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_open_questions_stay_open():
    d = json.loads(CERT.read_text(encoding="utf-8"))
    assert d["pass_5647"]["status"] == "OPEN", "168 is neither killed nor established"
    assert d["pass_5650"]["status"] == "OPEN"
    assert d["pass_5650"]["proved"] is False
    assert d["pass_5650"]["dual_bound"] < d["pass_5650"]["hoffman"], "bound beats Hoffman"
