#!/usr/bin/env python3
"""Exact minimally 16-effect Witting supported informationally complete POVM."""
from fractions import Fraction as F
import numpy as np
import sympy as sp
from collections import Counter
import toe_20261122_witting_qutrit_sic_mub30 as G
import toe_20261122_witting_minimal_lie_control as L
from toe_20261122_round6_minimal_ic import get_mats
S=(1,2,5,6,7,8,9,16,17,22,28,29,30,31,34,35)
HEAVY=(6,9,17,30)
WEIGHTS={i:(F(2,5) if i in HEAVY else F(1,5)) for i in S}

def proof():
  Ps=[G.P_of(r) for r in G.W.all_rays()]
  target=tuple(tuple(G.ONE if i==j else G.ZERO for j in range(4)) for i in range(4))
  M=tuple(tuple(G.sumz([G.W.scale(Ps[k][i][j],WEIGHTS[k]) for k in S]) for j in range(4)) for i in range(4))
  assert M==target,('Failed exact identity',M)
  rank=[]
  for p in L.PRIMES:
    mats=[]
    for v,vc in L.all_witting_rays(p):
      norm=sum(int(a)*int(b) for a,b in zip(v,vc))%p
      mats.append((np.array(L.outer(v,vc,p),dtype=np.int64)*pow(norm,-1,p)%p).ravel().tolist())
    r=L.modular_rank([mats[i] for i in S],p);rank.append((p,r))
    assert r==16,(p,r)
  # Completely independent rational Hilbert-Schmidt Gram determinant.
  r=G.W.all_rays()
  rat=lambda q:sp.Rational(q.numerator,q.denominator)
  Gram=sp.Matrix(16,16,lambda i,j:
      rat(G.abs2(G.dots(r[S[i]],r[S[j]]))) /
      (rat(G.dots(r[S[i]],r[S[i]])[0])*rat(G.dots(r[S[j]],r[S[j]])[0])))
  det=Gram.det()
  assert det==sp.Rational(25,3**10),(det,Gram)
  hist={str(k):v for k,v in Counter(list(Gram)).items()}
  assert hist=={'1':16,'0':90,'1/3':150}
  P,A,b=get_mats()
  weights=np.array([float(WEIGHTS[k]) for k in S]);assert max(abs(A[:,list(S)]@weights-b))<1e-12
  M=np.column_stack([weights[j]*P[k].ravel() for j,k in enumerate(S)])
  frame=M@M.conj().T;ev=np.linalg.eigvalsh(frame);assert ev.min()>1e-12
  return {'indices':S,'heavy_indices':HEAVY,'weights':{str(k):str(WEIGHTS[k]) for k in S},'exact_normalization':True,'finite_field_ranks':rank,'exact_projector_Gram_determinant':str(det),'exact_Gram_entry_histogram':hist,'frame_eigenvalues':ev.tolist(),'condition':float(ev.max()/ev.min())}
if __name__=='__main__':print(proof())
