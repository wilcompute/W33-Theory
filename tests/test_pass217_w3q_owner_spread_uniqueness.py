"""Focused regression for the GAP-owned Pass 217 W(3,q) count theorem."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass217_w3q_owner_spread_uniqueness.g"
CERT = ROOT / "data" / "w33_pass217_w3q_owner_spread_uniqueness.json"


def run_gap() -> dict:
    subprocess.run(
        ["gap", "-q", str(SCRIPT.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        timeout=300,
    )
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_pass217_gap_certificate() -> None:
    data = run_gap()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())


def test_pass217_unique_count_closure_is_q3() -> None:
    data = json.loads(CERT.read_text(encoding="utf-8"))
    theorem = data["count_theorem"]
    assert theorem["required_spreads"] == "q^2*(q+1)"
    assert theorem["regular_spread_orbit"] == "q^2*(q^2-1)/2"
    assert theorem["regular_over_required"] == "(q-1)/2"
    assert "q=3,5,7" in theorem["tested_odd_anchor_owner_map"]
    assert "1-,2-,3-fold" in theorem["tested_odd_anchor_owner_map"]
    assert "q^2(q^2-1)/2" in theorem["orbit_stabilizer_derivation"]
    assert theorem["unique_closure"] == "q=3 among prime powers q>=2"


def test_pass217_anchor_table() -> None:
    anchors = {
        row["q"]: row
        for row in json.loads(CERT.read_text(encoding="utf-8"))["anchors"]
    }
    assert anchors[2]["all_spreads"] == 6
    assert anchors[2]["required_spreads"] == 12
    assert anchors[3]["all_spreads"] == anchors[3]["regular_orbit"] == 36
    assert anchors[3]["owner_candidate_profile"] == [[1, 120]]
    assert anchors[3]["owner_cover_degree"] == 1
    assert anchors[5]["owner_cover_degree"] == 2
    assert anchors[7]["owner_cover_degree"] == 3
    assert anchors[2]["owner_candidate_profile"] == [[0, 30]]
    assert anchors[4]["owner_candidate_profile"] == [[0, 340]]
    for q in (4, 5, 7):
        assert anchors[q]["regular_orbit"] > anchors[q]["required_spreads"]
