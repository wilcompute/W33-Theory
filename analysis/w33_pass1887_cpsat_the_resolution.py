"""Pass 1887 -- settle chi(H) = 9 with a real CP solver, via a reformulation
that makes the instance tiny.

Every one of the 240 edges lies in exactly 9 frames, and any two frames sharing
that edge are adjacent in H.  So each edge gives a 9-CLIQUE of H.  Each frame has
4 edges, and H is 32-regular with 32 = 4 x 8 -- which forces any two adjacent
frames to share EXACTLY one edge, hence:

    H is precisely the union of 240 edge-disjoint 9-cliques.

(The script verifies that rather than assuming it.)  A proper 9-colouring of H is
therefore nothing but an assignment of 1..9 to the 540 frames making each of the
240 nine-sets AllDifferent -- 540 variables and 240 AllDifferent constraints,
which is a small CP model rather than the 4,860-variable / 99,909-clause CNF that
five previous attempts choked on.

Symmetry breaking: one clique's nine frames may be fixed to 1..9 outright, which
quotients out the 9! = 362,880 colour permutations.

Run:  py -3 analysis/w33_pass1887_cpsat_the_resolution.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "data", "w33_pass1887_cpsat_resolution.json")

from w33_pass1612_1614_frame_kernel_and_the_simplex import (  # noqa: E402
    build_w33, edge_list, frames_and_M)


def main():
    res = {}
    pts, idx, A, lines = build_w33()
    E, eidx = edge_list(A)
    frames, rws, M = frames_and_M(A, lines, eidx)
    F = len(frames)
    G = M @ M.T
    AH = ((G - np.diag(np.diag(G))) > 0).astype(np.int64)

    cliques = [np.nonzero(M[:, e])[0].tolist() for e in range(240)]
    sizes = sorted({len(c) for c in cliques})
    deg = sorted({int(x) for x in AH.sum(axis=1)})
    print(f"frames {F}, edges {len(E)}")
    print(f"  clique sizes (frames per edge) : {sizes}")
    print(f"  H is regular of degree         : {deg}")

    # verify H IS the union of these cliques, edge-disjointly
    seen, dup = set(), 0
    for c in cliques:
        for i in range(len(c)):
            for j in range(i + 1, len(c)):
                p = (c[i], c[j])
                if p in seen:
                    dup += 1
                seen.add(p)
    nH = int(AH.sum()) // 2
    print(f"  pairs covered by the 240 cliques : {len(seen)}   "
          f"edges of H : {nH}   equal: {len(seen) == nH}")
    print(f"  cliques pairwise edge-disjoint   : {dup == 0}   "
          f"(so any two adjacent frames share exactly one edge)")
    exact = (len(seen) == nH and dup == 0 and sizes == [9])
    print(f"  => a proper 9-colouring of H == 240 AllDifferent(9): {exact}")
    res["reformulation_valid"] = bool(exact)
    assert exact, "reformulation does not hold; do not trust the model"

    # ---------------- the CP model
    m = cp_model.CpModel()
    x = [m.new_int_var(0, 8, f"f{i}") for i in range(F)]
    for c in cliques:
        m.add_all_different([x[i] for i in c])
    for k, i in enumerate(cliques[0]):          # symmetry break: fix one clique
        m.add(x[i] == k)

    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = 900.0
    s.parameters.num_search_workers = 8
    s.parameters.log_search_progress = False
    print("\nsolving: 540 vars in 0..8, 240 AllDifferent(9), one clique fixed\n")
    st = s.solve(m)
    name = s.status_name(st)
    print(f"  STATUS   : {name}")
    print(f"  wall time: {s.wall_time:.1f}s   branches: {s.num_branches}   "
          f"conflicts: {s.num_conflicts}")
    res["status"] = name
    res["wall_time"] = round(s.wall_time, 2)
    res["branches"] = int(s.num_branches)
    res["conflicts"] = int(s.num_conflicts)

    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        col = [s.value(v) for v in x]
        classes = [[i for i in range(F) if col[i] == k] for k in range(9)]
        ok_sizes = all(len(c) == 60 for c in classes)
        ok_cover = True
        for c in classes:
            cov = M[c].sum(axis=0)
            if cov.max() != 1 or cov.min() != 1:
                ok_cover = False
        ok_proper = all(col[a] != col[b]
                        for a in range(F) for b in np.nonzero(AH[a])[0])
        print(f"\n  RESOLUTION FOUND")
        print(f"  class sizes all 60                     : {ok_sizes}")
        print(f"  every class exactly covers 240 edges   : {ok_cover}")
        print(f"  colouring is proper on H               : {ok_proper}")
        res["resolution_found"] = True
        res["verified"] = bool(ok_sizes and ok_cover and ok_proper)
        res["class_sizes"] = [len(c) for c in classes]
        res["witness"] = col
        print(f"  chi(H) = 9  CONFIRMED : "
              f"{ok_sizes and ok_cover and ok_proper}")
    elif st == cp_model.INFEASIBLE:
        print(f"\n  PROVED INFEASIBLE -- no resolution exists, chi(H) > 9")
        res["resolution_found"] = False
        res["proved_infeasible"] = True
    else:
        print(f"\n  UNDECIDED within the time limit")
        res["resolution_found"] = None

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")


if __name__ == "__main__":
    main()
