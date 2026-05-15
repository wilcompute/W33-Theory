"""Part DCCXVIII -- Pincer-bound theorem tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxviii_pincer_bound_theorem import (  # noqa: E402
    OUT_PATH,
    Q_STAR,
    build_bridge,
    delta_h,
    is_dihedral_dominant,
    is_non_abelian_sym,
    lower_bound_q,
    upper_bound_q,
    write_bridge,
)


def test_delta_h_zero_at_q_3():
    assert math.isclose(delta_h(Q_STAR), 0.0, abs_tol=1e-12)


def test_delta_h_negative_below():
    for q in (1, 2):
        assert delta_h(q) < 0


def test_delta_h_positive_above():
    for q in range(4, 13):
        assert delta_h(q) > 0


def test_delta_h_strictly_increasing_for_q_geq_3():
    last = delta_h(3)
    for q in range(4, 12):
        cur = delta_h(q)
        assert cur > last
        last = cur


def test_lower_bound_is_3():
    assert lower_bound_q() == 3


def test_upper_bound_is_3():
    assert upper_bound_q() == 3


def test_non_abelian_predicate():
    assert not is_non_abelian_sym(1)
    assert not is_non_abelian_sym(2)
    assert is_non_abelian_sym(3)
    assert is_non_abelian_sym(4)


def test_dihedral_dominant_predicate():
    for q in (1, 2, 3):
        assert is_dihedral_dominant(q)
    for q in (4, 5, 6, 10):
        assert not is_dihedral_dominant(q)


def test_intersection_is_singleton_3():
    b = build_bridge()
    assert b["deep_chain"]["intersection"] == [3]
    assert b["deep_chain"]["uniqueness"] is True


def test_master_equation_saturates_pincer():
    b = build_bridge()
    assert b["identities"]["master_equation_saturates_pincer"] is True


def test_all_identities_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_scan_size_and_q_3_row():
    b = build_bridge()
    rows = b["scan"]
    assert len(rows) >= 6
    row3 = next(r for r in rows if r["q"] == 3)
    assert row3["factorial_q"] == 6
    assert row3["two_q"] == 6
    assert row3["saturation"] == "saturated"


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Pincer-Bound Theorem" in b["theorem"]
    assert "q = 3" in b["one_line"]


def test_write_bridge_creates_json():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["q_star"] == 3
    assert data["summary"]["pincer_collapses_to_singleton"] is True


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "scan",
        "deep_chain",
        "entropy_gap",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
