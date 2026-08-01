"""Passes 1892, 1893, 1896 -- audit my own bound, prescribe sigma_S, and branch
on the spread variables.

1896 (first, because it audits pushed work).  The free-cuts model of Pass 1887
asserted that a colour class meets each spread K10 in AT MOST 5 frames.  I never
derived that.  Measure it against real exact covers.  If it is false the model
was unsound -- it returned UNKNOWN so no wrong conclusion was published, but an
unsound model is still a defect and belongs on the record.

1893.  Every prescribed automorphism tried in Pass 1887 had order 3 or 9 and all
were rejected.  sigma_S -- the spread involution that Pass 1882 showed generates
the obstruction -- has order 2 and is the natural candidate.  Build all 36 of
them and test.

1892.  Pass 1818 measured the spread-pair family at 0.9535 branching value, the
highest of any family, while the free cuts measured 0.0000.  Every attack so far
has branched on frames.  Put the spread-pair counts in as explicit variables and
tell the solver to decide them first.

Run:  py -3 analysis/w33_pass1892_1896_spread_encoding_and_a_self_audit.py
"""

from __future__ import annotations

import json
import os
import random
import sys
import time

import numpy as np
from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "data", "w33_pass1892_1896_spread_encoding.json")

from w33_pass1612_1614_frame_kernel_and_the_simplex import (  # noqa: E402
    build_w33, edge_list, frames_and_M)
from w33_pass1817_1818_free_cuts_and_branching import spreads  # noqa: E402


def main():
    res = {}
    pts, idx, A, lines = build_w33()
    E, eidx = edge_list(A)
    frames, rws, M = frames_and_M(A, lines, eidx)
    F = len(frames)
    cliques = [np.nonzero(M[:, e])[0].tolist() for e in range(240)]
    ES = [set(np.nonzero(M[i])[0].tolist()) for i in range(F)]
    sp = spreads(lines, A)
    fidx = {frozenset(f): i for i, f in enumerate(frames)}
    traps = [[fidx[frozenset((a, b))] for i, a in enumerate(S) for b in S[i + 1:]]
             for S in sp]

    # ---------- 1896: is the "<= 5 per spread K10" bound true?
    print("[1896] auditing my own '<= 5 frames per spread K10 per class' bound\n")
    m0 = cp_model.CpModel()
    y = [m0.new_bool_var(f"y{f}") for f in range(F)]
    for cl in cliques:
        m0.add_exactly_one([y[f] for f in cl])          # one exact cover
    hi, lo, seen = 0, 99, []
    s0 = cp_model.CpSolver()
    s0.parameters.max_time_in_seconds = 20.0
    s0.parameters.num_search_workers = 8
    for t in range(60):
        m = m0.clone()
        m.add(sum(y[f] for f in traps[t % 36]) >= (6 if t < 30 else 0))
        s0.parameters.random_seed = t
        st = s0.solve(m)
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            c = [f for f in range(F) if s0.value(y[f])]
            v = max(len(set(c) & set(tr)) for tr in traps)
            hi = max(hi, v)
            lo = min(lo, v)
            seen.append(v)
    print(f"  exact covers sampled              : {len(seen)}")
    print(f"  |cover cap K10| observed range    : {lo} .. {hi}")
    ok = hi <= 5
    print(f"  is the asserted bound <= 5 TRUE?  : {ok}")
    if not ok:
        print(f"  *** the bound is FALSE -- a cover reaching {hi} exists, so the")
        print(f"      Pass 1887 free-cuts model was UNSOUND (it returned UNKNOWN,")
        print(f"      so nothing wrong was concluded, but the model was wrong).")
    res["pass1896"] = {"covers_sampled": len(seen), "min": lo, "max": hi,
                       "asserted_bound_5_holds": bool(ok)}

    # ---------- 1893: prescribe sigma_S (order 2)
    print("\n[1893] prescribing sigma_S, the spread involution (order 2)\n")
    on = [[] for _ in range(40)]
    for ei, (p, q) in enumerate(E):
        for li, L in enumerate(lines):
            if p in L and q in L:
                on[li].append(ei)
    lpos = {frozenset(L): i for i, L in enumerate(lines)}
    accepted, rejected = [], 0
    for si, S in enumerate(sp):
        own = set(e for li in S for e in on[li])
        cand = [i for i in range(F) if ES[i] <= own]
        sig = [-1] * 40
        for i in cand:
            for e in ES[i]:
                u, v = E[e]
                sig[u], sig[v] = v, u
        if any(x < 0 for x in sig):
            rejected += 1
            continue
        lp = [lpos[frozenset(sig[p] for p in L)] for L in lines]
        fp = [fidx[frozenset((lp[f[0]], lp[f[1]]))] for f in frames]
        oid, orb = [-1] * F, 0
        for i in range(F):
            if oid[i] < 0:
                oid[i] = orb
                oid[fp[i]] = orb
                orb += 1
        clash = any(len({oid[f] for f in cl}) != len(cl) for cl in cliques)
        if clash:
            rejected += 1
        else:
            accepted.append((si, orb, oid))
    print(f"  sigma_S built for {len(sp)} spreads; "
          f"rejected by the clique test: {rejected}, accepted: {len(accepted)}")
    row = {"spreads": len(sp), "rejected": rejected, "accepted": len(accepted)}
    if accepted:
        si, norb, oid = accepted[0]
        print(f"  solving the orbit colouring for spread {si}: {norb} orbits")
        m = cp_model.CpModel()
        x = [m.new_int_var(0, 8, f"o{k}") for k in range(norb)]
        for cl in cliques:
            m.add_all_different([x[oid[f]] for f in cl])
        for k, f in enumerate(cliques[0]):
            m.add(x[oid[f]] == k)
        s = cp_model.CpSolver()
        s.parameters.max_time_in_seconds = 240.0
        s.parameters.num_search_workers = 8
        st = s.solve(m)
        row["orbit_solve"] = s.status_name(st)
        row["orbits"] = norb
        print(f"  STATUS: {s.status_name(st)}  [{s.wall_time:.1f}s]")
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            col = [s.value(x[oid[f]]) for f in range(F)]
            cls = [[f for f in range(F) if col[f] == c] for c in range(9)]
            good = all(len(c) == 60 and M[c].sum(axis=0).max() == 1
                       and M[c].sum(axis=0).min() == 1 for c in cls)
            print(f"  *** RESOLUTION FOUND, verified: {good} ***")
            row["resolution_found"] = bool(good)
            row["witness"] = col
    res["pass1893"] = row

    # ---------- 1892: branch on the spread-pair variables
    print("\n[1892] branching on the spread-pair counts (0.9535 branching value)"
          "\n")
    m = cp_model.CpModel()
    b = [[m.new_bool_var(f"x{f}_{c}") for c in range(9)] for f in range(F)]
    for f in range(F):
        m.add_exactly_one(b[f])
    for cl in cliques:
        for c in range(9):
            m.add_exactly_one([b[f][c] for f in cl])
    for c in range(9):
        m.add(sum(b[f][c] for f in range(F)) == 60)
    n = [[m.new_int_var(0, min(45, hi if hi else 45), f"n{t}_{c}")
          for c in range(9)] for t in range(36)]
    for t in range(36):
        for c in range(9):
            m.add(n[t][c] == sum(b[f][c] for f in traps[t]))
        m.add(sum(n[t][c] for c in range(9)) == 45)
    for c in range(9):
        m.add(b[cliques[0][c]][c] == 1)
    m.add_decision_strategy([n[t][c] for t in range(36) for c in range(9)],
                            cp_model.CHOOSE_MIN_DOMAIN_SIZE,
                            cp_model.SELECT_MAX_VALUE)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = 600.0
    s.parameters.num_search_workers = 8
    s.parameters.search_branching = cp_model.FIXED_SEARCH
    st = s.solve(m)
    print(f"  STATUS: {s.status_name(st)}  [{s.wall_time:.1f}s, "
          f"{s.num_branches} branches, {s.num_conflicts} conflicts]")
    res["pass1892"] = {"status": s.status_name(st),
                       "seconds": round(s.wall_time, 1),
                       "branches": int(s.num_branches),
                       "conflicts": int(s.num_conflicts)}
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        col = [next(c for c in range(9) if s.value(b[f][c])) for f in range(F)]
        cls = [[f for f in range(F) if col[f] == c] for c in range(9)]
        good = all(len(c) == 60 and M[c].sum(axis=0).max() == 1
                   and M[c].sum(axis=0).min() == 1 for c in cls)
        print(f"  *** RESOLUTION FOUND, verified: {good} ***")
        res["pass1892"]["resolution_found"] = bool(good)
        res["pass1892"]["witness"] = col

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")


if __name__ == "__main__":
    main()
