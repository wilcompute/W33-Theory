"""Rigorous negative result: NO uniform 78-dimensional elliptic lower bound
H >= c*P^2-C with c>0 for the actual Weyl-ordered W33 160-current H.

Construct a normalized highly oscillatory Gaussian packet localized at
the Pass11769 principal-symbol common zero; its carrier momentum lies
in the nullspace of all active transport directions. Compute *exact*
Gaussian moments for <H> and <P²>. Then <H>/<P²> ->0.
This does NOT preclude subellipticity, compact resolvent or positive gap.
"""
from pathlib import Path
import json,sys
from fractions import Fraction as F
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as V
def certificate():
    geom=V.geometry()
    U=np.rint(40*geom['u']).astype(np.int64)
    W=np.rint(40*geom['v']).astype(np.int64)
    qi=np.array([39]+[-1]*39+[0]*40,dtype='int64')
    X=W@qi+40
    active=np.flatnonzero(X)
    assert len(active)==4 and not np.any((U@W.T).diagonal())
    k=None
    for base in (range(40),range(40,80)):
      for i in base:
        for j in base:
          if j<=i:continue
          v=np.zeros(80,dtype='int64');v[i]=1;v[j]=-1
          if not np.any(U[active]@v):k=v;break
        if k is not None:break
      if k is not None:break
    assert k is not None and not np.any(U[active]@k)
    assert np.sum(k[:40])==np.sum(k[40:])==0
    a2=F(1,20)
    # b_e= a*X_e/40: <b_e^2> = a² X_e²/1600
    b2=[a2*F(int(z*z),1600) for z in X]
    v2=[F(int(w@w),1600) for w in W]
    u2=[F(int(u@u),1600) for u in U]
    uk=[F(int(u@k),40) for u in U]
    assert all((not b2[i] or uk[i]==0) for i in range(160))
    assert len(set(v2))==len(set(u2))==1
    assert all(int(U[i]@W[i])==0 for i in range(160))
    # Gaussian |psi|² has configuration covariance δ² I/2, δ=Λ^-1/2.
    # ∫||Je psi||² = [(Λ Uk+a)^2 (b²+ δ² v²/2)
    #                 + b² u²/(2δ²) + v²u²/4 + (V.U)²/2]
    # linear in Λ except a vanishing term as Λ^-1.
    leading=sum((v2[i]*uk[i]**2/2 + b2[i]*u2[i]/2 for i in range(160)),F(0))
    constant=sum((a2*b2[i] + v2[i]*u2[i]/4 for i in range(160)),F(0))
    # cross 2a Lambda Uk times delta² v² /2 => a v² Uk
    # cancellation by sum U_e=0
    assert sum((v2[i]*uk[i] for i in range(160)),F(0))==0
    reciprocal=sum((a2*v2[i]/2 for i in range(160)),F(0))
    normk=F(int(k@k))
    assert normk==2
    results=[]
    for Lam in (10,100,1000,10000):
      H=leading*Lam+constant+reciprocal/F(Lam)
      P2=normk*Lam**2+F(78,2)*Lam
      results.append(dict(Lambda=Lam,energy=float(H),
        momentum_square=float(P2),ratio=float(H/P2)))
    assert results[-1]['ratio']<results[0]['ratio']/100
    return dict(status='PASS',
      normalizable_packet='psi_L(q)=(pi*delta²)^(-78/4) exp(-||q-q0||²/(2delta²)) exp(i L k.q), delta=L^-1/2',
      carrier_integral_vector=list(map(int,k)),active_incidence_indices=list(map(int,active)),
      current_symbol_zero='At q0, every incidence current symbol has either Vq0+a=0 or Uk=0. k lies in 78D physical augmentation.',
      full_H_expectation='A*L+B+C/L',A=str(leading),B=str(constant),C=str(reciprocal),
      free_momentum_expectation='2*L²+39*L',
      exact_asymptotic_ratio='(A*L+B+C/L)/(2*L²+39*L) ->0',
      controls=results,
      theorem='No c>0,C finite can satisfy H>=c P²-C as a quadratic form on smooth Schwartz vectors, since normalizable packet family has <H>=O(L), <P²>=2L²+O(L).',
      physical_limit='Excludes uniform elliptic full-gradient domination only. Cannot exclude hypoelliptic/subelliptic estimates, compact resolvent, or a positive quantum mass gap.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_no_uniform_ellipticity_packet.json').write_text(json.dumps(d,indent=2)+'\n')
 print('NO ELLIPTIC',d['A'],d['B'],d['C'],d['controls'])
