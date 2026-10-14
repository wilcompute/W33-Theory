"""TOE73: reproducible five-front exact / finite numerical gates."""
import math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe73_exact_fronts import (
    witness_crossing,seven_orbit_star,w33_squared_cw)
from w33_20261014_toe73_gauge_static_dipole import certificate as gauge
from w33_20261014_toe73_eleven_site_ed import certificate as matter

def test_exact_unique_disorder_crossing_descartes_and_rational_bracket():
    c=witness_crossing()
    assert c["descartes_sign_changes_on_positive_r"]==1
    assert c["root_lower_fraction"]=="24461518/100000000"
    assert c["root_upper_fraction"]=="24461519/100000000"
    assert c["exact_lower_sign"]==1 and c["exact_upper_sign"]==-1
    assert "NO global" in c["mathematical_scope"]

def test_seven_orbit_six_bijections_and_exact_truncated_star_bands():
    c=seven_orbit_star()
    assert c["proven_orbits"]==7
    assert c["six_center_target_matching_edges"]==311040
    assert c["adjacency_star_multiplicities"]==[51840,259200,51840]
    assert c["inter_orbit_truncated_star_components"]==51840
    assert "compression" not in c["status"].lower()
    assert "truncated" in c["scope"]

def test_explicit_W33_squared_CW_cells_index_and_spin_ambiguity():
    c=w33_squared_cw()
    assert c["two_surface_product_4D_CW_cell_counts"]==[1,324,26246,324,1]
    assert c["surface_spin_structure_choices_as_power_of_two"]=="2^162"
    assert c["product_spin_structures_as_power_of_two"]=="2^324"
    assert c["graph_inherited_mixed_H2_rank"]==6561
    assert c["inherited_mixed_spin_Dirac_index"]==0
    assert c["dual_meridian_example_spin_Dirac_index"]==1

def test_native_two_loop_static_dipole_Gauss_and_exact_Q_bound():
    c=gauge()
    assert c["fixed_fermion_number"]==5
    assert c["total_background_charge_before_after"]==[5,5]
    assert len(c["dipole_minus_native_ground_energy_at_L1_L2"])==2
    for b in c["backgrounds"].values():
        assert [x["dimension"] for x in b["runs"]]==[4158,11550]
        assert b["omitted_flux_row_bound_L2"]["far_flux_tail_lower_units_2000"]==47200
        assert b["omitted_flux_row_bound_L2"]["Q_lower"]>0

def test_native_11_site_462_fermion_ED_four_flat_Z2_corners():
    c=matter()
    assert c["canonical_Fock_dimension"]==462
    assert len(c["scan"])==4
    assert all(len(s["sectors"])==4 for s in c["scan"])
    assert all(x["max_ground_Ritz_residual"]<1e-7
               for s in c["scan"] for x in s["sectors"])
    assert all(s["ground_energy_spread_over_four_Z2_sectors"]>=0
               for s in c["scan"])
    assert c["independent_Z2_fundamental_chords"]==2
