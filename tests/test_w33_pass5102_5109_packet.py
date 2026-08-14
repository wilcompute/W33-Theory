import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_pass5102_5109_frozen_certificates():
    p2=load('PART_W33_PASS5102_ROOT_EXPANSION_LOW_GENERATOR.json')
    assert p2['status']=='THEOREM_WITH_Q5_FRONTIER'
    assert p2['anchors']['5']['max_distinct_pair_intersection']==125
    assert p2['q5']['three_star_minimum']==1125
    assert sum(r['status']=='SAT_CHAMBER_STAR' for r in p2['q5']['minimum_cut_rigidity'])==8

    p3=load('PART_W33_PASS5103_Q4_HEAVY_CHART_CLOSURE.json')
    assert p3['heavy_chart_global_minimum']==384
    assert p3['minimum_shell']['minimum_words']==425
    assert all(r['objective']==384 and r['mip_gap']==0.0 for r in p3['four_chart_role_milps'])

    p4=load('PART_W33_PASS5104_SQRT17_GLOBAL_INTEGRAL_INTERTWINER.json')
    assert p4['minimal_index']==2
    assert p4['global_theta_carrier']['rank']==30
    assert p4['global_theta_carrier']['integral_lattice_index_for_15_lanes']==32768

    p5=load('PART_W33_PASS5105_U81_DUAL_TORSOR_CONTROLLER.json')
    assert p5['U']['order']==81 and p5['U']['derived']==9
    assert p5['weld']['intersection_equals_U_derived']
    assert p5['Steinberg']['native_restriction']=='H1(F3)|U ~= F3[U] free rank 1'

    p6=load('PART_W33_PASS5106_RANK2_LIE_DERIVATIVE_CURVATURE.json')
    assert p6['good_characteristic']['G2']['pair_generated_root_count_histogram']=={'2':10,'3':3,'5':1,'6':1}

    p7=load('PART_W33_PASS5107_ROOT_COSET_INCIDENCE_SMITH.json')
    assert p7['q3']['smith']=='1^68,3^1,0^12'
    assert p7['q3']['rank_F3']==68

    p8=load('PART_W33_PASS5108_U81_JENNINGS_MEMORY.json')
    assert p8['U81']['successive_layers']==[1,2,4,5,7,8,9,9,9,8,7,5,4,2,1]

    p9=load('PART_W33_PASS5109_CURVATURE_KERNEL_V4.json')
    assert p9['sorted_sector_dimensions']==[4,4,2,2]
    assert p9['character_traces']=={'e':12,'a':0,'b':-4,'c':0}

    insert=(ROOT/'analysis/PASS5098_5101_root_coset_supplement_insert.tex').read_text()
    assert r'\input{analysis/PASS5102_5109_root_expansion_controller_lie_insert}' in insert
    reg=load('w33_pass_namespace_registry_v2.d/5102-5109.json') if False else json.loads((ROOT/'data/w33_pass_namespace_registry_v2.d/5102-5109.json').read_text())
    assert reg['status'] in ('RESERVED','EXECUTED')
