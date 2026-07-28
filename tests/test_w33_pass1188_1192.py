from analysis.w33_pass1188_exact_kernel_residual_wedderburn import main as p1188
from analysis.w33_pass1189_group_extension_character_correction import main as p1189
from analysis.w33_pass1190_ihara_bass_degree40 import main as p1190
from analysis.w33_pass1191_point_module_rank3 import main as p1191
from analysis.w33_pass1192_parallel_synthesis_guard import main as p1192
def test_1188():
 r=p1188();assert r['domain']['commutant_dimension']==1193 and r['cubic_kernel']['commutant_dimension']==1118 and r['residual_after_steinberg']['commutant_dimension']==1109
def test_1189():
 r=p1189();assert r['orders']=={'PSp(4,3)':25920,'Sp(4,3)':51840,'W(E6)':51840} and r['exact_sum_of_squares']==51840
def test_1190():
 r=p1190();assert r['hashimoto_quadratic_coefficient']==11 and r['primitive_reduced_cycle_classes']['3']==320 and r['primitive_reduced_cycle_classes']['40']>0
def test_1191():
 r=p1191();assert r['projective_group_order']==25920 and r['point_stabilizer_subdegrees']==[1,12,27]
def test_1192():
 r=p1192();assert r['status']=='PASS' and r['violations']==[]
