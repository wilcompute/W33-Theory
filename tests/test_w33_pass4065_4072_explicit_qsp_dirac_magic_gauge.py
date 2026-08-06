from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/PART_4065_4072_EXPLICIT_QSP_DIRAC_MAGIC_GAUGE_BONKERS.json'
def load():return json.loads(DATA.read_text())
def test_five_fronts():
 x=load();assert x['semantic_sha256']=='342e8e7ae8f3ef06750716a1d3bdb25f2db432ee55e3ca35482086e16d6544ed'
 assert x['pass4065_explicit_qsp_phases']['max_top_left_residual']<1.3e-15
 assert x['pass4066_adaptive_magic_correction']['sample_K10']['expected_raw_A_phi']==2047
 assert x['pass4067_lorentzian_dirac_walk']['coin_dimension']==4
 assert x['pass4068_SK1_H1_robust_pulse']['pi_pulse']['coefficient_numeric']>4.77
 assert x['pass4069_gauge_commutant_obstruction']['unitary_gauge_group_from_unbroken_commutant']=='U(1)^3'
def test_three_bonkers():
 x=load();assert x['pass4070_bonkers_reflection_antithermalization']['pure_state_entropy_bound_bits']==1
 assert x['pass4071_bonkers_H1_frame_metrology']['maximum_total_QFI']=='2 t^2'
 assert x['pass4072_bonkers_Kirchhoff_tree_entropy']['exact_ratio']=='tau(Levi)/tau(W33)=4'
