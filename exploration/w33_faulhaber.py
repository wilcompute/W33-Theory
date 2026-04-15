"""
FAULHABER'S FORMULA -- power sums as exact polynomials in N.
============================================================

The FINITE counterpart to the infinite zeta tower.  Where

    zeta(2 n)  =  sum_{k >= 1}  1 / k^(2 n)   =   (2 pi)^(2 n) |B_{2 n}| / (2 (2 n)!)

is the INFINITE sum, Faulhaber's formula gives the FINITE sum

    S_p(N)  :=  sum_{k = 1}^{N}  k^p
            =   (1 / (p + 1))  sum_{j = 0}^{p}  C(p + 1, j)  B_j^+  N^(p + 1 - j)

as an exact polynomial of degree  p + 1  in  N.  Here  B_j^+ = B_j  for  j != 1
and  B_1^+ = +1/2  (Faulhaber / "plus" convention).

FAULHABER'S THEOREM.  For odd  p = 2 m + 1  with  m >= 1,  S_p(N)  is a
polynomial in  N (N + 1)  (equivalently in  S_1(N) = N(N+1)/2 ).  In
particular  S_3(N)  =  S_1(N)^2,  the classical "sum of cubes = square of
sum" identity.

FIRST TEN POLYNOMIALS.

    S_0(N)  =  N
    S_1(N)  =  N (N + 1) / 2
    S_2(N)  =  N (N + 1) (2 N + 1) / 6
    S_3(N)  =  N^2 (N + 1)^2 / 4
    S_4(N)  =  N (N + 1) (2 N + 1) (3 N^2 + 3 N - 1) / 30
    S_5(N)  =  N^2 (N + 1)^2 (2 N^2 + 2 N - 1) / 12
    ...

BRIDGE TO W(3,3).

    S_1(v)  =  v (v + 1) / 2  =  40 * 41 / 2  =  820       (triangular number of v=40)
    S_2(v)  =  v (v + 1) (2 v + 1) / 6  =  40 * 41 * 81 / 6  =  22140   (square-pyramidal)
    S_3(v)  =  S_1(v)^2   =  820^2  =  672400
    S_1(k)  =  k (k + 1) / 2  =  12 * 13 / 2  =  78         (= Phi_3(3) * 6)
    S_2(k)  =  k (k + 1) (2 k + 1) / 6  =  12 * 13 * 25 / 6 =  650

Each S_p(v), S_p(k), S_p(nn) is a RATIONAL closure in the SRG invariants.

EULER-MACLAURIN BRIDGE.  As  N -> oo,

    S_p(N)  =  N^(p+1) / (p + 1)  +  N^p / 2  +  O(N^(p-1))

recovers  integral_0^N x^p dx + (leading trapezoid correction).  The
Bernoulli corrections beyond the leading term are exactly the subleading
coefficients of  S_p(N).
"""
from __future__ import annotations

import json
from fractions import Fraction
from math import comb
from pathlib import Path

from w33_bernoulli_zeta import bernoulli


Poly = list  # list[Fraction], coefficients low-to-high


# ======================================================================
#  Bernoulli (plus convention):  B_j^+  =  B_j  for  j != 1,  B_1^+ = +1/2.
# ======================================================================
def bernoulli_plus(n: int) -> Fraction:
    b = bernoulli(n)
    return -b if n == 1 else b


# ======================================================================
#  Polynomial helpers.
# ======================================================================
def pstrip(p: Poly) -> Poly:
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def peval(p: Poly, x) -> Fraction:
    out = Fraction(0)
    for c in reversed(p):
        out = out * x + c
    return out


def pstr(p: Poly, var: str = "N") -> str:
    terms = []
    for deg in range(len(p) - 1, -1, -1):
        c = p[deg]
        if c == 0:
            continue
        sign = " + " if c > 0 and terms else (" - " if c < 0 and terms else ("-" if c < 0 else ""))
        cab = abs(c)
        if deg == 0:
            body = str(cab)
        elif deg == 1:
            body = var if cab == 1 else f"{cab} {var}"
        else:
            body = f"{var}^{deg}" if cab == 1 else f"{cab} {var}^{deg}"
        terms.append(f"{sign}{body}")
    return "".join(terms) or "0"


# ======================================================================
#  Faulhaber polynomial.
#
#      S_p(N)  =  (1 / (p + 1))  sum_{j = 0}^{p}  C(p + 1, j)  B_j^+  N^(p + 1 - j).
# ======================================================================
def faulhaber_poly(p: int) -> Poly:
    assert p >= 0
    out = [Fraction(0)] * (p + 2)
    for j in range(p + 1):
        exponent = p + 1 - j
        coef = Fraction(comb(p + 1, j)) * bernoulli_plus(j) / Fraction(p + 1)
        out[exponent] = coef
    return pstrip(out)


def power_sum_direct(N: int, p: int) -> int:
    """Direct sum  sum_{k = 1}^{N} k^p   for cross-verification."""
    return sum(k ** p for k in range(1, N + 1))


# ======================================================================
#  Faulhaber's theorem for odd p.
#
#  S_{2 m + 1}(N)  is a polynomial in  u = N (N + 1)  of degree  m + 1.
# ======================================================================
def faulhaber_in_u(p: int) -> list:
    """Return the coefficients of S_p(N) as a polynomial in u = N(N+1).

    Returns [c_0, c_1, ..., c_{m+1}] where  S_p(N) = sum_k  c_k  u^k.
    Only defined for odd p >= 1.  For even p this function returns None.
    """
    if p < 1 or p % 2 == 0:
        return None
    # Compute S_p(N) then reduce in u = N(N+1).
    S = faulhaber_poly(p)
    # Substitute: use the fact that S_p(N) = polynomial in u.
    # Strategy: evaluate S_p at (m+2) distinct integer N values, get u values,
    # and Lagrange-interpolate a polynomial in u.
    m = (p - 1) // 2
    degree_in_u = m + 1
    pts_u = []
    pts_s = []
    for N in range(1, degree_in_u + 2):
        u = N * (N + 1)
        if u in pts_u:
            continue
        pts_u.append(Fraction(u))
        pts_s.append(peval(S, N))
    # Lagrange interpolation for polynomial in u.
    coefs = [Fraction(0)] * (degree_in_u + 1)
    for i in range(degree_in_u + 1):
        # Lagrange basis L_i(u) = prod_{j != i} (u - pts_u[j]) / (pts_u[i] - pts_u[j])
        num_poly = [Fraction(1)]  # polynomial in u
        denom = Fraction(1)
        for j in range(degree_in_u + 1):
            if j == i:
                continue
            # multiply num_poly by (u - pts_u[j])
            new_poly = [Fraction(0)] * (len(num_poly) + 1)
            for k, c in enumerate(num_poly):
                new_poly[k] -= c * pts_u[j]
                new_poly[k + 1] += c
            num_poly = new_poly
            denom *= (pts_u[i] - pts_u[j])
        # accumulate pts_s[i] * num_poly / denom
        for k, c in enumerate(num_poly):
            coefs[k] += pts_s[i] * c / denom
    return pstrip(coefs)


# ======================================================================
#  Euler-Maclaurin leading-term verification.
# ======================================================================
def euler_maclaurin_leading(p: int) -> dict:
    """S_p(N) asymptotic expansion.

        S_p(N)  =  N^{p+1}/(p+1)  +  N^p / 2  +  (p / 12) N^{p-1}  +  ...

    Return the first three terms' exact coefficients (from faulhaber_poly).
    """
    S = faulhaber_poly(p)
    # degrees p+1, p, p-1 (the last exists only for p >= 1)
    c_lead = S[p + 1] if p + 1 < len(S) else Fraction(0)
    c_sub1 = S[p] if p < len(S) else Fraction(0)
    c_sub2 = S[p - 1] if p - 1 >= 0 and p - 1 < len(S) else Fraction(0)
    return {
        "p":                 p,
        "leading_coef":      str(c_lead),
        "subleading_coef":   str(c_sub1),
        "sub_subleading":    str(c_sub2),
        "expected_leading":  str(Fraction(1, p + 1)),
        "expected_subleading": "1/2",
        "leading_ok":        c_lead == Fraction(1, p + 1),
        "subleading_ok":     c_sub1 == Fraction(1, 2) if p >= 1 else True,
    }


# ======================================================================
#  W(3,3) / SRG closures via Faulhaber at the graph invariants.
# ======================================================================
def srg_faulhaber_closures() -> dict:
    """Evaluate  S_p  at the SRG constants  v = 40, k = 12, mu = 4, nn = 27.

    Each value is an exact rational (in fact integer) closure.
    """
    v, k, mu, nn = 40, 12, 4, 27
    out = {}
    for p in range(0, 5):
        S = faulhaber_poly(p)
        out[f"S_{p}"] = {
            "S_p(v=40)":   int(peval(S, v)),
            "S_p(k=12)":   int(peval(S, k)),
            "S_p(mu=4)":   int(peval(S, mu)),
            "S_p(nn=27)":  int(peval(S, nn)),
        }
    return out


# ======================================================================
#  Driver.
# ======================================================================
def derive_all_faulhaber(max_p: int = 8) -> dict:
    polys = {}
    for p in range(0, max_p + 1):
        S = faulhaber_poly(p)
        polys[f"S_{p}(N)"] = {
            "coefficients_lowest_to_highest": [str(c) for c in S],
            "pretty": pstr(S),
            "leading": str(Fraction(1, p + 1)),
        }

    # Faulhaber's theorem for odd p.
    faulhaber_u = {}
    for p in (1, 3, 5, 7, 9):
        in_u = faulhaber_in_u(p)
        faulhaber_u[f"S_{p}(N) as poly in u=N(N+1)"] = [str(c) for c in in_u]

    # Sum of cubes = square of sum.
    S1 = faulhaber_poly(1)
    S3 = faulhaber_poly(3)
    # S_3(N) == S_1(N)^2 as polynomials.
    # Compute S_1(N)^2 explicitly and compare.
    S1_sq = [Fraction(0)] * (2 * len(S1) - 1)
    for i, a in enumerate(S1):
        for j, b in enumerate(S1):
            S1_sq[i + j] += a * b
    S1_sq = pstrip(S1_sq)
    sum_cubes_identity = (S3 == S1_sq)

    # Euler-Maclaurin leading terms.
    em = {f"S_{p}": euler_maclaurin_leading(p) for p in range(1, 8)}

    # SRG closures.
    srg_closures = srg_faulhaber_closures()

    # Direct verification for small N, random p.
    checks = []
    for p in range(0, 6):
        for N in (10, 50, 100):
            S = faulhaber_poly(p)
            formula = int(peval(S, N))
            direct = power_sum_direct(N, p)
            checks.append({"p": p, "N": N, "formula": formula,
                           "direct": direct, "ok": formula == direct})

    return {
        "faulhaber_polynomials":               polys,
        "odd_faulhaber_in_u=N(N+1)":            faulhaber_u,
        "sum_of_cubes_equals_square_of_sum":    sum_cubes_identity,
        "euler_maclaurin_leading_terms":       em,
        "srg_faulhaber_closures":               srg_closures,
        "direct_verification":                 checks,
    }


def main() -> None:
    print("=" * 72)
    print("  FAULHABER'S FORMULA  --  power sums as exact polynomials")
    print("=" * 72)
    print()

    print("  FAULHABER POLYNOMIALS  S_p(N) = sum_{k=1}^N k^p :")
    for p in range(0, 9):
        S = faulhaber_poly(p)
        print(f"    S_{p}(N) = {pstr(S)}")
    print()

    print("  FAULHABER'S THEOREM (odd p):  S_p(N) as polynomial in  u = N(N+1):")
    for p in (1, 3, 5, 7, 9):
        in_u = faulhaber_in_u(p)
        terms = []
        for k, c in enumerate(in_u):
            if c == 0:
                continue
            term = f"{c}" if k == 0 else (f"u^{k}" if c == 1 else f"{c} u^{k}")
            terms.append(term)
        print(f"    S_{p}(N) = {' + '.join(terms)}")
    print()

    S1 = faulhaber_poly(1)
    S3 = faulhaber_poly(3)
    S1_sq = [Fraction(0)] * (2 * len(S1) - 1)
    for i, a in enumerate(S1):
        for j, b in enumerate(S1):
            S1_sq[i + j] += a * b
    S1_sq = pstrip(S1_sq)
    print(f"  SUM-OF-CUBES IDENTITY:  S_3(N) == S_1(N)^2  ?  {S3 == S1_sq}")
    print(f"    S_1(N)^2 = {pstr(S1_sq)}")
    print(f"    S_3(N)   = {pstr(S3)}")
    print()

    print("  EULER-MACLAURIN LEADING TERMS:  S_p(N) = N^{p+1}/(p+1) + N^p/2 + ...")
    for p in (1, 2, 3, 4, 5, 6, 7):
        em = euler_maclaurin_leading(p)
        print(f"    S_{p}: lead = {em['leading_coef']},"
              f"  sublead = {em['subleading_coef']},"
              f"  sub-sub = {em['sub_subleading']}")
    print()

    print("  SRG FAULHABER CLOSURES (power sums at the graph constants):")
    closures = srg_faulhaber_closures()
    for name, row in closures.items():
        print(f"    {name}: {row}")
    print()

    chain = derive_all_faulhaber(max_p=10)
    out = Path(__file__).resolve().parent.parent / "data" / "w33_faulhaber.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
