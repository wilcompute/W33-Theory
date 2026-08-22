import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_pass7179_d4_scheme():
    d=load('PART_W33_PASS7179_D4_SCHEME_KREIN.json')
    assert d['status']=='PASS'
    assert d['full_scheme_automorphism_order']==103680
    assert d['Rshare_maximal_9_cliques']==80
    assert d['q_polynomial_orderings']==[]

def test_pass7180_q9_radius():
    d=load('PART_W33_PASS7180_Q9_LOCAL_EDIT_RADIUS.json')
    assert d['status']=='PASS'
    assert d['target48_excluded_for_all_core_deletion_radii_0_through_8'] is True
    assert d['exact_maximum_total_after_exact_core_deletions_0_to_5']=={'0':47,'1':46,'2':47,'3':46,'4':46,'5':46}
    assert all(not x['exists'] for x in d['target48_exclusion_additional_radii'])

def test_pass7181_7183_e6_affine_voltage():
    d=load('PART_W33_PASS7181_E6_MINUSCULE_FIBER_VOLTAGE.json')
    assert d['status']=='PASS' and d['Schlaefli']=={'edges':216,'inner_product_counts':d['Schlaefli']['inner_product_counts'],'k':16,'lambda':10,'mu':8,'v':27}
    a=load('PART_W33_PASS7183_C3_AFFINE_AREA_COCYCLE.json')
    assert a['status']=='PASS'
    assert a['zero_holonomy_triangles']==12
    assert a['affine_plane_isomorphisms_fixing_origin']==48
    assert a['determinant_cocycle_matches']==48

def test_pass7182_7184_codes():
    d=load('PART_W33_PASS7182_D4_GLUE_SPREAD_CODE.json')
    assert d['status']=='PASS'
    assert d['all_E8_D4']['D4_subsystems']==3150
    assert d['spread_incidence_code']=='[45,21,5]_2'
    assert d['dual_min_words']==120
    m=load('PART_W33_PASS7184_SPREAD_CODE_V20_V24_MODULE.json')
    assert m['status']=='PASS'
    assert m['V20_identification']['PSp_Hom_dimension']==1
    assert m['V20_identification']['unique_nonzero_intertwiner_rank']==20
    assert m['V20_identification']['outer_PGSp_generator_intertwined'] is True

def test_pass7185_7186_atlas_h27():
    a=load('PART_W33_PASS7185_E8_D4_CHART_ATLAS.json')
    assert a['status']=='PASS' and a['cross4_D4_pairs']==1080 and a['cross4_pairs_per_spread']==40
    assert a['closed_path_holonomy'].startswith('identity')
    h=load('PART_W33_PASS7186_E8_MATTER_H27_CAYLEY.json')
    assert h['status']=='PASS'
    assert h['full_automorphism_order']==1296
    assert h['automorphism_structure']=='H27 : GL(2,3)'
    assert h['distance_transitive'] is True
    assert h['intersection_array']=='{8,6,1;1,3,8}'

def test_aggregate():
    d=load('PART_W33_PASS7171_7186_AGGREGATE.json')
    assert d['status']=='PASS'
    assert d['pass7171_full_E8_root_association_scheme']['Bose_Mesner_dimension']==5
    assert d['pass7176_D4_micro_triality']['triality_frames_per_D4']==3
    assert d['pass7177_support_codes']['90_D4_support_rank']==39
    assert 'global q9 target-48 problem remains open' in d['boundary']
