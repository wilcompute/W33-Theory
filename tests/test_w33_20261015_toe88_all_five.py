"""TOE88 five-track exact and synthetic reproducibility tests."""
from functools import lru_cache
import json
from pathlib import Path
import pytest
from analysis import w33_20261015_toe88_tate_albert_bridge as T
from analysis import w33_20261015_toe88_parity_membranes as P
from analysis import w33_20261015_toe88_ancilla_syndrome as A
from analysis import w33_20261015_toe88_adaptive_mub as M

ROOT=Path(__file__).resolve().parents[1]

@lru_cache(None)
def fresh(t):
    return {"tate":T.certificate,"parity":P.certificate,
            "ancilla":A.certificate,"mub":M.certificate}[t]()

def test_binary_26dim_albert_candidate_is_explicit_isomorphism():
    x=fresh("tate")
    b=x["binary_aug_equivariant_isomorphism_to_selected_H1"]
    assert x["augmentation_module_dimension"]==26
    assert b["rank"]==26
    assert len(b["explicit_aug_to_H1_basis_images"])==26
    assert x["F3_equivariant_isomorphism_to_regular_augmentation"]=="OBSTRUCTED_BY_CENTRAL_JORDAN_RANK"

def test_F3_central_Jordan_obstruction():
    x=fresh("tate")
    assert x["F3_aug_center_Jordan"]["Jordan_1_2_3_block_counts"]==[0,1,8]
    assert x["F3_selected_H1_center_Jordan"]["Jordan_1_2_3_block_counts"]==[1,2,7]
    assert x["F3_aug_center_Jordan"]["rank_g_minus_identity"]==17
    assert x["F3_selected_H1_center_Jordan"]["rank_g_minus_identity"]==16

def test_all_13_cyclic_Tate_sector_selectors():
    x=fresh("tate")
    cls=x["ternary_H1_H2_Jordan_Tate_all_13_classes"]
    assert len(cls)==13 and sum(v["size"] for v in cls)==468
    for obj in cls:
        d=obj["cyclic_Jordan_Tate"][:4]
        for module in ("H1","H2"):
            ranks=[c[module]["rank_g_minus_identity"] for c in d]
            tate=[c[module]["cyclic_Tate_H0_Hminus1_dimension"] for c in d]
            assert tate.index(max(tate))==ranks.index(min(ranks))
            assert tate.count(max(tate))==1
        assert d[0]["H1"]["Jordan_1_2_3_block_counts"]!=[]

def test_torsion_parity_membrane_construction_and_controls():
    x=fresh("parity")
    assert [c["mod2_Bockstein_image_rank"] for c in x["representatives"]]==[0,0,2,2]
    for c in x["representatives"][2:]:
        assert len(c["integer_membrane_witnesses"])==2
        for m in c["integer_membrane_witnesses"]:
            assert m["face_count"]==24
            assert m["square_face_count"]+m["triangle_face_count"]==24
            assert len(m["Bockstein_edge_support"])>0

def test_99_ancilla_six_layer_SUM_schedule():
    x=fresh("ancilla")
    assert x["face_Z_stabilizer_count"]==99
    assert x["edge_data_qutrits"]==135
    assert x["ancilla_qutrits_per_round"]==99
    assert x["SUM_gates_per_round"]==351
    assert x["conflict_free_parallel_layers_per_round"]==6
    assert x["ancilla_Z_hook_propagation_witness"]["unmeasured_by_Z_type_checks"]

def test_correlated_faults_and_invisible_Z_error_control():
    x=fresh("ancilla")
    b,zero=x["configurations"]
    assert b["scenario"]=="noise_baseline"
    assert zero["scenario"]=="no_hook_Z"
    assert b["rounds"]==zero["rounds"]==3
    assert b["shots"]==zero["shots"]==320
    assert b["observed_means"]["true_Z_nonzero"]>0
    assert zero["observed_means"]["true_Z_nonzero"]==0
    assert b["observed_means"]["majority_readout_mismatch"]<b["observed_means"]["raw_final_readout_mismatch"]

def test_adaptive_EB_and_SPAM_robust_bound():
    x=fresh("mub")
    assert x["conservative_true_EB_survival_bound"]==pytest.approx(.52)
    assert x["calibrated_postnoise_EB_bound"]==pytest.approx(.508968)
    assert x["accepted_shots"]==1200
    assert x["reject_at_successes_at_least"]==665
    assert x["exact_max_EB_tail_alpha"]<=.001
    assert x["alternative_power_under_ideal_conditional_independence"]>.99

def test_setting_dependent_loss_entanglement_breaking_spoof():
    x=fresh("mub")
    controls=x["state_dependent_heralding_attacks"]
    assert controls[0]["accepted_state_mean_fidelity"]==.5
    assert controls[1]["total_accepted_fraction"]==pytest.approx(.325)
    assert controls[1]["accepted_state_mean_fidelity"]==pytest.approx(11/13)
    assert controls[2]["accepted_state_mean_fidelity"]==1
    assert x["adaptive_EB_conditional_per_round_survival_bound"]==.5

@pytest.mark.parametrize("track,filename",[
    ("tate","w33_20261015_toe88_tate_albert_bridge.json"),
    ("parity","w33_20261015_toe88_parity_membranes.json"),
    ("ancilla","w33_20261015_toe88_ancilla_syndrome.json"),
])
def test_exact_or_seeded_frozen_certificate(track,filename):
    current=fresh(track)
    frozen=json.loads((ROOT/"data"/filename).read_text(encoding="utf8"))
    assert current==frozen
