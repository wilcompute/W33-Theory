"""Hasse bound for elliptic curves over F_p, and Eichler-Shimura
for the conductor-11 newform.

Hasse's theorem (1933).  Let E : y^2 = x^3 + ax + b be an elliptic
curve over F_p (p odd prime, p doesn't divide 4a^3 + 27b^2).  Then

    #E(F_p) = p + 1 - a_p,     with     |a_p| <= 2 sqrt(p).

a_p is the trace of Frobenius, and is computable by

    a_p = -sum_{x in F_p} chi((x^3 + a x + b)),

where chi = Legendre symbol (quadratic residue character modulo p).

Eichler-Shimura (weight 2, level 11).  The modular form

    f_11(q) = eta(q)^2 eta(q^11)^2
            = q prod_{n>=1} (1-q^n)^2 (1-q^{11n})^2

is the unique normalized newform in S_2(Gamma_0(11)), and its
Fourier coefficients a_p(f_11) agree with the Hasse trace a_p(E_11)
for the elliptic curve

    E_11 : y^2 + y = x^3 - x^2        (conductor 11).

First few:  a_2 = -2,  a_3 = -1,  a_5 = 1,  a_7 = -2,  a_{13} = 4.

This is Layer 57 — the arithmetic-geometry face of the modular-form
tower: Hasse trace of Frobenius is the Hecke eigenvalue of the
associated cusp form.  Links Layer 50 (Delta, tau, Hecke) to point
counting over finite fields.
"""

from __future__ import annotations

import math
from typing import Any


# ----------------------------------------------------------------------
# Legendre / Jacobi symbol.
# ----------------------------------------------------------------------
def legendre(a: int, p: int) -> int:
    """Legendre symbol (a/p) for p odd prime, a in Z.
       Returns -1, 0, or 1."""
    a_mod = a % p
    if a_mod == 0:
        return 0
    # Euler's criterion: a^{(p-1)/2} mod p.
    v = pow(a_mod, (p - 1) // 2, p)
    return 1 if v == 1 else -1


# ----------------------------------------------------------------------
# Point counting on y^2 = x^3 + a x + b over F_p.
# ----------------------------------------------------------------------
def count_points_weierstrass(a: int, b: int, p: int) -> int:
    """#E(F_p) for E : y^2 = x^3 + a x + b.  p odd prime, curve smooth."""
    count = 1  # point at infinity
    for x in range(p):
        rhs = (x ** 3 + a * x + b) % p
        if rhs == 0:
            count += 1
        else:
            sym = legendre(rhs, p)
            if sym == 1:
                count += 2
    return count


def a_p_weierstrass(a: int, b: int, p: int) -> int:
    """a_p(E) = p + 1 - #E(F_p)."""
    return p + 1 - count_points_weierstrass(a, b, p)


# ----------------------------------------------------------------------
# Elliptic curve E_11: y^2 + y = x^3 - x^2, conductor 11.
#
# In short Weierstrass form: let Y = 2y + 1, then
#   Y^2 = 4y^2 + 4y + 1 = 4(x^3 - x^2) + 1 = 4x^3 - 4x^2 + 1.
# Substitute X = 4x - 4/3 (not over Z), so we use the affine count
# directly for E_11.
# ----------------------------------------------------------------------
def count_points_E11(p: int) -> int:
    """#E_11(F_p) for E_11 : y^2 + y = x^3 - x^2 over F_p.

    For p=11 the curve is smooth but we exclude it from the generic
    Hasse pin because p = level (bad reduction)."""
    count = 1  # infinity
    for x in range(p):
        # y^2 + y - (x^3 - x^2) = 0 is a quadratic in y.
        # Solutions y mod p exist iff discriminant 1 + 4(x^3 - x^2)
        # is a QR mod p (p odd).
        c = (x ** 3 - x ** 2) % p
        disc = (1 + 4 * c) % p
        if p == 2:
            # y^2 + y = c mod 2 <=> y(y+1) = c; y(y+1) is always 0 mod 2,
            # so solutions exist iff c = 0 mod 2, and then both y=0,1 solve.
            if c % 2 == 0:
                count += 2
        else:
            sym = legendre(disc, p)
            if sym == 1:
                count += 2
            elif sym == 0:
                count += 1  # double root
    return count


def a_p_E11(p: int) -> int:
    """Frobenius trace for E_11."""
    return p + 1 - count_points_E11(p)


# ----------------------------------------------------------------------
# f_11 q-expansion via eta(q)^2 eta(q^11)^2.
# ----------------------------------------------------------------------
def eta_base_series(N: int, k: int = 1) -> list[int]:
    """Q-series of eta(q^k)^1 / q^{k/24}, i.e. prod_{n>=1}(1 - q^{k n})
       truncated to q^{N-1}.  Returns phi(q^k)."""
    out = [0] * N
    out[0] = 1
    step = k
    while step < N:
        for i in range(N - 1, step - 1, -1):
            out[i] -= out[i - step]
        step += k
    return out


def _mul(a: list[int], b: list[int], N: int) -> list[int]:
    out = [0] * N
    for i in range(N):
        ai = a[i]
        if ai == 0:
            continue
        for j in range(N - i):
            out[i + j] += ai * b[j]
    return out


def _pow(a: list[int], n: int, N: int) -> list[int]:
    result = [0] * N
    result[0] = 1
    base = a[:]
    while n:
        if n & 1:
            result = _mul(result, base, N)
        base = _mul(base, base, N)
        n >>= 1
    return result


def f_11_q_expansion(N: int) -> list[int]:
    """f_11(q) = q * prod_{n>=1}(1-q^n)^2 (1-q^{11n})^2, truncated
    to q^{N-1}.

    We build prod(1-q^n)^2 (1-q^{11n})^2 and then shift by q^1."""
    # N_inner enough to produce q^{N-1} in the final series (after the
    # q * shift), so we need N_inner = N (the shift is +1 but we cut to N).
    inner = _pow(eta_base_series(N, 1), 2, N)
    inner_11 = _pow(eta_base_series(N, 11), 2, N)
    prod = _mul(inner, inner_11, N)
    out = [0] * N
    for i in range(N - 1):
        out[i + 1] = prod[i]
    return out


# ----------------------------------------------------------------------
# Verifiers.
# ----------------------------------------------------------------------
def verify_hasse_bound_weierstrass(a: int, b: int,
                                      primes: list[int] | None = None) -> dict[str, Any]:
    if primes is None:
        primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]
    rows: list[dict[str, Any]] = []
    all_match = True
    for p in primes:
        disc = (-16 * (4 * a ** 3 + 27 * b ** 2)) % p
        if disc == 0:
            rows.append({"p": p, "bad_reduction": True})
            continue
        ap = a_p_weierstrass(a, b, p)
        bound = 2 * math.isqrt(p)
        match = abs(ap) <= bound + 1  # +1 for isqrt floor
        rows.append({"p": p, "a_p": ap, "2_sqrt_p_floor": bound, "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows, "curve": (a, b)}


def verify_hasse_bound_E11(primes: list[int] | None = None) -> dict[str, Any]:
    if primes is None:
        primes = [2, 3, 5, 7, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
    rows: list[dict[str, Any]] = []
    all_match = True
    for p in primes:
        ap = a_p_E11(p)
        bound_ceil = math.ceil(2 * math.sqrt(p))
        match = abs(ap) <= bound_ceil
        rows.append({"p": p, "a_p": ap, "2_sqrt_p_ceil": bound_ceil,
                     "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_eichler_shimura_E11(primes: list[int] | None = None,
                                 N: int = 80) -> dict[str, Any]:
    """a_p(E_11) = a_p(f_11) for p != 11."""
    if primes is None:
        primes = [2, 3, 5, 7, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
    f = f_11_q_expansion(N)
    rows: list[dict[str, Any]] = []
    all_match = True
    for p in primes:
        if p >= N:
            continue
        ap_curve = a_p_E11(p)
        ap_form = f[p]
        match = ap_curve == ap_form
        rows.append({
            "p": p,
            "a_p_E11": ap_curve,
            "a_p_f11": ap_form,
            "match": match,
        })
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows, "f_first_15": f[:15]}


def verify_f_11_leading_coefficients(N: int = 30) -> dict[str, Any]:
    """f_11 = q - 2q^2 - q^3 + 2q^4 + q^5 + 2q^6 - 2q^7 + 0 - 2q^9 + ...
       matches the modular-forms tabulation of S_2(Gamma_0(11))."""
    f = f_11_q_expansion(N)
    expected = {
        1: 1, 2: -2, 3: -1, 4: 2, 5: 1, 6: 2, 7: -2, 8: 0,
        9: -2, 10: -2, 11: 1, 12: -2, 13: 4, 14: 4, 15: -1, 16: -4,
    }
    rows: list[dict[str, Any]] = []
    all_match = True
    for n, e in expected.items():
        match = f[n] == e
        rows.append({"n": n, "f[n]": f[n], "expected": e, "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Specific small-curve sanity.
# ----------------------------------------------------------------------
def verify_curve_y2_x3_minus_x(primes: list[int] | None = None) -> dict[str, Any]:
    """For the CM curve y^2 = x^3 - x (conductor 32), we can cross-check
    Hasse by noting the supersingular primes (a_p = 0) are those with
    p == 3 mod 4 (Fermat)."""
    if primes is None:
        primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    rows: list[dict[str, Any]] = []
    for p in primes:
        ap = a_p_weierstrass(-1, 0, p)
        rows.append({
            "p": p,
            "p_mod_4": p % 4,
            "a_p": ap,
            "supersingular_predicted": p % 4 == 3,
            "is_supersingular": ap == 0,
            "ss_matches_prediction": (p % 4 == 3) == (ap == 0),
        })
    all_match = all(r["ss_matches_prediction"] for r in rows)
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    hasse_generic = verify_hasse_bound_weierstrass(-1, 0)
    hasse_E11 = verify_hasse_bound_E11()
    eichler = verify_eichler_shimura_E11()
    f11 = verify_f_11_leading_coefficients(N=30)
    cm_curve = verify_curve_y2_x3_minus_x()
    chain = {
        "hasse_bound_holds_for_y2_equals_x3_minus_x":
            hasse_generic["all_match"],
        "hasse_bound_holds_for_E11_over_primes_up_to_61":
            hasse_E11["all_match"],
        "eichler_shimura_a_p_E11_equals_a_p_f_11":
            eichler["all_match"],
        "f_11_leading_coefficients_match_newform_table":
            f11["all_match"],
        "y2_equals_x3_minus_x_CM_supersingular_at_p_equiv_3_mod_4":
            cm_curve["all_match"],
    }
    return {
        "hasse_generic": hasse_generic,
        "hasse_E11": hasse_E11,
        "eichler_shimura": eichler,
        "f_11_leading": f11,
        "cm_curve": cm_curve,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nf_11 first 15 q-coefficients (Eichler-Shimura modular form):")
    print(" ", s["eichler_shimura"]["f_first_15"])
    print("\nEichler-Shimura table E_11 vs f_11:")
    for row in s["eichler_shimura"]["rows"]:
        print(f"  p={row['p']:>3}: a_p(E_11)={row['a_p_E11']:>4}"
              f",  a_p(f_11)={row['a_p_f11']:>4},  match={row['match']}")
    print("\nCM curve y^2 = x^3 - x supersingular pattern:")
    for row in s["cm_curve"]["rows"]:
        print(f"  p={row['p']:>3} (p mod 4 = {row['p_mod_4']}):"
              f"  a_p={row['a_p']:>4}  ss_predicted={row['supersingular_predicted']}"
              f"  ss_actual={row['is_supersingular']}")
