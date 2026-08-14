import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(n):return json.loads((ROOT/'data'/n).read_text())
def test_5134():
 d=J('PART_W33_PASS5134_THETA_FIRST_ORDER_BLINDNESS.json')
 assert all(a['support_induced_degree']==a['support_external_degree']==a['ambient_degree']//2 for a in d['anchors'].values())
def test_5135():
 d=J('PART_W33_PASS5135_BT865_PARABOLIC_ALIGNMENT.json');assert d['point_parabolic']['pencil_image']=='A4' and d['point_parabolic']['quotient_by_H27']=='SL(2,3)' and d['line_parabolic']['line_point_image']=='S4' and d['line_parabolic']['kernel_equals_root_F3_3']
def test_5136():
 d=J('PART_W33_PASS5136_ODDQ_BICYCLE_EXTRA_ANCHORS.json');assert d['anchors']['9']['rank_F2']==451 and d['anchors']['9']['bicycle_dimension']==737 and d['anchors']['13']['rank_F2']==1275 and d['anchors']['13']['bicycle_dimension']==2209
def test_5137():
 d=J('PART_W33_PASS5137_RANK3_JENNINGS_MEMORY.json')
 for k,p in [('A3_p5',5**6),('C3_p7',7**9)]:
  a=d['examples'][k];L=a['layers'];assert L==L[::-1] and len(L)==a['layer_count'] and sum(L)==p==a['regular_module_dimension'] and L[a['central_layer_index']]==a['central_layer_dimension']
def test_5138():
 d=J('PART_W33_PASS5138_Q4_ROOT_COSET_SPECTRUM.json');assert sum(d['spectrum'].values())==256 and d['generic_rank']==184 and d['native_F2_rank']==180 and d['native_rank_drop']==4
def test_5139():
 d=J('PART_W33_PASS5139_Q5_ROOT_COSET_SPECTRUM.json');assert sum(d['spectrum'].values())==625 and d['minus4_multiplicity']==220 and d['generic_rank']==405 and d['native_F5_rank']==397 and d['native_rank_drop']==8
def test_5140():
 d=J('PART_W33_PASS5140_Q3_THETA_TRIANGLE_CURVATURE.json');rows=[d['single_chamber_star']]+list(d['two_star_xor_by_gallery_distance'].values());assert all(r['induced_edges']==4*r['weight'] and r['fully_selected_theta_checks']==0 for r in rows) and len({r['selected_triangles'] for r in rows})>1
def test_5141():
 d=J('PART_W33_PASS5141_Q3_CUBIC_THETA_MOMENT.json');rows=d['rows'];assert {r['normalized_moment_2'] for r in rows.values()}=={'8'} and [r['normalized_moment_3'] for r in rows.values()]==['8','6','7','98/13','39/5']
