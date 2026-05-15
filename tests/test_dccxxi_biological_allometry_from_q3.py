"""Part DCCXXI -- Biological allometry from q = 3 tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxi_biological_allometry_from_q3 import (  # noqa: E402
    OUT_PATH,
    Q,
    QUARTER,
    allometric_family,
    build_bridge,
    expected_dimension_from_kleiber,
    write_bridge,
)


def test_quarter_is_one_over_q_plus_one():
    assert math.isclose(QUARTER, 1 / (Q + 1), abs_tol=1e-12)
    assert math.isclose(QUARTER, 0.25, abs_tol=1e-12)


def test_kleiber_exponent_is_three_quarters():
    fam = allometric_family()
    kleiber = next(f for f in fam if "Kleiber" in f["source_law"])
    assert math.isclose(kleiber["exponent"], 0.75, abs_tol=1e-12)
    assert math.isclose(kleiber["exponent"], Q / (Q + 1), abs_tol=1e-12)


def test_inverting_kleiber_recovers_q():
    d = expected_dimension_from_kleiber(0.75)
    assert math.isclose(d, Q, abs_tol=1e-12)


def test_all_exponents_quantised_in_quarters():
    fam = allometric_family()
    for f in fam:
        n, denom = f["n_over_q_plus_one"]
        assert denom == Q + 1
        assert math.isclose(f["exponent"], n / denom, abs_tol=1e-12)


def test_family_size():
    assert len(allometric_family()) >= 10


def test_heart_rate_is_minus_quarter():
    fam = allometric_family()
    heart = next(f for f in fam if "heart" in f["quantity"])
    assert math.isclose(heart["exponent"], -0.25, abs_tol=1e-12)


def test_lifespan_is_quarter():
    fam = allometric_family()
    life = next(f for f in fam if "lifespan" in f["quantity"])
    assert math.isclose(life["exponent"], 0.25, abs_tol=1e-12)


def test_blood_pressure_invariant():
    fam = allometric_family()
    bp = next(f for f in fam if "pressure" in f["quantity"])
    assert math.isclose(bp["exponent"], 0.0, abs_tol=1e-12)


def test_white_matter_is_five_quarters():
    fam = allometric_family()
    wm = next(f for f in fam if "white matter" in f["quantity"])
    assert math.isclose(wm["exponent"], 1.25, abs_tol=1e-12)


def test_summary_verified():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_wbe_derivation_chain_five_steps():
    b = build_bridge()
    assert len(b["wbe_derivation_chain"]) == 5


def test_first_chain_step_is_master_equation():
    b = build_bridge()
    assert "q! = 2q" in b["wbe_derivation_chain"][0]["from"]


def test_theorem_mentions_kleiber_and_wbe():
    b = build_bridge()
    assert "Kleiber" in b["theorem"]
    assert "WBE" in b["theorem"]


def test_one_line_mentions_three_quarters_and_q():
    b = build_bridge()
    line = b["one_line"]
    assert "3/4" in line
    assert "q" in line


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert data["kleiber_inverted_dimension"]["matches_q"] is True


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "allometric_family",
        "wbe_derivation_chain",
        "kleiber_inverted_dimension",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
