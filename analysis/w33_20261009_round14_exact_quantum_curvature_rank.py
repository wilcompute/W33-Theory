"""EXACT rank of effective magnetic curvature 2-form: symbolic
low-dimensional Schur structure + integer-rank certificate.

Prior Round13: rank mod three primes =16 => rational rank>=16,
floating rank=16, but rigorously rank<=16 was OPEN.

At q = (e0-e39)/(10sqrt20), t_i in {360,400,440}.
The exact solution y=T^-1 b lies in 2D invariant subspace:
y=(a,b,b,...,b,0,...,0) in adapted 78D coordinates.
Use two exact equations to solve for a,b and verify ALL 78.
Define W=U.T diag(t*(1-U y)) V.
Then C-C.T=32000 T^-1(W T - T W.T) T^-1,
so curvature rank=rank of integer S=(den W)T-T(den W).T.
All inverse operations are avoided by the integer Schur witness.
Calculate rank exactly using SymPy's DomainMatrix over ZZ/QQ.
"""
from pathlib import Path
import json,sys
import numpy as np
import sympy as S
from sympy.polys.matrices import DomainMatrix
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as H
from w33_20261009_quantum_curvature_fullrank_modp import rank_mod
def certificate():
 geo=H.geometry()
 u40=np.rint(40*geo['u']).astype(np.int64)
 v40=np.rint(40*geo['v']).astype(np.int64)
 D=np.zeros((80,78),dtype=np.int64)
 for j in range(39):D[j,j]=1;D[39,j]=-1
 for j in range(39):D[40+j,39+j]=1;D[79,39+j]=-1
 hin=40*np.eye(78,dtype=np.int64);hin[:39,:39]-=1;hin[39:,39:]-=1
 u=u40@D@hin;v=v40@D;t=400+v[:,0]
 T=u.T@((t*t)[:,None]*u);target=u.T@(t*t)
 basis=np.zeros((78,2),dtype=np.int64)
 basis[0,0]=1;basis[1:39,1]=1
 A=T@basis
 M=S.Matrix([[int(A[i,j]) for j in range(2)] for i in (0,1)])
 RHS=S.Matrix([int(target[i]) for i in (0,1)])
 coeff=M.inv()*RHS
 numerator=np.array([int(x) for x in coeff*int(S.ilcm(*[S.denom(x) for x in coeff]))],dtype=object)
 den=int(S.ilcm(*[S.denom(x) for x in coeff]))
 yy=basis.astype(object)@numerator
 assert all(sum(int(T[i,j])*int(yy[j]) for j in range(78))==den*int(target[i]) for i in range(78))
 # Explicit integer numerator W for all ranks.
 uu=u.astype(object);vv=v.astype(object);tt=t.astype(object)
 ts=np.array([tt[i]*(den-sum(uu[i,j]*yy[j] for j in range(78))) for i in range(160)],dtype=object)
 W=uu.T@(ts[:,None]*vv)
 TT=T.astype(object)
 skew=W@TT-TT@W.T
 assert all(skew[i,i]==0 for i in range(78))
 assert all(skew[i,j]==-skew[j,i] for i in range(78) for j in range(i+1,78))
 # Convert to genuine exact rank via sparse integer DomainMatrix.
 matrix=S.Matrix([[int(x) for x in row] for row in skew])
 rank=int(DomainMatrix.from_Matrix(matrix).rank())
 assert rank%2==0
 prior=json.loads((ROOT/'data/w33_20261009_quantum_curvature_fullrank_modp.json').read_text())
 assert rank>=max(x['rank_skew2form_over_Fp'] for x in prior['finite_field_rank_lower_bounds'])
 return dict(status='PASS',
     original_model='Actual full-H 160-current differential connection in 78D quantum configuration space',
     adapted_exact_y_coefficients=[str(x) for x in coeff],adapted_two_parameter_y_verified_all_78=True,
     numerator_common_denominator=den,
     exact_antisymmetric_integer_schur_rank=rank,
     exact_magnetic_curvature_Q_rank=rank,
     prior_three_modp_rank_lower_bound=16,
     proof='The rational 78x78 magnetic curvature is congruent via invertible T to integer skew matrix S=W_n T - T W_n^T. Exact integer DomainMatrix rank of S certifies the exact rational rank; 2-parameter exact y solves all 78 equations, so all entries computed without float inversion.',
     limitation='Model connection curvature only; no proof of actual vacuum irrep, global numeric spectral gap or Einstein gravity.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_round14_exact_quantum_curvature_rank.json').write_text(json.dumps(d,indent=2)+'\n')
 print('EXACT FULL H CURVATURE',d)
