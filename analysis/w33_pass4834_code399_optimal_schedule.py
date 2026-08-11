#!/usr/bin/env python3
"""Pass4834 — search and certify a globally optimal syndrome schedule for code399.

The six independent global W6 checks are pairwise intersecting for every basis,
so any disjoint-support schedule needs at least six layers. We search bases of W6
and, for each one, solve the exact per-K6-cell list-coloring problem for the 1620
local checks with the six global checks fixed to distinct colors. Cells have
disjoint physical support, so per-cell feasibility is equivalent to a global
six-layer schedule. A found witness proves optimal depth six.
"""
from __future__ import annotations
import itertools,json,random
from collections import defaultdict
from pathlib import Path
import numpy as np
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle
from w33_pass4819_4822_outer_code_levi_classification import Qm,nullspace
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4834_CODE399_OPTIMAL_SCHEDULE.json'

def rank_masks(vals):
    piv={}
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def color_cell(rows,global_rows):
    n=len(rows);adj=[set() for _ in range(n)];forbid=[]
    for i,j in itertools.combinations(range(n),2):
        if rows[i]&rows[j]:adj[i].add(j);adj[j].add(i)
    for r in rows:forbid.append({c for c,g in enumerate(global_rows) if r&g})
    order=sorted(range(n),key=lambda i:(-(len(adj[i])+len(forbid[i])),-len(adj[i])))
    col=[-1]*n
    def dfs(t):
        if t==n:return True
        v=order[t];used={col[w] for w in adj[v] if col[w]>=0}|forbid[v]
        for c in range(6):
            if c not in used:
                col[v]=c
                if dfs(t+1):return True
                col[v]=-1
        return False
    return col if dfs(0) else None

def span_basis(B):
    V=[]
    for z in range(1,1<<len(B)):
        x=0
        for i,b in enumerate(B):
            if (z>>i)&1:x^=b
        V.append(x)
    return V

def main():
    D=build_all();B=build_bundle();rm=D['rmasks'];U=D['cube_unions'];cubeR=D['cube_residues'];N=np.asarray(D['selected_incidence']);phiU=D['phiU'];phiR=D['phiR']
    hot={tuple(sorted(e)) for e in B['hot']};cold={tuple(sorted(e)) for e in B['cold']};router=hot|cold;K5=B['K5'];packets=B['packets']
    owner=[]
    for T in B['projected']:
        h=[i for i,S in enumerate(K5) if set(T)<=S];assert len(h)==1;owner.append(h[0])
    packet_of={s:p for p,T in enumerate(packets) for s in T};union_to_R={}
    for R in cubeR:
        u=0
        for r in R:u|=rm[r]
        union_to_R[u]=tuple(R)
    cells={}
    for ui,u in enumerate(U):
        s=phiU[ui];R=union_to_R[u];inc=set(np.flatnonzero(N[s]).tolist());p=packet_of[s];F=sorted(i for i,S in enumerate(K5) if p in S)
        groups={f:sorted(v for v in inc if owner[v]==f) for f in F};H={tuple(sorted(groups[f])) for f in F};blocks={}
        for a,b in itertools.combinations(F,2):blocks[(a,b)]=sorted(tuple(sorted((x,y))) for x in groups[a] for y in groups[b])
        cells[s]={'fibers':F,'hot':sorted(H),'blocks':blocks}
    edges=sorted(router);eidx={e:i for i,e in enumerate(edges)};bit=lambda e:1<<eidx[e]
    byline=defaultdict(list);cell_rows={};global_pick={};logical=[]
    for s,C in sorted(cells.items()):
        F=C['fibers'];H=C['hot'];block_info={};R=[]
        for pair,E in sorted(C['blocks'].items()):
            e0,e1,e2,e3=E;R += [bit(e0)^bit(e1),bit(e1)^bit(e2),bit(e2)^bit(e3)]
            L=next(iter(set(F)-set(pair)));block_info[L]=(E,e0,e3)
        h0,h1,h2=H;R += [bit(h0)^bit(h1),bit(h1)^bit(h2)]
        rc=bit(h0)
        for L in F:rc^=bit(block_info[L][1])
        R.append(rc);assert len(R)==12;cell_rows[s]=R
        for L in F:
            j=len(logical);logical.append((s,L));byline[L].append(j);global_pick[j]=bit(block_info[L][2])
    line_rows=[]
    for L in range(27):
        r=0
        for j in byline[L]:r^=global_pick[j]
        assert r.bit_count()==15;line_rows.append(r)
    qp=[x for x in range(1,64) if Qm(x)==0];ql=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if (a^b) in qp});Lgeo=[tuple(i for i,Q in enumerate(ql) if p in Q) for p in qp]
    inc=[sum(1<<i for i,S in enumerate(Lgeo) if p in S) for p in range(45)];W6b=nullspace(inc,27);assert len(W6b)==6
    W=span_basis(W6b);assert len(set(W))==63
    assert {x.bit_count() for x in W}=={12,16}
    assert all(a&b for a,b in itertools.combinations(W,2))
    rng=random.Random(4834);witness=None
    candidates=[list(W6b)]
    for _ in range(20000):
        Bc=[]
        for x in rng.sample(W,20):
            if rank_masks(Bc+[x])>len(Bc):Bc.append(x)
            if len(Bc)==6:break
        if len(Bc)==6:candidates.append(Bc)
    for Bc in candidates:
        globals=[]
        for h in Bc:
            r=0
            for L in range(27):
                if (h>>L)&1:r^=line_rows[L]
            globals.append(r)
        assert all(a&b for a,b in itertools.combinations(globals,2))
        colors={};ok=True
        for s,R in cell_rows.items():
            c=color_cell(R,globals)
            if c is None:ok=False;break
            colors[s]=c
        if ok:witness=(Bc,globals,colors);break
    if witness is None:raise RuntimeError('No six-layer witness found in deterministic 20001-basis search; do not infer impossibility')
    Bc,globals,colors=witness
    layer_counts=[]
    for c in range(6):
        used=globals[c];cnt=1
        for s,R in cell_rows.items():
            for i,r in enumerate(R):
                if colors[s][i]==c:
                    assert not (used&r);used|=r;cnt+=1
        layer_counts.append(cnt)
    assert sum(layer_counts)==1626
    out={'pass':4834,'code':'[2025,399,14]_2','optimal_schedule_depth':6,'lower_bound':6,'lower_bound_reason':'the six independent nonzero W6 global checks form a K6 conflict graph for every W6 basis','witness_outer_basis_masks':[int(x) for x in Bc],'layer_check_counts':layer_counts,'local_cells_list_colored':135,'basis_candidates_tested_at_most':len(candidates),'rank':1626,'decoder_radius_preserved':6,'theorem':'A six-layer disjoint-support syndrome schedule exists for all 1626 checks of [2025,399,14]_2. Six layers are also necessary because every basis of the six-dimensional outer dual W6 consists of six pairwise-intersecting global checks. Hence the exact optimal schedule depth is six in the stated disjoint-support model.','boundary':'Optimality is for the same classical disjoint-physical-support check model as Pass4821/4826; it is not a measured hardware clock depth.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
