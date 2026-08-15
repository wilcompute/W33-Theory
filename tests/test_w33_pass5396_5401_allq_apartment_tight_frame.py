from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_pass5396_5401_allq_apartment_tight_frame.py"
FROZEN = ROOT / "data/PART_W33_PASS5396_5401_ALLQ_APARTMENT_TIGHT_FRAME.json"
BT546 = ROOT / "data/PART_BT546_W33_LEVI_CYCLE_PHASE_FRAME_UNIFICATION_results.json"


def load_module():
    spec = importlib.util.spec_from_file_location("pass5396_apartments", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_all_anchor_apartment_counts_and_overlaps():
    m = load_module()
    for q in m.ANCHORS:
        row = m.row(q)
        n = (q + 1) ** 2 * (q * q + 1)
        assert row["flags"] == n
        assert row["apartments"] * 8 == n * q**4
        assert row["apartments_per_flag_edge"] == q**4
        assert row["pair_apartment_counts_by_distance"] == [q**4, q**3, q**2, q, 1]
        assert row["signed_overlap_by_distance"] == [q**4, -q**3, q**2, -q, 1]
        assert row["CCt_rank"] == q**4
        assert row["CCt_nonzero_eigenvalue"] == n


def test_frozen_certificate_matches_executable_structure():
    m = load_module()
    observed = m.build_certificate()
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert observed == frozen


def test_q3_exactly_recovers_bt546_cycle_frame():
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    old = json.loads(BT546.read_text(encoding="utf-8"))
    q3 = frozen["anchors"]["3"]
    assert old["objects"]["levi_edges_flags"] == q3["flags"] == 160
    assert old["objects"]["simple_8_cycles"] == q3["apartments"] == 1620
    assert old["objects"]["levi_beta1"] == q3["cycle_dimension"] == 81
    assert old["signed_phase_frame"]["rank"] == q3["CCt_rank"] == 81
    assert old["signed_phase_frame"]["spectrum"]["160"] == 81
    assert old["unification"]["support_identity"] == "160*81 = 1620*8 = 12960"
