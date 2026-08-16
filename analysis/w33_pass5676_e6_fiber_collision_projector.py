#!/usr/bin/env python3
"""Pass5676: the exact extra principle that separates E6 horizontal36 from vertical9.

Pass5620/5628 established that the 45 E6 cubic supports are a Z3 bundle split

    36 horizontal line lifts  +  9 complete vertical fibers,

and that local bundle gauge invariance alone permits independent couplings g_H,g_V.
This pass asks whether a *locality/Hodge-like* rule can remove the vertical nine.

For a cubic support T let n_b(T) be the number of its three vertices over base site b.
Define the gauge-invariant same-fiber collision count

    C(T) = sum_b binom(n_b,2) = (||n||^2-3)/2.

Then exactly

    C(T)=0  for every horizontal support (occupancy 1+1+1),
    C(T)=3  for every vertical support   (occupancy 3).

Thus on the 45-dimensional cubic-support basis the diagonal collision operator has
spectrum 0^36 + 3^9 and gives exact projectors

    P_H = I-C/3,    P_V=C/3.

This operator is invariant under arbitrary independent Z3 translations inside the
nine fibers because it only sees the bundle projection.  A hard-core/locality axiom
"at most one field insertion per fiber" therefore kills the bad9 exactly.

Crucially this axiom is *additional physics*, not a consequence of gauge symmetry.
The 9x12 AG(2,3) point-line incidence matrix has rank nine, so the horizontal base-line
occupancies already span the whole base site space.  No linear projector acting only
on base C0 can kill all vertical site vectors while preserving all horizontal lines.
The first exact separator is the quadratic collision invariant above.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS5676_E6_FIBER_COLLISION_PROJECTOR.json"
Q = 3


def ag23():
    pts = [(x, y) for x in range(Q) for y in range(Q)]
    pi = {p: i for i, p in enumerate(pts)}
    dirs = [(1, m) for m in range(Q)] + [(0, 1)]
    lines = set()
    for p in pts:
        for dx, dy in dirs:
            line = tuple(sorted({
                ((p[0] + t * dx) % Q, (p[1] + t * dy) % Q)
                for t in range(Q)
            }))
            lines.add(line)
    return pts, pi, sorted(lines)


def collision(n):
    n = np.asarray(n, dtype=int)
    assert int(n.sum()) == 3
    return int((n @ n - 3) // 2)


def main():
    pts, pi, lines = ag23()
    assert (len(pts), len(lines)) == (9, 12)

    # Point-line incidence.  For AG(2,3), BB^T=3I+J and hence rank(B)=9.
    B = np.zeros((9, 12), dtype=int)
    for j, line in enumerate(lines):
        for p in line:
            B[pi[p], j] = 1
    gram = B @ B.T
    assert np.array_equal(gram, 3 * np.eye(9, dtype=int) + np.ones((9, 9), dtype=int))
    assert np.linalg.matrix_rank(B) == 9

    horizontal = []
    for j in range(12):
        n = B[:, j].copy()
        # Three connection lifts per affine line have the same base occupancy.
        for k in range(3):
            horizontal.append((j, k, n.copy()))
    vertical = []
    for b in range(9):
        n = np.zeros(9, dtype=int)
        n[b] = 3
        vertical.append((b, n))
    assert len(horizontal) == 36 and len(vertical) == 9
    assert {collision(n) for _, _, n in horizontal} == {0}
    assert {collision(n) for _, n in vertical} == {3}

    Cdiag = np.array([0] * 36 + [3] * 9, dtype=float)
    PH = np.diag(1.0 - Cdiag / 3.0)
    PV = np.diag(Cdiag / 3.0)
    assert np.allclose(PH @ PH, PH)
    assert np.allclose(PV @ PV, PV)
    assert np.allclose(PH @ PV, 0)
    assert np.allclose(PH + PV, np.eye(45))
    assert (int(round(np.trace(PH))), int(round(np.trace(PV)))) == (36, 9)

    # Gauge invariance is immediate from projection occupancy: arbitrary fiber
    # translations t_b -> t_b+s_b do not alter n_b.  Exhaust a toy support check.
    shifts = list(itertools.product(range(3), repeat=3))
    sample_sites = [0, 1, 2]
    sample = [(sample_sites[i], i) for i in range(3)]
    n0 = np.zeros(9, dtype=int)
    for b, _ in sample:
        n0[b] += 1
    for ss in shifts:
        moved = [(b, (t + ss[i]) % 3) for i, (b, t) in enumerate(sample)]
        n = np.zeros(9, dtype=int)
        for b, _ in moved:
            n[b] += 1
        assert np.array_equal(n, n0) and collision(n) == collision(n0)

    out = {
        "pass": 5676,
        "status": "EXACT_GAUGE_INVARIANT_FIBER_COLLISION_PROJECTOR_SEPARATES_36_PLUS_9",
        "bundle": {"base": "AG(2,3)", "sites": 9, "lines": 12, "fiber": "Z3"},
        "point_line_incidence": {
            "rank": 9,
            "gram_identity": "B B^T = 3 I_9 + J_9",
            "consequence": "horizontal line occupancies span all base C0; no linear base-site projector can keep every horizontal line while killing every vertical site vector"
        },
        "collision_invariant": "C(T)=sum_b binom(n_b(T),2)=(||n(T)||^2-3)/2",
        "horizontal36": {"occupancy": "1+1+1 on an affine line", "collision": 0},
        "vertical9": {"occupancy": "3 on one fiber", "collision": 3},
        "cubic_basis_spectrum": "C_45 = 0^36 + 3^9",
        "projectors": {
            "P_H": "I-C/3, rank 36",
            "P_V": "C/3, rank 9"
        },
        "gauge_invariance": "arbitrary independent Z3 translations inside fibers preserve the base occupancy n_b and therefore commute with C, P_H and P_V",
        "mechanism": "a hard-core/fiber-locality rule allowing at most one insertion from each gauge fiber projects exactly onto the horizontal36",
        "physics_boundary": "Gauge symmetry itself still does not set g_V=0. The collision penalty or hard-core rule is an additional locality/dynamical postulate whose coefficient is not derived here."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
