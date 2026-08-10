from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
def read(name): return json.loads((DATA/name).read_text(encoding="utf-8"))
def summary(): return read('w33_pass1320_1324_transport_linking.json')
def p1320(): return read('w33_pass1320_six_channel_diagonalization.json')['pass1320_six_channel_diagonalization']
def p1322(): return read('w33_pass1322_species20_hashimoto_dynamics.json')['pass1322_species20_hashimoto_dynamics']
def p1324(): return read('w33_pass1324_manuscript_ledger_promotion.json')['pass1324_manuscript_ledger_promotion']
def p1321():
 d=read('w33_pass1321_full_hecke_matrix_units.json')['pass1321_full_hecke_matrix_units']; d['blocks']={n:read(f)['block'] for n,f in d['block_files'].items()}; return d
def p1323():
 d=read('w33_pass1323_transport_composition_and_morita_context.json')['pass1323_transport_composition_and_morita_context'];
 d['x_side_products_in_hecke_matrix_units']=read(d['x_side_table'])['x_side_products_in_hecke_matrix_units']; d['y_side_products_in_species_refined_hashimoto_basis']=read(d['y_side_table'])['y_side_products_in_species_refined_hashimoto_basis']; return d

def test_release_status_and_global_checks():
 d=summary(); assert d['status']=='PASS'; assert all(d['checks'].values()); assert len(d['components'])==5

def test_six_channels_split_and_hashimoto_spectrum():
 d=p1320(); c=d['aligned_channels']; assert len(c)==6
 assert [sum(x['species']==s for x in c) for s in ('1','15a','20','60a')]==[1,1,3,1]
 assert d['projection_ranks']=={'1':1,'15a':1,'20':3,'60a':1}; assert d['hashimoto_eigenvalue_multiplicities_on_hom']=={'11':1,'-1':5}

def test_aligned_coefficients_and_singular_scales_are_frozen():
 c=p1320()['aligned_channels']; got=[(x['species'],x['copy'],x['orbital_coefficients'],x['squared_singular_scale']) for x in c]
 assert got==[('1',0,['1','1','1','1','1','1'],'207360'),('15a',0,['1','1','1','-3','-3','-3'],'41472'),('20',0,['1','-1','0','-3','0','3'],'20736'),('20',1,['1','-2','1','3','-3','0'],'31104'),('20',2,['1','1','-2','1','-2','1'],'20736'),('60a',0,['2','-1','-1','0','3','-3'],'10368')]

def test_full_hecke_matrix_unit_blocks():
 d=p1321(); assert d['wedderburn_dimension']==26; assert d['all_matrix_unit_laws_verified']; b=d['blocks']
 assert {n:b[n]['multiplicity'] for n in ('6','20','30','64')}=={'6':2,'20':3,'30':2,'64':2}; assert b['20']['splitter_eigenvalues']==['-6','2','10']; assert b['20']['primitive_idempotent_ranks']==[20,20,20]; assert len(b['20']['matrix_units'])==9

def test_species20_hashimoto_is_minus_identity_and_nonselecting():
 d=p1322(); assert d['minimal_polynomial']=='x+1'; assert d['characteristic_polynomial']=='(x+1)^20'; assert d['hashimoto_eigenvalue']==-1; assert not d['selects_unique_432_copy']; assert d['restricted_matrix']==[[-1 if i==j else 0 for j in range(20)] for i in range(20)]

def test_linking_algebra_and_morita_context():
 d=p1323(); assert d['x_side_product_span_dimension']==12; assert d['y_side_product_span_dimension']==4; assert len(d['x_side_products_in_hecke_matrix_units'])==36; assert len(d['y_side_products_in_species_refined_hashimoto_basis'])==36; assert d['linking_algebra_dimension']==28; assert d['linking_algebra']=='M_2(C) + M_2(C) + M_4(C) + M_2(C)'; assert d['linking_associativity_verified']; assert len(d['aligned_channel_partial_isometries'])==6

def test_both_manuscript_ledgers_contain_theorem_proof_and_retractions():
 d=p1324()
 for key in ('shared_insert','w33_paper_ledger','photonic_holonet_ledger'):
  text=(ROOT/d[key]).read_text(encoding="utf-8"); assert 'Exact transport/linking theorem' in text; assert 'Exact computational proof' in text; assert 'Historical claim & Active status & Exact replacement' in text; assert 'Hashimoto does not choose a preferred species-$20$ copy' in text
