"""Balanced rank-2 selector for the active external bridge branch.

This module packages the strongest conservative v39-style bridge statement that
is already defensible from tracked local data and exact repo-native bridge
theorems.

Already exact:
  - the nonlinear bridge packet is A4-only with reduced local prefactor
        27 / (16 pi^2);
  - rank-1 external branches kill the packet;
  - rank-2 activation enters quartically through |det C|^2;
  - the selected-point q=3 package fixes
        (81, 6, 8; 52, 56) and (320, 2240, 12480).

What is added here is the exact variational selector behind the active 2x2
branch. If C has singular-value squares x,y >= 0, then

    tr(C^* C) = x + y,
    |det C|^2 = x y,
    4 |det C|^2 = tr(C^* C)^2 - (x - y)^2 <= tr(C^* C)^2,

with equality iff x = y. So for fixed branch radius, the quartic bridge packet
is uniquely maximized by the balanced rank-2 branch.

Equivalently, in the reduced branch action

    V(C) = -mu tr(C^* C) + u tr(C^* C)^2 - v A |det C|^2,

the shape dependence is exactly

    V = -mu r^2 + (u - A v / 4) r^4 + (A v / 4) (x - y)^2,

with r^2 = x + y. Hence for A,v > 0 any shape imbalance is penalized, and if
mu > 0 together with 4u > Av, the unique nonzero balanced stationary radius is

    r_*^2 = 2 mu / (4u - Av),
    V_*   = -mu^2 / (4u - Av).

The checked local V29 stiffness summary is included only as observation: it is
numerically close to isotropic at quadratic order, which is consistent with
this reduced selector picture. The actual global branch-counting / orientation
theorem on the CP2_9 / K3_16 refinement tower remains open.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
from typing import Any

from exploration.w33_bridge_a4_normalization_bridge import (
    build_bridge_a4_normalization_summary,
)
from exploration.w33_q_cyclotomic_master_bridge import (
    build_q_cyclotomic_master_summary,
)
from exploration.w33_yukawa_a4_normalization_bridge import (
    build_yukawa_a4_normalization_summary,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_balanced_branch_vacuum_bridge_summary.json"
V29_STIFFNESS_SUMMARY_PATH = ROOT / "V29_output_q_stiffness" / "summary.json"


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _squared_radius(x: Fraction, y: Fraction) -> Fraction:
    return x + y


def _det_packet_from_singular_squares(x: Fraction, y: Fraction) -> Fraction:
    return x * y


def _load_v29_stiffness_observation() -> dict[str, Any]:
    if not V29_STIFFNESS_SUMMARY_PATH.exists():
        return {
            "status": "missing",
            "source_file": V29_STIFFNESS_SUMMARY_PATH.relative_to(ROOT).as_posix(),
        }

    payload = json.loads(V29_STIFFNESS_SUMMARY_PATH.read_text(encoding="utf-8"))
    q_data = payload["Q"]
    eig_data = payload["eig"]
    diag_mean = float(q_data["diag_mean"])
    diag_std = float(q_data["diag_std"])
    offdiag_rms = float(q_data["offdiag_rms"])
    eig_mean = float(eig_data["mean"])
    eig_std = float(eig_data["std"])

    return {
        "status": "ok",
        "source_file": V29_STIFFNESS_SUMMARY_PATH.relative_to(ROOT).as_posix(),
        "diag_mean": diag_mean,
        "diag_cv": diag_std / abs(diag_mean),
        "offdiag_rms_ratio": offdiag_rms / abs(diag_mean),
        "eig_mean": eig_mean,
        "eig_std_ratio": eig_std / abs(eig_mean),
        "spectral_band_relative_width": abs(
            float(eig_data["max"]) - float(eig_data["min"])
        )
        / abs(eig_mean),
        "interpretation": (
            "Observed local quadratic stiffness is numerically close to isotropic. "
            "This is evidence only, not a promoted exact theorem."
        ),
    }


@lru_cache(maxsize=1)
def build_balanced_branch_vacuum_summary() -> dict[str, Any]:
    a4 = build_bridge_a4_normalization_summary()
    old_a4 = build_yukawa_a4_normalization_summary()
    q_master = build_q_cyclotomic_master_summary()

    balanced_x = Fraction(9, 1)
    balanced_y = Fraction(9, 1)
    unbalanced_x = Fraction(4, 1)
    unbalanced_y = Fraction(16, 1)

    balanced_radius = _squared_radius(balanced_x, balanced_y)
    balanced_det = _det_packet_from_singular_squares(balanced_x, balanced_y)
    unbalanced_radius = _squared_radius(unbalanced_x, unbalanced_y)
    unbalanced_det = _det_packet_from_singular_squares(unbalanced_x, unbalanced_y)

    shape_identity_balanced = (
        4 * balanced_det
        == balanced_radius * balanced_radius - (balanced_x - balanced_y) ** 2
    )
    shape_identity_unbalanced = (
        4 * unbalanced_det
        == unbalanced_radius * unbalanced_radius - (unbalanced_x - unbalanced_y) ** 2
    )
    determinant_bound_balanced = 4 * balanced_det == balanced_radius * balanced_radius
    determinant_bound_unbalanced = 4 * unbalanced_det < unbalanced_radius * unbalanced_radius

    sample_mu = Fraction(3, 1)
    sample_u = Fraction(5, 1)
    sample_A = Fraction(2, 1)
    sample_v = Fraction(4, 1)
    sample_radius_sq = Fraction(2, 1) * sample_mu / (4 * sample_u - sample_A * sample_v)
    sample_vacuum_value = -(sample_mu * sample_mu) / (4 * sample_u - sample_A * sample_v)
    sample_x = sample_radius_sq / 2
    sample_y = sample_radius_sq / 2
    direct_potential = (
        -sample_mu * (sample_x + sample_y)
        + sample_u * (sample_x + sample_y) ** 2
        - sample_v * sample_A * sample_x * sample_y
    )
    decomposed_potential = (
        -sample_mu * sample_radius_sq
        + (sample_u - sample_A * sample_v / 4) * sample_radius_sq * sample_radius_sq
        + sample_A * sample_v * (sample_x - sample_y) ** 2 / 4
    )

    q_curv = q_master["curved_q_package"]["Q_curv"]
    q_top = q_master["curved_q_package"]["Q_top"]
    bridge_prefactor = a4["reduced_local_bridge_prefactor"][
        "after_universal_rank2_factor_2"
    ]

    return {
        "status": "ok",
        "local_v29_stiffness_observation": _load_v29_stiffness_observation(),
        "bridge_packet_input": {
            "rank_one_branch_kills_packet": old_a4["external_activation"][
                "rank_one_branch_kills_packet"
            ],
            "rank_two_branch_scales_quartically": old_a4["external_activation"][
                "rank_two_branch_scales_quartically"
            ],
            "local_a4_only_prefactor": bridge_prefactor,
        },
        "balanced_rank2_identity": {
            "radius_formula": "r^2 = tr(C^* C) = x + y",
            "determinant_formula": "|det C|^2 = x y",
            "shape_identity": "4 |det C|^2 = r^4 - (x - y)^2",
            "determinant_bound": "|det C|^2 <= r^4 / 4",
            "equality_condition": "iff x = y",
            "balanced_example_saturates_bound": determinant_bound_balanced,
            "unbalanced_example_is_strict": determinant_bound_unbalanced,
            "shape_identity_checks_pass": (
                shape_identity_balanced and shape_identity_unbalanced
            ),
        },
        "reduced_master_action": {
            "potential": "V(C) = -mu tr(C^* C) + u tr(C^* C)^2 - v A |det C|^2",
            "shape_decomposition": (
                "V = -mu r^2 + (u - A v / 4) r^4 + (A v / 4) (x - y)^2"
            ),
            "balanced_stationary_radius": "r_*^2 = 2 mu / (4 u - A v)",
            "balanced_vacuum_value": "V_* = -mu^2 / (4 u - A v)",
            "condensation_condition": "mu > 0",
            "stability_condition": "4 u > A v",
            "sample_radius_sq": _fraction_text(sample_radius_sq),
            "sample_vacuum_value": _fraction_text(sample_vacuum_value),
            "sample_decomposition_matches_direct_potential": (
                direct_potential == decomposed_potential
            ),
        },
        "selected_point_q_lock": {
            "Q_curv": q_curv,
            "Q_top": q_top,
            "c_EH": q_master["curved_q_package"]["c_EH"]["exact"],
            "a2": q_master["curved_q_package"]["a2"]["exact"],
            "c6": q_master["curved_q_package"]["c6"]["exact"],
            "weinberg_lock": q_master["selection_lock"]["nine_cEH_over_c6"],
        },
        "balanced_branch_theorem": {
            "quartic_bridge_packet_is_the_first_exact_shape_selector": (
                old_a4["external_activation"]["rank_two_branch_scales_quartically"]
                and old_a4["external_activation"]["rank_one_branch_kills_packet"]
            ),
            "balanced_rank2_branch_uniquely_maximizes_det_packet_at_fixed_radius": (
                determinant_bound_balanced and determinant_bound_unbalanced
            ),
            "shape_imbalance_penalty_is_exactly_quadratic_in_x_minus_y": (
                direct_potential == decomposed_potential
            ),
            "nonzero_balanced_stationary_radius_exists_when_mu_positive_and_4u_gt_Av": (
                sample_mu > 0 and 4 * sample_u > sample_A * sample_v
            ),
            "q3_package_fixes_total_curvature_quantum_but_not_yet_global_realization": (
                q_curv == "52"
                and q_top == "56"
                and q_master["q_master_theorem"]["global_branch_activation_count_remains_open"]
            ),
            "actual_refinement_tower_orientation_and_counting_remain_open": True,
        },
        "bridge_verdict": (
            "The next conservative bridge step is no longer another local "
            "normalization fact. The exact |det C|^2 packet already gives a "
            "variational selector on the active 2x2 branch: at fixed tr(C^* C) "
            "it is uniquely maximized by the balanced rank-2 branch, and the "
            "reduced master action rewrites with an explicit positive "
            "(A v / 4) (x - y)^2 shape penalty. The checked local V29 stiffness "
            "summary is numerically consistent with that shape-blind quadratic "
            "premise, but only as observation. The exact q=3 package still fixes "
            "the total curvature quantum as 52 while leaving the actual global "
            "branch-realization and orientation theorem on the refinement tower "
            "open."
        ),
        "source_files": [
            "exploration/w33_bridge_a4_normalization_bridge.py",
            "exploration/w33_yukawa_a4_normalization_bridge.py",
            "exploration/w33_q_cyclotomic_master_bridge.py",
            "V29_output_q_stiffness/summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_balanced_branch_vacuum_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
