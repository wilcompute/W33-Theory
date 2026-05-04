"""
Part CCLXXIII — Tests: Six Pariah Groups and W(3,3)

pytest test suite verifying that the 6 pariah sporadic groups encode
W(3,3) strongly-regular graph parameters in their p-adic valuations,
and that the Monster's own valuations mirror those parameters.
"""

import pytest

# ── W(3,3) constants ──────────────────────────────────────────────────────────
V         = 40
K         = 12
LAM       = 2
MU        = 4
Q         = 3
M_LAM     = 27
LAP_MID   = 10
LAP_TOP   = 16
EDGES     = 240
AUT_ORDER = 51840
PHI3      = 13
PHI4      = 10
PHI6      = 7

# Group orders
J1_ORDER = 175560
J3_ORDER = 50232960
J4_ORDER = 86775571046077562880
LY_ORDER = 51765179004000000
RU_ORDER = 145926144000
ON_ORDER = 460815505920
M_ORDER  = (2**46 * 3**20 * 5**9 * 7**6 * 11**2 * 13**3 *
            17 * 19 * 23 * 29 * 31 * 41 * 47 * 59 * 71)

MONSTER_PRIMES = frozenset([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71])

PARIAH_ORDERS = {
    "J1": J1_ORDER, "J3": J3_ORDER, "J4": J4_ORDER,
    "Ly": LY_ORDER, "Ru": RU_ORDER, "ON": ON_ORDER,
}


# ── helpers ────────────────────────────────────────────────────────────────────
def p_adic_val(n: int, p: int) -> int:
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def omega(n: int) -> int:
    count, d = 0, 2
    while d * d <= n:
        if n % d == 0:
            count += 1
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        count += 1
    return count


def bigomega(n: int) -> int:
    count, d = 0, 2
    while d * d <= n:
        while n % d == 0:
            count += 1
            n //= d
        d += 1
    if n > 1:
        count += 1
    return count


def prime_factors(n: int):
    factors = set()
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.add(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


# ═══════════════════════════════════════════════════════════════════════════════
# §1  Sporadic group counting
# ═══════════════════════════════════════════════════════════════════════════════
class TestSporadicCounting:
    def test_happy_family_equals_v_over_2(self):
        assert 20 == V // 2

    def test_pariah_count_equals_lam_times_q(self):
        assert 6 == LAM * Q

    def test_total_sporadics_is_26(self):
        assert 20 + 6 == 26

    def test_total_equals_v_over_2_plus_lam_q(self):
        assert 26 == V // 2 + LAM * Q

    def test_partition_completeness(self):
        """Happy + Pariah exhausts all 26 sporadic groups."""
        assert V // 2 + LAM * Q == 26


# ═══════════════════════════════════════════════════════════════════════════════
# §2  Monster p-adic valuations
# ═══════════════════════════════════════════════════════════════════════════════
class TestMonsterPadic:
    def test_nu3_equals_v_over_2(self):
        assert p_adic_val(M_ORDER, 3) == V // 2

    def test_nu5_equals_q_squared(self):
        assert p_adic_val(M_ORDER, 5) == Q ** 2

    def test_nu7_equals_lam_times_q(self):
        assert p_adic_val(M_ORDER, 7) == LAM * Q

    def test_nu11_equals_lam(self):
        assert p_adic_val(M_ORDER, 11) == LAM

    def test_nu13_equals_q(self):
        assert p_adic_val(M_ORDER, 13) == Q

    def test_omega_equals_k_plus_lam_plus_1(self):
        assert omega(M_ORDER) == K + LAM + 1

    def test_nu7_equals_pariah_count(self):
        """The Monster's 7-adic valuation = the number of Pariah groups."""
        assert p_adic_val(M_ORDER, 7) == 6  # = LAM * Q

    def test_nu3_equals_happy_family_count(self):
        """The Monster's 3-adic valuation = the number of Happy Family groups."""
        assert p_adic_val(M_ORDER, 3) == 20  # = V // 2


# ═══════════════════════════════════════════════════════════════════════════════
# §3  Janko J₁
# ═══════════════════════════════════════════════════════════════════════════════
class TestJankoJ1:
    def test_nu2_equals_q(self):
        assert p_adic_val(J1_ORDER, 2) == Q

    def test_omega_equals_lam_times_q(self):
        assert omega(J1_ORDER) == LAM * Q

    def test_bigomega_equals_2_mu(self):
        assert bigomega(J1_ORDER) == 2 * MU

    def test_nu7_equals_1(self):
        assert p_adic_val(J1_ORDER, 7) == 1

    def test_order_correct(self):
        assert J1_ORDER == 2**3 * 3 * 5 * 7 * 11 * 19


# ═══════════════════════════════════════════════════════════════════════════════
# §4  Janko J₃
# ═══════════════════════════════════════════════════════════════════════════════
class TestJankoJ3:
    def test_nu2_equals_phi6(self):
        assert p_adic_val(J3_ORDER, 2) == PHI6

    def test_nu3_equals_q_plus_lam(self):
        assert p_adic_val(J3_ORDER, 3) == Q + LAM

    def test_omega_equals_q_plus_lam(self):
        assert omega(J3_ORDER) == Q + LAM

    def test_order_correct(self):
        assert J3_ORDER == 2**7 * 3**5 * 5 * 17 * 19


# ═══════════════════════════════════════════════════════════════════════════════
# §5  Janko J₄
# ═══════════════════════════════════════════════════════════════════════════════
class TestJankoJ4:
    def test_nu2_equals_q_times_phi6(self):
        assert p_adic_val(J4_ORDER, 2) == Q * PHI6

    def test_nu3_equals_q(self):
        assert p_adic_val(J4_ORDER, 3) == Q

    def test_omega_equals_phi4(self):
        assert omega(J4_ORDER) == PHI4

    def test_order_correct(self):
        assert J4_ORDER == 2**21 * 3**3 * 5 * 7 * 11**3 * 23 * 29 * 31 * 37 * 43


# ═══════════════════════════════════════════════════════════════════════════════
# §6  Lyons group
# ═══════════════════════════════════════════════════════════════════════════════
class TestLyons:
    def test_nu2_equals_lam_times_mu(self):
        assert p_adic_val(LY_ORDER, 2) == LAM * MU

    def test_nu3_equals_phi6(self):
        assert p_adic_val(LY_ORDER, 3) == PHI6

    def test_nu5_equals_lam_times_q(self):
        assert p_adic_val(LY_ORDER, 5) == LAM * Q

    def test_omega_equals_2_mu(self):
        assert omega(LY_ORDER) == 2 * MU

    def test_order_correct(self):
        assert LY_ORDER == 2**8 * 3**7 * 5**6 * 7 * 11 * 31 * 37 * 67


# ═══════════════════════════════════════════════════════════════════════════════
# §7  Rudvalis group
# ═══════════════════════════════════════════════════════════════════════════════
class TestRudvalis:
    def test_nu2_equals_k_plus_lam(self):
        assert p_adic_val(RU_ORDER, 2) == K + LAM

    def test_nu3_equals_q(self):
        assert p_adic_val(RU_ORDER, 3) == Q

    def test_nu5_equals_q(self):
        assert p_adic_val(RU_ORDER, 5) == Q

    def test_omega_equals_lam_times_q(self):
        assert omega(RU_ORDER) == LAM * Q

    def test_phi3_divides_order(self):
        assert RU_ORDER % PHI3 == 0

    def test_v_minus_k_plus_1_divides_order(self):
        assert RU_ORDER % (V - K + 1) == 0

    def test_order_correct(self):
        assert RU_ORDER == 2**14 * 3**3 * 5**3 * 7 * 13 * 29


# ═══════════════════════════════════════════════════════════════════════════════
# §8  O'Nan group
# ═══════════════════════════════════════════════════════════════════════════════
class TestONan:
    def test_nu2_equals_q_squared(self):
        assert p_adic_val(ON_ORDER, 2) == Q ** 2

    def test_nu3_equals_mu(self):
        assert p_adic_val(ON_ORDER, 3) == MU

    def test_nu7_equals_q(self):
        assert p_adic_val(ON_ORDER, 7) == Q

    def test_omega_equals_phi6(self):
        assert omega(ON_ORDER) == PHI6

    def test_order_correct(self):
        assert ON_ORDER == 2**9 * 3**4 * 5 * 7**3 * 11 * 19 * 31


# ═══════════════════════════════════════════════════════════════════════════════
# §9  Cross-cutting identities
# ═══════════════════════════════════════════════════════════════════════════════
class TestCrossCutting:
    def test_extra_pariah_prime_count_equals_q(self):
        pariah_primes = set()
        for order in PARIAH_ORDERS.values():
            pariah_primes |= prime_factors(order)
        extra = pariah_primes - MONSTER_PRIMES
        assert len(extra) == Q

    def test_extra_pariah_primes_are_37_43_67(self):
        pariah_primes = set()
        for order in PARIAH_ORDERS.values():
            pariah_primes |= prime_factors(order)
        extra = pariah_primes - MONSTER_PRIMES
        assert extra == {37, 43, 67}

    def test_extra_primes_sum_equals_q_times_phi6_sq(self):
        assert 37 + 43 + 67 == Q * PHI6 ** 2

    def test_nu2_sum_equals_v_plus_k_plus_phi4(self):
        nu2_sum = sum(p_adic_val(o, 2) for o in PARIAH_ORDERS.values())
        assert nu2_sum == V + K + PHI4

    def test_max_nu2_equals_q_times_phi6(self):
        max_nu2 = max(p_adic_val(o, 2) for o in PARIAH_ORDERS.values())
        assert max_nu2 == Q * PHI6

    def test_pariahs_with_q_dividing_nu2_count_equals_q(self):
        count = sum(
            1 for o in PARIAH_ORDERS.values()
            if p_adic_val(o, 2) % Q == 0
        )
        assert count == Q

    def test_pariah_orders_pairwise_distinct(self):
        orders = list(PARIAH_ORDERS.values())
        assert len(set(orders)) == len(orders)

    def test_all_pariah_orders_positive(self):
        assert all(o > 0 for o in PARIAH_ORDERS.values())
