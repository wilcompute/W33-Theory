import sys,json
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_surface_hodge_transport import hodge_audit,transport_audit,DurableSurface
from w33_oscillator_calibration_test import audit as oscillator
from w33_frozen_formula_null_audit import audit as null_audit,uniform_window_probability

def test_exact_hodge_and_snapshot_certificates():
    stored=json.loads((ROOT/'analysis/w33_surface_hodge_transport.json').read_text())
    assert hodge_audit()==stored['hodge']
    assert transport_audit()==stored['transport']

def test_repeated_surgery_preserves_updated_old_state(tmp_path):
    p=json.loads((ROOT/'analysis/w33_genus_six_execution.json').read_text())['surface']
    vm=DurableSurface(p['oriented_faces'],p['symplectic_cycles'],[0]*12)
    vm.allocate();vm.allocate();vm.state[0]=2
    path=tmp_path/'state.json';vm.save(path);vm=DurableSurface.recover(path)
    vm.free();vm.free();assert vm.state==[2]+[0]*11

def test_synthetic_inference_replay():
    a=oscillator();b=json.loads((ROOT/'analysis/w33_oscillator_calibration_test.json').read_text())
    np.testing.assert_allclose(a['mechanical_fit'],b['mechanical_fit'],rtol=1e-8)
    assert a['heldout_chi_square_first_order']>100*a['heldout_chi_square_mechanical']

def test_frozen_formula_hash_and_invalid_null():
    assert null_audit()==json.loads((ROOT/'analysis/w33_frozen_formula_null_audit.json').read_text())
    with pytest.raises(ValueError):uniform_window_probability(.5,.6,1,0)
