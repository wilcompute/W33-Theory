"""Exact scalar/operator laws for the CKM family doublet and CP bivector split.

This bridge closes the main remaining ambiguity in the current tetra/Clifford
picture.  The previous modules already showed where the live and paper CKM
operators *live*:

- family asymmetry on the tetrahedral doublet inside Sym^2(4),
- CP on the bivector shell Lambda^2(4) = 3 + 3'.

The new step is to derive the actual scalar strengths from the operator stack
instead of reading them off from projector norms after the fact.

The key laws are:

1. Family doublet law

   On the canonical tetra doublet basis, both the live family envelope and the
   paper real asymmetry lie on the *same universal axis*

       (1, 1/sqrt(3)).

   Their only difference is the scalar in front:

       live scalar  = -(1 - a b) / 2,
       paper scalar = (d22 - u22 - a12 d32) / 4
                    = (1/(2 Phi_6) - q/(v-q) - 1/(v q)) / 4.

   So the paper family asymmetry is the same family-doublet axis, but with a
   weaker operator-selected coefficient.  The extra `1/(v q)` term is the exact
   real cross-term between the Cabibbo leg `q^2/v` and the down-only injector
   `1/q^3`.

2. CP bivector law

   In the canonical mode split

       4 = 1 + 3,

   write a packet as `c = (u, s)` with scalar mode `u` and standard mode
   `s in C^3`.  Then the bivector shell decomposes canonically as

       Lambda^2(4) = (1 ^ 3) + Lambda^2(3) = 3 + 3'

   with exact operators

       3  :  B = Im(u * conj(s))      (line-shell interference),
       3' :  W = Re(s) x Im(s)        (shell self-wedge).

   For the live packet, these become

       ||B||   = sqrt(2 sigma^2 + 4 delta^2),
       ||W||   = sqrt(2) sigma,

   where sigma=(a+b)/2 and delta=(a-b)/2.
"""

from __future__ import annotations

from fractions import Fraction
import json
from math import sqrt
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_ckm_operator_scalar_law_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_ckm_family_doublet_axis_bridge import _doublet_basis
from exploration.w33_ckm_clifford_sector_separation_bridge import _build_irrep_projectors
from exploration.w33_tetrahedral_ckm_oscillator_bridge import (
    _paper_up_down_vectors,
    _tetra_fourier_matrix,
    _two_edge_vector,
)


Q = Fraction(3, 1)
V = Fraction(40, 1)
PHI6 = Fraction(7, 1)
A12 = Q**2 / V
U22 = Q / (V - Q)
D22 = Fraction(1, 1) / (2 * PHI6)
D32 = Fraction(1, 1) / (Q**3)


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _sym_coords(matrix: np.ndarray) -> np.ndarray:
    basis = [(i, j) for i in range(4) for j in range(i, 4)]
    return np.array([matrix[i, j] for i, j in basis], dtype=float)


def _doublet_coordinates(matrix: np.ndarray) -> np.ndarray:
    basis = _doublet_basis()
    return basis.T @ _sym_coords(matrix)


def _mode_coordinates(vector: np.ndarray) -> np.ndarray:
    return np.conjugate(_tetra_fourier_matrix()).T @ vector


def _bivector_split_from_modes(vector: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    coordinates = _mode_coordinates(vector)
    scalar_mode = coordinates[0]
    standard_mode = coordinates[1:]
    triplet = np.imag(scalar_mode * np.conjugate(standard_mode))
    twisted_triplet = np.cross(standard_mode.real, standard_mode.imag)
    return triplet, twisted_triplet


def _serialize_float_vector(values: np.ndarray) -> list[float]:
    return [float(value) for value in values]


def build_summary() -> dict[str, Any]:
    quarter_turn = _load_json("w33_quarter_turn_quark_sheet_bridge_summary.json")
    lift = _load_json("w33_two_sheet_ckm_lift_bridge_summary.json")
    ckm_sectors = _load_json("w33_ckm_clifford_sector_separation_bridge_summary.json")

    live_a = float(quarter_turn["refined_q11_q21_quarter_turn_family"]["best_error"]["amplitude"])
    live_b = float(lift["second_layer_lift_edge"]["amplitude"])
    sigma = (live_a + live_b) / 2.0
    delta = (live_a - live_b) / 2.0
    live_vector = _two_edge_vector(live_a, live_b)

    paper_up, paper_down = _paper_up_down_vectors()

    live_sym = np.outer(live_vector, np.conjugate(live_vector)).real
    paper_real_asym = (
        np.outer(paper_up, np.conjugate(paper_up)).real
        - np.outer(paper_down, np.conjugate(paper_down)).real
    ) / 2.0

    live_doublet = _doublet_coordinates(live_sym)
    paper_doublet = _doublet_coordinates(paper_real_asym)
    universal_axis = np.array([1.0, 1.0 / sqrt(3.0)])

    live_scalar = -(1.0 - live_a * live_b) / 2.0
    paper_scalar_exact = (D22 - U22 - A12 * D32) / 4
    paper_scalar = float(paper_scalar_exact)

    live_triplet, live_twisted_triplet = _bivector_split_from_modes(live_vector)
    up_triplet, up_twisted_triplet = _bivector_split_from_modes(paper_up)
    down_triplet, down_twisted_triplet = _bivector_split_from_modes(paper_down)

    live_triplet_formula_norm = sqrt(2.0 * sigma * sigma + 4.0 * delta * delta)
    live_twisted_formula_norm = sqrt(2.0) * abs(sigma)

    up_beta = float(U22)
    down_beta = float(D22)
    t = float(A12)
    s = float(D32)
    up_triplet_formula_norm = t * sqrt((1.0 + up_beta + up_beta * up_beta) / 2.0)
    up_twisted_formula_norm = t * sqrt((1.0 - up_beta + up_beta * up_beta) / 2.0)
    down_triplet_formula_norm = sqrt(
        ((down_beta * t + s) / 2.0) ** 2
        + (((1.0 + down_beta) * (t - s)) / 2.0) ** 2
        + ((t + down_beta * s) / 2.0) ** 2
    )
    down_twisted_formula_norm = sqrt(
        ((down_beta * t + s) / 2.0) ** 2
        + (((1.0 - down_beta) * (t + s)) / 2.0) ** 2
        + ((t + down_beta * s) / 2.0) ** 2
    )

    return {
        "family_doublet_law": {
            "universal_doublet_axis": [float(value) for value in universal_axis],
            "live_doublet_coordinates": _serialize_float_vector(live_doublet),
            "paper_doublet_coordinates": _serialize_float_vector(paper_doublet),
            "live_scalar_formula": {
                "expression": "-(1 - a b) / 2",
                "value": live_scalar,
            },
            "paper_scalar_formula": {
                "expression": "(d22 - u22 - a12*d32) / 4 = (1/(2Phi6) - q/(v-q) - 1/(vq)) / 4",
                "exact_value": str(paper_scalar_exact),
                "value": paper_scalar,
            },
            "paper_cross_term_dictionary": {
                "real_dressing_difference": str(D22 - U22),
                "cabibbo_injector_cross_term": str(A12 * D32),
                "full_scalar_numerator_before_dividing_by_4": str(D22 - U22 - A12 * D32),
            },
        },
        "cp_bivector_law": {
            "general_dictionary": {
                "mode_split": "4 = 1 + 3",
                "triplet_3": "B = Im(u * conj(s))",
                "twisted_triplet_3prime": "W = Re(s) x Im(s)",
            },
            "live_packet": {
                "sigma_half_sum": sigma,
                "delta_half_difference": delta,
                "triplet_vector": _serialize_float_vector(live_triplet),
                "twisted_triplet_vector": _serialize_float_vector(live_twisted_triplet),
                "triplet_norm": float(np.linalg.norm(live_triplet)),
                "twisted_triplet_norm": float(np.linalg.norm(live_twisted_triplet)),
                "triplet_norm_formula": live_triplet_formula_norm,
                "twisted_triplet_norm_formula": live_twisted_formula_norm,
            },
            "paper_packets": {
                "up_triplet_norm": float(np.linalg.norm(up_triplet)),
                "up_triplet_norm_formula": up_triplet_formula_norm,
                "up_twisted_triplet_norm": float(np.linalg.norm(up_twisted_triplet)),
                "up_twisted_triplet_norm_formula": up_twisted_formula_norm,
                "down_triplet_norm": float(np.linalg.norm(down_triplet)),
                "down_triplet_norm_formula": down_triplet_formula_norm,
                "down_twisted_triplet_norm": float(np.linalg.norm(down_twisted_triplet)),
                "down_twisted_triplet_norm_formula": down_twisted_formula_norm,
            },
        },
        "comparison_to_irrep_projection": {
            "live_irrep_triplet_norm": ckm_sectors["live_branch_packet"]["plus_branch"]["wedge_irrep_norms"]["3"],
            "live_irrep_twisted_triplet_norm": ckm_sectors["live_branch_packet"]["plus_branch"]["wedge_irrep_norms"]["3'"],
            "paper_up_irrep_triplet_norm": ckm_sectors["paper_packet"]["up"]["wedge_irrep_norms"]["3"],
            "paper_up_irrep_twisted_triplet_norm": ckm_sectors["paper_packet"]["up"]["wedge_irrep_norms"]["3'"],
            "paper_down_irrep_triplet_norm": ckm_sectors["paper_packet"]["down"]["wedge_irrep_norms"]["3"],
            "paper_down_irrep_twisted_triplet_norm": ckm_sectors["paper_packet"]["down"]["wedge_irrep_norms"]["3'"],
        },
        "ckm_operator_scalar_law_theorem": {
            "the_live_family_doublet_projection_is_exactly_a_universal_axis_times_scalar_minus_one_minus_ab_over_two": bool(
                np.allclose(live_doublet, live_scalar * universal_axis, atol=1e-12)
            ),
            "the_paper_real_asymmetry_projection_is_exactly_the_same_axis_with_scalar_one_over_four_times_d22_minus_u22_minus_a12d32": bool(
                np.allclose(paper_doublet, paper_scalar * universal_axis, atol=1e-12)
            ),
            "the_paper_family_scalar_contains_an_exact_cabibbo_injector_cross_term_one_over_vq": bool(
                A12 * D32 == Fraction(1, 120)
            ),
            "the_live_cp_triplet_norm_is_exactly_sqrt_2_sigma_squared_plus_4_delta_squared": bool(
                abs(np.linalg.norm(live_triplet) - live_triplet_formula_norm) < 1e-12
            ),
            "the_live_twisted_triplet_norm_is_exactly_sqrt2_times_sigma": bool(
                abs(np.linalg.norm(live_twisted_triplet) - live_twisted_formula_norm) < 1e-12
            ),
            "the_general_line_shell_and_shell_self_wedge_formulas_reproduce_the_projected_live_and_paper_3_and_3prime_norms": bool(
                abs(np.linalg.norm(live_triplet) - ckm_sectors["live_branch_packet"]["plus_branch"]["wedge_irrep_norms"]["3"]) < 1e-12
                and abs(np.linalg.norm(live_twisted_triplet) - ckm_sectors["live_branch_packet"]["plus_branch"]["wedge_irrep_norms"]["3'"]) < 1e-12
                and abs(np.linalg.norm(up_triplet) - ckm_sectors["paper_packet"]["up"]["wedge_irrep_norms"]["3"]) < 1e-12
                and abs(np.linalg.norm(up_twisted_triplet) - ckm_sectors["paper_packet"]["up"]["wedge_irrep_norms"]["3'"]) < 1e-12
                and abs(np.linalg.norm(down_triplet) - ckm_sectors["paper_packet"]["down"]["wedge_irrep_norms"]["3"]) < 1e-12
                and abs(np.linalg.norm(down_twisted_triplet) - ckm_sectors["paper_packet"]["down"]["wedge_irrep_norms"]["3'"]) < 1e-12
            ),
        },
        "interpretation": (
            "The remaining scalar problem is now much sharper. The family side is "
            "one universal tetra-doublet axis, with the live strength -(1-ab)/2 and "
            "the paper strength (d22-u22-a12*d32)/4. The extra a12*d32 term is the "
            "exact real Cabibbo-injector cross-term 1/(vq). On the CP side, the "
            "bivector shell splits canonically into line-shell interference and shell "
            "self-wedge. So the CKM sector is no longer a single messy complex packet: "
            "family strength, CP triplet, and twisted CP triplet each have their own "
            "exact operator law."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["ckm_operator_scalar_law_theorem"], indent=2))


if __name__ == "__main__":
    main()
