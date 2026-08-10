#!/usr/bin/env python3
"""Pass 4781 — exact covering-radius and Hamiltonian landscape bounds.

A radius-14 H10 coset is exhibited explicitly.  Since H10^perp has distance 4,
every H10 coset is an OA of strength 3; the first three Krawtchouk moment
equations plus complement symmetry exclude coset minimum >=17. Thus
14 <= rho(H10) <= 16.

For the 270-check syndrome code, every one of the 540 dependency triangles has
even syndrome parity. Incidence counting gives wt(s)<=180. Equality would force
the 90 zero coordinates to meet every dependency triangle exactly once. An exact
binary MILP proves that perfect transversal infeasible, hence wt(s)<=179.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy import sparse
from w33_pass4495_4502_distance_prism_reconstruction import geometry

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4781_HAMILTONIAN_COVERING_BOUNDS.json'
WITNESS=253626779097

def gf2_basis(vals):
    piv={};B=[]
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;B.append(y);break
    return B

def span(B):
    V=[0]
    for b in B:V += [x^b for x in V]
    return V

def K(n,j,i):return sum((-1)**s*math.comb(i,s)*math.comb(n-i,j-s) for s in range(max(0,j-(n-i)),min(j,i)+1))

def main()->int:
    pts,pidx,lines,A,apartments,_,_=geometry();A=np.asarray(A,dtype=np.uint8)
    rows=[]
    for i in range(40):
        m=sum(1<<j for j in np.flatnonzero(A[i]));rows.append(m)
    B=gf2_basis(rows);assert len(B)==10;C=span(B);assert len(C)==1024
    enum=Counter(x.bit_count() for x in C);assert enum==Counter({20:672,16:135,24:135,12:40,28:40,0:1,40:1})
    dist=Counter((WITNESS^c).bit_count() for c in C)
    assert min(dist)==14 and dist==Counter({20:256,18:192,22:192,16:128,24:128,14:64,26:64})

    # OA strength 3 moment obstruction to a coset with all weights >=17.
    # Complement symmetry comes from 1^40 in H10; parity is constant because H10 is even.
    # Odd candidate: weights 17,19,21,23. Even candidate: 18,20,22.
    for weights in ([17,19,21,23],[18,20,22]):
        xs=sp.symbols('x:'+str(len(weights)),nonnegative=True)
        eq=[sp.Eq(sum(xs),1024)]
        for j in range(1,4):eq.append(sp.Eq(sum(xs[k]*K(40,j,w) for k,w in enumerate(weights)),0))
        # Add complement symmetry.
        for k,w in enumerate(weights):
            if 40-w in weights and w<40-w:eq.append(sp.Eq(xs[k],xs[weights.index(40-w)]))
        sol=sp.solve(eq,xs,dict=True)
        assert not sol or all(any(v.is_number and v<0 for v in s.values()) for s in sol)

    # Reconstruct the 270 weight-4 dual checks and their 540 minimum dependencies.
    residues=[]
    for S in itertools.combinations(range(40),4):
        if not np.any(np.sum(A[:,S],axis=1)&1):residues.append(S)
    assert len(residues)==270;rm=[sum(1<<i for i in S) for S in residues]
    cold=[set() for _ in range(270)]
    for i,j in itertools.combinations(range(270),2):
        if (rm[i]&rm[j]).bit_count()==2:cold[i].add(j);cold[j].add(i)
    dep=[]
    for a in range(270):
        for b in (x for x in cold[a] if x>a):
            for c in cold[a]&cold[b]:
                if c>b and rm[a]^rm[b]^rm[c]==0:dep.append((a,b,c))
    assert len(dep)==540 and Counter(i for t in dep for i in t)==Counter({i:6 for i in range(270)})

    # If a syndrome y had weight 180, each dependency triangle would contain
    # exactly two y=1 coordinates, so z=1+y would meet each triangle exactly once.
    rr=[];cc=[];dd=[]
    for r,t in enumerate(dep):
        for i in t:rr.append(r);cc.append(i);dd.append(1.)
    M=sparse.coo_matrix((dd,(rr,cc)),shape=(540,270)).tocsr()
    R=milp(np.zeros(270),integrality=np.ones(270),bounds=Bounds(np.zeros(270),np.ones(270)),
           constraints=LinearConstraint(M,np.ones(540),np.ones(540)),options={'presolve':True})
    assert R.status==2

    synd=lambda x:sum(((x&r).bit_count()&1) for r in rm)
    sw=synd(WITNESS);assert sw==156
    out={'pass':4781,'H10':{'parameters':'[40,10,12]','covering_radius_lower_bound':14,'covering_radius_upper_bound':16,
      'radius14_witness':WITNESS,'witness_weight':WITNESS.bit_count(),'witness_coset_weight_distribution':dict(sorted(dist.items())),
      'upper_bound_reason':'dual distance 4 => every coset OA strength 3; Krawtchouk moments plus all-one complement symmetry exclude minimum >=17',
      'unresolved':'rho=14,15,or16; no equality beyond these bounds is claimed'},
      'syndrome_code':{'parameters':'[270,30,27]','dependency_triangles':540,'checks_per_dependency_incidence':6,
        'weight_upper_bound_by_incidence':180,'weight180_exact_transversal_feasible':False,'certified_weight_upper_bound':179,
        'radius14_witness_syndrome_weight':sw},
      'Hamiltonian':{'H':'-sum_R prod_{i in R} Z_i','energy_from_syndrome_weight':'E=-270+2s','certified_energy_ceiling':88},
      'theorem':'The H10 covering radius is rigorously bracketed 14<=rho<=16. Independently, no 270-check syndrome can have weight 180, so every commuting-check energy lies at or below 88.',
      'boundary':'The covering radius is not yet determined exactly; the certificate intentionally records the unresolved 14/15/16 trichotomy.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
