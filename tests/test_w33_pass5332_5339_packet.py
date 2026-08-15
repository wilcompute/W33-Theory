from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT/'data'/name).read_text())

def test_pass5332_wedderburn():
    d=load('PART_W33_PASS5332_Q5_K0_ORBITAL_WEDDERBURN.json')
    assert d['orbital_rank']==21
    assert d['symmetric_orbitals']==11 and d['directed_orbitals']==10
    assert d['center_dimension']==7 and d['commutator_subspace_dimension']==14
    assert d['complex_wedderburn']=='C^4 + M2(C)^2 + M3(C)'
    assert sum(x['algebra_block_dimension'] for x in d['primitive_blocks'])==21
    assert sum(x['multiplicity']*x['irreducible_dimension'] for x in d['primitive_blocks'])==2340

def test_pass5333_base_fiber_firewall():
    d=load('PART_W33_PASS5333_Q5_K0_BASE_FIBER_CONSTITUENT.json')
    assert d['central_spectrum_on_base_fiber_space']=={'9878':1,'128':90,'998':65}
    assert 'Do NOT identify' in d['modular_firewall']

def test_pass5334_rank_complement():
    d=load('PART_W33_PASS5334_ALLODD_CHARACTERISTIC_RANK_COMPLEMENT.json')
    assert d['q5_characteristic_flip']=={'rank_Q':91,'nullity_Q':65,'rank_F2':65,'nullity_F2':91}
    assert d['anchors_rank2_equals_g']['q13']==1105

def test_pass5335_kernel_linecode():
    d=load('PART_W33_PASS5335_ALLODD_KERNEL_EQUALS_LINECODE_ANCHORS.json')
    for q in ('q3','q5','q7','q9','q11','q13'):
        a=d['verified_anchor_equality'][q]
        assert a['kernel_dimension']==a['W_line_code_dimension']

def test_pass5336_local_fiber():
    d=load('PART_W33_PASS5336_Q5_LOCAL_FIBER_A5_WEDDERBURN.json')
    assert d['local_fiber_size']==15 and d['pair_stabilizer_order']==4
    assert d['orbital_rank']==6 and d['center_dimension']==3 and d['commutator_dimension']==3
    assert d['permutation_module']=='15 = 1 + 4 + 2*5'

def test_pass5337_tower():
    d=load('PART_W33_PASS5337_Q5_K0_STABILIZER_TOWER.json')
    assert d['G_order']//d['point_stabilizer_order']==156
    assert d['point_stabilizer_order']//d['shell_label_stabilizer_order']==15
    assert d['G_order']//d['shell_label_stabilizer_order']==2340

def test_pass5338_branching():
    d=load('PART_W33_PASS5338_Q5_K0_INDUCED_BRANCHING.json')
    assert d['point_induction']=='Ind_P^G(1) = 1 + 90 + 65_a'
    assert d['four_induction']=='Ind_P^G(4) = 104 + 520'
    assert d['five_induction']=='Ind_P^G(5) = 90 + 65_b + 625'

def test_packet_frontier_firewalls():
    d=load('PART_W33_PASS5332_5339_RESULTS.json')
    assert d['range']==[5332,5339]
    assert 'OPEN' in d['frontier']['q11_footprint_distance']
    assert 'OPEN' in d['frontier']['hoffman_shortening']
    assert 'OPEN' in d['frontier']['all_odd_rank']
