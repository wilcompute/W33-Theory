"""Exact condensation from the level-3 theta tower to the level-1 modular plane.

The previous toroidal/Elkies bridge showed that the discrete toroidal
oscillator lifts first to the continuous level-3 theta tower

    A2  ->  E6  ->  K12

on Gamma_1(3).  This module closes the next seam: the level-1 Eisenstein and
Leech lines already condense from that same level-3 lattice-theta algebra.

Using Elkies' exact weight-4 formulas

    theta_{A2^4}   = (E4(z) + 9 E4(3z)) / 10,
    theta_{A2 E6}  = (13 E4(z) + 27 E4(3z)) / 40,

we solve exactly:

    E4(z)  =  4 theta_{A2 E6} - 3 theta_{A2^4}.

Likewise, on the weight-6 rank-12 side the exact level-3 theta algebra gives

    E6(z)  =  9 theta_{A2^6} - 6 theta_{A2^3 E6} - 2 theta_{E6^2}.

Hence the whole weight-12 collision plane condenses from the level-3 lattice
theta algebra:

    D := 1728 Delta = E4^3 - E6^2,
    L := 12 Theta_Leech = 7 E4^3 + 5 E6^2,
    I := 691 E12 = (691 L + 455 D) / 12.

So the discrete-to-continuous route is now algebraically continuous all the
way through the first level-1 collision plane.  The toroidal q=3 oscillator
does not merely meet the E8/Leech plane numerically; it generates it through
the intermediate level-3 theta tower.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_level3_level1_theta_condensation_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_lattice_theta import e4_series, e6_series, leech_theta_coefficients, _series_mul
from w33_modular_weight12_line_triad_bridge import build_summary as build_weight12_line_triad_summary
from w33_theta_e8_lattice import e12_times_691_series
from w33_toroidal_elkies_theta_heat_bridge import theta_a2_series, theta_e6_series


N_MAX = 8


def _mul_frac(a: list[Fraction], b: list[Fraction], n_max: int) -> list[Fraction]:
    out = [Fraction(0) for _ in range(n_max + 1)]
    for i in range(n_max + 1):
        if a[i] == 0:
            continue
        for j in range(n_max + 1 - i):
            if b[j] != 0:
                out[i + j] += a[i] * b[j]
    return out


def _pow_frac(a: list[Fraction], exponent: int, n_max: int) -> list[Fraction]:
    out = [Fraction(0) for _ in range(n_max + 1)]
    out[0] = Fraction(1)
    for _ in range(exponent):
        out = _mul_frac(out, a, n_max)
    return out


def _to_frac(xs: list[int]) -> list[Fraction]:
    return [Fraction(x) for x in xs]


def _to_int_if_exact(xs: list[Fraction]) -> list[int]:
    out: list[int] = []
    for x in xs:
        assert x.denominator == 1
        out.append(x.numerator)
    return out


def build_summary(n_max: int = N_MAX) -> dict[str, Any]:
    a2 = theta_a2_series(n_max)
    e6_theta = theta_e6_series(n_max)

    theta_a2_4 = _series_mul(_series_mul(a2, a2, n_max), _series_mul(a2, a2, n_max), n_max)
    theta_a2e6 = _series_mul(a2, e6_theta, n_max)
    theta_a2_6 = _series_mul(theta_a2_4, _series_mul(a2, a2, n_max), n_max)
    theta_a2_3 = _series_mul(_series_mul(a2, a2, n_max), a2, n_max)
    theta_a2_3e6 = _series_mul(theta_a2_3, e6_theta, n_max)
    theta_e6_sq = _series_mul(e6_theta, e6_theta, n_max)

    theta_a2_4_f = _to_frac(theta_a2_4)
    theta_a2e6_f = _to_frac(theta_a2e6)
    theta_a2_6_f = _to_frac(theta_a2_6)
    theta_a2_3e6_f = _to_frac(theta_a2_3e6)
    theta_e6_sq_f = _to_frac(theta_e6_sq)

    e4 = e4_series(n_max)
    e6 = e6_series(n_max)
    e4_f = _to_frac(e4)
    e6_f = _to_frac(e6)

    e4_condensed_f = [
        4 * theta_a2e6_f[i] - 3 * theta_a2_4_f[i]
        for i in range(n_max + 1)
    ]
    e6_condensed_f = [
        9 * theta_a2_6_f[i] - 6 * theta_a2_3e6_f[i] - 2 * theta_e6_sq_f[i]
        for i in range(n_max + 1)
    ]

    e4_cubed_f = _pow_frac(e4_condensed_f, 3, n_max)
    e6_squared_f = _pow_frac(e6_condensed_f, 2, n_max)
    d12_condensed_f = [e4_cubed_f[i] - e6_squared_f[i] for i in range(n_max + 1)]
    l12_condensed_f = [7 * e4_cubed_f[i] + 5 * e6_squared_f[i] for i in range(n_max + 1)]
    i12_condensed_f = [(691 * l12_condensed_f[i] + 455 * d12_condensed_f[i]) / 12 for i in range(n_max + 1)]

    d12_condensed = _to_int_if_exact(d12_condensed_f)
    l12_condensed = _to_int_if_exact(l12_condensed_f)
    i12_condensed = _to_int_if_exact(i12_condensed_f)

    e4_cubed_int = _series_mul(_series_mul(e4, e4, n_max), e4, n_max)
    e6_squared_int = _series_mul(e6, e6, n_max)
    d12_direct = [e4_cubed_int[i] - e6_squared_int[i] for i in range(n_max + 1)]
    l12_direct = [12 * c for c in leech_theta_coefficients(n_max)]
    i12_direct = e12_times_691_series(n_max)

    triad = build_weight12_line_triad_summary()
    qdict = triad["weight12_line_triad_qseries_dictionary"]

    d_prefix = qdict["1728_Delta"]
    l_prefix = qdict["12_Theta_Leech"]
    i_prefix = qdict["691_E12"]

    return {
        "level3_rank_dictionary": {
            "theta_A2^4": theta_a2_4,
            "theta_A2E6": theta_a2e6,
            "theta_A2^6": theta_a2_6,
            "theta_A2^3E6": theta_a2_3e6,
            "theta_E6^2": theta_e6_sq,
        },
        "level1_condensation_dictionary": {
            "E4_from_level3": e4_condensed_f[: n_max + 1],
            "E6_from_level3": e6_condensed_f[: n_max + 1],
            "E4_formula": "E4 = 4*theta_{A2 E6} - 3*theta_{A2^4}",
            "E6_formula": "E6 = 9*theta_{A2^6} - 6*theta_{A2^3 E6} - 2*theta_{E6^2}",
        },
        "weight12_condensation_dictionary": {
            "D_condensed": d12_condensed,
            "L_condensed": l12_condensed,
            "I_condensed": i12_condensed,
            "D_formula": "D = E4^3 - E6^2",
            "L_formula": "L = 7 E4^3 + 5 E6^2 = 12 Theta_Leech",
            "I_formula": "I = (691 L + 455 D) / 12",
        },
        "condensation_theorem": {
            "E4_condenses_exactly_from_the_level3_rank8_theta_pair": e4_condensed_f == e4_f,
            "E6_condenses_exactly_from_the_level3_rank12_theta_triple": e6_condensed_f == e6_f,
            "the_weight12_cusp_line_D_condenses_exactly_from_level3_theta_algebra": (
                d12_condensed == d12_direct and d12_condensed[: len(d_prefix)] == d_prefix
            ),
            "the_weight12_Leech_line_L_condenses_exactly_from_level3_theta_algebra": (
                l12_condensed == l12_direct and l12_condensed[: len(l_prefix)] == l_prefix
            ),
            "the_weight12_Eisenstein_line_I_condenses_exactly_from_level3_theta_algebra": (
                i12_condensed == i12_direct and i12_condensed[: len(i_prefix)] == i_prefix
            ),
            "the_weight12_line_triad_is_now_fully_expressed_in_the_level3_lattice_theta_algebra": (
                d12_condensed[: len(d_prefix)] == d_prefix
                and l12_condensed[: len(l_prefix)] == l_prefix
                and i12_condensed[: len(i_prefix)] == i_prefix
            ),
        },
        "interpretation": (
            "The level-3 theta tower is not merely adjacent to the level-1 modular plane. "
            "It condenses onto it exactly. E4 already equals 4 theta_{A2 E6} - 3 theta_{A2^4}, "
            "E6 already equals 9 theta_{A2^6} - 6 theta_{A2^3 E6} - 2 theta_{E6^2}, and therefore "
            "the whole weight-12 line triad D / L / I is already a polynomial object in the level-3 "
            "lattice-theta algebra. This closes the discrete-to-continuous route through the first "
            "level-1 collision plane rather than just up to the shared packet 60480."
        ),
        "sources": {
            "elkies_level3_lattices": "https://people.math.harvard.edu/~elkies/M272.19/nov25.pdf",
            "elkies_weighted_theta": "https://people.math.harvard.edu/~elkies/M272.19/nov11.pdf",
        },
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=" * 72)
    print("W33 LEVEL-3 TO LEVEL-1 THETA CONDENSATION BRIDGE")
    print("=" * 72)
    for key, value in summary["condensation_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
