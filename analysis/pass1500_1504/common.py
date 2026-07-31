from __future__ import annotations
import hashlib, json, math
from pathlib import Path
import numpy as np
import sympy as sp
import _selector_five_frontiers_impl as ff
from pass1370_1374 import core, modular_radicals
GOOD=1_000_003
ROOT=Path(__file__).resolve().parents[2]
def sha(payload):
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),default=str)
    return hashlib.sha256(raw.encode()).hexdigest()
def capture(): return ff.capture_mackey()
def rank_mod(A,p=GOOD): return ff.rank_mod(np.asarray(A,dtype=np.int64),p)
def rref_key(A,p):
    A=np.asarray(A,dtype=np.int64)%p
    if A.size==0:return ()
    R,_=modular_radicals.rref(A,p)
    return tuple(tuple(int(x) for x in row) for row in R if np.any(row))
def factor_kernel_key(factor,p):
    d=factor[0].shape[0]; eq=[]
    for i in range(d):
      for j in range(d): eq.append([int(factor[a][i,j]) for a in range(len(factor))])
    K=modular_radicals.nullspace(np.asarray(eq,dtype=np.int64)%p,p)
    return rref_key(K,p)
class SparseRank:
    def __init__(self,p): self.p=p; self.pivots={}
    def add(self,row):
      p=self.p; r={int(k):int(v)%p for k,v in row.items() if int(v)%p}
      while r:
        c=min(r)
        if c not in self.pivots:
          inv=pow(r[c],-1,p); r={k:v*inv%p for k,v in r.items() if v*inv%p}; self.pivots[c]=r; return True
        f=r[c]
        for k,v in self.pivots[c].items():
          nv=(r.get(k,0)-f*v)%p
          if nv:r[k]=nv
          else:r.pop(k,None)
      return False
    @property
    def rank(self): return len(self.pivots)
def matrix_stats(M):
    M=sp.Matrix(M); maxnum=0; maxden=1; nnz=0; payload=[]
    for x in M:
      q=sp.Rational(x); payload.append([int(q.p),int(q.q)])
      if q: nnz+=1; maxnum=max(maxnum,abs(int(q.p))); maxden=max(maxden,int(q.q))
    return {"shape":[M.rows,M.cols],"nonzero":nnz,"max_abs_numerator":maxnum,"max_denominator":maxden,"sha256":sha(payload)}
def denominator_lcm(M):
    out=1
    for x in M: out=math.lcm(out,int(sp.Rational(x).q))
    return out
