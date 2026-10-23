"""Regress exact metaplectic infinite-order witness and four-rail leakage law."""
import math,sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_walsh_qutrit_metaplectic_noise_20261023 import (
    exact_infinite_order_witness,code_basis,leakage_for_phases,unequal_loss,sweep,run)

def test_exact_algebraic_noninteger_trace_and_determinant():
    p=exact_infinite_order_witness()
    assert p['F3_times_D_trace_exact']=='-1/sqrt(3)'
    assert p['F3_times_D_determinant_exact']=='-i'
    assert p['Qsqrt3_trace_norm_exact']=='-1/3'
    assert 'does NOT imply' in p['limitation']

def test_four_mode_walsh_code_isometry_and_aux():
    V,a=code_basis()
    assert np.linalg.norm(V.conj().T@V-np.eye(3))<1e-14
    assert np.linalg.norm(V.conj().T@a)<1e-14
    assert np.linalg.norm(V@V.conj().T+np.outer(a,a.conj())-np.eye(4))<1e-14

def test_single_differential_rail_breaks_code_but_global_does_not():
    assert leakage_for_phases((.4,.4,.4,.4))<1e-13
    val=leakage_for_phases((.0,.0,.0,.4))
    assert 0<val<1/3
    assert leakage_for_phases((.4,.0,.0,.0))==pytest.approx(val,abs=1e-14)
    with pytest.raises(ValueError):leakage_for_phases((0,0,0))

def test_loss_distinguishes_environment_and_auxiliary():
    equal=unequal_loss((.8,)*4)
    assert equal['power_in_auxiliary']<1e-14
    assert equal['survival_4rails']==pytest.approx(.64)
    assert equal['lost_environment']==pytest.approx(.36)
    asymmetric=unequal_loss((1,.9,.8,.7))
    assert asymmetric['power_in_auxiliary']>0
    assert asymmetric['survival_4rails']+asymmetric['lost_environment']==pytest.approx(1)
    with pytest.raises(ValueError):unequal_loss((1,1,1,1.1))

def test_analytic_gaussian_leakage_expectation_against_monte_carlo():
    result=sweep(samples=1500)
    for row in result['phase_noise']['measurements']:
        sig=row['rail_phase_sigma_rad']
        prediction=(1-math.exp(-sig**2))/4
        assert row['analytic_expected_auxiliary_leakage']==pytest.approx(prediction)
        assert row['absolute_error']<6*row['monte_carlo_standard_error']+1e-7

def test_exact_reproducibility_and_scope():
    a,b=run(samples=800),run(samples=800)
    assert a['sha256']==b['sha256']
    assert any('four different child nodes' in s for s in a['hardware_boundary'])
    assert any('not' in s.lower() for s in a['hardware_boundary'])
