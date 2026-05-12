"""Part CCCCXXXVIII -- E8 Z3 Edge-Sector Bridge."""

from __future__ import annotations

import json
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

mod = importlib.import_module("PART_CCCCXXXVIII_E8_Z3_EDGE_SECTOR_BRIDGE")


def test_verified_true() -> None:
    assert mod.Verified is True


def test_all_checks_pass() -> None:
    failed = [label for label, ok in mod.checks if not ok]
    assert failed == []


def test_check_count() -> None:
    assert len(mod.checks) == 24


def test_w33_packet_sum() -> None:
    assert mod.W33_EDGE_CORE + mod.W33_EDGE_PLUS + mod.W33_EDGE_MINUS == mod.EDGES_W33 == 240


def test_e8_packet_sum() -> None:
    assert mod.E8_G0 + mod.E8_G1 + mod.E8_G2 == 240


def test_g0_decomposition() -> None:
    assert mod.G0_DECOMP_A + mod.G0_DECOMP_B + mod.G0_DECOMP_C == mod.E8_G0 == 78


def test_e6_anchor() -> None:
    assert mod.E8_G0 == mod.EXCITED_DF2_E6 == 78


def test_81_identity() -> None:
    assert mod.E8_G1 == mod.E8_G2 == mod.Q**4 == 81


def test_run_main_writes_json() -> None:
    rc = mod.main()
    assert rc == 0
    out = ROOT / "PART_CCCCXXXVIII_e8_z3_edge_sector_bridge_results.json"
    assert out.exists()


def test_json_fields() -> None:
    out = ROOT / "PART_CCCCXXXVIII_e8_z3_edge_sector_bridge_results.json"
    if not out.exists():
        mod.main()
    data = json.loads(out.read_text(encoding="utf-8"))

    assert data["part"] == "CCCCXXXVIII"
    assert data["Verified"] is True
    assert data["checks_total"] == 24
    assert data["checks_passed"] == 24

    assert data["w33_edge_packets"]["sum"] == 240
    assert data["e8_z3_packets"]["sum"] == 240
    assert data["g0_decomposition"]["sum"] == 78
    assert data["g0_decomposition"]["equals_dim_E6"] is True
