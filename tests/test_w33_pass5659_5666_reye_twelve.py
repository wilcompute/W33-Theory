"""Regression lock for Passes 5659-5666."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "PART_W33_PASS5659_5666_THE_REYE_TWELVE_IS_T12_165.json"
pytestmark = pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")


def cert():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_reye_twelve_is_t12_165():
    p = cert()["pass_5659"]
    assert p["transitive_id"] == 165
    assert p["stabiliser_id"] == [48, 48]
    assert p["faithful"] is True and p["action_on_16_faithful"] is True


def test_exactly_three_of_nine_are_wf4z():
    p = cert()["pass_5660"]
    assert p["transitive_degree12_order576"] == 9
    assert sorted(p["isomorphic_to_wf4z"]) == [161, 163, 165]
    assert 165 in p["isomorphic_to_wf4z"], "the Reye 12 must be one of them"


def test_the_two_1152s_have_different_ids():
    p = cert()["pass_5661"]
    a, b = p["the_two_1152s"]
    assert a != b, "coincidence ten, at the level of an identifier"
    assert a == [1152, 157478] and b == [1152, 157849]
    assert p["the_576s_are_all"] == [576, 8654]


def test_seven_side_does_not_meet():
    p = cert()["pass_5662"]
    assert p["seven_divides_576"] is False
    assert p["lcm"] == 4032 == 576 * 7
    assert 576 % 7 != 0 and 168 % 7 == 0


def test_the_settling_test_is_recorded_with_all_outcomes():
    p = cert()["pass_5663"]
    assert p["typed_here"] is False, "must not claim what was not computed"
    assert set(p["outcomes"]) == {"165", "161_or_163", "other"}


def test_guard_narrowed_and_selftests():
    p = cert()["pass_5664_5665"]
    f = [v["findings"] for v in p["progression"]]
    assert f == sorted(f, reverse=True), "each narrowing must reduce findings"
    assert f[0] == 547 and f[-1] == 124
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_transitivity.py"),
                        "--selftest"], capture_output=True, text=True, timeout=300)
    assert r.returncode == 0 and "FAIL" not in r.stdout


def test_zero_findings_is_recorded_as_inapplicable():
    p = cert()["pass_5666"]
    assert p["findings"] == 0
    assert "INAPPLICABLE" in p["reading"], "must not read zero as verification"
