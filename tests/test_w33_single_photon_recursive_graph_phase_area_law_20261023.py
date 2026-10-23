"""Exact SRG spectral certificate and W33 one-photon recursive graph-state area law."""
import sys,math
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_single_photon_recursive_graph_phase_area_law_20261023 import (
    matrix,spectrum,state,local_cut_svd,analytic_area_law)
def test_adjacency_srg_matrix_identity():
    a=matrix()
    assert a.shape==(40,40)
    assert (a.sum(axis=1)==12).all()
    assert np.array_equal(a@a,12*np.eye(40,dtype=int)+2*a+4*(1-np.eye(40,dtype=int)-a))
def test_two_digit_exact_w33_phase_schmidt_multiplicities():
    a=spectrum()
    assert a['Schmidt_rank']==40
    assert a['Schmidt_probability_spectrum']=={'0.16':1,'0.04':15,'0.01':24}
    assert a['Schmidt_purity']==pytest.approx(.052)
    assert a['Schmidt_entropy_bits']<math.log2(40)
    assert a['Schmidt_entropy_bits']>4.8
def test_depth_three_every_contiguous_cut_obeys_area_law():
    for n in (2,3):
        for cut in range(1,n):
            vals=local_cut_svd(n,cut)
            expected=np.array([.4]+[.2]*15+[.1]*24)
            assert len(vals)==40
            assert np.allclose(vals,expected,atol=1e-11)
def test_uniform_recursive_addresses_without_cross_digit_phase_are_product():
    for n in (2,3):
        a=np.ones((40,)*(n),dtype=float)/40**(n/2)
        mat=a.reshape(40,-1)
        assert np.linalg.matrix_rank(mat,tol=1e-12)==1
def test_area_law_all_cut_table_extends_without_exponential_svd():
    a=analytic_area_law(maxdepth=7)
    assert len(a['recursion_table'])==sum(range(1,7))
    assert all(row['Schmidt_rank']==40 for row in a['recursion_table'])
    assert len({round(row['Schmidt_entropy_bits'],12) for row in a['recursion_table']})==1
    assert a['recursion_table'][-1]['physical_mode_address_count_if_all_independent']==40**7
def test_computational_guard_prevents_unbounded_full_state():
    with pytest.raises(ValueError):state(5)
    with pytest.raises(ValueError):local_cut_svd(4,2)
def test_no_unbuilt_photonic_gate_claimed():
    a=analytic_area_law()
    assert any('fabricated' in x for x in a['physical_boundary'])
    assert 'programmable phase' in a['physical_boundary'][0]
