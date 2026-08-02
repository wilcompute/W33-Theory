"""Fail-closed constraint auditing.

Version 5 separates two questions that earlier versions conflated:

1. exact enumeration on a *small* witness model;
2. scalable validation on named feasible witnesses or an explicitly supplied
   finite group orbit.

`assert_cuts_small_exact()` may return ``None`` whenever enumeration is
truncated.  It must not be used as a full-scale 540-variable audit.

`audit_named_witnesses()` and `audit_feasible_orbit()` do not enumerate the
unknown global solution set.  They certify only what they literally test:
that a cut rejects at least one known base-feasible assignment, preserves at
least one base-feasible representative, and—when supplied—respects an explicit
equivalence relation or finite feasible orbit.

A scalable witness certificate proves non-vacuity on the supplied witnesses. It
does not estimate the number of all feasible assignments and does not predict
solver performance.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable, Iterable, Optional, Sequence

from ortools.sat.python import cp_model

Assignment = Any
Predicate = Callable[[Assignment], bool]


@dataclass(frozen=True)
class WitnessAudit:
    label: str
    rejected_base_feasible: bool
    rejected_violates_cut: bool
    survivor_base_feasible: bool
    survivor_satisfies_cut: bool
    equivalent: Optional[bool]

    @property
    def passed(self) -> bool:
        required = (
            self.rejected_base_feasible,
            self.rejected_violates_cut,
            self.survivor_base_feasible,
            self.survivor_satisfies_cut,
        )
        return all(required) and self.equivalent is not False

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["passed"] = self.passed
        return out


@dataclass(frozen=True)
class OrbitAudit:
    label: str
    orbit_size: int
    base_feasible: int
    survives_cut: int

    @property
    def removed(self) -> int:
        return self.base_feasible - self.survives_cut

    @property
    def passed(self) -> bool:
        return (
            self.orbit_size > 0
            and self.base_feasible == self.orbit_size
            and 0 < self.survives_cut <= self.base_feasible
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "orbit_size": self.orbit_size,
            "base_feasible": self.base_feasible,
            "survives_cut": self.survives_cut,
            "removed": self.removed,
            "passed": self.passed,
        }


def audit_named_witnesses(
    base_ok: Predicate,
    cut_ok: Predicate,
    rejected: Assignment,
    survivor: Assignment,
    *,
    equivalent: Optional[Callable[[Assignment, Assignment], bool]] = None,
    label: str = "constraint",
    fail: bool = True,
) -> WitnessAudit:
    """Audit a cut on two named assignments in time linear in their size.

    `rejected` must satisfy the base model and violate the cut. `survivor` must
    satisfy both.  If `equivalent` is supplied, the two assignments must be in
    the same certified symmetry class.
    """

    result = WitnessAudit(
        label=label,
        rejected_base_feasible=bool(base_ok(rejected)),
        rejected_violates_cut=not bool(cut_ok(rejected)),
        survivor_base_feasible=bool(base_ok(survivor)),
        survivor_satisfies_cut=bool(cut_ok(survivor)),
        equivalent=(None if equivalent is None else bool(equivalent(rejected, survivor))),
    )
    if fail and not result.passed:
        raise AssertionError(f"{label}: witness audit failed: {result.to_dict()}")
    return result


def audit_feasible_orbit(
    base_ok: Predicate,
    cut_ok: Predicate,
    orbit: Iterable[Assignment],
    *,
    label: str = "constraint orbit",
    fail: bool = True,
) -> OrbitAudit:
    """Audit a cut on an explicitly supplied finite feasible orbit.

    This is exact for the supplied orbit only. It makes no statement about
    assignments outside that orbit.
    """

    items = list(orbit)
    base = sum(bool(base_ok(x)) for x in items)
    after = sum(bool(base_ok(x)) and bool(cut_ok(x)) for x in items)
    result = OrbitAudit(label, len(items), base, after)
    if fail and not result.passed:
        raise AssertionError(f"{label}: orbit audit failed: {result.to_dict()}")
    return result


def assert_added(model: cp_model.CpModel, before_proto_size: int,
                 label: str = "constraint") -> bool:
    """Fail unless the model's serialized constraint list actually grew."""

    after = len(model.proto.constraints)
    if after <= before_proto_size:
        raise AssertionError(
            f"{label}: verified constraint was not added "
            f"({before_proto_size} -> {after})")
    return True


def _count_small_exact(build, add, cap: int, seconds: float):
    model, variables = build()
    if add is not None:
        add(model, variables)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_search_workers = 1

    class Counter(cp_model.CpSolverSolutionCallback):
        def __init__(self):
            super().__init__()
            self.n = 0

        def on_solution_callback(self):
            self.n += 1
            if self.n >= cap:
                self.stop_search()

    counter = Counter()
    status = solver.solve(model, counter)
    complete = (
        counter.n < cap
        and status in (cp_model.OPTIMAL, cp_model.INFEASIBLE)
    )
    return counter.n, complete, solver.status_name(status)


def assert_cuts_small_exact(
    build_base,
    add_constraint,
    label: str = "small exact constraint",
    cap: int = 200_000,
    seconds: float = 60.0,
    verbose: bool = True,
):
    """Return True/False only after complete small-model enumeration.

    Returns `(None, before, after)` if either enumeration is incomplete.  The
    monotonicity invariant `after <= before` is checked whenever both are exact.
    """

    before, complete_before, status_before = _count_small_exact(
        build_base, None, cap, seconds)
    after, complete_after, status_after = _count_small_exact(
        build_base, add_constraint, cap, seconds)
    if not (complete_before and complete_after):
        if verbose:
            print(
                f"UNKNOWN {label}: incomplete enumeration "
                f"({status_before}, {status_after})")
        return None, before, after
    if after > before:
        raise AssertionError(
            f"{label}: impossible monotonicity violation {before} -> {after}")
    verdict = after < before
    if verbose:
        print(f"{'CUTS' if verdict else 'VACUOUS'} {label}: {before} -> {after}")
    return verdict, before, after


def assert_cuts(*args, **kwargs):
    """Compatibility alias for small exact models only.

    New full-scale code should use `audit_named_witnesses` or
    `audit_feasible_orbit` and name the certificate's scope explicitly.
    """

    return assert_cuts_small_exact(*args, **kwargs)


def selftest(verbose: bool = True) -> bool:
    def small_model():
        model = cp_model.CpModel()
        xs = [model.new_int_var(0, 8, f"t{i}") for i in range(3)]
        model.add_all_different(xs)
        return model, xs

    vacuous = assert_cuts_small_exact(
        small_model,
        lambda model, xs: [model.add(x <= 8) for x in xs],
        "selftest vacuous",
        verbose=verbose,
    )
    real = assert_cuts_small_exact(
        small_model,
        lambda model, xs: model.add(xs[0] < xs[1]),
        "selftest real",
        verbose=verbose,
    )

    domain = list(range(9))
    witness = audit_named_witnesses(
        lambda pair: pair[0] in domain and pair[1] in domain,
        lambda pair: pair[0] < pair[1],
        (8, 0),
        (0, 8),
        equivalent=lambda a, b: sorted(a) == sorted(b),
        label="selftest named witness",
    )
    orbit = audit_feasible_orbit(
        lambda pair: pair[0] != pair[1],
        lambda pair: pair[0] < pair[1],
        ((0, 1), (1, 0)),
        label="selftest orbit",
    )
    return (
        vacuous[0] is False
        and real[0] is True
        and witness.passed
        and orbit.passed
        and orbit.survives_cut == 1
    )


if __name__ == "__main__":
    raise SystemExit(0 if selftest() else 1)
