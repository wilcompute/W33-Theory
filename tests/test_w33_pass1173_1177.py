from analysis.w33_pass1173_clebsch_gordan_sym3 import main as p1173
from analysis.w33_pass1174_d5_adjoint_image import main as p1174
from analysis.w33_pass1175_meataxe_gf7_simulation import main as p1175
from analysis.w33_pass1176_manuscript_amendment import main as p1176
from analysis.w33_pass1177_ihara_zeta_degree30 import main as p1177
def test_1173():
 r=p1173();assert r['degree_square_sum']==51840 and 'not Clebsch' in r['scope_barrier']
def test_1174():
 r=p1174();assert r['exact_we6_image_decomposition']=='1 + 20 + 24' and r['d5_adjoint_identified'] is False
def test_1175():
 r=p1175();assert r['module_total_dim']==2195 and r['simulation_performed'] is False and 'does not' in r['field_warning']
def test_1176():
 r=p1176();assert r['exact_residual_dimension']==1952 and r['exact_residual_commutant']==1109
def test_1177():
 r=p1177();assert r['hashimoto_coefficient']==11 and r['primitive_cycle_classes']['3']==320
