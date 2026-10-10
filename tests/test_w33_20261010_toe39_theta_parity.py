"""Regression: theta parity exact symmetries and analytic order-five correction."""
from importlib.util import module_from_spec,spec_from_file_location
from pathlib import Path
modpath=Path(__file__).resolve().parents[1]/"analysis"/"w33_20261010_toe39_theta_parity_fifth_order.py"
spec=spec_from_file_location("toe39",modpath)
mod=module_from_spec(spec); spec.loader.exec_module(mod)

def test_theta_parity_and_fifth_order():
    v=mod.run()
    assert v["status"]=="PASS"
    assert len(v["cases"])==3
    for c in v["cases"]:
        assert c["parity_residual"]<1e-12
        assert c["off_block_residual"]<1e-12
        assert c["odd_determinant_residual"]<1e-12
        assert all(0 < r < .30 for r in c["halving_error_ratios"])
