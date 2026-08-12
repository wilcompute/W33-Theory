import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_5000_radius_barrier():
    x=load('PART_W33_PASS5000_OCTAHEDRAL_RADIUS_ILP_BARRIER.json')
    assert x['status']=='FEASIBLE_LOCAL_RELAXATION_GLOBAL_CLOSURE_REQUIRED'
    assert x['octahedral_local_ILP_witness']['cells']==270
    assert x['octahedral_local_ILP_witness']['T3']==-1080
    assert x['global_character_cut']['local_witness_violates_global_cut']
    assert x['covering_radius']=={'proved_interval':[134,173],'improved_here':False}

def test_5001_kernel_is_tritangent_v20():
    x=load('PART_W33_PASS5001_KERNEL20_TRITANGENT_V20_INTERTWINER.json')
    assert x['kernel_dimension']==20
    assert x['tritangent_selector_code']['rank']==20
    assert x['intertwiner']['Hom_dimension']==1
    assert x['intertwiner']['unique_nonzero_intertwiner_rank']==20
    assert x['intertwiner']['outer_PGSp_generator_also_intertwined']

def test_5002_corrected_reader_distance():
    x=load('PART_W33_PASS5002_CORRECTED_85_READER_ERASURE_DISTANCE.json')
    assert x['exact_global_erasure_distance']==6
    assert x['guaranteed_erasure_tolerance']==5
    assert x['minimum_raw_dependencies']['support']==6
    assert x['minimum_raw_dependencies']['count']==240
    assert not x['mixed_support8']['exist']
    old=load('PART_W33_PASS4993_EXACT_85_READER_ERASURE_DISTANCE.json')
    assert old['status']=='CORRECTED_SUPERSEDED_BY_PASS5002'
    assert old['correction']['exact_global_erasure_distance']==6

def test_5003_real_oct_module():
    x=load('PART_W33_PASS5003_OCTAHEDRON_REAL_MODULE_DECOMPOSITION.json')
    assert x['edge_frame']=={'GF2_rank':90,'active_real_spectral_space':'1 + 20 + 15 + 84','real_rank':120}
    assert x['share3_graph_spectrum']=={'-4':150,'2':84,'8':15,'14':20,'32':1}
    assert x['natural_spread_carrier_map']['real_rank']==36
    assert x['natural_spread_carrier_map']['spectral_projection_ranks']=={'-4':0,'2':0,'8':15,'14':20,'32':1}

def test_5004_c3_origin_nogo():
    x=load('PART_W33_PASS5004_C3_TORSOR_ORIGIN_NOGO.json')
    assert not x['equivariant_origin_selector_exists']
    assert x['PSp_action']['image']=='C3 regular/transitive'
    assert x['PGSp_action']['image']=='S3 transitive'
    assert x['PSp_action']['kernel_order']==x['PGSp_action']['kernel_order']==54

def test_5005_nonsplit():
    x=load('PART_W33_PASS5005_NONSPLIT_20_30_10_EXTENSION.json')
    assert not x['PSp_equivariant_section_exists']
    assert not x['full_PGSp_section_exists']
    assert x['section_system_variables']==300
    assert x['sequence'].startswith('0 -> V20_trit')

def test_5006_binary_oct_extension():
    x=load('PART_W33_PASS5006_OCTAHEDRON_BINARY_60_90_30_EXTENSION.json')
    assert x['binary_oct_frame']=={'rank':90,'shape':[270,360]}
    assert x['shared_line_projection']['image_rank']==30
    assert x['kernel_dimension']==60

def test_5007_minimum_failure_tight_frame():
    x=load('PART_W33_PASS5007_MINIMUM_COCIRCUIT_24_TIGHT_FRAME.json')
    assert x['support_size']==6 and x['distinct_supports']==240
    assert x['rank']==24 and x['line_reader_left_nullity']==24
    assert x['spans_entire_left_nullspace']
    assert x['frame_operator_spectrum']=={'0':16,'60':24}

def test_firewall_knows_reader_correction():
    x=load('PART_W33_PASS4996_STALE_CLAIM_FIREWALL.json')
    assert x['status']=='PASS' and x['violations']==[]
    assert 'reader_global_distance8' in x['rules']
    auth=x['authoritative_replacements']['data/PART_W33_PASS5002_CORRECTED_85_READER_ERASURE_DISTANCE.json']
    assert all(auth.values())
