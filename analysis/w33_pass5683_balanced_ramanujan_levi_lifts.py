#!/usr/bin/env python3
"""Pass5683: balanced nontrivial Levi voltages and the Ramanujan tower theorem.

The W33 point-line Levi graph is 4-regular bipartite with spectrum
  +/-4, +/-sqrt(6), 0.
Hence it is already Ramanujan because sqrt(6) < 2*sqrt(3).

Marcus-Spielman-Srivastava (Interlacing Families I, arXiv:1304.4132)
prove that every d-regular bipartite Ramanujan graph has a 2-lift that is again
bipartite Ramanujan. Iterating therefore gives an EXISTENTIAL infinite 4-regular
Ramanujan 2-lift tower from the W33 Levi graph, with uniform nontrivial adjacency
bound 2*sqrt(3) and combinatorial Laplacian gap >= 4-2*sqrt(3).

This verifier also gives an explicit first-level locally-balanced witness: exactly
80 of 160 incidences are negative, and every one of the 80 Levi vertices meets
exactly two negative edges. Its signed spectral radius is < 2*sqrt(3), so the
corresponding 2-lift is connected and Ramanujan.
"""
from __future__ import annotations
import itertools, json, math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5683_BALANCED_RAMANUJAN_LEVI_LIFTS.json'
Q=3
J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%Q
NEG=[1,3,4,6,8,11,13,14,16,17,22,23,25,27,28,29,32,34,37,38,40,42,46,47,48,50,53,55,56,57,62,63,66,67,68,71,72,73,78,79,80,83,85,87,90,91,92,94,96,97,102,103,104,107,109,110,113,114,117,118,120,122,124,126,128,129,133,135,137,138,140,141,144,147,149,151,152,154,156,158]

def norm(v):
    v=tuple(int(x)%Q for x in v)
    for a in v:
        if a:
            z=pow(a,-1,Q);return tuple((z*x)%Q for x in v)
    raise ValueError('zero')
def B(x,y):return int(np.array(x,dtype=int)@J@np.array(y,dtype=int))%Q

def levi():
    pts=sorted({norm(v) for v in itertools.product(range(Q),repeat=4) if any(v)})
    pi={p:i for i,p in enumerate(pts)};lines=set()
    for i,p in enumerate(pts):
        for q in pts[i+1:]:
            if B(p,q):continue
            L={norm(tuple((a*p[k]+b*q[k])%Q for k in range(4))) for a,b in itertools.product(range(Q),repeat=2) if (a,b)!=(0,0)}
            if len(L)==4:lines.add(tuple(sorted(pi[x] for x in L)))
    lines=sorted(lines);E=[]
    for j,L in enumerate(lines):
        for p in L:E.append((p,40+j))
    assert (len(pts),len(lines),len(E))==(40,40,160)
    return E

def adj(E,sign=None):
    A=np.zeros((80,80),float)
    if sign is None:sign=np.ones(len(E))
    for s,(u,v) in zip(sign,E):A[u,v]=A[v,u]=s
    return A

def components(A):
    n=len(A);seen=set();sizes=[]
    for s in range(n):
        if s in seen:continue
        st=[s];seen.add(s);m=0
        while st:
            u=st.pop();m+=1
            for v in np.where(abs(A[u])>0)[0]:
                v=int(v)
                if v not in seen:seen.add(v);st.append(v)
        sizes.append(m)
    return sorted(sizes,reverse=True)

def lift(E,sign):
    n=80;A=np.zeros((160,160),float)
    for s,(u,v) in zip(sign,E):
        flip=1 if s<0 else 0
        for a in (0,1):
            x=u+a*n;y=v+(a^flip)*n
            A[x,y]=A[y,x]=1
    return A

def main():
    E=levi();A=adj(E);ev=np.linalg.eigvalsh(A)
    target=np.array([-4]+[-math.sqrt(6)]*24+[0]*30+[math.sqrt(6)]*24+[4])
    assert np.max(abs(ev-target))<1e-8
    ram=2*math.sqrt(3);old_nontr=math.sqrt(6)
    assert old_nontr<ram
    s=np.ones(160);s[NEG]=-1
    assert int(np.sum(s<0))==80
    nd=np.zeros(80,dtype=int)
    for i in NEG:
        u,v=E[i];nd[u]+=1;nd[v]+=1
    assert set(nd)=={2}
    As=adj(E,s);rho=float(np.max(abs(np.linalg.eigvalsh(As))))
    assert rho<ram
    L=lift(E,s);assert components(L)==[160]
    lev=np.linalg.eigvalsh(L)
    # old + new spectrum identity
    union=np.sort(np.r_[np.linalg.eigvalsh(A),np.linalg.eigvalsh(As)])
    assert np.max(abs(lev-union))<1e-8
    gap=min(4-old_nontr,4-rho)
    out={
      'pass':5683,'status':'W33_LEVI_IS_RAMANUJAN_AND_HAS_EXPLICIT_LOCALLY_BALANCED_RAMANUJAN_2LIFT',
      'base':{'vertices':80,'edges':160,'degree':4,'spectrum':'(+/-4)^1,(+/-sqrt6)^24,0^30','nontrivial_radius':old_nontr},
      'ramanujan_bound':ram,'uniform_existence_gap':4-ram,
      'MSS_external_theorem':'Every regular bipartite Ramanujan graph has a regular bipartite Ramanujan 2-lift; iteration gives an existential infinite tower (arXiv:1304.4132).',
      'explicit_first_lift':{'negative_edge_indices':NEG,'negative_edges':80,'negative_degree_at_every_vertex':2,'signed_spectral_radius':rho,'connected':True,'laplacian_gap':gap},
      'theorem':'The earlier single-chord tower is not the only connected refinement. W33 Levi satisfies the exact hypothesis of the MSS Ramanujan 2-lift theorem, and an explicit locally balanced first signing already lies below the Ramanujan threshold.',
      'boundary':'The infinite tower is existential via MSS; this file constructs only the first balanced lift. Ramanujan expansion is not by itself a spacetime continuum or a selected physical metric.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
