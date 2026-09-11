#!/usr/bin/env python3
"""Presymplectic three-qubit-Pauli normal form of the E8-selected D4/Reye sector.

Pass8909-8916 proves that the explicit ternary E8 residue selects a complementary
D4 inside E7, with 12 antipodal roots and 16 zero-sum A2 blocks forming a
(12_4,16_3) Reye/Klein-Latin configuration.  The Schur64/E7 Pauli bridge fixes
a standard three-qubit coordinate gauge (x1,z1,x2,z2,x3,z3).

In that gauge this certificate proves the selected 12 D4 root pairs are exactly

    {X,Y,Z}_1 x {I,Z}_2 x {I,X}_3,

or equivalently W \ Rad(W), where

    W = <X1,Z1,Z2,X3>  <= F2^6,
    Rad(W) = <Z2,X3>.

Thus the 12 points are the three nonzero cosets of the four-element radical.
Same-coset pairs commute and different-coset pairs anticommute, so the
anticommutation graph is K4,4,4.  Its 16 closed anticommuting XOR triangles are
exactly a (12_4,16_3) incidence geometry and are typed-isomorphic to the repo's
Q4/tomotope and 24-cell Reye models.

This supplies a Pauli-coordinate explanation of the old D4/Reye selector; it
does not claim that the four-dimensional span is a nondegenerate two-qubit
Pauli space.  In fact its restricted symplectic rank is exactly two.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys

import networkx as nx
from networkx.algorithms import isomorphism as iso
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_schur64_e7_threequbit_pauli_objectwise_bridge import (  # noqa: E402
    JSTD, build_result as build_pauli_bridge, omega, pauli_word, root_pair_key,
)
from analysis.w33_q4_tomotope_reye_double_cover import reye_configuration_graph  # noqa: E402
from analysis.w33_reye_tomotope_24cell_common_spine import twenty_four_cell_reye_graph  # noqa: E402

OUT = ROOT / "data" / "w33_e7_d4_presymplectic_reye_normal_form.json"
ZERO = (0,0,0,0,0,0)


def vxor(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def span(vectors):
    out = {ZERO}
    for v in vectors:
        out |= {vxor(x, v) for x in tuple(out)}
    return out


def complementary_d4_pairs():
    roots = set()
    for i, j in combinations(range(4), 2):
        for a in (2, -2):
            for b in (2, -2):
                v = [0] * 8
                v[4+i] = a
                v[4+j] = b
                roots.add(tuple(v))
    assert len(roots) == 24
    pairs = {root_pair_key(r) for r in roots}
    assert len(pairs) == 12
    return pairs


def build_result():
    bridge = build_pauli_bridge()
    assert bridge["status"] == "PASS"
    root_to_bits = {
        tuple(row["e7_antipodal_root_pair_representative"]):
        tuple(row["standard_bits_x1z1x2z2x3z3"])
        for row in bridge["dictionary"]
    }
    d4pairs = complementary_d4_pairs()
    assert d4pairs <= set(root_to_bits)
    selected = {root_to_bits[r] for r in d4pairs}
    assert len(selected) == 12

    W = span(selected)
    assert len(W) == 16
    radical = {
        v for v in W
        if all(omega(v, w, JSTD) == 0 for w in W)
    }
    assert len(radical) == 4
    assert selected == W - radical

    # Exact standard-gauge Pauli description.
    selected_words = {pauli_word(v) for v in selected}
    expected_words = {
        a+b+c
        for a in ("X", "Y", "Z")
        for b in ("I", "Z")
        for c in ("I", "X")
    }
    assert selected_words == expected_words
    radical_words = {pauli_word(v) for v in radical}
    assert radical_words == {"III", "IZI", "IIX", "IZX"}

    # Restricted symplectic rank = 2, radical dimension = 2.
    basis_rows = np.array(sorted(W), dtype=np.uint8)
    gram = (basis_rows @ JSTD @ basis_rows.T) % 2
    def rank2(A):
        A = np.array(A, dtype=np.uint8) % 2
        m, n = A.shape; r = 0
        for c in range(n):
            p = next((i for i in range(r, m) if A[i,c]), None)
            if p is None:
                continue
            A[[r,p]] = A[[p,r]]
            for i in range(m):
                if i != r and A[i,c]:
                    A[i] ^= A[r]
            r += 1
        return r
    restricted_rank = rank2(gram)
    assert restricted_rank == 2

    # The three nonzero radical cosets partition the selected 12 states.
    cosets = set()
    for v in selected:
        cosets.add(frozenset(vxor(v, r) for r in radical))
    assert len(cosets) == 3 and {len(C) for C in cosets} == {4}
    cosets = tuple(sorted(cosets, key=lambda C: sorted(C)))
    assert set().union(*map(set, cosets)) == selected
    assert all(set(cosets[i]).isdisjoint(cosets[j]) for i in range(3) for j in range(i+1,3))

    # Same coset = commute; distinct nonzero cosets = anticommute.
    for i, C in enumerate(cosets):
        assert all(omega(a,b,JSTD) == 0 for a,b in combinations(sorted(C),2))
        for j in range(i+1,3):
            assert all(omega(a,b,JSTD) == 1 for a in C for b in cosets[j])

    # Closed anticommuting XOR triangles.
    triangles = set()
    for a, b in combinations(sorted(selected), 2):
        if omega(a,b,JSTD) != 1:
            continue
        c = vxor(a,b)
        assert c in selected
        triangles.add(frozenset((a,b,c)))
    assert len(triangles) == 16
    multiplicity = Counter(v for T in triangles for v in T)
    assert set(multiplicity.values()) == {4}

    # Build typed Reye incidence graph: 12 point states, 16 triple blocks.
    points = tuple(sorted(selected))
    pi = {p:i for i,p in enumerate(points)}
    blocks = tuple(sorted((frozenset(pi[v] for v in T) for T in triangles), key=lambda B: tuple(sorted(B))))
    G = nx.Graph()
    for i in range(12):
        G.add_node(("P",i), kind="point")
    for j,B in enumerate(blocks):
        G.add_node(("L",j), kind="line")
        for i in B:
            G.add_edge(("P",i),("L",j))
    assert G.number_of_edges() == 48
    assert dict(sorted(Counter(dict(G.degree()).values()).items())) == {3:16,4:12}

    node_match = iso.categorical_node_match("kind", None)
    q4 = reye_configuration_graph()["graph"]
    cell24 = twenty_four_cell_reye_graph()["graph"]
    q4_iso = nx.is_isomorphic(G, q4, node_match=node_match)
    cell24_iso = nx.is_isomorphic(G, cell24, node_match=node_match)
    assert q4_iso and cell24_iso

    # K4,4,4 anticommutation graph on the 12 selected states.
    Agraph = nx.Graph()
    Agraph.add_nodes_from(range(12))
    for i,j in combinations(range(12),2):
        if omega(points[i], points[j], JSTD):
            Agraph.add_edge(i,j)
    assert Agraph.number_of_edges() == 48
    assert set(dict(Agraph.degree()).values()) == {8}
    assert nx.is_isomorphic(Agraph, nx.complete_multipartite_graph(4,4,4))

    checks = {
        "selected_D4_root_pairs_are_12": len(selected) == 12,
        "span_is_4dim_16element_flat": len(W) == 16,
        "restricted_symplectic_rank_is_2": restricted_rank == 2,
        "radical_is_2dim_4element": len(radical) == 4,
        "selected_set_is_exactly_span_minus_radical": selected == W-radical,
        "standard_Pauli_product_description_exact": selected_words == expected_words,
        "radical_words_are_III_IZI_IIX_IZX": radical_words == {"III","IZI","IIX","IZX"},
        "three_nonzero_radical_cosets_have_size4": len(cosets) == 3 and {len(C) for C in cosets} == {4},
        "anticommutation_graph_is_K444": nx.is_isomorphic(Agraph, nx.complete_multipartite_graph(4,4,4)),
        "closed_anticommuting_XOR_triangles_are_16": len(triangles) == 16,
        "each_selected_point_lies_on_4_triangles": set(multiplicity.values()) == {4},
        "Pauli_triangle_incidence_is_Q4_tomotope_Reye": q4_iso,
        "Pauli_triangle_incidence_is_24cell_Reye": cell24_iso,
    }

    return {
        "schema": "w33.e7-d4-presymplectic-reye-normal-form.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "standard_coordinate_order": ["x1","z1","x2","z2","x3","z3"],
        "normal_form": {
            "span_generators": ["X1","Z1","Z2","X3"],
            "span_order": 16,
            "span_dimension": 4,
            "restricted_symplectic_rank": restricted_rank,
            "radical_generators": ["Z2","X3"],
            "radical_order": 4,
            "radical_words": sorted(radical_words),
            "selected_words": sorted(selected_words),
            "formula": "selected = W \\ Rad(W) = {X,Y,Z}_1 x {I,Z}_2 x {I,X}_3",
        },
        "coset_geometry": {
            "nonzero_radical_cosets": [[pauli_word(v) for v in sorted(C)] for C in cosets],
            "commutation_inside_each_coset": "all commute",
            "commutation_between_distinct_cosets": "all anticommute",
            "anticommutation_graph": "K4,4,4",
        },
        "Reye": {
            "points": 12,
            "blocks": 16,
            "incidences": 48,
            "block_rule": "closed anticommuting XOR triple {a,b,a+b}",
            "point_multiplicity": 4,
            "typed_Q4_tomotope_isomorphism": q4_iso,
            "typed_24cell_isomorphism": cell24_iso,
        },
        "theorem": (
            "The E8-selected complementary D4 of Pass8909 has the standard three-qubit-Pauli normal form W\\Rad(W), where W=<X1,Z1,Z2,X3> has two-dimensional radical <Z2,X3>. The three nonzero radical cosets give K4,4,4 and the 16 closed anticommuting XOR triangles are exactly the Reye incidence blocks."
        ),
        "prior_repo_boundary": (
            "Pass8909-8916 already proved the selected complementary D4, the 12_4,16_3 Reye-type incidence, K4,4,4 point graph, and Klein-V4 Latin isotopy. New here is the explicit presymplectic three-qubit-Pauli normal form and the radical-coset/XOR-triangle derivation."
        ),
        "checks": checks,
    }


def main():
    r = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": r["status"],
        "span": r["normal_form"]["span_order"],
        "radical": r["normal_form"]["radical_order"],
        "selected": r["Reye"]["points"],
        "triangles": r["Reye"]["blocks"],
    }, sort_keys=True))
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
