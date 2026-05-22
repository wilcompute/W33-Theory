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
            if cyc not in sq: sq.add(cyc); quads.append((cyc,tuple(sorted((a,b,c,d)))))
    C=np.zeros((120,len(quads)),dtype=np.int8)
    for qi,(cyc,verts) in enumerate(quads):
        inc=defaultdict(list)
        for u,v in cyc: inc[u].append((u,v)); inc[v].append((u,v))
        for p,es in inc.items():
            lp=tuple(sorted(el[tuple(sorted(x))] for x in es))
            C[ai[va[(p,lp)]],qi]=1
    G=C@C.T; X=(G>0).astype(np.int8); np.fill_diagonal(X,0)
    return A, lines, axes, X

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
    D=np.abs(R@R.T); A=np.isclose(D,0).astype(np.int8); np.fill_diagonal(A,0)
    return R,A,D

def srg(A):
    deg=Counter(map(int,A.sum(1))); la=Counter(); mu=Counter()
    for i,j in combinations(range(A.shape[0]),2):
        c=int(A[i]@A[j]); (la if A[i,j] else mu)[c]+=1
    eig=Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))
    return {'deg':dict(deg),'lambda':dict(la),'mu':dict(mu),'eig':dict(eig)}

def zero_sum_orientations(R, tri):
    e=list(tri); count=0
    for s in product((1,-1), repeat=3):
        if np.allclose(sum(s[k]*R[e[k]] for k in range(3)),0): count+=1
    return count

def main():
    trueA,true_lines,axes,axisA=w33_axes(); R,rootA,D=root_lines()
    gm=nx.algorithms.isomorphism.GraphMatcher(nx.from_numpy_array(axisA),nx.from_numpy_array(rootA)); assert gm.is_isomorphic(); mp=dict(gm.mapping)
    tri={p:set(mp[i] for i,a in enumerate(axes) if a[0]==p) for p in range(40)}
    # point-first adjacency: two point-triads are adjacent iff all 3x3 root-line pairs are orthogonal.
    recA=np.zeros((40,40), dtype=np.int8); counts=Counter(); bytruth=defaultdict(Counter)
    for p,q in combinations(range(40),2):
        c=sum(int(rootA[i,j]) for i in tri[p] for j in tri[q]); counts[c]+=1; bytruth[bool(trueA[p,q])][c]+=1
        if c==9: recA[p,q]=recA[q,p]=1
    # Recover lines as maximal 4-cliques from the reconstructed point graph.
    G=nx.from_numpy_array(recA)
    cliques=sorted(tuple(sorted(c)) for c in nx.find_cliques(G) if len(c)==4)
    # Recover ordinary quadrangles from only recA.
    quads=set()
    for a,b in combinations(range(40),2):
        if recA[a,b]: continue
        common=[x for x in range(40) if recA[a,x] and recA[b,x]]
        for c,d in combinations(common,2):
            cyc=tuple(sorted(tuple(sorted(x)) for x in ((a,c),(c,b),(b,d),(d,a))))
            quads.add(cyc)
    # Local pencil-octahedra are line graph L(K4) of the four recovered lines through a point.
    point_lines=defaultdict(list)
    for li,L in enumerate(cliques):
        for p in L: point_lines[p].append(li)
    octahedra_ok=(Counter(len(v) for v in point_lines.values())==Counter({4:40}))
    # Triad zero-sum orientation: one self-entangled photon phase loop per point.
    zdist=Counter(zero_sum_orientations(R,T) for T in tri.values())
    ok=(np.array_equal(trueA,recA) and sorted(cliques)==sorted(true_lines) and len(quads)==1620 and octahedra_ok and zdist==Counter({2:40}) and srg(recA)=={'deg':{12:40},'lambda':{2:240},'mu':{4:540},'eig':{-4:15,2:24,12:1}})
    out={'all_checks_passed':ok,'summary':{'primitive':'point = A2 zero-sum root-line triad','point_triads':40,'zero_sum_orientation_distribution':dict(zdist),'triad_orthogonality_counts':dict(counts),'by_true_collinearity':{str(k):dict(v) for k,v in bytruth.items()},'recovered_lines':len(cliques),'recovered_quadrangles':len(quads),'recovered_local_octahedra':40 if octahedra_ok else 0,'recovered_graph':'SRG(40,12,2,4)'},'checks':{'adjacency_recovered_from_9_vs_3':np.array_equal(trueA,recA),'lines_recovered_as_4_cliques':sorted(cliques)==sorted(true_lines),'quadrangles_recovered':len(quads)==1620,'local_pencils_recovered':octahedra_ok,'point_triad_zero_sum':zdist==Counter({2:40})},'interpretation':'The point is the primitive A2 triad: a three-phase self-cancelling root-line loop.  From the 40 point triads alone, the 9-vs-3 orthogonality rule recovers W33 adjacency; 4-cliques recover lines; ordinary quadrangles recover loops; four lines through each point recover the local octahedron.'}
    path=ROOT/'data'/'w33_point_first_photon_triad_reconstruction.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
