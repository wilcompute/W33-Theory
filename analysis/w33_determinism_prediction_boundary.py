#!/usr/bin/env python3
"""Determinism / prediction boundary for the HoloVM two-counter core.

The VM transition relation is deterministic. This script demonstrates the
correct operational predictor: bounded simulation is a one-sided semidecision
procedure.

If HALT is reached within fuel, report HALTS. If fuel is exhausted, report
UNKNOWN -- never NONHALT. For every tested fuel bound F, a program that halts
after more than F steps is a finite counterexample to interpreting fuel
exhaustion as non-halting.

The stronger all-program boundary is reduction-theoretic: the repository's
two-counter core is a universal abstract machine, so a total algorithm deciding
HALT/NONHALT for every finite program/state would decide the halting problem.
"""
import json
from pathlib import Path

from w33_typed_universal_microvm import (
    Capability,
    Carrier,
    Instruction,
    Program,
    TypedUniversalMicroVM,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_DETERMINISM_PREDICTION_BOUNDARY.json"


def delayed_halt(delay):
    if delay < 0:
        raise ValueError("delay")
    rows = []
    for i in range(delay):
        rows.append(Instruction("INC", 0, target=i + 1))
    rows.append(Instruction("HALT"))
    return Program(tuple(rows), name=f"delayed-halt-{delay}")


def forever():
    return Program((Instruction("INC", 0, target=0),), name="forever-inc")


def bounded_halting_semidecider(program, fuel):
    cap = Capability(Carrier.CIRCUIT_ST81, 81)
    vm = TypedUniversalMicroVM(program, cap)
    try:
        final = vm.run(fuel=fuel)
    except RuntimeError as exc:
        if str(exc) != "fuel exhausted":
            raise
        return {"verdict": "UNKNOWN", "steps": fuel}
    return {"verdict": "HALTS", "steps": final.steps}


def verify():
    immediate = bounded_halting_semidecider(delayed_halt(0), 1)
    assert immediate["verdict"] == "HALTS"

    horizon_rows = []
    for fuel in range(1, 17):
        p = delayed_halt(fuel + 2)
        short = bounded_halting_semidecider(p, fuel)
        long = bounded_halting_semidecider(p, 4 * fuel + 16)
        assert short["verdict"] == "UNKNOWN"
        assert long["verdict"] == "HALTS"
        horizon_rows.append({
            "fuel": fuel,
            "program": p.name,
            "bounded_verdict": short["verdict"],
            "eventual_verdict_with_more_fuel": long["verdict"],
            "eventual_steps": long["steps"],
        })

    loop_rows = []
    p_loop = forever()
    for fuel in (1, 2, 4, 8, 16, 32, 64):
        row = bounded_halting_semidecider(p_loop, fuel)
        assert row["verdict"] == "UNKNOWN"
        loop_rows.append({"fuel": fuel, **row})

    return {
        "schema": "w33.determinism-prediction-boundary.v1",
        "status": "PASS",
        "deterministic_transition_semantics": True,
        "bounded_predictor": "HALTS-or-UNKNOWN semidecider",
        "finite_horizon_counterexamples": horizon_rows,
        "known_diverger_bounded_results": loop_rows,
        "never_infer_nonhalt_from_fuel_exhaustion": True,
        "universal_boundary": {
            "repository_core": "finite INC/DECJZ/HALT two-counter programs with unbounded natural counters",
            "bridge": "analysis/w33_static_holoir_counter_bridge.py",
            "statement": (
                "Under ordinary Turing-computability assumptions, if a total algorithm decided "
                "whether every encoded HoloVM two-counter execution eventually reaches HALT, "
                "it would decide the halting problem. Therefore deterministic laws do not imply "
                "a universal prediction oracle."
            ),
        },
        "separation": [
            "deterministic transition law",
            "state knowledge",
            "computable prediction for a particular instance",
            "efficient prediction",
            "total all-instance decidability",
        ],
        "boundary": (
            "The executable part proves only the finite-fuel semidecision discipline and its "
            "counterexamples. The no-total-predictor statement is the standard computability "
            "consequence of the already-implemented universal two-counter semantics."
        ),
    }


if __name__ == "__main__":
    result = verify()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
