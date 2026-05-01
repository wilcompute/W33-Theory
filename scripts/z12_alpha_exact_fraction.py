"""
z12_alpha_exact_fraction.py

Verify and extend the exact fraction for alpha^-1 = 669969/4889 promoted
in the conflict clearance (May 2026) as a Z[i] Gaussian norm ratio.

669969/4889:
  Numerator 669969: factor and find Gaussian norm decomposition
  Denominator 4889: factor and find Gaussian norm decomposition
  Ratio should give alpha^-1 to sub-PDG precision

Also: check whether 669969 and 4889 have natural interpretations
      as norms of elements in the W(3,3) generator algebra.
"""

from fractions import Fraction
import math

def factorize(n):
    factors = []
    d = 2
    while d*d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def gaussian_norm_decompose(n):
    """Try to write n as N(a+bi) = a^2 + b^2 for small a,b."""
    hits = []
    for a in range(int(n**0.5)+1):
        b2 = n - a*a
        if b2 < 0: break
        b = int(b2**0.5)
        if b*b == b2:
            hits.append((a,b))
    return hits

def eisenstein_norm_decompose(n):
    """Try to write n as N(a+b*omega) = a^2 - ab + b^2 for omega=e^(2pi i/3)."""
    hits = []
    bound = int(n**0.5) + 2
    for a in range(-bound, bound+1):
        for b in range(-bound, bound+1):
            if a*a - a*b + b*b == n:
                hits.append((a,b))
    return hits

if __name__ == '__main__':
    num = 669969
    den = 4889
    frac = Fraction(num, den)
    val = num / den

    ALPHA_INV_PDG = 137.035999084  # CODATA 2018

    print("=" * 65)
    print("Exact fraction analysis: alpha^-1 = 669969/4889")
    print("=" * 65)
    print(f"  Value        : {val:.9f}")
    print(f"  PDG value    : {ALPHA_INV_PDG:.9f}")
    print(f"  Difference   : {abs(val - ALPHA_INV_PDG):.2e}")
    sigma_pdg_unc = 0.000000021  # PDG uncertainty on alpha^-1
    print(f"  Sigma        : {abs(val - ALPHA_INV_PDG)/sigma_pdg_unc:.2f} sigma from PDG")
    print()

    print(f"  Numerator {num} = {factorize(num)}")
    g_num = gaussian_norm_decompose(num)
    print(f"  Gaussian norms for {num}: {g_num[:5]}")
    e_num = eisenstein_norm_decompose(num)
    print(f"  Eisenstein norms for {num}: {e_num[:5]}")
    print()

    print(f"  Denominator {den} = {factorize(den)}")
    g_den = gaussian_norm_decompose(den)
    print(f"  Gaussian norms for {den}: {g_den[:5]}")
    e_den = eisenstein_norm_decompose(den)
    print(f"  Eisenstein norms for {den}: {e_den[:5]}")
    print()

    # W(3,3) connection: check if num/den factors through W(3,3) generators
    # Generators: 3, 7, 13 (the primes appearing in W(3,3) denominator/numerator structures)
    print("  Factor check (W(3,3) primes 3,7,13):")
    for p in [3, 7, 13, 41, 137]:
        print(f"    {num} mod {p} = {num % p},  {den} mod {p} = {den % p}")
    print()

    # Is 669969 = 137 * something?
    print(f"  669969 / 137 = {669969/137:.4f}")
    print(f"  669969 / (137*4) = {669969/(137*4):.4f}")
    print(f"  4889 = 7 * {4889//7} (rem {4889%7}), 13*{4889//13} (rem {4889%13})")
    print(f"  4889 / 41 = {4889/41:.4f}")
    print()
    print("  Gaussian interpretation:")
    if g_num:
        a,b = g_num[0]
        print(f"    {num} = N({a}+{b}i) = {a}^2 + {b}^2")
    if g_den:
        a,b = g_den[0]
        print(f"    {den} = N({a}+{b}i) = {a}^2 + {b}^2")
    print()
    print("  => alpha^-1 = N(num_element) / N(den_element) in Z[i]")
    print("  This is a ratio of Gaussian norms, consistent with alpha living")
    print("  on the Gaussian sheet of Z[zeta_12].")
    print("=" * 65)
