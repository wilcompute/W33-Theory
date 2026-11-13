"""Cross-front regression. Individual sources produce full JSON certificates.
Run directly: python tests/test_toe_20261113_ccz_causal_h27.py
The separate nine-puncture exhaustive enumeration was executed independently
once (costly); this runner checks its archived exact results fail-closed.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_ccz_clifford_normalform as C
import toe_20261113_h27_maximal_translation_bridge as H
import toe_20261113_clock_causal_holographic_firewall as Q
import toe_20261113_chiral_e6_cubic_compatibility as E

def test_ccz_normal_form():
    x=C.verify()
    assert x["ccz_count"]==1
    assert x["nonclifford"] and x["hierarchy_level"]==3
    assert x["cyclotomic_integer_eigenmode_checks"]==27
    assert x["numeric_max_matrix_error"]<1e-12
    assert x["linear_map_det_mod3"]==1

def test_h27_maximal_abelian():
    x=H.verify()
    assert x["four_maximal_abelian_subgroups_order9"]==4
    assert x["maximal_common_commuting_translation_order"]==9
    assert x["no_full_F3_cube_translation_embedding_in_H27"]
    assert x["checked_all_right_actions"]==729

def test_microcausal_circuit():
    x=Q.verify()["unrolling"]
    assert x["strict_temporal_unrolling_acyclic"]
    assert x["events"]==135 and x["interlayer_links"]==324
    assert [t["supported_spatial_sites"] for t in
            x["four_layer_support_counts"]]==[3,9,27,27]
    assert x["max_numerical_factorization_error"]<1e-12

def test_entropic_holography_firewall():
    x=json.loads((ROOT/"data/toe_20261113_causal_holographic_firewalls.json").read_text())
    s=x["holographic_output"]
    assert s["single_qutrit_schmidt_ranks"]==[3,2,3]
    assert s["reduced_purities"]==["11/27","5/9","11/27"]
    assert not s["is_one_uniform_AME_3_3"]
    assert s["three_party_pure_I3_exactly_zero"]

def test_e6_non_equivariant_falsifier():
    x=json.loads((ROOT/"data/toe_20261113_chiral_e6_cubic_compatibility.json").read_text())
    assert x["nonzero_output_count"]==27
    assert x["nonzero_examples"][0]["signed_norm_of_9Ue_cubed"]==46
    assert "NOT" in x["validity"]

def test_five_qubit_puncture_failclosed():
    x=json.loads((ROOT/"data/toe_20261113_five_qubit_nine_puncture_census.json").read_text())
    assert x["nonsingular_candidate_matrices_checked"]==13888
    assert [s["extendible_candidates"] for s in x["puncture_rows"]]==[
        40,36,40,36,40,40,44]
    assert all(s["puncture_can_be_extended_back"] for s in x["puncture_rows"])
    assert "undecided" in x["status_eight"]

if __name__=="__main__":
    for fn in [test_ccz_normal_form,test_h27_maximal_abelian,
               test_microcausal_circuit,test_entropic_holography_firewall,
               test_e6_non_equivariant_falsifier,test_five_qubit_puncture_failclosed]:
        fn()
        print("PASS",fn.__name__,flush=True)
    print("PASS 6/6 exact/certificate and conditional-scope checks")
