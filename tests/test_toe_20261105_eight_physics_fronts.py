"""Eight physics-first TOE fronts: executable tests; no global conftest.

No certificate-only tests: every physics model is recomputed in module fixture.
"""
from __future__ import annotations
import importlib,json,math,sys
from pathlib import Path
import pytest,numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
FILES={
 "rg":"toe_20261105_twoloop_proton_consistency",
 "causal":"toe_20261105_causal_growth_without_background",
 "matter":"toe_20261105_multiparticle_local_scattering",
 "seesaw":"toe_20261105_anomalyfree_bl_seesaw_degeneracy",
 "speed":"toe_20261105_universal_speed_radiative_guard",
 "extra":"toe_20261105_three_orthogonal_quantum_gravity_controls",
 "mix":"toe_20261105_crossfront_bl_kinetic_mixing"}
@pytest.fixture(scope="module")
def r():
    return {k:importlib.import_module(v).main() for k,v in FILES.items()}

def test_rg_top_two_loop_coefficients(r):
    x=r["rg"]
    assert x["SM_B"]==[[3.98,2.7,8.8],[.9,35/6,12],[1.1,4.5,-26]]
    assert x["SM_top_yukawa_gauge_d"]==[1.7,1.5,2.]

@pytest.mark.parametrize("name,scale",[
  ("Dirac_vectorlike_quark_doublet_3_2_1_6",2.118910322756e7),
  ("Majorana_weak_adjoint_1_3_0",8.406127667399e7)])
def test_rg_two_loop_fitted_mass(r,name,scale):
    t=r["rg"]["scans"][name]
    assert t["two_loop_gauge_with_top_yukawa_one_loop"]["threshold_mass_GeV"]==pytest.approx(scale,rel=2e-7)
    assert t["two_loop_gauge_with_top_yukawa_one_loop"]["max_two_coupling_mismatch"]<1e-8

def test_rg_threshold_dramatic_shift(r):
    for row in r["rg"]["scans"].values():
        lo=row["one_loop_recomputed"]["threshold_mass_GeV"]
        tw=row["two_loop_gauge_with_top_yukawa_one_loop"]["threshold_mass_GeV"]
        assert tw/lo>5

def test_proton_decay_not_pure_maths_exclusion(r):
    for row in r["rg"]["scans"].values():
        x=row["two_loop_gauge_with_top_yukawa_one_loop"]
        assert x["minimum_reference_K_years_for_p_to_e_pi0_limit"]>1e37
        assert "K unspecified" in x["proton_decay_assumptions"]

def test_sm_two_loop_still_does_not_meet(r):
    assert all(row["max_spread"]>3 for row in r["rg"]["SM_no_new_particles_control"])

def test_causal_growth_intrinsic_not_embedded(r):
    assert len(r["causal"]["samples"])==18
    assert all(x["transitively_related_pairs"]>=x["direct_bonds"] for x in r["causal"]["samples"])

@pytest.mark.parametrize("p,bounds",[(.025,(1.9,2.4)),(.065,(1.9,2.2)),(.15,(1.3,1.7))])
def test_causal_grown_dimension_does_not_select_4(r,p,bounds):
    key=f"n320_p{p}"
    d=r["causal"]["family_summary"][key]["median_across_replicates"]
    assert bounds[0]<d<bounds[1]
    assert abs(d-4)>1

def test_causal_rare_intervals_from_slow_growth(r):
    slow=[x for x in r["causal"]["samples"] if x["n"]==160 and x["p"]==.025]
    assert sum(x["eligible_intervals"] for x in slow)<5

def test_one_boson_no_double_click(r):
    assert r["matter"]["two_site"]["exact_one_excitation_double_coincidence"]==0
    assert all(x["both_ends_probability"]==0 for x in r["matter"]["four_site"][0]["records"])

def test_hong_ou_mandel_two_particles(r):
    x=r["matter"]["two_site"]["two_site_two_excitation_results"][0]
    assert x["local_coincidence_probability"]<1e-25
    assert x["mode_entanglement_negativity"]==pytest.approx(.5,abs=1e-12)

@pytest.mark.parametrize("idx,expected",[(1,.015532),(2,.227187),(3,.865629),(4,.962461)])
def test_interaction_affects_two_particle_coincidence(r,idx,expected):
    z=r["matter"]["two_site"]["two_site_two_excitation_results"][idx]
    assert z["local_coincidence_probability"]==pytest.approx(expected,rel=5e-5)

def test_distant_two_detector_coincidences_rise(r):
    a=r["matter"]["four_site"][1]["records"]
    assert a[0]["both_ends_probability"]==0
    assert a[2]["both_ends_probability"]>a[1]["both_ends_probability"]>0

def test_anomaly_free_gauged_bl_spectrum(r):
    a=r["seesaw"]
    assert all(v=="0" for v in a["per_generation_chiral_anomalies"].values())
    assert a["without_Nc_anomalies"]["BL_grav"]=="-1"
    assert a["without_Nc_anomalies"]["BL_cubic"]=="-1"
    assert a["scalar_S_BL_charge"]==-2

def test_seesaw_rank2_two_measured_splittings_fit_not_predicted(r):
    a=r["seesaw"]["seesaw"]
    rows=a["examples"]
    assert len(rows)==4
    assert all(row["Dirac_Yukawa_rank"]==2 for row in rows)
    assert all(row["PMNS_reconstruction_error_GeV"]<1e-24 for row in rows)
    assert rows[0]["light_masses_eV"]==pytest.approx([0,.0086139421869432,.0501497756724793])

def test_seesaw_continuous_high_energy_degeneracy(r):
    a=r["seesaw"]["seesaw"]["examples"]
    assert abs(a[0]["Yukawa_Frobenius_norm"]-a[1]["Yukawa_Frobenius_norm"])>.006
    assert a[1]["Yukawa_Frobenius_norm"]==pytest.approx(a[3]["Yukawa_Frobenius_norm"],abs=1e-12)
    assert a[1]["heavy_N_masses_GeV"][0]!=a[3]["heavy_N_masses_GeV"][0]

def test_massless_branches_change_not_unify(r):
    a=r["speed"]["normal_mode_sweep"]
    assert [x["massless_mode_count"] for x in a]==[2,1,1,1]
    assert all(z["acoustic_effective_speed"]==pytest.approx(math.sqrt(1.22),rel=1e-12) for z in a[1:])
    assert all(z["optical_gap"]>0 for z in a[1:])

def test_phi4_one_loop_tadpole_changes_mass_not_speed(r):
    a=r["speed"]["one_loop_quartic_tadpole_sweep"]
    assert all(tuple(x["kinetic_counterterms_at_one_loop"])==(0,0) for x in a)
    assert all(x["velocity_difference_after_one_loop_in_tadpole_approx"]==pytest.approx(.2) for x in a)
    assert a[0]["mass_counterterm_A"]<a[1]["mass_counterterm_A"]<a[2]["mass_counterterm_A"]

def test_five_chiral_fermions_anomaly_free_but_landaubeta_positive(r):
    a=r["extra"]["chiral_landau"]
    assert a["chiral_charge_spectrum"]==[-9,-5,-1,7,8]
    assert a["one_loop_beta_coefficient_b"]==pytest.approx(440/3)
    assert a["anomaly_free"] and a["chiral_no_opposite_pairs"]

def test_landau_coupling_dependence(r):
    s=r["extra"]["chiral_landau"]["illustrative_couplings"]
    assert s[0]["one_loop_Landau_pole_GeV"]>1e19
    assert s[-1]["one_loop_Landau_pole_GeV"]<1e9

def test_clock_redshift_can_entangle_paths(r):
    s=r["extra"]["proper_time_quantum_clock"]["rows"]
    assert s[3]["clock_Ramsey_visibility"]<1e-12
    assert s[3]["internal_clock_path_entanglement_ebits"]==pytest.approx(1,abs=1e-12)
    assert s[-1]["internal_clock_path_entanglement_ebits"]<1e-12

def test_local_vacuum_entanglement_gapped_versus_critical(r):
    s=r["extra"]["vacuum_entanglement_area_critical"]["records"]
    assert .28<s["0.001"]["finite_chord_log_slope"]<.34
    assert 0<s["0.5"]["finite_chord_log_slope"]<.001
    assert s["0.001"]["finite_chord_log_slope"]>300*s["0.5"]["finite_chord_log_slope"]

def test_each_fresh_run_wrote_its_certificate(r):
    names={
      "rg":"toe_20261105_two_loop_threshold_proton_guard.json",
      "causal":"toe_20261105_causal_growth_no_embedded_dimension.json",
      "matter":"toe_20261105_multiparticle_scattering_locality.json",
      "seesaw":"toe_20261105_bl_gauge_seesaw_flavour_degeneracy.json",
      "speed":"toe_20261105_universal_lightcone_radiative_guard.json",
      "extra":"toe_20261105_three_independent_toe_controls.json",
      "mix":"toe_20261105_bl_sm_threshold_kinetic_mixing_no_go.json"}
    for key,name in names.items():
        loaded=json.loads((ROOT/"data"/name).read_text(encoding="utf8"))
        assert loaded==json.loads(json.dumps(r[key]))

def test_gauged_BL_combined_spectrum_anomaly_free_but_mixes(r):
    x=r["mix"]
    assert all(s=="0" for s in x["all_local_polynomial_U1_gauge_anomalies"].values())
    assert x["trace_Y_BL_SM_three_families"]=="8"
    assert x["trace_Y_BL_added_vectorlike_pair"]=="2/3"
    assert x["mixed_beta_b_Y_BL_with_vectorlike"]=="52/9"
    assert x["one_loop_BL_diagonal_b_with_vectorlike_and_scalar"]=="116/9"

def test_BL_kinetic_mixing_not_radiatively_stable_zero(r):
    x=r["mix"]
    assert x["nonzero_radiative_kinetic_mixing"]
    assert .02<x["loop_generated_kinetic_mixing_estimate"]<.04
    assert "radiatively closed" in x["consequence"]
