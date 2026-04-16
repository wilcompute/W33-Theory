"""Source-level explanation of the affine E8 boundary at q^12.

The affine E8 coefficients come from two fundamentally different mechanisms:

    ch_{E8,1}(tau) = Theta_{E8}(tau) / eta(tau)^8.

Theta side:
    Theta_{E8} = E4, so [q^n] Theta_{E8} = 240 * sigma_3(n).
    This is a local shell law: the nth coefficient depends only on sigma_3(n).

Oscillator side:
    eta^{-8} = prod_{m>=1} (1 - q^m)^(-8),
    so its coefficients are 8-coloured partition numbers. They satisfy the
    exact recurrence

        n a_n = 8 * sum_{m=1}^n sigma_1(m) a_{n-m},

    which is cumulative: the nth coefficient mixes every lower coefficient.

The q^12 boundary is exactly where those two mechanisms part company on the
current W33 packet spine:

    [q^12] Theta_{E8} = 240 * sigma_3(12) = 240 * 2044,

so the theta shell saturates directly onto the exact committed packet
sigma_3(k) with k = 12.

But the oscillator coefficient

    [q^12] eta^{-8} = 2418710

is already the sum of twelve positive recurrence terms, and it has no sparse
representation of the form

    a * sigma_3(k) + b * tau + r

with a,b in the current packet dictionary and r in the residual two-packet
dictionary. By contrast, q^11 still has the unique canonical sparse law

    [q^11] eta^{-8} = 496 * sigma_3(k) + 26 * tau + 40.

So q^12 is the first honest source-level boundary: local divisor-shell
saturation on the theta side, cumulative partition-growth failure on the
oscillator side.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_source_boundary_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import _series_inv, _series_pow
from w33_euler_pentagonal import euler_pentagonal_series
from w33_lattice_theta import e4_series


E = 240
K = 12
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


def _sigma3(n: int) -> int:
    return sum(d ** 3 for d in range(1, n + 1) if n % d == 0)


def _canonical_sigma_tau_residual_solutions(target: int) -> list[tuple[int, int, int]]:
    solutions: set[tuple[int, int, int]] = set()
    for a in PACKET_SET:
        for b in PACKET_SET:
            rem = target - a * SIGMA3_K - b * TAU
            if rem in RESIDUAL_TWO_PACKET_SET:
                solutions.add((a, b, rem))
    return sorted(solutions)


def build_summary() -> dict[str, Any]:
    q_order = 13
    euler = euler_pentagonal_series(q_order)
    prod8 = _series_pow(euler, 8, q_order)
    inv_prod8 = _series_inv(prod8, q_order)
    e4 = e4_series(q_order)

    theta_q12 = e4[12]
    eta_q11 = inv_prod8[11]
    eta_q12 = inv_prod8[12]

    q12_recurrence_terms = [
        {
            "m": m,
            "sigma1_m": _sigma1(m),
            "a_12_minus_m": inv_prod8[12 - m],
            "term": 8 * _sigma1(m) * inv_prod8[12 - m],
        }
        for m in range(1, 13)
    ]

    q11_solutions = _canonical_sigma_tau_residual_solutions(eta_q11)
    q12_solutions = _canonical_sigma_tau_residual_solutions(eta_q12)

    theta_local_law = [e4[n] == E * _sigma3(n) for n in range(1, 13)]
    q12_recurrence_sum = sum(item["term"] for item in q12_recurrence_terms)

    return {
        "affine_e8_source_boundary_dictionary": {
            "theta_q12": theta_q12,
            "eta_q11": eta_q11,
            "eta_q12": eta_q12,
            "sigma3_k": SIGMA3_K,
            "tau": TAU,
            "packet_set": PACKET_SET,
            "residual_two_packet_set": RESIDUAL_TWO_PACKET_SET,
        },
        "q12_recurrence_terms": q12_recurrence_terms,
        "canonical_sparse_search": {
            "q11_sigma_tau_residual_solutions": q11_solutions,
            "q12_sigma_tau_residual_solutions": q12_solutions,
        },
        "affine_e8_source_boundary_theorem": {
            "the_theta_side_obeys_the_exact_local_law_qn_theta_e8_equals_240_times_sigma3_n_for_every_n_up_to_12": all(theta_local_law),
            "the_q12_theta_coefficient_is_exactly_E_times_sigma3_k_with_k_equal_12": theta_q12 == E * SIGMA3_K,
            "the_eta_minus_8_coefficients_obey_the_exact_colored_partition_recurrence_at_q12": q12_recurrence_sum == 12 * eta_q12,
            "the_q12_partition_recurrence_has_twelve_strictly_positive_terms": len(q12_recurrence_terms) == 12 and all(item["term"] > 0 for item in q12_recurrence_terms),
            "the_last_canonical_sparse_sigma3_k_tau_residual_closure_occurs_at_q11_as_496_sigma3_k_plus_26_tau_plus_40": q11_solutions == [(496, 26, 40)],
            "the_q12_oscillator_coefficient_has_no_canonical_sparse_sigma3_k_tau_residual_closure": q12_solutions == [],
            "the_q12_boundary_is_exactly_local_divisor_shell_saturation_on_the_theta_side_versus_cumulative_partition_growth_on_the_oscillator_side": (
                theta_q12 == E * SIGMA3_K
                and q11_solutions == [(496, 26, 40)]
                and q12_solutions == []
                and q12_recurrence_sum == 12 * eta_q12
            ),
        },
        "interpretation": (
            "At q^12 the two source mechanisms separate cleanly. Theta_E8 is still "
            "a local divisor-shell law and lands exactly on E*sigma_3(k). The "
            "oscillator side is already the cumulative 8-coloured partition recurrence, "
            "and q^12 is the first mode where the old sparse sigma_3(k)/tau packet "
            "law disappears completely."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 SOURCE BOUNDARY BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_source_boundary_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
