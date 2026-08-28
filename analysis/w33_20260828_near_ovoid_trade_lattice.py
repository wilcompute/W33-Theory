#!/usr/bin/env python3
"""Exact global trade lattice of the 2880 optimal W(3,3) near-ovoids.

Every oriented collinear pair (a,b) has six optimal ten-point completions with
the same line-occupancy vector. Differences of completions are therefore
integer vectors in ker(N), where N is the 40x40 line-point incidence matrix.

This program proves that the local trades generate the entire integral
incidence kernel. Equivalently they generate the canonical 15-dimensional
(-4)-eigenspace lattice of the W33 point graph.

The proof is finite and exact:
* rebuild W(3,3) from F_3^4;
* enumerate all 480 oriented defect dipoles and all six completions each;
* verify 2880 unique optima;
* take five base-relative trades in every six-fibre;
* verify all trades lie in ker(N) and have support 12 (= six +1, six -1);
* compute rational/mod-p ranks;
* compute the Smith form. Its fifteen nonzero factors are all 1.

Since ker_Z(N) is saturated and the trade lattice is a primitive rank-15
sublattice with the same rational span, the two lattices are equal.
"""
from __future__ import annotations
import itertools, json
from collections import Counter
from pathlib import Path
from fractions import Fraction

Q=3
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"PART_W33_20260828_NEAR_OVOID_TRADE_LATTICE.json"

def norm(v):
    i=next(k for k,x in enumerate(v) if x%Q)
    z=pow(v[i]%Q,-1,Q)
    return tuple((z*x)%Q for x in v)

def form(u,v):
    return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%Q

def geometry():
    pts=sorted({norm(v) for v in itertools.product(range(Q),repeat=4) if any(v)})
    idx={v:i for i,v in enumerate(pts)}
    lines=set()
    for ia,ib in itertools.combinations(range(40),2):
        a,b=pts[ia],pts[ib]
        if form(a,b): continue
        span=set()
        for s,t in itertools.product(range(Q),repeat=2):
            if s==t==0: continue
            span.add(idx[norm(tuple((s*a[k]+t*b[k])%Q for k in range(4)))])
        if len(span)==4: lines.add(tuple(sorted(span)))
    lines=sorted(lines)
    assert len(pts)==len(lines)==40
    return pts,lines

def solve_target(lines, point_lines, target):
    allowed=[p for p in range(40) if all(target[li]>0 for li in point_lines[p])]
    A=set(allowed); cand=[[p for p in L if p in A] for L in lines]
    counts=[0]*40; chosen=[]; sols=set()
    def rec():
        if len(chosen)>10: return
        unmet=[]
        for li,t in enumerate(target):
            if counts[li]>t: return
            need=t-counts[li]
            if need:
                feasible=[p for p in cand[li] if p not in chosen and
                          all(counts[lj]<target[lj] for lj in point_lines[p])]
                if len(feasible)<need: return
                unmet.append((len(feasible),-need,li,feasible))
        if not unmet:
            if len(chosen)==10: sols.add(tuple(sorted(chosen)))
            return
        _,neg,_,feasible=min(unmet); need=-neg
        for sub in itertools.combinations(feasible,need):
            delta=Counter()
            for p in sub:
                for lj in point_lines[p]: delta[lj]+=1
            if any(counts[lj]+d>target[lj] for lj,d in delta.items()): continue
            chosen.extend(sub)
            for lj,d in delta.items(): counts[lj]+=d
            rec()
            for lj,d in delta.items(): counts[lj]-=d
            del chosen[-len(sub):]
    rec()
    return sorted(sols)

def rank_mod(rows,p):
    A=[[x%p for x in r] for r in rows if any(x%p for x in r)]
    if not A:return 0
    m,n=len(A),len(A[0]); r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if A[i][c]),None)
        if piv is None: continue
        A[r],A[piv]=A[piv],A[r]
        inv=pow(A[r][c],-1,p)
        A[r]=[(inv*x)%p for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                z=A[i][c]
                A[i]=[(A[i][j]-z*A[r][j])%p for j in range(n)]
        r+=1
        if r==m:return r
    return r

def rank_q(rows):
    A=[[Fraction(x) for x in r] for r in rows if any(r)]
    if not A:return 0
    m,n=len(A),len(A[0]); r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if A[i][c]),None)
        if piv is None: continue
        A[r],A[piv]=A[piv],A[r]
        z=A[r][c]; A[r]=[x/z for x in A[r]]
        for i in range(r+1,m):
            if A[i][c]:
                z=A[i][c]
                A[i]=[A[i][j]-z*A[r][j] for j in range(n)]
        r+=1
        if r==m:return r
    return r

def main():
    _,lines=geometry()
    point_lines=[[] for _ in range(40)]
    N=[[0]*40 for _ in range(40)]
    for li,L in enumerate(lines):
        for p in L:
            point_lines[p].append(li);N[li][p]=1
    pencils=point_lines

    all_opt=set(); fibres=[]; trades=[]
    oriented=0
    for a in range(40):
        for b in range(40):
            if a==b: continue
            hinge=set(pencils[a])&set(pencils[b])
            if len(hinge)!=1: continue
            oriented+=1
            h=next(iter(hinge))
            miss=sorted(set(pencils[a])-{h})
            doub=sorted(set(pencils[b])-{h})
            target=[1]*40
            for li in miss: target[li]=0
            for li in doub: target[li]=2
            sols=solve_target(lines,point_lines,target)
            assert len(sols)==6
            fibres.append((a,b,sols))
            all_opt.update(sols)
            base=sols[0]
            bv=[int(i in base) for i in range(40)]
            for S in sols[1:]:
                sv=[int(i in S) for i in range(40)]
                d=[sv[i]-bv[i] for i in range(40)]
                assert sum(abs(x) for x in d)==12
                assert Counter(d)==Counter({0:28,1:6,-1:6})
                assert all(sum(N[li][p]*d[p] for p in range(40))==0 for li in range(40))
                trades.append(d)
    assert oriented==480 and len(fibres)==480 and len(all_opt)==2880
    assert len(trades)==2400
    raw=0
    for _,_,sols in fibres:
        for A,B in itertools.combinations(sols,2):
            raw+=1
            d=[int(i in B)-int(i in A) for i in range(40)]
            assert Counter(d)==Counter({0:28,1:6,-1:6})
    assert raw==7200

    rankN={str(p):rank_mod(N,p) for p in (2,3,5,7)}
    rankT={str(p):rank_mod(trades,p) for p in (2,3,5,7)}
    assert rankN=={"2":25,"3":25,"5":25,"7":25}
    assert rankT=={"2":15,"3":15,"5":15,"7":15}
    rq=rank_q(trades); assert rq==15

    from sympy import Matrix, ZZ
    from sympy.matrices.normalforms import smith_normal_form
    D=smith_normal_form(Matrix(trades),domain=ZZ)
    diag=[abs(int(D[i,i])) for i in range(min(D.shape)) if D[i,i]!=0]
    assert diag==[1]*15

    out={
      "schema":"w33.20260828.near-ovoid-trade-lattice.v1",
      "status":"PASS",
      "optimal_near_ovoids":2880,
      "oriented_defect_dipoles":480,
      "completions_per_dipole":6,
      "local_unordered_pair_trades":7200,
      "base_relative_generators":2400,
      "trade_profile":{"support":12,"plus_ones":6,"minus_ones":6},
      "incidence_matrix":{"shape":[40,40],"rank_mod":rankN,"kernel_dimension":15},
      "trade_lattice":{"rank_Q":rq,"rank_mod":rankT,"smith_nonzero_diagonal":diag,
                       "primitive":True,"equals_integral_incidence_kernel":True},
      "spectral_identification":"ker(N) is the -4 eigenspace of the W33 point graph because N^T N=A+4I",
      "theorem":"Differences of the six optimal near-ovoid completions over all 480 oriented defect dipoles generate exactly ker_Z(N), the primitive rank-15 integral W33 incidence-kernel lattice. Every elementary local trade has six +1 and six -1 coordinates.",
      "boundary":"This is an exact finite lattice theorem. It does not identify this 15-dimensional module with a physical Hilbert space or with any unrelated 15-state carrier."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","rank":15,"smith":"1^15","optima":2880,"pair_trades":7200}))

if __name__=="__main__": main()
