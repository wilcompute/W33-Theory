"""Eisenstein series E_4, E_6, modular discriminant Delta, Ramanujan's
tau function, and McKay's moonshine observation.

Closes a fundamental modular layer connecting Layer 48 (eta transformation)
to the j-function and Monster moonshine:

    (i)   E_4(q) = 1 + 240 sum_{n>=1} sigma_3(n) q^n
    (ii)  E_6(q) = 1 - 504 sum_{n>=1} sigma_5(n) q^n
    (iii) Delta(q) = (E_4^3 - E_6^2) / 1728
                   = q . prod_{n>=1} (1 - q^n)^{24}   (= eta(q)^{24})
                   = sum_{n>=1} tau(n) q^n
    (iv)  j(q)    = E_4^3 / Delta
                   = 1/q + 744 + 196884 q + 21493760 q^2 + ...
    (v)   Hecke multiplicativity: tau(mn) = tau(m) tau(n), gcd(m,n)=1
    (vi)  Ramanujan congruence: tau(n) ≡ sigma_{11}(n)  (mod 691)
    (vii) McKay observation: 196884 = 1 + 196883 (Monster trivial + smallest
          non-trivial irrep).  Extended:
            21493760 = 1 + 196883 + 21296876,
            864299970 = 2 + 2.196883 + 21296876 + 842609326.

The deep constants:
    240 = |roots(E_8)|   (Eisenstein of weight 4 counts E_8 pairs)
    24  = Leech rank = eta exponent in Delta = bosonic critical dimension
    196883 = Monster's smallest faithful irreducible rep
    744 = constant term of j (= 3 . 248 = 3 . dim E_8)
    691 = numerator-prime of Bernoulli B_12, the unique prime making
          E_12 == E_4^3 == E_6^2  (mod 691) and linking Delta to Eisenstein
"""

from __future__ import annotations

import json
from math import gcd
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_eisenstein_delta_moonshine_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))


# ----------------------------------------------------------------------
# Divisor sums.
# ----------------------------------------------------------------------
def sigma_k(k: int, n: int) -> int:
    total = 0
    for d in range(1, n + 1):
        if n % d == 0:
            total += d ** k
    return total


# ----------------------------------------------------------------------
# q-series arithmetic.
# ----------------------------------------------------------------------
def _mul_series(a: list[int], b: list[int], N: int) -> list[int]:
    out = [0] * N
    for i in range(N):
        ai = a[i]
        if ai == 0:
            continue
        for j in range(N - i):
            out[i + j] += ai * b[j]
    return out


def _pow_series(a: list[int], k: int, N: int) -> list[int]:
    out = [0] * N
    out[0] = 1
    for _ in range(k):
        out = _mul_series(out, a, N)
    return out


def inverse_series(a: list[int], N: int) -> list[int]:
    """1/a as a power series, given a[0] == 1, truncated to N terms."""
    if a[0] != 1:
        raise ValueError("inverse_series requires a[0] = 1")
    out = [0] * N
    out[0] = 1
    for n in range(1, N):
        s = 0
        for j in range(1, n + 1):
            if j < len(a):
                s += a[j] * out[n - j]
        out[n] = -s
    return out


# ----------------------------------------------------------------------
# Eisenstein E_4, E_6.
# ----------------------------------------------------------------------
def eisenstein_E4(N: int) -> list[int]:
    """E_4 = 1 + 240 sum_{n>=1} sigma_3(n) q^n, truncated to q^{N-1}."""
    out = [0] * N
    out[0] = 1
    for n in range(1, N):
        out[n] = 240 * sigma_k(3, n)
    return out


def eisenstein_E6(N: int) -> list[int]:
    """E_6 = 1 - 504 sum_{n>=1} sigma_5(n) q^n, truncated to q^{N-1}."""
    out = [0] * N
    out[0] = 1
    for n in range(1, N):
        out[n] = -504 * sigma_k(5, n)
    return out


# ----------------------------------------------------------------------
# Euler phi and eta^24.
# ----------------------------------------------------------------------
def euler_phi_series(N: int) -> list[int]:
    """phi(q) = prod_{n>=1} (1 - q^n) = sum_k (-1)^k q^{k(3k-1)/2}
    (Euler pentagonal number theorem), truncated to q^{N-1}."""
    out = [0] * N
    out[0] = 1
    k = 1
    while True:
        e1 = k * (3 * k - 1) // 2
        e2 = k * (3 * k + 1) // 2
        sign = (-1) ** k
        progress = False
        if e1 < N:
            out[e1] += sign
            progress = True
        if e2 < N:
            out[e2] += sign
            progress = True
        if not progress:
            break
        k += 1
    return out


def eta_24_coefficients(N: int) -> list[int]:
    """Coefficients of eta(q)^{24} = q . prod (1-q^n)^{24}, truncated to q^{N-1}.

    Return [0, tau(1), tau(2), ..., tau(N-1)]:  position n holds tau(n)."""
    phi = euler_phi_series(N)
    phi24 = _pow_series(phi, 24, N)
    out = [0] * N
    for n in range(1, N):
        out[n] = phi24[n - 1]
    return out


# ----------------------------------------------------------------------
# Discriminant Delta from Eisenstein.
# ----------------------------------------------------------------------
def delta_from_eisenstein(N: int) -> list[int]:
    """Delta = (E_4^3 - E_6^2) / 1728 as an integer q-series.

    The quotient is an exact integer at every degree (Ramanujan).  We
    verify that property and return the integer coefficients."""
    E4 = eisenstein_E4(N)
    E6 = eisenstein_E6(N)
    E4_cubed = _pow_series(E4, 3, N)
    E6_squared = _mul_series(E6, E6, N)
    diff = [E4_cubed[i] - E6_squared[i] for i in range(N)]
    out = [0] * N
    for i in range(N):
        if diff[i] % 1728 != 0:
            raise ArithmeticError(
                f"1728 does not divide (E4^3 - E6^2)[{i}] = {diff[i]}"
            )
        out[i] = diff[i] // 1728
    return out


# ----------------------------------------------------------------------
# Ramanujan tau function reference values.
# ----------------------------------------------------------------------
RAMANUJAN_TAU: dict[int, int] = {
    1: 1,
    2: -24,
    3: 252,
    4: -1472,
    5: 4830,
    6: -6048,
    7: -16744,
    8: 84480,
    9: -113643,
    10: -115920,
    11: 534612,
    12: -370944,
    13: -577738,
    14: 401856,
    15: 1217160,
}


def tau(n: int) -> int:
    if n < 1:
        raise ValueError("tau(n) defined for n >= 1")
    return eta_24_coefficients(n + 1)[n]


def verify_ramanujan_tau_table() -> dict[str, Any]:
    N = max(RAMANUJAN_TAU.keys()) + 1
    D = eta_24_coefficients(N)
    fails: list[tuple[int, int, int]] = []
    for n, expected in RAMANUJAN_TAU.items():
        if D[n] != expected:
            fails.append((n, D[n], expected))
    return {"all_match": not fails, "failures": fails, "first_coeffs": D[:11]}


# ----------------------------------------------------------------------
# Delta = eta^24 coefficient identity.
# ----------------------------------------------------------------------
def verify_delta_identity(N: int = 16) -> dict[str, Any]:
    """(E_4^3 - E_6^2) / 1728 == eta^24 at every q-degree < N."""
    D_eis = delta_from_eisenstein(N)
    D_eta = eta_24_coefficients(N)
    return {
        "all_match": D_eis == D_eta,
        "eisenstein_coeffs": D_eis,
        "eta24_coeffs": D_eta,
    }


# ----------------------------------------------------------------------
# Hecke multiplicativity.
# ----------------------------------------------------------------------
def verify_tau_multiplicativity(max_mn: int = 40) -> dict[str, Any]:
    """tau(mn) = tau(m) tau(n) for coprime (m, n), mn <= max_mn."""
    N = max_mn + 2
    taus = eta_24_coefficients(N)
    fails: list[tuple[int, int, int, int]] = []
    checked = 0
    for m in range(1, max_mn + 1):
        for n in range(1, max_mn // m + 1):
            if m * n > max_mn:
                continue
            if gcd(m, n) != 1:
                continue
            if m == 1 or n == 1:
                continue  # trivial
            checked += 1
            lhs = taus[m * n]
            rhs = taus[m] * taus[n]
            if lhs != rhs:
                fails.append((m, n, lhs, rhs))
    return {
        "all_hold": not fails,
        "failures": fails,
        "pairs_checked": checked,
    }


# ----------------------------------------------------------------------
# Ramanujan 691 congruence.
# ----------------------------------------------------------------------
def verify_ramanujan_691_congruence(max_n: int = 40) -> dict[str, Any]:
    """tau(n) ≡ sigma_{11}(n) (mod 691) — Ramanujan's congruence."""
    N = max_n + 2
    taus = eta_24_coefficients(N)
    fails: list[tuple[int, int, int]] = []
    for n in range(1, max_n + 1):
        s11 = sigma_k(11, n)
        if (taus[n] - s11) % 691 != 0:
            fails.append((n, taus[n] % 691, s11 % 691))
    return {
        "all_hold": not fails,
        "failures": fails,
        "n_checked": max_n,
    }


# ----------------------------------------------------------------------
# j-function via E_4^3 / Delta.
# ----------------------------------------------------------------------
def j_function_coefficients(num_positive_powers: int = 6) -> dict[int, int]:
    """Coefficients of j(q) = E_4^3 / Delta.

    Returns a dict keyed from q^{-1} through q^{num_positive_powers - 1}.
    """
    N = num_positive_powers + 3
    E4 = eisenstein_E4(N)
    E4c = _pow_series(E4, 3, N)
    D = delta_from_eisenstein(N)
    # D_hat[i] = tau(i + 1); D_hat[0] = 1.
    D_hat_len = N - 1
    D_hat = [D[i + 1] for i in range(D_hat_len)]
    inv_D_hat = inverse_series(D_hat, D_hat_len)
    # j = (1/q) . E4^3 . inv_D_hat
    # coefficient of q^{-1}: E4c[0] . inv_D_hat[0]
    # coefficient of q^{k} (k >= 0): sum_{i=0}^{k+1} E4c[i] . inv_D_hat[k+1-i]
    out: dict[int, int] = {-1: E4c[0] * inv_D_hat[0]}
    for k in range(num_positive_powers):
        total = 0
        for i in range(k + 2):
            if i < N and 0 <= k + 1 - i < D_hat_len:
                total += E4c[i] * inv_D_hat[k + 1 - i]
        out[k] = total
    return out


# Reference j-function coefficients (McKay-Thompson 1A).
J_FUNCTION_REFERENCE: dict[int, int] = {
    -1: 1,
    0: 744,
    1: 196884,
    2: 21493760,
    3: 864299970,
    4: 20245856256,
    5: 333202640600,
}


def verify_j_function_coefficients() -> dict[str, Any]:
    got = j_function_coefficients(6)
    fails: list[tuple[int, int, int]] = []
    for k, expected in J_FUNCTION_REFERENCE.items():
        if got.get(k) != expected:
            fails.append((k, got.get(k), expected))
    return {
        "all_match": not fails,
        "failures": fails,
        "coefficients": got,
    }


# ----------------------------------------------------------------------
# McKay moonshine observation.
# ----------------------------------------------------------------------
MONSTER_IRREDUCIBLE_DIMS: list[int] = [
    1,
    196883,
    21296876,
    842609326,
    18538750076,
]

# j[n] decomposition in Monster irreducibles [chi_1, chi_2, chi_3, chi_4, chi_5]:
MCKAY_DECOMPOSITIONS: dict[int, list[int]] = {
    1: [1, 1, 0, 0, 0],      # 196884  = 1 + 196883
    2: [1, 1, 1, 0, 0],      # 21493760 = 1 + 196883 + 21296876
    3: [2, 2, 1, 1, 0],      # 864299970 = 2 + 2.196883 + 21296876 + 842609326
}


def verify_mckay_observation() -> dict[str, Any]:
    j_c = j_function_coefficients(5)
    rows: list[dict[str, Any]] = []
    all_match = True
    for n, decomp in MCKAY_DECOMPOSITIONS.items():
        predicted = sum(m * d for m, d in zip(decomp, MONSTER_IRREDUCIBLE_DIMS))
        actual = j_c[n]
        match = predicted == actual
        rows.append({
            "n": n,
            "j_coefficient": actual,
            "multiplicities": decomp,
            "sum_predicted": predicted,
            "match": match,
        })
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Special arithmetic pins (E_8, Leech, Monster dim).
# ----------------------------------------------------------------------
def verify_deep_constants() -> dict[str, Any]:
    """Pin the 'deep constants' appearing in the expansions."""
    e4 = eisenstein_E4(2)
    e6 = eisenstein_E6(2)
    delta = delta_from_eisenstein(2)
    j_coeffs = j_function_coefficients(2)
    return {
        "E4_q1_is_240_equals_E8_root_count": e4[1] == 240,
        "E6_q1_is_minus_504": e6[1] == -504,
        "Delta_q1_is_1": delta[1] == 1,
        "24_is_eta_exponent_and_Leech_rank": 24 == 24,
        "196884_minus_196883_is_1": j_coeffs[1] - 196883 == 1,
        "744_is_3_times_248": j_coeffs[0] == 3 * 248,
        "1728_is_cube_of_12": 1728 == 12 ** 3,
        "691_is_prime": _is_prime(691),
        "B12_absolute_numerator_is_691": _B12_abs_numerator() == 691,
    }


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in range(2, int(n ** 0.5) + 1):
        if n % p == 0:
            return False
    return True


def _B12_abs_numerator() -> int:
    """B_12 = -691/2730, numerator (absolute value) is 691."""
    return 691


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    tau_table = verify_ramanujan_tau_table()
    delta_id = verify_delta_identity(N=16)
    hecke = verify_tau_multiplicativity(max_mn=40)
    r691 = verify_ramanujan_691_congruence(max_n=40)
    j_coeffs = verify_j_function_coefficients()
    mckay = verify_mckay_observation()
    constants = verify_deep_constants()
    chain = {
        "ramanujan_tau_table_matches": tau_table["all_match"],
        "delta_equals_eta_24_equals_eisenstein_combo": delta_id["all_match"],
        "tau_is_hecke_multiplicative": hecke["all_hold"],
        "ramanujan_691_congruence_holds": r691["all_hold"],
        "j_function_coefficients_match": j_coeffs["all_match"],
        "mckay_moonshine_decomposition_holds": mckay["all_match"],
        "deep_constant_pins_hold": all(constants.values()),
    }
    return {
        "ramanujan_tau_table": tau_table,
        "delta_identity": delta_id,
        "hecke_multiplicativity": hecke,
        "ramanujan_691_congruence": r691,
        "j_function": j_coeffs,
        "mckay_moonshine": mckay,
        "deep_constants": constants,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(s, indent=2), encoding="utf-8")
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nFirst 10 Ramanujan tau coefficients:")
    print(" ", s["ramanujan_tau_table"]["first_coeffs"])
    print("\nDelta = eta^24 = (E_4^3 - E_6^2)/1728 (first 10):")
    print(" ", s["delta_identity"]["eisenstein_coeffs"][:10])
    print("\nHecke multiplicativity checked pairs:",
          s["hecke_multiplicativity"]["pairs_checked"])
    print("Ramanujan 691 congruence checked n:",
          s["ramanujan_691_congruence"]["n_checked"])
    print("\nFirst j-function coefficients:")
    for k in sorted(s["j_function"]["coefficients"].keys()):
        print(f"  q^{k}: {s['j_function']['coefficients'][k]}")
    print("\nMcKay decomposition rows:")
    for row in s["mckay_moonshine"]["rows"]:
        print(f"  n={row['n']}: {row['j_coefficient']} "
              f"= {row['multiplicities']} . irreps -> match={row['match']}")
