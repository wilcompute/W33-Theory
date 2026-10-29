from pathlib import Path
import sys,json
from fractions import Fraction
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import w33_pass12392_12396_exact_controls as p
import w33_pass12396_clifford_seed as seed

def test_exact_certificate_via_rational_block_embedding():
 d=json.loads((p.ROOT/'data/w33_pass12392_12396_exact_controls.json').read_text())['exact_coercivity']
 A,B,X,Y=[np.array(d[k],dtype=object) for k in ['matrix_a','matrix_b','inverse_a','inverse_b']]
 S=np.block([[A,-B],[B,A-B]]);T=np.block([[X,-Y],[Y,X-Y]])
 den=d['matrix_denominator']*d['inverse_denominator'];E=S@T-den*np.eye(270,dtype=object)
 a,b=E[:135,:135],E[135:,:135]
 r=Fraction(max(sum(abs(int(x))+abs(int(y)) for x,y in zip(row,col)) for row,col in zip(a,b)),den)
 assert r==Fraction(d['residual_bound']) and r<1
 norm=Fraction(max(sum(abs(int(x))+abs(int(y)) for x,y in zip(row,col)) for row,col in zip(X,Y)),d['inverse_denominator'])
 assert (1-r)/norm==Fraction(d['certified_physical_eigenvalue_lower_bound'])

def test_native_gauge_covariance():
 r=p.native_overlap();assert r['GW_residual']<1e-12 and r['gauge_covariance_residual']<1e-12
 assert abs(r['index_trace'])<1e-10

def test_seed_and_cocycle_obstruction():
 r=seed.run();assert len(r['gates'])==16 and r['amplitude_error']<1e-14
 c=p.reciprocity_obstruction();assert c['left_exponent']!=c['right_exponent']
