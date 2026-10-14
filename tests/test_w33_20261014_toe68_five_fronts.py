"""TOE68 five-front regression: source-regenerating exact + numerical gates."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe68_combinatorial_fronts import disorder_corner,matching_and_bundle
from w33_20261014_toe68_native_octagon_gauge import certificate as gauge
from w33_20261014_toe68_overlap_control import certificate as overlap

def test_native_160_flip_exact_rational_disorder():
    r=disorder_corner()
    assert r["tested_edge_flips"]==160
    assert r["all_flips_strictly_increase_rayleigh"] is True
    assert r["polynomial_coefficient_by_high_count"]==[0,0,72,46,34,0,0,0,-12]
    assert r["rayleigh_numerator"]<0
    assert r["min_positive_flip_numerator"]>0

def test_native_matched_link_zero_modes_are_generically_liftable():
    c=matching_and_bundle()["zero_mode_lifting"]
    assert len(c["matching_40_edge_indices"])==40
    assert abs(c["leading_integer_coefficient"])==1
    assert c["smallest_singular_values_at_pi"]["1.0"]<1e-11
    assert c["smallest_singular_values_at_pi"]["1.001"]>1e-7

def test_native_80_vertex_pairing_fiber_is_automorphism_equivariant():
    c=matching_and_bundle()["symmetry_bundle"]
    assert c["Levi_vertices"]==80
    assert c["opposite_pairings_per_vertex"]==3
    assert c["automorphism_checks"]==400
    assert c["full_group_invariant_single_ribbon_selection"] is False

def test_native_octagon_dynamic_gauge_and_gauss():
    c=gauge()
    assert c["octagon_vertices"]==[0,40,4,44,1,45,13,41]
    assert [x["dimension"] for x in c["sectors"]]==[210,350,490]
    assert all(x["first_excitation_gap"]>.5 for x in c["sectors"])
    assert c["sectors"][2]["flux_boundary_probability"]<1e-7
    assert c["sectors"][2]["Gauss_equalities_checked"]==3920
    assert abs(c["sectors"][1]["ground_energy"]-c["zero_magnetic_control"]["ground_energy"])>.01

def test_genuine_nonnative_4d_overlap_signature_control():
    c=overlap()
    assert c["matrix_dimension"]==324
    assert [x["overlap_index"] for x in c["overlap_runs"]]==[0,0,0,1,-1]
    assert all(x["minimum_hermitian_kernel_gap"]>.3 for x in c["overlap_runs"])
    assert all(x["max_exact_flux_plaquette_deviation"]<1e-12 for x in c["overlap_runs"])
    assert c["mixed_U1_gravity_anomaly"]==0
    assert c["cubic_U1_anomaly"]==0
    assert "non-W33" in c["scope"]
