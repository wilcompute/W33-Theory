from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(name):return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))

def test_4632_module_separation():
    d=J('PART_W33_PASS4632_PERIODIC_HOMOLOGY_MODULE_SEPARATION.json')
    assert d['periodic_homology']=={'H27_dimension':15,'H36_dimension':24}
    assert d['point_side_W33_modular_layers']['rank_A_mod2']==16
    c=d['equivariant_map_comparison']
    assert c['H36_to_Q24']['nonzero_map_ranks']==[9]
    assert c['Q24_to_H36']['nonzero_map_ranks']==[1]
    assert c['H27_to_Q15']['nonzero_map_ranks']==[14]
    assert c['Q15_to_H27']['nonzero_map_ranks']==[1]

def test_4633_corrected_sextet_and_stabilizer():
    d=J('PART_W33_PASS4633_M24_SEXTET_SECTION_STABILIZER.json')
    assert d['corrected_Pass4615']['zero_coordinate_assignment']==[21,20,19,18,22,17]
    assert d['M24_action']['sextet_orbit']==1771
    assert d['M24_action']['sextet_stabilizer_order']==138240
    assert d['M24_action']['six_tetrad_image_order']==720
    assert d['M24_action']['six_tetrad_kernel_order']==192
    assert d['section_stabilizer']['order']==2160
    assert d['section_stabilizer']['section_codeword_orbits']==[1,18,45]
    old=J('PART_W33_PASS4615_HEXACODE_SECTION_RECONSTRUCTS_MOG_SEXTET.json')
    assert old['sextet_completion']['zero_coordinate_assignment']==[21,20,19,18,22,17]
    assert old['sextet_completion']['all_pairwise_unions_are_Golay_octads'] is True

def test_4634_support11_mass():
    d=J('PART_W33_PASS4634_SUPPORT11_EXACT.json')
    assert d['subsets']==2311801440 and d['distinct_weights']==153
    assert (d['minimum_weight'],d['minimum_count'])==(614,12960)
    assert (d['maximum_weight'],d['maximum_count'])==(1026,1080)
    assert sum(d['spectrum'].values())==2311801440

def test_4635_six_signature_collision():
    d=J('PART_W33_PASS4635_C8_SIX_SIGNATURE_COLLISION_CRITERION.json')
    a={x['geometry']:x for x in d['anchors']}
    assert a['GQ(2,2)']['collision'] is True
    assert a['GQ(2,2)']['apartment_coefficient']==a['GQ(2,2)']['star_coefficient']==36
    assert a['GQ(2,4)=Q^-(5,2)']['apartment_coefficient']==60
    assert a['GQ(3,3)=W33']['apartment_coefficient']==712
    assert a['GQ(3,3)=W33']['star_coefficient']==180

def test_4636_construction_a_boundary():
    d=J('PART_W33_PASS4636_CONSTRUCTION_A_GOLAY_LEECH_OBSTRUCTION.json')
    c=d['construction_A']
    assert (c['det_L_C6'],c['det_L_G24'],c['index_LG24_over_LC6'])==(4096,1,64)
    assert c['norm2_roots_LC6']==c['norm2_roots_LG24']==48
    assert 'not' in d['Leech_obstruction'].lower() or 'rootless' in d['Leech_obstruction'].lower()

def test_4637_4639_bonkers():
    d7=J('PART_W33_PASS4637_SEXTET_TRANSVERSAL_CODE_AFFINE_BIJECTION.json')
    assert d7['transversal_orbits']==d7['codeword_orbits']==[1,18,45]
    assert [x['admissible_fixed_targets'] for x in d7['equivariant_bijection_certificates']]==[1,1]
    d8=J('PART_W33_PASS4638_GOLAY_GLUE_TETRAD_MODULE.json')
    assert d8['glue_quotient']['induced_group_order']==d8['tetrad_module']['induced_group_order']==720
    assert d8['intertwiner_space']['ranks_of_three_nonzero_maps']==[1,6,6]
    d9=J('PART_W33_PASS4639_SIMPLEX_DOUBLE_DIFFERENTIAL_CANCELLATION.json')
    assert d9['operators']['D0_cross']['rank']==12 and d9['operators']['Delta_within']['rank']==12
    assert d9['operators']['D_full_polar']['rank']==6
    assert d9['operators']['D_full_polar']['homology_dimension']==51
    assert d9['simplex_CSS']['CSS']=='[[63,51,3]]'
