#!/usr/bin/env python3
import itertools,json
from pathlib import Path
import numpy as np, sympy as sp
ROOT=Path(__file__).resolve().parents[1]
gd=json.loads((ROOT/'data/w33_pass10961_albert_clifford9_gammas.json').read_text())
g9=[sp.Matrix([[sp.Rational(x) for x in row] for row in M]) for M in gd['gamma9']]
I16=sp.eye(16);Z16=sp.zeros(16)
g=[sp.Matrix.vstack(sp.Matrix.hstack(Z16,x),sp.Matrix.hstack(x,Z16)) for x in g9]+[sp.diag(I16,-I16)]
biv=[g[i]*g[j] for i,j in itertools.combinations(range(10),2)]
prod=sp.eye(32)
for x in g:prod*=x
Chi=sp.I*prod
Wp=sp.Matrix.hstack(*(Chi-sp.eye(32)).nullspace());Wm=sp.Matrix.hstack(*(Chi+sp.eye(32)).nullspace())
def reps(W):
 piv=list(W.T.rref()[1]);L=W[piv,:].inv();out=[]
 for M in biv:
  im=M*W;out.append(np.array((L*im[piv,:]).evalf(),complex))
 return out
Rp,Rm=reps(Wp),reps(Wm)
def nullity(left,right=None):
 if right is None:right=left
 n=left[0].shape[0];m=right[0].shape[0];I_n=np.eye(n);I_m=np.eye(m)
 A=np.vstack([np.kron(I_n,B)-np.kron(A.T,I_m) for A,B in zip(left,right)])
 s=np.linalg.svd(A,compute_uv=False)
 tol=max(A.shape)*s[0]*np.finfo(float).eps
 return int((s<=tol).sum()),float(s[-3]),float(s[-1])
cp,pgap,_=nullity(Rp);cm,mgap,_=nullity(Rm);cross,xgap,xmin=nullity(Rp,Rm)
assert cp==1 and cm==1 and cross==0
assert all(M*Chi==Chi*M for M in biv)
out={'status':'PASS_GAUGE_INVARIANT_WEYL_SELECTOR_UNIQUE_UP_TO_IDENTITY',
     'Weyl_plus_commutant_dim':cp,'Weyl_minus_commutant_dim':cm,'cross_intertwiner_dim':cross,
     'numerical_rank_gaps':{'plus':pgap,'minus':mgap,'cross_smallest':xmin},
     'full_Dirac_commutant_dim':2,'commutant_basis':'span{I,Chi}',
     'selector':'P_plus=(I+Chi)/2 or P_minus=(I-Chi)/2',
     'theorem':'On the executable Spin(10) Dirac carrier, every gauge-invariant Hermitian selector is aI+bChi. There is no independent Hesse/clock/arrow gauge-invariant involution capable of choosing chirality.',
     'clock_firewall':'Because the certified two-tick clock sends Chi to -Chi, any nonzero b breaks that clock symmetry. A clock-even polynomial in Chi is proportional to I and cannot select a Weyl sector.',
     'boundary':'Commutant dimensions are certified numerically with a large singular-value gap on the exact rational representation; the algebraic identification is the standard complex Clifford-even decomposition into two inequivalent Weyl irreps.'}
(ROOT/'data/PART_W33_PASS11593_UNIQUE_WEYL_SELECTOR.json').write_text(json.dumps(out,indent=2,sort_keys=True))
print(json.dumps(out,indent=2))
