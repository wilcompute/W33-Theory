"""
JACOBI TRIPLE PRODUCT
=====================

    prod_{n>=1} (1 - x^n)(1 + x^{n - 1/2} y)(1 + x^{n - 1/2} y^{-1})
        = sum_{k in Z} x^{k^2 / 2} y^k.

To avoid half-integers, substitute x -> q^2, y -> z, giving the more
common integer form

    prod (1 - q^{2n})(1 + q^{2n-1} z)(1 + q^{2n-1} z^{-1})
        = sum_{k in Z} q^{k^2} z^k.                               (*)

From (*) three classical identities fall out by specialisation:

(a) Pentagonal theorem (Euler).
    Put  q -> q^{3/2},  z = -q^{-1/2}.  After clearing half-integer
    exponents, the left side becomes  prod (1 - q^n)  and the right
    side becomes  sum_{k in Z} (-1)^k q^{k(3k-1)/2}.

(b) Triangular-number theta (Gauss).
    z = 1  gives  theta_2(q) / (2 q^{1/4})-flavoured identity.
    A cleaner triangular form: set z = q in (*):
        prod (1 - q^{2n})(1 + q^{2n})^2 = sum_{k in Z} q^{k^2 + k}
    and since k^2 + k = 2 * T_k with T_k = k(k+1)/2,
        sum_{k>=0} q^{T_k}  = (1/2) sum_{k in Z} q^{k(k+1)/2}
    is the triangular theta series.

(c) Sum of four squares (Jacobi).
    theta_3(q)^4 = 1 + 8 sum_{n>=1, 4 does not divide n} sigma_1(n) q^n
    where theta_3(q) = sum_{k in Z} q^{k^2}.  The coefficient of q^n
    counts r_4(n), the number of ways to write n as an ordered sum of
    four squares (including signs and zero), and equals 8 sigma(n) when
    n is odd and 24 * sigma(largest odd divisor of n) when n is even.

BRIDGE TO W(3,3).

The k = 12 valency sits inside this identity in two distinct guises:
    * Pentagonal expansion of prod(1-q^n) feeds eta, and eta^{2k} = Delta.
    * theta_3(q)^{24} specialisation (Jacobi theta series raised to 2k)
      governs lattice theta series in dimension 24 (Leech, etc.).
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


# ======================================================================
#  Truncated Laurent series in z over Q[[q]].
#  Represent as dict (k -> list of q-coefficients, i.e. polynomial in q).
# ======================================================================
def _series_mul(A: dict, B: dict, q_order: int) -> dict:
    """Multiply two Laurent series in z with polynomial-in-q coefficients."""
    out: dict = {}
    for ka, pa in A.items():
        for kb, pb in B.items():
            k = ka + kb
            row = out.setdefault(k, [0] * (q_order + 1))
            for i, ca in enumerate(pa):
                if ca == 0:
                    continue
                if i > q_order:
                    break
                for j, cb in enumerate(pb):
                    if i + j > q_order or cb == 0:
                        continue
                    row[i + j] += ca * cb
    return out


def _series_one() -> dict:
    return {0: [1]}


def jacobi_lhs(q_order: int, z_range: int) -> dict:
    """Compute prod (1 - q^{2n})(1 + q^{2n-1} z)(1 + q^{2n-1} z^{-1})
    truncated to q^q_order and |k| <= z_range."""
    out = _series_one()
    n = 1
    while 2 * n - 1 <= q_order:
        # Factor A(n) = 1 - q^{2n}
        if 2 * n <= q_order:
            A = {0: [0] * (q_order + 1)}
            A[0][0] = 1
            A[0][2 * n] = -1
            out = _series_mul(out, A, q_order)
        # Factor B(n) = 1 + q^{2n-1} z
        B = {0: [0] * (q_order + 1), 1: [0] * (q_order + 1)}
        B[0][0] = 1
        B[1][2 * n - 1] = 1
        out = _series_mul(out, B, q_order)
        # Factor C(n) = 1 + q^{2n-1} z^{-1}
        C = {0: [0] * (q_order + 1), -1: [0] * (q_order + 1)}
        C[0][0] = 1
        C[-1][2 * n - 1] = 1
        out = _series_mul(out, C, q_order)
        n += 1
    # Trim to |k| <= z_range
    return {k: v for k, v in out.items() if abs(k) <= z_range}


def jacobi_rhs(q_order: int, z_range: int) -> dict:
    """sum_{k = -z_range..z_range} q^{k^2} z^k, truncated to q^q_order."""
    out: dict = {}
    for k in range(-z_range, z_range + 1):
        e = k * k
        if e > q_order:
            continue
        row = [0] * (q_order + 1)
        row[e] = 1
        out[k] = row
    return out


def verify_jacobi_triple(q_order: int = 30, z_range: int = 6) -> dict:
    """Check LHS = RHS as power series in q, Laurent in z."""
    L = jacobi_lhs(q_order, z_range)
    R = jacobi_rhs(q_order, z_range)
    all_k = sorted(set(L) | set(R))
    mismatches = []
    for k in all_k:
        lv = L.get(k, [0] * (q_order + 1))
        rv = R.get(k, [0] * (q_order + 1))
        # Pad
        lv = lv + [0] * (q_order + 1 - len(lv))
        rv = rv + [0] * (q_order + 1 - len(rv))
        for i in range(q_order + 1):
            if lv[i] != rv[i]:
                mismatches.append((k, i, lv[i], rv[i]))
    return {
        "q_order":      q_order,
        "z_range":      z_range,
        "mismatches":   mismatches,
        "all_match":    len(mismatches) == 0,
        "sample_k0":    L.get(0, [])[:10],
        "sample_k1":    L.get(1, [])[:10],
    }


# ======================================================================
#  Specialisation (a): Euler's pentagonal theorem.
#
#  Set z = -q in (*):  product side becomes
#      prod (1 - q^{2n}) (1 - q^{2n})(1 - q^{2n-2})
#  which, after index shift, collapses to prod (1 - q^n) * something.
#
#  Cleaner route: in (*), replace q -> q^{3/2}, z = -q^{-1/2} gives
#      prod (1 - q^n)   on LHS
#      sum (-1)^k q^{k(3k-1)/2}  on RHS.
#
#  We can avoid half-integers by verifying the IDENTITY ITSELF in the
#  "q^2, -q" substitution: z = -q in (*) gives
#      prod (1 - q^{2n})(1 - q^{2n-1+1})(1 - q^{2n-1-1})
#        = prod (1 - q^{2n})(1 - q^{2n})(1 - q^{2n-2}).
#  This is not the pentagonal form directly; the true pentagonal
#  specialisation needs the half-integer substitution.
#
#  Instead, we do a DIRECT verification:
#      prod (1 - q^n)  ==  sum (-1)^k q^{k(3k-1)/2}
#  which is what the pentagonal theorem says, and which is recovered
#  from Jacobi via the half-integer substitution.
# ======================================================================
def pentagonal_from_jacobi_check(q_order: int = 30) -> dict:
    """Direct check prod (1-q^n) = Euler pentagonal series, as a pin of the
    half-integer specialisation of Jacobi."""
    # prod (1-q^n)
    prod = [0] * (q_order + 1)
    prod[0] = 1
    for n in range(1, q_order + 1):
        new = prod[:]
        for i in range(q_order + 1 - n):
            new[i + n] -= prod[i]
        prod = new
    # pentagonal sum
    pent = [0] * (q_order + 1)
    pent[0] = 1
    k = 1
    while True:
        e1 = k * (3 * k - 1) // 2
        e2 = k * (3 * k + 1) // 2
        if e1 > q_order and e2 > q_order:
            break
        sign = (-1) ** k
        if e1 <= q_order:
            pent[e1] += sign
        if e2 <= q_order:
            pent[e2] += sign
        k += 1
    return {
        "q_order":   q_order,
        "prod":      prod,
        "pentagon":  pent,
        "all_match": prod == pent,
    }


# ======================================================================
#  Specialisation (c): theta_3(q)^4 and r_4(n).
#
#  theta_3(q) = sum_{k in Z} q^{k^2}  (the k=0 row of Jacobi RHS at z=1).
#  Jacobi's four-square theorem:
#      r_4(n) = 8 * sum_{d | n, 4 not | d} d.
# ======================================================================
def theta3(q_order: int) -> list:
    """theta_3(q) = sum_{k in Z} q^{k^2}."""
    out = [0] * (q_order + 1)
    k = 0
    while k * k <= q_order:
        if k == 0:
            out[0] += 1
        else:
            out[k * k] += 2  # k and -k
        k += 1
    return out


def poly_mul(A: list, B: list, q_order: int) -> list:
    out = [0] * (q_order + 1)
    for i, a in enumerate(A):
        if a == 0 or i > q_order:
            continue
        for j, b in enumerate(B):
            if i + j > q_order or b == 0:
                continue
            out[i + j] += a * b
    return out


def theta3_to_the_4(q_order: int) -> list:
    t = theta3(q_order)
    t2 = poly_mul(t, t, q_order)
    t4 = poly_mul(t2, t2, q_order)
    return t4


def r4_jacobi(n: int) -> int:
    """r_4(n) = 8 * sum_{d | n, 4 does not divide d} d."""
    if n == 0:
        return 1
    s = 0
    for d in range(1, n + 1):
        if n % d == 0 and d % 4 != 0:
            s += d
    return 8 * s


def verify_r4(q_order: int = 20) -> dict:
    t4 = theta3_to_the_4(q_order)
    jacobi = [r4_jacobi(n) for n in range(q_order + 1)]
    return {
        "q_order":     q_order,
        "theta3^4":    t4,
        "jacobi_r4":   jacobi,
        "all_match":   t4 == jacobi,
        "mismatches":  [(n, t4[n], jacobi[n]) for n in range(q_order + 1) if t4[n] != jacobi[n]],
    }


# ======================================================================
#  Specialisation (b): triangular theta.
#  sum_{k>=0} q^{T_k} with T_k = k(k+1)/2
#  comes from Jacobi via z = q, then dividing.
# ======================================================================
def triangular_theta(q_order: int) -> list:
    out = [0] * (q_order + 1)
    k = 0
    while k * (k + 1) // 2 <= q_order:
        out[k * (k + 1) // 2] += 1
        k += 1
    return out


def jacobi_at_z_equals_q(q_order: int) -> list:
    """[q^n] RHS of Jacobi at z = q:
        sum_{k in Z} q^{k^2} * q^k = sum_{k in Z} q^{k^2+k} = sum_{k in Z} q^{2 T_k}
    which equals 1 + 2 sum_{k>=1} q^{2 T_k}  (k and -(k+1) give the same value? no:
    k^2+k evaluated at k and -1-k gives (-1-k)^2 + (-1-k) = k^2 + 2k + 1 - 1 - k = k^2+k).
    So each value 2 T_k is hit exactly twice for k != -1/2, meaning all k in Z contribute."""
    out = [0] * (q_order + 1)
    for k in range(-q_order - 1, q_order + 2):
        e = k * k + k
        if 0 <= e <= q_order:
            out[e] += 1
    return out


def verify_triangular_identity(q_order: int = 30) -> dict:
    """sum_{k in Z} q^{k^2+k} = 2 * sum_{k>=0} q^{2T_k}
    (because k and -1-k collide on k^2+k)."""
    lhs = jacobi_at_z_equals_q(q_order)
    rhs = [2 * c for c in triangular_theta(q_order // 2)]
    # Embed rhs at even indices: q^{2T_k}
    rhs_full = [0] * (q_order + 1)
    k = 0
    while 2 * (k * (k + 1) // 2) <= q_order:
        rhs_full[2 * (k * (k + 1) // 2)] = 2
        k += 1
    return {
        "q_order":   q_order,
        "lhs":       lhs[:20],
        "rhs":       rhs_full[:20],
        "all_match": lhs == rhs_full,
    }


# ======================================================================
#  Driver.
# ======================================================================
def derive_all_jacobi(q_order: int = 30) -> dict:
    triple = verify_jacobi_triple(q_order=q_order, z_range=5)
    pent = pentagonal_from_jacobi_check(q_order=q_order)
    r4 = verify_r4(q_order=20)
    tri = verify_triangular_identity(q_order=q_order)
    return {
        "jacobi_triple_product":  triple,
        "pentagonal_specialisation": pent,
        "four_squares_r4":        r4,
        "triangular_identity":    tri,
        "summary_chain": {
            "jacobi_triple_LHS_equals_RHS":          triple["all_match"],
            "pentagonal_matches_prod_1_minus_q_n":   pent["all_match"],
            "theta3^4_equals_jacobi_r4":             r4["all_match"],
            "triangular_theta_identity":             tri["all_match"],
        },
    }


def main() -> None:
    print("=" * 72)
    print("  JACOBI TRIPLE PRODUCT AND SPECIALISATIONS")
    print("=" * 72)
    print()

    triple = verify_jacobi_triple(q_order=20, z_range=5)
    print(f"  Jacobi triple product LHS == RHS  (q<=20, |k|<=5): {triple['all_match']}")
    print(f"    z^0 row: {triple['sample_k0'][:10]}")
    print(f"    z^1 row: {triple['sample_k1'][:10]}")
    print()

    pent = pentagonal_from_jacobi_check(q_order=30)
    print(f"  Pentagonal specialisation: prod(1-q^n) matches pentagonal sum: {pent['all_match']}")
    print(f"    prod (1-q^n) first 13 coefs: {pent['prod'][:13]}")
    print()

    r4 = verify_r4(q_order=20)
    print(f"  theta_3(q)^4 matches Jacobi r_4(n) = 8 sum_{{d|n, 4 not | d}} d: {r4['all_match']}")
    print(f"    theta_3^4 first 11 coefs: {r4['theta3^4'][:11]}")
    print(f"    r_4(n) via Jacobi formula: {r4['jacobi_r4'][:11]}")
    print()

    tri = verify_triangular_identity(q_order=30)
    print(f"  Triangular identity (Jacobi at z=q): {tri['all_match']}")
    print()

    chain = derive_all_jacobi(30)
    print("  SUMMARY CHAIN:")
    for k, v in chain["summary_chain"].items():
        print(f"    {k}: {v}")
    print()

    out = Path(__file__).resolve().parent.parent / "data" / "w33_jacobi_triple.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
