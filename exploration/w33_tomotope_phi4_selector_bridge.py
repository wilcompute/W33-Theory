"""Resolve the live selector packet as a tomotope-versus-matter split.

The previous bridge derived the live CKM amplitudes exactly:

    a = 9/25,
    b = 3/80,
    sigma = 159/800,
    delta = 129/800,
    delta / sigma = 43/53.

The remaining question is whether the numerators 53 and 43 are merely
arithmetic shadows or whether they come from already-established carrier
objects.  They do.

Two exact packets were isolated much earlier:

    96 = |Aut(tomotope)| = mu * f,
    10 = Phi_4 = the exact matter-10 packet.

Then

    53 = (96 + 10)/2,
    43 = (96 - 10)/2,

so

    sigma = q(96 + 10) / (2 mu (q+lambda) v),
    delta = q(96 - 10) / (2 mu (q+lambda) v).

Equivalently,

    a = q*96 / (mu (q+lambda) v),
    b = q*10 / (mu (q+lambda) v),
    a / b = 96 / 10 = 48/5.

This is the cleanest current selector law: the live family/CP packet is the
normalized split of the tomotope automorphism packet against the matter-10
packet.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_tomotope_phi4_selector_bridge_summary.json"


Q = Fraction(3, 1)
LAMBDA = Fraction(2, 1)
MU = Fraction(4, 1)
V = Fraction(40, 1)
F_EULER = Fraction(24, 1)
PHI4 = Fraction(10, 1)

TOMOTOPE_ORDER = MU * F_EULER
A_CANON = Fraction(9, 25)
B_CANON = Fraction(3, 80)
SIGMA = (A_CANON + B_CANON) / 2
DELTA = (A_CANON - B_CANON) / 2
COMMON_DEN = MU * (Q + LAMBDA) * V


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _fraction_report(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "value": float(value)}


def build_summary() -> dict[str, Any]:
    tomotope = _load_json("w33_tomotope_semidirect_triality_bridge_summary.json")
    spectral = _load_json("w33_spectral_democracy.json")
    scalar = _load_json("w33_live_scalar_selector_bridge_summary.json")

    plus_packet = (TOMOTOPE_ORDER + PHI4) / 2
    minus_packet = (TOMOTOPE_ORDER - PHI4) / 2

    sigma_forms = {
        "q_times_tomotope_plus_phi4_over_2mu_branch_v": Q * (TOMOTOPE_ORDER + PHI4) / (2 * COMMON_DEN),
        "q_times_53_over_mu_branch_v": Q * plus_packet / COMMON_DEN,
    }
    delta_forms = {
        "q_times_tomotope_minus_phi4_over_2mu_branch_v": Q * (TOMOTOPE_ORDER - PHI4) / (2 * COMMON_DEN),
        "q_times_43_over_mu_branch_v": Q * minus_packet / COMMON_DEN,
    }
    a_forms = {
        "q_times_tomotope_order_over_mu_branch_v": Q * TOMOTOPE_ORDER / COMMON_DEN,
        "qf_over_branch_v": Q * F_EULER / ((Q + LAMBDA) * V),
    }
    b_forms = {
        "q_times_phi4_over_mu_branch_v": Q * PHI4 / COMMON_DEN,
        "canonical_b": B_CANON,
    }

    return {
        "primitive_packets": {
            "tomotope_order_96": _fraction_report(TOMOTOPE_ORDER),
            "matter_phi4_10": _fraction_report(PHI4),
            "plus_packet_53": _fraction_report(plus_packet),
            "minus_packet_43": _fraction_report(minus_packet),
        },
        "live_selector_dictionary": {
            "a": _fraction_report(A_CANON),
            "b": _fraction_report(B_CANON),
            "sigma": _fraction_report(SIGMA),
            "delta": _fraction_report(DELTA),
            "a_over_b": _fraction_report(A_CANON / B_CANON),
            "sigma_over_delta": _fraction_report(SIGMA / DELTA),
            "sigma_forms": {name: _fraction_report(value) for name, value in sigma_forms.items()},
            "delta_forms": {name: _fraction_report(value) for name, value in delta_forms.items()},
            "a_forms": {name: _fraction_report(value) for name, value in a_forms.items()},
            "b_forms": {name: _fraction_report(value) for name, value in b_forms.items()},
        },
        "cross_checks": {
            "tomotope_order_matches_committed_order_96": (
                tomotope["group_packet"]["order"] == int(TOMOTOPE_ORDER)
            ),
            "matter_packet_matches_committed_phi4_10": (
                spectral["MULTIPLICITIES"]["m1"] == "Phi4 = q^2+1 = 10"
            ),
            "live_scalar_bridge_sigma_is_the_plus_split": (
                scalar["triality_packet_scalars"]["sigma_half_sum"]["exact"] == str(SIGMA)
                and all(value == SIGMA for value in sigma_forms.values())
            ),
            "live_scalar_bridge_delta_is_the_minus_split": (
                scalar["triality_packet_scalars"]["delta_half_difference"]["exact"] == str(DELTA)
                and all(value == DELTA for value in delta_forms.values())
            ),
        },
        "tomotope_phi4_selector_theorem": {
            "the_live_cabibbo_cp_amplitude_is_exactly_the_normalized_tomotope_packet": (
                all(value == A_CANON for value in a_forms.values())
            ),
            "the_live_vcb_lift_amplitude_is_exactly_the_normalized_matter_phi4_packet": (
                all(value == B_CANON for value in b_forms.values())
            ),
            "the_live_triality_half_sum_is_exactly_the_plus_split_of_96_and_10": (
                plus_packet == 53 and all(value == SIGMA for value in sigma_forms.values())
            ),
            "the_live_triality_half_difference_is_exactly_the_minus_split_of_96_and_10": (
                minus_packet == 43 and all(value == DELTA for value in delta_forms.values())
            ),
            "the_live_amplitude_ratio_is_exactly_tomotope_over_matter_96_over_10": (
                A_CANON / B_CANON == TOMOTOPE_ORDER / PHI4
            ),
            "the_live_selector_packet_is_the_symmetric_antisymmetric_split_of_tomotope_and_matter": (
                A_CANON == SIGMA + DELTA and B_CANON == SIGMA - DELTA
            ),
        },
        "interpretation": (
            "The live selector packet is now anchored to two exact old objects. "
            "The first edge amplitude a is the normalized tomotope automorphism "
            "packet 96 = mu f, while the second edge amplitude b is the normalized "
            "matter packet Phi_4 = 10. The triality half-sum and half-difference "
            "then become the plus and minus packets 53 and 43. So the live family/CP "
            "carrier is the symmetric/antisymmetric split of tomotope-96 against "
            "matter-10, not an isolated late-stage fit."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    theorem = summary["tomotope_phi4_selector_theorem"]

    print("=" * 72)
    print("W33 TOMOTOPE/PHI4 SELECTOR BRIDGE")
    print("=" * 72)
    print(f"96 = |Aut(tomotope)| = mu*f = {TOMOTOPE_ORDER}")
    print(f"10 = Phi4 = {PHI4}")
    print(f"53 = (96+10)/2 = {(TOMOTOPE_ORDER + PHI4) / 2}")
    print(f"43 = (96-10)/2 = {(TOMOTOPE_ORDER - PHI4) / 2}")
    print(f"a/b = {A_CANON / B_CANON}")
    print()
    print("Selector theorem:")
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
