import json
from pathlib import Path

R=Path(__file__).resolve().parents[1]

def load(name):return json.loads((R/'data'/name).read_text())

def test_pass5348_5355_consolidated_frontier():
    d=load('PART_W33_PASS5348_5355_RESULTS.json')
    assert d['5355']['footprint_code']=='[7381,671,121]_2'
    assert d['5355']['minimum_r_over_lambda']==120
    assert d['5354b']['support_graph']=='K10,10 + C10 + (C5+C5)'
    assert d['5351_5352']['direction_split'].startswith('9+6')
    assert d['5348c']['identity']=='Hull(C_F)=Row_F2(A_NO5+5)'
    assert 'PENDING' in d['status']

def test_q11_moment_arithmetic():
    d=load('PART_W33_PASS5355_Q11_DUAL20_ORBIT_MOMENT.json')
    vals={int(k):int(v) for k,v in d['nontrivial_orbital_valencies'].items()}
    cnt={int(k):int(v) for k,v in d['seed_pair_counts'].items()}
    assert sum(cnt.values())==190
    ratios={k:20*vals[k]//(2*cnt[k]) for k in cnt}
    assert ratios=={0:660,1:440,3:1320,4:2640,5:120,9:880}
    assert min(ratios.values())==120

def test_q11_dual20_certificate_shape():
    d=load('PART_W33_PASS5354B_Q11_MOD4_TWOFACTOR_CAYLEY_SEARCH.json')
    assert len(d['selected_carriers'])==20
    assert len(set(d['selected_carriers']))==20
    assert d['carrier_graph']['edges']==120
    assert d['carrier_graph']['degree']==12
    assert d['point_multiplicity_histogram']=={'0':1224,'2':240}

def test_allodd_homology_and_pauli_firewalls():
    h=load('PART_W33_PASS5350B_ALLODD_FOOTPRINT_CHAIN_COMPLEX.json')
    assert h['point_homology']=='H_V=ker(F^T|V0)/im(F)=C_W/C_W^perp, dimension q^2+1.'
    p=load('PART_W33_PASS5351_5352_HOFFMAN_PAULI_LATIN_SYMPLECTIC_SPREAD.json')
    assert p['latin_spread_isotropic_lines']==3
    assert p['latin_spread_nonisotropic_lines']==2
    assert 'no physical' in p['boundary'].lower()

def test_manifest_imports_packet():
    s=(R/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text()
    assert r'\input{analysis/PASS5348_5355_q11_homology_pauli_tightframe_hoffman_insert}%' in s
