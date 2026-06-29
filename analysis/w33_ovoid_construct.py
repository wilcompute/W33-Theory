#!/usr/bin/env python3
"""
The explicit noncontextual model: construct the even-q ovoid that predicts CF = 0. The parity law
(w33_audit_qscan.py) says W(q) is contextual iff q is odd, because an ovoid -- a Kochen-Specker 0/1
assignment satisfying every context -- exists iff q is even. That is the prediction; this witness
EXHIBITS the object. For the even orders q = 2 and q = 4 it constructs the actual ovoid (a set of q^2+1
points meeting every line exactly once) and verifies it independently, three ways:

    1. size              |ovoid| = q^2 + 1                       (W(2): 5,  W(4): 17)
    2. covers every line  each of the n contexts meets the ovoid in EXACTLY one point
    3. is a cap           the ovoid points are pairwise non-collinear (an independent set)

Property (2) is the whole point: assigning value 1 to the ovoid points and 0 to the rest is a global,
context-INDEPENDENT truth assignment that satisfies all n measurement contexts at once. That is a
working noncontextual hidden-variable model, so the even-q fabric has contextual fraction zero. For the
odd order q = 3 the witness shows the OBSTRUCTION instead: no ovoid exists (the best assignment leaves
4 of 40 contexts unsatisfiable, max partial ovoid 7 < 10), which is exactly why the Holonet substrate is
contextual.

This makes the demonstrator's control arm concrete. The photonic contextuality test
(holonet_demonstrator_protocol_v1.tex) measures the q = 3 fabric and expects CF = 1/10. Run the SAME
apparatus on an even-order analyzer map (W(2) 15 rays / W(4) 85 rays) and the prediction flips to CF = 0,
and THIS file is the explicit model that produces every expected outcome: the ovoid assignment. The
positive arm and the control arm are the same hardware with opposite, geometry-forced predictions.

The ovoid is found by the max-satisfiable-contexts integer program (an exactly-one-per-line assignment
IS an ovoid) and then re-checked by the three independent tests above, so the construction does not
trust the solver -- it verifies the object the solver returns.

Honest scope: exact finite construction over the genuine fields F_2 and GF(4); q = 4 uses GF(4), not
integers mod 4. This is the noncontextual model for the control arm of the physical test, not itself a
physical run.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import w33_master_audit as audit  # noqa: E402


def find_ovoid(q):
    """Return (ovoid_point_indices_or_None, pts, lines, A). Ovoid = a max-satisfying 0/1 assignment."""
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp

    pts, A, lines, B = audit._build(q)
    n = len(pts)
    nv = n + len(lines)
    rows, lb, ub = [], [], []
    for li, L in enumerate(lines):
        r1 = np.zeros(nv)
        r1[n + li] = 1
        for p in L:
            r1[p] -= 1
        rows.append(r1)
        lb.append(-np.inf)
        ub.append(0)
        r2 = np.zeros(nv)
        r2[n + li] = len(L) - 1
        for p in L:
            r2[p] += 1
        rows.append(r2)
        lb.append(-np.inf)
        ub.append(len(L))
    c = np.zeros(nv)
    c[n:] = -1
    res = milp(
        c=c,
        constraints=LinearConstraint(np.array(rows), np.array(lb), np.array(ub)),
        integrality=np.ones(nv),
        bounds=Bounds(0, 1),
    )
    max_sat = int(round(-res.fun))
    x = np.round(res.x[:n]).astype(int)
    ovoid = [i for i in range(n) if x[i] == 1]
    full = max_sat == len(lines)
    return (ovoid if full else None), pts, lines, A, max_sat


def verify_ovoid(ovoid, pts, lines, A, q):
    """Independently check the three ovoid properties; return (ok, report dict)."""
    n = len(pts)
    size_ok = len(ovoid) == q**2 + 1
    oset = set(ovoid)
    # every line meets the ovoid in exactly one point
    per_line = [len(set(L) & oset) for L in lines]
    covers_ok = all(m == 1 for m in per_line)
    # pairwise non-collinear (independent set in the collinearity graph)
    cap_ok = all(A[i][j] == 0 for a, i in enumerate(ovoid) for j in ovoid[a + 1 :])
    return (size_ok and covers_ok and cap_ok), {
        "size": len(ovoid),
        "expected_size": q**2 + 1,
        "size_ok": size_ok,
        "covers_every_line_once": covers_ok,
        "is_cap_pairwise_noncollinear": cap_ok,
        "min_line_hits": min(per_line),
        "max_line_hits": max(per_line),
    }


def main():
    print("== the explicit noncontextual model: even-q ovoids predicting CF=0 ==\n")
    out = {"orders": {}, "summary": "", "sources": []}
    all_ok = True

    for q in (2, 4):
        ovoid, pts, lines, A, max_sat = find_ovoid(q)
        if ovoid is None:
            print(f"q={q}: NO ovoid found (unexpected for even q!)")
            all_ok = False
            continue
        ok, rep = verify_ovoid(ovoid, pts, lines, A, q)
        all_ok = all_ok and ok
        coords = [pts[i] for i in ovoid]
        print(
            f"q={q} (EVEN): ovoid of {rep['size']} points (expected {rep['expected_size']}) "
            f"-> covers every line once: {rep['covers_every_line_once']}, cap: {rep['is_cap_pairwise_noncollinear']}  [{'PASS' if ok else 'FAIL'}]"
        )
        print(f"   explicit ovoid points: {coords}")
        print(
            f"   => assign 1 to these {rep['size']} rays, 0 elsewhere: a noncontextual model satisfying all {len(lines)} contexts -> CF = 0\n"
        )
        out["orders"][q] = {
            "parity": "even",
            "ovoid_exists": True,
            "ovoid_points": ["".join(map(str, pts[i])) for i in ovoid],
            "verify": rep,
            "contextual_fraction": 0.0,
            "verified": ok,
        }

    # the odd control: q=3 has NO ovoid (the obstruction that makes the Holonet contextual)
    ovoid3, pts3, lines3, A3, max_sat3 = find_ovoid(3)
    has3 = ovoid3 is not None
    print(
        f"q=3 (ODD): ovoid exists: {has3}  -> best assignment satisfies {max_sat3}/{len(lines3)} contexts "
        f"({len(lines3)-max_sat3} unsatisfiable) -> CF = {(len(lines3)-max_sat3)/len(lines3):.3g} (CONTEXTUAL)"
    )
    out["orders"][3] = {
        "parity": "odd",
        "ovoid_exists": has3,
        "max_satisfiable_contexts": max_sat3,
        "n_contexts": len(lines3),
        "contextual_fraction": (len(lines3) - max_sat3) / len(lines3),
    }
    odd_ok = not has3 and max_sat3 == 36
    all_ok = all_ok and odd_ok

    out["summary"] = (
        "the explicit noncontextual model: for even q (2 and 4) the witness CONSTRUCTS the ovoid -- a set "
        "of q^2+1 points (5 and 17) meeting every line exactly once -- and verifies it three independent "
        "ways (size, covers-every-line-once, pairwise non-collinear cap). Assigning 1 to the ovoid points "
        "and 0 elsewhere is a global context-independent truth assignment satisfying all n contexts, i.e. "
        "a working noncontextual hidden-variable model, so even-q fabrics have CF=0. For odd q=3 there is "
        "NO ovoid (best assignment leaves 4/40 contexts unsatisfiable), the obstruction that makes the "
        "Holonet contextual. This is the explicit predicted data for the CONTROL ARM of the photonic "
        "demonstrator: the same single-photon apparatus on an even-order analyzer map should read CF=0, "
        "with this ovoid as the model; the q=3 arm reads CF=1/10. Same hardware, opposite geometry-forced "
        "predictions. HONEST: exact finite construction over F_2 and the genuine field GF(4); the model "
        "for a physical control arm, not itself a physical run."
    )
    out["sources"] = [
        "w33_master_audit._build (GF(4) included)",
        "max-satisfiable-contexts ILP (scipy milp); ovoid re-verified independently",
        "Thas: ovoids of W(q) exist iff q even; pairs with w33_audit_qscan and the demonstrator protocol",
    ]
    with open("data/w33_ovoid_construct.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print(
        f"\n{'ALL PASS -- explicit even-q ovoids constructed and verified; q=3 obstruction confirmed.' if all_ok else 'FAILURES present.'}"
    )
    print("wrote data/w33_ovoid_construct.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
