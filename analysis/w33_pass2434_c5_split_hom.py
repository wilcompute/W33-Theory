#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, itertools, json
from pathlib import Path
import numpy as np
import sympy as sp
from w33_pass1801_1805_common import build_geometry
ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/w33_pass2434_c5_split_hom.json';P=101

def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
def inverse(p):
 z=[0]*len(p)
 for i,j in enumerate(p):z[j]=i
 return tuple(z)
def porder(p):
 x=tuple(range(len(p)))
 for n in range(1,20):
  x=compose(p,x)
  if x==tuple(range(len(p))):return n
 raise AssertionError
def rank_mod(A):
 A=np.array(A,dtype=np.int64)%P;m,n=A.shape;r=0
 for c in range(n):
  nz=np.flatnonzero(A[r:,c])
  if not len(nz):continue
  i=r+int(nz[0]);A[[r,i]]=A[[i,r]];A[r]=A[r]*pow(int(A[r,c]),-1,P)%P
  for j in np.flatnonzero(A[:,c]):
   if j!=r:A[j]=(A[j]-A[j,c]*A[r])%P
  r+=1
  if r==m:break
 return r
def signed_action(g,edges,ei):
 q=np.empty(len(edges),dtype=np.int16);s=np.empty(len(edges),dtype=np.int8)
 for j,(a,b) in enumerate(edges):
  x,y=g[a],g[b]
  if x<y:q[j]=ei[(x,y)];s[j]=1
  else:q[j]=ei[(y,x)];s[j]=-1
 return q,s
def class_sum(C,edges,ei):
 M=np.zeros((240,240),dtype=np.int64);cols=np.arange(240)
 for g in C:
  q,s=signed_action(g,edges,ei);M[q,cols]=(M[q,cols]+s)%P
 return M
def projector(M,lam,vals):
 I=np.eye(M.shape[0],dtype=np.int64);R=I.copy()
 for mu in vals:
  if mu!=lam:R=(R@((M-mu*I)%P)*pow((lam-mu)%P,-1,P))%P
 return R
def atlas_phi5_check():
 w,t=sp.symbols('w t')
 B=sp.Matrix([[0,1,0,0],[0,0,0,1],[-w,-w,0,1],[0,w,-1-w,-1]])
 coeff=[]
 for c in sp.Poly(B.charpoly(t).as_expr(),t).all_coeffs():
  coeff.append(int(sp.rem(sp.Poly(c,w),sp.Poly(w*w+w+1,w)).as_expr()))
 assert coeff==[1,1,1,1,1]
 return coeff
def build_full():
 D=build_geometry();gens=[a[0] for a in D['acts']];ident=tuple(range(40));G={ident};q=collections.deque([ident])
 while q:
  x=q.popleft()
  for g in gens:
   y=compose(g,x)
   if y not in G:G.add(y);q.append(y)
 assert len(G)==25920;G=list(G);invs={g:inverse(g) for g in G}
 def cclass(g):return {compose(compose(h,g),invs[h]) for h in G}
 c40=[];c45=[];c5=[];done=set()
 for g in G:
  if g in done:continue
  o=porder(g)
  if o not in (2,3,5):continue
  C=cclass(g);done|=C
  if o==3 and len(C)==40:c40.append(C)
  elif o==2 and len(C)==45:c45.append(C)
  elif o==5 and len(C)==5184:c5.append(C)
 assert len(c40)==2 and len(c45)==1 and len(c5)==1
 edges=list(D['edges']);ei={e:i for i,e in enumerate(edges)};I=np.eye(240,dtype=np.int64)
 C1,C2=[class_sum(C,edges,ei) for C in c40];M45=class_sum(c45[0],edges,ei);S=(C1+C2)%P
 P8=projector(S,8,[32,20,0,8]);P90=(P8@((M45+15*I)%P)*pow(12,-1,P))%P
 assert rank_mod(P90)==90 and int(np.trace(P90)%P)==90
 g5=next(iter(c5[0]));tr=[];x=ident;cycles=[]
 for _ in range(4):
  x=compose(g5,x);perm,sgn=signed_action(x,edges,ei)
  tr.append(sum(int(sgn[j])*int(P90[j,int(perm[j])]) for j in range(240))%P)
 seen=set()
 for i in range(40):
  if i in seen:continue
  z=[];j=i
  while j not in seen:seen.add(j);z.append(j);j=g5[j]
  cycles.append(len(z))
 assert tr==[0,0,0,0] and sorted(cycles)==[5]*8
 e8=[0,2,2,2,2];co=[18]*5;hom=sum(a*b for a,b in zip(e8,co));assert hom==144
 return {'group_order':len(G),'order5_class_size':len(c5[0]),'point_cycle_lengths':sorted(cycles),'coexact90_nonidentity_traces_mod101':tr,'coexact90_C5_multiplicities':co,'E8_degree4_atlas_generator_characteristic_polynomial':atlas_phi5_check(),'E8_real8_C5_multiplicities':e8,'Hom_dimension':hom}
def verify(d):
 assert d['sha256_without_hash_field']==digest(d) and all(d['checks'].values())
 assert d['restriction']['Hom_C5_E8_to_coexact90_dimension']==144
 assert d['restriction']['E8_real8_multiplicities']==[0,2,2,2,2]
 assert d['restriction']['coexact90_multiplicities']==[18,18,18,18,18]
 return d
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');ap.add_argument('--write-json',type=Path);a=ap.parse_args()
 if a.full:
  z=build_full();print(json.dumps(z,sort_keys=True));return
 d=verify(json.loads(CERT.read_text()))
 if a.write_json:a.write_json.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field'],'Hom_C5':144},sort_keys=True))
if __name__=='__main__':main()
