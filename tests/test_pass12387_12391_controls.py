from pathlib import Path
import sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import w33_pass12388_12391_constructive_controls as p

def test_complex_reflection():
 rng=np.random.default_rng(4)
 x=rng.normal(size=11)+1j*rng.normal(size=11);x/=np.linalg.norm(x)
 y=rng.normal(size=11)+1j*rng.normal(size=11);y/=np.linalg.norm(y)
 v=x-y;H=np.eye(11)-np.outer(v,v.conj())/np.vdot(v,x)
 assert np.max(abs(H@x-y))<1e-13
 assert np.max(abs(H.conj().T@H-np.eye(11)))<1e-13

def test_overlap_spectrum_and_relation():
 rows=p.overlap()['samples'];assert max(x['GW_residual'] for x in rows)<1e-12
 assert rows[0]['overlap_smallest_singular']<1e-12
 assert all(x['overlap_smallest_singular']>1 for x in rows[1:16])

def test_preparation_and_invalid_extension():
 r=p.preparation();assert r['embedding_error']<1e-12 and r['unitarity_error']<1e-12
 assert len(r['rank_one_reflections'])==27
 c=p.ggso_negative();assert c['first_counterexample']['candidate_product_sign']!=c['first_counterexample']['required_sign']
