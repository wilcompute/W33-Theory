#!/usr/bin/env python3
"""Construct seven explicit quadratic intertwiners from the signed 90.

This is the expensive standalone reconstruction.  It builds PSp(4,3), its
signed 240-edge action, the relevant class sums and block projectors, and then
forms the bilinear tensors literally.  It is intentionally not run in CI.
"""
from __future__ import annotations
import hashlib,json,itertools,math
from pathlib import Path
import numpy as np
from w33_pass1060_1064_core import build_w33,matrix_perm

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/w33_pass2051_explicit_quadratic_intertwiners.json'
EXPECTED='8ab0957d202b517e7ee8104f2c180e986607074c746d5643b76f8f066f70d3dc'

def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def spectral_projector(M,lam,vals):
 P=np.eye(M.shape[0])
 for mu in vals:
  if mu!=lam:P=P@(M-mu*np.eye(M.shape[0]))/(lam-mu)
 return (P+P.T)/2
def basis(P):
 z,V=np.linalg.eigh((P+P.T)/2);return V[:,z>.5]
def tensor_stats(T):
 s=np.linalg.svd(T.reshape(T.shape[0],-1),compute_uv=False)
 return int(np.sum(s>1e-8)),float(s[0]),float(s[-1]),float(np.sum(s*s))
def main():
 w=build_w33();edges=[(a,b) for a in range(40) for b in range(a+1,40) if w.adj[a,b]]
 ei={e:i for i,e in enumerate(edges)};assert len(edges)==240
 def signed(g):
  M=np.zeros((240,240))
  for j,(a,b) in enumerate(edges):
   x,y=int(g(a)),int(g(b));u,v=(x,y) if x<y else (y,x)
   M[ei[(u,v)],j]=1 if x<y else -1
  return M
 classes=w.G.conjugacy_classes()
 c40=[c for c in classes if len(c)==40 and int(next(iter(c)).order())==3]
 c45=[c for c in classes if len(c)==45 and int(next(iter(c)).order())==2]
 assert len(c40)==2 and len(c45)==1
 def ckey(c):return min(tuple(int(g(i)) for i in range(40)) for g in c)
 c40=sorted(c40,key=ckey)
 C1=sum((signed(g) for g in c40[0]),np.zeros((240,240)))
 C2=sum((signed(g) for g in c40[1]),np.zeros((240,240)))
 M45=sum((signed(g) for g in c45[0]),np.zeros((240,240)))
 S=C1+C2;D40=C1-C2;I=np.eye(240);vals=[32,20,0,8]
 P15=spectral_projector(S,32,vals);P24=spectral_projector(S,20,vals)
 P81=spectral_projector(S,0,vals);P8=spectral_projector(S,8,vals)
 P30=(P8@(M45+3*I))/(-12);P90=(P8@(M45+15*I))/12
 P={15:(P15+P15.T)/2,24:(P24+P24.T)/2,81:(P81+P81.T)/2,
    30:(P30+P30.T)/2,90:(P90+P90.T)/2}
 B={k:basis(v) for k,v in P.items()};assert {k:v.shape[1] for k,v in B.items()}=={15:15,24:24,81:81,30:30,90:90}
 B90=B[90];J90=B90.T@D40@B90/math.sqrt(192)
 assert np.linalg.norm(J90@J90+np.eye(90))<1e-10
 # Point-to-edge incidence contractions.
 D=np.zeros((40,240));Q=np.zeros((40,240))
 for e,(a,b) in enumerate(edges):D[a,e]=-1;D[b,e]=1;Q[a,e]=Q[b,e]=1
 Pp15=spectral_projector(w.adj.astype(float),-4,[12,2,-4]);Pp24=spectral_projector(w.adj.astype(float),2,[12,2,-4])
 Tv=np.einsum('ve,ei,ej->vij',Q,B90,B90,optimize=True)
 def vt(target,Pp):return np.einsum('at,va,vij->tij',D@B[target],Pp,Tv,optimize=True)
 T15=vt(15,Pp15);T24=vt(24,Pp24)
 # Edge flows as skew 40x40 matrices; K=I or point adjacency.
 X=[]
 for i in range(90):
  Z=np.zeros((40,40))
  for e,(a,b) in enumerate(edges):Z[a,b]=B90[e,i];Z[b,a]=-B90[e,i]
  X.append(Z)
 def comm(target,K):
  T=np.zeros((target,90,90));Bt=B[target]
  for i in range(90):
   for j in range(90):
    C=X[i]@K@X[j]-X[j]@K@X[i]
    T[:,i,j]=Bt.T@np.array([C[a,b] for a,b in edges])
  return T
 A30I=comm(30,np.eye(40));A30A=comm(30,w.adj.astype(float));A81A=comm(81,w.adj.astype(float))
 zero=max(np.max(np.abs(comm(t,K))) for t in (15,24) for K in (np.eye(40),w.adj.astype(float)))
 def jtwist(T):
  return np.einsum('tkj,ki->tij',T,J90,optimize=True)+np.einsum('tki,kj->tij',T,J90,optimize=True)
 S30J=jtwist(A30I);S81J=jtwist(A81A)
 T={'S15':(T15,15),'S24':(T24,24),'A30I':(A30I,30),'A30A':(A30A,30),
    'A81A':(A81A,81),'S30J':(S30J,30),'S81J':(S81J,81)}
 expected={'S15':(15,4.0,240.0),'S24':(24,5.67340286,772.5),'A30I':(30,1.0,30.0),
           'A30A':(30,math.sqrt(10),300.0),'A81A':(81,math.sqrt(15),1215.0),
           'S30J':(30,math.sqrt(2),60.0),'S81J':(81,math.sqrt(30),2430.0)}
 stats={}
 for name,(tensor,target) in T.items():
  rank,hi,lo,n2=tensor_stats(tensor);er=expected[name]
  assert rank==er[0] and abs(hi-er[1])<1e-7 and abs(lo-er[1])<1e-7 and abs(n2-er[2])<1e-6
  stats[name]={'target':target,'rank':rank,'singular_value':hi,'tensor_norm_squared':n2}
 assert zero<1e-12
 # Outer chirality parity.
 outer=matrix_perm(w,np.diag([1,2,1,2]));O=signed(outer);Oc={k:B[k].T@O@B[k] for k in B}
 assert np.linalg.norm(Oc[90]@J90@Oc[90].T+J90)<1e-10
 def perr(tensor,target,eta):
  left=np.einsum('ab,bij->aij',Oc[target],tensor,optimize=True)
  right=np.einsum('akl,ki,lj->aij',tensor,Oc[90],Oc[90],optimize=True)
  return float(np.max(np.abs(left-eta*right)))
 parity={n:(-1 if n in ('S30J','S81J') else 1) for n in T}
 assert max(perr(t,targ,parity[n]) for n,(t,targ) in T.items())<1e-10
 # Simultaneous internal mu6 rotation on both inputs.
 U=.5*np.eye(90)+math.sqrt(3)/2*J90
 def transform(tensor,R):return np.einsum('akl,ki,lj->aij',tensor,R,R,optimize=True)
 orbitdim={}
 for n,(tensor,_) in T.items():
  rows=[];R=np.eye(90)
  for _ in range(6):rows.append(transform(tensor,R).ravel());R=R@U
  orbitdim[n]=int(np.linalg.matrix_rank(np.vstack(rows),tol=1e-8))
 assert orbitdim=={'S15':1,'S24':3,'A30I':3,'A30A':3,'A81A':3,'S30J':1,'S81J':1}
 cert=json.loads(CERT.read_text());assert cert['sha256_without_hash_field']==EXPECTED==digest(cert);assert all(cert['checks'].values())
 out={'status':'PASS','blocks':{str(k):v.shape[1] for k,v in B.items()},'J2_error':float(np.linalg.norm(J90@J90+np.eye(90))),
      'zero_antisymmetric_15_24':float(zero),'maps':stats,'chirality_parity':parity,'mu6_orbit_dimension':orbitdim,'certificate':EXPECTED}
 print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=='__main__':main()
