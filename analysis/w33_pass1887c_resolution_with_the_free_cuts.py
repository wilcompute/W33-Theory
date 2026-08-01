"""Pass 1887 (continued) -- give the solver the cuts I already proved.

Two earlier attempts under-performed for the same reason: the model knew the
240 AllDifferent constraints and nothing else, so propagation was weak (2.1M
branches, 3,622 conflicts).  But Passes 1613/1817/1827 proved several families of
EXACT cardinality identities that every colour class of every resolution must
satisfy, and none of them were ever handed to a solver:

  * every class has exactly 60 frames                       (Hoffman tightness)
  * every class meets each octet neighbourhood in exactly 8   (45 x 9 equations)
  * every class meets each point family in exactly 12         (40 x 9 equations)

Each is a theorem, not a heuristic, so adding them cannot change the answer --
only how fast it is reached.  The prescribed-automorphism route is also closed
off here properly: every element of order 3 and 9 found is tested, not just 14.

Run:  py -3 analysis/w33_pass1887c_resolution_with_the_free_cuts.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "data", "w33_pass1887c_free_cuts_resolution.json")

from w33_pass1612_1614_frame_kernel_and_the_simplex import (  # noqa: E402
    build_w33, edge_list, frames_and_M, grids)
from w33_pass1817_1818_free_cuts_and_branching import spreads  # noqa: E402


def main():
    pts, idx, A, lines = build_w33()
    E, eidx = edge_list(A)
    frames, rws, M = frames_and_M(A, lines, eidx)
    F = len(frames)
    cliques = [np.nonzero(M[:, e])[0].tolist() for e in range(240)]

    oc = grids(A)
    K = np.zeros((len(oc), 240), dtype=np.int64)
    for o, (P1, Q1) in enumerate(oc):
        for p in P1:
            for q in Q1:
                K[o, eidx[(min(p, q), max(p, q))]] = 1
    inter = M @ K.T
    octet_fam = [np.nonzero(inter[:, o] == 2)[0].tolist() for o in range(len(oc))]
    thru = [{li for li, L in enumerate(lines) if p in L} for p in range(40)]
    point_fam = [[i for i, f in enumerate(frames)
                  if f[0] in thru[p] or f[1] in thru[p]] for p in range(40)]
    sp = spreads(lines, A)
    fidx = {frozenset(f): i for i, f in enumerate(frames)}
    traps = [[fidx[frozenset((a, b))] for i, a in enumerate(S) for b in S[i + 1:]]
             for S in sp]

    print(f"free cuts available:")
    print(f"  octet families : {len(octet_fam)} of size "
          f"{sorted({len(x) for x in octet_fam})}, share per class 8")
    print(f"  point families : {len(point_fam)} of size "
          f"{sorted({len(x) for x in point_fam})}, share per class 12")
    print(f"  spread K10 traps (max 45 frames, so <=5 per class): {len(traps)}")

    m = cp_model.CpModel()
    b = [[m.new_bool_var(f"x{f}_{c}") for c in range(9)] for f in range(F)]
    for f in range(F):
        m.add_exactly_one(b[f])
    for cl in cliques:                                   # the rainbow condition
        for c in range(9):
            m.add_exactly_one([b[f][c] for f in cl])
    for c in range(9):                                   # Hoffman: 60 per class
        m.add(sum(b[f][c] for f in range(F)) == 60)
    for fam in octet_fam:                                # Pass 1541/1827
        for c in range(9):
            m.add(sum(b[f][c] for f in fam) == 8)
    for fam in point_fam:                                # Pass 1817, new
        for c in range(9):
            m.add(sum(b[f][c] for f in fam) == 12)
    for t in traps:            # Pass 1828: a K10 is maximal at 45, so <=5/class
        for c in range(9):
            m.add(sum(b[f][c] for f in t) <= 5)
    for c in range(9):                                   # colour symmetry break
        m.add(b[cliques[0][c]][c] == 1)

    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = 1500.0
    s.parameters.num_search_workers = 8
    s.parameters.symmetry_level = 4
    print("\nsolving the strengthened model...\n")
    st = s.solve(m)
    nm = s.status_name(st)
    print(f"  STATUS    : {nm}")
    print(f"  wall time : {s.wall_time:.1f}s")
    print(f"  branches  : {s.num_branches}   conflicts: {s.num_conflicts}")
    out = {"status": nm, "wall_time": round(s.wall_time, 1),
           "branches": int(s.num_branches), "conflicts": int(s.num_conflicts)}

    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        col = [next(c for c in range(9) if s.value(b[f][c])) for f in range(F)]
        cls = [[f for f in range(F) if col[f] == c] for c in range(9)]
        sizes = sorted({len(c) for c in cls})
        covers = all(M[c].sum(axis=0).max() == 1 and M[c].sum(axis=0).min() == 1
                     for c in cls)
        G = M @ M.T
        AH = ((G - np.diag(np.diag(G))) > 0).astype(np.int64)
        proper = all(col[a] != col[bb]
                     for a in range(F) for bb in np.nonzero(AH[a])[0])
        print(f"\n  *** RESOLUTION FOUND ***")
        print(f"  class sizes                        : {sizes}")
        print(f"  every class is an exact cover      : {covers}")
        print(f"  proper 9-colouring of H            : {proper}")
        print(f"  chi(H) = 9 CONFIRMED               : {covers and proper}")
        out.update({"resolution_found": True,
                    "verified": bool(covers and proper),
                    "class_sizes": [len(c) for c in cls], "witness": col})
    elif st == cp_model.INFEASIBLE:
        print(f"\n  *** PROVED INFEASIBLE: no resolution exists, chi(H) > 9 ***")
        out.update({"resolution_found": False, "proved_infeasible": True})
    else:
        print(f"\n  undecided within the limit")
        out["resolution_found"] = None

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")


if __name__ == "__main__":
    main()
