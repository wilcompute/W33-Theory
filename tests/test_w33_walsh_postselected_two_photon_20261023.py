"""Independent checks of two-photon Walsh-qutrit passive-optics postselection."""
import sys,math
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_walsh_two_photon_postselected_entangler_20261023 import (
    encoder,eight_mode_coupler,coincidence_kraus,state_stats,scan)
def test_eight_mode_passive_primitive_is_unitary():
    for theta in (0,.1,math.pi/4,math.pi/2):
        U=eight_mode_coupler(theta)
        assert np.linalg.norm(U.conj().T@U-np.eye(8))<1e-12
def test_permanent_coin_blocks_and_no_bosonic_loss_at_zero():
    K=coincidence_kraus(eight_mode_coupler(0))
    assert np.linalg.norm(K-np.eye(16))<1e-12
    V=encoder();E=np.kron(V,V)
    assert np.linalg.norm(E.T@K@E-np.eye(9))<1e-12
def test_full_rail_swap_postselected_qutrit_entangled_state():
    rep=scan()
    target=rep['ideal_full_swap_end_state']
    assert target['whole_bank_coincidence_probability']==pytest.approx(5/8)
    assert target['qutrit_code_postselected_success_probability']==pytest.approx(.5)
    assert target['partial_transpose_negativity']==pytest.approx(.25)
    assert target['entanglement_entropy_bits']>0
def test_without_nonlocal_beamsplitter_initial_product_stays_product():
    V=encoder();E=np.kron(V,V)
    state=np.eye(9)[:,0]
    x=E.T@coincidence_kraus(eight_mode_coupler(0))@E@state
    assert state_stats(x)['partial_transpose_negativity']<1e-12
def test_destructive_conditioning_is_not_heralded_gate():
    r=scan()
    assert any('NOT' in x or 'not' in x for x in r['postselection'].split())
    assert any('composable' in x for x in r['not_claimed'])
