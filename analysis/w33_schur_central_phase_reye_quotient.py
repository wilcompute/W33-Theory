#!/usr/bin/env python3
"""Central-phase quotient of the Schur extraspecial coset geometry is dual Reye.

The Schur (24_4,32_3) configuration was independently reconstructed in the
companion certificates as

    points = E = 2_+^{1+4},
    lines  = left cosets of three V4 subgroups V1,V2,V3 < E,

where the V_i project to one ruling of Q^+(3,2) in E/Z(E).

This verifier quotients the 32-point E-torsor by the central phase
Z(E)=<z> of order two.  Because each V_i avoids z, every Schur line gV_i and
its central translate zgV_i project to the same 4-point affine plane.  Hence
32 points -> 16 central-phase classes and 24 lines -> 12 line classes.

The resulting quotient has type 16_3,12_4, i.e. the *incidence dual* of the
project-native Reye models, which are stored as 12_4,16_3.  Since Reye is
self-dual this is the same abstract configuration, but the typed orientation
matters and is checked explicitly here rather than erased by an untyped graph
isomorphism.

Prior-art boundary: Nurowski, arXiv:2609.10751 (2026-09-09), independently
identifies the antipodal quotient of the Naskrecki--Pokora Schur configuration
with the classical Reye configuration.  This script is a project-internal
extraspecial-group reconstruction and cross-check, not a priority claim.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
import sys

import networkx as nx
from networkx.algorithms import isomorphism as iso

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_schur_quartic_d4_triality_bridge import (  # noqa: E402
    f4_roots, schur_incidence, restrict_perm, wd4_group,
)
from w33_threeway_576_provenance_closure import (  # noqa: E402
    center, compose, derived_subgroup, wf4_and_kernels,
)
from analysis.w33_q4_tomotope_reye_double_cover import reye_configuration_graph  # noqa: E402
from analysis.w33_reye_tomotope_24cell_common_spine import twenty_four_cell_reye_graph  # noqa: E402

OUT = ROOT / "data" / "w33_schur_central_phase_reye_quotient.json"


def typed_dual(graph: nx.Graph) -> nx.Graph:
    """Swap point/line incidence types while preserving the underlying graph."""
    out = graph.copy()
    for node, attrs in out.nodes(data=True):
        kind = attrs.get("kind")
        if kind == "point":
            attrs["kind"] = "line"
        elif kind == "line":
            attrs["kind"] = "point"
    return out


def build_result():
    roots = f4_roots()
    d4, triples = schur_incidence(roots)
    ridx = {r: i for i, r in enumerate(d4)}
    tsets = tuple(frozenset(ridx[r] for r in T) for T in triples)
    tidx = {T: i for i, T in enumerate(tsets)}

    _wf4, longk, shortk, rotk, _auto = wf4_and_kernels()
    WD4 = wd4_group(roots)
    kernels = [K for K in (longk, shortk, rotk) if WD4 <= K]
    assert len(kernels) == 1
    H = kernels[0]
    E = derived_subgroup(derived_subgroup(H, 48), 48)
    assert len(H) == 576 and len(E) == 32
    Z = tuple(center(E))
    assert len(Z) == 2
    identity = tuple(range(48))
    z = next(g for g in Z if g != identity)

    def root_perm(g):
        return restrict_perm(roots, d4, g)

    def triple_perm(g):
        rp = root_perm(g)
        return tuple(tidx[frozenset(rp[i] for i in T)] for T in tsets)

    # Identify the 32 triple points with E by the regular action on triple 0.
    point_to_elem = {}
    for g in E:
        j = triple_perm(g)[0]
        assert j not in point_to_elem
        point_to_elem[j] = g
    assert len(point_to_elem) == 32

    # Original Schur lines: four triple points on each D4 root.
    line_points = tuple(
        frozenset(j for j, T in enumerate(triples) if r in T)
        for r in d4
    )
    assert len(line_points) == 24 and {len(S) for S in line_points} == {4}

    # Quotient E by the center. Each quotient point is a two-element phase pair.
    cosets = []
    coset_of = {}
    for g in E:
        if g in coset_of:
            continue
        C = frozenset((g, compose(z, g)))
        k = len(cosets)
        cosets.append(C)
        for h in C:
            coset_of[h] = k
    assert len(cosets) == 16

    triple_to_qpoint = {j: coset_of[g] for j, g in point_to_elem.items()}
    assert len(set(triple_to_qpoint.values())) == 16
    qpoint_fibres = Counter(triple_to_qpoint.values())
    assert set(qpoint_fibres.values()) == {2}

    # Every 4-point Schur line projects injectively to four quotient points;
    # central-translate line pairs project to the same block.
    projected = []
    for S in line_points:
        B = frozenset(triple_to_qpoint[j] for j in S)
        assert len(B) == 4
        projected.append(B)
    block_mult = Counter(projected)
    assert len(block_mult) == 12
    assert set(block_mult.values()) == {2}
    blocks = tuple(sorted(block_mult, key=lambda B: tuple(sorted(B))))

    # Build the quotient Levi graph: 16 points of degree 3, 12 blocks of degree 4.
    G = nx.Graph()
    for p in range(16):
        G.add_node(("P", p), kind="point")
    for i, B in enumerate(blocks):
        G.add_node(("B", i), kind="line")
        for p in B:
            G.add_edge(("P", p), ("B", i))
    degree_profile = dict(sorted(Counter(dict(G.degree()).values()).items()))
    assert G.number_of_nodes() == 28
    assert G.number_of_edges() == 48
    assert degree_profile == {3: 16, 4: 12}
    assert nx.is_connected(G)

    # Project-native Reye models are typed 12 points of degree 4 + 16 lines of
    # degree 3. Our quotient is the dual typing 16 points + 12 lines. Compare
    # against the typed dual explicitly, and also record that the same-typing
    # comparison fails for the expected degree reason.
    node_match = iso.categorical_node_match("kind", None)
    q4_reye = reye_configuration_graph()["graph"]
    cell24_reye = twenty_four_cell_reye_graph()["graph"]
    q4_same_typed = nx.is_isomorphic(G, q4_reye, node_match=node_match)
    cell24_same_typed = nx.is_isomorphic(G, cell24_reye, node_match=node_match)
    q4_dual_iso = nx.is_isomorphic(G, typed_dual(q4_reye), node_match=node_match)
    cell24_dual_iso = nx.is_isomorphic(G, typed_dual(cell24_reye), node_match=node_match)
    assert not q4_same_typed and not cell24_same_typed
    assert q4_dual_iso and cell24_dual_iso

    # The central action pairs the original 24 lines exactly 2-to-1.
    zt = triple_perm(z)
    line_index = {S: i for i, S in enumerate(line_points)}
    z_line_perm = []
    for S in line_points:
        image = frozenset(zt[j] for j in S)
        assert image in line_index
        z_line_perm.append(line_index[image])
    assert all(z_line_perm[z_line_perm[i]] == i for i in range(24))
    assert all(z_line_perm[i] != i for i in range(24))
    assert len({frozenset((i, z_line_perm[i])) for i in range(24)}) == 12
    assert all(projected[i] == projected[z_line_perm[i]] for i in range(24))

    checks = {
        "extraspecial_center_order2": len(Z) == 2,
        "32_triples_quotient_to_16_phase_classes": len(cosets) == 16 and set(qpoint_fibres.values()) == {2},
        "24_lines_pair_to_12_blocks": len(blocks) == 12 and set(block_mult.values()) == {2},
        "central_element_pairs_lines_fixed_point_freely": all(z_line_perm[i] != i for i in range(24)),
        "quotient_is_16_3_12_4": degree_profile == {3: 16, 4: 12} and G.number_of_edges() == 48,
        "same_typed_orientation_is_not_project_Reye": not q4_same_typed and not cell24_same_typed,
        "quotient_is_typed_dual_of_Q4_tomotope_Reye": q4_dual_iso,
        "quotient_is_typed_dual_of_24cell_Reye": cell24_dual_iso,
    }

    return {
        "schema": "w33.schur-central-phase-reye-quotient.v2",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "upstairs": {
            "configuration": "Schur (24_4,32_3)",
            "point_model": "E = 2_+^{1+4} torsor",
            "triple_points": 32,
            "lines": 24,
        },
        "central_phase": {
            "center_order": len(Z),
            "point_fibre_size": 2,
            "line_fibre_size": 2,
            "hidden_bits_per_point_fibre": 1,
        },
        "downstairs": {
            "points": 16,
            "blocks": 12,
            "incidences": 48,
            "degree_profile": degree_profile,
            "configuration": "dual Reye 16_3,12_4",
            "typed_orientation": "incidence dual of project-native Reye 12_4,16_3",
            "same_typed_Q4_Reye": q4_same_typed,
            "same_typed_24cell_Reye": cell24_same_typed,
            "typed_dual_Q4_tomotope_Reye": q4_dual_iso,
            "typed_dual_24cell_Reye": cell24_dual_iso,
        },
        "theorem": (
            "Quotienting the Schur extraspecial coset geometry by the central phase Z(E) pairs its 32 triple points and 24 lines 2-to-1 and yields the typed incidence dual of the project-native Reye configuration."
        ),
        "prior_art_boundary": (
            "Nurowski, arXiv:2609.10751 (2026-09-09), independently proves that the antipodal quotient of the Schur 24-line configuration is Reye. This certificate supplies the project-internal extraspecial-group/coset derivation and explicit dual-typed isomorphisms to the pre-existing Q4/tomotope and 24-cell Reye models."
        ),
        "checks": checks,
    }


def main():
    r = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": r["status"],
        "upstairs": [r["upstairs"]["triple_points"], r["upstairs"]["lines"]],
        "downstairs": [r["downstairs"]["points"], r["downstairs"]["blocks"]],
        "hidden_bits": r["central_phase"]["hidden_bits_per_point_fibre"],
        "orientation": r["downstairs"]["typed_orientation"],
    }, sort_keys=True))
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
