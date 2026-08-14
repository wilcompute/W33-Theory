import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(name):return json.loads((ROOT/'data'/name).read_text())

def test_pass5126_q5_leader18():
    d=J('PART_W33_PASS5126_Q5_LEADER18.json')
    assert d['status']=='THEOREM_Q5_SUB625_COUNTEREXAMPLE_LEADER_AT_LEAST_18'
    assert d['universal_girth8_wedge_cap']==25
    assert d['delsarte']['distance_pair_counts']==[25,66,45,0]
    assert d['delsarte']['bonferroni_weight_lower_bound']==625

def test_pass5127_half_escape():
    d=J('PART_W33_PASS5127_THETA_FIRST_ORDER_BLINDNESS.json')
    for q,a in d['anchors'].items():
        assert a['support_induced_degree']==a['support_external_degree']==a['ambient_degree']//2
        assert a['indicator_laplacian_rayleigh']==4*(int(q)-1)

def test_pass5128_parabolic_alignment():
    d=J('PART_W33_PASS5128_BT865_PARABOLIC_ALIGNMENT.json')
    assert d['point_parabolic']['pencil_image']=='A4'
    assert d['point_parabolic']['kernel_derived_equals_root_H27']
    assert d['point_parabolic']['quotient_by_H27']=='SL(2,3)'
    assert d['line_parabolic']['line_point_image']=='S4'
    assert d['line_parabolic']['kernel_equals_root_F3_3']

def test_pass5129_bicycle_anchors():
    d=J('PART_W33_PASS5129_ODDQ_BINARY_INCIDENCE_RANK.json')
    for q,a in d['anchors'].items():
        q=int(q);assert a['binary_rank_drop']==0
        assert a['levi_bicycle_dimension']==q**3+q-1
    assert d['anchors']['9']['field']=='F9 extension anchor'

def test_pass5130_jennings_profiles():
    d=J('PART_W33_PASS5130_RANK3_JENNINGS_MEMORY.json')
    for key,power in [('A3_p5',5**6),('C3_p7',7**9)]:
        a=d['examples'][key];L=a['layers']
        assert L==L[::-1]
        assert len(L)==a['layer_count']
        assert sum(L)==power==a['regular_module_dimension']
        assert L[a['central_layer_index']]==a['central_layer_dimension']
    assert d['examples']['C3_p7']['central_layer_dimension']==925601

def test_pass5131_q4_spectrum():
    d=J('PART_W33_PASS5131_Q4_ROOT_COSET_SPECTRUM.json')
    assert sum(d['spectrum'].values())==256
    assert d['generic_rank']==184 and d['native_F2_rank']==180 and d['native_rank_drop']==4

def test_pass5132_q5_spectrum():
    d=J('PART_W33_PASS5132_Q5_ROOT_COSET_SPECTRUM.json')
    assert sum(d['spectrum'].values())==625
    assert d['minus4_multiplicity']==220 and 625-220==d['generic_rank']==405
    assert d['native_F5_rank']==397 and d['native_rank_drop']==8

def test_pass5133_triangle_curvature():
    d=J('PART_W33_PASS5133_Q3_THETA_TRIANGLE_CURVATURE.json')
    rows=[d['single_chamber_star']]+list(d['two_star_xor_by_gallery_distance'].values())
    assert all(r['induced_edges']==4*r['weight'] for r in rows)
    assert all(r['fully_selected_theta_checks']==0 for r in rows)
    assert len({r['selected_triangles'] for r in rows})>1
