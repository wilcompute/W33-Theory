#!/usr/bin/env python3
"""
PART_CCCCCXLIV_C_BASE_SCAN.py

Scan small bases and measure how clearly each base makes the 7-structure and
W(3,3) mod-7/mod-12 patterns visible.

Metrics per base b:
  - factorization of b
  - ord_7(b)
  - whether 7 is a single digit (b > 7)
  - for b >= 10: period spectrum of 1/n, n=1..9
  - whether 1/7 has uniquely maximal period among n=1..9

This is exploratory and prints human-readable tables.
"""

from math import gcd


def factorize(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def multiplicative_order(base, mod):
    """Return ord_mod(base) if gcd(base, mod) == 1, else None."""
    if gcd(base, mod) != 1:
        return None
    x = base % mod
    k = 1
    while x != 1:
        x = (x * base) % mod
        k += 1
    return k


def period_1_over_n_in_base(n, base):
    """Return period length of 1/n in base `base` (0 if terminating)."""
    # 1/n terminates if all prime factors of n divide base
    base_primes = set(factorize(base))
    n_primes = set(factorize(n))
    if n_primes.issubset(base_primes):
        return 0
    # otherwise period is multiplicative order of base mod n' where n'
    # has factors 2 and 5 removed in the base-10 case; here we just use
    # coprimality heuristic when gcd(base, n) == 1.
    if gcd(base, n) != 1:
        # mixed case; we could strip gcd, but this is enough for small n.
        m = n
        g = gcd(base, m)
        while g != 1:
            m //= g
            g = gcd(base, m)
        if m == 1:
            return 0
        ordm = multiplicative_order(base, m)
        return ordm or 0
    ordn = multiplicative_order(base, n)
    return ordn or 0


def scan_bases(b_min=2, b_max=36):
    results = []
    for b in range(b_min, b_max + 1):
        fac = factorize(b)
        ord7 = multiplicative_order(b, 7)
        single_digit_7 = b > 7
        # For b >= 10, compute period spectrum for 1..9
        period_spectrum = None
        unique_max_7 = None
        if b >= 10:
            periods = {n: period_1_over_n_in_base(n, b) for n in range(1, 10)}
            max_p = max(periods.values())
            # unique maximal and attained at n=7?
            unique_max_7 = (
                periods[7] == max_p
                and list(periods.values()).count(max_p) == 1
            )
            period_spectrum = periods
        results.append({
            'b': b,
            'factors': fac,
            'ord7': ord7,
            'single_digit_7': single_digit_7,
            'period_spectrum': period_spectrum,
            'unique_max_7': unique_max_7,
        })
    return results


def main():
    q = 3
    g2 = 6
    print("=" * 80)
    print("SMALL-BASE SCAN FOR 7 / W(3,3) VISIBILITY")
    print("=" * 80)

    results = scan_bases(2, 36)

    print("\n1. ord_7(b) and primitive-root classes (2 ≤ b ≤ 36)")
    print("  b  | factors     | ord_7(b)")
    print("  " + "-" * 30)
    for r in results:
        b = r['b']
        fac = '×'.join(map(str, r['factors']))
        ord7 = r['ord7']
        tag = ""
        if ord7 == 6:
            tag = "  <-- full reptend for 7"
        print(f"  {b:2d} | {fac:<11s} | {str(ord7):>7s}{tag}")

    print("\n2. Bases with full-reptend 7 and single-digit 7 (b > 7, ord_7(b) = 6)")
    full_reptend_bases = [
        r for r in results if r['single_digit_7'] and r['ord7'] == 6
    ]
    if not full_reptend_bases:
        print("  None in scanned range.")
    else:
        print("  Candidates:")
        for r in full_reptend_bases:
            print(f"    b={r['b']:2d}, factors={r['factors']}")

    print("\n3. Period spectra for bases b ≥ 10")
    print("  For each base, show period(1/n) for n=1..9 and whether 1/7 is unique max.")
    for r in results:
        b = r['b']
        if b < 10:
            continue
        periods = r['period_spectrum']
        if periods is None:
            continue
        print("\n  Base b =", b)
        print("    periods (n: period):")
        for n in range(1, 10):
            print(f"      1/{n}: {periods[n]}")
        print(f"    ord_7({b}) = {r['ord7']}")
        print(f"    7 is single digit? {r['single_digit_7']}")
        print(f"    1/7 uniquely maximal period? {r['unique_max_7']}")

    print("\n4. High-visibility bases (heuristic)")
    print("  Criteria: b ≥ 10, ord_7(b) = 6, 7 single-digit, 1/7 unique max period for n=1..9.")
    hv = [
        r for r in results
        if r['b'] >= 10
        and r['ord7'] == 6
        and r['single_digit_7']
        and r['unique_max_7']
    ]
    if not hv:
        print("  No bases in 2..36 satisfy all criteria.")
    else:
        for r in hv:
            print(f"  b={r['b']}: factors={r['factors']}, ord_7(b)={r['ord7']}, unique_max_7={r['unique_max_7']}")

    print("\n5. Interpretation")
    print("  This scan empirically shows which small bases replicate the \"decimal miracle\":")
    print("  - full-reptend 7 (ord_7(b)=6),")
    print("  - 7 as a single digit, and")
    print("  - 1/7 carrying uniquely maximal period among 1..9.")
    print("  Base 10 is one such base; this script reveals whether any other bases up to 36")
    print("  share that visibility profile.")


if __name__ == '__main__':
    main()
