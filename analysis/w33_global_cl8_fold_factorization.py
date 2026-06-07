#!/usr/bin/env python3
"""BT520: Global Cl8 Fold Factorization Theorem.

Executes next-step branch 2.

Lift the local BT517 6x8 octa-cube fold over all 40 W33 points:
  F is 240 x 320, rows=(p, oct vertex), cols=(p, signed face).
Local row degree 4, column degree 3, rank 4; globally:
  rank(F)=160, row degree 4, column degree 3.

Let R be the 240 x 1620 corner/quadrangle incidence matrix from the old
corner-hypergraph theorem, and M the 320 x 1620 signed-Xmin lift from BT511.
Then the global Cl8 fold factors the signed lift exactly:
  F M = 4 R.

So the signed Xmin/quadrangle lift is a 4-fold refinement of the old corner
hypergraph through the global Cl8 octa-cube fold.
"""
from __future__ import annotations

import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np

P=3
Vec=tuple[int,int,int,int]

def canonical(v)->Vec:
    vv=tuple(int(x)%P for x in v)
    if vv==(0,0,0,0): raise ValueError('zero')
    for x in vv:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%P for y in vv)  # type: ignore[return-value]
    raise AssertionError

def omega(u:Vec,v:Vec)->int:
    return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P

def geom():
    pts=[]; seen=set()
    for raw in itertools.product(range(P),repeat=4):
        if raw==(0,0,0,0): continue
        c=canonical(raw)
        if c not in seen: seen.add(c); pts.append(c)
    pidx={p:i for i,p in enumerate(pts)}; edges=[]; A=np.zeros((40,40),dtype=int)
    for i,j in itertools.combinations(range(40),2):
        if omega(pts[i],pts[j])==0: A[i,j]=A[j,i]=1; edges.append((i,j))
    lines=set()
    for i,j in edges:
        u,v=pts[i],pts[j]; line=set()
        for a,b in itertools.product(range(P),repeat=2):
            if a==0 and b==0: continue
            line.add(pidx[canonical((a*u[t]+b*v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines=sorted(lines); point_lines=defaultdict(list); edge_to_line={}
    for li,L in enumerate(lines):
        for p in L: point_lines[p].append(li)
        for e in itertools.combinations(L,2): edge_to_line[tuple(sorted(e))]=li
    return A,point_lines,edge_to_line

def quads(A):
    qs=[]; seen=set()
    for a,b in itertools.combinations(range(40),2):
        if A[a,b]: continue
        common=[x for x in range(40) if A[a,x] and A[b,x]]
        for c,d in itertools.combinations(common,2):
            cyc=tuple(sorted(tuple(sorted(e)) for e in ((a,c),(c,b),(b,d),(d,a))))
            if cyc not in seen: seen.add(cyc); qs.append(cyc)
    return qs

def local(p,Ls):
    Ls=sorted(Ls); verts=[]; faces=[]; v2f=defaultdict(list)
    for pair in itertools.combinations(Ls,2): verts.append((p,tuple(sorted(pair))))
    for L in Ls:
        others=[x for x in Ls if x!=L]
        star=[tuple(sorted((L,M))) for M in others]
        opp=[tuple(sorted(pair)) for pair in itertools.combinations(others,2)]
        fp=(p,L,1); fm=(p,L,-1); faces += [fp,fm]
        for v in star: v2f[(p,v)].append(fp)
        for v in opp: v2f[(p,v)].append(fm)
    return verts,faces,v2f

def main()->dict:
    A,point_lines,edge_to_line=geom(); qs=quads(A)
    verts=[]; signed=[]; v2f={}
    for p in range(40):
        vs,fs,loc=local(p,point_lines[p]); verts+=vs; signed+=fs; v2f.update(loc)
    verts=sorted(verts); signed=sorted(signed); vi={v:i for i,v in enumerate(verts)}; si={f:i for i,f in enumerate(signed)}
    F=np.zeros((240,320),dtype=np.int8)
    for v,fs in v2f.items():
        for f in fs: F[vi[v],si[f]]=1
    assert Counter(F.sum(axis=1))==Counter({4:240}) and Counter(F.sum(axis=0))==Counter({3:320})
    assert np.linalg.matrix_rank(F.astype(float))==160
    R=np.zeros((240,1620),dtype=np.int8); M=np.zeros((320,1620),dtype=np.int8)
    for qi,cyc in enumerate(qs):
        inc=defaultdict(list)
        for u,v in cyc: inc[u].append((u,v)); inc[v].append((u,v))
        for p,es in inc.items():
            lpair=tuple(sorted(edge_to_line[tuple(sorted(e))] for e in es)); R[vi[(p,lpair)],qi]=1
            for f in v2f[(p,lpair)]: M[si[f],qi]=1
    assert Counter(R.sum(axis=1))==Counter({27:240})
    assert Counter(M.sum(axis=1))==Counter({81:320})
    assert np.array_equal(F@M,4*R)
    assert np.linalg.matrix_rank(R.astype(float))==240
    assert np.linalg.matrix_rank(M.astype(float))==160
    results={
      'theorem':'BT520 Global Cl8 Fold Factorization Theorem',
      'global_fold':{'F_shape':[240,320],'rank':160,'row_degree':4,'column_degree':3,'total_flags':960},
      'factorization':'F M = 4 R',
      'matrices':{'R':'240x1620 octahedron-corner/quadrangle incidence','M':'320x1620 signed-Xmin/quadrangle lift','F':'240x320 global octa-cube fold'},
      'ranks':{'rank_R':240,'rank_M':160,'rank_F':160},
      'reading':'signed Xmin lift is a fourfold face refinement of the old corner hypergraph through the global Cl8 fold',
      'substrate_reading':{'240':'octahedron corner states / E8 roots','320':'signed Xmin faces','960':'40*24 global Cl8 fold flags','4':'each octa vertex sees four signed faces and fold factor'}
    }
    out=Path('data/PART_BT520_GLOBAL_CL8_FOLD_FACTORIZATION_results.json'); out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results
if __name__=='__main__': main()
