import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name): return json.loads((ROOT/'data'/name).read_text())

def test_pass4857_4864_cross_certificates():
    a=load('PART_W33_PASS4857_RATIONAL_ORBITAL_BLOCKS.json')
    b=load('PART_W33_PASS4858_TERNARY_TEN_MODULE.json')
    c=load('PART_W33_PASS4859_SWITCHING_ENUMERATOR_RADIUS.json')
    d=load('PART_W33_PASS4860_INTRINSIC_STEINER_SIGNING.json')
    e=load('PART_W33_PASS4861_PORT_MATCHING_SYMMETRY_BREAK.json')
    f=load('PART_W33_PASS4862_STEINER_TWO_GRAPH_CODE.json')
    g=load('PART_W33_PASS4863_4864_O5_ADJOINT_HOMOLOGY.json')
    old=load('PART_W33_PASS4849_4852_4854_4855_4856_E6_KERNEL_CODE.json')
    assert a['PGSp']['rational_Wedderburn']=='Q^6 x M2(Q)^4 x M3(Q)^3'
    assert 'M2(K)' in a['PSp']['rational_Wedderburn']
    assert b['quotient_dimension_F3']==10 and b['PSp']['absolutely_irreducible']
    assert g['exterior_square_intertwiner']['unique_nonzero_intertwiner_rank']==10
    assert g['Lie_algebra']['center_dimension']==0 and g['Lie_algebra']['derived_dimension']==10
    assert c['nontrivial_switching_coset']['size']==2**35
    assert sum(c['nontrivial_switching_coset']['complete_weight_enumerator'].values())==2**35
    assert c['covering_radius']['lower_bound']==124 and c['covering_radius']['upper_bound']==179
    assert not c['covering_radius']['exact_closed']
    assert d['Steiner_trihedral_pairs']==120 and d['triangle_triple_intersection_profile']=={'0':120,'4':1080}
    assert f['Steiner_parity']['odd_triangles']==120 and f['dual']['minimum_checks']==1080
    assert f['triangle_parity_map']['rank_F2']==325
    assert old['kernel_code']['parameters']=='[360,36,20]_2'
    assert e['local_stabilizer_of_full_matching']==1 and e['choices_per_point']==6
    assert e['global_stabilizer']['port_matching_plus_global_chirality'].startswith('PSp(4,3)')
