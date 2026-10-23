"""Self-entanglement and recursion falsifiers, including reused vs fresh clock."""
import sys, math
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_single_photon_recursive_self_entanglement_20261023 import (
 ptime_state,fresh_time_ghz,coherent_mixture,pure_density,reduced_path,
 pure_negativity,vn_entropy,eraser_witness,choi,channel_choi_dephase,
 negativity,coherent_budget,certificate)
def test_reuse_of_three_time_bins_revives_and_is_periodic():
    for n in range(7):
        assert np.linalg.norm(ptime_state(n)-ptime_state(n%3))<1e-13
        assert pure_negativity(ptime_state(n),3)==pytest.approx(0 if n%3==0 else 1,abs=1e-12)
    assert np.linalg.norm(ptime_state(3)-ptime_state(0))<1e-13
def test_fresh_register_entanglement_saturates_not_grows():
    for n in range(1,6):
        s=fresh_time_ghz(n)
        assert np.linalg.norm(s)==pytest.approx(1)
        assert vn_entropy(reduced_path(s,3**n))==pytest.approx(math.log2(3))
        assert pure_negativity(s,3**n)==pytest.approx(1)
def test_quantum_eraser_distinguishes_coherent_from_incoherent_same_diagonal():
    for n in range(1,6):
        coherent=eraser_witness(n,1)
        mixed=eraser_witness(n,0)
        assert coherent['all_time_fourier_plus_trigger_probability']==pytest.approx(3**(-n))
        assert mixed['all_time_fourier_plus_trigger_probability']==pytest.approx(3**(-n))
        assert coherent['conditional_path_plus_probability']==pytest.approx(1)
        assert mixed['conditional_path_plus_probability']==pytest.approx(1/3)
        assert coherent['conditional_path_state_purity']==pytest.approx(1)
        assert mixed['conditional_path_state_purity']==pytest.approx(1/3)
def test_quantum_eraser_separates_dephasing_visibility():
    for v in (0,.2,.5,.9,1):
        z=eraser_witness(3,v)
        assert z['conditional_path_plus_probability']==pytest.approx((1+2*v)/3)
def test_choi_identity_is_maximally_entangled_mathematically_even_when_no_physical_pair():
    for U in (np.eye(3),np.diag([1,np.exp(2j*np.pi/3),1])):
        v=choi(U)
        assert vn_entropy(reduced_path(v,3))==pytest.approx(math.log2(3))
        assert pure_negativity(v,3)==pytest.approx(1)
def test_choi_composed_dephasing_has_exact_decay():
    for lam in (0,.1,.5,.9,1):
        for n in range(6):
            a=channel_choi_dephase(n,lam)
            assert np.trace(a)==pytest.approx(1)
            assert negativity(a,3,3)==pytest.approx(lam**n,abs=1e-11)
def test_self_entanglement_is_not_two_photon_nonlocality():
    x=certificate(3)
    assert 'not two copies of the physical photon' in x['operational_boundary'][0]
    assert 'not a loophole-free Bell nonlocality' in x['operational_boundary'][2]
    assert 'no quantum storage' in x['operational_boundary'][4]
def test_w33_fractal_and_time_mode_resources_both_exponential():
    x=certificate(5)
    assert len(x['budgets'])==6
    assert x['budgets'][5]['W33_site_substitution_packet_count']==40**5
    assert x['budgets'][5]['full_time_hilbert_dimension']==243
    assert x['budgets'][5]['BT1700_ABI_total_ticks_not_seconds']==72*40**5
    assert x['budgets'][5]['all_plus_time_eraser_trigger']==pytest.approx(1/243)
def test_per_step_loss_and_dephasing_are_not_automatically_self_correction():
    arr=[coherent_budget(n,.5,.1) for n in range(6)]
    assert all(arr[i+1]['survival_probability']<arr[i]['survival_probability'] for i in range(5))
    assert all(arr[i+1]['phase_offdiag_visibility']<arr[i]['phase_offdiag_visibility'] for i in range(5))
def test_invalid_physical_omissions_are_caught():
    with pytest.raises(ValueError):choi(np.zeros((3,3)))
    with pytest.raises(ValueError):eraser_witness(0)
    with pytest.raises(ValueError):fresh_time_ghz(7)
    with pytest.raises(ValueError):channel_choi_dephase(2,1.01)
