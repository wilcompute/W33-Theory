"""Part DCCLVIII -- Universal multi-overdetermination tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclviii_universal_overdetermination import (  # noqa: E402
    OUT_PATH,
    Q,
    alternating_cyclic,
    build_bridge,
    evaluate_at_q,
    frobenius_gq_edge,
    identity_121,
    independence_classes,
    kissing_tower_match,
    loop_closure_min,
    master_equation,
    mersenne_eq_heawood,
    monster_prime_count,
    non_neighbours_eq_E6_fund,
    overdetermination_catalogue,
    overdetermination_scan,
    perfect_matchings,
    pincer_zero,
    sin_theta_W,
    sphere_packing_denoms,
    write_bridge,
)


def test_master_equation_at_q_3():
    assert master_equation(3) is True
    for q in (1, 2, 4, 5, 6, 7):
        assert master_equation(q) is False


def test_alternating_cyclic_at_q_3():
    assert alternating_cyclic(3) is True


def test_loop_closure_at_q_3():
    assert loop_closure_min(3) is True
    assert loop_closure_min(2) is False
    assert loop_closure_min(4) is False


def test_pincer_zero_at_q_3():
    assert pincer_zero(3) is True
    assert pincer_zero(2) is False
    assert pincer_zero(4) is False


def test_mersenne_eq_heawood_at_q_3():
    """2^3 - 1 = 7 = 3 + 4 unique at q = 3."""
    assert mersenne_eq_heawood(3) is True
    for q in (1, 2, 4, 5, 6, 7):
        assert mersenne_eq_heawood(q) is False


def test_frobenius_gq_at_q_3():
    """q^5 - q = q(q+1)^2(q^2+1)/2 unique at q = 3."""
    assert frobenius_gq_edge(3) is True
    for q in (2, 4, 5, 6, 7):
        assert frobenius_gq_edge(q) is False


def test_perfect_matchings_K4_eq_3():
    assert perfect_matchings(3) is True


def test_identity_121_unique_at_q_3():
    assert identity_121(3) is True
    for q in (2, 4, 5):
        assert identity_121(q) is False


def test_non_neighbours_at_q_3():
    assert non_neighbours_eq_E6_fund(3) is True


def test_sin_theta_W_at_q_3():
    """3q^2 - 10q + 3 = 0 at q = 3."""
    assert sin_theta_W(3) is True
    for q in (1, 2, 4, 5):
        assert sin_theta_W(q) is False


def test_kissing_tower_match_at_q_3():
    assert kissing_tower_match(3) is True


def test_sphere_packing_denoms_at_q_3():
    assert sphere_packing_denoms(3) is True


def test_monster_prime_count_at_q_3():
    assert monster_prime_count(3) is True


def test_catalogue_has_15_entries():
    assert len(overdetermination_catalogue()) == 15


def test_at_least_10_independence_classes():
    classes = independence_classes()
    assert len(classes) >= 10


def test_q_3_satisfies_all_15():
    results = evaluate_at_q(3)
    assert all(r["satisfied"] for r in results)


def test_q_3_is_unique_max_in_scan():
    scan = overdetermination_scan(11)
    max_val = max(scan.values())
    unique_max = [q for q, c in scan.items() if c == max_val]
    assert unique_max == [3]
    assert max_val == 15


def test_no_other_q_satisfies_more_than_one():
    scan = overdetermination_scan(11)
    for q, count in scan.items():
        if q != 3:
            assert count <= 1


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Universal Multi-Overdetermination" in b["theorem"]
    assert "15" in b["one_line"]


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "overdetermination_catalogue",
        "independence_classes",
        "evaluate_at_q_3",
        "overdetermination_scan",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
