"""Does this constraint actually restrict anything?

Six times in the Passes 1612-1955 arc something shaped like a constraint turned
out to restrict nothing:

  1. heredoc escapes eaten into backspace bytes -- a regex matching nothing
  2. the k<9 symmetry break, valid at k=9 and silently reused below it
  3. "|class cap K10| <= 5", an average promoted to a bound
  4. `x[i] <= x[g[i]] + 8` over a domain of 0..8, true for every assignment
  5. the same again, one batch later
  6. a VERIFIED constraint that was then never added to the model it was built for

This module exists so the next one is caught before it is reported on.  It lives
in scripts/ rather than in an analysis file because a tool nobody imports is a
tool that does not run -- the same gap that made TOPICAL_ALIASES.md need a
pre-commit hook.

    from constraint_audit import assert_cuts, assert_added

`assert_cuts` answers (1)-(5): does adding this remove at least one otherwise
feasible assignment?  `assert_added` answers (6): did the model actually grow?

IMPORTANT: `assert_cuts` carries a self-test (`selftest()`), and it needs one.
Two earlier versions of it were themselves vacuous -- one saturated a solution
cap so real and fake scored alike, one sampled CP-SAT's systematic enumeration
and got a biased sample -- and only the self-test caught either.
"""

from __future__ import annotations

from ortools.sat.python import cp_model


def _count(build, add, cap):
    m, xs = build()
    if add is not None:
        add(m, xs)
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


def assert_cuts(build_base, add_constraint, label="constraint", cap=200_000,
                verbose=True):
    """True iff `add_constraint` removes at least one feasible assignment.

    Returns (verdict, before, after); verdict is None when either count
    saturates `cap`, because a saturated comparison is exactly how version 1 of
    this function reported a vacuous constraint as real.
    """
    a, sat_a = _count(build_base, None, cap)
    b, sat_b = _count(build_base, add_constraint, cap)
    if sat_a or sat_b:
        if verbose:
            print(f"  UNKNOWN {label:<46} counts saturated at {cap}")
        return None, a, b
    ok = b < a
    if verbose:
        pct = 100.0 * (a - b) / a if a else 0.0
        print(f"  {'CUTS   ' if ok else 'VACUOUS'} {label:<46} "
              f"{a} -> {b}  ({pct:.1f}% removed)")
    return ok, a, b


def assert_added(model, before_proto_size, label="constraint"):
    """True iff the model actually grew -- catches failure mode (6)."""
    after = len(model.proto.constraints)
    ok = after > before_proto_size
    print(f"  {'ADDED  ' if ok else 'NOT ADDED'} {label:<46} "
          f"constraints {before_proto_size} -> {after}")
    if not ok:
        raise AssertionError(
            f"{label}: verified to cut but never added to the model")
    return ok


def selftest(verbose=True):
    """A known-vacuous and a known-real constraint. Both versions 1 and 2 of
    assert_cuts failed this; without it they would have shipped."""
    def base():
        m = cp_model.CpModel()
        xs = [m.new_int_var(0, 8, f"t{i}") for i in range(3)]
        m.add_all_different(xs)
        return m, xs

    v, *_ = assert_cuts(base, lambda m, xs: [m.add(x <= 8) for x in xs],
                        "SELFTEST vacuous: x <= 8 over 0..8", verbose=verbose)
    r, *_ = assert_cuts(base, lambda m, xs: m.add(xs[0] < xs[1]),
                        "SELFTEST real: x0 < x1", verbose=verbose)
    ok = (v is False) and (r is True)
    if verbose:
        print(f"  selftest {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if selftest() else 1)
