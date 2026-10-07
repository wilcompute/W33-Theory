#!/usr/bin/env python3
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def gammas():
 sx=np.array([[0,1],[1,0]],complex);sy=np.array([[0,-1j],[1j,0]],complex);sz=np.diag([1,-1]).astype(complex);I=np.eye(2)
 g=[np.kron(sx,s) for s in [sx,sy,sz]]+[np.kron(sy,I)];return g,g[0]@g[1]@g[2]@g[3]
def links(L,q):
 sites=list(itertools.product(range(L),repeat=4));idx={x:i for i,x in enumerate(sites)};U=np.ones((len(sites),4),complex)
 for i,x in enumerate(sites):
  for first in (0,2):
   U[i,first]=np.exp(-2j*np.pi*q*x[first+1]/L**2)
   if x[first+1]==L-1:U[i,first+1]=np.exp(2j*np.pi*q*x[first]/L)
 T=[]
 for mu in range(4):
  M=np.zeros((len(sites),len(sites)),complex)
  for i,x in enumerate(sites):
   y=list(x);y[mu]=(y[mu]+1)%L;M[i,idx[tuple(y)]]=U[i,mu]
  T.append(M)
 return T
def index_gap(L,q,mass):
 g,g5=gammas();T=links(L,q);n=L**4;G=np.kron(np.eye(n),g5);I4=np.eye(4)
 W=(4-mass)*np.eye(4*n,dtype=complex)
 for mu in range(4):
  W-=(np.kron(T[mu],I4-g[mu])+np.kron(T[mu].conj().T,I4+g[mu]))/2
 w=np.linalg.eigvalsh(G@W)
 return int(round(-np.sign(w).sum()/2)),float(min(abs(w)))
scan=[]
for mass in (1.6,1.7,1.8):
 idx,gap=index_gap(5,6,mass);scan.append({'L':5,'q':6,'mass':mass,'index':idx,'gap':gap});print(scan[-1],flush=True)
assert scan[0]['index']==-35
assert [r['index'] for r in scan[1:]]==[-36,-36]
assert scan[-1]['gap']>.08
out={'status':'PASS_Q6_OVERLAP_INDEX_MINUS36_RESOLVED_ON_L5',
     'scan':scan,
     'theorem':'The largest primitive SM hypercharge magnitude q=6 has a well-defined overlap phase on the L=5 background: after the finite-volume spectral-flow crossing, m0=1.7 and 1.8 give index -36=-q^2 with nonzero Wilson gap.',
     'boundary':'The admissible phase depends on lattice resolution and Wilson mass; this is not a continuum proof by itself.'}
(ROOT/'data/PART_W33_PASS11592_Q6_OVERLAP_ADMISSIBILITY.json').write_text(json.dumps(out,indent=2,sort_keys=True))
print(json.dumps(out,indent=2))
