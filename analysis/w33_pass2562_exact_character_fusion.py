#!/usr/bin/env python3
from fractions import Fraction
from pathlib import Path
import sys,json,collections,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass2553_pgsp_orbitals as W

def close(gens):
 n=len(gens[0]);I=tuple(range(n));S={I};q=collections.deque([I])
 while q:
  p=q.popleft()
  for g in gens:
   z=tuple(g[p[i]] for i in range(n))
   if z not in S:S.add(z);q.append(z)
 return list(S)
def orbitals(G):
 rel=np.full((540,540),-1,dtype=np.int16);reps=[]
 for a in range(540):
  for b in range(540):
   if rel[a,b]>=0:continue
   O={(p[a],p[b]) for p in G};r=len(reps)
   for x,y in O:rel[x,y]=r
   reps.append((a,b))
 return rel,reps
def structure(rel,reps):
 r=len(reps);P=np.zeros((r,r,r),dtype=np.int64)
 for k,(a,b) in enumerate(reps):
  for x in range(540):P[rel[a,x],rel[x,b],k]+=1
 tr=[int(rel[b,a]) for a,b in reps];val=[int(np.sum(rel[0]==i)) for i in range(r)]
 return P,tr,val
pg,fg=W.geom();G=close(fg[:5]);assert len(G)==25920
rel,reps=orbitals(G);assert len(reps)==32
P,tr,val=structure(rel,reps);r=32
z=[0,-4,-4,4,0,8,0,0,0,4,4,0,4,0,4,0,0,4,2,0,0,4,4,4,2,0,0,0,0,0,0,0]
def mul(a,b):
 out=[Fraction(0) for _ in range(r)]
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:
     for k,p in enumerate(P[i,j]):
      if p:out[k]+=x*y*int(p)
 return out
one=[Fraction(0)]*r;one[0]=1;zf=list(map(Fraction,z));lams=[-88,-64,-40,0,8,32,80,800]
C=[]
for lam in lams:
 num=one;den=1
 for mu in lams:
  if mu!=lam:num=mul(num,[zf[i]-mu*one[i] for i in range(r)]);den*=lam-mu
 c=[x/Fraction(den) for x in num];assert mul(c,c)==c;C.append(c)
def traceprod(a,b):return sum(a[i]*b[tr[i]]*540*val[i] for i in range(r))
ranks=[int(traceprod(c,one)) for c in C]
GG=W.actions();relg,repsg=orbitals(GG);assert len(repsg)==22
psp_to_pg=[int(relg[a,b]) for a,b in reps]
S=json.loads((ROOT/'data/w33_pass2472_rank9_scheme_decode.json').read_text());blocks=S['blocks'];q2b={q:i for i,B in enumerate(blocks) for q in B};Q=S['second_eigenmatrix_Q']
def rat(x):return Fraction(x['num'],x['den']) if isinstance(x,dict) else Fraction(x)
Es=[[rat(Q[q2b[psp_to_pg[i]]][j])/540 for i in range(r)] for j in range(9)]
M=[[int(traceprod(e,c)) for c in C] for e in Es]
assert [sum(row) for row in M]==S['multiplicities'];assert [sum(M[i][j] for i in range(9)) for j in range(8)]==ranks
out={'central_element_coefficients':z,'central_eigenvalues':lams,'central_isotypic_ranks':ranks,'rank9_multiplicities':S['multiplicities'],'intersection_matrix':M,'psp_to_pgsp_orbital':psp_to_pg}
(ROOT/'data/w33_pass2562_exact_character_fusion.rebuilt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
