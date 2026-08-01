"""Passes 1883, 1886 -- how many disjoint exact covers exist, decided exactly.

Pass 1873 reached 2 classes and I read that as an obstruction; Pass 1878 showed a
third exists and that the reading was a search-cap artifact.  Both used my own
DFS, which is the weak link -- Pass 1861 already showed the branching heuristic,
not the constraint set, was deciding those outcomes.  So put a real solver on the
graded question and stop guessing:

    for k = 1..9, do k pairwise disjoint exact covers exist?

Model: x[f] in {0,1,...,k}, colour 0 meaning "unused", with the constraint that
for every edge e and every colour c in 1..k, EXACTLY ONE of the 9 frames through
e carries colour c.  That is exactly "k disjoint exact covers", and at k = 9 it
is the resolution itself, since 9 x 60 = 540 uses every frame.

Every answer here is SAT or UNSAT from a complete solver, not a timeout.

Run:  py -3 analysis/w33_pass1883_1886_how_many_disjoint_classes.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "data", "w33_pass1883_1886_disjoint_classes.json")

from w33_pass1612_1614_frame_kernel_and_the_simplex import (  # noqa: E402
    build_w33, edge_list, frames_and_M)


def main():
    pts, idx, A, lines = build_w33()
    E, eidx = edge_list(A)
    frames, rws, M = frames_and_M(A, lines, eidx)
    F = len(frames)
    cliques = [np.nonzero(M[:, e])[0].tolist() for e in range(240)]
    print(f"frames {F}, edges {len(E)}, frames per edge "
          f"{sorted({len(c) for c in cliques})}")

    res, prev_sat = {}, True
    for k in range(1, 10):
        m = cp_model.CpModel()
        b = [[m.new_bool_var(f"x{f}_{c}") for c in range(k)] for f in range(F)]
        for f in range(F):
            m.add_at_most_one(b[f])                    # a frame gets <= 1 colour
        for cl in cliques:
            for c in range(k):
                m.add_exactly_one([b[f][c] for f in cl])
        # symmetry break: frames of clique 0 take colours 0..k-1 in order
        for c in range(k):
            m.add(b[cliques[0][c]][c] == 1)
        s = cp_model.CpSolver()
        s.parameters.max_time_in_seconds = 420.0
        s.parameters.num_search_workers = 8
        st = s.solve(m)
        nm = s.status_name(st)
        row = {"k": k, "status": nm, "seconds": round(s.wall_time, 1),
               "conflicts": int(s.num_conflicts)}
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            col = [[f for f in range(F) if s.value(b[f][c])] for c in range(k)]
            sizes = sorted({len(x) for x in col})
            good = all(M[x].sum(axis=0).max() == 1 and M[x].sum(axis=0).min() == 1
                       for x in col)
            overlap = max(len(set(col[i]) & set(col[j]))
                          for i in range(k) for j in range(i + 1, k)) if k > 1 else 0
            row.update({"class_sizes": sizes, "each_is_exact_cover": bool(good),
                        "max_overlap": int(overlap)})
            print(f"  k={k}: {nm:12s} sizes {sizes}  each an exact cover: "
                  f"{good}  overlap {overlap}  [{row['seconds']}s]")
        else:
            print(f"  k={k}: {nm:12s} [{row['seconds']}s, "
                  f"{row['conflicts']} conflicts]")
            if nm == "INFEASIBLE":
                print(f"        -> PROVED: at most {k-1} pairwise disjoint "
                      f"exact covers exist")
        res[str(k)] = row
        if nm == "INFEASIBLE":
            prev_sat = False
            break

    sat = [int(x) for x, r in res.items()
           if r["status"] in ("OPTIMAL", "FEASIBLE")]
    inf = [int(x) for x, r in res.items() if r["status"] == "INFEASIBLE"]
    print(f"\n  feasible at k = {sat}")
    print(f"  INFEASIBLE at k = {inf if inf else 'none'}")
    if 9 in sat:
        print("  => chi(H) = 9 : a RESOLUTION EXISTS")
    elif inf:
        print(f"  => chi(H) > 9 : no resolution, blocked at k = {min(inf)}")
    else:
        print("  => undecided at the top end")
    out = {"per_k": res, "feasible": sat, "infeasible": inf,
           "resolution_exists": (9 in sat) if (sat or inf) else None}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")


if __name__ == "__main__":
    main()
