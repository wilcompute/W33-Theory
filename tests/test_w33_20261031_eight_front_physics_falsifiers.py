"""Eight-front falsifier regression using frozen W33 geometry and explicit toy inputs."""
import math, json
import numpy as np
import pytest
from analysis import w33_20261031_eight_front_physics_falsifiers as F
from analysis import w33_20261031_torsion_order5_probe as T

@pytest.fixture(scope="module")
def result():
    data=F.build()
    torsion=T.run()
    assert data["status"]=="PASS_EIGHT_FINITE_TESTBED_FRONTS"
    assert torsion["status"]=="PASS_ORDER5_GRAPH_AUTOMORPHISM_TORSION_JORDAN"
    return data,torsion

def test_modular_torsion_and_graph_cohomology_are_not_same(result):
    a,t=result
    d=a["original_five"]["q9_A5_torsion"]
    assert d["graph_H1_dimension_F5"]==193
    assert d["integral_cokernel_torsion_dimension_F5"]==7
    assert t["nilpotent_image_ranks"]==[7,4,2,0,0,0]
    assert t["fixed_space_dim"]==3
    assert {o:t["other_orders"][o]["torsion_kernel_dimension"] for o in ("2","3","5")}=={"2":4,"3":3,"5":3}

def test_loss_and_noise_on_54d_unitary(result):
    d=result[0]["original_five"]["real_optical_noise"]["orientations"]
    for value in d.values():
        assert value["blocks"]==27
        assert .99<value["unitary_average_gate_fidelity_ideal_vs_noisy"]<1
        assert abs(value["coherent_common_global_phase_fidelity"]-1)<1e-13
        assert value["max_unitarity_defect"]<1e-12
        assert abs(value["assumed_uniform_power_survival_per_five_stages_eta_0p995"]-.995**5)<1e-14

def test_local_clock_chain_cannot_select_geometry(result):
    d=result[0]["original_five"]["local_clock_symmetry_audit"]
    assert d["positive_temperature_unique_symmetric_transfer_state"]
    assert d["one_dimensional_correlation_length_sites"]>0
    assert "S3 wreath S40" in d["larger_than_W33_symmetry"]

def test_antiunitary_chern_partner_and_gaps(result):
    d=result[0]["original_five"]["chiral_index_control"]
    for m in ("-3.0","-1.0","1.0","3.0"):
        entry=d["phase_diagram"][m]
        assert entry["chern"]==-entry["antiunitary_partner_chern"]
        assert entry["sampled_min_band_gap"]>1
    assert d["phase_diagram"]["-1.0"]["chern"]==-1

def test_native_wave_cfl_and_refinement(result):
    d=result[0]["original_five"]["finite_speed_periodic_continuum"]
    assert d["chosen_dt"]<d["analytic_stable_dt_upper_bound"]
    errs=[x["relative_error"] for x in d["refinement"]]
    assert all(errs[i]>errs[i+1] for i in range(len(errs)-1))
    assert errs[-1]<.003

def test_independent_z5_graph_connection_not_torsion(result):
    d=result[0]["additional_three"]["z5_synthetic_flux"]
    assert d["cycle_rank"]==193 and d["incidence_cokernel_torsion_rank"]==7
    assert d["gauge_invariance_error"]<1e-12

def test_single_photon_directed_readout(result):
    d=result[0]["additional_three"]["directional_photon_readout"]
    assert math.isclose(d["total_variation_distance_one_shot"],
                        12/(7*math.sqrt(14)),rel_tol=1e-13)
    assert abs(sum(d["plus_port_probabilities"])-1)<1e-14
    assert abs(sum(d["minus_port_probabilities"])-1)<1e-14
    t=d["optimal_equal_prior_bayes_test"]["photons_to_error_thresholds"]
    assert (t["0.001"]["required_detected_photons"],
            t["0.001"]["required_injected_photons_with_loss_eta0p995_per_stage"])==(23,24)
    assert (t["1e-06"]["required_detected_photons"],
            t["1e-06"]["required_injected_photons_with_loss_eta0p995_per_stage"])==(54,56)

def test_spectator_w33_does_not_create_external_chern(result):
    d=result[0]["additional_three"]["external_chern_w33_spectator"]
    assert d["occupied_bundle_chern"]==-40
    assert d["partner_bundle_chern"]==40
    assert not d["topological_charge_from_W33_alone"]

def test_freeze_matches_calculated_key_results(result):
    saved=json.loads(F.OUT.read_text())
    assert saved["status"]==result[0]["status"]
    assert saved["additional_three"]["directional_photon_readout"]["exact_distance"]=="12/(7 sqrt(14))"
    t=json.loads((F.ROOT/"data/w33_20261031_torsion_order5_probe.json").read_text())
    assert t["nilpotent_image_ranks"]==result[1]["nilpotent_image_ranks"]
