"""Independent scoped regressions of W33 physical frontier robustness packet."""
from __future__ import annotations
import itertools, math, sys
from fractions import Fraction as F
from pathlib import Path

import networkx as nx
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_physical_frontiers_robustness as m
from w33_20261008_dual_27_electrical_transport import build_graphs
from w33_20261008_six_toe_frontier_followthrough import levi_graph, OPS, Z6


def test_label_free_coherent_gap_and_hermitian_unitarity():
    r=m.coherent_device()
    assert abs(r["time"]-.78)<1e-10
    assert r["probability_gap"]>.26
    assert r["separation_survivors"]==r["disorder_trials"]==32
    assert r["noisy_gap_min"]>.25
    assert 9*r["edge_and_onsite_uniform_error_delta"]<r["guaranteed_operator_norm_epsilon"]
    for a in build_graphs().values():
        eig,v=np.linalg.eigh(a)
        u=(v*np.exp(-1j*r["time"]*eig))@v.T
        assert np.max(abs(u.conj().T@u-np.eye(27)))<1e-12
    # State-preparation/readout relabeling cannot change a maximum.
    perm=np.random.default_rng(44).permutation(27)
    a=build_graphs()["point_far_H27"]
    vals,v=np.linalg.eigh(a[np.ix_(perm,perm)])
    u=(v*np.exp(-1j*r["time"]*vals))@v.T
    assert abs(np.max(np.abs(u[~np.eye(27,dtype=bool)])**2)-r["point_max"])<1e-12


def test_actual_eight_cycle_lie_nonzero_center_and_perfect_derived_mod101():
    r=m.gravity_algebra()
    assert r["generated_dimension_over_Q"]==34
    assert r["derived_ideal_dimension_mod_101"]==34
    assert r["center_dimension_mod_101"]==1
    assert r["generated_dimension_mod_101"]==34


def test_flag_local_triangles_and_new_cycle_rank():
    g=levi_graph()
    fg=nx.line_graph(g)
    assert g.number_of_edges()-g.number_of_nodes()+nx.number_connected_components(g)==81
    assert fg.number_of_edges()-fg.number_of_nodes()+nx.number_connected_components(fg)==321
    assert sum(nx.triangles(fg).values())//3==320
    # Isotropic incidence is bipartite so every line-graph triangle
    # is three original edges sharing exactly one degree-four vertex.
    assert sum(math.comb(d,3) for _,d in g.degree())==320
    assert sum(math.comb(d-1,2) for _,d in g.degree())==240
    assert m.flag_topology()["extra_flag_graph_cycle_rank"]==240


def test_p6_not_subgroup_generated_solely_by_Y_BL():
    info=m.discrete_vacuum()
    assert info["solutions_qP6_equals_a3BL_plus_b6Y_mod6"]==[]
    assert info["sixY"]["Q"]==info["threeBL"]["Q"]==1
    assert info["sixY"]["Uc"]==-4 and info["threeBL"]["Uc"]==-1
    # Exhaustively check just the two obstructing superfields.
    for a,b in itertools.product(range(6),repeat=2):
        assert not ((a+b)%6==0 and (-a-4*b)%6==1)
    for op in ("QQQL","UUDE","QLD","UDD","LLE"):
        assert sum(Z6[x] for x in OPS[op])%6!=0


def test_holomorphic_cubic_needs_three_positive_norms():
    r=m.physical_flavor()
    c=F(1,2)
    assert r["conditional_physical_magnitude_interval_eKhalf_fixed"]==["1/16","1/2"]
    assert min([float(c/(z**1.5)) for z in (1,4)])==1/16
    assert max([float(c/(z**1.5)) for z in (1,4)])==1/2
    assert r["normalization_span_factor"]==8
    assert 0.25<=r["observed_min_singular_ratio"]<=r["observed_max_singular_ratio"]<=1


def test_flux_convex_balance_needs_nine_positive_terms():
    r=m.flux_geometry()
    k=np.array(r["actual_flat_torus_flux_exponent"])
    assert np.all(k>0)
    vectors=np.vstack([np.eye(8),-np.ones((1,8))])
    assert np.array_equal(vectors.sum(axis=0),np.zeros(8))
    hess=vectors.T@vectors
    assert np.allclose(np.linalg.eigvalsh(hess),[1]*7+[9])
    # For at most eight spanning independent exponent vectors in R8,
    # no strictly positive nontrivial linear dependence can sum to zero.
    assert r["minimal_full_dimensional_positive_balance_terms"]==9
    assert r["full_Einstein_solution_or_CC_screening_derived"] is False


def test_certificate_has_all_six_and_scoped_claims():
    out=m.build()
    assert len(out)==7
    assert all(k in out for k in ("coherent_photonic","gravity_lie",
            "chiral_flag_topology","proton_hexality_origin","physical_flavor","flux_vacuum"))
    assert "TOE open" in out["scope"]
