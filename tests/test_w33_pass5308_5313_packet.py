import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT/'data'/name).read_text())

def test_5308_d4_triality():
    d=load('PART_W33_PASS5308_HOFFMAN_D4_TRIALITY.json')
    assert d['H_order']==576 and d['N_order']==192
    assert d['N_structure']=='(C2)^3 : S4 = W(D4)'
    assert d['N_center_order']==2 and d['normal_V8_count']==3
    assert d['quotient_H_over_N']=='C3'
    assert sorted(d['triality_cycle_on_three_V8s'])==[0,1,2]

def test_5309_tomotope_action():
    d=load('PART_W33_PASS5309_HOFFMAN_TOMOTOPE_DEGREE12_ACTION.json')
    assert d['cover_orbits']==[1,12]
    assert d['action_kernel_order']==2
    assert d['induced_degree12_order']==d['tomotope_published_group_order']==96
    assert len(d['explicit_12point_conjugator'])==12
    assert d['group_isomorphism']=='W(D4)/Z(W(D4)) ~= Gamma(T)'

def test_5310_two_192_covers():
    d=load('PART_W33_PASS5310_TESSERACT_D4_TOMOTOPE_DOUBLECOVERS.json')
    assert d['full_tesseract_symmetry_order']==384
    assert d['rotation_group']['order']==d['WD4']['order']==192
    assert d['rotation_group']['element_orders']['8']==48
    assert '8' not in d['WD4']['element_orders']
    assert d['central_quotients']['rotation_over_center']==96
    assert d['central_quotients']['WD4_over_center']==96
    assert d['intersection']['order']==96 and d['intersection']['center']==2

def test_5311_latin_q4_census():
    d=load('PART_W33_PASS5311_ORDER4_LATIN_TOROIDAL_Q4_CENSUS.json')
    assert d['latin_squares']==576
    assert d['same_symbol_knight_edge_census']=={'0':96,'8':192,'16':288}
    assert sorted(x['size'] for x in d['common_action_orbits'])==[48,48,96,192,192]
    assert d['common_grid_Q4_board_group_order']==128

def test_5312_action_obstruction():
    d=load('PART_W33_PASS5312_HOFFMAN_LATIN_DEGREE12_ACTION_OBSTRUCTION.json')
    assert d['hoffman_degree12']['point_stabilizer']['center']==2
    assert d['latin_even_degree12']['point_stabilizer']['center']==1
    assert d['latin_even_degree12']['point_stabilizer']['element_orders']['4']==6
    assert d['latin_autotopy96']['natural_12label_orbits']==[4,4,4]

def test_5313_triality_parastrophe():
    d=load('PART_W33_PASS5313_D4_TRIALITY_LATIN_PARASTROPHE_QUOTIENT.json')
    assert d['hoffman_diagram']['H_over_WD4']=='C3'
    assert d['latin_diagram']['quotient']=='C3'
    assert d['hoffman_diagram']['after_center']['WD4_over_Z']==96
    assert d['latin_diagram']['autotopy_order']==96
