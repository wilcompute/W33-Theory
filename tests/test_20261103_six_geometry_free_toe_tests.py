"""Six independent, previously researched November 3 TOE extension falsifiers.
Focused pytest replays every producer and validates the machine certificates.
"""
from pathlib import Path
import subprocess,sys,json,math
import pytest
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS={
    "pachner":("2026_11_03_local_pachner_gauss_bonnet","2026_11_03_pachner_sphere_dimension_obstruction"),
    "code":("2026_11_03_five_qubit_algebraic_locality","2026_11_03_five_qubit_algebraic_locality"),
    "causal":("2026_11_03_blind_two_growth_causal_competition","2026_11_03_blind_two_growth_causal_competition"),
    "curved":("2026_11_03_curved_covariant_holonomy","2026_11_03_curved_covariant_holonomy_obstruction"),
    "matter":("2026_11_03_two_species_stress_gravity_ward","2026_11_03_two_species_stress_spin2_ward"),
    "metric":("2026_11_03_operational_metric_from_dynamics","2026_11_03_operational_metric_from_dynamics")
}
@pytest.fixture(scope="module")
def certs():
    for k,(source,_) in SCRIPTS.items():
        p=subprocess.run([sys.executable,str(ROOT/"analysis"/(source+".py"))],
             cwd=str(ROOT),capture_output=True,text=True,timeout=120)
        assert p.returncode==0,(k,p.stdout[-2000:],p.stderr[-2000:])
        assert "PACHNER" in p.stdout or "QUBIT" in p.stdout or "BLIND" in p.stdout or "CURVATURE" in p.stdout or "SPECIES" in p.stdout or "METRIC" in p.stdout
    return {k:json.loads((ROOT/"data"/(dest+".json")).read_text(encoding="utf-8"))
            for k,(_,dest) in SCRIPTS.items()}
def test_six_producers_replay(certs):
    assert len(certs)==6
    assert all(x["status"].startswith("PASS_") for x in certs.values())
def test_pachner_moves_preserve_topological_dimension_and_deficit(certs):
    c=certs["pachner"]
    assert c["accepted_moves"]>=100
    assert set(c["move_census"])=={"1-3","3-1","2-2"}
    assert all(v>5 for v in c["move_census"].values())
    assert all(h["euler_characteristic"]==2 for h in c["history"])
    assert all(h["deficit_units_pi_over3"]==12 for h in c["history"])
    assert all(abs(h["gauss_bonnet_angle_sum_radians"]-4*math.pi)<1e-12 for h in c["history"])
def test_code_correctability_all_two_erasures(certs):
    c=certs["code"]
    assert c["code_dimension"]==2 and c["physical_qubits"]==5 and c["distance"]==3
    assert c["pauli_errors_weight_at_most_2_checked"]==106
    assert c["max_logical_compression_deviation"]<1e-12
    assert c["all_two_qubit_erasures_Knill_Laflamme"]
    assert len(c["three_qubit_region_reconstruction_witnesses"])==10
def test_same_code_logical_unitary_multiple_physical_regions(certs):
    c=certs["code"]["same_logical_unitary_from_distinct_physical_three_body_Hamiltonians"]
    assert c["A_region"]!=c["B_region"]
    assert c["physical_Hamiltonian_difference_operator_norm"]>.5
    assert c["max_difference_on_all_encoded_unitary_evolutions"]<1e-10
def test_blind_causets_fit_density_not_hidden_interval_profile(certs):
    c=certs["causal"]
    assert c["target_dimension_supplied"]==4
    assert c["frozen_selected_params"]=={"transitive_percolation":0.04,"disjoint_independent_chains":10}
    target=c["heldout_36_target_sprinklings"]
    for name,n in c["heldout_null_100_each"].items():
        assert abs(n["pair_fraction"]-target["pair_fraction"])<.025
        assert n["L1_interval_profile_discrepancy"]>.3
        assert abs(n["mean_chain_height_difference"])>.8
def test_gauge_holonomy_and_continuum_flux(certs):
    c=certs["curved"]
    assert len(c["rows"])==9
    assert all(x["gauge_transform_verified"] for x in c["rows"])
    assert all(x["covariant_shift_commutator_norm"]<1e-12 for x in c["rows"] if x["flux_integer_m"]==0)
    for m in (1,2):
        rows=sorted((x for x in c["rows"] if x["flux_integer_m"]==m),key=lambda x:x["L"])
        assert rows[-1]["covariant_shift_commutator_norm"]<rows[0]["covariant_shift_commutator_norm"]
        assert all(x["quantized_total_flux"]==m for x in rows)
def test_two_independent_stress_sources_and_universal_soft_constraint(certs):
    c=certs["matter"]
    assert all(all(v=="0" for v in x["stress_divergence"]) for x in c["matter_species"])
    assert any(z!="0" for z in c["off_shell_control_divergence"])
    assert "kA" in c["exact_soft_spin2_polarization_variation"]
    assert "kB" in c["exact_soft_spin2_polarization_variation"]
    assert c["universal_coupling_nullspace"]==[1,1]
    assert c["species_mass_squared"]==[0,9,0,9]
def test_operational_distance_requires_interaction_graph(certs):
    c=certs["metric"]
    rows=c["same_degree_nonisomorphic_graphs"]
    assert len(rows)==2 and all(r["degree_sequence"]==[3]*8 for r in rows)
    assert rows[0]["pair_distance_census"]=={"1":12,"2":12,"3":4}
    assert rows[1]["pair_distance_census"]=={"1":12,"2":16}
    assert all(r["exact_Taylor_order_recovers_all_pair_distances"] for r in rows)
    assert all(r["unidentifiable_absolute_J_and_t_separately"] for r in rows)
