"""Exact global quantitative affine coefficient bound of 160 W33 currents.

For w_e(q)=Ve.q+1/sqrt20, sum_e Ve=0,
sum_e w_e(q)^2=8+q^T S q, S=V^T V.
S spectrum: 0^2, (4-sqrt6)^24,4^30,(4+sqrt6)^24
on the 78-dimensional physical augmentation.
This is a coercive bound on affine coefficients, NOT a bound on H.
"""
from pathlib import Path
import json,sys
from fractions import Fraction as F
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as V
from w33_20261009_local_hormander_depth import rank_mod
def certificate():
  g=V.geometry()
  raw=np.rint(40*g['v']).astype(np.int64)
  assert np.array_equal(raw.sum(axis=0),np.zeros(80,dtype=np.int64))
  K=raw.T@raw
  assert K.shape==(80,80) and rank_mod(K)==78
  I=np.eye(80,dtype=np.int64)
  X=K-6400*I
  poly=K@X@(X@X-15360000*I)
  assert np.max(np.abs(poly))==0, np.max(np.abs(poly))
  ev=np.linalg.eigvalsh(K.astype(float)/1600.)
  target=np.array([0]*2+[4-np.sqrt(6)]*24+[4]*30+[4+np.sqrt(6)]*24)
  assert np.max(np.abs(ev-target))<3e-11
  a=1/np.sqrt(20)
  rs=np.random.default_rng(1337)
  cases=[]
  for scale in (0.,.25,1.,10.):
    q=rs.normal(size=80)*scale
    q=q-np.r_[np.full(40,q[:40].mean()),np.full(40,q[40:].mean())]
    w=(raw@q)/40+a
    norm=float(w@w)
    formula=float(8+q@K@q/1600)
    lower=float(8+(4-np.sqrt(6))*q@q)
    assert abs(norm-formula)<2e-10*max(1,norm)
    assert norm>=lower-1e-9*max(1,norm)
    cases.append(dict(qnorm=float(np.linalg.norm(q)),sum_w_square=norm,
       radial_lower=lower,largest_abs_affine=float(np.max(abs(w)))))
  return dict(status='PASS',integer_matrix_minimal_polynomial='K*(K-6400I)*((K-6400I)^2-15360000I)=0',
       raw_matrix_rank=78,eigenmultiplicities={'0':2,'4-sqrt6':24,'4':30,'4+sqrt6':24},
       affine_identity='sum_e (Ve.q+1/sqrt20)^2 = 8+q^T (V^T V)q',
       uniform_physical_78D_bound='>=8+(4-sqrt6)||q||^2',
       max_coefficient_lower='max_e |Ve.q+a| >=sqrt((8+(4-sqrt6)||q||^2)/160)',
       samples=cases,meaning='Uniform quantitative affine-coefficient nonvanishing and growth at infinity. First-order transport current frame may be pointwise rank-deficient, so this is NOT a lower spectral bound for the sum of squared quantum currents.')
if __name__=='__main__':
  d=certificate();(ROOT/'data/w33_20261009_affine_coefficient_coercivity.json').write_text(json.dumps(d,indent=2)+'\n')
  print('COEFF SPECTRUM',d['eigenmultiplicities'],d['uniform_physical_78D_bound'])
