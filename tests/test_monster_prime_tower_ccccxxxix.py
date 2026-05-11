"""
Part CCCCXXXIX -- All 15 Monster (Supersingular) Primes in W(3,3)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXXXIX_MONSTER_PRIME_TOWER_W33 import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6, H_0,
    SUPERSINGULAR_PRIMES_W33,
    MONSTER_FACTORIZATION, monster_order,
    LOWER_TIER, MIDDLE_TIER, CONWAY_TIER,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_fifteen_supersingular_primes():
    assert len(SUPERSINGULAR_PRIMES_W33) == 15


def test_all_W33_forms_evaluate_correctly():
    for p, form, val in SUPERSINGULAR_PRIMES_W33:
        assert val == p, f"{p} != {val}"


def test_three_tier_total():
    assert len(LOWER_TIER) + len(MIDDLE_TIER) + len(CONWAY_TIER) == 15


def test_middle_tier_W33_forms():
    """The 3 middle supersingular primes 29, 31, 41."""
    assert 29 == Q ** Q + LAM
    assert 31 == V - Q ** 2
    assert 41 == V + 1


def test_conway_primes_W33_forms():
    """The 3 Conway primes 47, 59, 71."""
    assert 47 == V + PHI6
    assert 59 == PHI6 * LAM ** Q + Q
    assert 71 == H_0 + 1


def test_bernoulli_primes_W33_forms():
    """Lower tier: 9 Bernoulli small primes 2-23."""
    assert 2 == LAM
    assert 3 == Q
    assert 5 == MU + 1
    assert 7 == PHI6
    assert 11 == K - 1
    assert 13 == PHI3
    assert 17 == PHI3 + MU
    assert 19 == F - MU - 1
    assert 23 == PHI3 + PHI4


def test_monster_order():
    """|M| = 8.08e53"""
    M = monster_order()
    assert 8e53 < M < 9e53
    assert M == 808017424794512875886459904961710757005754368000000000


def test_distinct_primes():
    primes = [p for p, _, _ in SUPERSINGULAR_PRIMES_W33]
    assert len(set(primes)) == 15


def test_primes_in_correct_tier():
    for p in LOWER_TIER:
        assert p in [a for a, _, _ in SUPERSINGULAR_PRIMES_W33]
    for p in MIDDLE_TIER:
        assert p in [a for a, _, _ in SUPERSINGULAR_PRIMES_W33]
    for p in CONWAY_TIER:
        assert p in [a for a, _, _ in SUPERSINGULAR_PRIMES_W33]


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCXXXIX_MONSTER_PRIME_TOWER_W33")
    mod.main()
    assert (ROOT / "PART_CCCCXXXIX_monster_prime_tower_w33_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCXXXIX_monster_prime_tower_w33_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCXXXIX_MONSTER_PRIME_TOWER_W33").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_all_15_primes():
    out = ROOT / "PART_CCCCXXXIX_monster_prime_tower_w33_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data["supersingular_primes"]) == 15
