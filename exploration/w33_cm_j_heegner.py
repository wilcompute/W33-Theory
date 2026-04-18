"""CM j-invariant values at Heegner points, and the
e^{pi sqrt(d)}-near-integer phenomenon.

For each d in the Heegner list {1, 2, 3, 7, 11, 19, 43, 67, 163}, the
imaginary quadratic field Q(sqrt(-d)) has class number 1, so j(tau_d)
is an integer (in fact a rational integer that is a perfect cube):

    d=1   (tau = i):               j = 12^3    = 1728
    d=2   (tau = i sqrt 2):        j = 20^3    = 8000
    d=3   (tau = (1+i sqrt 3)/2):  j = 0^3     = 0
    d=7   (tau = (1+i sqrt 7)/2):  j = (-15)^3 = -3375
    d=11:                          j = (-32)^3 = -32768
    d=19:                          j = (-96)^3 = -884736
    d=43:                          j = (-960)^3 = -884736000
    d=67:                          j = (-5280)^3 = -147197952000
    d=163:                         j = (-640320)^3 = -262537412640768000

From j(tau) = q^{-1} + 744 + O(q) with q = -exp(-pi sqrt(d)) for
d ≡ 3 mod 4, we get e^{pi sqrt(d)} ≈ |H_d|^3 + 744, making Ramanujan's
constant e^{pi sqrt(163)} ≈ 640320^3 + 744 an almost-integer to
12 decimal places.

This closes the Heegner-Stark theorem's numerical face: these 9 values
exhaust the class-number-1 imaginary quadratic orders.
"""

from __future__ import annotations

from typing import Any

import mpmath as mp


# ----------------------------------------------------------------------
# Heegner numbers and reference j-values.
# ----------------------------------------------------------------------
HEEGNER_NUMBERS: list[int] = [1, 2, 3, 7, 11, 19, 43, 67, 163]

HEEGNER_J_VALUES: dict[int, int] = {
    1: 1728,
    2: 8000,
    3: 0,
    7: -3375,
    11: -32768,
    19: -884736,
    43: -884736000,
    67: -147197952000,
    163: -262537412640768000,
}

HEEGNER_CUBE_ROOTS: dict[int, int] = {
    1: 12,
    2: 20,
    3: 0,
    7: -15,
    11: -32,
    19: -96,
    43: -960,
    67: -5280,
    163: -640320,
}


# ----------------------------------------------------------------------
# j-function q-expansion coefficients (OEIS A000521).
# ----------------------------------------------------------------------
J_COEFFS_EXPANSION: list[int] = [
    196884,
    21493760,
    864299970,
    20245856256,
    333202640600,
    4252023300096,
    44656994071935,
    401490886656000,
    3176440229784420,
    22567393309593600,
    146211911499519294,
    874313719685775360,
    4872010111798142520,
    25497827389410525184,
    126142916465781843075,
    593121772421445058560,
    2662842413150775245160,
    11459912788444786513920,
    47438786801234168813250,
    189449976248893390028800,
]


# ----------------------------------------------------------------------
# tau_d and q_d.
# ----------------------------------------------------------------------
def heegner_tau(d: int) -> mp.mpc:
    """The fundamental CM point tau_d for Q(sqrt(-d))."""
    if d in (1, 2):
        return mp.mpc(0, mp.sqrt(d))
    if d % 4 != 3:
        raise ValueError(f"d = {d} is not a Heegner number (must be 1, 2, or 3 mod 4).")
    return mp.mpc(mp.mpf(1) / 2, mp.sqrt(d) / 2)


def heegner_q(d: int) -> mp.mpc:
    """q = exp(2 pi i tau_d).  For d ≡ 3 mod 4 this is -exp(-pi sqrt(d))."""
    return mp.exp(2j * mp.pi * heegner_tau(d))


# ----------------------------------------------------------------------
# j at CM points via q-expansion.
# ----------------------------------------------------------------------
def j_at_heegner(d: int, n_terms: int | None = None) -> mp.mpc:
    """j(tau_d) via q-expansion with enough terms for precision."""
    q = heegner_q(d)
    if n_terms is None:
        # Adaptive: stop when term magnitude falls below 10^{-dps}.
        n_terms = len(J_COEFFS_EXPANSION)
    j = 1 / q + mp.mpf(744)
    for i in range(n_terms):
        term = J_COEFFS_EXPANSION[i] * q ** (i + 1)
        j += term
        # Early-stop heuristic.
        if abs(term) < mp.mpf(10) ** (-mp.mp.dps + 5):
            break
    return j


# ----------------------------------------------------------------------
# Verifiers.
# ----------------------------------------------------------------------
def verify_heegner_j_values(dps: int = 60) -> dict[str, Any]:
    """j(tau_d) rounds to HEEGNER_J_VALUES[d] for all 9 Heegner numbers."""
    mp.mp.dps = dps
    rows: list[dict[str, Any]] = []
    all_match = True
    for d in HEEGNER_NUMBERS:
        j = j_at_heegner(d)
        expected = HEEGNER_J_VALUES[d]
        # Allow tolerance relative to magnitude.
        imag_err = abs(j.imag)
        real_err = abs(j.real - expected)
        scale = max(abs(mp.mpf(expected)), mp.mpf(1))
        match = (real_err < scale * mp.mpf("1e-20")) and imag_err < mp.mpf("1e-10")
        rows.append({
            "d": d,
            "j_real": float(j.real) if abs(j.real) < 1e18 else str(j.real),
            "j_imag_abs": float(imag_err),
            "expected": expected,
            "abs_err": float(real_err) if real_err < 1e10 else str(real_err),
            "match": bool(match),
        })
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows, "dps_used": dps}


def verify_heegner_cubes() -> dict[str, Any]:
    """j(tau_d) = H_d^3 for integer H_d (the Heegner cube root)."""
    rows: list[dict[str, Any]] = []
    all_match = True
    for d in HEEGNER_NUMBERS:
        H = HEEGNER_CUBE_ROOTS[d]
        cube = H ** 3
        j_val = HEEGNER_J_VALUES[d]
        match = cube == j_val
        rows.append({
            "d": d,
            "H": H,
            "H_cubed": cube,
            "j": j_val,
            "match": match,
        })
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def near_integer_ramanujan(d: int, dps: int = 60) -> dict[str, Any]:
    """For d ≡ 3 mod 4 Heegner, e^{pi sqrt(d)} is near |H_d|^3 + 744.

    Derivation: tau_d = (1+i sqrt d)/2, q = -e^{-pi sqrt d},
    q^{-1} = -e^{pi sqrt d}, j = q^{-1} + 744 + O(q) ⇒
             -e^{pi sqrt d} + 744 + (sum c_n q^n) = H_d^3,
             e^{pi sqrt d} = |H_d|^3 + 744 + (sum c_n (-q)^n).
    """
    if d not in (3, 7, 11, 19, 43, 67, 163):
        raise ValueError("Near-integer formula applies to d ≡ 3 mod 4 only.")
    mp.mp.dps = dps
    exp_val = mp.exp(mp.pi * mp.sqrt(d))
    H = HEEGNER_CUBE_ROOTS[d]
    predicted = mp.mpf(abs(H)) ** 3 + 744
    deviation = exp_val - predicted
    return {
        "d": d,
        "exp_pi_sqrt_d": str(exp_val),
        "H_abs_cubed_plus_744": str(predicted),
        "deviation": float(deviation) if abs(deviation) < 1e10 else str(deviation),
        "log10_abs_deviation": float(mp.log10(abs(deviation))) if deviation != 0 else None,
    }


def verify_ramanujan_163_almost_integer(dps: int = 40) -> dict[str, Any]:
    """Specifically pin e^{pi sqrt 163} - 640320^3 - 744 is ~ -7.5e-13."""
    mp.mp.dps = dps
    lhs = mp.exp(mp.pi * mp.sqrt(163))
    rhs = mp.mpf(640320) ** 3 + 744
    deviation = lhs - rhs
    return {
        "lhs": str(lhs),
        "rhs": str(rhs),
        "deviation": float(deviation),
        "within_1e_9": bool(abs(deviation) < mp.mpf("1e-9")),
        "within_1e_12": bool(abs(deviation) < mp.mpf("1e-12")),
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    j_check = verify_heegner_j_values(dps=60)
    cubes = verify_heegner_cubes()
    r163 = verify_ramanujan_163_almost_integer(dps=40)
    near_int_rows = [
        near_integer_ramanujan(d, dps=60)
        for d in [7, 11, 19, 43, 67, 163]
    ]
    chain = {
        "j_at_all_9_heegner_points_is_integer": j_check["all_match"],
        "every_heegner_j_is_a_perfect_cube": cubes["all_match"],
        "ramanujan_e_pi_sqrt_163_within_1e_9_of_640320_cubed_plus_744":
            r163["within_1e_9"],
    }
    return {
        "heegner_j_evaluation": j_check,
        "heegner_cubes": cubes,
        "ramanujan_163": r163,
        "near_integer_rows": near_int_rows,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nHeegner j-values:")
    for row in s["heegner_j_evaluation"]["rows"]:
        print(f"  d={row['d']:>3}:  expected={row['expected']},  match={row['match']}")
    print("\nHeegner cube structure:")
    for row in s["heegner_cubes"]["rows"]:
        print(f"  d={row['d']:>3}:  j = {row['H']}^3 = {row['H_cubed']}")
    print("\nRamanujan e^(pi sqrt 163) near-integer:")
    for k, v in s["ramanujan_163"].items():
        print(f"  {k}: {v}")
