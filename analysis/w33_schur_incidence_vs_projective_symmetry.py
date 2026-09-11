#!/usr/bin/env python3
"""Separate bare Schur (24_4,32_3) incidence symmetry from projective half symmetry.

Using the D4-root incidence model from arXiv:2607.10090, build the 56-vertex
Levi graph (24 roots, 32 zero-sum triples).  Exact graph-isomorphism enumeration
shows that its abstract combinatorial automorphism group has order 1152.  Its
induced action on the 24 roots is exactly the full W(F4) root action.

External geometric input from Hohn: the projective stabilizer of one Schur
24-line half is only W(D4):C3 of order 576.  Thus forgetting the K3/projective
embedding restores an extra C2 of abstract incidence symmetry.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_schur_quartic_d4_triality_bridge import (  # noqa: E402
    f4_roots, schur_incidence, restrict_perm,
)
from w33_threeway_576_provenance_closure import wf4_and_kernels  # noqa: E402

OUT = ROOT / "data" / "w33_schur_incidence_vs_projective_symmetry.json"


def build_result():
    roots = f4_roots()
    d4, triples = schur_incidence(roots)
    ridx = {r: i for i, r in enumerate(d4)}

    G = nx.Graph()
    rnodes = [("r", i) for i in range(24)]
    tnodes = [("t", j) for j in range(32)]
    G.add_nodes_from(rnodes)
    G.add_nodes_from(tnodes)
    for j, T in enumerate(triples):
        for r in T:
            G.add_edge(("r", ridx[r]), ("t", j))

    gm = nx.algorithms.isomorphism.GraphMatcher(G, G)
    root_perms = set()
    count = 0
    for iso in gm.isomorphisms_iter():
        count += 1
        p = tuple(iso[("r", i)][1] for i in range(24))
        root_perms.add(p)
    assert count == 1152 and len(root_perms) == 1152

    WF4, _long, _short, _rot, _auto = wf4_and_kernels()
    wf4_root_action = {restrict_perm(roots, d4, p) for p in WF4}
    assert len(wf4_root_action) == 1152
    assert root_perms == wf4_root_action

    checks = {
        "Levi_vertices_56": G.number_of_nodes() == 56,
        "Levi_edges_96": G.number_of_edges() == 96,
        "abstract_incidence_automorphisms_1152": count == 1152,
        "root_action_faithful_1152": len(root_perms) == 1152,
        "abstract_root_action_equals_WF4": root_perms == wf4_root_action,
        "projective_half_stabilizer_external_order_576": True,
        "incidence_to_projective_index_is_2": count // 576 == 2,
    }

    return {
        "schema": "w33.schur-incidence-vs-projective-symmetry.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "bare_incidence": {
            "configuration": "(24_4,32_3)",
            "Levi_vertices": 56,
            "Levi_edges": 96,
            "automorphism_order": count,
            "root_action": "exactly W(F4) on the 24 D4 roots",
        },
        "Schur_geometric_half": {
            "projective_stabilizer_order": 576,
            "structure": "W(D4):C3",
            "source": "Gerald Hohn, arXiv:2607.10090",
        },
        "information_reading": (
            "The isolated incidence observer forgets projective/K3 embedding data and consequently admits twice as many symmetries as the stabilizer of the realized 24-line half. This is symmetry gained by coarse-graining, not evidence that every abstract incidence automorphism is induced by a projective automorphism preserving that half."
        ),
        "theorem": (
            "The bare D4-root (24_4,32_3) Levi graph has full automorphism group W(F4) of order 1152, while the Schur-quartic realization of a chosen half has projective stabilizer W(D4):C3 of order 576."
        ),
        "checks": checks,
    }


def main():
    r = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": r["status"], "incidence_aut": r["bare_incidence"]["automorphism_order"], "projective_half": r["Schur_geometric_half"]["projective_stabilizer_order"]}, sort_keys=True))
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
