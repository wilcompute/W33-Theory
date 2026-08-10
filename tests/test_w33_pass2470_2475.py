import importlib.util,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):
 p=ROOT/'data'/name;d=json.loads(p.read_text(encoding="utf-8"));x=dict(d);x.pop('sha256_without_hash_field',None);assert hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()==d['sha256_without_hash_field'];return d
def test_u6_union():
 d=load('w33_pass2470_multishard_u6_union_engine.json');assert d['runs']['8']['unique_representatives']==16762010;assert d['runs']['8']['collision_unmarked_union_representatives']==11354885
def test_signature_radius4():
 d=load('w33_pass2471_radius4_signature_trade_obstruction.json');assert len(d['candidate_results'])==14;assert all(r['zero_pairs'] for r in d['candidate_results'])
def test_rank9():
 d=load('w33_pass2472_rank9_scheme_decode.json');assert d['multiplicities']==[1,15,15,20,162,135,108,24,60];assert not d['p_polynomial_candidates'] and not d['q_polynomial_candidates']
def test_tomotope():
 d=load('w33_pass2473_tomotope_rank_colour_quotient_obstruction.json');assert d['local_elementary_event_change_graph']['degree_histogram']=={'2':96,'5':96};assert d['checks']['no_rank_union_match']
def test_normalizer():
 d=load('w33_pass2474_f20_lifted_normalizer_hom.json');assert d['sylow5_normalizer']['lifted_group']=='5:8';assert d['lifted_normalizer_action']['Hom_5colon8_dimension']==0
