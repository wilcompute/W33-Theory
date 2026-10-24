"""Independent GQ(3,3) cospectral phase entanglement vs GF2 circuit rank tests."""
import math,sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_q43_cospectral_mode_entanglement_phase_complexity_20261023 import (
 graphs,phase_model,local_isometry_witness,certificate,S_operator)
from w33_q43_four_address_alternating_cut_purity_20261023 import (
 alternating_four_integer_purity,certificate as purity_certificate)
from w33_q43_eight_term_oracle_rtl_20261023 import produce
from w33_phase_oracle_mod_local_gauge_rank14_20261023 import centered,rank_factor

def test_both_srg_parameters_and_numerical_spectrum_match():
    W,Q=graphs()
    for A in (W,Q):
        ev=np.linalg.eigvalsh(A)
        assert np.allclose(ev,np.array([-4]*15+[2]*24+[12]))
        assert np.all(A.sum(axis=0)==12)
def test_computational_address_phase_oracle_cost_is_different():
    W,Q=graphs()
    assert rank_factor(W)[0].shape[1]==16
    assert rank_factor(Q)[0].shape[1]==10
    assert rank_factor(centered(W))[0].shape[1]==14
    assert rank_factor(centered(Q))[0].shape[1]==8
def test_all_1600_phase_entries_and_seven_versus_four_symplectic_pairs():
    W,Q=graphs()
    for A,r,sp in ((W,14,7),(Q,8,4)):
        p=phase_model('test',A)
        assert p['optimal_nonlocal_binary_rank_mod_local_phases']==r
        assert p['hyperbolic_pair_count']==sp
        L=np.array(p['cross_register_flags_40xR_L'])
        R=np.array(p['cross_register_flags_40xR_R'])
        fix=np.array(p['left_local_phase_table'])
        fix2=np.array(p['right_local_phase_table'])
        assert np.array_equal(((L@R.T)%2)^fix[:,None]^fix2[None,:],A)
def test_equal_pure_state_schmidt_probabilities_and_entropy():
    p=certificate()
    W,Q=p['systems']['W33'],p['systems']['Q43']
    assert W['schmidt_probs']==Q['schmidt_probs']
    assert W['schmidt_entropy_bits']==pytest.approx(Q['schmidt_entropy_bits'],abs=1e-12)
    assert W['schmidt_purity']==pytest.approx(.052)
def test_explicit_real_orthogonal_local_equivalence_exists():
    W,Q=graphs()
    p=local_isometry_witness(W,Q)
    assert p['sign_state_local_equivalence_frobenius_residual']<1e-9
    assert p['adjacency_similarity_frobenius_residual']<1e-9
    assert 'no two-party entanglement monotone' in p['critical_consequence']
def test_even_four_address_alternating_cut_purity_is_cospectrally_blind():
    z=purity_certificate()
    assert not z['numerators_different']
    assert z['W33']['purity']==pytest.approx(.0020128)
    assert z['Q43']['purity']==pytest.approx(.0020128)
    assert z['W33']['nonadjacent_two_address_xAx_values']=={'-32':1080}
    assert z['Q43']['nonadjacent_two_address_xAx_values']=={'-32':1080}
def test_integer_noncontiguous_purity_contraction_matches_explicit_terms():
    W,_=graphs()
    S=S_operator(W)
    H=S@S
    for a,aprime,c,cprime in [(0,1,2,3),(8,6,4,9),(2,2,17,17)]:
        x=(S[:,c]*S[:,cprime])
        left=sum(S[a,b]*S[aprime,b]*x[b] for b in range(40))
        expr=H[c,cprime]*left/40**4
        direct=0.
        for b in range(40):
            for dd in range(40):
                f=S[a,b]*S[b,c]*S[c,dd]/(40**2)
                g=S[aprime,b]*S[b,cprime]*S[cprime,dd]/(40**2)
                direct+=f*g
        assert expr==pytest.approx(direct,abs=1e-14)
def test_q43_rtl_generation_uses_four_pairs_and_complete_address_controls():
    p=produce()
    assert p['binary_cross_terms']==8 and p['symplectic_pairs']==4
    assert p['valid_address_truth_table_cases']==1600
    assert p['invalid_address_cases']==2496
    assert p['full_interface_bits']==28
    s=(ROOT/'hardware/q43_phase_oracle_rank8_20261023.sv').read_text()
    assert "cross_comb=da[7:0]&db[7:0]" in s
    assert 'flip_comb=(^cross_comb)^da[8]^db[8]' in s
def test_bounded_hardware_claims_are_explicit_in_certificate():
    c=certificate()
    assert c['difference_in_optimal_restricted_binary_couplings']==6
    assert 'unrestricted local' in c['local_equivalence']['critical_consequence'].lower()
    assert 'not optical MZI' in c['physical_no_go']
