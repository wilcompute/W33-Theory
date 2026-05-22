#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; P=3

def canon(v):
    v=tuple(int(x)%P for x in v)
    if v==(0,0,0,0): raise ValueError
    for x in v:
        if x: return tuple(((1 if x==1 else 2)*y)%P for y in v)

def sp(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P

def w33_axes():
    pts=[]; seen=set()
    for raw in product(range(P), repeat=4):
        if raw==(0,0,0,0): continue
        c=canon(raw)
        if c not in seen: seen.add(c); pts.append(c)
    pi={p:i for i,p in enumerate(pts)}
    e=[(i,j) for i,j in combinations(range(40),2) if sp(pts[i],pts[j])==0]
    A=np.zeros((40,40),dtype=np.int8)
    for i,j in e: A[i,j]=A[j,i]=1
    lines=set()
    for i,j in e:
        u,v=pts[i],pts[j]; L=set()
        for a,b in product(range(P), repeat=2):
            if a==0 and b==0: continue
            L.add(pi[canon((a*u[t]+b*v[t] for t in range(4)))])
        lines.add(tuple(sorted(L)))
    lines=sorted(lines); pl=defaultdict(list); el={}
    for li,L in enumerate(lines):
        for p in L: pl[p].append(li)
        for x in combinations(L,2): el[tuple(sorted(x))]=li
    axes=[]; va={}
    for p in range(40):
        a,b,c,d=sorted(pl[p])
        for ax in [((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))]:
            ax=tuple(sorted(tuple(sorted(z)) for z in ax)); key=(p,ax); axes.append(key)
            for pair in ax: va[(p,pair)]=key
    axes=sorted(axes); ai={a:i for i,a in enumerate(axes)}
    quads=[]; sq=set()
    for a,b in combinations(range(40),2):
        if A[a,b]: continue
        common=[x for x in range(40) if A[a,x] and A[b,x]]
        for c,d in combinations(common,2):
            cyc=tuple(sorted(tuple(sorted(x)) for x in ((a,c),(c,b),(b,d),(d,a))))
            if cyc not in sq: sq.add(cyc); quads.append(cyc)
    C=np.zeros((120,len(quads)),dtype=np.int8)
    for qi,cyc in enumerate(quads):
        inc=defaultdict(list)
        for u,v in cyc: inc[u].append((u,v)); inc[v].append((u,v))
        for p,es in inc.items():
            lp=tuple(sorted(el[tuple(sorted(x))] for x in es))
            C[ai[va[(p,lp)]],qi]=1
    G=C@C.T; X=(G>0).astype(np.int8); np.fill_diagonal(X,0)
    return A, axes, X

def root_lines():
    roots=[]
    for i in range(8):
        for j in range(i+1,8):
            for si in (1,-1):
                for sj in (1,-1):
                    r=[0]*8; r[i]=si; r[j]=sj; roots.append(tuple(r))
    for s in product((1,-1), repeat=8):
        if sum(x<0 for x in s)%2==0: roots.append(tuple(x/2 for x in s))
    V=np.array(roots,float); used=set(); reps=[]
    for i in range(240):
        if i in used: continue
        for j in range(i+1,240):
            if j not in used and np.allclose(V[i]+V[j],0):
                used.add(i); used.add(j); reps.append(np.array(min(tuple(V[i]),tuple(V[j])),float)); break
    reps=sorted(reps,key=lambda x:tuple(x.tolist())); R=np.array(reps,float)
    D=np.abs(R@R.T); A=np.isclose(D,0).astype(np.int8); np.fill_diagonal(A,0); return A,D

def sig(S,A,D):
    idx=sorted(S); sub=A[np.ix_(idx,idx)]
    deg=tuple(sorted(Counter(map(int,sub.sum(1))).items()))
    eig=tuple(sorted(Counter(int(round(x)) for x in np.linalg.eigvalsh(sub.astype(float))).items()))
    comp=1-sub-np.eye(len(idx),dtype=int)
    comps=tuple(sorted(len(c) for c in nx.connected_components(nx.from_numpy_array(comp))))
    dots=tuple(sorted(Counter(float(D[i,j]) for i,j in combinations(idx,2)).items()))
    return dict(degree=deg,spectrum=eig,complement_components=comps,absolute_dots=dots)

def main():
    trueA,axes,axisA=w33_axes(); rootA,D=root_lines()
    gm=nx.algorithms.isomorphism.GraphMatcher(nx.from_numpy_array(axisA),nx.from_numpy_array(rootA)); assert gm.is_isomorphic(); mp=dict(gm.mapping)
    tri={p:set(mp[i] for i,a in enumerate(axes) if a[0]==p) for p in range(40)}
    species=defaultdict(Counter); examples={}; pair_counts=Counter(); compnames=Counter()
    for p,q in combinations(range(40),2):
        S=tri[p]|tri[q]; sg=sig(S,rootA,D); key=json.dumps(sg,sort_keys=True)
        species[bool(trueA[p,q])][key]+=1; examples.setdefault(key,sg)
        orth=sum(int(rootA[i,j]) for i in tri[p] for j in tri[q]); pair_counts[(bool(trueA[p,q]),orth)]+=1
        if bool(trueA[p,q]): compnames['collinear_pair_K33_orthogonality']+=1
        else: compnames['noncollinear_pair_perfect_matching_orthogonality_octahedral_complement']+=1
    ok=(len(species[True])==1 and list(species[True].values())==[240] and len(species[False])==1 and list(species[False].values())==[540] and pair_counts==Counter({(True,9):240,(False,3):540}))
    out={'all_checks_passed':ok,'summary':{'collinear_pairs':240,'noncollinear_pairs':540,'triad_pair_orthogonality_counts':{str(k):v for k,v in pair_counts.items()},'species_names':dict(compnames)},'species_by_collinearity':{str(k):dict(v) for k,v in species.items()},'species_signatures':examples,'meaning':'A point is an A2 triad.  A collinear point pair gives a K3,3 orthogonality block.  A noncollinear point pair gives a perfect matching orthogonality block whose complement is the octahedron graph.'}
    path=ROOT/'data'/'w33_point_pair_rootline_species.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
