"""Five continuation fronts plus three independent numerical falsifiers.

Runs producer algorithms, does not treat JSON certificates as primary evidence.
To avoid huge repository-wide collection hooks:
python -m pytest -q --noconftest tests/test_toe_20261105_next5_plus3.py
"""
import importlib.util
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
def run(path):
    name=path.replace(".py","")
    spec=importlib.util.spec_from_file_location(name,ROOT/"analysis"/path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.main()

@pytest.fixture(scope="module")
def d():
    return {
        "gauge":run("toe_20261105_s3_nonabelian_matter_gauge.py"),
        "ward":run("toe_20261105_4d_ward_locality_cfl.py"),
        "three":run("toe_20261105_photon_memory_chirality.py"),
        "orthogonal":run("toe_20261105_three_orthogonal_physics_falsifiers.py")
    }

def test_nonabelian_exact_gauge_projector_and_dynamics(d):
    r=d["gauge"]
    assert r["physical_gauge_invariant_dimension"]==27
    assert r["raw_hilbert_dimension"]==144
    assert r["exact_projector_and_Gauss_constraints"]
    assert r["electric_magnetic_commutator_frobenius"]>10
    assert all(x["max_Gauss_invariance_error"]<1e-11 for x in r["scans"])

def test_nonabelian_27_not_claimed_isomorphic_to_history(d):
    r=d["gauge"]
    assert "no canonical H27/W33 intertwiner" in r["nonidentification"]

def test_4d_ward_and_cfl_separate_guards(d):
    r=d["ward"]
    assert r["symmetric_metric_components"]==10
    assert r["physical_operator_rank"]==6
    assert r["discrete_gauge_null_directions"]==4
    assert r["stable_zone_corner_argument"]>=-1
    assert r["unstable_zone_corner_argument"] < -1
    assert all(x["max_Ward_divergence_residual"]<1e-8 for x in r["records"])

def test_lattice_locality_4d_is_supplied_not_emerged(d):
    r=d["ward"]
    assert abs(r["records"][-1]["heat_spectral_dimension_t002"]-4)<.05
    assert "not derived from W33" in r["conclusion"]

def test_native_witting_compiled_helstrom_advantage(d):
    r=d["three"]["results"]["adaptive_Witting_photonic"]
    assert len(r["records"])==12
    assert all(row["Helstrom_four_port_success"]>row["native_Witting40_success"]
               for row in r["records"])
    assert all(row["two_mode_givens_gates"]<=6 for row in r["records"])

def test_photonic_nonorthogonal_case_exists(d):
    r=d["three"]["results"]["adaptive_Witting_photonic"]
    x=[row for row in r["records"] if row["type"]=="nonorthogonal"]
    assert len(x)==6 and all(z["Witting_total_variation"]>0 for z in x)

def test_memory_reset_entanglement_and_heralding_guard(d):
    r=d["three"]["results"]["trusted_memory"]
    assert abs(r["coherent_reset_fidelity"]-1)<1e-11
    assert abs(r["classical_dephased_memory_fidelity"]-1/3)<1e-11
    assert r["state_dependent_loss_false_witness_conditional_fidelity"]>.8
    assert any(z["binomial_power"]>.99 for z in r["binomial_records"])

def test_flavour_anomaly_yukawa_ambiguity(d):
    r=d["three"]["results"]["chirality_flavor"]
    assert r["integer_U1_charge_parameter_choices"]==48
    assert r["all_six_anomalies_vanish"] and r["all_four_yukawa_monomials_allowed"]
    assert max(r["topological_open_SSH_smallest_abs_modes"])<.001
    assert min(r["trivial_open_SSH_smallest_abs_modes"])>.4

def test_isospectral_different_local_geometry(d):
    r=d["orthogonal"]["results"]["isospectral_geometry"]
    assert not r["isomorphic"]
    assert r["first_degree_sequence"]!=r["second_degree_sequence"]
    assert all(x["sorted_local_heat_diagonal_distance"]>1e-5 for x in r["records"])

def test_z3_critical_gap_scaling(d):
    r=d["orthogonal"]["results"]["z3_criticality"]["records"]
    assert len(r)==5
    assert abs(r[-1]["critical_n_times_gap"]-r[0]["critical_n_times_gap"])<.1
    assert abs(r[-1]["disordered_gap"]-r[-3]["disordered_gap"])<.1

def test_stationary_entropy_does_not_set_current(d):
    r=d["orthogonal"]["results"]["entropy_arrow"]
    assert r["equilibrium"]["entropy_production"]==0
    assert r["clockwise"]["entropy_production"]>.6
    assert r["clockwise"]["clockwise_net_current"]==-r["counterclockwise"]["clockwise_net_current"]
    assert r["clockwise"]["stationary_shannon_entropy"]==r["equilibrium"]["stationary_shannon_entropy"]
