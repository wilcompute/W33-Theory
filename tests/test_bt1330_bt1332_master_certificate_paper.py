#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1330_source_epoch_wording_patched():
    bt1321 = (ROOT / "proofs" / "BT1321_holonet_q3_atlas_bridge.md").read_text(encoding="utf-8")
    bt1326 = (ROOT / "proofs" / "BT1326_w33_holonet_master_synthesis.md").read_text(encoding="utf-8")
    assert "rolling chart-phase closure" in bt1321
    assert "rolling chart-phase closure" in bt1326
    assert "lcm(3660, 1620) = 10980" not in bt1321
    assert "lcm(3660, 1620)" not in bt1326


def test_bt1331_master_certificate_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1331_master_synthesis_certificate.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1331
    assert out["verified"] is True
    data = json.loads((ROOT / "data" / "bt1331_master_synthesis_certificate.json").read_text(encoding="utf-8"))
    assert data["checks"]["bt1326_mentions_rolling_epoch"] is True
    assert data["checks"]["bt1326_no_false_epoch_lcm"] is True


def test_bt1332_paper_build_manifest():
    data = json.loads((ROOT / "data" / "bt1332_paper_build_manifest.json").read_text(encoding="utf-8"))
    assert data["compiled"] is True
    assert data["pages"] == 9
    assert "BT1328 rolling epoch repair" in data["paper_scope"]
    assert "lcm" in data["key_correction"]
