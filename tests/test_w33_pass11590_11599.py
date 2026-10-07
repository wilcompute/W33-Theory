import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

def load(name): return json.loads((DATA/name).read_text())

def test_family_shell():
 d=load('PART_W33_PASS11590_E8_THREE_SPIN10_FAMILIES.json')
 assert d['chosen_shell_D5_content']=={'Spin10_16':48,'Spin10_10':30,'Spin10_1':3}
 assert d['modules_are_inequivalent']

def test_hesse_yukawa():
 d=load('PART_W33_PASS11591_SPIN10_DELTA54_HESSE_YUKAWA.json')
 assert d['symmetric_family_tensor_dimension']==2
 assert 'a**3' in d['determinant']

def test_q6_overlap():
 d=load('PART_W33_PASS11592_Q6_OVERLAP_ADMISSIBILITY.json')
 assert d['scan'][-1]['index']==-36 and d['scan'][-1]['gap']>0.08

def test_selector_neutrino_coupling():
 s=load('PART_W33_PASS11593_UNIQUE_WEYL_SELECTOR.json')
 n=load('PART_W33_PASS11595_NEUTRINO_MAJORANA_CHANNEL.json')
 c=load('PART_W33_PASS11596_SPIN10_COUPLING_NORMALIZATION.json')
 assert s['full_Dirac_commutant_dim']==2
 assert n['required_scalar_vev_charges']=={'qBL':-6,'r':2,'sixY':0}
 assert c['TrY2_over_T2']=='5/3'

def test_gravity_firewall():
 d=load('PART_W33_PASS11594_REFINED_GRAVITY_FIREWALL.json')
 assert d['status'].startswith('FIREWALL_')
 assert len(d['rows'])==3

def test_flavor_breaking_and_clock():
 f=load('PART_W33_PASS11597_FAMILY_CLIFFORD_BREAKING.json')
 c=load('PART_W33_PASS11598_CLOCK_FLOQUET_CHIRALITY.json')
 assert (f['Delta54_invariant_dimension'],f['Clifford648_invariant_dimension'])==(2,0)
 assert c['G4_equals_minus_identity_error']<1e-10

def test_synthesis():
 d=load('PART_W33_PASS11590_11599_FAMILIES_FLAVOR_CHIRALITY_GRAVITY.json')
 assert d['status']=='PASS_WITH_CHIRALITY_AND_GRAVITY_FIREWALLS'
 assert d['11599']['three_family_matter'].startswith('one selected E8')
