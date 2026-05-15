#!/usr/bin/env python3
"""Part DCCXXXI: loop-closure clock bridge.

Formalizes the user insight:
- 3 points are the minimum for loop closure (triangle boundary),
- closure introduces a 4th object (the bounded face / closure channel),
- repeated closure events define a monotone discrete clock parameter.

This part is intentionally discrete and exact; interpretation as physical time
remains a conditional bridge claim.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxiv_loop_closure_origin import Q as Q_DCCXXIV, QP1 as QP1_DCCXXIV
from verify_dccxxx_clifford_even_quaternion_pauli_bridge import build_bridge as build_dccxxx

OUT_PATH = ROOT / "data" / "dccxxxi_loop_closure_clock_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    minimum_loop_vertices: int
    closure_channel_dimension: int
    quaternion_basis_dimension: int
    clock_steps: int
    final_clock_value: int
    all_identities_hold: bool


def closure_event_sequence(length: int = 7) -> list[int]:
    """Deterministic closure events in {0,1}.

    A 1 denotes an achieved loop-closure update; 0 denotes a non-closing step.
    This sequence is fixed so the theorem artifact is reproducible.
    """
    base = [1, 0, 1, 1, 0, 1, 1]
    if length <= len(base):
        return base[:length]
    # periodic extension if ever needed.
    reps = (length + len(base) - 1) // len(base)
    seq = (base * reps)[:length]
    return seq


def discrete_clock(events: Iterable[int]) -> list[int]:
    """Cumulative closure clock tau_n = sum_{i<=n} events_i."""
    tau = []
    total = 0
    for e in events:
        if e not in (0, 1):
            raise ValueError("Events must be binary closure indicators")
        total += e
        tau.append(total)
    return tau


def build_bridge() -> dict[str, Any]:
    dccxxx = build_dccxxx()

    events = closure_event_sequence(7)
    tau = discrete_clock(events)

    identities = {
        "dccxxiv_minimum_loop_is_three": Q_DCCXXIV == 3,
        "closure_adds_fourth_channel_at_count_level": QP1_DCCXXIV == 4 and Q_DCCXXIV + 1 == QP1_DCCXXIV,
        "dccxxx_clifford_even_basis_is_dimension_four": (
            dccxxx["summary"]["quaternion_basis_count"] == 4
            and dccxxx["summary"]["ternary_bivector_count"] == 3
        ),
        "closure_event_sequence_is_binary": all(e in (0, 1) for e in events),
        "clock_is_monotone_non_decreasing": all(tau[i] <= tau[i + 1] for i in range(len(tau) - 1)),
        "clock_increment_equals_event": all((tau[i] - (tau[i - 1] if i else 0)) == events[i] for i in range(len(tau))),
        "clock_advances_on_every_closure_event": sum(events) == tau[-1] == len([e for e in events if e == 1]),
    }

    summary = BridgeSummary(
        minimum_loop_vertices=Q_DCCXXIV,
        closure_channel_dimension=QP1_DCCXXIV,
        quaternion_basis_dimension=dccxxx["summary"]["quaternion_basis_count"],
        clock_steps=len(events),
        final_clock_value=tau[-1],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "loop_closure": {
            "q": Q_DCCXXIV,
            "q_plus_1": QP1_DCCXXIV,
            "statement": "Three points close the minimal loop; closure yields a fourth channel (the face/closure cell).",
        },
        "clock_model": {
            "events": events,
            "tau": tau,
            "definition": "tau_n = cumulative sum of closure-event indicators",
        },
        "clifford_link": {
            "even_basis": dccxxx["clifford_even_subalgebra"]["basis"],
            "quaternion_map": dccxxx["quaternion_realization"]["map"],
        },
        "bridge_claim": {
            "exact_layer": (
                "Discrete closure events induce a canonical monotone clock parameter in the closure channel."
            ),
            "conditional_layer": (
                "Interpreting this discrete clock as physical time requires additional dynamical/continuum assumptions."
            ),
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
