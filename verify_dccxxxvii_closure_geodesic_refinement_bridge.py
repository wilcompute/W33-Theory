#!/usr/bin/env python3
"""Part DCCXXXVII: closure geodesic refinement bridge.

Builds on DCCXXXVI by introducing a quadratic micro-action on causal refinements.

For a causal history from T_a to T_b written as positive integer jumps
    Delta_tau = d_1 + ... + d_m,
we define the refinement action
    A_ref = d_1^2 + ... + d_m^2.

For fixed endpoints, A_ref is minimized exactly by the unit-step refinement
    (1,1,...,1),
which is the canonical monotone closure path.

This provides the first exact extremal principle in the closure-time chain.
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

from verify_dccxxxvi_closure_action_weight_bridge import build_bridge as build_dccxxxvi

OUT_PATH = ROOT / "data" / "dccxxxvii_closure_geodesic_refinement_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    total_proper_time_span: int
    canonical_step_count: int
    canonical_refinement_action: int
    coarse_one_jump_action: int
    extremal_gap: int
    all_identities_hold: bool


def compositions(n: int, max_part: int | None = None) -> list[list[int]]:
    if n <= 0:
        return [[]]
    if max_part is None:
        max_part = n
    out: list[list[int]] = []
    for first in range(1, min(max_part, n) + 1):
        for tail in compositions(n - first, max_part=n - first if n - first else 0):
            out.append([first, *tail])
    return out


def refinement_action(parts: list[int]) -> int:
    return sum(p * p for p in parts)


def build_bridge() -> dict[str, Any]:
    dccxxxvi = build_dccxxxvi()
    max_path = dccxxxvi["path_table"][0][-1]
    total_span = max_path["action"]

    refs = compositions(total_span)
    refinements = [
        {
            "partition": parts,
            "step_count": len(parts),
            "sum": sum(parts),
            "linear_action": sum(parts),
            "refinement_action": refinement_action(parts),
            "weight_denominator": 2 ** sum(parts),
        }
        for parts in refs
    ]

    min_action = min(item["refinement_action"] for item in refinements)
    minimizers = [item for item in refinements if item["refinement_action"] == min_action]
    canonical = next(item for item in minimizers if item["partition"] == [1, 1, 1, 1, 1])
    coarse = next(item for item in refinements if item["partition"] == [5])

    identities = {
        "all_refinements_preserve_endpoint_span": all(item["sum"] == total_span for item in refinements),
        "linear_action_is_endpoint_invariant": all(item["linear_action"] == total_span for item in refinements),
        "all_refinements_have_same_weight": all(item["weight_denominator"] == 2 ** total_span for item in refinements),
        "canonical_unit_refinement_exists": canonical["partition"] == [1, 1, 1, 1, 1],
        "canonical_refinement_minimizes_quadratic_action": len(minimizers) == 1 and canonical["refinement_action"] == total_span,
        "coarse_one_jump_has_larger_quadratic_action": coarse["refinement_action"] == total_span * total_span,
        "extremal_gap_is_20": coarse["refinement_action"] - canonical["refinement_action"] == 20,
    }

    summary = BridgeSummary(
        total_proper_time_span=total_span,
        canonical_step_count=canonical["step_count"],
        canonical_refinement_action=canonical["refinement_action"],
        coarse_one_jump_action=coarse["refinement_action"],
        extremal_gap=coarse["refinement_action"] - canonical["refinement_action"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "endpoint_data": {
            "from": 0,
            "to": 5,
            "total_span": total_span,
            "linear_action": total_span,
            "weight": {"numerator": 1, "denominator": 2 ** total_span},
        },
        "refinement_family": {
            "count": len(refinements),
            "all_refinements": refinements,
            "quadratic_action_definition": "A_ref = sum_i d_i^2 for positive integer jump refinement d_1+...+d_m = Delta_tau",
            "canonical_minimizer": canonical,
            "coarse_maximizer_example": coarse,
        },
        "bridge_claim": {
            "exact_layer": (
                "Among all causal refinements with fixed endpoints, the linear action and weight are endpoint invariants, but the quadratic refinement action is uniquely minimized by the unit-step monotone closure path."
            ),
            "conditional_layer": (
                "Interpreting this discrete extremal law as a continuum geodesic principle requires an additional continuum limiting argument."
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
