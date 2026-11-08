"""Hodge-frame, genuine E6 matrix-rank, and optical routing regressions."""
import importlib.util
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("w33_gauge_e6_optics",
       ROOT/"analysis/w33_20261108_gauge_E6_optical_followthrough.py")
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)

@pytest.fixture(scope="module")
def cert():return M.produce(ROOT)

def test_exact_hodge_translation_frame_multiplicities(cert):
    a=cert["gauge"]
    assert a["S4_seed_rank"]==2
    assert a["T27_averaged_frame_eigenvalues"]=={"0":90,"1/12":12,"1/6":6}
    assert a["affine_generated_sector_rank"]==18
    assert a["unreached_H1_dim"]==28

def test_S4_seed_is_not_translation_stable(cert):
    a=cert["gauge"]
    assert a["S4_seed_translation_commutator_norm"]>0.1
    assert abs(a["frame_trace"]-2)<1e-10
    assert "translation stable" in a["constraint"]

def test_native_1620_tensor_alternating_81(cert):
    a=cert["E6"]
    assert a["records"]==1620
    assert a["dimension"]==81 and a["native_rank"]==78
    assert a["max_antisymmetry_residual"]<1e-10
    assert a["max_zero_singular_value"]<1e-8
    assert a["min_nonzero_singular_value"]>1e-7

def test_minimum_rank_three_repair_is_algebraic_not_e6_physics(cert):
    a=cert["E6"]
    assert a["rank_after_rank_k_artificial_corrections"]=={"0":78,"1":79,"2":80,"3":81}
    assert a["alternating_odd_size_never_full_rank"]
    assert "not E6-invariant" in a["physical_limit"]

def test_optical_block_order_exhaustive_certificate(cert):
    a=cert["optics"]
    assert a["tested_orders"]==362880
    assert a["initial_lexicographic_crossing_counts"]==[12,162,162,12]
    assert a["b_first_lexicographic_crossing_counts"]==[12,54,54,12]
    assert a["optimized_crossing_counts"]==[12,30,30,12]
    assert a["full_permutation_swaps_after"]==84
    assert a["full_permutation_swaps_before"]==348

def test_optical_scope_cannot_ignore_tritter_routing(cert):
    o=cert["optics"]
    assert o["tritter_count"]==27
    assert o["upper_bound_internal_two_mode_couplers"]==81
    assert o["generic_27_port_unitary_couplers"]==351
    assert "NOT included" in o["critical_limit"]
    assert "interferometrically" in o["phase_witness"]


def test_full_tritter_regroup_route_shows_hidden_cost(cert):
    x=cert["optics"]
    route=x["best_feasible_tritter_regroup_route"]
    assert route["total_regroup_swaps"]==288
    assert route["tritter_axis_sequence"] in ([0,2,1],[2,0,1])
    assert sum(route["routing_swaps_by_transition"])==288
    assert x["total_1d_adjacent_swaps_in_explicit_schedule"]==372
    assert x["upper_bound_internal_plus_active_swap_interactions"]==453
    assert x["not_global_tritter_routing_optimum"]

def test_regrup_several_axis_groups_are_physically_contiguous():
    import itertools
    order=list(itertools.product(range(3),repeat=3))
    for axis in range(3):
        nxt,cost=M.tritter_regroup_nearest(order,axis)
        assert 0<=cost<=27*26//2
        for i in range(0,27,3):
            triples=nxt[i:i+3]
            assert len({tuple(v[k] for k in range(3) if k!=axis) for v in triples})==1
            assert len({v[axis] for v in triples})==3
