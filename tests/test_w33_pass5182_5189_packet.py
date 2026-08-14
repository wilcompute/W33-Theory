from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT/'data'/name).read_text())


def test_pass5182_leader32_wall():
    d=load('PART_W33_PASS5182_Q5_LEADER32_SHARP_PATH_CLOSURE.json')
    assert d['status']=='THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_32'
    assert d['leader_size_closed']==31
    assert d['critical_layer']['N1']==54
    assert d['critical_layer']['integer_weight_lower_bound']==673
    assert d['dense_rebound']['integer_weight_lower_bound']==832


def test_pass5183_leader33_wall():
    d=load('PART_W33_PASS5183_Q5_LEADER33_P5_N4_COUPLING.json')
    assert d['status']=='THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_33'
    assert d['leader_size_closed']==32
    assert d['five_path_geodesic_coupling']=='P5 <= 2 N4'
    assert d['critical_N1_56']['integer_weight_lower_bound']==631


def test_pass5184_n3_quadratic_bridge():
    d=load('PART_W33_PASS5184_ALLQ_N3_QUADRATIC_FORM_BRIDGE.json')
    assert d['status']=='THEOREM_ALL_Q_GALLERY_N3_QUADRATIC_FORM_BRIDGE'
    assert d['identity']=='(x^T A_P x + y^T A_L y)/2 = N1 + 2 N2 + N3'
    assert d['q5_m33_dense_caps']=={'N1=55':532,'N1=56':536,'N1=57':540,'N1=58':544}


def test_pass5185_full_cut_leader():
    d=load('PART_W33_PASS5185_ALLQ_FULL_CUT_LEADER_INEQUALITY.json')
    assert d['status']=='THEOREM_ALL_Q_FULL_CUT_COSET_LEADER_INEQUALITY'
    assert '2|Y cap delta(S)| <= |delta(S)|' in d['cut_leader_criterion']
    assert 'degree-three' in d['q5_degree3_incidence']
    assert '3-2-3' in d['q5_323_path']


def test_pass5186_point_design():
    d=load('PART_W33_PASS5186_P_COMPONENT_KQQ_POINT_DESIGN.json')
    assert d['status']=='THEOREM_ALL_Q_P_COMPONENT_KQQ_POINT_DESIGN'
    q5=d['anchors']['5']
    assert q5['W_points']==156 and q5['P_components']==325
    assert q5['components_per_point_footprint']==25
    assert q5['component_point_graph']=='K_6,6'
    assert q5['component_minimum_atoms']==36
    assert q5['pair_intersection_histogram']=={'1':9750,'5':2340}


def test_pass5187_dual_grid_gram_bridge():
    d=load('PART_W33_PASS5187_DUAL_GRID_POLAR_PAIR_GRAM_BRIDGE.json')
    assert d['status']=='THEOREM_ALL_Q_P_COMPONENT_DUAL_GRID_POLAR_PAIR_AND_GRAM_BRIDGE'
    assert 'BB^T=(q^2-1)I+(q-1)A+J=(q-1)NN^T+J'==d['incidence_gram']
    assert 'B^T N=0' in d['binary_orthogonality']
    assert d['odd_q_binary_rank_anchors']['q=5']=={'rank_F2_B':65,'nullity_F2_N':65}


def test_pass5188_q5_incidence_dual_code():
    d=load('PART_W33_PASS5188_Q5_DUAL_GRID_CODE_EXACT.json')
    assert d['status']=='THEOREM_Q5_DUAL_GRID_CODE_EQUALS_BINARY_INCIDENCE_DUAL'
    assert d['point_line_incidence']['rank_F2']==91
    assert d['P_component_incidence']['rank_F2']==65
    assert d['code_parameters']=='[156,65,12]_2'
    assert '325' in d['minimum_shell']


def test_pass5189_allq_minimum_shell():
    d=load('PART_W33_PASS5189_ALLQ_INCIDENCE_DUAL_MINIMUM_SHELL.json')
    assert d['status']=='THEOREM_ALL_Q_BINARY_W_LINE_DUAL_MINIMUM_SHELL'
    assert d['minimum_distance']=='2(q+1)'
    assert d['minimum_shell_size']=='q^2(q^2+1)/2'
    assert d['q5']['minimum_distance']==12
    assert d['q5']['minimum_words']==325


def test_manuscript_chain():
    manifest=(ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text()
    assert r'\input{analysis/PASS5182_5189_q5_dual_grid_incidence_insert}' in manifest
    insert=(ROOT/'analysis/PASS5182_5189_q5_dual_grid_incidence_insert.tex').read_text()
    assert 'leaders $\\ge33$' in insert or 'leaders $\ge33$' in insert
    assert '[156,65,12]_2' in insert
