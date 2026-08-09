import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))

def test_pass4544_upper_lattice_boundary():
    d=load('PART_W33_PASS4544_DUAL_MIDDLE_MODULE_LATTICE.json')
    assert d['middle_module']['dimension']==364
    assert d['upper_lattice']['number_of_S358']==3
    assert d['upper_lattice']['common_K352']==352
    assert d['top_quotient']['structure'].startswith('U6 direct-sum U6')
    assert d['top_quotient']['proper_nonzero_submodules']==3
    assert d['K352_over_S330']['structure']=='V8 direct-sum V14'
    assert d['K256_frontier']['unique_S186_dimension']==186
    assert d['K256_frontier']['unique_S250_dimension']==250
    assert d['K256_frontier']['open']

def test_pass4545_4549_cubic_intertwiner():
    d=load('PART_W33_PASS4545_4549_SCHLAFLI_DOUBLE_SIX_INTERTWINER.json')
    assert d['incidence']['shape']==[27,36]
    assert d['incidence']['rank_over_Q']==21
    assert d['matrix_identities']['RRt']=='10 I27 + 2 A27 + 6 J27'
    assert d['matrix_identities']['RtR']=='6 I36 - 2 A36 + 6 J36'
    assert d['rational_constituents']['R_survives']=='1 + 20'

def test_pass4546_enumerator_remains_fail_closed():
    d=load('PART_W33_PASS4546_ORBIT_NATIVE_ENUMERATOR_ENGINE.json')
    assert d['status']=='RESUMABLE_FRONTIER'
    assert d['complement_assembly']['total_codeword_orbits']==10789604
    assert d['complement_assembly']['support20_PGSp_plus_complement_orbits']==1347360
    assert 'FULL_RUN_OPEN' in d['boundary']

def test_pass4547_4550_q53_fan_code():
    d=load('PART_W33_PASS4547_4550_Q53_FAN_JOHNSON_CODE.json')
    assert d['local_fan_code']['dimension']==9
    assert d['local_fan_code']['minimum_distance']==56
    assert d['local_fan_code']['weight_enumerator']=={'0':1,'56':10,'64':45,'96':210,'104':120,'120':126}
    assert d['prism_shell']['distance64_graph']=='Johnson J(10,3)'
    assert d['prism_shell']['global_prisms']==544320

def test_pass4548_c8_selects_apartments():
    d=load('PART_W33_PASS4548_C7_C8_HIGHER_BODY_TOMOGRAPHY.json')
    assert d['C7_degree3']['nonzero_support_orbits'][1]['coefficient']==204
    assert '1620' in d['C8_degree4']['apartment_theorem']
    assert '712' in d['C8_degree4']['apartment_theorem']
    assert d['C8_degree4']['PSp_orbits']==10

def test_pass4551_zeta_reconstructs_code_matrix():
    d=load('PART_W33_PASS4551_ZETA_TO_APARTMENT_CODE.json')
    assert d['C8_selector']['apartment_coefficient']==712
    assert d['C8_selector']['selected_supports']==1620
    assert d['reconstructed_matrix']['shape']==[40,1620]
    assert d['reconstructed_matrix']['rank_F2']==39
    assert d['reconstructed_matrix']['Gram_mod2'].startswith('A_*')
