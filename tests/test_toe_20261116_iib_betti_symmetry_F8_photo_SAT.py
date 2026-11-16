"""2026-11-16 independent controls across IIB topology, W33 ancillas,
four-photon passive-only no-go, genus6 SAT, F8 basis and photon pilot.

The local parallel author's IIB files are *not* imported or modified.
This suite is fully reproducible from committed repo sources and the
newly named producers. Genus solver certificate is replayed without
rerunning a resource-budget-dependent 40s SAT solve.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,math
import pytest
ROOT=Path(__file__).resolve().parents[1]
def module(filename):
    p=ROOT/"analysis"/filename
    spec=importlib.util.spec_from_file_location(filename.removesuffix(".py"),p)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj)
    return obj

@pytest.fixture(scope="module")
def topology():
    return module("toe_20261116_iib_circle_gysin_betti_BF_audit.py").run()
@pytest.fixture(scope="module")
def privatebit():
    return module("toe_20261116_F8_minimal_new_basis_private_bit.py").run()
@pytest.fixture(scope="module")
def photonresource():
    return module("toe_20261116_W33_quartic_resource_onebody_no_go.py").run()
@pytest.fixture(scope="module")
def photpilot():
    return module("toe_20261116_photonic_pilot_CP_confidence.py").run()
@pytest.fixture(scope="module")
def ancillary():
    return module("toe_20261116_W33_ancilla_nontrivial_branching.py").run()
@pytest.fixture(scope="module")
def genus():
    return json.loads((ROOT/"data"/"toe_20261116_genus6_cadical_chirotope_local_sat.json").read_text())

def test_dual_gysin_has_betti_three(topology):
    assert topology["all_nontrivial_c1_deRham_betti"]==[1,0,1,1,0,1]
    assert topology["baryonic_Betti_U1"].startswith("Exactly one free H3")
    assert topology["massless_vector_sector_warning"].startswith("The 7 light")

def test_c1_gcd_torsion_and_spin(topology):
    mod=module("toe_20261116_iib_circle_gysin_betti_BF_audit.py")
    for p in range(-4,5):
        for q in range(-4,5):
            if p==q==0:continue
            x=mod.topology(p,q)
            g=math.gcd(abs(p),abs(q))
            assert x["gcd"]==g
            assert x["pi1"]=="Z_"+str(g)
            assert x["cohomology"]["H4"]=="Z_"+str(g)
            assert x["independent_spin_structures"]==(2 if g%2==0 else 1)

def test_T11_flux_quotient_and_central_charge(topology):
    assert topology["equal_flux_Y"]=="T^{1,1}/Z_N as an S1 bundle over S2xS2 of Chern numbers (N,N)"
    assert topology["equal_flux_leading_a_c"]=="(27/64)*N*N0^2"
    cases=topology["case_tables"]
    assert cases[0]["gcd"]==1 and cases[1]["gcd"]==2

def test_BF_torus_momentum_band(topology):
    assert topology["BF_band_open"]==[0,12]
    assert topology["minimizer_lambda"]=="15/4"
    assert topology["minimum_m2L2"]=="-25/4"
    for x in topology["square_torus_samples"]:
        assert x["BF_violation_from_shortest_lattice_mode"]==(x["N"]/x["N0"]>math.pi/4)

def test_supersymmetry_mode_scope(topology):
    assert "Spin structures existing" in topology["spinor_parallel_susy_warning"]
    assert "not disproven" in topology["IIB_supergravity_scope"]

def test_F8_hidden_basis_eigen_support(privatebit):
    assert privatebit["extension_maximal_commuting_group_size"]==64
    assert privatebit["new_single_64_outcome_basis_achieves_perfect_discrimination"]
    assert (privatebit["code_supported_basis_outcomes"],privatebit["complement_supported_basis_outcomes"])==(2,62)

@pytest.mark.parametrize("k,p",[ (0,"1/2"),(1,"47/62"),(2,"55/62"),(3,"59/62"),(4,"61/62"),(5,"1") ])
def test_F8_k_syndromes_optimal_success(privatebit,k,p):
    x=privatebit["syndrome_success_by_k"][k]
    assert x["number_of_independent_stabilizer_generators"]==k
    assert x["equal_prior_optimal_success_given_full_k_syndrome"]==p
    assert x["perfect_discrimination"]==(k==5)

def test_F8_does_not_claim_minimal_arbitrary_POVM(privatebit):
    assert "not a universal lower bound" in privatebit["scope"]

def test_sparse60_onebody_exact_I40_over40(photonresource):
    a=photonresource["cases"]["sparse60"]
    assert a["onebody_rank"]==40
    assert a["onebody_is_maximally_mixed"]
    assert a["onebody_purity"]=="1/40"
    assert a["onebody_min_eigenvalue"]==pytest.approx(.025)
    assert a["onebody_integer_offdiagonal_nonzero_pairs"]==0

def test_compiler960_onebody_not_passive_from_four_modes(photonresource):
    a=photonresource["cases"]["best_uniform960"]
    assert a["onebody_rank"]==40
    assert a["onebody_purity"]=="221/7680"
    assert a["onebody_min_eigenvalue"]>.006
    assert a["onebody_max_eigenvalue"]==pytest.approx(.05625)
    assert "heralded optical preparation" in photonresource["limits"]

def test_ancilla_labeled_copies_through_three_still_no_six(ancillary):
    vals=ancillary["modules"]["V40_tensor_power_labeled"]
    assert [x["Hom_to_1_20_6"] for x in vals[:5]]==[
       [1,0,0],[1,0,0],[3,2,0],[18,62,0],[226,2154,348]]
    assert all(not x["all_27_target_sectors_present"] for x in vals[:4])
    assert vals[4]["all_27_target_sectors_present"]

def test_ancilla_20_dimension_allows_two_symmetric_W33(ancillary):
    a=ancillary["modules"]["Schlafli20"]
    assert a[2]["Hom_to_1_20_6"]==[2,24,3]
    assert a[2]["full_output_permutation_representation_possible"]

def test_exterior_square_no_output_target(ancillary):
    assert ancillary["modules"]["V40_antisymmetric2"]["Hom_to_1_20_6"]==[0,0,0]

def test_neutral_ancilla_cannot_override_min_degree(ancillary):
    assert ancillary["trivial_ancilla_does_not_change_sector_presence"]
    assert ancillary["modules"]["trivial1"][3]["Hom_to_1_20_6"][2]==0
    assert ancillary["modules"]["trivial1"][4]["Hom_to_1_20_6"][2]>0

def test_fast_genus_CNF_not_false_certificate(genus):
    assert genus["rank4_chirotope_variables"]==715
    assert genus["face_local_no_cross_clauses"]==528
    assert genus["grassmann_pluecker_axioms"]==25740
    assert genus["cnf_variables"]==81103
    assert genus["cnf_clauses"]==373560
    assert genus["solver_result"] in ("unknown","sat","unsat")
    if genus["solver_result"]=="unsat":
        assert genus.get("formal_proof_log_exported") is False
    assert "does not ensure no global face intersections" in genus["scope"]

def test_photon_fixed_pilot_certification_budget(photpilot):
    assert photpilot["pilot_sample_size_prespecified"]==50000
    assert photpilot["synthetic_not_hardware"]
    assert sum(photpilot["pilot_multinomial_counts"])==50000
    assert all(x["synthetic_true_value_below_upper"] for x in photpilot["pilot_rail_checks"])
    assert sum(photpilot["joint_failure_budget"].values())==pytest.approx(.01)

def test_photon_pilot_net_cost_and_conditional_fidelity(photpilot):
    assert photpilot["total_synthetic_99pct_accepted_shots_including_pilot"]==568023
    assert photpilot["net_fraction_saved_including_pilot"]>.49
    assert photpilot["synthetic_witness_99pct_lower_bound"]>.91
    assert photpilot["pilot_upper_envelope_weighted_optimizer"]["aggregate_contrast_calibration_radius"]<=.01

def test_all_seven_producer_certificates_present(topology,privatebit,photonresource,photpilot,ancillary,genus):
    for x in (
        "toe_20261116_iib_circle_gysin_betti_BF_audit.json",
        "toe_20261116_F8_minimum_new_stabilizer_syndrome.json",
        "toe_20261116_W33_quartic_60_960_onebody_resource.json",
        "toe_20261116_photonic_pilot_certified_envelope_99pct.json",
        "toe_20261116_W33_ancilla_irrep_Schlafli_antisym2.json",
        "toe_20261116_genus6_cadical_chirotope_local_sat.json"
    ):
        y=json.loads((ROOT/"data"/x).read_text())
        assert y["status"]


@pytest.fixture(scope="module")
def winding():
    return module("toe_20261116_iib_weakcurvature_winding_control.py").run()

def test_independent_iib_string_and_fiber_scale(winding):
    assert winding["IIB_AdS_radius_string4"]=="(27*pi/4)*gs*N*N0 = L^4/alpha'^2"
    assert winding["IIB_fiber_radius_string4"]=="(4*pi/3)*gs*N0/N^3 = Rf^4/alpha'^2"
    assert len(winding["examples"])==9
    assert winding["winding_BF_safe_necessary_and_sufficient_in_this_sector"].startswith("Im(tau)")

def test_no_conflation_weak_coupling_and_square_M_torus(winding):
    assert winding["tau_axiodilaton"].startswith("tau=C0+i/gs")
    cases=winding["examples"]
    assert any(x["winding_BF_violation_in_this_channel"] for x in cases)
    assert any(not x["winding_BF_violation_in_this_channel"] for x in cases)
    assert any(x["large_AdS_radius_criterion_Ls_ge10"] and
               not x["fiber_radius_ge_string_length"] for x in cases)


def test_quotient_spinor_lifts_are_not_circle_invariant(topology):
    lifts=topology["equal_flux_quotient_Killing_spinor_lifts"]
    assert len(lifts)==12
    assert [(v["quotient_N"],v["preserving_lifts"]) for v in lifts if v["preserving_lifts"]]==[(1,["0"]),(2,["1/2"])]
    assert topology["local_conifold_spinor_fiber_charges_in_std_4pi_coordinate"]==["1/2","-1/2"]
    assert "Circle-invariant supergravity T-duality may lose" in topology["IIB_supergravity_vs_M11_supersymmetry_warning"]
