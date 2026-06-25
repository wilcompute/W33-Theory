#!/usr/bin/env python3
"""BT1793: align the 18 BT1788 nonconcurrent Hesse tables with the H27/Payne support triples."""
from __future__ import annotations
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1793_payne_frontier_alignment_matrix.json'
F=range(3)
def rep(v):
    v=tuple(x%3 for x in v)
    for x in v:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%3 for y in v)
    raise ValueError('zero')
def form(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%3
def projective_points(): return sorted({rep(v) for v in product(F, repeat=4) if any(v)})
def projective_line(u,v): return frozenset(rep(tuple((a*u[i]+b*v[i])%3 for i in range(4))) for a,b in product(F,F) if a or b)
def shell_coord(v):
    if v[2]==2: v=tuple((2*x)%3 for x in v)
    assert v[2]==1
    return (v[0],v[1],v[3])
def build_patches():
    P=projective_points(); anchor=rep((1,0,0,0)); shell=set(p for p in P if p!=anchor and form(anchor,p)!=0)
    lines=sorted({projective_line(u,v) for u,v in combinations(P,2) if form(u,v)==0}, key=lambda L: sorted(L))
    old=[]
    for L in lines:
        if anchor in L: continue
        old.append(tuple(sorted(shell_coord(x) for x in L if x in shell)))
    new=[tuple((a,b,d) for a in F) for b,d in product(F,F)]
    return [(f'O{i:02d}',frozenset(L),'old') for i,L in enumerate(old)] + [(f'N{i:02d}',frozenset(L),'new') for i,L in enumerate(new)]
def table_triangle(i,j,s):
    return frozenset([(0,i,j),(1,i,s),(2,j,s)])
def main():
    patches=build_patches()
    rows=[]; global_hist=Counter(); exact=[]
    for i,j,s in product(F,F,F):
        if s==(j-i)%3: continue
        tri=table_triangle(i,j,s); row=[]; row_hist=Counter()
        for name,L,kind in patches:
            m=len(tri & L)
            global_hist[m]+=1; row_hist[m]+=1
            if m:
                row.append({'patch':name,'kind':kind,'intersection':m})
        e=[r for r in row if r['intersection']==3]
        if e: exact.append({'table':f'T{i}{j}{s}','tuple':[i,j,s],'exact_patch':e})
        rows.append({'table':f'T{i}{j}{s}','tuple':[i,j,s],'is_concurrent':False,'intersection_histogram':dict(sorted(row_hist.items())),'two_point_overlaps':[r for r in row if r['intersection']==2],'exact_patches':e})
    two_hist=Counter(len(r['two_point_overlaps']) for r in rows)
    payload={'bt':'BT1793','title':'Payne/frontier alignment matrix','tables':18,'patches':45,'matrix_shape':[18,45],'entry_intersection_histogram':dict(sorted(global_hist.items())),'rows_with_exact_H27_patch':len(exact),'exact_patch_rows':exact,'two_point_overlap_count_histogram':dict(sorted(two_hist.items())),'alignment_rows':rows,'conclusion':'Under the canonical frontier labelling, only 2 of the 18 BT1788 nonconcurrent table triangles are themselves H27/Payne lines; most are transversal triangles meeting the H27 line sheaf in one- or two-point overlaps. Therefore the true 18 accepted ternary tuple lists must be projection-matched to the 45 H27 support triples; they cannot be identified naively with the 45 triples.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'shape':[18,45],'intersection_histogram':dict(sorted(global_hist.items())),'exact_rows':len(exact),'two_point_overlap_count_histogram':dict(sorted(two_hist.items()))},indent=2,sort_keys=True))
if __name__=='__main__': main()
