"""Five new W33 quantum phase/eraser/nonlocal/process frontiers, independent regressions."""
import sys, math
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_photonic_five_fronts_GF2_phase_causal_break_20261023 import (
 adjacency,gf2_compiler,nine_mode_eraser,phase_recursive_nonlocal,
 causal_break_witness,_causal_break,_negativity,result)

def test_w33_40_by_40_adjacency_is_binary_symmetric_regular():
    a=adjacency()
    assert a.shape==(40,40) and np.array_equal(a,a.T)
    assert not np.any(np.diag(a)) and np.all(a.sum(axis=1)==12)
def test_gf2_factorization_exact_1600_entries():
    p=gf2_compiler()
    u=np.array(p['selected_row_coordinates'],dtype=int)
    v=np.array(p['selected_column_coordinates'],dtype=int)
    assert (u.shape,v.shape)==((40,16),(40,16))
    assert np.array_equal((u@v.T)%2,adjacency())
def test_binary_factor_rank_16_cannot_use_15_links():
    m=adjacency()
    # Independent row reduction over GF(2), separately from compiled factor.
    x=[int(''.join(map(str,reversed(a.tolist()))),2) for a in m]
    piv={}
    for num in x:
        while num:
            k=num.bit_length()-1
            if k not in piv:
                piv[k]=num;break
            num^=piv[k]
    assert len(piv)==16
def test_binary_phase_compiler_selects_exact_480_ordered_edges():
    p=gf2_compiler()
    assert p['ordered_address_phase_flips']==480
    assert p['graph_edges_undirected']==240
    assert p['bilinear_phase_links']==16
    assert p['logical_link_reduction_vs_edge_truth_table']==pytest.approx(15)
def test_nine_mode_controlled_delay_permutation_and_unitary():
    p=nine_mode_eraser()
    u=np.array(p['controlled_SUM_matrix_9x9_real'])
    assert np.array_equal(u.T@u,np.eye(9,dtype=int))
    assert np.array_equal(np.linalg.matrix_power(u,3),np.eye(9,dtype=int))
def test_eraser_causal_coherent_vs_incoherent():
    p=nine_mode_eraser()['rows']
    assert len(p)==5
    for row in p:
        c=row['offdiagonal_coherence']
        assert row['time_plus_trigger']==pytest.approx(1/3)
        assert row['path_plus_conditioned_on_time_plus']==pytest.approx((1+2*c)/3)
    assert p[0]['path_plus_and_time_plus_joint_probability']==pytest.approx(1/9)
    assert p[-1]['path_plus_and_time_plus_joint_probability']==pytest.approx(1/3)
def test_nonnearest_neighbor_recursion_breaks_nearest_boundary_area_law():
    p=phase_recursive_nonlocal()
    h=p['single_cross_edge_entropy_bits']
    assert h==pytest.approx(4.803856189774729)
    assert p['depth4_two_cross_edges_middle_cut']['entropy_bits']==pytest.approx(2*h)
    assert p['depth4_two_cross_edges_middle_cut']['schmidt_rank']==1600
    assert p['depth4_one_edge_middle_cut']['schmidt_rank']==40
def test_two_spokes_phase_graph_has_normalized_density():
    p=phase_recursive_nonlocal()
    ev=np.array(p['depth3_two_spokes_spectrum'])
    assert ev.min()>=-1e-10
    assert ev.sum()==pytest.approx(1,abs=1e-9)
    assert p['depth3_two_spokes_cross_cut_entropy_bits']>0
def test_memory_reference_entanglement_survives_only_when_E_retained():
    p=causal_break_witness()
    assert p['final_RS_negativity_environment_retained']==pytest.approx(1)
    assert p['final_RS_negativity_environment_erased_at_break']==pytest.approx(0)
    assert p['three_qutrit_total_dimension']==27
def test_coherent_input_survives_break_distinct_from_incoherent_null():
    vals=causal_break_witness()['coherence_control']
    assert vals[0]['post_break_path_plus_with_E_memory']==pytest.approx(1)
    assert vals[1]['post_break_path_plus_with_E_memory']==pytest.approx(1/3)
    assert all(v['with_environment_reset']==pytest.approx(1/3) for v in vals)
def test_only_maths_not_fabricated_memory():
    d=result()
    assert d['parts']['W33_GF2_16_channel_phase_compiler']['adjacency_reconstruction_exact']
    assert 'no calibrated' in d['physical_boundary'].lower()
    assert 'nonlinearities' in d['parts']['W33_GF2_16_channel_phase_compiler']['engineering']
