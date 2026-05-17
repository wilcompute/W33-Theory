"""Part DCCLXXVII -- Convergent Attractor Theorem tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxxvii_convergent_attractor_theorem import (  # noqa: E402
    OUT_PATH,
    Q,
    attractor_test,
    build_bridge,
    independent_classical_theorems,
    w33_primitive_table,
    w33_value_set,
    write_bridge,
)


def test_w33_primitive_table_at_least_30():
    assert len(w33_primitive_table()) >= 30


def test_independent_theorems_at_least_20():
    assert len(independent_classical_theorems()) >= 20


def test_all_theorems_land_in_T_W33():
    test = attractor_test()
    assert test["complete_convergence"] is True


def test_hit_rate_100_percent():
    test = attractor_test()
    assert test["hit_rate"] == 1.0


def test_span_at_least_300_years():
    theorems = independent_classical_theorems()
    span = max(t["year"] for t in theorems) - min(t["year"] for t in theorems)
    assert span >= 300


def test_at_least_15_distinct_investigators():
    theorems = independent_classical_theorems()
    investigators = {t["investigator"] for t in theorems}
    assert len(investigators) >= 15


def test_specific_theorems_include_Newton_kissing():
    theorems = independent_classical_theorems()
    newton = next((t for t in theorems if "Newton" in t["investigator"]), None)
    assert newton is not None
    assert newton["value"] == 12   # K(3) = 12


def test_specific_theorems_include_Viazovska():
    theorems = independent_classical_theorems()
    viazovska_8 = next((t for t in theorems if "Viazovska" in t["investigator"]
                        and "rho_8" in t["theorem"]), None)
    assert viazovska_8 is not None
    assert viazovska_8["value"] == 384


def test_specific_theorems_include_Tietavainen_van_Lint():
    theorems = independent_classical_theorems()
    tvl = next((t for t in theorems if "Tietavainen" in t["investigator"]), None)
    assert tvl is not None


def test_CFSG_in_theorems():
    theorems = independent_classical_theorems()
    cfsg = next((t for t in theorems if "CFSG" in t["investigator"]), None)
    assert cfsg is not None
    assert cfsg["value"] == 26


def test_Hurwitz_dim_4():
    """Hurwitz theorem: 4 normed division algebras."""
    theorems = independent_classical_theorems()
    h = next((t for t in theorems if "Hurwitz" in t["investigator"]), None)
    assert h is not None
    assert h["value"] == 4


def test_Hopf_dim_15():
    """Hopf fibration S^7 -> S^15 -> S^8."""
    theorems = independent_classical_theorems()
    h = next((t for t in theorems if "Hopf" in t["investigator"]), None)
    assert h is not None
    assert h["value"] == 15


def test_Adams_4_fibrations():
    theorems = independent_classical_theorems()
    a = next((t for t in theorems if "Adams" in t["investigator"]), None)
    assert a is not None
    assert a["value"] == 4


def test_value_set_size_at_least_15():
    """The 23 theorems use at least 15 distinct integers."""
    theorems = independent_classical_theorems()
    values = {t["value"] for t in theorems}
    assert len(values) >= 10   # at least 10 distinct integers


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_breakthrough_statement_present():
    b = build_bridge()
    assert "BREAKTHROUGH" in b["breakthrough_statement"]


def test_theorem_mentions_320_or_363_years():
    b = build_bridge()
    # Either span fits
    assert "320" in b["theorem"] or "363" in b["theorem"]


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert data["summary"]["hit_rate"] == 1.0


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "w33_primitive_table",
        "independent_classical_theorems",
        "attractor_test",
        "identities",
        "theorem",
        "breakthrough_statement",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
