#!/usr/bin/env python3
import json,itertools
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
# Family triplet with Delta(54)=<X,Z,R>.  For a symmetric 16_i16_j channel,
# represent T_{ijk}=T_{jik}; Z invariance is i+j+k=0 mod3.
basis=[(i,j,k) for i in range(3) for j in range(i,3) for k in range(3)]
v=sp.symbols('t0:'+str(len(basis))); pos={b:n for n,b in enumerate(basis)}
def var(i,j,k):
 if i>j:i,j=j,i
 return v[pos[(i,j,k)]]
eq=[]
for i,j,k in basis:
 if (i+j+k)%3: eq.append(var(i,j,k))
 # X: all family labels shift together
 ii,jj,kk=(i+1)%3,(j+1)%3,(k+1)%3
 eq.append(var(i,j,k)-var(ii,jj,kk))
 # R: c -> -c
 ii,jj,kk=(-i)%3,(-j)%3,(-k)%3
 eq.append(var(i,j,k)-var(ii,jj,kk))
A,_=sp.linear_eq_to_matrix(eq,v); ns=A.nullspace()
assert len(ns)==2
supports=[]
for w in ns:
 supports.append([(basis[n],str(sp.simplify(c))) for n,c in enumerate(w) if c])
a,b,h0,h1,h2=sp.symbols('a b h0 h1 h2')
Y=sp.Matrix([[a*h0,b*h2,b*h1],[b*h2,a*h1,b*h0],[b*h1,b*h0,a*h2]])
det=sp.factor(Y.det())
target=sp.expand((a**3+2*b**3)*h0*h1*h2-a*b**2*(h0**3+h1**3+h2**3))
assert sp.expand(det-target)==0
lam=sp.factor((a**3+2*b**3)/(3*a*b**2))
# exact cross-track identity with Pass11114: a=s, b=d.
old=json.loads((ROOT/'data/w33_pass11114_hesse_mass_determinant.json').read_text())
out={
 'status':'PASS_SPIN10_FAMILY_TRIPLET_HAS_TWO_DELTA54_YUKAWA_TENSORS_AND_HESSE_DETERMINANT',
 'symmetric_family_tensor_dimension':2,
 'basis_supports':supports,
 'Yukawa_matrix':'[[a h0,b h2,b h1],[b h2,a h1,b h0],[b h1,b h0,a h2]]',
 'determinant':str(det),
 'Hesse_parameter_lambda':str(lam),
 'equal_vev_eigenvalues':['a+2b','a-b','a-b'],
 'cross_track_map':'a=s=Y_same, b=d=Y_dist; this is exactly the Pass11114 Hesse mass matrix, now welded to the Spin(10) 16*16*10_H channel.',
 'pass11114_lambda_cubed_at_rho':old['lambda_cubed_at_rho'],
 'boundary':'Delta(54) fixes the tensor space to two complex coefficients; it does not predict their values or the Higgs alignment.'
}
OUT=ROOT/'data/PART_W33_PASS11591_SPIN10_DELTA54_HESSE_YUKAWA.json'
OUT.write_text(json.dumps(out,indent=2,sort_keys=True))
print(json.dumps(out,indent=2))
