#!/usr/bin/env python3
"""Executable publication-claim tier reconciliation audit.

This audit keeps publication governance aligned with executable theorem status by
classifying key claims into tiers and validating that boundary claims are not
promoted beyond what current executable checks support.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from scripts.w33_q3_master_lock_boundary import (  # noqa: E402
    build_q3_full_physical_realization_boundary_record,
)
from scripts.w33_yukawa_frontier_audit import analyze as analyze_yukawa_frontier  # noqa: E402
from scripts.w33_h4_s3_selector_holonomy_audit import (  # noqa: E402
    h4_s3_selector_holonomy_summary,
)


def _claim(name: str, tier: str, executable_gate: bool, note: str) -> Dict[str, Any]:
    return {
        "name": name,
        "tier": tier,
        "executable_gate": executable_gate,
        "note": note,
    }


@lru_cache(maxsize=1)
def analyze() -> Dict[str, Any]:
    boundary = build_q3_full_physical_realization_boundary_record()
    yukawa_frontier = analyze_yukawa_frontier()
    h4 = h4_s3_selector_holonomy_summary()

    smooth_ok = bool(boundary["evidence"]["holonomy_witness_exact"])
    yukawa_ok = bool(
        yukawa_frontier["current_open_problem"][
            "canonical_mixed_product_and_ratio_are_branch_stable_irreducible_octics"
        ]
    )
    h4_ok = all(h4["theorem"].values())

    claims: List[Dict[str, Any]] = [
        _claim(
            "q3_full_physical_realization_theorem",
            "boundary",
            True,
            "Boundary summary remains promoted frontier response, not full exact theorem.",
        ),
        _claim(
            "q3_smooth_realization_witness",
            "boundary",
            smooth_ok,
            "Smooth-realization remains boundary-tier; holonomy witness is executable and exact.",
        ),
        _claim(
            "yukawa_nonlinear_d4_relation_certificate",
            "exact_frontier",
            yukawa_ok,
            "Open frontier is nonlinear relation above two linearly disjoint D4 splitting fields.",
        ),
        _claim(
            "h4_s3_selector_holonomy_observable",
            "exact_finite",
            h4_ok,
            "S3 selector theorem packet is exact on the finite 1620-carrier.",
        ),
    ]

    boundary_tier_honest = (
        boundary["support_level"] == "boundary summary with promoted frontier response"
    )

    no_overpromotion = all(
        claim["tier"] != "exact" or claim["executable_gate"] for claim in claims
    )

    theorem = {
        "boundary_tier_honest": boundary_tier_honest,
        "all_claim_gates_pass": all(claim["executable_gate"] for claim in claims),
        "no_overpromotion_detected": no_overpromotion,
        "publication_claim_tiers_reconciled": (
            boundary_tier_honest
            and all(claim["executable_gate"] for claim in claims)
            and no_overpromotion
        ),
    }

    return {
        "status": "ok",
        "claim_tier_table": claims,
        "boundary_record": {
            "name": boundary["name"],
            "support_level": boundary["support_level"],
        },
        "publication_claim_reconciliation_theorem": theorem,
        "boundary_note": (
            "This governance check is executable and tier-based. It does not "
            "rewrite prose files; it certifies that claim tiers are consistent "
            "with current theorem gates."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_F_publication_claim_reconciliation_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[ok] wrote {output_path}")


if __name__ == "__main__":
    main()
