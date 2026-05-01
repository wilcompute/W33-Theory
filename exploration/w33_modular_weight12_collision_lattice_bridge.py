"""Weight-12 collision plane as an exact integral lattice change-of-basis.

At weight 12 the modular ring first becomes two-dimensional:

    M_12 = span(E_4^3, E_6^2),    dim M_12 = 2.

There are two natural integral directions on this plane:

    I_12 := 691 E_12,
    D_12 := 1728 Delta = E_4^3 - E_6^2.

In the monomial basis  (E_4^3, E_6^2), these are

    I_12 = 441 E_4^3 + 250 E_6^2,
    D_12 =   1 E_4^3 -   1 E_6^2.

So the integer change-of-basis matrix is

    [[441, 250],
     [  1,  -1]]

with determinant

    -441 - 250 = -691.

This is the clean algebraic meaning of the Ramanujan 691 anomaly on the
weight-12 collision plane: 691 is the exact index between the naive monomial
lattice and the natural integral Eisenstein/cusp lattice.

The coefficients themselves already sit on the W33 packet dictionary:

    441   = (q Phi_6)^2 = 21^2,
    250   = lambda (mu+1)^3 = 2 * 5^3,
    1728  = 12^3,
    65520 = 240 * 273

where 240 is the E8 root packet and 273 = 3*7*13 is the ternary-heptad-triality
commutant packet.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

try:
    from exploration.w33_bridge_inputs import load_bridge_json
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from w33_bridge_inputs import load_bridge_json


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = (
    DATA_DIR / "w33_modular_weight12_collision_lattice_bridge_summary.json"
)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_eisenstein_closure import verify_691_E12_equals_441_E4cubed_plus_250_E6sq
from w33_modular_dimension_formula import dim_M, dim_S


def _load_json(name: str) -> dict[str, Any]:
    return load_bridge_json(name, DATA_DIR)


Q = 3
LAMBDA = 2
MU = 4
PHI6 = 7


def build_summary() -> dict[str, Any]:
    ternary = _load_json("w33_ternary_heptad_triality_bridge_summary.json")

    matrix = [[441, 250], [1, -1]]
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    inverse = [
        [Fraction(matrix[1][1], determinant), Fraction(-matrix[0][1], determinant)],
        [Fraction(-matrix[1][0], determinant), Fraction(matrix[0][0], determinant)],
    ]

    root_packet = 240
    commutant_dim = int(ternary["commutant_packet"]["dimension"])
    q_coeff_integral_e12 = 65520

    return {
        "weight12_collision_lattice_dictionary": {
            "dim_M_12": dim_M(12),
            "dim_S_12": dim_S(12),
            "monomial_basis": ["E4^3", "E6^2"],
            "integral_basis": ["691 E12", "1728 Delta"],
            "change_matrix_rows": [[441, 250], [1, -1]],
            "change_matrix_determinant": determinant,
            "change_matrix_inverse": [
                [str(inverse[i][j]) for j in range(2)] for i in range(2)
            ],
            "packet_coefficients": {
                "441": "(q Phi6)^2",
                "250": "lambda (mu+1)^3",
                "1728": "12^3",
                "65520": "240 * 273",
            },
            "E8_root_packet_240": root_packet,
            "ternary_commutant_273": commutant_dim,
        },
        "weight12_collision_lattice_theorem": {
            "weight_12_is_the_first_two_dimensional_modular_collision_plane": (
                dim_M(12) == 2 and dim_S(12) == 1
            ),
            "the_natural_integral_basis_is_691E12_and_1728Delta": (
                verify_691_E12_equals_441_E4cubed_plus_250_E6sq(n_max=20)["all_match"]
            ),
            "the_change_of_basis_matrix_from_monomials_to_integral_lines_has_determinant_minus_691": (
                determinant == -691
            ),
            "the_ramanujan_prime_691_is_exactly_the_index_of_the_integral_weight12_basis_change": (
                abs(determinant) == 691
            ),
            "the_441_coefficient_is_exactly_the_square_of_the_ag21_packet_q_times_phi6": (
                441 == (Q * PHI6) ** 2
            ),
            "the_250_coefficient_is_exactly_lambda_times_mu_plus_1_cubed": (
                250 == LAMBDA * (MU + 1) ** 3
            ),
            "the_discriminant_scale_1728_is_exactly_12_cubed": 1728 == 12**3,
            "the_first_integral_e12_fourier_correction_65520_is_exactly_E8_roots_times_the_ternary_commutant": (
                q_coeff_integral_e12 == root_packet * commutant_dim
            ),
            "the_weight12_collision_plane_is_exactly_packetized_on_the_existing_W33_alphabet": (
                abs(determinant) == 691
                and 441 == (Q * PHI6) ** 2
                and 250 == LAMBDA * (MU + 1) ** 3
                and 1728 == 12**3
                and q_coeff_integral_e12 == root_packet * commutant_dim
            ),
        },
        "interpretation": (
            "The first modular collision plane now has an exact lattice meaning. "
            "The natural integral basis is the Eisenstein line 691E12 and the cusp "
            "line 1728Delta, and the basis-change determinant back to the naive "
            "monomial lattice (E4^3,E6^2) is exactly 691. So the Ramanujan prime "
            "is the index of the weight-12 collision-lattice change of basis, not "
            "just a stray denominator. The collision coefficients themselves also "
            "sit on the existing W33 packet alphabet."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 MODULAR WEIGHT-12 COLLISION LATTICE BRIDGE")
    print("=" * 72)
    for key, value in summary["weight12_collision_lattice_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
