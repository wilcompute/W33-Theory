"""Part DCCXIX -- Self-closure theorem tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxix_self_closure_theorem import (  # noqa: E402
    OUT_PATH,
    build_bridge,
    codec_entropy_bits,
    delta_h,
    saturation_entropy_bits,
    write_bridge,
)


def test_loop_closes():
    assert build_bridge()["summary"]["loop_closes"] is True


def test_all_identities_hold():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_codec_entropy_equals_saturation_entropy():
    assert math.isclose(codec_entropy_bits(3), saturation_entropy_bits(3), abs_tol=1e-12)


def test_codec_entropy_value():
    # log2(12) ~ 3.585
    assert math.isclose(codec_entropy_bits(3), math.log2(12), abs_tol=1e-12)


def test_delta_h_zero_at_q_3():
    assert math.isclose(delta_h(3), 0.0, abs_tol=1e-12)


def test_closure_loop_has_seven_steps():
    b = build_bridge()
    assert len(b["closure_loop"]) == 7


def test_loop_first_and_last_step_match():
    b = build_bridge()
    first = b["closure_loop"][0]["from"]
    last = b["closure_loop"][-1]["to"]
    assert "Delta_H" in first
    assert "loop closes" in last


def test_axioms_used():
    b = build_bridge()
    assert any("DCCXVII" in a for a in b["axioms_used"])
    assert any("DCCXVIII" in a for a in b["axioms_used"])


def test_q_factorial_plus_two_q_identity_at_q_3():
    assert math.factorial(3) + 2 * 3 == 4 * 3 == 12


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Self-Closure Theorem" in b["theorem"]
    assert "loop closes" in b["one_line"].lower()


def test_write_bridge_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["loop_closes"] is True
    assert data["summary"]["all_identities_hold"] is True


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "closure_loop",
        "consistency",
        "identities",
        "theorem",
        "one_line",
        "axioms_used",
        "honesty_boundary",
    ):
        assert key in data
