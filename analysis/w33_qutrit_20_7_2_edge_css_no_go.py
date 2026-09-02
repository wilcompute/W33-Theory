#!/usr/bin/env python3
"""Exact no-go certificate for a literal [[20,7,2]]_3 -> W33 edge-CSS embedding.

The canonical W33 edge code has physical qutrits on 240 graph edges and
HX=d1 (vertex-edge incidence), HZ=d2^T.  This is the first repository carrier
whose coordinates are type-compatible with the external code's 20 physical
qutrit coordinates.

We test the strongest literal adapter class:
  * choose 20 distinct parent edge coordinates;
  * permute them and multiply coordinates by nonzero GF(3) scalars;
  * extend external stabilizers by zero outside those coordinates;
  * preserve CSS type, so external X stabilizers land in row(HX).

No selector enumeration is required. Every nonzero word y^T d1 has support on
exactly the W33 graph edges whose endpoint potentials y differ. Therefore its
weight is at least the graph edge-connectivity lambda(G). Stoer-Wagner computes
lambda(W33)=12, and a one-vertex potential attains weight 12. The external H0
stabilizer span contains a nonzero weight-6 word. Monomial coordinate maps
preserve Hamming support weight, so that word cannot land in row(HX).

Result: the entire literal CSS-preserving zero-extension/monomial search is
UNSAT. More general symplectic Clifford intertwiners that mix X/Z sectors or
encode a physical qutrit nonlocally are NOT ruled out.
"""
from __future__ import annotations

from itertools import product
import json
from pathlib import Path
from typing import Any

from w33_levi_next5_v5_common import build_w33

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = ROOT / "data" / "w33_qutrit_20_7_2_external_code.json"


def weight(v: list[int]) -> int:
    return sum((x % 3) != 0 for x in v)


def add_scaled(a: list[int], b: list[int], scale: int) -> list[int]:
    return [(x + scale * y) % 3 for x, y in zip(a, b)]


def external_h0_weight_spectrum() -> dict[str, Any]:
    payload = json.loads(EXTERNAL.read_text(encoding="utf-8"))
    h0 = payload["H0_x_stabilizer_rows"]
    words = []
    for a, b in product(range(3), repeat=2):
        if a == 0 and b == 0:
            continue
        v = [0] * len(h0[0])
        v = add_scaled(v, h0[0], a)
        v = add_scaled(v, h0[1], b)
        words.append({"coefficients": [a, b], "weight": weight(v), "word": v})
    words.sort(key=lambda row: (row["weight"], row["coefficients"]))
    return {
        "minimum_nonzero_weight": words[0]["weight"],
        "minimum_witness": words[0],
        "spectrum": sorted(row["weight"] for row in words),
        "words": words,
    }


def stoer_wagner_min_cut(adjacency: list[list[int]]) -> tuple[int, list[int]]:
    """Global min cut for a nonnegative undirected integer-weight graph."""
    n = len(adjacency)
    w = [row[:] for row in adjacency]
    vertices = list(range(n))
    groups = {i: [i] for i in range(n)}
    best = 10**18
    best_side: list[int] = []

    while len(vertices) > 1:
        used: set[int] = set()
        score = {v: 0 for v in vertices}
        previous = None
        for phase_index in range(len(vertices)):
            sel = max((v for v in vertices if v not in used), key=lambda v: (score[v], -v))
            if phase_index == len(vertices) - 1:
                cut = score[sel]
                if cut < best:
                    best = cut
                    best_side = list(groups[sel])
                if previous is None:
                    raise RuntimeError("invalid Stoer-Wagner phase")
                for v in vertices:
                    if v in (previous, sel):
                        continue
                    w[previous][v] += w[sel][v]
                    w[v][previous] = w[previous][v]
                groups[previous].extend(groups[sel])
                vertices.remove(sel)
                break
            used.add(sel)
            previous = sel
            for v in vertices:
                if v not in used:
                    score[v] += w[sel][v]
    return int(best), sorted(best_side)


def parent_x_minimum_weight() -> dict[str, Any]:
    w33 = build_w33()
    adjacency = [[int(x) for x in row] for row in w33.adjacency.tolist()]
    cut, side = stoer_wagner_min_cut(adjacency)
    degrees = [sum(row) for row in adjacency]
    one_vertex_weight = min(degrees)
    # For any nonconstant GF(3) vertex potential, choose one nonempty proper
    # value class. Its boundary is a subset of the nonzero gradient support, so
    # every nonzero coboundary has weight >= lambda(G). A one-vertex indicator
    # is a coboundary of weight degree=12, establishing equality here.
    return {
        "edge_connectivity": cut,
        "minimum_cut_side": side,
        "degree_distribution": sorted(degrees),
        "one_vertex_potential_weight": one_vertex_weight,
        "minimum_nonzero_row_HX_weight": cut if cut == one_vertex_weight else None,
        "edge_count": int(w33.adjacency.sum() // 2),
    }


def smt_problem_summary() -> dict[str, Any]:
    return {
        "candidate_class": "20 distinct W33 edge coordinates with permutation and nonzero GF(3) coordinate scalings; zero extension; CSS X->X",
        "selector_variables": "x[j,e] in {0,1}, 20x240, one edge per external coordinate and at most one coordinate per edge",
        "scaling_variables": "s[j] in {1,2}",
        "stabilizer_membership": "for every h in span(H0), zero_extend(s*h) must lie in row(HX=d1)",
        "solver_status": "SHORT-CIRCUITED_UNSAT_BY_WEIGHT_CERTIFICATE",
        "reason": "span(H0) contains weight 6, while every nonzero row(HX) word has weight >= 12",
    }


def verify() -> dict[str, Any]:
    ext = external_h0_weight_spectrum()
    parent = parent_x_minimum_weight()
    parent_min = parent["minimum_nonzero_row_HX_weight"]
    checks = {
        "canonical_parent_has_240_edge_coordinates": parent["edge_count"] == 240,
        "w33_is_12_regular": parent["degree_distribution"] == [12] * 40,
        "stoer_wagner_edge_connectivity_is_12": parent["edge_connectivity"] == 12,
        "one_vertex_potential_attains_weight_12": parent["one_vertex_potential_weight"] == 12,
        "parent_x_stabilizer_minimum_weight_is_12": parent_min == 12,
        "external_x_stabilizer_span_contains_weight_6": ext["minimum_nonzero_weight"] == 6,
        "literal_css_monomial_embedding_is_impossible": parent_min is not None and ext["minimum_nonzero_weight"] < parent_min,
    }
    return {
        "schema": "w33.qutrit-20-7-2-edge-css-no-go.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "decision": "UNSAT_LITERAL_CSS_MONOMIAL_20_TO_240",
        "external_H0": ext,
        "parent_W33_edge_CSS": parent,
        "smt_search": smt_problem_summary(),
        "checks": checks,
        "interpretation": "The type-correct W33 physical-qutrit carrier is the 240-edge CSS code, but its X-stabilizer rowspace has minimum nonzero weight 12. The external [[20,7,2]]_3 X-stabilizer space contains weight 6. Hence no 20-edge selector, permutation, GF(3) coordinate rescaling and zero-extension can produce a CSS-preserving X->X intertwiner.",
        "open_class": "General symplectic/Clifford intertwiners that mix X and Z, use ancillas, or encode external physical coordinates nonlocally are not excluded by this certificate.",
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
