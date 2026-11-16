"""2026-11-16 independently replayed six-plus-front TOE pass controls.

Molien and sparse quartic compilers are replayed from group geometry;
D9/F8/photon producers are replayed from exact arithmetic. SAT timeout
is read from its certificate, with a strict requirement NEVER to infer
UNSAT or realizability from z3's UNKNOWN.
"""
import importlib.util,json,math
from fractions import Fraction as F
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
def run(name):
    file=ROOT/"analysis"/name
    spec=importlib.util.spec_from_file_location(name.removesuffix(".py"),file)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod.run()
@pytest.fixture(scope="module")
def molien():
    return run("toe_20261116_W33_Molien_sympower_branching.py")
@pytest.fixture(scope="module")
def orbitals():
    return run("toe_20261116_W33_quartic_orbital_sparse_compilers.py")
@pytest.fixture(scope="module")
def d9():
    return run("toe_20261116_D9_charged_monopole_harmonics.py")
@pytest.fixture(scope="module")
def f8():
    return run("toe_20261116_F8_nine_MUB_data_hiding.py")
@pytest.fixture(scope="module")
def photon():
    return run("toe_20261116_photonic_weighted_rail_allocation.py")
@pytest.fixture(scope="module")
def sat():
    return json.loads((ROOT/"data"/"toe_20261116_genus6_full_chirotope_SAT.json").read_text())

def test_group_cycle_index_exact(molien):
    assert molien["group_size"]==25920
    assert molien["Schlafli_irrep_dimensions"]==[1,20,6]
    assert sum(x["group_element_count"] for x in molien["class_fingerprints"])==25920

@pytest.mark.parametrize("d,total,six",[
    (0,1,0),(1,1,0),(2,5,0),(3,19,0),(4,164,18),
    (5,1181,192),(6,8721,1700)])
def test_all_equivariant_Hom_characters(molien,d,total,six):
    x=molien["symmetric_power_degrees"][d]
    assert x["Hom_to_27"]==total
    assert x["Hom_to_Schlafli6"]==six
    assert x["Hom_to_27"]==sum(x["Hom_to_"+k]
      for k in ("uniform1","Schlafli20","Schlafli6"))

def test_orbits_and_Molien_independently_agree(molien,orbitals):
    assert orbitals["PSp4_order"]==molien["group_size"]
    assert orbitals["total_output_line_orbits"]==molien["symmetric_power_degrees"][4]["Hom_to_27"]==164
    assert orbitals["output_stabilizer_order"]==960
    assert orbitals["full_sym4_input_dimension"]==math.comb(43,4)
    assert orbitals["orbital_rank_histogram"]=={"1":2,"21":80,"27":82}

def test_sparse_full_rank_quartic_orbital(orbitals):
    o=orbitals["sparsest_full_rank_orbital"]
    assert o["output_rank"]==27
    assert o["support_per_output"]==60
    assert o["gram_eigenvalues_1_20_6"]==[60]*3
    assert orbitals["sparsest_uniform_product_success_exact"]=="243/16000"
    assert orbitals["sparsest_and_best_uniform_exact_27x27_Gram_verified"]

def test_best_product_p_improves_old_channel(orbitals):
    o=orbitals["best_uniform_product_heralding_orbital"]
    assert o["output_rank"]==27
    assert o["support_per_output"]==960
    assert o["gram_eigenvalues_1_20_6"]==[960]*3
    assert o["uniform_identical_fourcopy_heralding_probability"]==pytest.approx(.243)
    assert .243>.198818181818
    assert orbitals["best_uniform_product_success_exact"]=="243/1000"
    assert orbitals["both_preferred_orbitals_are_coisometries"]

def test_genus6_weak_sat_but_no_global_theorem(sat):
    assert sat["nonzero_chirotope_sign_variables"]==715
    assert sat["face_simple_no_crossing_clauses"]==528
    assert sat["Grassmann_Pluecker_uniform_rank4_axioms"]==25740
    assert sat["saved_candidate_violated_face_simplicity_clauses"]==8
    assert sat["saved_candidate_satisfies_all_GP_axioms"]
    assert sat["no_cross_only_SAT_status"]=="sat"
    assert sat["no_cross_and_GP_SAT_status"]=="unknown"
    assert sat["no_global_polyhedron_claim"]

def test_D9_charged_test_scalar_harmonics(d9):
    assert d9["number_of_charge_pairs_checked"]==81
    assert d9["nonzero_flux_charged_probe_has_positive_covariant_gap"]
    assert d9["unit_flux_example_lowest_m2L2"]==15
    assert d9["unit_flux_example_lowest_multiplicity"]==6
    for x in d9["charge_grid_results"]:
        n1,n2=x["charges"]
        assert x["lowest_degeneracy"]==(abs(n1)+1)*(abs(n2)+1)
        assert x["charged_spectrum_is_nonzero_if_any_flux"]==bool(n1 or n2)

def test_D9_is_not_mixed_Einstein_Maxwell_mass(d9):
    assert "not automatically contain" in d9["scope"]

def test_F8_perfect_restricted_data_hiding(f8):
    assert f8["measured_distributions_identical"]
    assert f8["measured_probability_per_outcome_each_MUB"]=="1/64"
    assert f8["unrestricted_optimal_quantum_Helstrom_trace_distance"]=="1"
    assert f8["unrestricted_optimal_binary_discrimination_success"]=="1"
    assert f8["hilbert_schmidt_difference_norm_squared"]=="16/31"
    assert f8["adaptive_single_copy_nine_MUB_transcripts_information_bits"]==0

def test_photon_KKT_nonuniform_shot_optimizer(photon):
    r=photon["illustrative_independently_certified_envelope"]
    assert r["accepted_total_rail_calibration"]==244874
    assert r["aggregate_contrast_calibration_radius"]<=.01
    assert photon["previous_equal16_accepted_rail_calibrations"]==842272
    assert photon["exact_two_rail_occupancy_control"]["accepted_total_rail_calibration"]==105284
    assert photon["uniform_occupancy_with_exact_upper_bounds_control"]["accepted_total_rail_calibration"]==842272
    assert photon["conditional_total_calibration_with_parity"]==539986
    assert photon["conditional_synthetic_99pct_witness_fidelity_lower"]>.9

def test_all_machine_certificates_exist(molien,orbitals,sat,d9,f8,photon):
    for name in [
      "toe_20261116_W33_sym_power_Molien_characters.json",
      "toe_20261116_W33_quartic_164_orbital_sparse_compilers.json",
      "toe_20261116_genus6_full_chirotope_SAT.json",
      "toe_20261116_D9_charged_monopole_KK_probe.json",
      "toe_20261116_F8_nine_MUB_private_bit.json",
      "toe_20261116_photonic_occupancy_weighted_calibration.json",
    ]:
        assert json.loads((ROOT/"data"/name).read_text())["status"]
