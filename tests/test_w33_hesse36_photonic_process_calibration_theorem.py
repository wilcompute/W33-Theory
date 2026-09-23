from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_hesse36_photonic_process_calibration_theorem.py"
DATA=ROOT/"data/w33_hesse36_photonic_process_calibration_theorem.json"
def load():
    s=importlib.util.spec_from_file_location("photonic_cal",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_budget():
    o=json.loads(DATA.read_text())
    d=o["design_target"]
    assert d["F_target"]==0.99
    assert d["per_factor_min"]>0.996
    assert d["hold_phase_deg_max"]<3.4
    assert d["hold_differential_power_loss_abs_db_max"]<0.51
    assert d["sufficient_product_bound"]==0.99
    assert len(o["single_device_protocol"])==6
    assert all(o["checks"].values())
