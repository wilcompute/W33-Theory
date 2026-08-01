#!/usr/bin/env python3
"""Pass 1839: four geometrically fingerprinted probes reconstruct the four chiral traces."""
from __future__ import annotations
import itertools,json,sys
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass1801_1805_common import build_geometry,rank_mod,nullspace,basis_columns,inv_mod
P=1000003;D=build_geometry();points=D['points'];edges=D['edges'];eidx=D['eidx'];lines=D['lines'];frames=D['frames'];octets=D['octets']
def comp(p,q):return tuple(p[q[i]] for i in range(40))
def eval_inner(word):
 p=tuple(range(40));gens=[tuple(a[0]) for a in D['acts']]
 for ch in reversed(word):p=comp(gens[int(ch)],p)
 return p
outer=tuple(D['outer'][0])
def induced(pp):
 ed={e:i for i,e in enumerate(edges)};ld={l:i for i,l in enumerate(lines)};fd={f:i for i,f in enumerate(frames)}
 ep=tuple(ed[tuple(sorted((pp[a],pp[b])))] for a,b in edges)
 lp=tuple(ld[tuple(sorted(pp[x] for x in L))] for L in lines)
 fp=tuple(fd[tuple(sorted((lp[a],lp[b])))] for a,b in frames)
 os=[frozenset(l)|frozenset(r) for l,r in octets];od={x:i for i,x in enumerate(os)}
 op=tuple(od[frozenset(pp[x] for x in (set(l)|set(r)))] for l,r in octets)
 return ep,lp,fp,op
def order(p):
 import math
 seen=[False]*40;o=1
 for i in range(40):
  if seen[i]:continue
  j=i;n=0
  while not seen[j]:seen[j]=True;n+=1;j=p[j]
  o=math.lcm(o,n)
 return o
bd=np.zeros((40,240),dtype=np.int64)
for j,(a,b) in enumerate(edges):bd[a,j]=-1;bd[b,j]=1
tri=[]
for L in lines:
 for a,b,c in itertools.combinations(L,3):
  r=np.zeros(240,dtype=np.int64);r[eidx[(a,b)]]=1;r[eidx[(b,c)]]=1;r[eidx[(a,c)]]=-1;tri.append(r)
tri=np.array(tri,dtype=np.int64);A=np.zeros((40,40),dtype=np.int64)
for a,b in edges:A[a,b]=A[b,a]=1
E15=nullspace((A+4*np.eye(40,dtype=np.int64))%P,P);E24=nullspace((A-2*np.eye(40,dtype=np.int64))%P,P)
G15=E15@bd%P;G24=E24@bd%P
s=np.zeros((45,40),dtype=np.int64);u=np.zeros((45,240),dtype=np.int64)
for o,(left,right) in enumerate(octets):
 s[o,list(left)]=1;s[o,list(right)]=-1
 for a in left:
  for b in right:u[o,eidx[tuple(sorted((a,b)))]]=1 if a<b else -1
V=(4*u+s@bd)%P;H=nullspace(np.vstack([bd,tri])%P,P)
def prep(B):
 B=B[basis_columns(B.T,P),:]%P;cols=np.array(basis_columns(B,P));return B,cols,inv_mod(B[:,cols],P)
def trace(dat,pp,ep):
 B,cols,Ci=dat;sign=np.array([1 if pp[a]<pp[b] else -1 for a,b in edges],dtype=np.int64);Y=np.zeros_like(B);Y[:,np.array(ep)]=B*sign%P;R=Y[:,cols]@Ci%P
 assert np.array_equal(R@B%P,Y);t=int(np.trace(R)%P);return t if t<P//2 else t-P
mods=[prep(x) for x in (G15,G24,V,H)]
probes=[('',[3,4,2,3]),('3210',[-1,0,4,-3]),('23410',[-2,1,-1,0]),('10',[1,0,0,-1])]
records=[]
for word,expected in probes:
 pp=comp(outer,eval_inner(word));ep,lp,fp,op=induced(pp);tr=[trace(m,pp,ep) for m in mods];assert tr==expected
 records.append({'outer_word':'s' if not word else 's*'+word,'order':order(pp),'fixed_points':sum(pp[i]==i for i in range(40)),'fixed_lines':sum(lp[i]==i for i in range(40)),'fixed_frames':sum(fp[i]==i for i in range(540)),'fixed_octets':sum(op[i]==i for i in range(45)),'traces':tr})
T=sp.Matrix([r['traces'] for r in records]);assert T.det()==80
print(json.dumps({'status':'PASS','trace_matrix':[r['traces'] for r in records],'determinant':int(T.det()),'probes':records},indent=2))
