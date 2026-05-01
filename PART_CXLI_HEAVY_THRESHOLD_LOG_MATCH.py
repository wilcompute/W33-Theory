#!/usr/bin/env python3
"""
PART CXLI — Heavy-Threshold Log Match for the W(3,3) RG Window
==============================================================

Part CXL showed that the inverse RG target k3_eff sits between the two
structural W(3,3) rational candidates

    24/13 < k3_eff < 13/7

and that only sub-percent GUT thresholds are required to pin either rational
to the observed alpha_s(M_Z).

This module asks whether the required thresholds look like natural one-loop
heavy-threshold logarithms built out of W(3,3) invariants.

Threshold convention:

    alpha_s(M_GUT) = alpha_unified/k3_bare * (1 + delta_GUT)
    delta_GUT      = (alpha_unified/(2*pi)) * tau

where tau is the dimensionless threshold in natural loop units.

Core observation:

    For k3_bare = 24/13:
        tau_target = -0.280966506...
        log sqrt(mu/Phi6) = -1/2 log(7/4) = -0.279807894...
        residual delta = -7.38e-6   (k3 error ~ -7.4 ppm)

    For k3_bare = 13/7:
        tau_target = +0.652358888...
        log sqrt((k-1)/q) = +1/2 log(11/3) = +0.649641492...
        residual delta = +1.73e-5   (k3 error ~ +17.2 ppm)

This is not promoted as an exact theorem.  It is a strong diagnostic: the
required threshold size is exactly the scale of a single square-root mass
ratio built from the same W(3,3) invariants already selected by the Hashimoto
quadratic-field and QCD beta layers.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from PART_CXXXIX_RG_EMBEDDING_INVERSION import ALPHA_UNIFIED, solve_k3_for_target
from PART_CXL_RG_THRESHOLD_PINNING import delta_gut_for_candidate

ROOT = Path(__file__).resolve().parent

# W(3,3) atoms.
Q = 3
LAMBDA = 2
MU = 4
K = 12
V = 40
E = V * K // 2
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
ALPHA_INTEGER = (K - 1) ** 2 + MU**2


@dataclass(frozen=True)
class ThresholdTemplate:
    label: str
    bare_k3: float
    template: str
    target_loop_units: float
    template_loop_units: float
    loop_units_residual: float
    delta_gut_template: float
    delta_gut_target: float
    delta_residual: float
    effective_k3_from_template: float
    k3_error: float
    relative_k3_error_ppm: float


def loop_unit(alpha_unified: float = ALPHA_UNIFIED) -> float:
    return alpha_unified / (2.0 * math.pi)


def target_loop_units_for_candidate(k3_bare: float, k3_eff: float) -> float:
    return delta_gut_for_candidate(k3_bare, k3_eff) / loop_unit()


def evaluate_template(label: str, k3_bare: float, tau_template: float, template: str) -> ThresholdTemplate:
    k3_eff, _ = solve_k3_for_target()
    target_tau = target_loop_units_for_candidate(k3_bare, k3_eff)
    delta_template = loop_unit() * tau_template
    delta_target = loop_unit() * target_tau
    k3_from_template = k3_bare / (1.0 + delta_template)
    return ThresholdTemplate(
        label=label,
        bare_k3=k3_bare,
        template=template,
        target_loop_units=target_tau,
        template_loop_units=tau_template,
        loop_units_residual=target_tau - tau_template,
        delta_gut_template=delta_template,
        delta_gut_target=delta_target,
        delta_residual=delta_target - delta_template,
        effective_k3_from_template=k3_from_template,
        k3_error=k3_from_template - k3_eff,
        relative_k3_error_ppm=(k3_from_template / k3_eff - 1.0) * 1.0e6,
    )


def primitive_threshold_templates() -> List[ThresholdTemplate]:
    """Two field-primitively motivated square-root threshold templates."""
    return [
        evaluate_template(
            "24/13 primitive sqrt(mu/Phi6)",
            24 / 13,
            -0.5 * math.log(PHI6 / MU),
            "log sqrt(mu/Phi6) = -1/2 log(7/4)",
        ),
        evaluate_template(
            "13/7 primitive sqrt((k-1)/q)",
            PHI3 / PHI6,
            0.5 * math.log((K - 1) / Q),
            "log sqrt((k-1)/q) = +1/2 log(11/3)",
        ),
    ]


def catalog_atoms() -> Dict[str, int]:
    """Small W(3,3) atoms used by the threshold log scanner."""
    return {
        "q": Q,
        "mu": MU,
        "Phi6": PHI6,
        "Phi4": PHI4,
        "k-1": K - 1,
        "k": K,
        "Phi3": PHI3,
        "v-mu+1": V - MU + 1,
        "v": V,
        "E": E,
        "alpha_integer": ALPHA_INTEGER,
    }


def half_log_catalog_matches(k3_bare: float, max_results: int = 8) -> List[Dict[str, object]]:
    """Search half-log thresholds ±1/2 log(a/b) over W(3,3) atoms.

    Half-logs are natural because a heavy mass threshold often involves a
    mass ratio, while the Hashimoto sectors found in CXXXVIII are quadratic
    roots/square-root fields.
    """
    k3_eff, _ = solve_k3_for_target()
    target_tau = target_loop_units_for_candidate(k3_bare, k3_eff)
    atoms = catalog_atoms()
    rows: List[Dict[str, object]] = []
    items = list(atoms.items())
    for name_a, a in items:
        for name_b, b in items:
            if name_a == name_b or a <= 0 or b <= 0:
                continue
            tau = 0.5 * math.log(a / b)
            rows.append(
                {
                    "formula": f"1/2 log({name_a}/{name_b})",
                    "ratio": f"{a}/{b}",
                    "tau": tau,
                    "abs_residual": abs(target_tau - tau),
                    "signed_residual": target_tau - tau,
                }
            )
    rows.sort(key=lambda r: r["abs_residual"])
    return rows[:max_results]


def best_catalog_templates() -> List[ThresholdTemplate]:
    """Best W(3,3)-atom half-log matches found by the scanner."""
    return [
        evaluate_template(
            "24/13 best catalog sqrt(137/240)",
            24 / 13,
            -0.5 * math.log(E / ALPHA_INTEGER),
            "log sqrt(137/E) = -1/2 log(240/137)",
        ),
        evaluate_template(
            "13/7 best catalog sqrt((v-mu+1)/Phi4)",
            PHI3 / PHI6,
            0.5 * math.log((V - MU + 1) / PHI4),
            "log sqrt((v-mu+1)/Phi4) = +1/2 log(37/10)",
        ),
    ]


def heavy_threshold_log_match_audit() -> Dict[str, object]:
    k3_eff, alpha_star = solve_k3_for_target()
    primitives = primitive_threshold_templates()
    bests = best_catalog_templates()

    # The two primitive templates already pin the inverse k3 target at ppm scale.
    p24, p137 = primitives
    assert abs(p24.relative_k3_error_ppm) < 10.0
    assert abs(p137.relative_k3_error_ppm) < 20.0
    assert p24.delta_gut_template < 0.0
    assert p137.delta_gut_template > 0.0

    return {
        "module": "PART_CXLI_HEAVY_THRESHOLD_LOG_MATCH",
        "inputs": {
            "alpha_unified": ALPHA_UNIFIED,
            "loop_unit_alpha_over_2pi": loop_unit(),
            "k3_eff_from_CXXXIX": k3_eff,
            "alpha_s_MZ_at_k3_eff": alpha_star,
        },
        "w33_atoms": catalog_atoms(),
        "primitive_templates": [asdict(t) for t in primitives],
        "best_catalog_templates": [asdict(t) for t in bests],
        "scanner_top_matches": {
            "k3_24_over_13": half_log_catalog_matches(24 / 13, max_results=8),
            "k3_13_over_7": half_log_catalog_matches(PHI3 / PHI6, max_results=8),
        },
        "theorem_statement": (
            "The sub-percent GUT thresholds required by CXL are naturally of "
            "one-loop square-root-log size.  The structural templates "
            "log sqrt(mu/Phi6) for k3=24/13 and log sqrt((k-1)/q) for k3=13/7 "
            "pin the inverse k3 target to ppm-level accuracy in the effective "
            "embedding factor."
        ),
        "interpretive_note": (
            "This does not prove a heavy spectrum yet.  It narrows the search: "
            "derive a single quadratic-field threshold from the Hashimoto sectors, "
            "with mass ratio sqrt(mu/Phi6) on the 24/13 branch or sqrt((k-1)/q) "
            "on the 13/7 branch.  The scanner also finds very close catalog matches "
            "sqrt(137/E) and sqrt((v-mu+1)/Phi4), suggesting the threshold may be "
            "controlled by the interaction of the Gaussian alpha integer and the "
            "Phi4/Phi6 Hashimoto fields."
        ),
    }


def main() -> int:
    audit = heavy_threshold_log_match_audit()
    out = ROOT / "PART_CXLI_heavy_threshold_log_match_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
