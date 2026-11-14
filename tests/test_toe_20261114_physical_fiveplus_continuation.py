"""Five tested fronts plus one-sensor resilience and independent SAT boundary."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261114_physical_falsifiers_section_noise_fixed_radian as P
import toe_20261114_dropout_resilient_12axis_tomography as R

ROOT=Path(__file__).resolve().parents[1]

def test_four_copy_witness_exact_binomial_power():
    c=P.four_copy_witness()
    assert c["status"].startswith("PASS_")
    assert c["exact_binomial_likelihood_thresholds"]["1.0"]["prepared_copies"]==5600
    for d in c["exact_binomial_likelihood_thresholds"].values():
        assert d["false_positive_Haar"]<=.05+1e-12 and d["power_against_finite_180"]>=.90
def test_all_15552_incompatible_section_pairs():
    c=P.section_cross_obstruction()
    assert c["total_cross_pairs"]==15552 and c["minimum_cross_tensor_squared_norm"]==2
    assert c["cross_contraction_edges_histogram"]=={"2":1080,"6":4320,"10":432,"11":4320,"16":4320,"22":1080}
def test_noisy_180_fiber_decoder():
    c=P.noisy_decoder()
    assert c["samples_pure_states"]==4320
    assert c["results"]["0.81"]["240"]["mean_fidelity"]>.997
    assert c["adaptive_budget360_visibility081"]["pilot_shots_per_axis"]==12
def test_actual_fixed_gate_words_fidelities():
    c=P.fixed_radian_compiler()
    assert c["Clifford_signed_root_orbit_size"]==72
    assert c["depth_vs_fidelity"]["4000"]["min_certified_target_fidelity"]>.999
    assert c["depth_vs_fidelity"]["250"]["max_unit_ticks"]<10000
def test_independent_minimum_20_sensor_failure_tolerance():
    c=R.main()
    assert c["instances"]["1"]["minimum_menu"]==12
    assert c["instances"]["2"]["minimum_menu"]==20
    assert c["instances"]["2"]["all_single_sensor_dropout_patterns_verified"]==20
    assert c["instances"]["2"]["CP_SAT_menu_size_minus_one"]=="INFEASIBLE"
def test_MUB_sat_two_classes_unknown_not_misreported_as_unsat():
    j=json.loads((ROOT/"data/toe_20261114_fivequbit_MUB_independent_CaDiCaL_SAT.json").read_text())
    assert j["status"]=="PASS_INDEPENDENT_CADICAL_GF2_RANK_CODE_CNF_CONSTRUCTION"
    assert j["classification"]=="INDEPENDENT_SAT_FRONT_UNDECIDED"
    a=j["records"]
    assert len(a)==6
    assert [x["status"] for x in a[:4]]==["SAT_WITNESS","SAT_WITNESS","UNSAT_CADICAL","UNSAT_CADICAL"]
    assert [x["rep"] for x in a[4:]]==[692,694]
    assert all(x["status"]=="UNDECIDED_BOUNDED_CONFLICTS" for x in a[4:])
    assert all(x["total_clauses"]==1685712 and len(x["deterministic_CNF_clause_SHA256"])==64 for x in a[4:])

if __name__=="__main__":
    tests=[globals()[k] for k in sorted(globals()) if k.startswith("test_")]
    for f in tests:
        f()
        print("PASS",f.__name__,flush=True)
    print("PASS",len(tests),"/",len(tests),flush=True)
