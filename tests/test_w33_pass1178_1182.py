from analysis.w33_pass1178_sym3_v24_plethysm_search import main as p1178
from analysis.w33_pass1179_d5_image_split_checker import main as p1179
from analysis.w33_pass1180_meataxe_kernel_manifest import main as p1180
from analysis.w33_pass1181_manuscript_inline_patch_plan import main as p1181
from analysis.w33_pass1182_ihara_degree40_scaffold import main as p1182
def test_1178():
 r=p1178();assert r['target']==2600 and r['plethysm_decomposition_computed'] is False
def test_1179():
 r=p1179();assert r['best_candidate']==[1,20,24] and r['d5_adjoint_identified'] is False
def test_1180():
 r=p1180();assert r['prime']==7 and r['splitting_field_verified'] is False
def test_1181():
 r=p1181();assert r['required_invariants']['residual_commutant']==1109
def test_1182():
 r=p1182();assert r['next_degree']==40 and r['executed'] is True and r['hashimoto_coefficient']==11
