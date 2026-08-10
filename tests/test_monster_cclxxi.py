"""
Tests for Part CCLXXI: Monster Group, Baby Monster & Monstrous Moonshine.
57 tests covering all 40 bridge identities, JSON artifact, and
additional mathematical properties.
"""

import json
import pytest
from pathlib import Path

# ── W(3,3) strongly regular graph constants ──────────────────────────────────
V         = 40
K         = 12
LAM       = 2
MU        = 4
Q         = 3
M_LAM     = 27
PHI3      = 13
PHI4      = 10
PHI6      = 7
EDGES     = 240
LAP_TOP   = 16
LAP_MID   = 10
AUT_ORDER = 51840

# ── Group orders ──────────────────────────────────────────────────────────────
MONSTER_ORDER = (
    2**46 * 3**20 * 5**9 * 7**6 * 11**2 * 13**3
    * 17 * 19 * 23 * 29 * 31 * 41 * 47 * 59 * 71
)
BABY_ORDER = (
    2**41 * 3**13 * 5**6 * 7**2
    * 11 * 13 * 17 * 19 * 23 * 31 * 47
)

# ── Derived quantities ────────────────────────────────────────────────────────
MOONSHINE_PRIMES = [2, 3, 5, 7, 11, 23]
TWO_K = 2 * K                               # = 24

MONSTER_PRIMES = frozenset({2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71})
BABY_PRIMES    = frozenset({2, 3, 5, 7, 11, 13, 17, 19, 23, 31, 47})
UNIQUE_TO_M    = MONSTER_PRIMES - BABY_PRIMES   # {29, 41, 59, 71}

P47 = V + MU + Q                            # = 47
P59 = V + PHI3 + PHI4 - MU                 # = 59
P71 = V + PHI3 + LAP_TOP + LAM             # = 71
DIM_SMALLEST   = P47 * P59 * P71           # = 196 883

KISSING        = EDGES * Q**2 * PHI6 * PHI3  # = 196 560
H_E7           = K + MU + LAM              # = 18
DIM_V_NATURAL  = KISSING + H_E7**2         # = 196 884

REPO_ROOT = Path(__file__).parent.parent
JSON_PATH = REPO_ROOT / "PART_CCLXXI_monster_results.json"


def prime_exp(n: int, p: int) -> int:
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


# ════════════════════════════════════════════════════════════════════════════
# §1  Sporadic groups census  (B01–B05)
# ════════════════════════════════════════════════════════════════════════════

def test_B01_sporadic_total():
    assert 26 == 2 * K + 2


def test_B02_happy_family():
    assert 20 == EDGES // K


def test_B03_pariahs():
    assert 6 == LAM * Q


def test_B04_monster_prime_count():
    assert 15 == K + Q


def test_B05_baby_prime_count():
    assert 11 == LAP_TOP - PHI6 + LAM


# ════════════════════════════════════════════════════════════════════════════
# §2  Moonshine primes  (B06–B13)
# ════════════════════════════════════════════════════════════════════════════

def test_B06_moonshine_prime_count():
    assert len(MOONSHINE_PRIMES) == LAM * Q


def test_B07_moonshine_2():
    assert TWO_K % (2 + 1) == 0


def test_B08_moonshine_3():
    assert TWO_K % (3 + 1) == 0


def test_B09_moonshine_5():
    assert TWO_K % (5 + 1) == 0


def test_B10_moonshine_7():
    assert TWO_K % (7 + 1) == 0


def test_B11_moonshine_11():
    assert TWO_K % (11 + 1) == 0


def test_B12_moonshine_23():
    assert TWO_K % (23 + 1) == 0


def test_B13_moonshine_prime_sum():
    assert sum(MOONSHINE_PRIMES) == M_LAM + LAM * K


# ════════════════════════════════════════════════════════════════════════════
# §3  Monster order prime factorisation  (B14–B22)
# ════════════════════════════════════════════════════════════════════════════

def test_B14_v2_monster():
    assert prime_exp(MONSTER_ORDER, 2) == 2 * K + LAP_TOP + MU + LAM


def test_B15_v3_monster():
    assert prime_exp(MONSTER_ORDER, 3) == EDGES // K


def test_B16_v5_monster():
    assert prime_exp(MONSTER_ORDER, 5) == Q ** 2


def test_B17_v7_monster():
    assert prime_exp(MONSTER_ORDER, 7) == LAM * Q


def test_B18_v11_monster():
    assert prime_exp(MONSTER_ORDER, 11) == LAM


def test_B19_v13_monster():
    assert prime_exp(MONSTER_ORDER, 13) == Q


def test_B20_prime_29():
    assert 29 == M_LAM + LAM


def test_B21_prime_31():
    assert 31 == V - Q ** 2


def test_B22_prime_41():
    assert 41 == V + 1


# ════════════════════════════════════════════════════════════════════════════
# §4  Top-3 Monster primes & minimal representation  (B23–B27)
# ════════════════════════════════════════════════════════════════════════════

def test_B23_P47():
    assert P47 == 47


def test_B24_P59():
    assert P59 == 59


def test_B25_P71():
    assert P71 == 71


def test_B26_dim_smallest():
    assert DIM_SMALLEST == 196883


def test_B27_monster_only_prime_sum():
    assert 29 + 41 + 59 + 71 == MU * (V + LAP_MID)


# ════════════════════════════════════════════════════════════════════════════
# §5  Baby Monster order  (B28–B32)
# ════════════════════════════════════════════════════════════════════════════

def test_B28_v2_baby():
    assert prime_exp(BABY_ORDER, 2) == V + 1


def test_B29_v3_baby():
    assert prime_exp(BABY_ORDER, 3) == PHI3


def test_B30_v5_baby():
    assert prime_exp(BABY_ORDER, 5) == LAM * Q


def test_B31_v7_baby():
    assert prime_exp(BABY_ORDER, 7) == LAM


def test_B32_unique_to_monster_count():
    assert len(UNIQUE_TO_M) == MU


# ════════════════════════════════════════════════════════════════════════════
# §6  Moonshine representations and j-function  (B33–B38)
# ════════════════════════════════════════════════════════════════════════════

def test_B33_dim_V_natural():
    assert DIM_V_NATURAL == 196884


def test_B34_dim_difference():
    assert DIM_V_NATURAL - DIM_SMALLEST == 1


def test_B35_j_constant_744():
    assert 744 == (V - Q ** 2) * TWO_K


def test_B36_largest_moonshine_prime():
    assert 23 == TWO_K - 1


def test_B37_conjugacy_classes():
    assert 194 == LAM + K * LAP_TOP


def test_B38_monster_prime_sum():
    assert sum(sorted(MONSTER_PRIMES)) == LAM * M_LAM * PHI6


# ════════════════════════════════════════════════════════════════════════════
# §7  String-theory cross-links  (B39–B40)
# ════════════════════════════════════════════════════════════════════════════

def test_B39_bosonic_string():
    assert 26 == 2 * K + 2


def test_B40_superstring():
    assert 10 == PHI4


# ════════════════════════════════════════════════════════════════════════════
# Additional mathematical properties  (A01–A12)
# ════════════════════════════════════════════════════════════════════════════

def test_A01_moonshine_primes_are_prime():
    assert all(is_prime(p) for p in MOONSHINE_PRIMES)


def test_A02_happy_plus_pariahs_equals_sporadic():
    assert (EDGES // K) + (LAM * Q) == 2 * K + 2


def test_A03_baby_primes_subset_of_monster_primes():
    assert BABY_PRIMES <= MONSTER_PRIMES


def test_A04_unique_to_monster_correct():
    assert UNIQUE_TO_M == frozenset({29, 41, 59, 71})


def test_A05_kissing_formula():
    assert KISSING == 196560


def test_A06_h_e7_formula():
    assert H_E7 == 18


def test_A07_dim_V_natural_components():
    assert KISSING + H_E7 ** 2 == 196884


def test_A08_dim_smallest_is_odd():
    assert DIM_SMALLEST % 2 == 1


def test_A09_dim_V_natural_is_even():
    assert DIM_V_NATURAL % 2 == 0


def test_A10_monster_prime_list():
    assert sorted(MONSTER_PRIMES) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71]


def test_A11_moonshine_max_prime():
    assert max(MOONSHINE_PRIMES) == TWO_K - 1


def test_A12_monster_order_divisible_by_all_baby_primes():
    for p in BABY_PRIMES:
        assert MONSTER_ORDER % p == 0, f"Monster order not divisible by {p}"


# ════════════════════════════════════════════════════════════════════════════
# JSON artifact checks
# ════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="module")
def result_json():
    assert JSON_PATH.exists(), f"JSON not found: {JSON_PATH}"
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def test_json_exists():
    assert JSON_PATH.exists()


def test_json_part(result_json):
    assert result_json["part"] == "CCLXXI"


def test_json_verified(result_json):
    assert result_json["verified"] is True


def test_json_checks_count(result_json):
    assert result_json["checks_total"] == 40


def test_json_all_pass(result_json):
    assert result_json["checks_passed"] == 40
