#!/usr/bin/env python3
"""
PART CXL — RG Threshold Pinning of the W(3,3) k3 Rational Window
================================================================

Part CXXXIX inverted the corrected two-loop QCD RG map and found

    k3_eff = 1.849461957...

for alpha_unified=1/25 and M_GUT=(13/7)*1e16 GeV.

This module answers the next question:

    If W(3,3) wants a finite rational k3 such as 24/13 or 13/7,
    how large a GUT-scale threshold correction is needed to pin that
    rational to the inverse target?

Conventions:
    alpha_s(M_GUT) = alpha_unified/k3_bare * (1 + delta_GUT)

and k3_eff is defined by
    alpha_s(M_GUT) = alpha_unified/k3_eff.

Therefore
    delta_GUT(k3_bare -> k3_eff) = k3_bare/k3_eff - 1.

Key result:
    k3 = 24/13 needs delta_GUT = -0.0017895...  (-0.179%)
    k3 = 13/7  needs delta_GUT = +0.0041530...  (+0.415%)

So the two most structural W(3,3) rational candidates straddle the inverse
target, and each can be pinned to the observed alpha_s(M_Z) by a sub-percent
GUT threshold.  That is the real RG target now: derive this threshold from
the field-labeled Hashimoto/E8 sector, not fit it as a free parameter.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

from PART_CXXXIX_RG_EMBEDDING_INVERSION import (
    ALPHA_UNIFIED,
    PDG_ALPHA_S_MZ,
    PDG_SIGMA,
    alpha_s_mz_from_k3,
    solve_k3_for_target,
)

ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class ThresholdCandidate:
    label: str
    k3_bare: float
    alpha_s_mz_without_threshold: float | None
    sigma_without_threshold: float | None
    delta_gut_to_target: float
    delta_percent: float
    effective_k3_after_threshold: float
    natural_loop_units: float


def delta_gut_for_candidate(k3_bare: float, k3_eff: float) -> float:
    """Return delta such that alpha_un/k3_bare*(1+delta)=alpha_un/k3_eff."""
    return (k3_bare / k3_eff) - 1.0


def natural_loop_units(delta: float, alpha_unified: float = ALPHA_UNIFIED) -> float:
    """Express a threshold as delta / (alpha_unified/(2*pi))."""
    return delta / (alpha_unified / (2.0 * math.pi))


def evaluate_threshold_candidate(label: str, k3_bare: float, k3_eff: float) -> ThresholdCandidate:
    alpha_no = alpha_s_mz_from_k3(k3_bare)
    sigma = None if alpha_no is None else (alpha_no - PDG_ALPHA_S_MZ) / PDG_SIGMA
    delta = delta_gut_for_candidate(k3_bare, k3_eff)
    return ThresholdCandidate(
        label=label,
        k3_bare=k3_bare,
        alpha_s_mz_without_threshold=alpha_no,
        sigma_without_threshold=sigma,
        delta_gut_to_target=delta,
        delta_percent=100.0 * delta,
        effective_k3_after_threshold=k3_eff,
        natural_loop_units=natural_loop_units(delta),
    )


def threshold_candidates() -> List[ThresholdCandidate]:
    k3_eff, _ = solve_k3_for_target()
    raw = [
        ("24/13 = 2k/Phi3", 24 / 13),
        ("37/20", 37 / 20),
        ("50/27", 50 / 27),
        ("13/7 = Phi3/Phi6", 13 / 7),
    ]
    return [evaluate_threshold_candidate(label, value, k3_eff) for label, value in raw]


def required_heavy_log(delta: float, alpha_unified: float = ALPHA_UNIFIED) -> float:
    """A dimensionless proxy for a one-loop heavy threshold log.

    In many one-loop matching formulas, threshold shifts appear as
        delta ~ (alpha/(2*pi)) * C * log(M_H/M_GUT).

    With C=1 this function returns the log-size needed.  It is not a claim
    about a specific heavy spectrum; it is a naturalness gauge.
    """
    return natural_loop_units(delta, alpha_unified)


def rg_threshold_pinning_audit() -> Dict[str, object]:
    k3_eff, alpha_star = solve_k3_for_target()
    candidates = threshold_candidates()

    by_label = {c.label: c for c in candidates}
    c_24 = by_label["24/13 = 2k/Phi3"]
    c_137 = by_label["13/7 = Phi3/Phi6"]

    assert abs(alpha_star - PDG_ALPHA_S_MZ) < 1e-10
    assert abs(c_24.delta_percent) < 0.25
    assert abs(c_137.delta_percent) < 0.50
    assert c_24.delta_gut_to_target < 0
    assert c_137.delta_gut_to_target > 0

    return {
        "module": "PART_CXL_RG_THRESHOLD_PINNING",
        "inputs": {
            "alpha_unified": ALPHA_UNIFIED,
            "target_alpha_s_MZ": PDG_ALPHA_S_MZ,
            "pdg_sigma": PDG_SIGMA,
            "k3_eff_from_CXXXIX": k3_eff,
            "alpha_s_MZ_at_k3_eff": alpha_star,
            "threshold_convention": "alpha_s(M_GUT)=alpha_unified/k3_bare*(1+delta_GUT)",
            "delta_formula": "delta_GUT = k3_bare/k3_eff - 1",
        },
        "threshold_candidates": [asdict(c) for c in candidates],
        "pinning_window": {
            "lower_structural_candidate": "24/13",
            "upper_structural_candidate": "13/7",
            "k3_eff_lies_between": (24 / 13) < k3_eff < (13 / 7),
            "delta_24_over_13_percent": c_24.delta_percent,
            "delta_13_over_7_percent": c_137.delta_percent,
            "threshold_span_percent": c_137.delta_percent - c_24.delta_percent,
        },
        "theorem_statement": (
            "The inverse RG target k3_eff≈1.849461957 lies between the two "
            "structural W(3,3) rationals 24/13 and 13/7.  Pinning either "
            "rational to the observed alpha_s(M_Z) requires only a sub-percent "
            "GUT threshold: -0.179% for 24/13 or +0.415% for 13/7 under the "
            "minimal two-loop convention."
        ),
        "interpretive_note": (
            "This turns the RG problem into a small-threshold derivation problem. "
            "The W(3,3) finite geometry should not fit k3_eff as a real number; "
            "it should select a rational bare embedding such as 24/13 or 13/7, "
            "then derive the sign and size of delta_GUT from the heavy E8/"
            "Hashimoto field sectors."
        ),
    }


def main() -> int:
    audit = rg_threshold_pinning_audit()
    out = ROOT / "PART_CXL_rg_threshold_pinning_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
