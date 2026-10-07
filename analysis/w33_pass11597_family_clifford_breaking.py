#!/usr/bin/env python3
import json,itertools
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
w=-sp.Rational(1,2)+sp.I*sp.sqrt(3)/2
X=sp.zeros(3);R=sp.zeros(3)
for i in range(3):
 X[(i+1)%3,i]=1; R[(-i)%3,i]=1
Z=sp.diag(1,w,w**2)
F=sp.Matrix([[w**(i*j)/sp.sqrt(3) for j in range(3)] for i in range(3)])
P=sp.diag(1,1,w)
basis=[(i,j,k) for i in range(3) for j in range(i,3) for k in range(3)]
def action(G):
 M=sp.zeros(len(basis)); loc={b:n for n,b in enumerate(basis)}
 for col,(i,j,k) in enumerate(basis):
  for a,b,c in itertools.product(range(3),repeat=3):
   coeff=G[a,i]*G[b,j]*G[c,k]
   if coeff:
    aa,bb=sorted((a,b)); M[loc[(aa,bb,c)],col]+=coeff
 return sp.simplify(M)
I=sp.eye(len(basis))
def fixed_dim(gs):
 A=sp.Matrix.vstack(*[action(g)-I for g in gs])
 return len(A.nullspace()),A.nullspace()
d54,bd=fixed_dim([X,Z,R])
full,bf=fixed_dim([X,Z,R,F,P])
assert d54==2 and full==0
# Restrict F,P to the two canonical Hesse tensors.
Tdiag=sp.zeros(len(basis),1);Toff=sp.zeros(len(basis),1);loc={b:n for n,b in enumerate(basis)}
for i in range(3):Tdiag[loc[(i,i,i)]]=1
for t in [(0,1,2),(0,2,1),(1,2,0)]:Toff[loc[t]]=1
B=sp.Matrix.hstack(Tdiag,Toff)
rows=list(B.T.rref()[1]); L=B[rows,:].inv()
def restrict(g):
 im=action(g)*B
 Rm=L*im[rows,:]
 assert B*Rm==im
 return sp.simplify(Rm)
RF,RP=restrict(F),restrict(P)
out={
 'status':'PASS_FULL_QUTRIT_CLIFFORD_FORBIDS_SYMMETRIC_TRIPLET_YUKAWA_DELTA54_RELEASES_HESSE_PAIR',
 'Delta54_invariant_dimension':d54,
 'Clifford648_invariant_dimension':full,
 'F_on_Hesse_pair':[[str(x) for x in RF.row(i)] for i in range(2)],
 'P_on_Hesse_pair':[[str(x) for x in RP.row(i)] for i in range(2)],
 'interpretation':'The full H27:SL(2,3) family normalizer leaves no symmetric 3x3x3 Yukawa scalar. Reducing to the realized Delta(54)=H27:<-I> releases exactly the two Hesse tensors.',
 'boundary':'This proves symmetry breaking is necessary for this 10_H triplet Yukawa, not the dynamical origin or scale of that breaking.'
}
(ROOT/'data/PART_W33_PASS11597_FAMILY_CLIFFORD_BREAKING.json').write_text(json.dumps(out,indent=2,sort_keys=True))
print(json.dumps(out,indent=2))
