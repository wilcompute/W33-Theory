"""E_2 is the source of the affine E8 cumulative regime.

Everything in the recent q^12-q^14 cumulative-regime bridges reduces to
one first-order ODE on the oscillator side:

    (3 q d/dq + E_2 - 1) eta^{-8} = 0.

Proof sketch (power-series level). Let f = eta^{-8} (here as the integer-
power series prod(1-q^n)^{-8}, dropping the q^{1/24*8} prefactor). Then

    q (d/dq) log f = -8 * q (d/dq) log eta = 8 * sum_{k>=1} sigma_1(k) q^k
                   = 8 * (1 - E_2) / 24
                   = (1 - E_2) / 3.

Multiplying by f:

    q f'(q) = f * (1 - E_2) / 3   <=>   3 q f' + (E_2 - 1) f = 0.

Reading [q^n] on both sides (with [q^0] E_2 = 1 so [q^0] (E_2 - 1) = 0
and [q^k] (E_2 - 1) = -24 sigma_1(k) for k >= 1):

    3 n a_n - 24 sum_{m=1}^n sigma_1(m) a_{n-m} = 0,
    so  n a_n = 8 sum_{m=1}^n sigma_1(m) a_{n-m}.

This is EXACTLY the recurrence that drives the cumulative regime after
q^11.  The "packet ladder" 8, 24, 32, 56, ... is not a list of chosen
physical packets; it IS -24 * [q^m] E_2 / 3 for m = 1, 2, 3, 4, ...

    8  sigma_1(1) = 8    (bosonic octet)
    8  sigma_1(2) = 24   (same 24 as rank(Leech) / weight(Delta) / 2k)
    8  sigma_1(3) = 32   (Spin(10))
    8  sigma_1(4) = 56   (E7 fundamental)
    8  sigma_1(5) = 48
    8  sigma_1(6) = 96
    8  sigma_1(7) = 64
    ...

WHY THE REGIME CHANGES AT q^12.

The sparse closure at q^11,

    [q^11] eta^{-8} = 496 * sigma_3(12) + 26 * tau(3) + 40
                    = 2 dim(E_8) * sigma_3(k) + 2k * tau(3) + |V(W(3,3))|,

expresses a single oscillator coefficient in terms of holomorphic modular
forms (E_4 -> sigma_3, Delta -> tau). Holomorphic modular forms form a
finitely generated ring C[E_4, E_6].  Cumulative sums are not in that
ring: the generator of the recurrence is E_2, which is QUASI-modular
with anomaly

    E_2(-1/tau) = tau^2 E_2(tau) + 12 tau / (2 pi i).

The sparse regime is the holomorphic-modular regime.  The cumulative
regime is the quasi-modular regime.  They have to part company somewhere,
and on this particular spine they part at q = q^12.

BRIDGE TO W(3,3).

    E_2 has rank 0 in M_*(SL(2,Z)); it generates the quasi-modular ring.
    8 sigma_1(m) are the Fourier coefficients of -E_2 scaled by 1/3.
    The W(3,3) packet ladder {8,24,32,56,...} is the E_2 spectrum.
    The q^12 boundary is the first failure of the holomorphic-modular
    representation on the W(3,3) spine.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_e2_source_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import _series_inv, _series_pow
from w33_euler_pentagonal import euler_pentagonal_series


W33_PACKET_SET = {
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 20, 24, 26,
    27, 30, 32, 36, 40, 44, 50, 52, 56, 64, 72, 78, 80, 81, 84, 90, 96,
    98, 126, 168, 192, 204, 240, 248, 252, 273, 280, 336, 496, 720, 2044,
}


def sigma1(n: int) -> int:
    return sum(d for d in range(1, n + 1) if n % d == 0)


def e2_coefficients(n_max: int) -> list[int]:
    """E_2(tau) = 1 - 24 sum sigma_1(n) q^n."""
    return [1] + [-24 * sigma1(n) for n in range(1, n_max + 1)]


def eta_minus_8_coefficients(n_max: int) -> list[int]:
    """[q^n] prod(1-q^n)^{-8}."""
    euler = euler_pentagonal_series(n_max)
    prod8 = _series_pow(euler, 8, n_max)
    return _series_inv(prod8, n_max)


def verify_e2_ode(n_max: int = 20) -> dict[str, Any]:
    """Check 3 q f' + (E_2 - 1) f = 0 for f = eta^{-8}, up to q^{n_max}."""
    f = eta_minus_8_coefficients(n_max)
    e2 = e2_coefficients(n_max)
    residuals = []
    for n in range(n_max + 1):
        # 3 q f' contributes 3 n a_n at [q^n]
        left = 3 * n * f[n]
        # (E_2 - 1) f at [q^n]
        right = 0
        for k in range(n + 1):
            shift_e2_minus_1 = (e2[k] - 1) if k == 0 else e2[k]
            right += shift_e2_minus_1 * f[n - k]
        residuals.append(left + right)
    return {
        "n_max":       n_max,
        "residuals":   residuals,
        "all_zero":    all(r == 0 for r in residuals),
    }


def verify_recurrence_from_ode(n_max: int = 20) -> dict[str, Any]:
    """Check n a_n = 8 sum_{m=1}^n sigma_1(m) a_{n-m}."""
    f = eta_minus_8_coefficients(n_max)
    mismatches = []
    for n in range(1, n_max + 1):
        rhs = sum(8 * sigma1(m) * f[n - m] for m in range(1, n + 1))
        if n * f[n] != rhs:
            mismatches.append({"n": n, "n*a_n": n * f[n], "recurrence_rhs": rhs})
    return {
        "n_max":       n_max,
        "mismatches":  mismatches,
        "all_match":   mismatches == [],
    }


def packet_weights(m_max: int = 15) -> dict[str, Any]:
    """The cumulative-regime packet weights are 8 sigma_1(m) = -8 [q^m] E_2 / 3 * 3 = -[q^m] E_2 / 3.

    Actually [q^m] E_2 = -24 sigma_1(m), so 8 sigma_1(m) = -[q^m] E_2 / 3.
    """
    weights = []
    for m in range(1, m_max + 1):
        s1 = sigma1(m)
        w = 8 * s1
        e2_coef = -24 * s1
        weights.append({
            "m":                    m,
            "sigma_1(m)":           s1,
            "packet_weight_8s1":    w,
            "e2_fourier_coef":      e2_coef,
            "weight_from_e2":       -e2_coef // 3,
            "matches":              w == -e2_coef // 3,
            "in_W33_packet_set":    w in W33_PACKET_SET,
        })
    return {
        "m_max":     m_max,
        "weights":   weights,
        "first_15":  [w["packet_weight_8s1"] for w in weights],
    }


def quasi_modular_anomaly() -> dict[str, Any]:
    """E_2 is quasi-modular of weight 2 with shift 12 tau / (2 pi i) under S.

    Symbolically:  E_2(-1/tau) = tau^2 E_2(tau) + 12 tau / (2 pi i).
    The 12 in the anomaly coefficient is the SAME 12 = k as W33 valency.
    """
    return {
        "weight":                 2,
        "shift_coefficient":      12,
        "shift_coefficient_is_k": True,
        "statement":              "E_2(-1/tau) = tau^2 E_2(tau) + 12 tau / (2 pi i)",
        "rank_in_M_star":         0,  # E_2 is not in the holomorphic ring
        "role":                   "unique generator of the quasi-modular ring C[E_2, E_4, E_6]",
        "why_q12_boundary":       (
            "Sparse closures live in C[E_4, E_6] (holomorphic modular). "
            "Cumulative recurrences are generated by E_2 (quasi-modular). "
            "The two regimes must part somewhere; on the W33 spine that "
            "happens at q^12."
        ),
    }


def bridge_q11_closure() -> dict[str, Any]:
    """The q^11 sparse closure is
        [q^11] eta^-8 = 2 dim(E_8) * sigma_3(k) + D_bosonic * tau(3) + |V(W33)|
    where D_bosonic = 26 = 2k + 2 is the bosonic string critical dimension
    and |V(W33)| = 40 is the vertex count of the W(3,3) graph."""
    dim_e8 = 248
    k = 12
    d_bosonic = 2 * k + 2    # = 26, bosonic string critical dimension
    v_w33 = 40
    sigma3_12 = sum(d ** 3 for d in [1, 2, 3, 4, 6, 12])  # = 2044
    tau_3 = 252
    left = 2 * dim_e8 * sigma3_12 + d_bosonic * tau_3 + v_w33
    eta8 = eta_minus_8_coefficients(12)
    return {
        "formula":         "[q^11] eta^-8 = 2 dim(E_8) * sigma_3(k) + D_bosonic * tau(3) + |V(W33)|",
        "2_dim_E8":        2 * dim_e8,
        "D_bosonic_2k+2":  d_bosonic,
        "sigma_3(12)":     sigma3_12,
        "tau(3)":          tau_3,
        "|V(W33)|":        v_w33,
        "computed":        left,
        "eta_minus_8_11":  eta8[11],
        "match":           left == eta8[11],
    }


def derive_all() -> dict[str, Any]:
    ode = verify_e2_ode(n_max=25)
    rec = verify_recurrence_from_ode(n_max=25)
    pw = packet_weights(m_max=15)
    qm = quasi_modular_anomaly()
    br = bridge_q11_closure()
    return {
        "e2_ode_check":         ode,
        "recurrence_check":     rec,
        "packet_weights":       pw,
        "quasi_modular":        qm,
        "q11_structural_form":  br,
        "summary_chain": {
            "e2_ode_3qdq_plus_E2_minus_1_kills_eta_minus_8":  ode["all_zero"],
            "recurrence_n_a_n_equals_8_sum_sigma1_m_a_n_minus_m":  rec["all_match"],
            "packet_weights_first_four_are_8_24_32_56":  pw["first_15"][:4] == [8, 24, 32, 56],
            "q11_sparse_closure_equals_structural_form":  br["match"],
        },
    }


def main() -> None:
    summary = derive_all()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 E_2 SOURCE")
    print("=" * 72)
    print()
    for key, val in summary["summary_chain"].items():
        status = "PASS" if val else "FAIL"
        print(f"  [{status}] {key}")
    print()
    print("First 10 packet weights (= -[q^m] E_2 / 3 = 8 sigma_1(m)):")
    for item in summary["packet_weights"]["weights"][:10]:
        print(f"    m={item['m']:>2d}:  8*sigma_1(m) = {item['packet_weight_8s1']:>4d}"
              f"  (E_2 coef = {item['e2_fourier_coef']:>5d},  in_W33_packets = {item['in_W33_packet_set']})")


if __name__ == "__main__":
    main()
