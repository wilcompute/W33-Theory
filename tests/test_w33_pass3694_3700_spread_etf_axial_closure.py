from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass3694_3700_spread_etf_axial_closure.py"
FROZEN = ROOT / "data" / "PART_3694_3700_SPREAD_ETF_AXIAL_CLOSURE_results.json"


def load_module():
    spec = importlib.util.spec_from_file_location("pass3694_3700", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_frozen_certificate_reproduces_exactly():
    module = load_module()
    expected = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert module.build_certificate() == expected


def test_headline_invariants():
    data = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert all(data["checks"].values())
    assert data["spread_incidence_etf"]["frame"] == "real ETF(15,36)"
    assert data["naimark_photonic_certificate"]["minimal_guard_rank"] == 21
    assert data["norton_axial_algebra"]["triple_system"]["triples"] == 120
    assert data["magic_ray_firewall"]["degree_mismatch"] is True
    assert data["ternary_panel_cover_no_go"]["unbranched_type_preserving_cover_possible"] is False
