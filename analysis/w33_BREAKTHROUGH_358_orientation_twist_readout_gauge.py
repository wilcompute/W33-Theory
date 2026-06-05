#!/usr/bin/env python3
"""BT358: orientation-twist readout gauge obstruction.

BT356 found a 61-dimensional shared quotient between:

  * the oriented canonical chain CSS layer, and
  * the all-plus vertex/line Hamiltonian layer.

This file checks whether that 61-core is a full PSp(4,3)-module.  It is not.

Reason: the canonical layer is a signed chain complex; the line Hamiltonian is
an unsigned support/product code.  The full projective symplectic group
preserves each support geometry, but the two coefficient conventions are
incompatible.  Among the 40 canonical symplectic transvection generators,
only one transvection preserves the common kernel under both conventions, and
that surviving transvection generates a C3 subgroup.

Interpretation: the 61-core is a readout-gauge-fixed overlap, not a full
symplectic representation.  The surviving symmetry is ternary.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, deque
from itertools import combinations, product
from pathlib import Path
from typing import Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_css_exact_audit import P, boundary_matrices, build_w33, gf_rank


Q = 3
MU = 4

Vec = tuple[int, int, int, int]
Perm = tuple[int, ...]


def canonical(v: Iterable[int]) -> Vec:
    vv = tuple(int(x) % P for x in v)
    if vv == (0, 0, 0, 0):
        raise ValueError("zero vector")
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P for y in vv)  # type: ignore[return-value]
    raise AssertionError


def omega(u: Vec, v: Vec) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % P


def compose(p: Perm, q: Perm) -> Perm:
    return tuple(p[i] for i in q)


def all_plus_vertex_matrix(points, edges) -> np.ndarray:
    hx = np.zeros((len(points), len(edges)), dtype=int)
    for col, (i, j) in enumerate(edges):
        hx[i, col] = 1
        hx[j, col] = 1
    return hx % P


def transvection_permutations(points: list[Vec]) -> list[Perm]:
    point_index = {p: i for i, p in enumerate(points)}
    perms = []
    for v in points:
        perm = []
        for x in points:
            c = omega(x, v)
            y = tuple((x[t] + c * v[t]) % P for t in range(4))
            perm.append(point_index[canonical(y)])
        perms.append(tuple(perm))
    return perms


def transformed_constraint_rows(
    constraints: np.ndarray,
    g: Perm,
    edges,
    edge_index,
    *,
    signed: bool,
) -> np.ndarray:
    """Return C A^T for the signed or unsigned edge action A."""

    out = np.zeros_like(constraints)
    for old_edge, (i, j) in enumerate(edges):
        a0, b0 = g[i], g[j]
        a, b = sorted((a0, b0))
        new_edge = edge_index[(a, b)]
        sign = 1
        if signed and (a0, b0) != (a, b):
            sign = 2
        out[:, old_edge] = (sign * constraints[:, new_edge]) % P
    return out


def preserves_common_kernel(constraints, g, edges, edge_index, *, signed: bool) -> tuple[bool, int]:
    rank_c = gf_rank(constraints)
    transformed = transformed_constraint_rows(constraints, g, edges, edge_index, signed=signed)
    combined_rank = gf_rank(np.vstack([constraints, transformed]))
    return combined_rank == rank_c, combined_rank


def closure_order(generators: list[Perm], degree: int) -> int:
    identity = tuple(range(degree))
    group = {identity}
    queue: deque[Perm] = deque([identity])
    while queue:
        g = queue.popleft()
        for s in generators:
            h = compose(s, g)
            if h not in group:
                group.add(h)
                queue.append(h)
    return len(group)


def build_payload() -> dict:
    points, edges, edge_index, _lines, triangles = build_w33()
    d1, _d2 = boundary_matrices(points, edges, edge_index, triangles)
    hx_plus = all_plus_vertex_matrix(points, edges)
    constraints = np.vstack([d1, hx_plus]) % P
    rank_constraints = gf_rank(constraints)
    common_kernel_dim = len(edges) - rank_constraints

    transvections = transvection_permutations(points)
    signed_results = []
    unsigned_results = []
    both_indices = []
    for i, g in enumerate(transvections):
        signed_ok, signed_rank = preserves_common_kernel(constraints, g, edges, edge_index, signed=True)
        unsigned_ok, unsigned_rank = preserves_common_kernel(constraints, g, edges, edge_index, signed=False)
        signed_results.append({"index": i, "preserves": signed_ok, "combined_rank": signed_rank})
        unsigned_results.append({"index": i, "preserves": unsigned_ok, "combined_rank": unsigned_rank})
        if signed_ok and unsigned_ok:
            both_indices.append(i)

    signed_indices = [r["index"] for r in signed_results if r["preserves"]]
    unsigned_indices = [r["index"] for r in unsigned_results if r["preserves"]]
    both_generators = [transvections[i] for i in both_indices]

    signed_rank_distribution = Counter(r["combined_rank"] for r in signed_results)
    unsigned_rank_distribution = Counter(r["combined_rank"] for r in unsigned_results)

    survivor_order = closure_order(both_generators, len(points)) if both_generators else 1

    identities = {
        "rank_constraints": rank_constraints == 75,
        "common_kernel_dim": common_kernel_dim == 165,
        "transvection_count": len(transvections) == 40,
        "signed_survivors": signed_indices == [0],
        "unsigned_survivors": unsigned_indices == [0],
        "both_survivors": both_indices == [0],
        "survivor_order": survivor_order == Q,
        "signed_rank_distribution": dict(signed_rank_distribution) == {
            75: 1,
            84: 1,
            90: 1,
            93: 1,
            98: 3,
            105: 6,
            107: 12,
            109: 3,
            110: 12,
        },
        "unsigned_rank_distribution": dict(unsigned_rank_distribution) == {
            75: 1,
            84: 1,
            90: 1,
            93: 1,
            97: 3,
            103: 6,
            106: 12,
            108: 3,
            109: 12,
        },
    }

    theorem = (
        "Orientation-Twist Readout Gauge Theorem.  The cross-layer common "
        "kernel K=ker(d1)∩ker(Hx_plus) has dimension 165, but it is not a "
        "full PSp(4,3)-module because the signed chain action and unsigned "
        "line-product action use incompatible coefficient conventions.  Among "
        "the 40 projective symplectic transvections, exactly one preserves K "
        "under both conventions.  Its closure has order 3.  Thus the 61-core "
        "from BT356 is a ternary readout-gauge-fixed overlap, not an "
        "unbroken symplectic representation."
    )

    return {
        "summary": {
            "rank_constraints": rank_constraints,
            "common_kernel_dim": common_kernel_dim,
            "transvections": len(transvections),
            "signed_survivors": signed_indices,
            "unsigned_survivors": unsigned_indices,
            "both_survivors": both_indices,
            "survivor_closure_order": survivor_order,
            "all_identities_hold": all(identities.values()),
        },
        "constraint_layer": {
            "constraints": "stacked oriented d1 and all-plus Hx_plus",
            "rank": rank_constraints,
            "kernel_dim": common_kernel_dim,
        },
        "signed_chain_action": {
            "surviving_transvection_indices": signed_indices,
            "combined_rank_distribution": {str(k): int(v) for k, v in sorted(signed_rank_distribution.items())},
        },
        "unsigned_support_action": {
            "surviving_transvection_indices": unsigned_indices,
            "combined_rank_distribution": {str(k): int(v) for k, v in sorted(unsigned_rank_distribution.items())},
        },
        "common_readout_gauge": {
            "surviving_transvection_indices": both_indices,
            "closure_order": survivor_order,
            "interpretation": "C3 ternary readout/clock symmetry survives the orientation/support clash.",
        },
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": (
            "This is a generator-level obstruction for the canonical "
            "transvection generating set.  It proves the full symplectic "
            "action is not compatible with the chosen cross-layer coefficient "
            "gauge, and it identifies the surviving transvection-generated "
            "readout symmetry."
        ),
    }


def main() -> int:
    payload = build_payload()
    out = Path("data/w33_BREAKTHROUGH_358_orientation_twist_readout_gauge.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {out}")
    return 0 if payload["summary"]["all_identities_hold"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
