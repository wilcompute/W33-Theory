from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_e6_cubic_diagonal_phase_weld.py"
DATA=ROOT/"data/w33_e6_cubic_diagonal_phase_weld.json"
def load():
    s=importlib.util.spec_from_file_location("diag_phase_weld",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_diagonal_weld_unlocks_54():
    o=json.loads(DATA.read_text())
    r=o["rank_and_alignment"]
    assert r["center"]["exact_jacobian_rank"]==36
    assert r["center"]["quotient_projection_rank"]==36
    assert r["external"]["exact_jacobian_rank"]==54
    assert r["external"]["quotient_projection_rank"]==36
    assert r["center_plus_external"]["exact_jacobian_rank"]==66
    assert r["center_plus_external"]["quotient_projection_rank"]==54
    assert r["center_minus_external"]["exact_jacobian_rank"]==66
    assert r["center_minus_external"]["quotient_projection_rank"]==54
    assert o["weld_consequence"]["diagonal_center_external_weld_covers_full_retyped_quotient"] is True
    assert all(o["checks"].values())
