"""
Phase CCLXI — Monster Dimension Count and j-Invariant Shell Identities
========================================================================

THEOREM (Monster Dimension Count):
  194 = λ(Φ₁₂ + f) = 2 × 97

The number of irreducible representations of the Monster group is
itself a W(3,3) parameter expression.

THEOREM (j-invariant constant term):
  744 = λ^q · q · (f+Φ₆) = 2³ · 3 · 31

The constant term of the j-invariant (j(τ) = q⁻¹ + 744 + 196884q + ...)
is a product of three W(3,3) shell atoms.

THEOREM (Inner atom–exponent q⁴ identity):
  Φ₃ · exp(Φ₃) + Φ₆ · exp(Φ₆) = q⁴ = 2v + 1 = 81

  where exp(Φ₃) = q and exp(Φ₆) = k/λ are the Monster-order exponents.

THEOREM (Multi-exponent product atom-purity):
  ∏ exp(pᵢ) = (2f−λ)(v/λ)(q²)(k/λ)(λ)(q) = λ⁵ q⁴ (q+λ)(f−1) = 298080

  All prime factors of the product of multi-exponents are shell atoms.

Extends Phases CCLVIII (15 shell atoms) and CCLX (Monster order anatomy).
"""
import json
import math
import pytest
from pathlib import Path
from collections import Counter

# ── W(3,3) parameters ──
q    = 3
v    = 40
k    = 12
lam  = 2
mu   = 4
f    = 24
g    = 15
s    = -(q + 1)  # -4
Phi3 = q**2 + q + 1   # 13
Phi4 = q**2 + 1        # 10
Phi6 = q**2 - q + 1    # 7
Phi12 = q**4 - q**2 + 1  # 73

ATOM_SET = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71}


def _prime_factors(n):
    """Return set of prime factors of n."""
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


# ================================================================
# T1: 194 = lam * (Phi12 + f)
# ================================================================
class TestT1_MonsterIrrepCount:
    """The number of Monster irreps is a W(3,3) expression."""

    def test_194_formula(self):
        assert lam * (Phi12 + f) == 194

    def test_components(self):
        assert Phi12 + f == 97

    def test_97_is_prime(self):
        assert all(97 % d != 0 for d in range(2, 10))

    def test_load_and_count(self):
        """Cross-check against bundled data."""
        p = Path(__file__).resolve().parent.parent / "data" / "monster_degrees.json"
        degs = json.loads(p.read_text(encoding="utf-8"))
        assert len(degs) == 194
        assert len(degs) == lam * (Phi12 + f)


# ================================================================
# T2: 744 = lam^q * q * (f + Phi6)
# ================================================================
class TestT2_JInvariant744:
    """The j-invariant constant term is a shell-atom product."""

    def test_744_formula(self):
        assert lam**q * q * (f + Phi6) == 744

    def test_744_factorization(self):
        assert 2**3 * 3 * 31 == 744

    def test_744_atoms_pure(self):
        """All prime factors of 744 are shell atoms."""
        assert _prime_factors(744).issubset(ATOM_SET)

    def test_f_plus_Phi6_is_31(self):
        assert f + Phi6 == 31

    def test_31_is_shell_atom(self):
        assert 31 in ATOM_SET


# ================================================================
# T3: Phi3*q + Phi6*(k/lam) = q^4 = 2v+1
# ================================================================
class TestT3_InnerQ4Identity:
    """Middle atom-exponent products sum to q⁴."""

    def test_sum_is_q4(self):
        assert Phi3 * q + Phi6 * (k // lam) == q**4

    def test_q4_is_81(self):
        assert q**4 == 81

    def test_2v_plus_1(self):
        assert q**4 == 2 * v + 1

    def test_individual_terms(self):
        assert Phi3 * q == 39      # v - 1
        assert Phi6 * (k // lam) == 42  # v + lam


# ================================================================
# T4: Product of multi-exponents is atom-pure
# ================================================================
class TestT4_MultiExponentProduct:
    """Product of the 6 multi-exponents factors into shell atoms."""

    MULTI_EXPS = [2*f - lam, v // lam, q**2, k // lam, lam, q]
    # = [46, 20, 9, 6, 2, 3]

    def test_values(self):
        assert self.MULTI_EXPS == [46, 20, 9, 6, 2, 3]

    def test_product_value(self):
        assert math.prod(self.MULTI_EXPS) == 298080

    def test_product_atom_pure(self):
        """All prime factors of 298080 are shell atoms."""
        assert _prime_factors(298080).issubset(ATOM_SET)

    def test_product_formula(self):
        """298080 = lam^5 * q^4 * (q+lam) * (f-1)."""
        assert lam**5 * q**4 * (q + lam) * (f - 1) == 298080

    def test_product_alt(self):
        """298080 = 2^5 * 3^4 * 5 * 23."""
        assert 2**5 * 3**4 * 5 * 23 == 298080


# ================================================================
# T5: Atom-exponent products have W(3,3) meanings
# ================================================================
class TestT5_AtomExponentProducts:
    """Each pᵢ · exp(pᵢ) is a recognizable W(3,3) expression."""

    def test_2_times_46(self):
        """lam * (2f-lam) = 2*(v+Phi6-1) = 92."""
        assert lam * (2*f - lam) == 92

    def test_3_times_20(self):
        """q * (v/lam) = 60 = q*v/lam."""
        assert q * (v // lam) == 60

    def test_5_times_9(self):
        """(q+lam) * q^2 = 45."""
        assert (q + lam) * q**2 == 45

    def test_7_times_6(self):
        """Phi6 * (k/lam) = 42 = v + lam."""
        assert Phi6 * (k // lam) == v + lam == 42

    def test_11_times_2(self):
        """(k-1) * lam = 22."""
        assert (k - 1) * lam == 22

    def test_13_times_3(self):
        """Phi3 * q = 39 = v - 1."""
        assert Phi3 * q == v - 1 == 39


# ================================================================
# T6: The inner/outer atom threshold
# ================================================================
class TestT6_InnerOuterThreshold:
    """Inner atoms are all <= Phi3 = 13; outer are all >= f-Phi6 = 17."""

    def test_inner_max(self):
        inner = {lam, q, q + lam, Phi6, k - 1, Phi3}
        assert max(inner) == 13 == Phi3

    def test_outer_min(self):
        outer = {f - Phi6, k + Phi6, f - 1, f + Phi6 - lam,
                 f + Phi6, v + 1, v + Phi6, v + k + Phi6, Phi12 - lam}
        assert min(outer) == 17 == f - Phi6

    def test_gap(self):
        """The gap between inner and outer is exactly 4 = mu = q+1."""
        assert (f - Phi6) - Phi3 == 4 == mu

    def test_gap_is_mu(self):
        assert 17 - 13 == mu


# ================================================================
# T7: 97 as Phi12 + f
# ================================================================
class TestT7_NinetySeven:
    """97 = Phi12 + f appears in the Monster irrep count 194 = 2*97."""

    def test_value(self):
        assert Phi12 + f == 97

    def test_prime(self):
        assert all(97 % d != 0 for d in range(2, 10))

    def test_alt_expression(self):
        """97 = q^4 - q^2 + 1 + q(q+1)(q+1)/2 ... let me check q^4 + f - q^2 + 1."""
        assert q**4 + f - q**2 + 1 == 97  # = 81 + 24 - 9 + 1 = 97


# ================================================================
# T8: Sum of inner atom*exp and outer contributions
# ================================================================
class TestT8_WeightedSums:
    """Weighted sum identities for the Monster order."""

    def test_inner_weighted_sum(self):
        """Sum p_i * e_i over inner atoms = 300."""
        inner_sum = (2*46 + 3*20 + 5*9 + 7*6 + 11*2 + 13*3)
        assert inner_sum == 300

    def test_300_formula(self):
        """300 = lam^2 * 3 * (q+lam)^2 = 4*75 = 4*3*25."""
        assert 300 == lam**2 * 3 * (q + lam)**2

    def test_outer_identity_sum(self):
        """Sum of outer atoms = 337 = sum of simple primes."""
        outer_sum = 17 + 19 + 23 + 29 + 31 + 41 + 47 + 59 + 71
        assert outer_sum == 337
