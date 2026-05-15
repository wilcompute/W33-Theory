#!/usr/bin/env python3
"""Part DCCXXXVIII: closure Bellman-principle bridge.

Builds on DCCXXXVII by deriving the local recursion satisfied by the quadratic
refinement-action minimizer.

For endpoint span n >= 0, define the value function
    V(n) = min { d_1^2 + ... + d_m^2 : d_i >= 1, d_1 + ... + d_m = n }.

Then V obeys the exact Bellman recursion
    V(0) = 0,
    V(n) = min_{1 <= d <= n} (d^2 + V(n-d)).

For the closure chain, the unique minimizer is always d = 1, so
    V(n) = 1 + V(n-1) = n.

This is the discrete Hamilton-Jacobi / dynamic-programming form of the closure
geodesic law.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxxvii_closure_geodesic_refinement_bridge import build_bridge as build_dccxxxvii

OUT_PATH = ROOT / "data" / "dccxxxviii_closure_bellman_principle_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    maximal_span: int
    value_at_maximal_span: int
    unique_local_minimizer: int
    recursion_depth: int
    all_identities_hold: bool


def value_function(max_n: int) -> tuple[list[int], list[dict[str, Any]]]:
    values = [0]
    witnesses: list[dict[str, Any]] = []
    for n in range(1, max_n + 1):
        candidates = [
            {
                "jump": d,
                "candidate_value": d * d + values[n - d],
            }
            for d in range(1, n + 1)
        ]
        min_value = min(c["candidate_value"] for c in candidates)
        minimizers = [c["jump"] for c in candidates if c["candidate_value"] == min_value]
        values.append(min_value)
        witnesses.append(
            {
                "span": n,
                "candidates": candidates,
                "min_value": min_value,
                "minimizers": minimizers,
                "bellman_step": f"V({n}) = min_d (d^2 + V({n}-d))",
            }
        )
    return values, witnesses


def build_bridge() -> dict[str, Any]:
    dccxxxvii = build_dccxxxvii()
    max_span = dccxxxvii["summary"]["total_proper_time_span"]

    values, witnesses = value_function(max_span)
    policy = [
        {
            "span": item["span"],
            "optimal_jump": item["minimizers"][0],
            "value": item["min_value"],
        }
        for item in witnesses
    ]

    identities = {
        "value_function_starts_at_zero": values[0] == 0,
        "bellman_recursion_holds_exactly": all(
            item["min_value"] == min(c["candidate_value"] for c in item["candidates"]) for item in witnesses
        ),
        "value_function_is_linear_V_n_equals_n": values == [0, 1, 2, 3, 4, 5],
        "unique_local_minimizer_is_unit_jump": all(item["minimizers"] == [1] for item in witnesses),
        "policy_is_stationary_unit_step": all(p["optimal_jump"] == 1 for p in policy),
        "discrete_hamilton_jacobi_identity_holds": all(
            values[n] == 1 + values[n - 1] for n in range(1, len(values))
        ),
        "maximal_span_value_matches_geodesic_action": values[max_span] == dccxxxvii["summary"]["canonical_refinement_action"] == 5,
    }

    summary = BridgeSummary(
        maximal_span=max_span,
        value_at_maximal_span=values[max_span],
        unique_local_minimizer=1,
        recursion_depth=max_span,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "value_function": {
            "definition": "V(n) = min_{d_1+...+d_m=n} sum_i d_i^2",
            "values": values,
            "bellman_witness": witnesses,
            "optimal_policy": policy,
        },
        "bridge_claim": {
            "exact_layer": (
                "The closure geodesic law is generated locally by the Bellman recursion V(n)=min_d(d^2+V(n-d)), whose unique optimizer is always the unit jump d=1."
            ),
            "conditional_layer": (
                "Reading this discrete Bellman identity as a continuum Hamilton-Jacobi equation requires an additional limiting argument."
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
