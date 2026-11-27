"""Exact finite checks for A2^4 / E8 boundary geometry. Python 3 + sympy."""
from itertools import product, combinations
from fractions import Fraction
from collections import Counter
import json
import sympy as s
from sympy.matrices.normalforms import hermite_normal_form
V=list(product(range(3),repeat=4)); zero=(0,)*4
add=lambda a,b:tuple((x+y)%3 for x,y in zip(a,b))
scale=lambda a,k:tuple(k*x%3 for x in a)
dot=lambda a,b:sum(x*y for x,y in zip(a,b))%3
wt=lambda a:sum(x!=0 for x in a)
N=[v for v in V if dot(v,v)==0]
L=sorted({tuple(sorted({add(scale(a,i),scale(b,j)) for i,j in product(range(3),repeat=2)})) for a,b in combinations(N[1:],2) if dot(a,b)==0 and b!=scale(a,2)})
assert len(N)==33 and len(L)==8 and all(len(c)==9 for c in L)
sets=list(map(set,L)); fam0=[i for i,c in enumerate(sets) if i==0 or len(c&sets[0])==1]; fam1=[i for i in range(8) if i not in fam0]; order=fam0+fam1
L=[L[i] for i in order]; sets=list(map(set,L)); assert len(fam0)==len(fam1)==4
B=s.Matrix([[int(v in c) for c in sets] for v in V]); G=B.T*B/9
assert G.rank()==7 and s.expand(G.charpoly().as_expr()-s.Symbol('lambda')*(s.Symbol('lambda')-s.Rational(8,3))*(s.Symbol('lambda')-s.Rational(8,9))**6)==0
assert B*s.Matrix([1]*4+[-1]*4)==s.zeros(81,1)
for i,j in combinations(range(8),2): assert len(sets[i]&sets[j])==(1 if i//4==j//4 else 3)
for c in L:
 for inds in combinations(range(4),2): assert len({tuple(v[i] for i in inds) for v in c})==9
# S^2 is inversion. On even vectors S is rational.
R=sorted({min(v,scale(v,2)) for v in N}); assert len(R)==17
E=s.Matrix([[int(min(v,scale(v,2))==r) for r in R] for v in V])
F=s.Matrix([[sum((2 if dot(x,y)==0 else -1) for y in V if min(y,scale(y,2))==r)/s.Integer(18) for r in R] for x in V])
assert (F-E).rank()==10 and E.rank()==17
assert F*B[[V.index(r) for r in R],:]==B
# A2 discriminant generator (2,1)/3, norm 2/3.
A=s.diag(*([s.Matrix([[2,-1],[-1,2]])]*4)); lattice=[]
for c in L:
 glue=s.Matrix(8,9,lambda i,j: (2 if i%2==0 else 1)*c[j][i//2]); H=hermite_normal_form((3*s.eye(8)).row_join(glue)); U=H/3
 K=U.T*A*U; M=U.inv(); assert K.det()==1 and all(x.q==1 for x in K) and all(K[i,i]%2==0 for i in range(8)); assert all(x.q==1 for x in M) and abs(M.det())==9
 assert M.T*K*M==A
 J=s.diag(A,-K); W=s.eye(8).col_join(M); assert W.T*J*W==s.zeros(8)
 lattice.append({'gram':[[int(K[i,j]) for j in range(8)] for i in range(8)],'inclusion':[[int(M[i,j]) for j in range(8)] for i in range(8)]})
assert Counter(wt(v)%3 for v in V)=={0:33,1:24,2:24}
inter=[[len(a&b) for b in sets] for a in sets]; dims=[[9//x for x in row] for row in inter]
result={'null_count':len(N),'planes':L,'gram_times_9':(9*G).tolist(),'gram_spectrum':{'0':1,'8/9':6,'8/3':1},'modular_fixed_dimension':17-(F-E).rank(),'all_48_two_coordinate_projections_bijective':True,'intersection':inter,'boundary_defect_dimension_squared':dims,'lattice_certificates':lattice,'quadratic_value_histogram':{0:33,1:24,2:24}}
if __name__=='__main__': print(json.dumps(result,indent=2,default=int))
