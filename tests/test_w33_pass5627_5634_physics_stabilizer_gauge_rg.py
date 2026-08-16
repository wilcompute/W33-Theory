from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_5627_signed_stabilizer_no_go():
    x=load('PART_W33_PASS5627_DECK_STABILIZER_SPINOR_NO_GO.json')
    assert x['PSp43_order']==25920 and x['PSp_Segre_stabilizer_order']==48
    assert x['Sp43_order']==51840 and x['vector_Segre_stabilizer_order']==96
    assert x['central_minus_I_action']=='-I_16' and x['signed_character_self_inner_product']==8

def test_5628_gauge_two_coupling():
    x=load('PART_W33_PASS5628_E6_GAUGE_ACTION_TWO_COUPLING_NO_GO.json')
    assert x['horizontal_supports']==36 and x['vertical_supports']==9
    assert 'g_V=0' in x['no_go']

def test_5629_cover_tower_disconnects():
    x=load('PART_W33_PASS5629_CONNECTED_COVER_TOWER_OBSTRUCTION.json')
    assert x['level1']['connected'] is True
    assert x['level2_naive_C2']['components']==2
    assert x['level1']['distinct_adjacency_eigenvalues']==x['level2_naive_C2']['distinct_adjacency_eigenvalues']

def test_5630_ratio_not_protected():
    x=load('PART_W33_PASS5630_DECK_BDG_COMMUTANT_MASS_RATIO.json')
    assert x['complex_commutant_dimension']==8
    assert x['real_skew_commutant_dimension']==4
    assert abs(x['explicit_perturbation']['mass_ratio']-2)>1e-3

def test_5631_fixed_line_maps_to_average_conditionally():
    x=load('PART_W33_PASS5631_Q5_FIXED_LINE_CROSSQ_MODULE_GATE.json')
    assert 'sum of the 12 q3 orbit basis vectors' in x['only_possible_q3_image_under_degree12_intertwiner']
    assert x['direct_action_gate'] in {'PENDING_DIRECT_GAP_CONJUGATOR','DIRECT_MOVING12_CONJUGACY_CONFIRMED','DIRECT_MOVING12_CONJUGACY_REFUTED'}

def test_5632_no_equivariant_TR():
    x=load('PART_W33_PASS5632_PIN_BDG_SPIN_STATISTICS_NO_GO.json')
    assert x['joint_nullity']==0 and x['K_squared']==1

def test_5633_cochain_degree():
    x=load('PART_W33_PASS5633_BAD9_GAUGE_GENERATOR_NOT_BOSON.json')
    assert x['AG23']['sites']==9 and x['AG23']['one_skeleton_edges']==36
    assert x['gauge_cochains']['incidence_rank']==8 and x['gauge_cochains']['cycle_space_dimension']==28

def test_5634_sheet_feshbach():
    x=load('PART_W33_PASS5634_SHEET_DECIMATION_RESOLVENT_RG.json')
    assert x['A_B_commutator_max_abs']>1
    assert len(x['one_sheet_distinct_energies'])==15
    assert len(x['E0_effective_distinct_levels'])==16

def test_frozen_summary_boundary():
    x=load('PART_W33_PASS5627_5634_PHYSICS_STABILIZER_GAUGE_RG_SUMMARY.json')
    assert x['pass_range']==[5627,5634]
    assert 'spin-statistics' in x['boundary'] and 'Standard Model mass prediction' in x['boundary']
