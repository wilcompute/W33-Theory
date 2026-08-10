#!/usr/bin/env python3
"""Pass 4739: test, rather than assume, the q-family generalization.

The q=3 theorem says that the 270 four-fixed-line inner involutions are exactly
all minimum words of ker_2(A_*).  This script checks the nearby prime cases
q=2,3,5,7 directly from W(3,q).

Findings:
* q=2: rank_2(A_*)=14, kernel dimension 1, d=15 (the all-one word).
* q=3: rank=10=q^2+1 and d=4; the elliptic projective involution fixes four
  pairwise-skew lines and its mask lies in the kernel (the established case).
* q=5: rank=26=q^2+1, but an exact MILP proves d=6.  The canonical elliptic
  projective involution fixes EIGHT lines, not six, so it is not a minimum word.
  A minimum witness is a six-line pairwise-skew partial spread.
* q=7: rank=50=q^2+1.  The canonical elliptic involution fixes eight=q+1
  pairwise-skew lines and gives a kernel word of weight 8 (upper bound d<=8;
  this script does not claim the MILP lower bound at q=7).

Thus the exact q=3 statement does NOT generalize as 'involution fixed sets are
the complete minimum shell'.  There is a mod-4 branch already visible in the
elliptic fixed-set geometry: for q=3,7 (q=3 mod 4) the canonical J-action fixes
q+1 pairwise-skew lines, while at q=5 (q=1 mod 4) it fixes q+3=8 lines and the
true kernel minimum is smaller.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy import sparse

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4739_W3Q_INVOLUTION_MINIMUM_SHELL.json'

def norm(v,q):
    v=tuple(int(x)%q for x in v)
    for x in v:
        if x:
            z=pow(x,-1,q);return tuple((z*y)%q for y in v)
    raise ValueError('zero')

def geometry(q):
    pts=[]
    for lead in range(4):
        for tail in itertools.product(range(q),repeat=3-lead):
            pts.append((0,)*lead+(1,)+tail)
    pidx={p:i for i,p in enumerate(pts)}
    J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%q
    def sy(x,y):return int(np.array(x)@J@np.array(y))%q
    lines=set()
    for i,x in enumerate(pts):
        for y in pts[i+1:]:
            if sy(x,y):continue
            S=set()
            for a,b in itertools.product(range(q),repeat=2):
                if a or b:S.add(pidx[norm(tuple((a*u+b*v)%q for u,v in zip(x,y)),q)])
            if len(S)==q+1:lines.add(frozenset(S))
    lines=sorted(lines,key=lambda S:tuple(sorted(S)));lidx={L:i for i,L in enumerate(lines)}
    A=np.zeros((len(lines),len(lines)),dtype=np.uint8)
    for i,j in itertools.combinations(range(len(lines)),2):
        if lines[i]&lines[j]:A[i,j]=A[j,i]=1
    return pts,pidx,lines,lidx,A,J

def gf2_rank(M):
    piv={}
    for i in range(M.shape[0]):
        x=sum((int(M[i,j])&1)<<j for j in range(M.shape[1]))
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def line_perm(q,pts,pidx,lines,lidx,M):
    out=[]
    for L in lines:
        T=frozenset(pidx[norm(tuple((M@np.array(pts[i]))%q),q)] for i in L)
        out.append(lidx[T])
    return tuple(out)

def fixed_word(q,pts,pidx,lines,lidx,M,A):
    p=line_perm(q,pts,pidx,lines,lidx,M)
    F=[i for i,x in enumerate(p) if i==x]
    v=np.zeros(len(lines),dtype=np.uint8);v[F]=1
    return F,bool(not np.any((A@v)&1)),all(not A[i,j] for i,j in itertools.combinations(F,2))

def exact_kernel_min(A,time_limit=40):
    n=A.shape[0];rr=[];cc=[];dd=[]
    for i in range(n):
        for j in np.flatnonzero(A[i]):rr.append(i);cc.append(int(j));dd.append(1.0)
        rr.append(i);cc.append(n+i);dd.append(-2.0)
    M=sparse.coo_matrix((dd,(rr,cc)),shape=(n,2*n)).tocsr()
    c=np.zeros(2*n);c[:n]=1
    lb=np.zeros(2*n);ub=np.ones(2*n);ub[n:]=max(2,n//2)
    con=LinearConstraint(M,np.zeros(n),np.zeros(n))
    nz=sparse.csr_matrix(([1.0]*n,([0]*n,list(range(n)))),shape=(1,2*n))
    nonzero=LinearConstraint(nz,[1],[n])
    R=milp(c,integrality=np.ones(2*n),bounds=Bounds(lb,ub),constraints=[con,nonzero],
           options={'time_limit':time_limit,'presolve':True})
    assert R.success, R.message
    S=tuple(int(i) for i in np.flatnonzero(R.x[:n]>.5))
    return int(round(R.fun)),S

def main():
    out={'pass':4739,'cases':{}}
    for q in (2,3,5,7):
        pts,pidx,lines,lidx,A,J=geometry(q);n=len(lines);r=gf2_rank(A)
        assert n==(q+1)*(q*q+1)
        d=None;witness=None
        if q==2:
            assert n-r==1;d=15;witness=tuple(range(15))
        elif q in (3,5):
            d,witness=exact_kernel_min(A)
        J2=np.array([[0,1],[-1,0]],dtype=int)%q
        ell=np.block([[J2,np.zeros((2,2),int)],[np.zeros((2,2),int),J2]])%q
        split=np.diag([1,1,q-1,q-1])%q
        rec={'lines':n,'binary_adjacency_rank':r,'kernel_dimension':n-r}
        if q>2:
            Fe,ke,se=fixed_word(q,pts,pidx,lines,lidx,ell,A)
            Fs,ks,ss=fixed_word(q,pts,pidx,lines,lidx,split,A)
            rec.update({'elliptic_fixed_lines':len(Fe),'elliptic_mask_in_kernel':ke,
                        'elliptic_fixed_lines_pairwise_skew':se,
                        'split_fixed_lines':len(Fs),'split_mask_in_kernel':ks,
                        'split_formula_matches_(q+1)^2':len(Fs)==(q+1)**2})
        if d is not None:
            rec['exact_kernel_minimum']=d;rec['minimum_witness']=list(witness)
            rec['minimum_witness_pairwise_skew']=all(not A[i,j] for i,j in itertools.combinations(witness,2))
        else:
            rec['exact_kernel_minimum']='not claimed';rec['certified_upper_bound']=len(Fe)
        out['cases'][str(q)]=rec
    assert out['cases']['2']['exact_kernel_minimum']==15
    assert out['cases']['3']['exact_kernel_minimum']==4
    assert out['cases']['5']['exact_kernel_minimum']==6
    assert out['cases']['5']['elliptic_fixed_lines']==8
    assert out['cases']['7']['elliptic_fixed_lines']==8
    assert [out['cases'][str(q)]['binary_adjacency_rank'] for q in (3,5,7)]==[10,26,50]
    out['theorem_boundary']='The q=3 minimum-shell=involution-shell identification is exceptional as stated: q=5 has d=6 while the canonical elliptic projective involution fixes 8 lines.  The odd-q adjacency ranks tested are q^2+1, but no new all-q rank theorem is claimed here.'
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
