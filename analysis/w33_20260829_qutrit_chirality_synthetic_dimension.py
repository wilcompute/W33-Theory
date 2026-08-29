#!/usr/bin/env python3
"""Exact 3x2 normal form for the six near-ovoid microstates.

The prior six-state certificate proves image C3 x S3, a unique 3+3 block
system, block-fixing subgroup C3 x C3, and quotient C2.  This script exhibits
the canonical wreath normal form on labels |chi,t>, chi in F2, t in F3.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
from collections import Counter,deque
from sympy import Matrix,symbols,factor
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_QUTRIT_CHIRALITY_SYNTHETIC_DIMENSION.json'

def idx(chi,t): return 3*chi+(t%3)
def compose(p,q): return tuple(p[q[i]] for i in range(6))
def order(p):
    seen=set();o=1
    for i in range(6):
        if i in seen: continue
        j=i;n=0
        while j not in seen:seen.add(j);n+=1;j=p[j]
        o=math.lcm(o,n)
    return o

def perm(fn): return tuple(idx(*fn(i//3,i%3)) for i in range(6))
def closure(gens):
    e=tuple(range(6));G={e};Q=deque([e])
    while Q:
        a=Q.popleft()
        for g in gens:
            h=compose(g,a)
            if h not in G:G.add(h);Q.append(h)
    return G

def pmat(p):
    M=Matrix.zeros(6)
    for j,i in enumerate(p):M[i,j]=1
    return M

def main():
    # z is the central/common qutrit translation; r is the anti-diagonal
    # translation; s swaps chirality and inverts r by conjugation.
    z=perm(lambda c,t:(c,t+1))
    r=perm(lambda c,t:(c,t+(1 if c==0 else -1)))
    s=perm(lambda c,t:(1-c,t))
    G=closure([z,r,s]);assert len(G)==18
    e=tuple(range(6)); rinv=next(p for p in G if compose(r,p)==e)
    assert compose(s,compose(r,s))==rinv
    assert all(compose(z,g)==compose(g,z) for g in G)
    center=[g for g in G if all(compose(g,h)==compose(h,g) for h in G)];assert len(center)==3
    assert Counter(map(order,G))==Counter({1:1,2:3,3:8,6:6})

    # unique nontrivial 3+3 block system.
    systems=[];all6=set(range(6))
    for A0 in itertools.combinations(range(6),3):
        A=set(A0);B=all6-A
        if min(B)<min(A):continue
        if all(({g[i] for i in A}==A and {g[i] for i in B}==B) or ({g[i] for i in A}==B and {g[i] for i in B}==A) for g in G):systems.append((A,B))
    assert len(systems)==1

    # Minimal translation+chirality Hamiltonian.  This is an exact synthetic
    # 3-cycle x 2-leg ladder normal form, not a physical energy assignment.
    coupling=symbols('g'); x=symbols('x')
    H=pmat(z)+pmat(z).T+coupling*pmat(s)
    char=factor(H.charpoly(x).as_expr())
    expected=factor(((x-2)**2-coupling**2)*((x+1)**2-coupling**2)**2)
    assert factor(char-expected)==0

    out={
      'schema':'w33.20260829.qutrit-chirality-synthetic-dimension.v1','status':'PASS',
      'stateSpace':'F3 x F2','dimension':6,
      'group':{'order':18,'structure':'C3 x S3 = (C3 x C3) : C2','center':'C3 common qutrit translation',
               'elementOrders':{'1':1,'2':3,'3':8,'6':6}},
      'coordinates':{
        'z':'(chi,t)->(chi,t+1), central/common qutrit shift',
        'r':'(0,t)->(0,t+1), (1,t)->(1,t-1), anti-diagonal qutrit shift',
        's':'(chi,t)->(1-chi,t), chirality swap',
        'relation':'s r s = r^-1; z commutes with r and s'},
      'blockSystem':{'unique':'3+3','interpretation':'chi is selected by which residual hinge point lies in the high-release tetrad'},
      'syntheticHamiltonian':{'form':'H = Z + Z^dagger + g X_chi','characteristic':'((x-2)^2-g^2) ((x+1)^2-g^2)^2',
        'levels':'2+g, 2-g, (-1+g)^2, (-1-g)^2'},
      'reading':'The six local microstates admit an exact two-leg, three-site synthetic-coordinate normal form. The C3 center is a common qutrit translation and the C2 quotient is the chirality leg swap.',
      'boundary':'Finite permutation-group/synthetic-coordinate statement. The coordinate is analogous to synthetic dimensions used in photonics; no laboratory mode assignment, magnetic flux, or particle chirality is inferred.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','group':18,'factorization':'3x2','charpoly':str(char)}))
if __name__=='__main__':main()
