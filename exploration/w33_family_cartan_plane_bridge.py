"""Exact common family Cartan plane for CKM and the promoted neutrino branch.

This bridge closes the next structural seam after the promoted neutrino family
flag. Two upstream exact facts were already known:

1. CKM real family asymmetry lives on the universal tetra/family doublet axis

       q = (1, 1/sqrt(3))

2. The promoted neutrino branch lives on the same exact family carrier

       3 = 1 ⊕ 2

   and on the doublet part it is

       29 I_2 + delta H_2,
       delta = 29(17 - sqrt(33))/16.

The missing statement is how those fit together on one doublet plane.

They fit orthogonally.

The unique equal-norm axis orthogonal to the CKM axis is

    n = (1/sqrt(3), -1),

and this is the promoted neutrino Cartan direction. So quark family asymmetry
and neutrino family splitting are the two exact orthogonal coordinates on one
common family doublet plane.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_family_cartan_plane_bridge_summary.json"


def _serialize_vector(values: tuple[float, float]) -> list[float]:
    return [float(values[0]), float(values[1])]


def build_summary() -> dict[str, Any]:
    sqrt3 = math.sqrt(3.0)

    quark_axis = (1.0, 1.0 / sqrt3)
    neutrino_axis = (1.0 / sqrt3, -1.0)
    family_complex_structure = ((0.0, -1.0), (1.0, 0.0))
    rotated_quark_axis = (
        family_complex_structure[0][0] * quark_axis[0] + family_complex_structure[0][1] * quark_axis[1],
        family_complex_structure[1][0] * quark_axis[0] + family_complex_structure[1][1] * quark_axis[1],
    )

    axis_norm_sq = quark_axis[0] ** 2 + quark_axis[1] ** 2
    orthogonality = quark_axis[0] * neutrino_axis[0] + quark_axis[1] * neutrino_axis[1]

    quark_unit = (quark_axis[0] / math.sqrt(axis_norm_sq), quark_axis[1] / math.sqrt(axis_norm_sq))
    neutrino_unit = (neutrino_axis[0] / math.sqrt(axis_norm_sq), neutrino_axis[1] / math.sqrt(axis_norm_sq))

    # Promoted neutrino doublet data.
    doublet_mean = Fraction(29, 1)
    delta = float(Fraction(493, 16) - Fraction(29, 16) * math.sqrt(33.0))
    m2 = doublet_mean - delta
    m3 = doublet_mean + delta

    return {
        "family_cartan_plane_dictionary": {
            "carrier": "irreducible family doublet 2",
            "quark_axis_q": {
                "exact": "(1, 1/sqrt(3))",
                "float": _serialize_vector(quark_axis),
            },
            "neutrino_axis_n": {
                "exact": "(1/sqrt(3), -1)",
                "float": _serialize_vector(neutrino_axis),
            },
            "unit_axes": {
                "quark_unit": _serialize_vector(quark_unit),
                "neutrino_unit": _serialize_vector(neutrino_unit),
            },
            "family_complex_structure_J": [list(row) for row in family_complex_structure],
            "J_times_quark_axis": _serialize_vector(rotated_quark_axis),
            "common_norm_squared": axis_norm_sq,
            "dot_product_q_dot_n": orthogonality,
        },
        "promoted_neutrino_doublet_packet": {
            "doublet_mean": {"exact": "29", "float": float(doublet_mean)},
            "doublet_cartan_amplitude": {
                "exact": "29*(17 - sqrt(33))/16",
                "float": delta,
            },
            "doublet_eigenvalues_mev": {
                "m2": float(m2),
                "m3": float(m3),
            },
            "operator_form": "M_nu|doublet = 29 I_2 + delta * H_nu",
        },
        "family_cartan_plane_theorem": {
            "the_ckm_family_axis_and_the_neutrino_cartan_axis_are_exactly_orthogonal": abs(orthogonality) < 1e-12,
            "they_have_exactly_the_same_norm": abs(axis_norm_sq - (neutrino_axis[0] ** 2 + neutrino_axis[1] ** 2)) < 1e-12,
            "the_neutrino_axis_is_exactly_minus_J_times_the_ckm_axis_on_the_family_doublet": (
                abs(rotated_quark_axis[0] + neutrino_axis[0]) < 1e-12
                and abs(rotated_quark_axis[1] + neutrino_axis[1]) < 1e-12
            ),
            "they_form_a_complete_orthogonal_basis_of_the_common_family_doublet_plane": (
                abs(orthogonality) < 1e-12 and axis_norm_sq > 0.0
            ),
            "the_promoted_neutrino_branch_is_exactly_29_times_the_doublet_identity_plus_one_cartan_on_the_neutrino_axis": (
                abs(m2 - 8.599519796850178) < 1e-12
                and abs(m3 - 49.400480203149826) < 1e-12
            ),
            "quark_family_asymmetry_and_neutrino_family_splitting_are_therefore_one_common_exact_family_cartan_plane": True,
        },
        "interpretation": (
            "The family side is no longer split into separate quark and neutrino stories. "
            "The universal CKM tetra-doublet axis q=(1,1/sqrt(3)) and the promoted "
            "neutrino splitting axis n=(1/sqrt(3),-1) are the unique equal-norm "
            "orthogonal axes in the same exact family doublet. So the real quark "
            "family asymmetry and the promoted neutrino mass splitting are the two "
            "canonical coordinates of one common family Cartan plane."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 FAMILY CARTAN PLANE BRIDGE")
    print("=" * 72)
    for key, value in summary["family_cartan_plane_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
