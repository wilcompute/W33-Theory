#!/usr/bin/env python3
"""Pass4966 — oriented Witting Pancharatnam phase carries the PGSp/PSp sign.

Pass4963 identifies the Witting orthogonality graph with the standard W(3,3)
POINT action and gives an exact Eisenstein formula for its Bargmann phases.
Here we transport a generating PSp(4,3) action through that graph isomorphism
and test the oriented phase on all 3240 nonorthogonal triples.

Every PSp generator preserves the phase exactly.  An explicit symplectic
similitude M=diag(1,-1,1,-1) with multiplier -1 extends the group to PGSp of
order 51840 and negates the phase on every nonorthogonal oriented triple.
Thus the oriented Pancharatnam phase realizes the index-two outer character.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np,networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4966_WITTING_PHASE_OUTER_CHARACTER.json'

# Eisenstein integers a+b*w, w^2+w+1=0.
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
def rays():
    out=[]
    for i in range(4):
        v=[ZERO]*4;v[i]=ONE;out.append(tuple(v))
    for mu in range(3):
        for nu in range(3):
            out.append((ZERO,ONE,neg(POW[mu]),POW[nu]))
            out.append((ONE,ZERO,neg(POW[mu]),neg(POW[nu])))
            out.append((ONE,neg(POW[mu]),ZERO,POW[nu]))
            out.append((ONE,POW[mu],POW[nu],ZERO))
    assert len(out)==40;return out
R=rays()
def phase_code(i,j,k):
    z=mul(mul(inner(R[i],R[j]),inner(R[j],R[k])),inner(R[k],R[i]))
    a,b=z
    if a==2*b and b>0:return 1      # +pi/6
    if a==-b and b<0:return -1       # -pi/6
    if 2*a-b==0 and b>0:return 3     # +pi/2
    if 2*a-b==0 and b<0:return -3    # -pi/2
    raise AssertionError(('unexpected Bargmann phase',z))
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
    O=nx.Graph();O.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if inner(R[i],R[j])==ZERO:O.add_edge(i,j)
    assert O.number_of_edges()==240 and set(dict(O.degree()).values())=={12}

    pts=sorted({canon3(v) for v in itertools.product(range(3),repeat=4) if any(v)});pi={p:i for i,p in enumerate(pts)}
    J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%3
    WG=nx.Graph();WG.add_nodes_from(range(40))
    for a,b in itertools.combinations(range(40),2):
        if int(np.array(pts[a])@J@np.array(pts[b]))%3==0:WG.add_edge(a,b)
    iso=next(nx.algorithms.isomorphism.GraphMatcher(O,WG).isomorphisms_iter());inv={v:k for k,v in iso.items()}

    def transvection(v):
        v=np.array(v,dtype=int)%3;out=[]
        for p in pts:
            x=np.array(p,dtype=int);c=int(x@J@v)%3
            out.append(pi[canon3((x+c*v)%3)])
        return tuple(out)
    all_t=[transvection(v) for v in pts];gens=[];G={tuple(range(40))}
    for g in all_t:
        T=closure(gens+[g],40)
        if len(T)>len(G):gens.append(g);G=T
        if len(G)==25920:break
    assert len(G)==25920 and len(gens)==5
    ray_gens=[tuple(inv[g[iso[i]]] for i in range(40)) for g in gens]

    triples=[t for t in itertools.combinations(range(40),3)
      if inner(R[t[0]],R[t[1]])!=ZERO and inner(R[t[1]],R[t[2]])!=ZERO and inner(R[t[2]],R[t[0]])!=ZERO]
    assert len(triples)==3240
    generator_checks=[]
    for g in ray_gens:
        preserved=all(phase_code(*t)==phase_code(g[t[0]],g[t[1]],g[t[2]]) for t in triples)
        assert preserved;generator_checks.append(preserved)

    M=np.diag([1,2,1,2]).astype(int)%3
    assert np.array_equal((M.T@J@M)%3,(-J)%3)
    gout=tuple(pi[canon3(M@np.array(p,dtype=int))] for p in pts)
    assert len(closure(gens+[gout],40))==51840
    rout=tuple(inv[gout[iso[i]]] for i in range(40))
    cross=Counter()
    for t in triples:
        c=phase_code(*t);d=phase_code(rout[t[0]],rout[t[1]],rout[t[2]])
        assert d==-c;cross[(c,d)]+=1
    assert cross==Counter({(1,-1):1440,(-1,1):1440,(3,-3):180,(-3,3):180})

    out={
      'pass':4966,
      'carrier':'40 Witting rays = standard W(3,3) point action from Pass4963',
      'oriented_nonorthogonal_triples':3240,
      'PSp':{'order':25920,'generator_count':len(gens),'all_generators_preserve_oriented_phase':all(generator_checks)},
      'outer_similitude':{'matrix_mod3':'diag(1,2,1,2)','multiplier':-1,'extended_group_order':51840,
        'all_triples_phase_negated':True,
        'phase_cross_counts':{'+pi/6 -> -pi/6':1440,'-pi/6 -> +pi/6':1440,'+pi/2 -> -pi/2':180,'-pi/2 -> +pi/2':180}},
      'theorem':'On the 40-ray Witting/W33 point carrier, the oriented Pancharatnam phase is invariant under PSp(4,3) and changes sign under an explicit multiplier-minus-one symplectic similitude extending the action to PGSp(4,3) of order 51840. Hence phase orientation realizes the PGSp/PSp index-two character on every one of the 3240 nonorthogonal oriented triples.',
      'interpretation':'Complex conjugation of the finite Bargmann phase is the ray-level shadow of the outer symplectic-similitude coset.',
      'boundary':'The sign refers to oriented triple phase. Reversing triangle orientation also conjugates the Bargmann product. This finite sign character is not automatically a spacetime parity or CP transformation.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
