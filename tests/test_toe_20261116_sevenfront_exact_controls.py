"""Independent 2026-11-16 seven-front exact/conditional research suite.

Uses generated machine-readable certificates AND re-runs all producer
identities. No SciPy, numpy, networkx or random solver required.
"""
import importlib.util,math,json
from fractions import Fraction as F
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
FILES={
 "sym":"toe_20261116_W33_symmetry_minimal_fourcopy.py",
 "ent":"toe_20261116_W33_E6_perfect_source_1RDM.py",
 "steer":"toe_20261116_W33_E6_target_steering.py",
 "genus":"toe_20261116_genus6_matroid_crossing_signs.py",
 "d9":"toe_20261116_D9_monopole_global_group.py",
 "f8":"toe_20261116_F8_global_mixed_purity_zero_interval.py",
 "phot":"toe_20261116_photonic_grid_shot_optimizer.py"
}
@pytest.fixture(scope="module")
def results():
    out={}
    for name,src in FILES.items():
        spec=importlib.util.spec_from_file_location(name,ROOT/"analysis"/src)
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        out[name]=mod.run()
    return out

def test_reproduced_all_seven_fronts(results):
    assert len(results)==7
    assert all(x["status"] for x in results.values())

def test_min_degree_group_is_exact_PSp43(results):
    a=results["sym"]
    assert a["group_order"]==25920 and a["group_generators"]==5
    assert (a["W33_points"],a["W33_induced_K44_octets"],a["E6_cubic_lines"])==(40,45,27)
    assert a["minimum_copy_number_with_full_27_output"]==4
    assert a["zero_six_dimensional_sector_for_all_orbit_matrices"]

@pytest.mark.parametrize("degree,orbits,dimension,rank",[
    (1,1,40,1),(2,5,820,21),(3,19,11480,21)])
def test_every_equivariant_orbit_kills_dark_six(results,degree,orbits,dimension,rank):
    r=results["sym"]["degrees_leq_three"][degree-1]
    assert r["degree"]==degree
    assert r["orbit_count"]==orbits
    assert r["domain_dimension"]==dimension
    assert r["max_orbital_rank"]==rank
    assert len(r["orbit_Gram_certificates"])==orbits
    assert sum(o["orbit_size"] for o in r["orbit_Gram_certificates"])==27*dimension
    for o in r["orbit_Gram_certificates"]:
        d,a,b=o["gram_diagonal"],o["gram_adjacent"],o["gram_nonadjacent"]
        assert d-5*a+4*b==0
        assert o["eigenvalues_1_20_6"][2]==0
        assert o["rank"]<=21

def test_existing_quartic_witness_full_rank(results):
    assert results["sym"]["quartic_witness_rank"]==27
    assert results["sym"]["minimum_copy_number_with_full_27_output"]==4

def test_entanglement_exact_1RDM_eigen_spectrum(results):
    a=results["ent"]
    assert a["one_body_correlation_diagonal_adj_nonadj"]==[7128,1836,2160]
    assert a["one_body_correlation_integer_denom"]==4*71280
    ev=[F(x["numerator"],x["denominator"]) for x in a["one_body_eigenvalues_by_multiplicity"]]
    assert ev==[F(27,88),F(1,66),F(29,1320)]
    assert ev[0]+24*ev[1]+15*ev[2]==1

def test_entanglement_product_preparation_bound(results):
    a=results["ent"]
    assert a["one_body_purity"]=={"numerator":194,"denominator":1815}
    assert a["one_body_rank"]==40
    assert a["max_identical_fourfold_product_source_fidelity_upper"]=={"numerator":27,"denominator":88}
    assert a["uniform_coherent_fourfold_product_source_fidelity_exact"]=={"numerator":2187,"denominator":11000}

def test_all_27_target_states_reachable_exact(results):
    a=results["steer"]
    assert a["inverse_verified_by_27x27_rational_matrix_multiplication"]
    assert a["worst_target_success_lower_rational"]=="28/55"
    assert a["dark6_target_success"]=="13/22"
    assert a["single_cubic_line_basis_target_success"]=="91/170"
    assert a["uniform_target_success"]=="1"

def test_genus6_528_sign_constraints_are_coordinate_free(results):
    a=results["genus"]
    assert a["raw_3x3_normal_minors"]==220
    assert a["raw_4x4_plane_minors"]==495
    assert a["zero_minor_count"]==0
    assert a["SAT_ready_necessary_no_crossing_constraints"]==528
    assert len(a["crossing_constraints"])==8
    assert a["exact_crossings_total"]==8
    assert len(a["all_528_predicate_cases_sha256"])==64

def test_genus6_no_nonrealizability_claim(results):
    assert "No 59-map no-go" in results["genus"]["scope"]

def test_D9_global_gauge_parity_eighty_one_cases(results):
    a=results["d9"]
    assert a["integer_charge_grid_checked"]==81
    for row in a["detailed_cases"]:
        n1,n2=row["charges"]
        assert row["center_action_SU2xSU2"]==[(-1)**n1,(-1)**n2]
        assert len(row["kernel_Z2xZ2_lifts"])==4
        assert row["both_SO3_factors_lift_separately"]==((n1%2==0) and (n2%2==0))
    assert a["nontrivial_example"]==[1,2]

def test_D9_quantization_not_full_KK(results):
    assert "not spontaneous E6 enhancement" in results["d9"]["physical_scope"]

def test_F8_global_mixed_certainty_zero_interval(results):
    a=results["f8"]
    assert a["symplectically_isotropic_rank"]==5
    assert a["uncovered_subgroup_nonidentity_count"]==31
    assert a["covered_Pauli_observables"]==567
    assert a["centralizer_size"]==128
    assert a["logical_coset_covered_counts"]==[3,3,3]
    assert a["global_mixed_state_exact_min_zero_purity_interval"]==["1/64","1/2"]
    assert all(x["covered_certainty_exact"]==0 for x in a["exact_sample_families"])

def test_F8_above_half_only_upper_bounds(results):
    a=results["f8"]
    assert .85<a["two_explicit_upper_family_numeric_cross_purity"]<.86
    assert "No claim of maximal" in a["scope"]

def test_photon_curvature_optimized_resource(results):
    a=results["phot"]
    c=a["optimal_separate_regularities"]["curvature"]
    assert c["calibration_anchors"]==3
    assert c["accepted_total_calibration_shots"]==444728
    assert c["conditional_99pct_lower_witness_fidelity"]>.9
    assert c["verified_rail_union_Hoeffding_failure_bound"]<=.0025

def test_photon_Lipschitz_resource(results):
    a=results["phot"]
    c=a["optimal_separate_regularities"]["Lipschitz"]
    assert c["calibration_anchors"]==5
    assert c["accepted_total_calibration_shots"]==705192
    assert c["conditional_99pct_lower_witness_fidelity"]>.9
    assert a["actual_hardware_calibration_shots_collected"]==0

def test_all_seven_machine_certificates_saved(results):
    names=[
     "toe_20261116_W33_symmetry_minimal_fourcopy.json",
     "toe_20261116_W33_E6_perfect_source_entanglement.json",
     "toe_20261116_W33_E6_universal_target_steering.json",
     "toe_20261116_genus6_oriented_matroid_face_crossing_signs.json",
     "toe_20261116_D9_monopole_global_gauge_parity.json",
     "toe_20261116_F8_exact_mixed_purity_zero_interval.json",
     "toe_20261116_photonic_time_grid_calibration_optimizer.json"
    ]
    for name in names:
        r=json.loads((ROOT/"data"/name).read_text())
        assert r["status"]
