from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'
def load(name):return json.loads((DATA/name).read_text())

def test_4940_radius_hardword():
    d=load('PART_W33_PASS4940_EXACT_HARDWORD_COVER_DISTANCE.json')
    assert d['cp_sat']['status']=='OPTIMAL'
    assert d['cp_sat']['objective_distance']==d['cp_sat']['best_bound']
    assert d['cp_sat']['objective_distance']>=124
    assert d['twist_cross_certificate']['g_x_equals_x_plus_sigma']
    assert d['covering_radius_update']['upper_bound']==179

def test_4941_quartic():
    d=load('PART_W33_PASS4941_QUARTIC_AMBIGUITY_CANCELLATION.json')
    assert d['quartic_operation']['homogeneous_degree']==4
    assert d['quartic_operation']['PGSp_outer_parity'].startswith('even')
    assert d['quartic_operation']['image_span_dimension']==10
    assert d['support_structure']['two_support_inputs_zero']
    assert d['support_structure']['fiber_constant_40_space_annihilated_by_each_quadratic_channel']

def test_4942_char3_degeneration():
    d=load('PART_W33_PASS4942_TRANSVERSE_CHAR3_DEGENERATION.json')
    c=d['characteristic_three']
    assert (c['N_rank'],c['N_square_zero'],c['image_dimension'],c['kernel_dimension'])==(40,True,40,80)
    assert c['R2_nilpotent_ranks']==[34,14,0]
    assert c['R2_Jordan_blocks']=={'size1':66,'size2':6,'size3':14}
    assert c['R3_nilpotent_rank']==39 and c['R3_square_zero']

def test_4943_s6_crosswalk():
    d=load('PART_W33_PASS4943_COMMON_S6_CARRIER_CROSSWALK.json')
    assert d['common_core']['order']==720
    assert d['marked_double_six_extension']['center_order']==2
    assert d['duad_syntheme_extension']['center_order']==1
    assert not d['crosswalk']['extends_to_order1440_groups']

def test_4944_rtl():
    d=load('PART_W33_PASS4944_PORT_SELECTOR_RTL.json')
    assert d['encoding']['independent_binary_selector_state_bits']==135
    assert d['encoding']['information_theoretic_global_minimum_bits_from_Pass4872']==117
    assert d['verification']['yosys_single_selector']['num_cells']>0
    assert d['verification']['yosys_45_parallel']['num_cells']>0

def test_4945_holonomy():
    d=load('PART_W33_PASS4945_STEINER_NONEDGE_S3_HOLONOMY.json')
    assert d['edges']==540
    assert d['fundamental_cycle_holonomy']['group_order']==6
    assert d['fundamental_cycle_holonomy']['all_six_permutations_seen']

def test_4946_dual_w33():
    d=load('PART_W33_PASS4946_MAXCUT_STEINER_DUAL_W33_INCIDENCE.json')
    assert d['shells']['maximum_cuts']==d['shells']['Steiner_triangles']==120
    assert d['cross_incidence']['identical_row_classes']==[40,3]
    assert d['cross_incidence']['identical_column_classes']==[40,3]
    assert d['quotient']['zero_matrix_row_weight']==d['quotient']['zero_matrix_column_weight']==4
    assert d['quotient']['point_collinearity']=='SRG(40,12,2,4)'
    assert d['quotient']['explicit_isomorphism_to_Pass4870_W33']

def test_4947_curvature():
    d=load('PART_W33_PASS4947_W33_TRIAD_CURVATURE.json')
    assert d['W33_independent_triads']==3240
    assert d['curvature']=={'flat_identity':1080,'order3':0,'reflection_transposition':2160}
    assert d['geometric_classification']['acentric_common_neighbors_0']==1080
    assert d['geometric_classification']['centric_common_neighbors_2']==2160
