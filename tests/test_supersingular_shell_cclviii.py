"""
Phase CCLVIII — Supersingular Shell Theorem: 15 W(3,3) Atoms = Monster Support
================================================================================

THEOREM: The 15 prime divisors of |M| (the supersingular primes)
are *exactly* the 15 primes obtainable from W(3,3) parameter expressions:

  {λ, q, q+λ, Φ₆, k−1, Φ₃, f−Φ₆, k+Φ₆, f−1, f+Φ₆−λ, f+Φ₆, v+1, v+Φ₆, v+k+Φ₆, Φ₁₂−λ}
= {2, 3, 5,   7,  11,  13, 17,    19,    23,  29,      31,    41,  47,    59,       71}

COROLLARY: All 194 Monster irrep dimensions factor *purely* into these
15 atoms — the W(3,3) shell semiring generates the entire Monster
character table.

STRUCTURAL IDENTITIES:
  • Count of supersingular primes = g = 15 (second eigenvalue multiplicity)
  • Sum of supersingular primes = λq³Φ₆ = 378
  • Sum of exponents in |M| = (q+λ)(k+Φ₆) = f + Φ₁₂ − λ = 95

Extends Phase CCLVII (chi_1..chi_6 from 13 atoms) to all 194 irreps
with two additional atoms 5 = q+λ and 17 = f−Φ₆.
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
Phi3 = 13
Phi4 = 10
Phi6 = 7
Phi12 = q**4 - q**2 + 1  # 73

# ── 15 supersingular shell atoms ──
ATOMS = {
    'lam':         lam,             # 2
    'q':           q,               # 3
    'q+lam':       q + lam,         # 5
    'Phi6':        Phi6,            # 7
    'k-1':         k - 1,           # 11
    'Phi3':        Phi3,            # 13
    'f-Phi6':      f - Phi6,        # 17
    'k+Phi6':      k + Phi6,        # 19
    'f-1':         f - 1,           # 23
    'f+Phi6-lam':  f + Phi6 - lam,  # 29
    'f+Phi6':      f + Phi6,        # 31
    'v+1':         v + 1,           # 41
    'v+Phi6':      v + Phi6,        # 47
    'v+k+Phi6':    v + k + Phi6,    # 59
    'Phi12-lam':   Phi12 - lam,     # 71
}

ATOM_SET = set(ATOMS.values())

# ── Monster order exponents ──
MONSTER_EXPONENTS = {
    2: 46, 3: 20, 5: 9, 7: 6, 11: 2, 13: 3,
    17: 1, 19: 1, 23: 1, 29: 1, 31: 1,
    41: 1, 47: 1, 59: 1, 71: 1,
}


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


def _load_monster_degrees():
    """Load all 194 Monster irrep dimensions from bundled data."""
    p = Path(__file__).resolve().parent.parent / "data" / "monster_degrees.json"
    return json.loads(p.read_text(encoding="utf-8"))


# ================================================================
# T1: The 15 atoms are exactly the supersingular primes
# ================================================================
class TestT1_AtomsAreSupersingularPrimes:
    """15 shell atoms = 15 prime divisors of |M|."""

    def test_atom_count(self):
        assert len(ATOMS) == 15

    def test_all_prime(self):
        for name, p in ATOMS.items():
            assert p >= 2
            assert all(p % d != 0 for d in range(2, int(p**0.5) + 1)), \
                f"{name}={p} not prime"

    def test_atom_set_equals_monster_support(self):
        assert ATOM_SET == set(MONSTER_EXPONENTS.keys())

    def test_atom_values(self):
        expected = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71}
        assert ATOM_SET == expected


# ================================================================
# T2: Atom origin expressions
# ================================================================
class TestT2_AtomOrigins:
    """Each atom is a simple W(3,3) parameter expression."""

    def test_2_lam(self):
        assert lam == 2

    def test_3_q(self):
        assert q == 3

    def test_5_q_plus_lam(self):
        assert q + lam == 5

    def test_7_Phi6(self):
        assert Phi6 == 7

    def test_11_k_minus_1(self):
        assert k - 1 == 11

    def test_13_Phi3(self):
        assert Phi3 == 13

    def test_17_f_minus_Phi6(self):
        assert f - Phi6 == 17

    def test_19_k_plus_Phi6(self):
        assert k + Phi6 == 19

    def test_23_f_minus_1(self):
        assert f - 1 == 23

    def test_29_f_plus_Phi6_minus_lam(self):
        assert f + Phi6 - lam == 29

    def test_31_f_plus_Phi6(self):
        assert f + Phi6 == 31

    def test_41_v_plus_1(self):
        assert v + 1 == 41

    def test_47_v_plus_Phi6(self):
        assert v + Phi6 == 47

    def test_59_v_plus_k_plus_Phi6(self):
        assert v + k + Phi6 == 59

    def test_71_Phi12_minus_lam(self):
        assert Phi12 - lam == 71


# ================================================================
# T3: All 194 Monster irreps factor into 15 atoms
# ================================================================
class TestT3_All194IrrepsPure:
    """Every Monster irrep dimension is a product of supersingular primes."""

    @pytest.fixture(scope="class")
    def degrees(self):
        return _load_monster_degrees()

    def test_194_entries(self, degrees):
        assert len(degrees) == 194

    def test_trivial_irrep(self, degrees):
        assert degrees[0] == 1

    def test_chi1(self, degrees):
        assert degrees[1] == 196883

    def test_all_factor_into_atoms(self, degrees):
        for i, chi in enumerate(degrees):
            if chi == 1:
                continue
            exogenous = _prime_factors(chi) - ATOM_SET
            assert not exogenous, \
                f"chi_{i} = {chi} has exogenous primes {exogenous}"


# ================================================================
# T4: Count = g identity
# ================================================================
class TestT4_CountIsG:
    """Number of supersingular primes = g = 15."""

    def test_count_equals_g(self):
        assert len(ATOMS) == g

    def test_g_is_second_multiplicity(self):
        """g is the multiplicity of eigenvalue -4 in W(3,3)."""
        assert g == 15
        assert v - 1 - f == g  # v = 1 + f + g


# ================================================================
# T5: Sum = lam * q^3 * Phi6
# ================================================================
class TestT5_SumIdentity:
    """Sum of supersingular primes = lambda * q^3 * Phi_6 = 378."""

    def test_sum_value(self):
        assert sum(ATOM_SET) == 378

    def test_sum_formula(self):
        assert sum(ATOM_SET) == lam * q**3 * Phi6

    def test_sum_alt(self):
        """378 = 2 * 189 = 2 * 27 * 7."""
        assert sum(ATOM_SET) == 2 * 27 * 7


# ================================================================
# T6: Sum of exponents in |M| = 95
# ================================================================
class TestT6_ExponentSum:
    """Sum of exponents in the Monster order = (q+lam)(k+Phi6) = 95."""

    def test_sum_value(self):
        assert sum(MONSTER_EXPONENTS.values()) == 95

    def test_product_formula(self):
        assert sum(MONSTER_EXPONENTS.values()) == (q + lam) * (k + Phi6)

    def test_alt_formula(self):
        """95 = f + Phi12 - lam."""
        assert sum(MONSTER_EXPONENTS.values()) == f + Phi12 - lam

    def test_factorization(self):
        """95 = 5 * 19, both shell atoms."""
        assert 95 == 5 * 19
        assert 5 in ATOM_SET and 19 in ATOM_SET


# ================================================================
# T7: chi_7 shell formula
# ================================================================
class TestT7_Chi7ShellFormula:
    """chi_7 = 3879214937598 = lam*q*Phi6*(k-1)*Phi3^2*(k+Phi6)*(f-1)*(v+1)*(v+Phi6)*(v+k+Phi6)."""

    @pytest.fixture(scope="class")
    def degrees(self):
        return _load_monster_degrees()

    def test_chi7_value(self, degrees):
        assert degrees[7] == 3879214937598

    def test_chi7_shell_formula(self, degrees):
        val = lam * q * Phi6 * (k-1) * Phi3**2 * (k+Phi6) * (f-1) * (v+1) * (v+Phi6) * (v+k+Phi6)
        assert val == degrees[7]

    def test_chi7_primes_in_atoms(self, degrees):
        assert _prime_factors(degrees[7]).issubset(ATOM_SET)


# ================================================================
# T8: Original 13 atoms capture 32 irreps
# ================================================================
class TestT8_Original13Atoms:
    """The original 13 atoms (without 5 and 17) capture exactly 32 of 194 irreps."""

    ATOMS_13 = ATOM_SET - {5, 17}

    @pytest.fixture(scope="class")
    def degrees(self):
        return _load_monster_degrees()

    def test_13_atoms(self):
        assert len(self.ATOMS_13) == 13

    def test_32_pure(self, degrees):
        count = sum(
            1 for chi in degrees
            if chi == 1 or not (_prime_factors(chi) - self.ATOMS_13)
        )
        assert count == 32

    def test_only_5_and_17_needed(self, degrees):
        """The only exogenous primes vs 13-atom set are 5 and 17."""
        exo = set()
        for chi in degrees:
            if chi > 1:
                exo |= _prime_factors(chi) - self.ATOMS_13
        assert exo == {5, 17}


# ================================================================
# T9: 5 and 17 have W(3,3) origins
# ================================================================
class TestT9_NewAtomOrigins:
    """The two new atoms 5 and 17 have natural W(3,3) expressions."""

    def test_5_is_q_plus_lam(self):
        assert q + lam == 5

    def test_5_is_Phi4_over_lam(self):
        assert Phi4 // lam == 5
        assert Phi4 % lam == 0

    def test_17_is_f_minus_Phi6(self):
        assert f - Phi6 == 17

    def test_17_is_v_minus_f_plus_1(self):
        assert v - f + 1 == 17

    def test_both_prime(self):
        assert all(5 % d != 0 for d in range(2, 3))
        assert all(17 % d != 0 for d in range(2, 5))


# ================================================================
# T10: Missing primes check
# ================================================================
class TestT10_MissingPrimes:
    """Primes <= 71 not in the atom set are exactly {37, 43, 53, 61, 67}."""

    def _primes_up_to(self, n):
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        for i in range(2, int(n**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, n+1, i):
                    sieve[j] = False
        return {i for i in range(n+1) if sieve[i]}

    def test_missing_set(self):
        primes_71 = self._primes_up_to(71)
        missing = primes_71 - ATOM_SET
        assert missing == {37, 43, 53, 61, 67}

    def test_20_primes_to_71(self):
        primes_71 = self._primes_up_to(71)
        assert len(primes_71) == 20

    def test_5_missing(self):
        """20 - 15 = 5 non-supersingular primes below 71."""
        assert 20 - 15 == 5


# ================================================================
# T11: Monster order reconstruction
# ================================================================
class TestT11_MonsterOrder:
    """The Monster group order decomposes into atom powers."""

    MONSTER_ORDER = math.prod(p**e for p, e in MONSTER_EXPONENTS.items())

    def test_order_value(self):
        expected = 808017424794512875886459904961710757005754368000000000
        assert self.MONSTER_ORDER == expected

    def test_all_prime_factors_are_atoms(self):
        factors = _prime_factors(self.MONSTER_ORDER)
        assert factors == ATOM_SET

    def test_exponent_sum_identity(self):
        """Sum of exponents = (q+lam)(k+Phi6) = 95."""
        assert sum(MONSTER_EXPONENTS.values()) == (q + lam) * (k + Phi6)
