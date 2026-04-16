"""Persistence of the affine E8 cumulative regime beyond q^12.

The previous affine bridges proved two facts:

1. q^11 is the last mode with the canonical sparse oscillator law

       [q^11] eta^{-8} = 496*sigma_3(k) + 26*tau + 40

2. q^12 is the first one-sided boundary:
   theta remains exact and local, while the oscillator side no longer has a
   sparse sigma_3(k)/tau residual closure.

This bridge checks whether q^12 is an isolated failure or the start of a real
regime.  The answer is exact: the new cumulative regime persists at least
through q^18.

For n = 12,...,18:

    - the old sparse sigma_3(k)/tau residual law never returns;
    - the first four recurrence channels still contribute more than 6/7
      of the total;
    - the first eight recurrence channels still contribute more than 99%
      of the total;
    - both shares decrease monotonically, so cumulative feedback is taking
      over in a controlled way rather than randomly.

The first eight recurrence weights are

    8*sigma_1(m) for m=1,...,8 = 8, 24, 32, 56, 48, 96, 64, 120.

So the post-q^11 oscillator side is a persistent cumulative ladder driven by
the exact divisor-sum weights rather than by one-shot sparse shell lifts.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_cumulative_regime_persistence_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import _series_inv, _series_pow
from w33_euler_pentagonal import euler_pentagonal_series


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
    q_order = 19
    euler = euler_pentagonal_series(q_order)
    prod8 = _series_pow(euler, 8, q_order)
    inv_prod8 = _series_inv(prod8, q_order)

    channel_weights = [8 * _sigma1(m) for m in range(1, 9)]
    samples: dict[str, Any] = {}
    top4_shares: list[Fraction] = []
    top8_shares: list[Fraction] = []

    for n in range(12, 19):
        terms = [8 * _sigma1(m) * inv_prod8[n - m] for m in range(1, n + 1)]
        total = sum(terms)
        top4 = sum(terms[:4])
        top8 = sum(terms[:8])
        top4_share = Fraction(top4, total)
        top8_share = Fraction(top8, total)
        top4_shares.append(top4_share)
        top8_shares.append(top8_share)
        samples[str(n)] = {
            "eta_coefficient": inv_prod8[n],
            "sparse_sigma_tau_residual_solutions": _canonical_sigma_tau_residual_solutions(inv_prod8[n]),
            "top4_share": {
                "numerator": top4,
                "denominator": total,
                "fraction": str(top4_share),
            },
            "top8_share": {
                "numerator": top8,
                "denominator": total,
                "fraction": str(top8_share),
            },
            "first_eight_terms": terms[:8],
        }

    top4_monotone = all(top4_shares[i] > top4_shares[i + 1] for i in range(len(top4_shares) - 1))
    top8_monotone = all(top8_shares[i] > top8_shares[i + 1] for i in range(len(top8_shares) - 1))

    return {
        "affine_e8_cumulative_regime_persistence_dictionary": {
            "channel_weights_m1_to_m8": channel_weights,
            "samples_q12_to_q18": samples,
        },
        "affine_e8_cumulative_regime_persistence_theorem": {
            "the_sparse_sigma3_k_tau_residual_law_stays_dead_from_q12_through_q18": all(
                samples[str(n)]["sparse_sigma_tau_residual_solutions"] == [] for n in range(12, 19)
            ),
            "the_first_four_recurrence_channels_contribute_more_than_six_sevenths_of_the_total_from_q12_through_q18": all(
                7 * samples[str(n)]["top4_share"]["numerator"] > 6 * samples[str(n)]["top4_share"]["denominator"]
                for n in range(12, 19)
            ),
            "the_first_eight_recurrence_channels_contribute_more_than_ninety_nine_percent_of_the_total_from_q12_through_q18": all(
                100 * samples[str(n)]["top8_share"]["numerator"] > 99 * samples[str(n)]["top8_share"]["denominator"]
                for n in range(12, 19)
            ),
            "the_first_eight_channel_weights_are_exactly_8_24_32_56_48_96_64_120": channel_weights == [8, 24, 32, 56, 48, 96, 64, 120],
            "the_top4_share_decreases_strictly_from_q12_through_q18": top4_monotone,
            "the_top8_share_decreases_strictly_from_q12_through_q18": top8_monotone,
            "the_post_q11_oscillator_side_is_a_persistent_cumulative_regime_not_a_single_mode_exception": (
                all(samples[str(n)]["sparse_sigma_tau_residual_solutions"] == [] for n in range(12, 19))
                and all(7 * samples[str(n)]["top4_share"]["numerator"] > 6 * samples[str(n)]["top4_share"]["denominator"] for n in range(12, 19))
                and all(100 * samples[str(n)]["top8_share"]["numerator"] > 99 * samples[str(n)]["top8_share"]["denominator"] for n in range(12, 19))
                and top4_monotone
                and top8_monotone
            ),
        },
        "interpretation": (
            "The q^12 break is persistent. From q^12 through q^18 the old sparse "
            "sigma_3(k)/tau law never returns, while the oscillator side stays "
            "dominated by the first four and then first eight exact divisor-sum "
            "channels. The regime is cumulative and stable, not accidental."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 CUMULATIVE REGIME PERSISTENCE BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_cumulative_regime_persistence_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
