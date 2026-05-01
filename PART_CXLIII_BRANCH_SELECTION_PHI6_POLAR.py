#!/usr/bin/env python3
"""
PART CXLIII — Branch Selection: the Phi6-Polar QCD Threshold
============================================================

CXLII reduced the RG embedding problem to two ppm-close branches:

  A. Phi6-polar branch:
       k3_bare = 24/13,  tau = log sqrt(mu/Phi6)

  B. global radial/q-clock branch:
       k3_bare = 13/7,   tau = log sqrt((k-1)/q)

Both are numerically good.  This audit gives the finite-selection rule.

Selection principle:
    The correction being pinned is the SU(3)_c / QCD threshold.  Therefore
    the heavy threshold should be localized in the same finite sector that
    carries the QCD beta atom beta0 = Phi6(3) = 7.

CXXXVIII/CXLII show that this sector is the negative Hashimoto field

    x = -2 ± i sqrt(Phi6) = -2 ± i sqrt(7),

whose real/imaginary polar ratio is exactly sqrt(mu/Phi6).

The 13/7 branch is elegant but global: it uses the universal Ramanujan radius
sqrt(k-1) divided by the q-clock sqrt(q).  That is an Ihara-shell threshold,
not a color-local Phi6 threshold.

Conclusion:
    The QCD-specific branch selected by sector locality is

        k3_bare = 24/13,
        tau_GUT = log sqrt(mu/Phi6),
        k3_eff_template = 1.849448291286928,

    leaving only a -7.39 ppm residual relative to the inverse RG target.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

from PART_CXLII_HASHIMOTO_HEAVY_SPECTRUM_DERIVATION import (
    PHI3,
    PHI6,
    derived_threshold_branches,
    hashimoto_field_sectors,
)

ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class BranchScore:
    branch_label: str
    bare_k3: float
    threshold_tau_source: str
    relative_k3_error_ppm: float
    qcd_beta0_locality: int
    uses_phi6_field: int
    uses_color_specific_polar_ratio: int
    uses_global_radial_clock: int
    branch_score: int
    decision: str


def score_branches() -> List[BranchScore]:
    """Score the two CXLII branches by color-locality criteria.

    A branch earns points for:
      1. being in the Phi6 field carrying beta0=Phi6,
      2. using the Phi6 field explicitly,
      3. using a polar real/imaginary ratio of that field.

    The global radial/q-clock threshold is not wrong; it is simply not
    color-local, so it does not earn QCD-locality points here.
    """
    scores: List[BranchScore] = []
    for branch in derived_threshold_branches():
        is_phi6_polar = "Phi6-sector polar" in branch.branch_label
        is_radial = "Ramanujan radial" in branch.branch_label
        qcd_locality = 1 if is_phi6_polar else 0
        uses_phi6 = 1 if ("Phi6" in branch.tau_source or "sqrt(mu/Phi6)" in branch.tau_source) else 0
        uses_polar = 1 if "Re" in branch.tau_source and "Im" in branch.tau_source else 0
        uses_radial = 1 if is_radial else 0
        score = qcd_locality + uses_phi6 + uses_polar - uses_radial
        scores.append(
            BranchScore(
                branch_label=branch.branch_label,
                bare_k3=branch.bare_k3,
                threshold_tau_source=branch.tau_source,
                relative_k3_error_ppm=branch.relative_k3_error_ppm,
                qcd_beta0_locality=qcd_locality,
                uses_phi6_field=uses_phi6,
                uses_color_specific_polar_ratio=uses_polar,
                uses_global_radial_clock=uses_radial,
                branch_score=score,
                decision="SELECTED" if is_phi6_polar else "REJECTED_FOR_QCD_THRESHOLD",
            )
        )
    return scores


def selected_branch() -> BranchScore:
    scores = score_branches()
    return max(scores, key=lambda s: s.branch_score)


def branch_selection_audit() -> Dict[str, object]:
    sectors = hashimoto_field_sectors()
    scores = score_branches()
    selected = selected_branch()

    # Regression-grade selection checks.
    assert selected.branch_label == "24/13 branch from Phi6-sector polar ratio"
    assert selected.bare_k3 == 24 / PHI3
    assert abs(selected.relative_k3_error_ppm) < 10.0
    assert selected.branch_score > 0
    assert all(s.branch_score < selected.branch_score for s in scores if s.branch_label != selected.branch_label)

    return {
        "module": "PART_CXLIII_BRANCH_SELECTION_PHI6_POLAR",
        "selection_principle": (
            "Because the RG correction is an SU(3)_c/QCD threshold, the selected "
            "branch must be localized in the Phi6 sector carrying beta0=Phi6(3)=7, "
            "not merely in the global Ihara/Ramanujan shell."
        ),
        "qcd_beta_atom": {
            "beta0": PHI6,
            "formula": "beta0 = Phi6(3) = q^2-q+1 = 7",
            "sector": "negative Hashimoto field Q(sqrt(-Phi6)) from x=-2±i√7",
        },
        "field_sectors": [asdict(s) for s in sectors],
        "branch_scores": [asdict(s) for s in scores],
        "selected_branch": asdict(selected),
        "selected_effective_model": {
            "k3_bare": "24/13",
            "threshold_tau": "log sqrt(mu/Phi6)",
            "threshold_source": "Phi6-sector polar ratio |Re(-2+i√7)|/|Im(-2+i√7)|",
            "status": "QCD-local selected branch; ppm residual remains as multi-heavy/precision correction target",
        },
        "rejected_branch_note": (
            "The 13/7 branch is not discarded mathematically; it is rejected only "
            "as the QCD-local threshold because its source is the global Ramanujan "
            "radius over the q-clock, not the Phi6 color sector.  It remains useful "
            "as an Ihara-clock/universal threshold candidate."
        ),
        "theorem_statement": (
            "Sector-locality selects the Phi6-polar branch: the QCD beta atom "
            "beta0=Phi6 lives in the negative Hashimoto field x=-2±i√Phi6, "
            "and the corresponding polar ratio gives tau=log sqrt(mu/Phi6) "
            "with bare k3=24/13."
        ),
    }


def main() -> int:
    audit = branch_selection_audit()
    out = ROOT / "PART_CXLIII_branch_selection_phi6_polar_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
