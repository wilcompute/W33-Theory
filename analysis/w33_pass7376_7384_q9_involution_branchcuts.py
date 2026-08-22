#!/usr/bin/env python3
"""Pass7376-7384: exact C2-invariant quotient model for the frozen q=9 51-set.

The parallel Pass7213-7215 lane independently proves that the frozen 51-set has
projective symplectic stabilizer exactly C2. Pass7337-7352 exhibits an explicit
symplectic lift A with A^2=-I. This pass quotients the *A-invariant branch* of the
partial-ovoid problem and computes its line-clique LP bounds.

Important: a hypothetical unrestricted 52-set need not be A-invariant. Therefore
this quotient is a branch/search reduction, never a WLOG global reduction.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,csr_matrix
from w33_pass7107_q9_target_52 import ADD,MUL,NEG,INV,build,check_field

ROOT=Path(__file__).resolve().parents[1]
WIT=ROOT/'data'/'PART_W33_Q9_PARTIAL_OVOID_51.json'
OUT=ROOT/'data'/'PART_W33_PASS7376_7384_Q9_INVOLUTION_BRANCHCUTS.json'

A=[[6,0,0,0],[6,3,1,2],[1,0,4,2],[1,0,7,8]]

def sumf(xs):
    z=0
    for x in xs:z=ADD[z][x]
    return z

def mv(M,x):return tuple(sumf(MUL[M[i][j]][x[j]] for j in range(4)) for i in range(4))
def canon(v):
    z=INV[next(x for x in v if x)];return tuple(MUL[z][x] for x in v)
def add(u,v):return tuple(ADD[a][b] for a,b in zip(u,v))
def scale(a,v):return tuple(MUL[a][x] for x in v)
def line_through(a,b,pi):return frozenset([pi[canon(b)]]+[pi[canon(add(a,scale(t,b)))] for t in range(9)])

def lp(c,Aub,bub,Aeq=None,beq=None):
    r=linprog(c,A_ub=Aub,b_ub=bub,A_eq=Aeq,b_eq=beq,bounds=(0,1),method='highs')
    assert r.success
    return float(-r.fun)

def main():
    check_field();P,adj,B=build();pi={p:i for i,p in enumerate(P)};assert len(P)==820
    S=set(map(int,json.loads(WIT.read_text())['point_indices']));assert len(S)==51
    perm=tuple(pi[canon(mv(A,p))] for p in P);assert all(perm[perm[i]]==i for i in range(820))
    assert {perm[s] for s in S}==S
    orbs=[];seen=set()
    for i in range(820):
        if i in seen:continue
        O=tuple(sorted({i,perm[i]}));seen.update(O);orbs.append(O)
    assert Counter(map(len,orbs))==Counter({2:400,1:20})
    oi={p:k for k,O in enumerate(orbs) for p in O}

    # Exact isotropic lines.
    L=set()
    for a in range(820):
        for b in adj[a]:
            if a<b:L.add(line_through(P[a],P[b],pi))
    assert len(L)==820 and {len(x) for x in L}=={10}

    # An orbit containing two collinear points can never be selected invariantly.
    forbidden=[]
    for k,O in enumerate(orbs):
        if len(O)==2 and O[1] in adj[O[0]]:forbidden.append(k)
    assert len(forbidden)==40
    allowed=[k for k in range(len(orbs)) if k not in set(forbidden)]
    vi={k:i for i,k in enumerate(allowed)}
    assert Counter(len(orbs[k]) for k in allowed)==Counter({2:360,1:20})

    rr=[];cc=[];vv=[]
    for r,X in enumerate(L):
        cnt=Counter(oi[p] for p in X if oi[p] in vi)
        for k,n in cnt.items():
            assert n==1  # all internally-collinear 2-orbits were removed
            rr.append(r);cc.append(vi[k]);vv.append(1.0)
    Aline=coo_matrix((vv,(rr,cc)),shape=(820,len(allowed))).tocsr()
    weights=np.array([len(orbs[k]) for k in allowed],dtype=float)
    base=lp(-weights,Aline,np.ones(820))
    fixed=[vi[k] for k in allowed if len(orbs[k])==1]
    def fixed_lp(nfix):
        row=np.zeros(len(allowed));row[fixed]=1
        return lp(-weights,Aline,np.ones(820),csr_matrix(row.reshape(1,-1)),np.array([nfix],float))
    b0=fixed_lp(0);b1=fixed_lp(1);b2=fixed_lp(2)
    assert abs(base-74)<1e-7 and abs(b0-72)<1e-7 and abs(b1-73)<1e-7 and abs(b2-74)<1e-7

    # The frozen witness quotient is 1 fixed point + 25 two-cycles = 51.
    selected={oi[s] for s in S};assert sum(len(orbs[k]) for k in selected)==51
    assert Counter(len(orbs[k]) for k in selected)==Counter({2:25,1:1})

    # Even target 52 requires an even number of fixed points. The 20 fixed points
    # are two isotropic lines, so an invariant partial ovoid uses at most 2 fixed
    # points total: branches nfix=0 or 2 are exhaustive *within this C2 class*.
    fixedpts=[O[0] for O in orbs if len(O)==1];assert len(fixedpts)==20
    fixed_lines=[X for X in L if len(X&set(fixedpts))==10];assert len(fixed_lines)==2

    out={'schema':'w33.pass7376_7384.q9_involution_branchcuts.v1','status':'PASS',
      'involution':{'point_orbits':420,'fixed_points':20,'two_cycles':400,'internally_collinear_two_cycles_forbidden':40,
                    'allowed_orbit_variables':380,'frozen_51_quotient':'1 fixed + 25 two-cycles'},
      'fixed_locus':'two disjoint isotropic 10-point lines',
      'line_clique_quotient':{'constraints':820,'LP_bound':base,'branch_fixed0_LP':b0,'branch_fixed1_LP':b1,'branch_fixed2_LP':b2},
      'target52_invariant_branches':'fixed-point count 0 or 2 only',
      'boundary':'This is an exact quotient/LP theorem for the A-invariant symmetry class. It does not prove alpha(W(3,9))<=51 and cannot exclude asymmetric 52-sets.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','vars':380,'LP':74,'target52_fixed_branches':[0,2]}))
if __name__=='__main__':main()
