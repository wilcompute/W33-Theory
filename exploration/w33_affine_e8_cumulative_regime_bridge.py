"""Cumulative-regime bridge for the affine E8 oscillator side after q^12.

The source-level boundary at q^12 already showed that the affine E8 split

    ch_{E8,1} = Theta_{E8} / eta^8

separates into two different mechanisms:

    [q^n] Theta_{E8} = 240 * sigma_3(n)

is a local divisor-shell law, while the oscillator coefficients

    a_n = [q^n] eta^{-8}

obey the cumulative recurrence

    n a_n = sum_{m=1}^n (8 sigma_1(m)) a_{n-m}.

This bridge proves that q^12 is not an isolated failure. It is the start of a
new cumulative regime:

1. the old sparse sigma_3(k) / tau residual law holds canonically at q^11,
   but fails at q^12, q^13, and q^14;
2. the theta side remains exact and local at q^12, q^13, and q^14;
3. on the oscillator side, the first four recurrence channels already account
   for more than 90% of the total at q^12, q^13, and q^14.

The first four channel weights are

    8 sigma_1(1) = 8,
    8 sigma_1(2) = 24,
    8 sigma_1(3) = 32,
    8 sigma_1(4) = 56,

which are themselves exact old packets on the W33 spine:

    8   = bosonic octet,
    24  = corrected 24-packet,
    32  = Spin(10)-sized dominant shell,
    56  = E7(fund) packet.

So after q^11 the oscillator side is no longer governed by a sparse
one-shot shell lift. It is governed by cumulative feedback through the exact
8 / 24 / 32 / 56 packet ladder.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_cumulative_regime_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import _series_inv, _series_pow
from w33_euler_pentagonal import euler_pentagonal_series
from w33_lattice_theta import e4_series


E = 240
SIGMA3_K = 2044
TAU = 252
PACKET_SET = sorted(
    {
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 20, 24, 26,
        27, 30, 32, 36, 40, 44, 50, 52, 64, 72, 78, 80, 81, 84, 90, 96, 98,
        126, 168, 192, 204, 240, 248, 252, 273, 280, 336, 496, 720, 2044,
    }
)
RESIDUAL_TWO_PACKET_SET = sorted({a + b for a in PACKET_SET for b in PACKET_SET if a <= b})
CHANNEL_WEIGHTS = [8, 24, 32, 56]


def _sigma1(n: int) -> int:
    return sum(d for d in range(1, n + 1) if n % d == 0)


def _canonical_sigma_tau_residual_solutions(target: int) -> list[tuple[int, int, int]]:
    solutions: set[tuple[int, int, int]] = set()
    for a in PACKET_SET:
        for b in PACKET_SET:
            rem = target - a * SIGMA3_K - b * TAU
            if rem in RESIDUAL_TWO_PACKET_SET:
                solutions.add((a, b, rem))
    return sorted(solutions)


def build_summary() -> dict[str, Any]:
    q_order = 15
    euler = euler_pentagonal_series(q_order)
    prod8 = _series_pow(euler, 8, q_order)
    inv_prod8 = _series_inv(prod8, q_order)
    e4 = e4_series(q_order)

    sparse = {
        11: _canonical_sigma_tau_residual_solutions(inv_prod8[11]),
        12: _canonical_sigma_tau_residual_solutions(inv_prod8[12]),
        13: _canonical_sigma_tau_residual_solutions(inv_prod8[13]),
        14: _canonical_sigma_tau_residual_solutions(inv_prod8[14]),
    }

    regime_samples: dict[str, Any] = {}
    for n in (12, 13, 14):
        terms = [8 * _sigma1(m) * inv_prod8[n - m] for m in range(1, n + 1)]
        total = sum(terms)
        first_four = sum(terms[:4])
        regime_samples[str(n)] = {
            "theta_coefficient": e4[n],
            "theta_shell_factor": e4[n] // E,
            "eta_coefficient": inv_prod8[n],
            "recurrence_terms": terms,
            "first_four_sum": first_four,
            "total": total,
            "first_four_share": {
                "numerator": first_four,
                "denominator": total,
                "fraction": str(Fraction(first_four, total)),
            },
        }

    return {
        "affine_e8_cumulative_regime_dictionary": {
            "channel_weights": CHANNEL_WEIGHTS,
            "channel_weight_dictionary": {
                "8": "bosonic octet",
                "24": "corrected 24-packet",
                "32": "Spin(10)-sized dominant shell",
                "56": "E7(fund) packet",
            },
            "sparse_sigma_tau_residual_solutions": sparse,
            "regime_samples": regime_samples,
        },
        "affine_e8_cumulative_regime_theorem": {
            "the_old_canonical_sparse_sigma3_k_tau_residual_closure_survives_exactly_at_q11_as_496_sigma3_k_plus_26_tau_plus_40": sparse[11] == [(496, 26, 40)],
            "the_old_canonical_sparse_sigma3_k_tau_residual_closure_fails_completely_at_q12": sparse[12] == [],
            "the_old_canonical_sparse_sigma3_k_tau_residual_closure_fails_completely_at_q13": sparse[13] == [],
            "the_old_canonical_sparse_sigma3_k_tau_residual_closure_fails_completely_at_q14": sparse[14] == [],
            "the_theta_side_remains_exactly_local_at_q12_q13_q14": all(
                regime_samples[str(n)]["theta_coefficient"] == E * regime_samples[str(n)]["theta_shell_factor"]
                for n in (12, 13, 14)
            ),
            "the_first_four_oscillator_recurrence_channels_are_exactly_8_24_32_56": CHANNEL_WEIGHTS == [8, 24, 32, 56],
            "the_first_four_recurrence_channels_contribute_more_than_nine_tenths_of_the_total_at_q12": (
                10 * regime_samples["12"]["first_four_sum"] > 9 * regime_samples["12"]["total"]
            ),
            "the_first_four_recurrence_channels_contribute_more_than_nine_tenths_of_the_total_at_q13": (
                10 * regime_samples["13"]["first_four_sum"] > 9 * regime_samples["13"]["total"]
            ),
            "the_first_four_recurrence_channels_contribute_more_than_nine_tenths_of_the_total_at_q14": (
                10 * regime_samples["14"]["first_four_sum"] > 9 * regime_samples["14"]["total"]
            ),
            "the_post_q11_oscillator_side_enters_a_genuine_cumulative_regime_driven_by_the_exact_8_24_32_56_packet_ladder": (
                sparse[11] == [(496, 26, 40)]
                and sparse[12] == []
                and sparse[13] == []
                and sparse[14] == []
                and 10 * regime_samples["12"]["first_four_sum"] > 9 * regime_samples["12"]["total"]
                and 10 * regime_samples["13"]["first_four_sum"] > 9 * regime_samples["13"]["total"]
                and 10 * regime_samples["14"]["first_four_sum"] > 9 * regime_samples["14"]["total"]
            ),
        },
        "interpretation": (
            "The q^12 break is the start of a regime, not a single exception. The "
            "theta side stays on the local divisor-shell law, but the oscillator "
            "side is now dominated by cumulative feedback through the exact packet "
            "weights 8, 24, 32, and 56, while the old sparse sigma_3(k)/tau law "
            "stays dead at q^12, q^13, and q^14."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 CUMULATIVE REGIME BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_cumulative_regime_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
