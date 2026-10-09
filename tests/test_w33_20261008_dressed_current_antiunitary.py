"""Regression: all 160 actual edge currents admit dressed antiunitary."""
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("w33_dressed_t",ROOT/"analysis/w33_20261008_dressed_current_antiunitary.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_all_current_factors_swap_exactly():
    data=module.certificate()
    assert data["status"]=="PASS"
    assert data["currents_checked"]==160
    assert data["canonical_cross_product_max_abs"]==0
    assert "T J_e T^-1" in data["quantum_current_invariance"]
    assert data["hamiltonian_invariance"]=="T H T^-1=H for H=sum_e J_e^2"
