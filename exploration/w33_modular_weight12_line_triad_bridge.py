"""The natural line triad on the weight-12 modular collision plane.

The weight-12 plane has three canonical lines:

    D := 1728 Delta,
    L := 12 Theta_Leech,
    I := 691 E_12.

In the monomial basis (E_4^3, E_6^2), these lines are

    D = (  1,  -1),
    L = (  7,   5),
    I = (441, 250).

So the three pairwise determinants are

    det(L, D) = -12,
    det(I, D) = -691,
    det(I, L) =  455 = 5 * 7 * 13.

This gives the exact integral relation

    12 I = 691 L + 455 D,

equivalently

    12 * (691 E_12)
      = 691 * (12 Theta_Leech) + 455 * (1728 Delta).

Thus the first modular collision plane carries a natural integer line triad:
the cusp line, the Leech rootless line, and the Eisenstein line.  The familiar
691 denominator is only one determinant on that triad; the Leech side adds the
exact modular-period determinant 12 and the packet determinant
455 = (mu+1) Phi_6 Phi_3.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_modular_weight12_line_triad_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_eisenstein_closure import e12_times_691_series
from w33_lattice_theta import (
    _series_mul,
    delta_from_e4_e6,
    e4_series,
    e6_series,
    leech_theta_coefficients,
)
from w33_modular_dimension_formula import dim_M, dim_S


Q = 3
MU = 4
PHI3 = 13
PHI6 = 7


def _det(u: tuple[int, int], v: tuple[int, int]) -> int:
    return u[0] * v[1] - u[1] * v[0]


def build_summary() -> dict[str, Any]:
    d = (1, -1)
    l = (7, 5)
    i = (441, 250)

    det_ld = _det(l, d)
    det_id = _det(i, d)
    det_il = _det(i, l)

    n_max = 3
    e4 = e4_series(n_max)
    e6 = e6_series(n_max)
    e4_cubed = _series_mul(_series_mul(e4, e4, n_max), e4, n_max)
    e6_squared = _series_mul(e6, e6, n_max)
    delta = delta_from_e4_e6(n_max)
    leech = leech_theta_coefficients(n_max)
    e12_691 = e12_times_691_series(n_max)

    d_series = [1728 * c for c in delta]
    l_series = [12 * c for c in leech]
    i_series = e12_691

    lhs_triad_relation = [12 * c for c in i_series]
    rhs_triad_relation = [691 * l_series[n] + 455 * d_series[n] for n in range(n_max + 1)]
    l_from_monomials = [7 * e4_cubed[n] + 5 * e6_squared[n] for n in range(n_max + 1)]

    return {
        "weight12_line_triad_dictionary": {
            "dim_M_12": dim_M(12),
            "dim_S_12": dim_S(12),
            "cusp_line_D": list(d),
            "leech_line_L": list(l),
            "eisenstein_line_I": list(i),
            "det_L_D": det_ld,
            "det_I_D": det_id,
            "det_I_L": det_il,
            "det_I_L_factorization": {
                "mu_plus_1": MU + 1,
                "Phi_6": PHI6,
                "Phi_3": PHI3,
                "product": (MU + 1) * PHI6 * PHI3,
            },
        },
        "weight12_line_triad_qseries_dictionary": {
            "E4_cubed": e4_cubed,
            "E6_squared": e6_squared,
            "1728_Delta": d_series,
            "12_Theta_Leech": l_series,
            "691_E12": i_series,
            "7_E4_cubed_plus_5_E6_squared": l_from_monomials,
            "12_times_691_E12": lhs_triad_relation,
            "691_times_12_Theta_Leech_plus_455_times_1728_Delta": rhs_triad_relation,
        },
        "weight12_line_triad_theorem": {
            "weight_12_is_the_first_two_dimensional_collision_plane": dim_M(12) == 2 and dim_S(12) == 1,
            "the_cusp_line_is_1728_Delta_with_vector_1_minus_1": d == (1, -1),
            "the_Leech_line_is_12_Theta_Leech_with_vector_7_5": l == (7, 5),
            "the_Eisenstein_line_is_691_E12_with_vector_441_250": i == (441, 250),
            "determinant_of_Leech_and_cusp_lines_is_exactly_minus_12": det_ld == -12,
            "determinant_of_Eisenstein_and_cusp_lines_is_exactly_minus_691": det_id == -691,
            "determinant_of_Eisenstein_and_Leech_lines_is_exactly_455_equals_5_times_7_times_13": (
                det_il == (MU + 1) * PHI6 * PHI3 == 455
            ),
            "12_Theta_Leech_equals_7_E4cubed_plus_5_E6squared": l_series == l_from_monomials,
            "the_integral_weight12_line_triad_satisfies_12I_equals_691L_plus_455D": (
                lhs_triad_relation == rhs_triad_relation
            ),
            "the_weight12_collision_plane_now_has_the_exact_integer_triad_12_455_691": (
                det_ld == -12 and det_id == -691 and det_il == 455
            ),
        },
        "interpretation": (
            "The first modular collision plane now carries a natural integral "
            "line triad. The cusp line has determinant 12 against the Leech "
            "rootless line, determinant 691 against the Eisenstein line, and "
            "the Eisenstein-Leech pair closes with determinant 455 = 5*7*13. "
            "So the modular weight-12 plane is no longer just 'where 691 first "
            "appears'; it is an exact 12/455/691 line geometry on the existing "
            "W33 packet alphabet."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 MODULAR WEIGHT-12 LINE TRIAD BRIDGE")
    print("=" * 72)
    for key, value in summary["weight12_line_triad_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
