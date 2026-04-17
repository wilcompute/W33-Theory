r"""McKay-Thompson series T_pA via eta quotients for primes with (p-1) | 24.

For the five Monster primes  p in { 2, 3, 5, 7, 13 }  satisfying
(p - 1) | 24, the Hauptmodul of  X_0(p)+  has a beautifully simple
eta-quotient form:

    T_pA(tau)  =  ( eta(tau)/eta(p tau) )^k   +   c_p   +   p^k ( eta(p tau)/eta(tau) )^k,

where

    k    =  24 / (p - 1),
    c_p  =  k                   (chosen so the constant term of T_pA is 0),

making T_pA(tau)  =  q^{-1}  +  0  +  a_1 q  +  a_2 q^2  +  a_3 q^3  +  ...

The constants  k  and  p^k  for the five cases:

    p =  2 :  k = 24,   p^k = 2^24  = 16777216  (use  c_2 = 24)
    p =  3 :  k = 12,   p^k = 3^12  =   531441  (use  c_3 = 12)
    p =  5 :  k =  6,   p^k = 5^6   =    15625  (use  c_5 =  6)
    p =  7 :  k =  4,   p^k = 7^4   =     2401  (use  c_7 =  4)
    p = 13 :  k =  2,   p^k = 13^2  =      169  (use c_13 =  2)

Note that the "balance" identity  ord_infty( eta(tau)^k )  +  ord_infty( p^k eta(p tau)^k )
                                  =  k/24  +  k/24 . p   from Atkin-Lehner symmetry
                                  =  (1 + p) k / 24                  =  1 + p / (p-1).
The  -1  pole at infinity comes from the  ( eta(tau) / eta(p tau) )^k   piece.

CONNECTION TO MOONSHINE.

For each of the  194  conjugacy classes  [g]  of M, Conway and Norton's
moonshine conjecture (now Borcherds' theorem) attaches a normalized
Hauptmodul  T_g(tau)  =  q^{-1}  +  sum_{n >= 1}  a_n([g]) q^n   such that

    a_n([g])  =  trace_g (V_n^naturalmod),

where  V^natural  =  oplus_n V_n  is the Frenkel-Lepowsky-Meurman
moonshine module  (Z-graded VOA with  Aut V^natural  =  M).

For the  CLASSES  1A, 2A, 3A, 5A, 7A, 13A   (the "fundamental" prime
classes of orders  1, 2, 3, 5, 7, 13  whose centralizers contain a  Z/p
subgroup of largest possible exponent), the Hauptmoduls  T_pA  =
McKay-Thompson series for class  pA  match the Hauptmoduls of
X_0(p)+  -- this is THE Conway-Norton observation that the j-function
 j(tau) - 744 = T_1A(tau)  generalizes uniformly to one Hauptmodul per
Monster prime power.

CROSS-PIN WITH LAYER 39  (MOONSHINE COEFFICIENTS).

    T_1A(q)  =  J(q) - 744  =  q^{-1}  +  196884 q  +  21493760 q^2  +  864299970 q^3  +  ...
    The 196884  =  1 + 196883  (McKay) carries through to all five T_pA
    via fusion-rule restrictions; in particular, the q^1 coefficient of
    T_pA is the dimension of the smallest faithful representation of M
    on which the centralizer of the class pA acts.

This layer pins:
    (1) eta(tau)^k  q-expansion (pentagonal number theorem powered to k);
    (2) T_pA q-expansion equals eta-quotient + constant + dual-eta-quotient
        for p in {2, 3, 5, 7, 13};
    (3) the constant offset c_p = k = 24/(p-1) makes the constant term
        of T_pA exactly 0;
    (4) first six Fourier coefficients of T_pA match Conway-Norton tables;
    (5) all five primes are in MONSTER_PRIMES from Layer 39;
    (6) (p-1) | 24 for each, so the Hauptmodul construction is uniform.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from fractions import Fraction
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_mckay_thompson_eta_quotients_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))


from w33_monster_ogg_supersingular import MONSTER_PRIMES  # noqa: E402


# ----------------------------------------------------------------------
# Power series helpers (exact integer / Fraction arithmetic).
# ----------------------------------------------------------------------
def poly_mul(a: list, b: list, N: int) -> list:
    """Multiply two power series truncated to degree N (entries 0 .. N)."""
    out = [0] * (N + 1)
    for i in range(min(len(a), N + 1)):
        ai = a[i]
        if ai == 0:
            continue
        for j in range(min(len(b), N + 1 - i)):
            out[i + j] += ai * b[j]
    return out


def poly_pow(a: list, exp: int, N: int) -> list:
    """Raise power series to integer exp, truncated to degree N."""
    result = [0] * (N + 1)
    result[0] = 1
    base = list(a) + [0] * max(0, N + 1 - len(a))
    base = base[: N + 1]
    e = exp
    while e > 0:
        if e & 1:
            result = poly_mul(result, base, N)
        e >>= 1
        if e:
            base = poly_mul(base, base, N)
    return result


def euler_phi_pentagonal(N: int) -> list[int]:
    """Coefficients of  prod_{n >= 1} (1 - q^n)  via the pentagonal number theorem,
    truncated to degree N."""
    out = [0] * (N + 1)
    out[0] = 1
    k = 1
    while True:
        e1 = k * (3 * k - 1) // 2
        e2 = k * (3 * k + 1) // 2
        if e1 > N and e2 > N:
            break
        sign = -1 if k % 2 == 1 else 1
        if e1 <= N:
            out[e1] = sign
        if e2 <= N:
            out[e2] = sign
        k += 1
    return out


def eta_to_k_q_expansion(k: int, N: int) -> list[int]:
    """Coefficients of  prod_{n >= 1} (1 - q^n)^k  truncated to degree N
    (i.e.  eta(tau)^k  with the  q^{k/24}  prefactor stripped)."""
    base = euler_phi_pentagonal(N)
    return poly_pow(base, k, N)


def substitute_qp(coefs: list, p: int, N: int) -> list[int]:
    """Substitute q -> q^p in a power series, truncating to degree N."""
    out = [0] * (N + 1)
    for i, c in enumerate(coefs):
        if c == 0:
            continue
        idx = i * p
        if idx > N:
            break
        out[idx] = c
    return out


def series_div(a: list, b: list, N: int) -> list:
    """Divide power series a by power series b (b[0] must be nonzero, units only).

    Returns out with out[0..N] such that  a = b * out  truncated to degree N."""
    if b[0] == 0:
        raise ValueError("denominator constant term is zero; not invertible")
    out = [0] * (N + 1)
    inv0 = Fraction(1) / Fraction(b[0])
    for n in range(N + 1):
        s = Fraction(a[n] if n < len(a) else 0)
        for j in range(1, n + 1):
            if j < len(b) and b[j] != 0:
                s -= Fraction(b[j]) * out[n - j]
        out[n] = s * inv0
    return out


# ----------------------------------------------------------------------
# Eta-quotient core:  ( eta(tau)/eta(p tau) )^k  has q-expansion
#                     starting at  q^{((1-p)k/24)} = q^{-1}  (when k = 24/(p-1)).
# ----------------------------------------------------------------------
ETA_QUOTIENT_PARAMS: list[tuple[int, int]] = [
    (2,  24),  # k = 24/(2-1) = 24
    (3,  12),  # k = 24/(3-1) = 12
    (5,   6),  # k = 24/(5-1) = 6
    (7,   4),  # k = 24/(7-1) = 4
    (13,  2),  # k = 24/(13-1) = 2
]


def _eta_quotient_no_pole(p: int, k: int, N: int) -> list:
    """Return the Laurent-series shifted  q . (eta(tau)/eta(p tau))^k  (degree-N).

    (eta(tau)/eta(p tau))^k  =  q^{(1-p)k/24}  Pi(1-q^n)^k / Pi(1-q^(p n))^k
                              =  q^{-1}                  ratio_inner  for our k.

    We return the polynomial ratio_inner of degree at most N + 1, so that
    the Laurent coefficient of  q^m  in the original is  ratio_inner[m + 1].
    """
    num = eta_to_k_q_expansion(k, N + 1)
    inner_eta = euler_phi_pentagonal(N + 1)
    inner_eta_pk = substitute_qp(inner_eta, p, N + 1)
    den = poly_pow(inner_eta_pk, k, N + 1)
    return series_div(num, den, N + 1)


def eta_quotient_laurent(p: int, k: int, N: int) -> list:
    """Return [coeff(q^{-1}), coeff(q^0), coeff(q^1), ..., coeff(q^N)] of (eta(tau)/eta(p tau))^k."""
    inner = _eta_quotient_no_pole(p, k, N)
    # coefficient of q^m in the original = inner[m + 1]
    return [inner[m + 1] for m in range(-1, N + 1)]


def dual_eta_quotient(p: int, k: int, N: int) -> list:
    """Return [coeff(q^0), coeff(q^1), ..., coeff(q^N)] of  p^k . (eta(p tau)/eta(tau))^k.

    eta(p tau)^k  has q-shift  q^{p k / 24} = q^{p / (p-1)};  divide by eta(tau)^k
    with q-shift  q^{1/(p-1)};  net q-shift  q^{(p-1)/(p-1)} = q^1.

    So the Laurent expansion starts at  q^1.  We return the coefficient list
    starting at q^0 (which is 0).
    """
    num_inner_eta = euler_phi_pentagonal(N + 1)
    num_inner_eta_pk = substitute_qp(num_inner_eta, p, N + 1)
    num = poly_pow(num_inner_eta_pk, k, N + 1)
    den = eta_to_k_q_expansion(k, N + 1)
    inner = series_div(num, den, N + 1)
    # original q-shift = q^1, so coefficient of q^m = inner[m - 1] (for m >= 1)
    out = [Fraction(0)] * (N + 1)
    # The correct dual prefactor is p^{k/2} (Atkin-Lehner normalization)
    factor = Fraction(p ** (k // 2))
    for m in range(1, N + 1):
        if m - 1 < len(inner):
            out[m] = factor * inner[m - 1]
    return out


# ----------------------------------------------------------------------
# T_pA  =  eta-quotient + c_p + dual-eta-quotient,  with c_p chosen so
# the constant term of T_pA vanishes.
# ----------------------------------------------------------------------
def mckay_thompson_T_pA(p: int, N: int) -> list:
    """Return [coeff(q^{-1}), coeff(q^0), coeff(q^1), ..., coeff(q^N)] of T_pA.

    T_pA = (eta(tau)/eta(p tau))^k + c_p + p^k (eta(p tau)/eta(tau))^k,
    with c_p chosen so coeff(q^0) of T_pA is 0."""
    k = 24 // (p - 1)
    eta_q = eta_quotient_laurent(p, k, N)         # length N + 2 (q^{-1} ... q^N)
    dual = dual_eta_quotient(p, k, N)             # length N + 1 (q^0 ... q^N)
    # Sum: out[0] = q^{-1} coefficient, out[m+1] = q^m coefficient (m = 0..N).
    out = [Fraction(0)] * (N + 2)
    out[0] = eta_q[0]                             # q^{-1}
    for m in range(0, N + 1):
        out[m + 1] = eta_q[m + 1] + dual[m]
    # Choose c_p so out[1] (the constant term) becomes zero.
    c_p = -out[1]
    out[1] = Fraction(0)
    return out, c_p


# ----------------------------------------------------------------------
# Conway-Norton reference Fourier coefficients.
# Source: Conway-Norton (1979), "Monstrous Moonshine", and the LMFDB
# / Atlas of Moonshine tables.
# ----------------------------------------------------------------------
T_pA_REFERENCE_COEFFS: dict[int, list[int]] = {
    # T_2A:   q^{-1} + 4372 q + 96256 q^2 + 1240002 q^3 + 10698752 q^4 + 74428120 q^5
    2:  [4372, 96256, 1240002, 10698752, 74428120],
    # T_3A:   q^{-1} + 783 q + 8672 q^2 + 65367 q^3 + 371520 q^4 + 1741655 q^5
    3:  [783, 8672, 65367, 371520, 1741655],
    # T_5A:   q^{-1} + 134 q + 760 q^2 + 3345 q^3 + 12256 q^4 + 39350 q^5
    5:  [134, 760, 3345, 12256, 39350],
    # T_7A:   q^{-1} + 51 q + 204 q^2 + 681 q^3 + 1956 q^4 + 5135 q^5
    7:  [51, 204, 681, 1956, 5135],
    # T_13A:  q^{-1} + 12 q + 28 q^2 + 66 q^3 + 132 q^4 + 258 q^5
    13: [12, 28, 66, 132, 258],
}


# ----------------------------------------------------------------------
# Verification driver.
# ----------------------------------------------------------------------
def verify_T_pA_against_reference(N: int = 6) -> dict[str, Any]:
    discrepancies = []
    rows = []
    for p, k in ETA_QUOTIENT_PARAMS:
        coefs, c_p = mckay_thompson_T_pA(p, N=N)
        # coefs[0] = q^{-1} coeff (should be 1)
        # coefs[1] = constant (should be 0 by construction)
        # coefs[2] = q^1 coefficient
        # ...
        ref = T_pA_REFERENCE_COEFFS[p]
        got = [int(coefs[2 + j]) for j in range(len(ref))]
        coefs_ok = (int(coefs[0]) == 1 and int(coefs[1]) == 0 and got == ref)
        if not coefs_ok:
            discrepancies.append({"p": p, "got": got, "ref": ref,
                                  "qm1": int(coefs[0]), "q0": int(coefs[1])})
        rows.append({"p": p, "k": k, "c_p": int(c_p),
                     "q_minus_1_coef": int(coefs[0]),
                     "q_0_coef": int(coefs[1]),
                     "first_five_a_n": got,
                     "matches_reference": coefs_ok})
    return {
        "rows":          rows,
        "discrepancies": discrepancies,
        "all_match":     discrepancies == [],
    }


def verify_constant_offsets() -> dict[str, Any]:
    """c_p = k = 24/(p-1) by Atkin-Lehner balance."""
    discrepancies = []
    for p, k in ETA_QUOTIENT_PARAMS:
        _, c_p = mckay_thompson_T_pA(p, N=6)
        if int(c_p) != k:
            discrepancies.append({"p": p, "expected_c_p": k, "got_c_p": int(c_p)})
    return {
        "discrepancies": discrepancies,
        "all_c_p_equal_k": discrepancies == [],
    }


def verify_primes_are_in_monster() -> dict[str, Any]:
    eta_primes = [p for p, _ in ETA_QUOTIENT_PARAMS]
    in_monster = all(p in MONSTER_PRIMES for p in eta_primes)
    return {
        "eta_primes":       eta_primes,
        "all_in_monster":   in_monster,
        "five_of_fifteen":  len(eta_primes) == 5,
    }


def verify_p_minus_1_divides_24() -> dict[str, Any]:
    rows = []
    for p, _ in ETA_QUOTIENT_PARAMS:
        rows.append({"p": p, "p-1": p - 1, "(p-1)|24": 24 % (p - 1) == 0,
                     "k=24/(p-1)": 24 // (p - 1)})
    return {
        "rows":            rows,
        "all_divide_24":   all(r["(p-1)|24"] for r in rows),
    }


def verify_T_2A_q1_coefficient_4372() -> dict[str, Any]:
    """The 4372 = 1 + 4371 splits as moonshine: 4371 = dim(196883 |_{centralizer})
    of the smallest faithful M-rep restricted to the centralizer of a 2A involution.
    See Conway-Norton's character table of M.

    (4372 = 4 * 1093, with 1093 a Wieferich prime; numerologically suggestive.)
    """
    coefs, _ = mckay_thompson_T_pA(2, N=3)
    return {
        "T_2A_q1_coefficient":   int(coefs[2]),
        "matches_conway_norton": int(coefs[2]) == 4372,
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    coef_check = verify_T_pA_against_reference(N=6)
    offset_check = verify_constant_offsets()
    monster_check = verify_primes_are_in_monster()
    div_check = verify_p_minus_1_divides_24()
    t_2A_check = verify_T_2A_q1_coefficient_4372()
    return {
        "coefficient_check":          coef_check,
        "constant_offset_check":      offset_check,
        "monster_prime_check":        monster_check,
        "divisibility_check":         div_check,
        "T_2A_q1_coefficient_check":  t_2A_check,
        "summary_chain": {
            "T_pA_first_five_coefs_match_ref":   coef_check["all_match"],
            "constant_offset_c_p_equals_k":      offset_check["all_c_p_equal_k"],
            "all_five_p_in_Monster_primes":      monster_check["all_in_monster"],
            "p_minus_1_divides_24_for_each":     div_check["all_divide_24"],
            "T_2A_q1_is_4372":                   t_2A_check["matches_conway_norton"],
        },
    }


def main() -> None:
    summary = derive_all()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=" * 72)
    print("W33 LAYER 43 — MCKAY-THOMPSON SERIES T_pA  FOR  p in {2,3,5,7,13}")
    print("                VIA  ETA-QUOTIENT  HAUPTMODULS")
    print("=" * 72)
    print()
    for key, val in summary["summary_chain"].items():
        status = "PASS" if val else "FAIL"
        print(f"  [{status}] {key}")
    print()
    print("  CLASS    p    k=24/(p-1)   c_p    First five Fourier coefficients")
    for row in summary["coefficient_check"]["rows"]:
        coefs_str = ", ".join(f"{c:>10d}" for c in row["first_five_a_n"])
        print(f"   {row['p']}A    {row['p']:2d}      {row['k']:2d}        {row['c_p']:3d}    [{coefs_str}]")
    print()
    print("  Cross-pin: 4372 = T_2A q^1 coefficient = 1 + 4371")
    print("             4371 = dim of moonshine 196883-rep restricted to C_M(2A).")


if __name__ == "__main__":
    main()
