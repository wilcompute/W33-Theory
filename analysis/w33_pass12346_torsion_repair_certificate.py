"""Recovered exact continuation: torsion order bound and repair obstructions.
Inputs are the W,N matrices of Pass12341. No full TOE claim.
"""
from pathlib import Path
from itertools import combinations,permutations
from math import gcd,lcm,comb
from functools import reduce
import json,hashlib
import sympy as s
import numpy as np
W=s.Matrix([[0,1,1,-1],[-1,0,1,-1],[0,0,1,-1],[0,0,1,0]])
N=s.Matrix([[10,-5,1,-6],[-5,10,-5,6],[1,-5,10,-6],[-6,6,-6,12]])
h=s.symbols('h0:4');a=s.symbols('a0:4');t=s.symbols('t')
d=s.Matrix(h)-s.ones(4,1);Q=s.Poly(s.expand((d.T*N*d)[0]/2),*h);terms=Q.terms();exps=[v for v,c in terms]
def canon(rows):
 if not rows:return ()
 A=s.Matrix(rows).rref()[0]
 return tuple(tuple(A[i,j] for j in range(4)) for i in range(A.rows) if any(A[i,j] for j in range(4)))
def directions():
 seen=set();found={}
 def visit(rows):
  if rows in seen:return
  seen.add(rows)
  if len(rows)==4:return
  ker=s.Matrix(rows).nullspace() if rows else [s.eye(4)[:,i] for i in range(4)]
  groups={}
  for i,e in enumerate(exps):groups.setdefault(tuple(sum(e[j]*v[j] for j in range(4)) for v in ker),[]).append(i)
  single=[g[0] for g in groups.values() if len(g)==1]
  if not single:
   assert len(rows)==3
   v=ker[0];den=lcm(*(int(x.q) for x in v));v=[int(x*den) for x in v];g=reduce(gcd,v);v=[x//g for x in v]
   if next(x for x in v if x)<0:v=[-x for x in v]
   found[tuple(v)]=list(groups.values());return
  i=single[0]
  for group in groups.values():
   if i not in group:
    j=group[0];visit(canon(list(rows)+[tuple(exps[i][k]-exps[j][k] for k in range(4))]))
 visit(())
 assert len(seen)==232 and len(found)==17
 return found

def coset_certificate():
 forbidden={(0,0,1,1):a[1]-6,(1,1,0,1):5*a[2]**2+6,(1,1,0,0):a[2]-6,(0,1,0,1):6*a[3]**2+6*a[3]+5,(1,0,1,0):5*a[1]+6*a[3],(0,1,1,0):a[0]-6,(1,0,0,1):a[1]-6,(0,1,1,1):5*a[0]**2+6}
 out=[]
 for v,groups in sorted(directions().items()):
  k=next(i for i in range(4) if v[i]);rest=[a[i] for i in range(4) if i!=k]
  eq=[s.expand(sum(terms[i][1]*s.prod(a[j]**terms[i][0][j] for j in range(4)) for i in g).subs(a[k],1)) for g in groups]
  G=s.groebner(eq+[t*s.prod(rest)-1],t,*rest,order='grevlex');w=forbidden.get(v,s.Integer(1))
  assert G.reduce(w)[1]==0
  out.append({'direction':v,'normalization_axis':k,'equations':list(map(str,eq)),'basis':[str(p.as_expr()) for p in G.polys],'forbidden_consequence':str(w)})
 return out

def determinant_bound():
 diffs=sorted(set(tuple(x-y for x,y in zip(u,v)) for u,v in combinations(exps,2)));A=np.array(diffs,dtype=np.int64)
 pp=list(permutations(range(4)));ss=[(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4)) for p in pp];hist={};witness=None
 for i,j in combinations(range(len(A)),2):
  if j+2>=len(A):continue
  k,l=np.triu_indices(len(A)-j-1,1);k+=j+1;l+=j+1;val=np.zeros(len(k),dtype=np.int64)
  for p,sg in zip(pp,ss):val+=sg*A[i,p[0]]*A[j,p[1]]*A[k,p[2]]*A[l,p[3]]
  for z,count in zip(*np.unique(abs(val),return_counts=True)):hist[int(z)]=hist.get(int(z),0)+int(count)
  hit=np.flatnonzero(abs(val)==16)
  if witness is None and len(hit):r=int(hit[0]);witness=A[[i,j,int(k[r]),int(l[r])]].tolist()
 assert len(A)==53 and sum(hist.values())==comb(53,4)==292825 and max(hist)==16
 assert abs(s.Matrix(witness).det())==16
 orders=sorted({int(x) for b in range(1,17) for x in s.divisors(30030*b)})
 assert len(orders)==464 and max(orders)==480480
 return {'histogram':hist,'maximal_minor_witness':witness,'necessary_orders':orders,'mann_primorial':30030}

def q_at(z):
 z=list(map(s.sympify,z));delta=s.Matrix([s.prod(z[j]**int(W[i,j]) for j in range(4)) for i in range(4)])-s.ones(4,1)
 return s.simplify((delta.T*N*delta)[0]/2)
def repair_witnesses():
 w=(-1+s.I*s.sqrt(3))/2;b=(-17+4*s.I*s.sqrt(21))/25;c=(-1+2*s.I*s.sqrt(30))/11
 rows={(0,1):[1,1,w,w**2],(0,2):[1,b,1,-5*(b+1)/4],(0,3):[1,c,c+s.Rational(2,11),1],(1,2):[c,1,1,c+s.Rational(2,11)],(1,3):[b,1,-5*(b+1)/4,1],(2,3):[w,w,1,1]}
 result=[]
 for axes,z in rows.items():
  assert q_at(z)==0 and all(s.simplify(x*s.conjugate(x)-1)==0 for x in z)
  assert all(z[i]==1 for i in axes)
  result.append({'inactive_axes':axes,'character':list(map(str,z))})
 u=(1+3*s.I*s.sqrt(11))/10;z=[1/u,u*u,1,u]
 assert q_at(z)==0 and s.simplify(z[0]*z[3]-1)==0 and s.simplify(z[0]*z[1]/z[3]-1)==0
 return {'coordinate_pairs':result,'noncoordinate_character':list(map(str,z)),'primitive_irreducible_polynomial':'5*x^2-x+5'}
def run():
 return {'cosets':coset_certificate(),'torsion_bound':determinant_bound(),'repair':repair_witnesses(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
if __name__=='__main__':
 p=Path(__file__).resolve().parents[1]/'data/w33_pass12346_torsion_repair_certificate.json';p.write_text(json.dumps(run(),indent=2)+'\n');print(p)
