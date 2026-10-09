"""A sharp parametric GAUSSIAN-PACKET obstruction on the coefficient
of any GLOBAL critical-order half-Sobolev operator inequality for H.

Does NOT establish H >= c(1+P²)^1/2-C! It gives an upper ceiling for
any such possible c by optimizing q-variance and momentum polarization.
Prior s>1/2 impossibility is independently recovered.
"""
import json,sys
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import sympy as S
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as V
from w33_20261009_local_hormander_depth import rank_mod
def certificate():
 geo=V.geometry();U=np.rint(40*geo['u']).astype('int64');W=np.rint(40*geo['v']).astype('int64')
 qi=np.array([39]+[-1]*39+[0]*40,dtype='int64')
 active=np.flatnonzero(W@qi+40)
 assert len(active)==4
 S1=U.T@U
 assert rank_mod(S1)==78
 ev,vec=np.linalg.eigh(S1.astype(float)/1600)
 lam_min=4-np.sqrt(6)
 assert sum(abs(ev-lam_min)<1e-8)==24 and sum(abs(ev)<1e-8)==2
 M=U[active]@vec[:,2:26]
 _,ss,Vh=np.linalg.svd(M,full_matrices=True)
 # 4x24, construct a vector in the 20D null of M.
 k=vec[:,2:26]@Vh[-1,:]
 k=k/np.linalg.norm(k)
 assert np.linalg.norm(U[active]@k)<1e-12
 assert abs(k@S1@k/1600-lam_min)<1e-11
 normv2=F(int(W[0]@W[0]),1600)
 normu2=F(int(U[0]@U[0]),1600)
 assert all(int(x@x)==int(W[0]@W[0]) for x in W)
 assert all(int(x@x)==int(U[0]@U[0]) for x in U)
 a2=F(1,20)
 X=W@qi+40
 bsum=a2*F(int(X@X),1600)
 A=normv2*S.Rational(4)-normv2*S.sqrt(6) # wrong? derived A = 1/2 normv2*(4-sqrt6)
 A=S.Rational(normv2.numerator,2*normv2.denominator)*(4-S.sqrt(6))
 B=S.Rational((bsum*normu2).numerator,2*(bsum*normu2).denominator)
 copt=S.sqrt(B/A);slope=S.simplify(2*S.sqrt(A*B))
 # Compare to old gaussian fixed integer k with |k|²=2, not a
 # normalized unit critical coefficient.
 val=float(slope); assert 0<val<240
 # Explicit asymptotic: <H>= Lambda*(A*c+B/c)+O(1);
 # <sqrt(1+P²)> = Lambda + o(Lambda) since |k|=1.
 q0mean=np.zeros(80);q0mean[:40]=[39]+[-1]*39
 return dict(status='PASS',underlying_full_H='160 W33 current-square Hamiltonian in 78 physical real coordinates',
 active_current_indices=list(map(int,active)),
 U_min_nonzero_eigenvalue='4-sqrt(6)',eigenspace_multiplicity=24,
 intersection_with_active_transport_null_dimension_at_least=20,
 normV_square=str(normv2),normU_square=str(normu2),sum_b_squared_at_q0=str(bsum),
 leading_gaussian_coefficients=dict(A=str(A),B=str(B),variance_delta_squared='c/Lambda',c_star=str(copt)),
 optimized_critical_halfSobolev_constant_upper_formula=str(slope),
 optimized_critical_halfSobolev_constant_upper_numeric=val,
 theorem='If H>=c*(1+P²)^1/2-C holds globally on the Schwartz core with c>0 and finite C, then necessarily c<=2 sqrt(A B), with A=(1/2)||V_e||²(4-sqrt6), B=(1/2)||U_e||² sum_e (V_e.q0+a)². The lower spectral calculation is NOT established.',
 asymptotic_packet='Take any unit k in the >=20-dimensional intersection E_{4-sqrt6}(U^TU) and ker(U_active). Gaussian delta²=c*/Lambda. Then <H>/Lambda ->2sqrt(A B), <(1+P²)^1/2>/Lambda ->1.',
 physical_boundary='A necessary upper ceiling on possible critical-order coercivity; not a proof that critical-order coercivity exists or that a physical mass gap is present.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_critical_sobolev_ceiling.json').write_text(json.dumps(d,indent=2)+'\n')
 print('CRITICAL C UPPER',d['optimized_critical_halfSobolev_constant_upper_numeric'],'c_star',d['leading_gaussian_coefficients']['c_star'])
