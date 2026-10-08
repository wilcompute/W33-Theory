"""Independent checks of six bounded TOE-frontier constructions."""
from __future__ import annotations
import sys
from fractions import Fraction as F
from pathlib import Path

import networkx as nx
import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_six_toe_frontier_followthrough as m
from w33_20261008_dual_27_electrical_transport import build_graphs


def test_exact_projector_and_time_average_independent_phase_quadrature():
    r=m.coherent_frontier()
    for name,a in build_graphs().items():
        p=m.spectral_projectors(a)
        for lam,(num,den) in p.items():
            assert np.array_equal(num.T,num)
            assert np.array_equal(num@num,den*num)
            assert abs(np.trace(num)/den-r[name]["spectrum"][str(lam)])<1e-12
        # Integer eigenvalue gaps; 32 equally spaced Fourier samples cancel
        # every nonzero frequency difference (at most 12).
        sampled=np.zeros_like(a,dtype=float)
        for t in 2*np.pi*np.arange(32)/32:
            u=sum(np.exp(-1j*lam*t)*num/den for lam,(num,den) in p.items())
            sampled+=np.abs(u)**2/32
        analytic=np.array([
            [sum(float(F(int(num[i,j]*num[i,j]),den*den)) for num,den in p.values())
             for j in range(27)] for i in range(27)])
        assert np.max(abs(analytic-sampled))<1e-12
        assert np.max(abs(analytic.sum(axis=1)-1))<1e-12
    assert r["point_far_H27"]["exact_infinite_time_average_offdiag"]=={
        "13/1458":216,"20/729":108,"110/729":27}
    assert r["line_transverse_null"]["exact_infinite_time_average_offdiag"]=={
        "14/729":162,"20/729":108,"26/729":81}


def test_explicit_szegedy_isometry_and_reflection_norms():
    for a in build_graphs().values():
        v=np.zeros((729,27))
        for i in range(27):
            for j in range(27):
                if a[i,j]:v[27*i+j,i]=1/np.sqrt(8)
        assert np.max(abs(v.T@v-np.eye(27)))<1e-13
        x=np.arange(729,dtype=float)
        x/=np.linalg.norm(x)
        r=2*v@(v.T@x)-x
        assert abs(np.linalg.norm(r)-1)<1e-13
        uniform=np.zeros(729)
        uniform[np.ravel(a)>0]=1/np.sqrt(216)
        assert np.max(abs((2*v@(v.T@uniform)-uniform)-uniform))<1e-13
        assert np.array_equal(uniform.reshape(27,27).T,uniform.reshape(27,27))


def test_induced_cycle_closure_34_and_invariant_planes():
    r=m.lie_frontier()
    g=m.levi_graph()
    cyc=r["explicit_induced_8_cycle"]
    assert len(cyc)==8 and len(set(cyc))==8
    assert all(g.has_edge(cyc[i],cyc[(i+1)%8]) for i in range(8))
    assert all(not g.has_edge(cyc[i],cyc[(i+2)%8]) for i in range(8))
    assert r["cycle_nearest_edge_generators"]==8
    assert r["cycle_lie_closure_dimension_mod_101"]==34
    assert r["characteristic_zero_lie_dimension"]==34
    assert r["maximal_dimension_given_two_annihilators_and_trace"]==48


def test_flag_graph_cut_domain_walls_are_not_absolute_chirality():
    r=m.flag_frontier()
    g=m.levi_graph(); flags=nx.line_graph(g)
    assert flags.number_of_nodes()==160 and flags.number_of_edges()==480
    assert nx.edge_connectivity(flags)==6
    assert r["minimum_domain_wall_energy_over_J"]==12
    assert r["ferromagnetic_ground_state_count"]==2


def test_proton_hexality_constraints_and_negative_dimension_five():
    r=m.p6_frontier()
    q=m.Z6
    assert all(sum(q[x] for x in m.OPS[k])%6==0 for k in m.ALLOW)
    assert all(sum(q[x] for x in m.OPS[k])%6!=0 for k in m.VETO)
    assert r["operator_Z6_residues"]["QQQL"]==4
    assert r["operator_Z6_residues"]["UUDE"]==2
    assert r["charge_filter_candidate_counts_N2_to_N6"]=={
        "2":0,"3":0,"4":8,"5":0,"6":24}
    assert all(a%6==0 for a in r["mixed_mod6_necessary_sums"].values())


def test_kinetic_metric_rephasing_invariant_and_rank():
    r=m.flavor_frontier()
    assert r["single_certified_entry_rank_after_invertible_normalization"]==1
    assert r["unitary_left_frame_invariance_error_J"]<1e-12
    assert abs(r["bare_example"]["Jarlskog"]-r["canonically_normalized_example"]["Jarlskog"])>1e-4
    flow=r["toy_1loop_top_beta_fixed_gauge"]
    assert 0<flow["y_final"]<flow["y_initial"]


def test_operational_discrimination_bound_is_conditional():
    r=m.sixth_discrimination()
    assert r["conditional_detection_gap"]=="9/640"
    assert r["sufficient_pre_loss_trials_conservative"]>=r["sufficient_shots_per_known_pair_no_loss"]


def test_aggregate_six_consistency():
    r=m.build()
    assert len(r)==8
    assert r["classical_quantum_transport_cross_tab"]["point_d3_to_d2_time_mean_ratio"]=="220/13"
    assert r["local_constraint_lie_algebra"]["strict_nearest_neighbor_closure"] is False
    assert r["chirality_flag_domain_walls"]["spontaneous_sign_selection"] is False
    assert r["heterotic_proton_hexality_filter"]["scope"].startswith("operator-level")
    assert "no actual Ricci-flat/HYM solution" in r["kinetic_normalization_flavor"]["not_a_physical_prediction"]
