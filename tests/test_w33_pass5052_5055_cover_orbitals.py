import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(name): return json.loads((R/'data'/name).read_text())
def test_pass5052_5055_cover_orbitals():
 a=load('PART_W33_PASS5052_200_COVER_ORBITAL_DICTIONARY.json')
 b=load('PART_W33_PASS5053_COVER_GRAM_RECONSTRUCTS_W33.json')
 c=load('PART_W33_PASS5054_OVERLAP6_DIRECTED_EDGE_CARRIER.json')
 d=load('PART_W33_PASS5055_POINT_FLAG_V24_SUBFRAMES.json')
 assert a['ordered_orbitals']==19 and a['fibers']=={'point_covers':40,'flag_covers':160}
 assert [r['cover_overlap'] for r in a['FF_from_flag_pq_to_flag_rs']]==[9,3,0,0,0,3,4,1]
 assert b['Gram_shape']==[200,200] and b['entry_values']==[0,1,2,3,4,6,9]
 assert b['row_histogram_point']['6']==12 and b['row_histogram_flag']['6']==3
 assert c['vertices']==200 and c['edges']==480 and c['degree_profile']=={'point_covers':12,'flag_covers':3}
 assert d['point_frame']['rank']==24 and d['flag_frame']['rank']==24
 assert d['point_frame']['row_norm_squared']==180 and d['flag_frame']['row_norm_squared']==180
 assert d['cross_transform']['rank']==24
