"""TOE69: exact finite-geometry gates and independent overlap/gauge controls."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_five_fronts import (
    octagons,windings,disorder_two_flip,loop_cover,
    native_gauge_cutoff_bound,overlap_aliasing,free_staggered_mass)
from w33_20261014_toe69_two_octagon_covariance import patch,diagonalize

def test_exact_all_single_and_double_edge_flips():
    ed,adj,cycles=octagons()
    c=disorder_two_flip(cycles,ed,windings(cycles,ed))
    assert c["tested_pair_flips"]==12720
    assert c["smallest_positive_one_flip_integer"]=="52315612734624060937500"
    assert c["smallest_positive_two_flip_integer"]=="337991711991203123437500"
    assert c["min_two_flip_pair"]==[37,56]

def test_exact_twenty_octagon_cover_and_tri_axis_winding():
    ed,adj,cycles=octagons()
    c=loop_cover(cycles,ed,adj,windings(cycles,ed))
    assert c["every_edge_covered_once"]
    assert c["every_vertex_meets_two_octagons"]
    assert len(c["twenty_octagon_edge_lists"])==20
    assert c["intersection_edge_pair_multiplicity_counts"]=={"1":74,"2":3}
    assert c["three_selected_nontrivial_windings"]==[
        [0,0,-1],[0,1,0],[1,0,0]]

def test_native_rotor_conditional_complement_bounds():
    c=native_gauge_cutoff_bound()
    assert c["status"]=="PASS_SCHUR_BLOCK_INEQUALITY_NUMERIC_INPUT"
    assert c["bounds"][0]["conditional_interval_width"]<.061
    assert c["bounds"][1]["conditional_interval_width"]<.023
    assert "not certified" in c["limitation"]

def test_aliasing_vs_admissibility_refinement():
    c=overlap_aliasing()
    assert c["charge9_overlap_index_on_coarse_3pow4_background"]==0
    assert c["first_N_satisfying_that_cutoff"]==14
    assert c["first_N_for_five_charge_bound"]==12
    assert c["continuum_twist_Chern_product_at_charge9"]==81

def test_staggered_mass_gap_and_uniform_flux_scope():
    c=free_staggered_mass()
    assert c["rank_at_3pi"]==28
    assert c["massless_zero_single_particle_modes"]==24
    assert abs(c["trial_mass_gaps"][1]["computed_canonical_fock_gap"]-.4)<1e-9
    assert "parameter" in c["limitation"]

def test_two_loop_patch_wilson_gauss_and_measured_covariance():
    p=patch()
    assert p["support"]==[0,1,2,4,5,6,16,17,52,53,88,89]
    assert len(p["P"])==3 and len(p["chords"])==2
    c=diagonalize(1,p)
    assert c["dimension"]==4158
    assert abs(c["ground"]+3.16047161946957)<1e-6
    assert -.037<c["flux_covariance"][0][1]<-.035
    assert c["numerical_ritz_residual"]<1e-7
