"""Part DCCLXXVI -- Sporadic simple groups from W(3,3) tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxxvi_sporadic_simple_groups_w33 import (  # noqa: E402
    CONWAY,
    FISCHER,
    JANKO,
    K,
    MATHIEU,
    MU,
    OTHER,
    OUT_PATH,
    PARIAHS,
    PHI3,
    Q,
    V,
    all_sporadic_groups,
    build_bridge,
    family_counts,
    happy_family,
    pariahs,
    split_counts,
    write_bridge,
    w33_linked_sporadics,
)


def test_total_sporadics_eq_26():
    assert len(all_sporadic_groups()) == 26


def test_happy_family_count_20():
    assert len(happy_family()) == 20


def test_pariahs_count_6():
    assert len(pariahs()) == 6


def test_26_eq_D_bosonic():
    """26 = 2 * Phi_3 = HPS level 3 (DCCLII)."""
    assert 26 == 2 * PHI3


def test_20_eq_cuboctahedron_volume():
    """20 = central binomial C(2q, q) at q = 3."""
    assert 20 == math.comb(2 * Q, Q)
    assert 20 == V // 2


def test_6_eq_q_factorial():
    assert 6 == math.factorial(Q)


def test_Mathieu_count_eq_5():
    assert len(MATHIEU) == 5 == MU + 1


def test_Janko_count_eq_4():
    assert len(JANKO) == 4 == MU


def test_Conway_count_eq_3():
    assert len(CONWAY) == 3 == Q


def test_Fischer_count_eq_3():
    assert len(FISCHER) == 3 == Q


def test_Other_count_eq_11():
    assert len(OTHER) == 11 == K - 1


def test_family_counts_sum_to_26():
    total = len(MATHIEU) + len(JANKO) + len(CONWAY) + len(FISCHER) + len(OTHER)
    assert total == 26


def test_pariahs_are_J1_J3_J4_Ru_ON_Ly():
    expected = {"J_1", "J_3", "J_4", "Ru", "O'N", "Ly"}
    assert PARIAHS == expected


def test_M_12_aut_of_S_5_6_12():
    """M_12 is the automorphism of the ternary Golay code G_12 / Steiner S(5,6,12)."""
    linked = w33_linked_sporadics()
    m12 = next(r for r in linked if r["group"] == "M_12")
    assert m12["order"] == 95040


def test_M_24_aut_of_S_5_8_24():
    """M_24 = Aut(binary Golay G_24) = Aut(Steiner S(5, 8, 24))."""
    linked = w33_linked_sporadics()
    m24 = next(r for r in linked if r["group"] == "M_24")
    assert m24["order"] == 244823040


def test_split_w33_readings():
    split = split_counts()
    assert split["happy_family_count"] == 20
    assert split["pariah_count"] == 6
    assert split["total"] == 26


def test_family_counts_dict():
    fams = family_counts()
    assert fams["Mathieu"]["count"] == 5
    assert fams["Janko"]["count"] == 4
    assert fams["Conway"]["count"] == 3
    assert fams["Fischer"]["count"] == 3
    assert fams["Other"]["count"] == 11


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Sporadic Groups" in b["theorem"]
    assert "26" in b["one_line"]


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
        "all_26_sporadic_groups",
        "happy_family_20",
        "pariahs_6",
        "family_counts",
        "split_counts",
        "w33_linked_sporadics",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
