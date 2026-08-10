from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))

def test_pass1300_sign_twist_intertwiner():
    d=load('w33_pass1300_81_sign_twist_intertwiner.json')
    assert d['status']=='PASS'
    assert d['rank_plus_to_E4']==d['rank_minus_to_E4']==81
    assert d['target_scalar_plus']=='2' and d['target_scalar_minus']=='1'
    assert d['character_twist']=={
        '81_minus_equals_81_plus_tensor_sign':True,
        'Hom_W_untwisted':0,
        'Hom_W_twisted':1,
        'Hom_PSp_restriction':1,
    }

def test_pass1301_matrix_units():
    d=load('w33_pass1301_m3_m21_matrix_units.json')
    assert d['status']=='PASS'
    assert d['M3']['multiplicity']==3
    assert d['M3']['projector_denominator']==716800
    assert d['M3']['matrix_unit_laws_verified']
    assert d['M21']['multiplicity']==21
    assert d['M21']['domain_multiplicity_22']==22
    assert d['M21']['cubic_image_copy']=='orbit_08_size_240_20copy_1'
    assert len(d['M21']['kernel_copy_labels'])==21
    assert d['M21']['matrix_units']['count']==21**2
    assert len(d['M21']['matrix_units']['sha256'])==64
    assert d['M21']['cubic_column_sums']=={'0':2000,'6':240}

def test_pass1302_hecke_equality():
    d=load('w33_pass1302_a5_s5_hecke_equality.json')
    assert d['status']=='PASS'
    assert d['rank_W_S5']==d['rank_PSp_A5']==26
    assert d['same_orbitals']
    assert sum(d['subdegrees'])==432
    assert d['noncommutativity_witness']['p_ij_k']!=d['noncommutativity_witness']['p_ji_k']

def test_pass1303_literal_cycle_frontier():
    d=load('w33_pass1303_literal_cycle_orbits_7_8.json')
    assert d['status']=='PASS'
    seven=d['lengths']['7']; eight=d['lengths']['8']
    assert seven['primitive_oriented_rotation_classes']==2739840
    assert seven['PSp(4,3)']['orbit_count']==108
    assert seven['W(E6)']['orbit_count']==57
    assert eight['primitive_oriented_rotation_classes']==26750160
    assert eight['PSp(4,3)']['orbit_count']==1066
    assert eight['W(E6)']['orbit_count']==565
    assert seven['PSp(4,3)']['record_count']==108 and seven['W(E6)']['record_count']==57
    assert eight['PSp(4,3)']['record_count']==1066 and eight['W(E6)']['record_count']==565
    assert len(d['records_sha256'])==64
    assert sum(int(k)*v for k,v in seven['W(E6)']['orbit_size_distribution'].items())==2739840
    assert sum(int(k)*v for k,v in eight['W(E6)']['orbit_size_distribution'].items())==26750160

def test_pass1304_triality_boundary():
    d=load('w33_pass1304_a2_normalizer_triality.json')
    assert d['status']=='PASS'
    assert d['centralizer_product_subgroup']['order']==311040
    assert d['full_A2_subsystem_normalizer']['order']==622080
    assert d['full_A2_subsystem_normalizer']['index_in_W(E8)']==1120
    assert d['three_432_carriers']['S3_image_order']==6
    assert d['three_432_carriers']['point_stabilizer_order']==2
    assert d['three_432_carriers']['orientation_preserving_C3_is_free_transitive']
    assert d['six_27_carriers']['verdict']=='regular S3 torsor'
    assert d['six_27_carriers']['stabilizer_order']==1
