"""Pass 1887 (continued) -- attack chi(H)=9 by PRESCRIBING an automorphism.

The plain CP model (540 vars, 240 AllDifferent) ran 900 s to UNKNOWN with 2.1M
branches and only 3,622 conflicts.  That ratio is the signature of a symmetric
instance: the solver keeps finding fresh-looking partial assignments that are
images of ones it already refuted, so it learns almost nothing.

The standard cure for exactly this in design theory is the prescribed-automorphism
method: demand that the object sought be invariant under a chosen subgroup S, so
the unknowns become S-ORBITS rather than frames.  With |S| = 9 the 540 frames
collapse to ~60 orbits and the instance becomes small.

Collineations are built directly here as symplectic transvections
T_v(x) = x + <x,v> v, which generate Sp(4,q), so no external group data is
needed -- and every candidate is verified to preserve the collinearity graph
before it is used.

A necessary condition, checked first: no two frames of the same S-orbit may lie
in a common 9-clique, since a clique must be rainbow.

Run:  py -3 analysis/w33_pass1887b_prescribed_automorphism_resolution.py
"""

from __future__ import annotations

import itertools
import json
import os
import sys

import numpy as np
from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "data", "w33_pass1887b_prescribed_automorphism.json")

from w33_pass1612_1614_frame_kernel_and_the_simplex import (  # noqa: E402
    build_w33, edge_list, frames_and_M)

Q = 3
JM = np.array([[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]]) % Q


def norm(v):
    nz = next(i for i, x in enumerate(v) if x % Q)
    inv = pow(int(v[nz]) % Q, Q - 2, Q)
    return tuple((int(x) * inv) % Q for x in v)


def point_perm(g, P, idx):
    """The permutation of the 40 points induced by a symplectic matrix g."""
    return [idx[norm((P[i] @ g) % Q)] for i in range(len(P))]


def order_of(p):
    n, k, cur = len(p), 1, list(p)
    while cur != list(range(n)):
        cur = [p[i] for i in cur]
        k += 1
        if k > 200:
            return None
    return k


def main():
    pts, idx0, A, lines = build_w33()
    E, eidx = edge_list(A)
    frames, rws, M = frames_and_M(A, lines, eidx)
    F = len(frames)
    cliques = [np.nonzero(M[:, e])[0].tolist() for e in range(240)]

    # rebuild the same 40 points as F_3^4 vectors, matched to build_w33's order
    P = np.array([np.array(p) % Q for p in pts])
    idx = {norm(P[i]): i for i in range(len(P))}
    assert len(idx) == 40

    # transvections T_v(x) = x + <x,v> v
    gens = []
    for v in [P[i] for i in range(40)]:
        g = (np.eye(4, dtype=int) + np.outer(JM @ v % Q, v)) % Q
        pp = point_perm(g, P, idx)
        if all(A[a, b] == A[pp[a], pp[b]] for a in range(40) for b in range(40)):
            gens.append(pp)
    print(f"verified collineations from transvections : {len(gens)}")

    def compose(a, b):
        return [a[b[i]] for i in range(len(b))]

    # random words -> elements of order 3 and 9
    rng = np.random.default_rng(1887)
    pool, seen = [], set()
    cur = list(range(40))
    for _ in range(6000):
        cur = compose(cur, gens[rng.integers(len(gens))])
        t = tuple(cur)
        if t in seen:
            continue
        seen.add(t)
        o = order_of(cur)
        if o in (3, 9):
            pool.append((o, list(cur)))
    ords = sorted({o for o, _ in pool})
    print(f"elements found with order in {{3,9}} : {len(pool)}  orders {ords}")

    # act on frames
    lset = [frozenset(L) for L in lines]
    lpos = {s: i for i, s in enumerate(lset)}
    fpos = {frozenset(f): i for i, f in enumerate(frames)}

    def frame_perm(pp):
        lp = [lpos[frozenset(pp[p] for p in lines[i])] for i in range(40)]
        return [fpos[frozenset((lp[f[0]], lp[f[1]]))] for f in frames]

    def orbits_of(perms):
        seen_, orb = [False] * F, []
        for i in range(F):
            if seen_[i]:
                continue
            o, stack = set(), [i]
            while stack:
                x = stack.pop()
                if x in o:
                    continue
                o.add(x)
                for pm in perms:
                    stack.append(pm[x])
            for x in o:
                seen_[x] = True
            orb.append(sorted(o))
        return orb

    results, tried = [], 0
    for o, pp in pool:
        if tried >= 14:
            break
        fp = frame_perm(pp)
        orb = orbits_of([fp])
        sizes = sorted({len(x) for x in orb})
        oid = [0] * F
        for k, x in enumerate(orb):
            for y in x:
                oid[y] = k
        clash = any(len({oid[f] for f in cl}) != len(cl) for cl in cliques)
        tried += 1
        row = {"order": o, "orbits": len(orb), "orbit_sizes": sizes,
               "clique_clash": bool(clash)}
        if clash:
            row["status"] = "REJECTED (a clique repeats an orbit)"
            results.append(row)
            continue
        # 9-colour the ORBITS
        m = cp_model.CpModel()
        x = [m.new_int_var(0, 8, f"o{k}") for k in range(len(orb))]
        for cl in cliques:
            m.add_all_different([x[oid[f]] for f in cl])
        for k, f in enumerate(cliques[0]):
            m.add(x[oid[f]] == k)
        s = cp_model.CpSolver()
        s.parameters.max_time_in_seconds = 120.0
        s.parameters.num_search_workers = 8
        st = s.solve(m)
        row["status"] = s.status_name(st)
        row["seconds"] = round(s.wall_time, 1)
        print(f"  |S|={o}: {len(orb)} orbits, sizes {sizes} -> "
              f"{row['status']} [{row['seconds']}s]")
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            col = [s.value(x[oid[f]]) for f in range(F)]
            cls = [[f for f in range(F) if col[f] == c] for c in range(9)]
            good = all(len(c) == 60 and M[c].sum(axis=0).max() == 1
                       and M[c].sum(axis=0).min() == 1 for c in cls)
            row["verified_resolution"] = bool(good)
            row["class_sizes"] = [len(c) for c in cls]
            row["witness"] = col
            print(f"     *** RESOLUTION FOUND, verified: {good} "
                  f"class sizes {sorted(set(len(c) for c in cls))} ***")
            results.append(row)
            break
        results.append(row)

    found = [r for r in results if r.get("verified_resolution")]
    print(f"\n  subgroups tried : {len(results)}")
    print(f"  rejected by the clique test : "
          f"{sum(1 for r in results if r['clique_clash'])}")
    print(f"  INFEASIBLE (no S-invariant resolution) : "
          f"{sum(1 for r in results if r.get('status') == 'INFEASIBLE')}")
    print(f"  RESOLUTIONS FOUND : {len(found)}")
    out = {"results": results, "resolution_found": bool(found)}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")


if __name__ == "__main__":
    main()
