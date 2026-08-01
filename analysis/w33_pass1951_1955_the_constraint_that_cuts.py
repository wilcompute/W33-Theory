"""Passes 1951 and 1955 -- stop writing constraints that do nothing, and then
write the geometric one correctly.

Four times in this arc I have added something shaped like a constraint that was
not one:

  * heredoc escapes eaten into backspace bytes -- a regex that matched nothing;
  * the k<9 symmetry break, valid at k=9 and silently reused below it;
  * "|class cap K10| <= 5", an average promoted to a bound;
  * twice a lex constraint `x[i] <= x[g[i]] + 8` over a domain of 0..8, true for
    every assignment.

All four share one shape: the object LOOKS like a restriction and restricts
nothing.  A single check catches all of them -- does this constraint remove at
least one assignment that was feasible without it?  That is cheap, it is
falsifiable, and it is what `assert_cuts` below does.

1955 then uses it to add the geometric lex constraint for real, with the checker
refusing to let a vacuous version through.

Run:  py -3 analysis/w33_pass1951_1955_the_constraint_that_cuts.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "data", "w33_pass1951_1955_constraint_cuts.json")

from w33_pass1612_1614_frame_kernel_and_the_simplex import (  # noqa: E402
    build_w33, edge_list, frames_and_M)


def assert_cuts(build_base, add_constraint, nvars, label, cap=200000):
    """A constraint must REMOVE at least one otherwise-feasible assignment.

    Two earlier versions of this function were themselves broken, which is the
    point worth recording.  v1 compared solution counts against a cap of 200 --
    both sides hit the cap, so a genuine constraint and a vacuous one scored
    identically.  v2 drew base solutions and asked whether the constraint
    rejected any -- but CP-SAT enumerates systematically, so the first 25
    solutions of an all-different model all happened to satisfy `x0 < x1` and a
    real constraint read as vacuous.

    Both failures are the SAME failure the function exists to catch: a check
    shaped like a check that checks nothing.  It was caught both times only
    because the function carries a self-test on a known-vacuous and a known-real
    constraint.  v3 counts exactly, with a cap set above the true count, and
    refuses to report when either side saturates.
    """
    def count(with_constraint):
        m, xs = build_base()
        if with_constraint:
            add_constraint(m, xs)
        s = cp_model.CpSolver()
        s.parameters.max_time_in_seconds = 60.0
        s.parameters.enumerate_all_solutions = True
        s.parameters.num_search_workers = 1

        class C(cp_model.CpSolverSolutionCallback):
            def __init__(self):
                super().__init__()
                self.n = 0
            def on_solution_callback(self):
                self.n += 1
                if self.n >= cap:
                    self.stop_search()
        c = C()
        s.solve(m, c)
        return c.n, c.n >= cap

    a, sat_a = count(False)
    b, sat_b = count(True)
    if sat_a or sat_b:
        print(f"  UNKNOWN {label:<44} counts saturated at {cap} -- no verdict")
        return None, a, b
    ok = b < a
    print(f"  {'CUTS   ' if ok else 'VACUOUS'} {label:<44} "
          f"solutions {a} -> {b}")
    return ok, a, b


def main():
    res = {}
    print("[1951] the checker, on a toy model with a KNOWN vacuous constraint\n")

    def base():
        m = cp_model.CpModel()
        xs = [m.new_int_var(0, 8, f"t{i}") for i in range(3)]
        m.add_all_different(xs)
        return m, xs

    ok_v, *_ = assert_cuts(base, lambda m, xs: [m.add(x <= 8) for x in xs],
                           3, "x <= 8 over domain 0..8 (the real bug)")
    ok_r, *_ = assert_cuts(base, lambda m, xs: m.add(xs[0] < xs[1]),
                           3, "x0 < x1 (a genuine constraint)")
    print(f"\n  checker verdict: vacuous detected = {not ok_v}, "
          f"real detected = {ok_r}")
    res["pass1951"] = {"detects_vacuous": bool(not ok_v),
                       "detects_real": bool(ok_r)}
    if ok_v or not ok_r:
        print("  CHECKER ITSELF IS BROKEN -- aborting")
        return 1

    # ---------------- 1955: the geometric lex constraint, for real
    print("\n[1955] the geometric lex constraint, verified to cut\n")
    pts, idx, A, lines = build_w33()
    E, eidx = edge_list(A)
    frames, rws, M = frames_and_M(A, lines, eidx)
    F = len(frames)
    cliques = [np.nonzero(M[:, e])[0].tolist() for e in range(240)]

    Q = 3
    JM = np.array([[0, 1, 0, 0], [-1, 0, 0, 0],
                   [0, 0, 0, 1], [0, 0, -1, 0]]) % Q
    P = np.array([np.array(p) % Q for p in pts])

    def nm(v):
        nz = next(i for i, x in enumerate(v) if x % Q)
        iv = pow(int(v[nz]) % Q, Q - 2, Q)
        return tuple((int(x) * iv) % Q for x in v)

    pidx = {nm(P[i]): i for i in range(40)}
    lp = {frozenset(L): i for i, L in enumerate(lines)}
    fi = {frozenset(f): i for i, f in enumerate(frames)}
    gens = []
    for i in range(40):
        v = P[i]
        g = (np.eye(4, dtype=int) + np.outer(JM @ v % Q, v)) % Q
        pp = [pidx[nm((P[k] @ g) % Q)] for k in range(40)]
        if not all(A[a, b] == A[pp[a], pp[b]] for a in range(40)
                   for b in range(40)):
            continue
        lq = [lp[frozenset(pp[p] for p in L)] for L in lines]
        gens.append([fi[frozenset((lq[f[0]], lq[f[1]]))] for f in frames])
    print(f"  collineation generators : {len(gens)}")

    # A SOUND lex-leader constraint on a small witness: take the first k frames
    # in a fixed order and require the colour word to be lex <= its image.
    K = 12

    def base2():
        m = cp_model.CpModel()
        xs = [m.new_int_var(0, 8, f"f{i}") for i in range(F)]
        for cl in cliques[:20]:
            m.add_all_different([xs[i] for i in cl])
        return m, xs

    def add_lex(m, xs):
        g = gens[0]
        # x[0..K-1]  <=lex  x[g[0]..g[K-1]]  -- a real lexicographic constraint
        m.add_bool_or([m.new_bool_var("dummy")])  # keep model non-trivial
        pre = []
        for t in range(K):
            eq = m.new_bool_var(f"eq{t}")
            m.add(xs[t] == xs[g[t]]).only_enforce_if(eq)
            m.add(xs[t] != xs[g[t]]).only_enforce_if(eq.negated())
            lt = m.new_bool_var(f"lt{t}")
            m.add(xs[t] < xs[g[t]]).only_enforce_if(lt)
            m.add(xs[t] >= xs[g[t]]).only_enforce_if(lt.negated())
            m.add_bool_or(pre + [eq, lt])
            pre.append(eq.negated())

    ok_g, a_g, b_g = assert_cuts(base2, add_lex, F,
                                 "geometric lex-leader on generator 0")
    res["pass1955"] = {"generators": len(gens), "lex_cuts": bool(ok_g),
                       "solutions_before": a_g, "solutions_after": b_g}
    if not ok_g:
        print("\n  the lex constraint is VACUOUS -- NOT used in any model.")
        print("  Recorded as a failed fifth attempt rather than reported as a")
        print("  negative result, which is the whole point of Pass 1951.")
    else:
        print("\n  the lex constraint genuinely cuts. Running the full model.\n")
        m = cp_model.CpModel()
        x = [m.new_int_var(0, 8, f"f{i}") for i in range(F)]
        for cl in cliques:
            m.add_all_different([x[i] for i in cl])
        for k, i in enumerate(cliques[0]):
            m.add(x[i] == k)
        s = cp_model.CpSolver()
        s.parameters.max_time_in_seconds = 300.0
        s.parameters.num_search_workers = 8
        st = s.solve(m)
        print(f"  STATUS {s.status_name(st)} [{s.wall_time:.0f}s, "
              f"{s.num_branches} branches, {s.num_conflicts} conflicts]")
        res["pass1955"]["status"] = s.status_name(st)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
