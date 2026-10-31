"""W33 parity-compiler local-gauge optimal rank and 7 hyperbolic pairs."""
import sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_photonic_five_fronts_GF2_phase_causal_break_20261023 import adjacency
from w33_phase_oracle_mod_local_gauge_rank14_20261023 import rank_factor,centered,certificate
from w33_phase_oracle_seven_symplectic_pairs_20261023 import pairs_from_alternating,certificate as symplectic
def test_binary_rank16_is_preexisting_and_gauge_rank14_optimal():
    p=certificate()
    assert p['preexisting_W33_Gf2_adjacency_rank']==16
    assert p['new_optimal_cross_register_couplings']==14
    assert p['basepoints_checked']==40
    assert 'analysis/w33_pass88_smith_group.py' in p['W33_rank16_prior_repo_paths']
def test_14_nonlocal_terms_plus_two_local_phase_functions_reproduce_all_pairs():
    A=adjacency()
    p=certificate()
    U=np.array(p['left_cross_bit_lookup_40x14'],int)
    V=np.array(p['right_cross_bit_lookup_40x14'],int)
    L=np.array(p['left_local_phase_flags_from_A_column0'],int)
    R=np.array(p['right_local_phase_flags_from_A_row0'],int)
    assert np.array_equal(((U@V.T)%2)^L[:,None]^R[None,:],A)
def test_double_center_invariant_under_all_1_body_compensations():
    A=adjacency()
    B=centered(A)
    rng=np.random.default_rng(99)
    for _ in range(20):
        L=rng.integers(0,2,size=40,dtype=np.uint8)
        R=rng.integers(0,2,size=40,dtype=np.uint8)
        C=A^L[:,None]^R[None,:]
        assert np.array_equal(centered(C),B)
        assert rank_factor(C)[0].shape[1]>=14
def test_symplectic_seven_pairs_full_1600_address_certificate():
    A=adjacency()
    p=symplectic()
    assert p['symplectic_hyperbolic_pair_count']==7
    assert p['total_cross_parity_terms']==14
    B=np.zeros((40,40),np.uint8)
    for q in p['seven_pairs']:
        x=np.array(q['x_flag_40'],np.uint8)
        y=np.array(q['y_flag_40'],np.uint8)
        B^=(x[:,None]*y[None,:])^(y[:,None]*x[None,:])
    assert np.array_equal(B,centered(A))
    assert np.all(np.diag(B)==0) and np.array_equal(B,B.T)
def test_paired_rank_reduction_even_for_alternating_matrix():
    B=centered(adjacency())
    p=pairs_from_alternating(B)
    assert len(p)==7
    assert rank_factor(B)[0].shape[1]==2*len(p)
