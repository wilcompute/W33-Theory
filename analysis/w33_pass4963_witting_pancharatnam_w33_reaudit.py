#!/usr/bin/env python3
"""Pass4963 — re-audit the Witting/Pancharatnam thread after the W33/Q43 correction.

The legacy Pass4882 argument matched only SRG parameters and also used an invalid
ray->F3^4 encoder.  This producer works directly with the 40 Witting rays in
C^4, using exact Eisenstein-integer arithmetic for orthogonality and Bargmann
triple products.

It proves:
* the Witting orthogonality graph is the standard W(3,3) POINT graph, not the
  Q(4,3) W33-LINE/Steiner quotient;
* the legacy exponent encoder maps 40 rays to only 19 tuples and even maps 8
  rays to the zero tuple, so it is not a projective F3^4 identification;
* among the 3240 nonorthogonal ray triples, the Pancharatnam/Bargmann phase
  magnitude exactly detects the W33 point-triad center count:
    one center -> +/-pi/6 (1440 each), four centers -> +/-pi/2 (180 each).
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
import numpy as np,networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4963_WITTING_PANCHARATNAM_W33_REAUDIT.json'

# Eisenstein integers a+b*w, w^2+w+1=0, conjugation w->w^2=-1-w.
def add(z,u):return (z[0]+u[0],z[1]+u[1])
def neg(z):return (-z[0],-z[1])
def mul(z,u):
    a,b=z;c,d=u;return (a*c-b*d,a*d+b*c-b*d)
def conj(z):
    a,b=z;return (a-b,-b)
ZERO=(0,0);ONE=(1,0);W=(0,1);W2=(-1,-1);POW=(ONE,W,W2)
def inner(v,u):
    s=ZERO
    for a,b in zip(v,u):s=add(s,mul(conj(a),b))
    return s

def witting_rays():
    rays=[]
    for i in range(4):
        v=[ZERO]*4;v[i]=ONE;rays.append(tuple(v))
    for mu in range(3):
        for nu in range(3):
            rays.append((ZERO,ONE,neg(POW[mu]),POW[nu]))
            rays.append((ONE,ZERO,neg(POW[mu]),neg(POW[nu])))
            rays.append((ONE,neg(POW[mu]),ZERO,POW[nu]))
            rays.append((ONE,POW[mu],POW[nu],ZERO))
    assert len(rays)==40;return rays

def phase_code(z):
    # +1/-1 encode +/-pi/6; +3/-3 encode +/-pi/2.
    a,b=z
    if a==2*b and b>0:return 1
    if a==-b and b<0:return -1
    if 2*a-b==0 and b>0:return 3
    if 2*a-b==0 and b<0:return -3
    raise AssertionError(('unexpected Bargmann phase',z))

def canon3(v):
    v=np.array(v,dtype=int)%3;j=next(i for i,x in enumerate(v) if x)
    return tuple(int(x) for x in (v*pow(int(v[j]),-1,3))%3)

def legacy_encoder(ray,tol=1e-6):
    # Literal reproduction of the retired tools/pancharatnam_symplectic_invariants.py encoder.
    omega=np.exp(2j*np.pi/3);roots=[1,omega,omega**2]
    idx=next(i for i,z in enumerate(ray) if abs(z)>tol);ray_n=ray/ray[idx]
    nearest=min(roots,key=lambda r:abs(ray_n[idx]-r));ray_n*=nearest/ray_n[idx];ray_n=ray_n**2
    out=[]
    for z in ray_n:
        if abs(z)<tol:out.append(0)
        else:out.append(int(np.argmin([abs(z-r) for r in roots])))
    return tuple(out)

def numeric_rays():
    omega=np.exp(2j*np.pi/3);r=[]
    for i in range(4):
        v=np.zeros(4,dtype=complex);v[i]=1;r.append(v)
    for mu in range(3):
        for nu in range(3):
            r.append(np.array([0,1,-omega**mu,omega**nu],complex))
            r.append(np.array([1,0,-omega**mu,-omega**nu],complex))
            r.append(np.array([1,-omega**mu,0,omega**nu],complex))
            r.append(np.array([1,omega**mu,omega**nu,0],complex))
    return r

def main()->int:
    rays=witting_rays()
    O=nx.Graph();O.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if inner(rays[i],rays[j])==ZERO:O.add_edge(i,j)
    assert O.number_of_edges()==240 and set(dict(O.degree()).values())=={12}

    pts=sorted({canon3(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%3
    WG=nx.Graph();WG.add_nodes_from(range(40))
    for a,b in itertools.combinations(range(40),2):
        if int(np.array(pts[a])@J@np.array(pts[b]))%3==0:WG.add_edge(a,b)
    lines=sorted({tuple(sorted(c)) for c in nx.find_cliques(WG) if len(c)==4});assert len(lines)==40
    Q=nx.Graph();Q.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if set(lines[i])&set(lines[j]):Q.add_edge(i,j)
    assert nx.is_isomorphic(O,WG)
    assert not nx.is_isomorphic(O,Q)
    iso=next(nx.algorithms.isomorphism.GraphMatcher(O,WG).isomorphisms_iter())

    old=[legacy_encoder(r) for r in numeric_rays()]
    assert len(set(old))==19 and old.count((0,0,0,0))==8

    table=Counter();phase_totals=Counter();triples=0
    for i,j,k in itertools.combinations(range(40),3):
        z1=inner(rays[i],rays[j]);z2=inner(rays[j],rays[k]);z3=inner(rays[k],rays[i])
        if ZERO in (z1,z2,z3):continue
        triples+=1;code=phase_code(mul(mul(z1,z2),z3));phase_totals[code]+=1
        a,b,c=iso[i],iso[j],iso[k]
        centers=len(set(WG.neighbors(a))&set(WG.neighbors(b))&set(WG.neighbors(c)))
        table[(centers,code)]+=1
    assert triples==3240
    assert phase_totals==Counter({1:1440,-1:1440,3:180,-3:180})
    assert table==Counter({(1,1):1440,(1,-1):1440,(4,3):180,(4,-3):180})

    out={
      'pass':4963,
      'prior_art':{
        'Waegell_Aravind_arXiv_1701.06512':'40 Witting/Penrose rays live in CP(3), arising from a regular complex polytope in C^4; each ray is orthogonal to 12 others',
        'scope':'prior art supplies the ray realization; the W33/Q43 graph discrimination and phase-center cross-tab below are repo computations'},
      'witting_carrier':{
        'rays':40,'ambient':'C^4 / CP^3','orthogonality_edges':240,'orthogonality_degree':12,
        'orthogonality_graph':'isomorphic to standard W(3,3) point graph',
        'isomorphic_to_Q43_Steiner_line_graph':False},
      'legacy_encoder_failure':{'distinct_F3_tuples_from_40_rays':19,'zero_tuple_multiplicity':8,'projective_bijection':False},
      'nonorthogonal_triples':3240,
      'exact_pancharatnam_center_table':{
        'one_W33_common_center':{'+pi/6':1440,'-pi/6':1440,'total':2880},
        'four_W33_common_centers':{'+pi/2':180,'-pi/2':180,'total':360}},
      'correction_to_Pass4882':'The 40 Witting rays belong to the W33 point action, whereas the 40 Steiner fibers belong to the nonisomorphic Q(4,3)=W33-line action. The old parameter-only identification of those two 40-sets is withdrawn.',
      'theorem':'The exact Witting orthogonality graph is the standard W(3,3) point graph and not the Q(4,3) Steiner quotient. On its 3240 nonorthogonal triples, the exact Eisenstein Bargmann product has phase +/-pi/6 precisely for the 2880 one-center W33 triads and +/-pi/2 precisely for the 360 four-center triads.',
      'boundary':'This establishes the finite ray/graph/phase correspondence. It does not identify Pancharatnam phase with the old E6 Steiner signing, which lived on a different 40-set.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
