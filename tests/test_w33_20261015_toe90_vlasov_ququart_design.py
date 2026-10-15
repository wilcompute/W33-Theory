"""TOE90 finite-exact Vlasov/W33 ququart measurement witnesses."""
from functools import lru_cache
from pathlib import Path
import json
from fractions import Fraction
import pytest
from analysis import w33_20261015_toe90_vlasov_ququart_design as W
from analysis import w33_20261015_toe90_witting_shot_certification as S

ROOT=Path(__file__).resolve().parents[1]

@lru_cache(None)
def base(): return W.calculate()
@lru_cache(None)
def shots(): return S.certificate()

def test_exact_vlasov_orthogonality_is_W33():
    r=base()
    assert r["orthogonality_SRG"]=={
       "v":40,"k":12,"lambda":2,"mu":4,
       "edges":240,"nonorthogonal_pairs":540,
       "bases":40,"bases_per_ray":4}
    assert r["squared_inner_product_offdiagonal_histogram"]=={
      "0":480,"1/3":1080}

def test_40_ray_ququart_two_design_is_welch_tight():
    r=base()["two_design"]
    assert r["dimension"]==4 and r["rays"]==40
    assert r["frame_potential_2"]==r["Welch_bound"]=="1/10"
    assert r["max_matrix_residual_rounded_14dp"]==0

def test_full_40_basis_joint_entanglement_operator():
    r=base()["entanglement_witness"]
    assert r["max_matrix_residual_rounded_14dp"]==0
    assert r["basis_avg_joint_match_operator"]=="C=(I_16+4*|Phi4><Phi4|)/5"
    assert r["eigenvalue_multiplicities"]=={"1":1,"1/5":15}
    assert r["separable_joint_matching_upper_bound"]=="2/5"

def test_basis_intersection_attack_census():
    r=base()["intercept_resend"]
    assert r["40x40_context_pairs_by_intersection"]=={"0":1080,"1":480,"4":40}
    assert r["matched_probability_by_intersection"]=={"0":"1/3","1":"1/2","4":"1"}
    assert r["uniform_random_eve_basis_matched_probability"]=="2/5"
    assert r["uniform_random_eve_basis_error_probability"]=="3/5"

def test_isotropic_visibility_entanglement_boundary():
    r=base()["isotropic_noise"]
    assert r["strict_detection_visibility_threshold"]=="1/5"
    v={x["visibility"]:x for x in r["cases"]}
    assert v["1/5"]["matched_probability"]=="2/5"
    assert not v["1/5"]["certifies_entanglement"]
    assert v["1/4"]["matched_probability"]=="7/16"
    assert v["1/4"]["certifies_entanglement"]

def test_independent_readout_confusion_shot_protocol():
    c=shots()
    assert c["n_independent_accepted_pairs"]==8192
    assert c["per_side_readout_error"]=="1/50"
    assert c["separable_true_match_bound"]=="2/5"
    assert c["reject_separability_at_reported_match_count_at_least"]==3350
    assert c["exact_iid_binomial_false_positive_probability"]<=.001
    assert c["exact_iid_binomial_model_detection_power"]>.999
    assert Fraction(c["calibrated_separable_reported_match_upper_bound"]) < Fraction(c["calibrated_isotropic_reported_match"])

@pytest.mark.parametrize("kind,path",[
  ("design","w33_20261015_toe90_vlasov_ququart_design.json"),
  ("shots","w33_20261015_toe90_witting_shot_certification.json"),
])
def test_frozen_regeneration(kind,path):
    r=base() if kind=="design" else shots()
    assert r==json.loads((ROOT/"data"/path).read_text(encoding="utf8"))
