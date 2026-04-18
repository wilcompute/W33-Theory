"""Pin the Ogg-prime moonshine quiver extension."""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_monster_ogg_supersingular import MONSTER_PRIMES  # noqa: E402
from w33_ogg_prime_moonshine_quiver_bridge import build_summary  # noqa: E402


def test_covered_primes_equal_monster_primes():
    summary = build_summary()
    assert summary["ogg_prime_moonshine_quiver_dictionary"]["covered_monster_primes"] == sorted(MONSTER_PRIMES)


def test_ab_families_share_series():
    summary = build_summary()
    rows = {row["family"]: row for row in summary["ogg_prime_moonshine_quiver_dictionary"]["extension_rows"]}
    for family in ["23AB", "31AB", "47AB", "59AB", "71AB"]:
        assert rows[family]["theorems"]["shared_series_holds_for_AB_family"] is True


def test_all_extension_families_satisfy_prime_replicability():
    summary = build_summary()
    rows = summary["ogg_prime_moonshine_quiver_dictionary"]["extension_rows"]
    assert all(row["theorems"]["all_classes_satisfy_prime_replicability"] for row in rows) is True


def test_ogg_prime_quiver_summary_chain_is_all_true():
    summary = build_summary()
    theorem = summary["ogg_prime_moonshine_quiver_theorem"]
    assert all(theorem.values()) is True
