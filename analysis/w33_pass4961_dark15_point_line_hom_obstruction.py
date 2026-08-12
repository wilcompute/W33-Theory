#!/usr/bin/env python3
"""Pass4961 — exact obstruction to any equivariant point-line dark-15 bridge.

Pass4956 showed ordinary W(3,3) incidence Z transmits the common 24-dimensional
constituent and annihilates the two inequivalent 15-dimensional constituents.
This pass closes the obvious escape route: perhaps a different signed/oriented
point-line matrix could couple the dark 15s while remaining PSp/PGSp-equivariant.

The answer is no.  The group has exactly two orbits on point x line pairs:
incident (160) and nonincident (1440).  Therefore the entire equivariant matrix
space is two-dimensional, spanned by Z and J-Z.  Both basis matrices vanish
from the line 15 to the point 15, so the full Hom space is zero.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np,networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4961_DARK15_POINT_LINE_HOM_OBSTRUCTION.json'

def canon3(v):
    v=np.array(v,dtype=int)%3;j=next(i for i,x in enumerate(v) if x)
    return tuple(int(x) for x in (v*pow(int(v[j]),-1,3))%3)
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def closure(gens,n):
    I=tuple(range(n));S={I};D=deque([I])
    while D:
        a=D.popleft()
        for g in gens:
            z=comp(g,a)
            if z not in S:S.add(z);D.append(z)
    return S

def main()->int:
    pts=sorted({canon3(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    pi={p:i for i,p in enumerate(pts)}
    J4=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%3
    W=nx.Graph();W.add_nodes_from(range(40))
    for a,b in itertools.combinations(range(40),2):
        if int(np.array(pts[a])@J4@np.array(pts[b]))%3==0:W.add_edge(a,b)
    lines=sorted({tuple(sorted(c)) for c in nx.find_cliques(W) if len(c)==4});assert len(lines)==40
    li={frozenset(L):i for i,L in enumerate(lines)}
    Z=np.zeros((40,40),dtype=int)
    for j,L in enumerate(lines):Z[list(L),j]=1
    assert set(map(int,Z.sum(0)))=={4} and set(map(int,Z.sum(1)))=={4}

    def transvection(v):
        v=np.array(v,dtype=int)%3;out=[]
        for p in pts:
            x=np.array(p,dtype=int);c=int(x@J4@v)%3
            out.append(pi[canon3((x+c*v)%3)])
        return tuple(out)
    trans=[transvection(v) for v in pts]
    gens=[];G={tuple(range(40))}
    for g in trans:
        T=closure(gens+[g],40)
        if len(T)>len(G):gens.append(g);G=T
        if len(G)==25920:break
    assert len(G)==25920
    lgens=[tuple(li[frozenset(g[p] for p in L)] for L in lines) for g in gens]

    # Product orbitals on 40 points x 40 lines.
    seen=set();orbits=[]
    for z in itertools.product(range(40),repeat=2):
        if z in seen:continue
        O={z};seen.add(z);D=deque([z])
        while D:
            p,l=D.popleft()
            for gp,gl in zip(gens,lgens):
                q=(gp[p],gl[l])
                if q not in O:O.add(q);seen.add(q);D.append(q)
        orbits.append(O)
    sizes=sorted(map(len,orbits));assert sizes==[160,1440]
    incident=[O for O in orbits if all(p in lines[l] for p,l in O)]
    assert len(incident)==1 and len(incident[0])==160

    # Gram identities expose the dark sector directly.
    Aline=np.zeros((40,40),dtype=int)
    for i,j in itertools.combinations(range(40),2):
        if set(lines[i])&set(lines[j]):Aline[i,j]=Aline[j,i]=1
    assert np.array_equal(Z.T@Z,4*np.eye(40,dtype=int)+Aline)
    eig=np.linalg.eigvalsh(Aline)
    mult={k:sum(abs(eig-k)<1e-7) for k in (12,2,-4)}
    assert mult=={12:1,2:24,-4:15}

    out={
      'pass':4961,
      'group':{'PSp_order':25920,'point_action_degree':40,'line_action_degree':40},
      'point_times_line_orbits':{'incident':160,'nonincident':1440,'count':2},
      'equivariant_matrix_space':{
        'dimension':2,
        'basis':['Z = incidence','J-Z = nonincidence'],
        'general_form':'M=a Z + b (J-Z)'},
      'line_graph_spectrum':{'12':1,'2':24,'-4':15},
      'dark15_obstruction':{
        'J_on_nonconstant_sectors':'zero',
        'Z_on_line_minus4_sector':'zero because Z^T Z=4I+A_line',
        'Hom_PSp_V15line_to_V15point_dimension':0,
        'Hom_PSp_V15point_to_V15line_dimension':0,
        'signed_or_oriented_equivariant_incidence_can_evade':False},
      'theorem':'Every PSp-equivariant point-to-line matrix is a linear combination of incidence and nonincidence. Consequently every equivariant matrix annihilates the line 15-dimensional -4 constituent when mapping to the point module, and likewise in reverse. The missing 15<->15 bridge cannot be obtained by changing signs or orientations while retaining the same group equivariance.',
      'consequence':'A nonzero dark-15 bridge must add extra structure: symmetry breaking, a twisted target representation, or data outside the ordinary point/line permutation carriers.',
      'boundary':'This is a linear equivariant obstruction. It does not exclude nonlinear, symmetry-broken, or representation-twisted constructions.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
