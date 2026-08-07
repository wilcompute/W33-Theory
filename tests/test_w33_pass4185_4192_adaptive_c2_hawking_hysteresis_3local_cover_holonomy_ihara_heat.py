from importlib.util import module_from_spec,spec_from_file_location
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'analysis/w33_pass4185_4192_adaptive_c2_hawking_hysteresis_3local_cover_holonomy_ihara_heat.py'
s=spec_from_file_location('p4185',P); m=module_from_spec(s); s.loader.exec_module(m)

def test_all(): assert m.verify()
def test_semantic_hash(): assert m.semantic_hash(m.CERT)==m.CERT['semantic_sha256']
def test_adaptive_c2():
    p=m.CERT['pass4185_adaptive_c2']; assert round(m.c2_midpoint(7))==1; assert abs(m.c2_midpoint(9)-1)<.05; assert p['five_percent_samples']==6561
def test_hawking_surfaces():
    p=m.CERT['pass4186_hawking_critical_surface']; r=m.r_of_omega(.3); assert abs((__import__('math').exp(2*r)-1)/2-p['omega_table']['0.3']['n_ent'])<1e-14
def test_hysteresis():
    p=m.CERT['pass4187_hysteretic_backreaction']; assert len(p['g0p5_roots'])==3; assert [x['stable'] for x in p['g0p5_roots']]==[True,False,True]
def test_exact_three_local_clock():
    p=m.CERT['pass4188_exact_3local_clock']; assert p['max_locality']==3 and p['expanded_history_states']==49 and p['total_auxiliary_ancillas']==96
def test_high_girth_cover():
    p=m.CERT['pass4189_high_girth_levi_cover']; assert p['certified_girth_lower_bound']==14 and p['zero_voltage_cycles']=={'8':0,'10':0,'12':0}
def test_holonomy_and_ihara():
    assert m.CERT['pass4190_holonomic_universality']['closure']=='SU(2)'; assert m.CERT['pass4191_ihara_factorization']['ramanujan']
def test_heat_dimension_falsifier(): assert m.CERT['pass4192_heat_dimension']['maximum_spectral_dimension']<4
