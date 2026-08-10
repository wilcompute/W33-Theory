from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(name):return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))

def test_4697_three_39d_carriers():
    d=J('PART_W33_PASS4689_THREE_39D_MODULE_COMPARISON.json')
    assert d['canonical_cross_shell_split']['dimensions']==[15,24,39]
    c=d['equivariant_comparison']
    assert c['Hom_Hcross_to_Cap_dimension']==2
    assert c['ranks_of_three_nonzero_maps_Hcross_to_Cap']==[14,14,14]
    assert c['Hom_Cap_to_Hcross_dimension']==2
    assert c['ranks_of_three_nonzero_maps_Cap_to_Hcross']==[1,1,1]

def test_4698_full_affine_sextet():
    d=J('PART_W33_PASS4690_FULL_SEXTET_AFFINE_GROUP.json')
    assert d['sextet_stabilizer']['order']==138240
    assert d['translation_subgroup']['order']==64
    assert d['translation_subgroup']['structure']=='C2^6'
    assert d['translation_subgroup']['regular_on_transversals'] is True
    assert d['point_stabilizer']['order']==2160
    assert d['point_stabilizer']['tetrad_image_order']==720
    assert d['point_stabilizer']['tetrad_kernel_order']==3
    assert d['point_stabilizer']['nonzero_translation_orbits']==[18,45]

def test_4699_explicit_leech_neighbor():
    d=J('PART_W33_PASS4691_EXPLICIT_LEECH_TWO_NEIGHBOR.json')
    b=d['explicit_basis'];r=d['rootlessness']
    assert b['integer_numerator_determinant']==2**36
    assert b['gram_determinant']==1 and b['integral_even_gram'] is True
    assert r['all_old_roots_have_odd_v_pairing'] is True
    assert r['new_coset_all_24_numerators_odd'] is True
    assert r['minimum_norm']==4
    assert d['sextet_weld']['24_distinguished_coordinate_neighbors_in_one_sextet_stabilizer_orbit'] is True

def test_4700_c8_formulas_and_same_parameter_obstruction():
    d=J('PART_W33_PASS4692_C8_CLOSED_LOCAL_MASS_FORMULAS.json')
    a={x['geometry']:x for x in d['anchors']}
    assert a['W33']['coefficients']==[712,180]
    assert a['dual W33 = Q(4,3)']['coefficients']==[728,252]
    assert (a['W33']['s'],a['W33']['t'])==(3,3)
    assert (a['dual W33 = Q(4,3)']['s'],a['dual W33 = Q(4,3)']['t'])==(3,3)
    assert (a['W33']['rho'],a['W33']['sigma'],a['W33']['tau'])==(0,16,1)
    assert (a['dual W33 = Q(4,3)']['rho'],a['dual W33 = Q(4,3)']['sigma'],a['dual W33 = Q(4,3)']['tau'])==(4,0,3)

def test_4701_support12_exact_checksum():
    d=J('PART_W33_PASS4693_SUPPORT12_TRANSITIVITY_EXACT.json')
    assert d['transitivity_reduction']['fixed_point_subsets']==math.comb(39,11)==1676056044
    assert d['subsets']==math.comb(40,12)==5586853480
    assert sum(d['spectrum'].values())==5586853480
    assert len(d['spectrum'])==151
    assert (d['minimum_weight'],d['minimum_count'])==(608,1620)
    assert (d['maximum_weight'],d['maximum_count'])==(990,4320)

def test_4702_affine_u6_nogo():
    d=J('PART_W33_PASS4694_GOLAY_AFFINE_U6_FORM_NOGO.json')
    assert d['K_order']==2160
    assert d['invariant_quadratic_space_dimension']==0
    assert d['invariant_bilinear_space_dimension']==0

def test_4703_thickening_shell():
    d=J('PART_W33_PASS4695_SUPPORT12_MINIMA_APARTMENT_THICKENINGS.json')
    assert d['objects']=={'apartments':1620,'support12_minima':1620,'thickenings_distinct':1620}
    t=d['corner_star_thickening']
    assert (t['size'],t['extra_lines_per_corner'],t['apartment_code_weight'])==(12,2,608)
    assert d['intrinsic_inverse']['unique'] is True

def test_4704_even_apartment_subcode():
    d=J('PART_W33_PASS4696_THICKENING_SPAN_EVEN_APARTMENT_SUBCODE.json')
    assert d['coefficient_space']['thickening_mask_rank']==39
    c=d['image_subcode']
    assert c['dimension']==38 and c['parameters']=='[1620,38,270]'
    assert c['minimum_weight']==270 and c['minimum_words']==240
