import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def J(n): return json.loads((R/'data'/n).read_text())
def test_erasure():
 x=J('PART_W33_PASS5044_EXACT_APARTMENT_ERASURE.json'); assert x['code']==[1620,81,81] and x['weight3_check_rank']==1539 and x['safe_through']==80
def test_jacobian(): assert J('PART_W33_PASS5045_JACOBIAN_2ADIC_FILTRATION.json')['height_dimensions']==[81,29,29,23,1,1]
def test_compiler(): assert J('PART_W33_PASS5046_LOCAL_V24_COMPILER.json')['point_star']['rank']==24
def test_family(): assert J('PART_W33_PASS5047_W3Q_SYMBOLIC_BUILDING_THEOREM.json')['apartments_per_chamber']=='q^4'
def test_action():
 x=J('PART_W33_PASS5048_APARTMENT_ACTION.json'); assert x['dimension_sum']==1620 and x['square_sum']==131 and x['degree81_multiplicity']==5
def test_theta(): assert J('PART_W33_PASS5049_THETA_DUAL_GEOMETRY.json')['theta_triples']==4320
def test_qanchors():
 x=J('PART_W33_PASS5051_Q_FAMILY_THETA_CODE.json'); assert x['q2']['code']==[90,16,16] and x['q3']['code']==[1620,81,81]
