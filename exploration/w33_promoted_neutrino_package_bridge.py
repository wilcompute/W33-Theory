"""Promoted exact neutrino package from the committed W33 spine.

This bridge tightens the neutrino side rather than adding another detached
identity. The repo already contains four exact promoted inputs:

1. Sum rule:
       Sigma m_nu = lambda * (v - k + 1) = 58 meV
2. Splitting ratio:
       Delta m^2_31 / Delta m^2_21 = |Vieta_2| = 33 = 2 Phi_3 + Phi_6
3. PMNS packet:
       sin^2(theta_12) = mu / Phi_3  = 4/13
       sin^2(theta_23) = Phi_6/Phi_3 = 7/13
       sin^2(theta_13) = lambda/(Phi_3 Phi_6) = 2/91
4. Z_3 Majorana phases:
       alpha_21 = 2 pi / 3
       alpha_31 = 4 pi / 3

If the promoted physical branch is the minimal normal branch (lightest state
set to zero), then the masses and the neutrinoless-double-beta packet are
fixed exactly. This also makes the standing inconsistency honest:

the earlier exact democratic seesaw texture reproduces the 58 meV sum, but its
solar splitting is exactly zero, so it cannot be the promoted physical flavor
package.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_promoted_neutrino_package_bridge_summary.json"


Q = 3
V = 40
K = 12
LAM = 2
MU = 4
PHI3 = Q * Q + Q + 1
PHI6 = Q * Q - Q + 1

SIGMA_MEV = Fraction(LAM * (V - K + 1), 1)  # 58
RATIO31 = Fraction(2 * PHI3 + PHI6, 1)      # 33
RATIO32 = RATIO31 - 1                        # 32 on the minimal NH branch

SIN2_THETA12 = Fraction(MU, PHI3)            # 4/13
SIN2_THETA23 = Fraction(PHI6, PHI3)          # 7/13
SIN2_THETA13 = Fraction(LAM, PHI3 * PHI6)    # 2/91
COS2_THETA13 = 1 - SIN2_THETA13              # 89/91


RadPair = tuple[Fraction, Fraction]


def _fraction_dict(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "float": float(value)}


def _rad_pair_add(left: RadPair, right: RadPair) -> RadPair:
    return (left[0] + right[0], left[1] + right[1])


def _rad_pair_sub(left: RadPair, right: RadPair) -> RadPair:
    return (left[0] - right[0], left[1] - right[1])


def _rad_pair_mul(left: RadPair, right: RadPair, radicand: int = 33) -> RadPair:
    a, b = left
    c, d = right
    return (a * c + radicand * b * d, a * d + b * c)


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
        coeff_text = "" if coeff == 1 else str(coeff) + "*"
        term = f"{coeff_text}sqrt({radicand})"
        if pieces:
            sign = "+" if radical > 0 else "-"
            pieces.append(f" {sign} {term}")
        else:
            pieces.append(term if radical > 0 else f"-{term}")
    if not pieces:
        return "0"
    return "".join(pieces)


def _rad_pair_report(pair: RadPair) -> dict[str, Any]:
    return {"exact": _rad_pair_str(pair), "float": _rad_pair_float(pair)}


def build_summary() -> dict[str, Any]:
    audit_packet = (Fraction(4, 13), Fraction(7, 13), Fraction(2, 91))

    # Minimal normal hierarchy with m1 = 0 and Delta m^2_31 / Delta m^2_21 = 33.
    m1 = Fraction(0, 1)
    m2 = (Fraction(-29, 16), Fraction(29, 16))    # 29( sqrt(33) - 1 ) / 16
    m3 = (Fraction(957, 16), Fraction(-29, 16))   # 29( 33 - sqrt(33) ) / 16

    m2_sq = _rad_pair_mul(m2, m2)
    m3_sq = _rad_pair_mul(m3, m3)
    sigma_pair = _rad_pair_add((m1, Fraction(0, 1)), _rad_pair_add(m2, m3))

    delta21 = m2_sq
    delta31 = m3_sq
    delta32 = _rad_pair_sub(m3_sq, m2_sq)

    # Effective electron-neutrino mass m_beta^2 = sum |U_ei|^2 m_i^2.
    m_beta_sq = _rad_pair_add(
        _rad_pair_scale(SIN2_THETA12 * COS2_THETA13, m2_sq),
        _rad_pair_scale(SIN2_THETA13, m3_sq),
    )
    m_beta = math.sqrt(_rad_pair_float(m_beta_sq))

    # Majorana packet with alpha_21 = 2pi/3, alpha_31 = 4pi/3.
    a_coeff = SIN2_THETA12 * COS2_THETA13  # 356 / 1183
    b_coeff = SIN2_THETA13                 # 2 / 91
    a_line = _rad_pair_scale(a_coeff, m2)
    b_line = _rad_pair_scale(b_coeff, m3)
    # |A e^{2pi i / 3} + B e^{4pi i / 3}|^2 = A^2 + B^2 - AB
    m_bb_sq = _rad_pair_sub(
        _rad_pair_add(_rad_pair_mul(a_line, a_line), _rad_pair_mul(b_line, b_line)),
        _rad_pair_mul(a_line, b_line),
    )
    m_bb = math.sqrt(_rad_pair_float(m_bb_sq))

    # Earlier exact democratic seesaw packet: same total sum, zero solar split.
    raw_scale = Fraction(5 * LAM * (V - K + 1), 189)  # 290 / 189 meV
    raw_m12 = Fraction(25, 2) * raw_scale
    raw_m3 = Fraction(64, 5) * raw_scale
    raw_sigma = 2 * raw_m12 + raw_m3
    raw_delta21 = Fraction(0, 1)
    raw_delta31 = raw_m3 * raw_m3 - raw_m12 * raw_m12

    return {
        "status": "ok",
        "committed_exact_inputs": {
            "sum_rule_mev": _fraction_dict(SIGMA_MEV),
            "splitting_ratio_delta31_over_delta21": _fraction_dict(RATIO31),
            "splitting_ratio_delta32_over_delta21_on_minimal_normal_branch": _fraction_dict(RATIO32),
            "pmns_packet": {
                "sin2_theta12": _fraction_dict(SIN2_THETA12),
                "sin2_theta23": _fraction_dict(SIN2_THETA23),
                "sin2_theta13": _fraction_dict(SIN2_THETA13),
            },
            "z3_majorana_phases": {
                "alpha21_over_pi": _fraction_dict(Fraction(2, 3)),
                "alpha31_over_pi": _fraction_dict(Fraction(4, 3)),
            },
        },
        "promoted_minimal_normal_package": {
            "masses_mev": {
                "m1": _fraction_dict(m1),
                "m2": _rad_pair_report(m2),
                "m3": _rad_pair_report(m3),
            },
            "sum_rule_check": _rad_pair_report(sigma_pair),
            "squared_splittings_mev2": {
                "delta21": _rad_pair_report(delta21),
                "delta31": _rad_pair_report(delta31),
                "delta32": _rad_pair_report(delta32),
            },
            "effective_masses_mev": {
                "m_beta_squared": _rad_pair_report(m_beta_sq),
                "m_beta": {"float": m_beta},
                "m_beta_beta_squared": _rad_pair_report(m_bb_sq),
                "m_beta_beta": {"float": m_bb},
            },
        },
        "raw_democratic_seesaw_precursor": {
            "light_packet_mev": {
                "m1_raw": _fraction_dict(raw_m12),
                "m2_raw": _fraction_dict(raw_m12),
                "m3_raw": _fraction_dict(raw_m3),
            },
            "sum_rule_mev": _fraction_dict(raw_sigma),
            "squared_splittings_mev2": {
                "delta21_raw": _fraction_dict(raw_delta21),
                "delta31_raw": _fraction_dict(raw_delta31),
            },
        },
        "promoted_neutrino_package_theorem": {
            "pmns_audit_matches_mu_phi3_phi6_packet": audit_packet == (SIN2_THETA12, SIN2_THETA23, SIN2_THETA13),
            "promoted_sum_rule_is_exact": _rad_pair_sub(sigma_pair, (SIGMA_MEV, Fraction(0, 1))) == (0, 0),
            "promoted_delta31_over_delta21_is_exactly_33": _rad_pair_sub(delta31, _rad_pair_scale(RATIO31, delta21)) == (0, 0),
            "minimal_normal_branch_forces_delta32_over_delta21_to_be_32_not_33": _rad_pair_sub(delta32, _rad_pair_scale(RATIO32, delta21)) == (0, 0),
            "z3_majorana_packet_gives_sub_3_mev_mbeta_beta": 2.0 < m_bb < 3.0,
            "raw_democratic_seesaw_keeps_the_exact_sum_but_has_zero_solar_split": raw_sigma == SIGMA_MEV and raw_delta21 == 0,
            "raw_democratic_seesaw_therefore_cannot_be_the_promoted_physical_flavor_package": raw_delta21 == 0 and _rad_pair_float(delta21) > 0.0,
        },
        "interpretation": (
            "The promoted neutrino sector is now best read as the minimal normal "
            "branch selected by the exact sum 58 meV, the exact Vieta ratio 33, "
            "the exact PMNS packet 4/13, 7/13, 2/91, and the Z3 Majorana phases "
            "2pi/3 and 4pi/3. On that branch the masses, the corrected ratio "
            "Delta m^2_32 / Delta m^2_21 = 32, and the neutrinoless-double-beta "
            "packet all follow exactly. The earlier exact democratic seesaw "
            "texture still matters, but only as an unsplit precursor: it keeps "
            "the same 58 meV sum while forcing the solar splitting to zero, so it "
            "cannot be the final promoted physical flavor package."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    theorem = summary["promoted_neutrino_package_theorem"]
    print("=" * 72)
    print("W33 PROMOTED NEUTRINO PACKAGE BRIDGE")
    print("=" * 72)
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
