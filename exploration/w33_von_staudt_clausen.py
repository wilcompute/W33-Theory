"""Von Staudt-Clausen theorem and Kummer's irregular primes.

Theorem (von Staudt, Clausen, 1840).  For every even integer n >= 2,

    B_n + sum_{p prime, (p - 1) | n}  1/p    is an integer.

Equivalently the denominator of B_n in lowest terms equals exactly

    denom(B_n) = prod_{p prime, (p - 1) | n}  p.

Small examples:
    n =  2: (p - 1) | 2  <=>  p in {2, 3}.      denom(B_2)  = 6.
    n =  4:                   p in {2, 3, 5}.    denom(B_4)  = 30.
    n =  6:                   p in {2, 3, 7}.    denom(B_6)  = 42.
    n =  8:                   p in {2, 3, 5}.    denom(B_8)  = 30.
    n = 10:                   p in {2, 3, 11}.   denom(B_10) = 66.
    n = 12:                   p in {2, 3, 5, 7, 13}.  denom(B_12) = 2730.

Kummer's regularity (1850).  A prime p > 3 is *regular* iff p does not
divide the numerator of any of B_2, B_4, ..., B_{p - 3}.  The smallest
irregular primes are

    37, 59, 67, 101, 103, 131, 149, 157, ..., 691, ...

Kummer proved that for every regular prime p, Fermat's Last Theorem
holds at exponent p (the insoluble of x^p + y^p = z^p in nonzero
integers).  691 is irregular because 691 | numerator(B_12) -- this is
the exact same 691 that enters Ramanujan's tau congruence (Layer 63)
and zeta(-11) (Layer 61).

Six summary_chain pins below.

Layer 67 -- the arithmetic skeleton of Bernoulli numbers (which under-
wrote Layers 61 and 63) now pinned via its Gaussian-denominator law
(von Staudt-Clausen) and its irregularity detector (Kummer).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

from w33_zeta_functional_equation import bernoulli


# ----------------------------------------------------------------------
# Divisors of n and primes p with (p - 1) | n.
# ----------------------------------------------------------------------
def divisors(n: int) -> list[int]:
    if n < 1:
        return []
    divs = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            divs.append(d)
            if d != n // d:
                divs.append(n // d)
        d += 1
    return sorted(divs)


def _is_prime(p: int) -> bool:
    if p < 2:
        return False
    if p < 4:
        return True
    if p % 2 == 0:
        return False
    i = 3
    while i * i <= p:
        if p % i == 0:
            return False
        i += 2
    return True


def staudt_clausen_primes(n: int) -> list[int]:
    """Primes p with (p - 1) | n, for n >= 1 even."""
    return sorted({d + 1 for d in divisors(n) if _is_prime(d + 1)})


def staudt_clausen_denominator(n: int) -> int:
    """prod of primes p with (p - 1) | n."""
    out = 1
    for p in staudt_clausen_primes(n):
        out *= p
    return out


# ----------------------------------------------------------------------
# Integer part of B_n + sum 1/p.
# ----------------------------------------------------------------------
def integral_part_bernoulli(n: int) -> Fraction:
    """B_n + sum_{p: (p-1)|n} 1/p — predicted to be an integer for even n."""
    B = bernoulli(n)
    s = sum(Fraction(1, p) for p in staudt_clausen_primes(n))
    return B + s


# ----------------------------------------------------------------------
# Kummer's irregular-prime detector.
# ----------------------------------------------------------------------
def irregular_indices(p: int) -> list[int]:
    """List of even 2k with 2 <= 2k <= p - 3 for which p | numerator(B_{2k}).
    Empty list iff p is regular."""
    if p < 5 or not _is_prime(p):
        return []
    hits = []
    for k in range(1, (p - 1) // 2):
        two_k = 2 * k
        if two_k > p - 3:
            break
        B = bernoulli(two_k)
        # B = num / den ; p | num iff p | (B * den).numerator after reduction
        if B.numerator % p == 0:
            hits.append(two_k)
    return hits


def has_irregular_index(p: int, two_k: int) -> bool:
    """Return whether p divides numerator(B_two_k) for a valid Kummer index."""
    if p < 5 or not _is_prime(p) or two_k < 2 or two_k > p - 3 or two_k % 2:
        return False
    return bernoulli(two_k).numerator % p == 0


def is_regular_prime(p: int) -> bool:
    if p < 5 or not _is_prime(p):
        return True  # trivially for p = 2, 3 we skip; here we assume odd p >= 5
    for k in range(1, (p - 1) // 2):
        two_k = 2 * k
        if two_k > p - 3:
            break
        if has_irregular_index(p, two_k):
            return False
    return True


# ----------------------------------------------------------------------
# Verifiers.
# ----------------------------------------------------------------------
def verify_denominator_formula(n_max: int = 30) -> dict[str, Any]:
    """denom(B_n) = prod of primes p with (p - 1) | n for every even n
    up to n_max."""
    rows = []
    all_match = True
    for n in range(2, n_max + 1, 2):
        B = bernoulli(n)
        actual_den = B.denominator
        predicted = staudt_clausen_denominator(n)
        match = actual_den == predicted
        rows.append(
            {
                "n": n,
                "B_n": str(B),
                "actual_den": actual_den,
                "predicted_den": predicted,
                "primes": staudt_clausen_primes(n),
                "match": match,
            }
        )
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_integral_part(n_max: int = 30) -> dict[str, Any]:
    """B_n + sum_{p: (p-1)|n} 1/p is an integer for every even n <= n_max."""
    rows = []
    all_match = True
    for n in range(2, n_max + 1, 2):
        v = integral_part_bernoulli(n)
        match = v.denominator == 1
        rows.append(
            {
                "n": n,
                "integer_value": v.numerator if match else str(v),
                "is_integer": match,
            }
        )
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_first_irregular_primes() -> dict[str, Any]:
    """First irregular primes: 37, 59, 67, 101, 103, 131, 149, 157."""
    target = [37, 59, 67, 101, 103, 131, 149, 157]
    found: list[int] = []
    p = 5
    while len(found) < len(target) and p <= 200:
        if _is_prime(p) and not is_regular_prime(p):
            found.append(p)
        p += 2
    return {
        "expected": target,
        "found": found,
        "match": found == target,
    }


def verify_691_is_irregular_via_B_12() -> dict[str, Any]:
    """691 | numerator(B_12) = 691."""
    B12 = bernoulli(12)
    num_abs = abs(B12.numerator)
    return {
        "B_12": str(B12),
        "numerator_abs": num_abs,
        "is_691": num_abs == 691,
        "divides_by_691": num_abs % 691 == 0,
        "irregular_index": has_irregular_index(691, 12),
        "match": num_abs == 691 and has_irregular_index(691, 12),
    }


def verify_37_irregular_index() -> dict[str, Any]:
    """37 | numerator(B_32).  B_32 numerator = 7709321041217; 37 | that."""
    B32 = bernoulli(32)
    num_abs = abs(B32.numerator)
    return {
        "B_32_numerator_abs": num_abs,
        "mod_37": num_abs % 37,
        "divides_by_37": num_abs % 37 == 0,
        "irregular_index_32": 32 in irregular_indices(37),
        "match": (num_abs % 37 == 0) and (32 in irregular_indices(37)),
    }


def verify_small_primes_regular() -> dict[str, Any]:
    """5, 7, 11, 13, 17, 19, 23, 29, 31 are all regular (check)."""
    small = [5, 7, 11, 13, 17, 19, 23, 29, 31]
    rows = []
    all_match = True
    for p in small:
        reg = is_regular_prime(p)
        rows.append({"p": p, "regular": reg})
        all_match = all_match and reg
    return {"all_match": all_match, "rows": rows}


def verify_specific_denominators() -> dict[str, Any]:
    """Spot-check denom(B_n) for a few key n."""
    targets = {
        2: 6,  # 2 * 3
        4: 30,  # 2 * 3 * 5
        6: 42,  # 2 * 3 * 7
        8: 30,  # 2 * 3 * 5
        10: 66,  # 2 * 3 * 11
        12: 2730,  # 2 * 3 * 5 * 7 * 13
        14: 6,  # 2 * 3 (no 5, 7 since (p-1)|14 gives 2, 3, 8*no, 15*no, ...
        # wait (p-1)|14: divisors of 14 are 1,2,7,14, so p in {2,3,8,15};
        # primes are 2, 3 only.  denom = 6.
        16: 510,  # 2 * 3 * 5 * 17
        18: 798,  # 2 * 3 * 7 * 19
        20: 330,  # 2 * 3 * 5 * 11
        22: 138,  # 2 * 3 * 23
        24: 2730,  # 2 * 3 * 5 * 7 * 13
    }
    rows = []
    all_match = True
    for n, expected in targets.items():
        B = bernoulli(n)
        match = B.denominator == expected
        rows.append(
            {
                "n": n,
                "B_n": str(B),
                "actual_den": B.denominator,
                "expected_den": expected,
                "match": match,
            }
        )
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    den = verify_denominator_formula(n_max=30)
    integ = verify_integral_part(n_max=30)
    irreg = verify_first_irregular_primes()
    b691 = verify_691_is_irregular_via_B_12()
    b37 = verify_37_irregular_index()
    smallreg = verify_small_primes_regular()
    spec = verify_specific_denominators()
    chain = {
        "von_staudt_clausen_denominator_formula_up_to_n_30": den["all_match"],
        "von_staudt_clausen_integral_part_up_to_n_30": integ["all_match"],
        "first_eight_irregular_primes_are_37_59_67_101_103_131_149_157": irreg["match"],
        "691_is_irregular_via_B_12_numerator_equals_691": b691["match"],
        "37_is_irregular_at_index_32_via_B_32": b37["match"],
        "primes_5_through_31_all_regular": smallreg["all_match"],
        "specific_denominators_B_2_through_B_24": spec["all_match"],
    }
    return {
        "denominator_formula": den,
        "integral_part": integ,
        "irregular_primes": irreg,
        "b691": b691,
        "b37": b37,
        "small_regular": smallreg,
        "specific_dens": spec,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nVon Staudt-Clausen check: denominator of B_n:")
    for row in s["denominator_formula"]["rows"][:8]:
        print(
            f"  n={row['n']:>3}: B_n = {row['B_n']:<25} "
            f"den = {row['actual_den']:>5} "
            f"=  prod({row['primes']})"
        )
    print(f"\nFirst irregular primes: {s['irregular_primes']['found']}")
    print(
        f"691 is irregular? "
        f"numerator(B_12) = {s['b691']['numerator_abs']}, "
        f"match = {s['b691']['match']}"
    )
    print(
        f"37 is irregular at index 32? "
        f"B_32 num mod 37 = {s['b37']['mod_37']}, "
        f"match = {s['b37']['match']}"
    )
