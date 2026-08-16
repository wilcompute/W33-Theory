"""Regression lock for Passes 5651-5658.

Locks the divisibility obstruction, the Pass 5644 correction, and the guard's
self-test, so none of them can be quietly reversed.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "PART_W33_PASS5651_5658_BRIDGE_NOT_EQUIVARIANT_84_IS_THE_OBSTRUCTION.json"
PRIOR = ROOT / "data" / "PART_W33_PASS5643_5650_TOMOTOPE_W33_BRIDGE_IS_WF4_MOD_CENTRE.json"


def test_84_does_not_divide_576():
    """The structural obstruction: the 7 in 84 cannot appear in a 2^6*3^2 group."""
    assert 576 == 2 ** 6 * 3 ** 2
    assert 576 % 24 == 0
    assert 576 % 192 == 0
    assert 576 % 84 != 0, "84 = 2^2*3*7; the 7 is the obstruction"
    assert 576 % 168 != 0
    assert 84 % 7 == 0 and 576 % 7 != 0


def test_order_576_is_not_an_identification():
    """8,681 groups share order 576, so a 576 match identifies nothing."""
    d = json.loads(CERT.read_text(encoding="utf-8"))
    assert d["pass_5653"]["groups_of_order_576"] == 8681


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_equivariance_is_not_automatic():
    d = json.loads(CERT.read_text(encoding="utf-8"))
    p = d["pass_5651"]
    assert p["index12_classes"] == 7
    assert p["inequivalent_faithful_actions"] == 3
    assert p["faithful_images"] == [2, 4, 6, 7]


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_the_1152_kill_survives_the_correction():
    """Pass 5652 corrects a 576 field; the W(F4) vs S4wrS2 kill must stand."""
    d = json.loads(CERT.read_text(encoding="utf-8"))
    assert d["pass_5652"]["wf4_mod_z_smallgroup"] == [576, 8654]
    ids = [e["id"] for e in d["pass_5652"]["s4wrs2_index2_normal"]]
    assert [576, 8654] in ids, "W(F4)/Z IS an index-2 subgroup of S4 wr S2"
    assert len(ids) == 3, "three index-2 normal subgroups; First() picked the wrong one"
    prior = json.loads(PRIOR.read_text(encoding="utf-8"))
    assert prior["pass_5644"]["wf4_iso_s4wrs2"] is False, "the 1152 kill stands"
    assert "CORRECTED_BY_PASS_5652" in prior["pass_5645"], "the correction is recorded"


def test_transitivity_guard_selftest_passes():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_transitivity.py"),
                        "--selftest"], capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stdout
    assert "FAIL" not in r.stdout


def test_guard_reproduces_coincidence_nine():
    sys.path.insert(0, str(ROOT / "scripts"))
    from check_transitivity import findings
    assert findings({"rot_q4_order": 192, "orbit_sizes": [24, 84, 84]})
    assert not findings({"group_order": 192, "orbit_sizes": [96, 96]})


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_q9_bounds_stay_open():
    d = json.loads(CERT.read_text(encoding="utf-8"))
    p = d["pass_5658"]
    assert p["bounds"] == [51, 80]
    assert p["proved"] is False
    assert p["status"] == "OPEN"
    assert p["incumbent_now"] > p["incumbent_before"]
