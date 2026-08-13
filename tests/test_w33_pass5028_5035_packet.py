import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(n):return json.loads((R/'data'/n).read_text())
def test_5028():
 x=load('PART_W33_PASS5028_STEINBERG_PROJECTOR.json');assert x['steinberg_dimension']==81 and x['checks']['R_squared_equals_160R']
def test_5029():
 x=load('PART_W33_PASS5029_APARTMENT_COVER_OPERATOR.json');assert x['rank']==160 and x['gram_spectrum']['40']==81
def test_5030():
 x=load('PART_W33_PASS5030_COVER240_ORBIT_OBSTRUCTION.json');assert x['PGSp_orbit_profile']==[40,40,160]
def test_5031():
 x=load('PART_W33_PASS5031_CRITICAL_GROUPS.json');assert x['levi']['critical_group']=={'4':6,'40':22,'160':1};assert x['all_edge_subdivision']['critical_group']=={'2':52,'8':6,'80':22,'320':1}
def test_5032():
 x=load('PART_W33_PASS5032_APARTMENT_ORBIT_INCIDENCE.json');assert x['apartments']==1620 and x['PSp_stabilizer_order']==16 and x['PGSp_stabilizer_order']==32
def test_5033():
 x=load('PART_W33_PASS5033_CUBE_HOMOLOGY_REPRESENTATIONS.json');assert x['dimensions']=={'H0':1,'H1':81,'H2':40}
def test_5034():
 x=load('PART_W33_PASS5034_APARTMENT_STEINBERG_TIGHT_FRAME.json');assert x['rank']==81 and x['frame_constant']==160
def test_5035():
 x=load('PART_W33_PASS5035_TRIPLE_240_FIREWALL.json');assert x['cover_subdivision']['PGSp_orbits']==[40,40,160]
