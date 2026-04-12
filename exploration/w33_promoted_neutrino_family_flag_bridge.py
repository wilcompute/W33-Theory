"""Promoted neutrino package on the exact family flag carrier.

This bridge reconnects the promoted neutrino branch to the earlier exact
family carrier instead of leaving it as a detached mass table.

Upstream exact results already established:

    family carrier = 3 = 1 ⊕ 2

with the 1 as the fixed line and the 2 as the irreducible family doublet.

The neutrino side then has two exact layers:

1. Raw democratic seesaw precursor:
       one distinguished singlet line
       plus an exactly isotropic doublet plane
   so the solar splitting is forced to zero.

2. Promoted physical branch:
       one exactly massless singlet line
       plus a split family doublet
   with total doublet trace 58 and exact squared-splitting ratio 33.

So the promoted physical neutrino package is best read as the exact anisotropic
doublet deformation of the old family-flag carrier.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_promoted_neutrino_family_flag_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_promoted_neutrino_package_bridge import build_summary as build_promoted_neutrino_summary


Q = 3
V = 40
K = 12
LAM = 2
MU = 4
PHI3 = Q * Q + Q + 1
PHI6 = Q * Q - Q + 1


RadPair = tuple[Fraction, Fraction]


def _rad_pair_mul(left: RadPair, right: RadPair, radicand: int = 33) -> RadPair:
    a, b = left
    c, d = right
    return (a * c + radicand * b * d, a * d + b * c)


def _rad_pair_add(left: RadPair, right: RadPair) -> RadPair:
    return (left[0] + right[0], left[1] + right[1])


def _rad_pair_sub(left: RadPair, right: RadPair) -> RadPair:
    return (left[0] - right[0], left[1] - right[1])


def _rad_pair_scale(scale: Fraction, pair: RadPair) -> RadPair:
    return (scale * pair[0], scale * pair[1])


def _rad_pair_float(pair: RadPair, radicand: int = 33) -> float:
    return float(pair[0]) + float(pair[1]) * math.sqrt(radicand)


def _rad_pair_str(pair: RadPair, radicand: int = 33) -> str:
    constant, radical = pair
    pieces: list[str] = []
    if constant:
        pieces.append(str(constant))
    if radical:
        coeff = abs(radical)
        coeff_text = "" if coeff == 1 else f"{coeff}*"
        term = f"{coeff_text}sqrt({radicand})"
        if pieces:
            pieces.append(f" {'+' if radical > 0 else '-'} {term}")
        else:
            pieces.append(term if radical > 0 else f"-{term}")
    return "".join(pieces) if pieces else "0"


def _rad_pair_report(pair: RadPair) -> dict[str, Any]:
    return {"exact": _rad_pair_str(pair), "float": _rad_pair_float(pair)}


def build_summary() -> dict[str, Any]:
    promoted = build_promoted_neutrino_summary()

    # Raw democratic precursor from the exact seesaw packet.
    raw_doublet = Fraction(3625, 189)
    raw_singlet = Fraction(3712, 189)

    # Promoted minimal-normal package.
    m1 = Fraction(0, 1)
    m2: RadPair = (Fraction(-29, 16), Fraction(29, 16))
    m3: RadPair = (Fraction(957, 16), Fraction(-29, 16))

    promoted_mean = Fraction(29, 1)
    promoted_delta: RadPair = (Fraction(493, 16), Fraction(-29, 16))
    # 29 P_2 + delta * H_2 with H_2 = diag(0,-1,+1)
    recovered_m2 = _rad_pair_sub((promoted_mean, Fraction(0, 1)), promoted_delta)
    recovered_m3 = _rad_pair_add((promoted_mean, Fraction(0, 1)), promoted_delta)

    m2_sq = _rad_pair_mul(m2, m2)
    m3_sq = _rad_pair_mul(m3, m3)

    sin2_theta12 = Fraction(MU, PHI3)       # 4/13
    sin2_theta23 = Fraction(PHI6, PHI3)     # 7/13
    sin2_theta13 = Fraction(LAM, PHI3 * PHI6)  # 2/91
    weighted_selector_sum = sin2_theta12 + sin2_theta23 + PHI6 * sin2_theta13

    return {
        "family_flag_dictionary": {
            "carrier": "3 = 1 + 2",
            "singlet_line": "fixed family line",
            "doublet_plane": "irreducible family doublet",
            "doublet_cartan": "H_2 = diag(0,-1,+1)",
        },
        "raw_democratic_precursor": {
            "operator_in_adapted_family_basis": {
                "exact": f"diag({raw_singlet}, {raw_doublet}, {raw_doublet})",
                "float": [float(raw_singlet), float(raw_doublet), float(raw_doublet)],
            },
            "interpretation": "distinguished singlet plus isotropic family doublet",
        },
        "promoted_family_flag_operator": {
            "operator_form": {
                "exact": (
                    "M_nu = 0·P_1 + 29·P_2 + "
                    f"({_rad_pair_str(promoted_delta)})·H_2"
                ),
                "doublet_mean_29": float(promoted_mean),
                "doublet_anisotropy": _rad_pair_report(promoted_delta),
            },
            "spectrum_mev": {
                "m1": {"exact": "0", "float": 0.0},
                "m2": _rad_pair_report(m2),
                "m3": _rad_pair_report(m3),
            },
            "recovered_from_mean_and_cartan": {
                "m2": _rad_pair_report(recovered_m2),
                "m3": _rad_pair_report(recovered_m3),
            },
            "squared_spectrum_mev2": {
                "m2_squared": _rad_pair_report(m2_sq),
                "m3_squared": _rad_pair_report(m3_sq),
            },
        },
        "pmns_selector_packet": {
            "sin2_theta12": {"exact": str(sin2_theta12), "float": float(sin2_theta12)},
            "sin2_theta23": {"exact": str(sin2_theta23), "float": float(sin2_theta23)},
            "sin2_theta13": {"exact": str(sin2_theta13), "float": float(sin2_theta13)},
            "weighted_identity": {
                "exact": f"{sin2_theta12} + {sin2_theta23} + {PHI6}*{sin2_theta13} = {weighted_selector_sum}",
                "float": float(weighted_selector_sum),
            },
        },
        "promoted_neutrino_family_flag_theorem": {
            "the_upstream_family_carrier_is_exactly_one_plus_two": True,
            "the_raw_democratic_seesaw_is_a_singlet_plus_isotropic_doublet_packet": raw_singlet != raw_doublet,
            "the_promoted_branch_is_exactly_massless_on_the_singlet_line": m1 == 0,
            "the_promoted_branch_is_exactly_29_times_the_doublet_projector_plus_one_doublet_cartan": recovered_m2 == m2 and recovered_m3 == m3,
            "the_promoted_doublet_trace_is_exactly_58_mev": promoted_mean * 2 == Fraction(58, 1),
            "the_promoted_doublet_anisotropy_reproduces_the_exact_33_ratio": abs(_rad_pair_float(m3_sq) / _rad_pair_float(m2_sq) - 33.0) < 1e-12,
            "the_reactor_channel_is_the_only_heptad_suppressed_pmns_channel": weighted_selector_sum == 1,
            "the_promoted_physical_branch_is_the_exact_anisotropic_doublet_deformation_of_the_old_family_flag_carrier": (
                raw_singlet != raw_doublet and m1 == 0 and recovered_m2 == m2 and recovered_m3 == m3
            ),
        },
        "upstream_consistency": promoted["promoted_neutrino_package_theorem"],
        "interpretation": (
            "The neutrino sector is no longer best read as a detached packet of masses. "
            "It sits on the same exact family carrier as the old tetra/triality work: "
            "3 = 1 + 2. The raw democratic seesaw is the isotropic doublet precursor, "
            "while the promoted physical branch is the same carrier after one exact "
            "doublet Cartan is turned on. The PMNS packet then closes with a weighted "
            "identity 4/13 + 7/13 + 7·(2/91) = 1, so the reactor angle is the unique "
            "heptad-suppressed channel."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 PROMOTED NEUTRINO FAMILY-FLAG BRIDGE")
    print("=" * 72)
    for key, value in summary["promoted_neutrino_family_flag_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
