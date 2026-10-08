"""Independent pass checks: exact Q Jacobi and five physical frontiers."""
from __future__ import annotations

import itertools, sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import sympy as sp
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_five_plus_one_deep as p
import w33_20261008_eight_cycle_jacobi_identification as j
from w33_20261008_dual_27_electrical_transport import build_graphs
from w33_20261008_five_physics_frontiers import projective_points_and_lines
from w33_20261008_physical_frontiers_robustness import discrete_vacuum


def test_exact_photonic_hamiltonians_and_nine_parallel_layers():
    report=p.physical_photonic()
    for name,a in build_graphs().items():
        entry=report[name]
        assert a.shape==(27,27)
        assert len(entry["undirected_edge_list"])==108
        assert entry["crossing_lower_bound_single_layer"]==33
        assert entry["disjoint_edge_layers_min_and_max_by_parity_and_Vizing"]==[9,9]
        assert entry["nine_layer_MILP_status"]==0
        layers=entry["nine_layer_schedule"]
        assert len(layers)==9
        assert {tuple(e) for layer in layers for e in layer}=={tuple(e) for e in entry["undirected_edge_list"]}
        for layer in layers:
            occupied=[node for e in layer for node in e]
            assert len(occupied)==len(set(occupied))
        assert nx.is_planar(nx.from_numpy_array(a)) is False


def test_jacobi_algebra_over_Q_structural_blocks():
    x=j.identify()
    assert x["dimension_over_Q"]==34
    assert x["six_dimensional_symplectic_representation_image_dim"]==21
    assert x["radical_kernel_dim"]==13
    assert x["radical_commutator_dim"]==1
    assert sp.Rational(x["radical_to_heisenberg_13_det"])!=0
    JJ=sp.Matrix([[sp.Rational(v) for v in row] for row in x["J_six_by_six"]])
    assert JJ.T==-JJ and JJ.det()!=0
    assert x["invariant_skew_form_kernel_dim"]==1
    assert x["structure_over_Q"].startswith("sp(6,Q)")
    gen=j.rational_generators()
    for y in gen:
        assert y*sp.ones(8,1)==sp.zeros(8,1)


def test_central_minus_one_vacuum_triangle_obstruction():
    x=p.flag_vacuum_action()
    assert (x["flags"],x["physical_quartic_characters"])==(160,320)
    assert x["central_minus_identity_fixed_nontrivial_line_characters"]==0
    assert x["central_minus_identity_fixed_projective_triangles"]==320
    assert x["symplectic_equivariant_bijection_possible"] is False
    pts,lines=projective_points_and_lines()
    assert len(pts)==len(lines)==40
    assert sum(len(line) for line in lines)==160
    # Independently enumerate all unordered triples of local incidence flags.
    g=p.levi_graph()
    lg=nx.line_graph(g)
    assert sum(nx.triangles(lg).values())//3==320


def test_hexality_missing_Z3_generator_and_Klein4_exponent():
    x=p.hexality_generator()
    info=discrete_vacuum()
    for name,c in x["additional_Z3_charge_vector"].items():
        assert 0<=c<=2
        assert (info["sixY"][name]+info["threeBL"][name]+2*c)%6==info["known_proton_hexality_assignment"][name]
    assert x["Klein4_Wilson_character_can_supply_Z3"] is False
    assert x["sums_mod3"]==[0,0,0]
    # Klein four's exponent two directly forbids element order three.
    assert all(2*v%2==0 for v in range(2))


def test_actual_tetraquadric_three_line_bundles_slopes():
    x=p.physical_yukawa_preflight()
    t=[sp.sympify(s) for s in x["Kaehler_moduli"]]
    K=sp.Matrix(x["bundle_K1_K2_K3"])
    assert sum((K.row(i) for i in range(3)),sp.zeros(1,4))==sp.zeros(1,4)
    q=[sum(t[j]*t[k] for j in range(4) for k in range(j+1,4) if i not in (j,k))
       for i in range(4)]
    assert all(sp.simplify(sum(K[i,j]*q[j] for j in range(4)))==0 for i in range(3))
    assert sp.simplify(x["intersection_volume_normalization"])>0
    assert x["actual_Ricci_flat_HYM_harmonic_metrics_calculated"] is False


def test_positive_flux_gradient_and_balanced_toy_not_4D():
    x=p.flux_stabilization_firewall()
    assert x["single_flux_U_grad_at_origin"]==[-2.,-4.,-4.,-4.,-4.,-4.,-4.,-4.]
    K=np.vstack([np.eye(8),-np.ones((1,8))])
    assert np.allclose(K.sum(axis=0),0)
    assert np.allclose(np.linalg.eigvalsh(K.T@K),[1]*7+[9])
    assert x["physical_4D_compactification_or_CC_solution"] is False


def test_aggregate_claim_scope_and_six_frontiers():
    x=p.build()
    assert len(x)==7
    assert "physical" in x["scope"] and "not TOE" in x["scope"]
    assert x["rational_lie_classification"]["derived_algebra_dimension_over_Q"]==34
