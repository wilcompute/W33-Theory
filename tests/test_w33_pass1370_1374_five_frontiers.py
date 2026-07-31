from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'w33_pass1370_1374_five_frontiers.json'
EXPECTED='284d9d7f9462a83f0709734d48a3ccf3284da2cb6b5ede159da5c719b84332b9'

def load():
 raw=DATA.read_bytes(); assert hashlib.sha256(raw).hexdigest()==EXPECTED; return json.loads(raw)

def test_matrix_units():
 d=load()['pass1370_exact_rational_matrix_units']
 assert d['matrix_unit_count']==83 and d['block_count']==14
 assert [b['n'] for b in d['blocks']]==[1,1,1,1,1,1,1,2,2,3,3,3,4,5]
 assert sum(b['matrix_units'] for b in d['blocks'])==83

def test_stabilizer_structure():
 d=load()['pass1371_selector_stabilizer_structure']
 assert d['normal_3_type']=='elementary abelian C3^3'
 assert d['quotient_type']=='D8 x C2' and d['split_complement']
 assert d['action_decomposition']=='1 + 2 over F3'

def test_minimum_splitters():
 d=load()['pass1372_minimum_defect_splitters']
 assert d['ordered_orbital_pairs_tested']==128
 assert d['minimum_support_arbitrary']==540
 assert [[r['a'],r['b']] for r in d['minimum_arbitrary_pairs']]==[[18,63],[18,64]]

def test_modular_radicals():
 d=load()['pass1373_bad_characteristic_radicals']
 t=d['terwilliger_word_generated_reductions']; a=d['full_orbital_algebra']
 assert [t[str(p)]['reduced_algebra_dimension'] for p in (2,3,5)]==[42,54,74]
 assert t['2']['radical_power_dimensions']==[22,6,0]
 assert t['3']['radical_power_dimensions']==[48,36,22,13,4,0]
 assert a['2']['radical_power_dimensions']==[45,16,0]
 assert a['3']['radical_power_dimensions']==[72,49,27,14,4,0]
 assert t['5']['jacobson_radical_dimension']==a['5']['jacobson_radical_dimension']==0

def test_selector_levi_boundary():
 d=load()['pass1374_selector_levi_bimodule_boundary']
 assert d['cross_orbits']==4 and d['maximum_cross_map_rank']==40
 assert d['steinberg_81_channel_present'] is False
