"""TOE65: five-physics-front reproducibility + BT1643 correction.

No universal-TOE acceptance is asserted. Heavy interacting eigen-solves are
performed by their standalone producer, while these checks independently
validate its saved certificates and the native rational disorder witness.
"""
from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261013_toe65_surface_topology_correction import certificate as surface
from w33_20261013_toe65_spacetime_admission_gates import certificate as geometry
from w33_20261013_toe65_edge_product_adversary import C,W,SGN,phase_gap
from w33_20261013_toe62_global_flat_flux_proof import trace8

def load(name):
    return json.loads((ROOT/"data"/name).read_text())

def test_bt1643_surface_claim_is_refuted_by_actual_vertex_links():
    c=surface()
    assert c["vertex_links"]["component_sizes"]==[3,3,3,3]
    assert c["two_skeleton_betti_F2"]==[1,81,40]
    assert c["full_tetrahedral_clique_complex_betti_F2"]==[1,81,0,0]
    assert c["incidence_spine"]["cycle_rank"]==81

def test_native_4d_gate_and_nineteen_edge_necessary_bound():
    c=geometry()
    assert c["native_2complex"]["betti_F2"]==[1,3,1304]
    assert c["time_circle_product_H4_F2"]==0
    assert c["two_time_circles_product_betti_F2"][-1]==1304
    assert c["added_edge_necessary_condition"]["at_least_added_edges"]==19
    assert c["non_native_T4_positive_control"]["is_native_W33_index"] is False

def test_thermal_numerical_falsifier_only():
    c=load("w33_20261013_toe65_thermal_continuous_falsifier.json")
    assert len(c["boltzmann_beta_cases"])==5
    assert all(z["smallest_sobol_gap"]>0 for z in c["boltzmann_beta_cases"])
    assert all(z["best_minimizer_gap"]>=-1e-7 for z in c["boltzmann_beta_cases"])
    assert "not" in c["scope"].lower()

def test_native_edge_rational_falsifier_rebuild_exact_integer_polynomial():
    c=load("w33_20261013_toe65_exact_edge_disorder_bracket.json")
    bits=np.array(c["edge_high_bits"],int)
    q=np.array(c["integer_phase_test_direction"],int)
    assert len(bits)==160 and len(W)==238
    high=(C@bits).astype(int)
    A=[sum(int(SGN[i])*int(W[i]@q)**2 for i,k in enumerate(high) if k==j)
       for j in range(9)]
    assert A==c["integer_polynomial_coeff_by_high_edge_count"]
    p=245;d=1000
    integer_value=sum(A[j]*(d+p)**j*(d-p)**(8-j) for j in range(9))
    assert integer_value==c["exact_negative_integer_at_upper_fraction"]<0
    assert c["first_negative_grid_epsilon_rational"]=="245/1000"
    assert c["TOE64_proved_universal_lower_threshold"]<0.149

def test_native_weighted_80_band_eighth_moment_crosscheck():
    c=load("w33_20261013_toe65_exact_edge_disorder_bracket.json")
    pat=np.asarray(c["edge_high_bits"],int)
    q=np.asarray(c["integer_phase_test_direction"],float)
    eps=.245
    w=np.where(pat==1,1+eps,1-eps)
    dx=.015*q/np.linalg.norm(q)
    gap=phase_gap(np.log(w),dx)
    assert gap<0, gap
    pi=np.ones(3)*np.pi
    native_trace_diff=trace8(pi+dx,w)-trace8(pi,w)
    assert abs(native_trace_diff-16*gap)<1e-4,(native_trace_diff,gap)

def test_two_independent_cutoffs_and_variational_monotonicity():
    c=load("w33_20261013_toe65_three_loop_cutoff_grid.json")
    assert len(c["new_runs"])==3
    assert c["Galerkin_variational_nesting_checks"]==12
    assert c["coarse_rigorous_full_patch_lower_bound"]==-13.0
    assert any(row["sectors"]["neutral"]["Fock_boundary_weight"]>.08 for row in c["new_runs"])
    assert all(row["sectors"]["neutral"]["eigensolver_residual"]<1e-5 for row in c["new_runs"])
    assert "DOES NOT certify convergence" in c["scope"]
