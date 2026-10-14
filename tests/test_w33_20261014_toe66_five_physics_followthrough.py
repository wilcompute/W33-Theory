"""TOE66: source-regenerating tests, with explicit physics-layer guardrails."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe66_five_physics_followthrough import (
    certificate,native_adversary,thermal_front,ribbon_front,four_dim_front,cutoff_front)

def test_native_17_edge_integer_witness():
    c=native_adversary()
    assert len(c["high_edge_indices"])==17
    assert c["ray_polynomial_coefficients"]==[0,0,72,46,34,0,0,0,-12]
    assert int(c["exact_negative_integer"])<0
    assert int(c["preceding_exact_positive_integer"])>0
    assert c["new_counterexample_epsilon"]=="244616/1000000"

def test_all_beta_stationarity_is_not_all_beta_minimum():
    c=thermal_front()
    assert "stationary" in c["stationarity_proof"]
    assert c["curvature_cases"][1]["directional_second_difference"]<0
    assert c["curvature_cases"][5]["directional_second_difference"]>0
    assert 1.9<c["numerical_crossover_beta"]<2.1
    assert "not a certified" in c["scope"]

def test_actual_ribbon_permutation_and_doubling():
    c=ribbon_front()
    assert c["ribbon_boundary_lengths"]==[12,14,106,188]
    assert sum(c["ribbon_boundary_lengths"])==320
    assert (c["ribbon_genus"],c["ribbon_boundary_components"],c["doubled_closed_genus"])==(39,4,81)
    assert c["doubled_surface_euler"]==-160

def test_four_dim_index_is_continuum_and_nonnative():
    c=four_dim_front(ribbon_front())
    assert c["betti"]==[1,164,326,164,1]
    assert c["intersection_signature"]==[163,163]
    assert c["hyperbolic_planes"]==163
    assert c["selected_c1_square"]==2
    assert c["twisted_spin_Dirac_index"]==1
    assert "not a native overlap" in c["scope"]

def test_native_interacting_residual_is_not_ground_bound():
    c=cutoff_front()
    assert len(c["cases"])==14
    assert c["d2_L2_to_L3_neutral_shift"]<0
    assert c["d3_L1_to_L2_neutral_shift"]<-.1
    assert any(x["boundary_spectral_residual_upper"]>3 for x in c["cases"])
    assert "too loose" in c["scope"]

def test_all_five_in_one_regression():
    c=certificate()
    assert c["status"]=="PASS_TOE66_FIVE_FRONTS"
    assert set(c)=={"status","front1","front2","front3","front4","front5","physics_scope"}
    assert "remain open" in c["physics_scope"]
