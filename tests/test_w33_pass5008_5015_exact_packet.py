import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n):return json.loads((ROOT/'data'/n).read_text())
def test_5008_closure():
 x=load('PART_W33_PASS5008_GLOBAL_CHARACTER_CLOSURE_RADIUS_COMPILER.json');assert (x['observables'],x['character_rank'],x['XOR_relations'])==(1890,324,1566);assert x['cross_octahedron_relations']==1296 and x['covering_radius']==[134,173]
def test_5009_split():
 x=load('PART_W33_PASS5009_OCTAHEDRON_84_SPLITS_60_24.json');assert (x['V84_projector_rank'],x['tritangent_endpoint_image_rank'])==(84,24);assert x['V60_dimension']==60
def test_5010_structure():
 x=load('PART_W33_PASS5010_K60_STRUCTURE.json');assert (x['K60'],x['S14'],x['Q46'])==(60,14,46);assert x['V20_map_rank']==14 and x['V20_kernel']==6
def test_5011_reader():
 x=load('PART_W33_PASS5011_FIRST_MIXED_SUPPORT13_AND_TRIT_K33.json');assert x['pure_tritangent_minimum']=={'support':6,'count':120,'geometry':'signed K3,3'};assert x['mixed_minimum']['support']==13 and x['mixed_minimum']['count']==8000
def test_5012_v24():
 x=load('PART_W33_PASS5012_FAILURE_FRAME_IS_CANONICAL_V24.json');assert x['rank']==24 and x['rowspan_equals_kernel_C'];assert x['tight_frame_spectrum']=={'60':24,'0':16}
def test_5013_steiner():
 x=load('PART_W33_PASS5013_K33_STEINER_BIJECTION.json');assert x['support6_signed_K33_circuits']==120 and x['bijection']
def test_5014_points():
 x=load('PART_W33_PASS5014_40_TRITANGENT_COVERS_ARE_W33_POINTS.json');assert x['nine_tritangent_exact_covers']==200 and x['multiplicity_census']=={'one_line':160,'four_lines':40};assert x['special_40']['incidence_rank']==25
def test_5015_incident_pairs():
 x=load('PART_W33_PASS5015_160_COVERS_W33_INCIDENCES.json');assert x['covers']==160 and x['incident_point_line_pairs']==160 and x['bijection']
