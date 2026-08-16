from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_5675_bdg_normal_form():
    x=load('PART_W33_PASS5675_DECK16_EQUIVARIANT_BDG_NORMAL_FORM.json')
    assert x['pass']==5675 and x['real_parameter_dimension']==4
    assert x['magnetic_point']['ratio']==2
    assert x['numerical_replay']['all_level_multiplicities']==[4,4,4,4]
    assert x['numerical_replay']['max_quartic_residual']<1e-7

def test_5676_collision_projector():
    x=load('PART_W33_PASS5676_E6_FIBER_COLLISION_PROJECTOR.json')
    assert x['horizontal36']['collision']==0 and x['vertical9']['collision']==3
    assert x['point_line_incidence']['rank']==9

def test_5677_connected_tower():
    x=load('PART_W33_PASS5677_CONNECTED_LEVI_VOLTAGE_TOWER.json')
    assert x['base']['beta1']==81
    lev=x['verified_levels']
    assert [r['vertices'] for r in lev[:5]]==[80,160,320,640,1280]
    assert [r['beta1'] for r in lev[:5]]==[81,161,321,641,1281]

def test_5678_spectral_bottleneck():
    x=load('PART_W33_PASS5678_VOLTAGE_TOWER_SPECTRUM_BOTTLENECK.json')
    assert x['verified_distinct_counts']['depth_0_to_4']==[5,13,29,61,125]
    for r in x['levels'][:-1]:
        assert r['next_lift']['cross_sheet_edges']==2
        assert r['next_lift']['next_combinatorial_gap'] <= r['next_lift']['cheeger_easy_upper_bound']+1e-9

def test_5679_real_imag_parent():
    x=load('PART_W33_PASS5679_SECTION_PARENT_REAL_IMAG_FESHBACH.json')
    assert x['bare_distinct_poles']==15
    assert x['bare_poles_coincide_with_full_physical_energies'] is False
    assert x['schur_probe_max_relative_error']<1e-7

def test_5680_pfaffian_triviality():
    x=load('PART_W33_PASS5680_DECK16_CLASSD_PFAFFIAN_TRIVIALITY.json')
    signs={r['pfaffian_sign'] for r in x['signature_component_representatives']}
    assert signs=={-1}
    assert x['magnetic_pfaffian_exact'].startswith('-104976')

def test_5681_agl_no_bracket():
    x=load('PART_W33_PASS5681_AGL23_VERTICAL_1PLUS8_NO_GLUON_BRACKET.json')
    assert x['group']['order']==432 and x['V8']['irreducible'] is True
    assert x['cochain_complex']['cycle_space_dim']==28
    assert x['alternating_bracket_test']['Hom_G(Lambda2 V8,V8)_dimension']==0

def test_5682_causal_scaling():
    x=load('PART_W33_PASS5682_COVER_TOWER_CAUSAL_SPEED_SCALING.json')
    assert all(r['local_degree']==4 for r in x['verified_levels'])
    assert all(r['max_nearest_neighbor_graph_speed_edges_per_tick']==1 for r in x['verified_levels'])
    assert x['physical_conversion']=='c_n = ell_n/tau_n'
