"""TOE70 five-front independent exact and numerical reproductions."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe70_disorder_certified_subcube import certificate as disorder
from w33_20261014_toe70_symmetry_topology import certificate as geometry
from w33_20261014_toe70_interacting_mass import (
    interacting_two_loop,cdw_channel)

def test_160_link_three_flip_rational_certificate():
    c=disorder()
    assert c["three_flip"]["count"]==669920
    assert c["three_flip"]["min_delta"]=="303334787318187810937500"
    assert c["three_flip"]["edges"]==[37,56,57]
    assert c["baseline_negative_integer"]=="-278181245315125293750000"

def test_unique_restricted_17_bit_subcube_global_minimum():
    c=disorder()
    s=c["restricted_subcube"]
    assert s["corners_checked"]==131072
    assert s["unique_global_minimum_at_all_17_high"]
    assert s["number_of_negative_corners"]==1
    assert "NOT" in s["scope"] or "not" in s["scope"]

def test_full_PGSp_orbit_no_stabilizer_and_complementary_obstruction():
    c=geometry()
    assert c["inner_PSp_cover_orbit"]==25920
    assert c["full_PGSp_cover_orbit"]==51840
    assert c["full_cover_stabilizer"]==1
    assert c["outer_similitude_image_in_inner_orbit"] is False
    o=c["complementary_cover_no_go"]
    assert o["distinct_locally_compatible_octagons"]==73
    assert o["native_edges_in_no_compatible_octagon"]==[45]
    assert o["applies_to_full_orbit"]

def test_topology_integer_homology_and_flat_holonomy_killing():
    c=geometry()["attached_twenty_faces"]
    assert c["homology_betti"]==[1,61,0]
    assert c["torsion_in_H1"] is False
    assert c["CW_times_T2_betti"]==[1,63,123,61,0]
    assert c["face_windings_in_three_TOE67_coordinates"]==[
       [0,0,-1],[0,1,0],[1,0,0]]
    assert c["flat_3deck_holonomies_on_X_are_forced_trivial"]

def test_native_two_loop_L3_covariance():
    c=interacting_two_loop()
    assert c["cutoff_sequence"][2]["dimension"]==22638
    assert -3.1899<c["cutoff_sequence"][2]["ground"]<-3.1898
    assert -.049<c["flux_covariance_at_L3"]<-.048
    assert c["flux_boundary_L3"]<2.1e-5
    assert all(x["numerical_ritz_residual"]<1e-7 for x in c["cutoff_sequence"])

def test_interaction_channel_gap_and_unrestricted_selfconsistency_guard():
    c=cdw_channel()
    assert c["singular_zero_values_at_three_pi"]==12
    assert len(c["samples"])==7
    assert all(r["Hartree_mass_m"]>0 and r["uniform_Hartree_energy_gain_vs_m0"]>0
               for r in c["samples"])
    assert abs(c["samples"][0]["Hartree_mass_m"]/c["samples"][0]["V"]-.6)<.01
    assert c["samples"][3]["local_point_line_density_stdev"][0]>.03
    assert "NOT" in c["scope"]
