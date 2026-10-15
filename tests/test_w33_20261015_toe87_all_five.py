"""TOE87 regression certificates: five independent tracks and explicit nulls."""
from functools import lru_cache
from pathlib import Path
import json
import math
import pytest

from analysis import w33_20261015_toe87_modular_bockstein_triples as M
from analysis import w33_20261015_toe87_adversarial_temporal as T
from analysis import w33_20261015_toe87_fault_aware_routing as F

ROOT=Path(__file__).resolve().parents[1]
@lru_cache(maxsize=None)
def fresh(kind):
    return {"modular":M.certificate,"temporal":T.test_design,
            "fault":F.certificate}[kind]()

def test_complete_13_modular_classes():
    x=fresh("modular")["modular_pair_classification"]
    assert len(x["classes"])==13
    assert x["all_468_pairs_represented"]==468
    assert x["shared_unique_H1_H2_polarization_class_count"]==13
    assert x["overlap_signature_count"]==4

def test_bockstein_rank_exactly_matches_prime_primary_torsion():
    x=fresh("modular")["modular_pair_classification"]
    for c in x["classes"]:
        tors=c["integral_torsion"]
        for p in (2,3):
            rank=c[f"Bockstein_F{p}"]["bockstein_image_dimension"]
            assert rank==sum(t%p==0 for t in tors)
            # The total chain dimensions imply k = 109-r, H2=99-r.
            assert c[f"Bockstein_F{p}"]["H1_Fp_dimension"]-c[f"Bockstein_F{p}"]["H2_Fp_dimension"]==10

def test_binary_representation_decomposition_uniform_by_torsion_class():
    x=fresh("modular")["modular_pair_classification"]
    for c in x["classes"]:
        a=c["H1"]["F2_semisimple"]
        b=c["H2"]["F2_semisimple"]
        t=c["integral_torsion"]
        assert a["trivial_multiplicity"]==0 and b["trivial_multiplicity"]==2
        if t==[]:
            assert a["faithful_6D_simple_multiplicity"]==3
            assert a["four_2D_simple_multiplicities"]==[1]*4
            assert b["faithful_6D_simple_multiplicity"]==1
        elif t==[3,3]:
            assert a["faithful_6D_simple_multiplicity"]==2
            assert a["four_2D_simple_multiplicities"]==[0]*4
            assert b["four_2D_simple_multiplicities"]==[0]*4
        else:
            assert t==[6,6]
            assert a["faithful_6D_simple_multiplicity"]==2
            assert sum(a["four_2D_simple_multiplicities"])==1
            assert sum(b["four_2D_simple_multiplicities"])==1

def test_ternary_radical_filtration_family_invariance():
    x=fresh("modular")["modular_pair_classification"]
    for c in x["classes"]:
        a=c["H1"]["F3_radical_filtration"]
        b=c["H2"]["F3_radical_filtration"]
        if c["integral_torsion"]==[]:
            assert a==[26,24,21,15,11,6,3,1,0]
            assert b==[16,13,10,6,4,2,1,0]
        else:
            assert a==[14,13,11,7,4,1,0]
            assert b==[4,3,2,0]

def test_three_orbit_counterexample_to_naive_polarization_extension():
    x=fresh("modular")["three_orbit_stress"]
    assert x["three_orbit_cases_checked"]==12
    assert x["sample_is_exhaustive"] is False
    assert x["counterexample_found"] is True
    c=next(a for a in x["cases"] if a["orbit_triple"]==[0,10,1])
    assert c["H1_four_direction_ranks"]==[2]*4
    assert c["H2_four_direction_ranks"]==[13,12,13,13]
    assert c["H2_dimension_F3"]==21 and c["logical_H1_dimension_F3"]==4

def test_overlap_histogram_not_an_integral_torsion_classifier():
    x=fresh("modular")["modular_pair_classification"]
    # Distinct torsion classes can share identical edge-overlap profiles.
    assert x["overlap_signatures_ambiguous_for_torsion"]
    assert set(["[]","[6, 6]"])==set(
        x["overlap_signatures_ambiguous_for_torsion"]["[675, 54, 0, 0, 0]"])

def test_four_MUB_2design_and_adversarial_EB_spoof():
    x=fresh("temporal")
    assert x["four_MUB_two_design_states"]==12
    assert x["two_design_residual_max_abs"]<1e-12
    assert x["entanglement_breaking_mean_fidelity_upper_bound"]==.5
    assert x["explicit_adversarial_single_probe_EB_success"]==pytest.approx(1)
    assert x["multiple_probe_mean_fidelities"]["rotated_EB"]==pytest.approx(.5)
    assert x["multiple_probe_mean_fidelities"]["clock_EB"]==pytest.approx(.5)
    assert x["multiple_probe_mean_fidelities"]["coherent_v025"]==pytest.approx(.625)

def test_temporal_statistical_design_and_assumptions():
    x=fresh("temporal")
    assert x["exact_max_null_false_positive_probability"]<=.001
    assert x["exact_alternative_power"]>.999
    assert x["calibrated_detected_shot_alternative_expectation"]>x["calibrated_detected_shot_EB_upper_bound"]
    assert x["accepted_shots"]==1200
    assert x["robustness_boundaries"]["state_independent_erasure"]
    assert x["robustness_boundaries"]["no_device_independence"]

def test_fault_aware_routing_exposure_strictly_changes_by_topology():
    x=fresh("fault")
    assert x["shots_per_case"]==192
    assert len(x["cases"])==6
    assert x["ambiguous_single_site_syndrome_patterns"]>=0
    for i in range(3):
        a,b=x["cases"][2*i:2*i+2]
        assert a["model"]=="all_to_all"
        assert b["model"]=="linear_nearest_neighbor"
        assert a["SWAP_count"]==90 and b["SWAP_count"]>=498
        assert a["analytic_prob_zero_gate_fault"]>b["analytic_prob_zero_gate_fault"]
        assert a["metrics"]["any_gate_fault_per_shot_mean"]<b["metrics"]["any_gate_fault_per_shot_mean"]

@pytest.mark.parametrize("type_,filename",[
    ("modular","w33_20261015_toe87_modular_bockstein_triples.json"),
    ("fault","w33_20261015_toe87_fault_aware_routing.json")
])
def test_exact_frozen_certificate(type_,filename):
    frozen=json.loads((ROOT/"data"/filename).read_text(encoding="utf8"))
    assert fresh(type_)==frozen

def test_stabilized_H27_binary_Euler_module_theorem():
    from analysis import w33_20261015_toe87_euler_stable_module as E
    x=E.certificate()
    assert x["vertex_H27_orbit_sizes"]==[27]
    assert x["edge_H27_orbit_sizes"]==[27]*5
    assert x["triangle_H27_orbit_sizes"]==[9]*5
    assert x["added_square_H27_orbit_sizes"]==[27]*2
    assert x["virtual_H1_minus_H2_simple_multiplicities"]==[-2,0,0,0,0,2]
    assert x["pairs_covered"]==468 and x["equivalence_classes_checked"]==13
    assert x["triangle_45_simple_multiplicities"]=={
        "trivial_multiplicity":5,
        "four_2D_simple_multiplicities":[2]*4,
        "faithful_6D_simple_multiplicity":4}
    frozen=json.loads((ROOT/"data/w33_20261015_toe87_euler_stable_module.json").read_text(encoding="utf8"))
    assert x==frozen
