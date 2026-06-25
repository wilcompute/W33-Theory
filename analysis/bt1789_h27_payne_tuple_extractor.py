#!/usr/bin/env python3
"""BT1789: H27 Payne tuple extractor.

Index-corrected successor to BT1788. The raw local 27-shell of W(3,3) is
not already Schlaefli/GQ(2,4); it is the affine Heisenberg bulk. Payne
derivation supplies the missing transform.
"""
from __future__ import annotations
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1789_h27_payne_tuple_extractor.json'
F=range(3)
def mod3(x:int)->int: return x%3
def rep(v):
    v=tuple(mod3(x) for x in v)
    for x in v:
        if x%3:
            inv=1 if x==1 else 2
            return tuple(mod3(inv*y) for y in v)
    raise ValueError('zero vector')
def form(u,v): return mod3(u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])
def projective_points(): return sorted({rep(v) for v in product(F, repeat=4) if any(v)})
def projective_line(u,v):
    return frozenset(rep(tuple(mod3(a*u[i]+b*v[i]) for i in range(4))) for a,b in product(F, repeat=2) if a or b)
def shell_coord(v):
    v=tuple(mod3(x) for x in v)
    if v[2]==2: v=tuple(mod3(2*x) for x in v)
    assert v[2]==1
    return (v[0],v[1],v[3])
def coord_vec(c):
    a,b,d=c
    return (a,b,1,d)
def srg_signature(G:nx.Graph):
    deg=sorted(set(dict(G.degree()).values()))
    lam,mu=Counter(),Counter()
    for u,v in combinations(G.nodes(),2):
        cn=len(set(G.neighbors(u)) & set(G.neighbors(v)))
        (lam if G.has_edge(u,v) else mu)[cn]+=1
    return {'vertices':G.number_of_nodes(),'edges':G.number_of_edges(),'degree_set':deg,'lambda_histogram':dict(sorted(lam.items())),'mu_histogram':dict(sorted(mu.items())),'is_srg':len(deg)==1 and len(lam)==1 and len(mu)==1,'parameters':[G.number_of_nodes(),deg[0],next(iter(lam)) if lam else None,next(iter(mu)) if mu else None] if len(deg)==1 and len(lam)==1 and len(mu)==1 else None}
def main():
    pts=projective_points(); anchor=rep((1,0,0,0)); assert len(pts)==40
    W=nx.Graph(); W.add_nodes_from(pts)
    for u,v in combinations(pts,2):
        if form(u,v)==0: W.add_edge(u,v)
    assert srg_signature(W)['parameters']==[40,12,2,4]
    shell=sorted([p for p in pts if p!=anchor and not W.has_edge(anchor,p)], key=shell_coord)
    coords=[shell_coord(p) for p in shell]; shell_set=set(shell); assert len(coords)==27
    raw=nx.Graph(); raw.add_nodes_from(coords)
    for x,y in combinations(coords,2):
        if form(coord_vec(x),coord_vec(y))==0: raw.add_edge(x,y)
    raw_sig=srg_signature(raw); assert raw_sig['degree_set']==[8] and raw.number_of_edges()==108
    lines=sorted({projective_line(u,v) for u,v in combinations(pts,2) if form(u,v)==0}, key=lambda L: sorted(L))
    assert len(lines)==40 and all(len(L)==4 for L in lines)
    old_lines=[]
    for L in lines:
        if anchor in L: continue
        sh=tuple(sorted(shell_coord(x) for x in L if x in shell_set))
        assert len(sh)==3
        old_lines.append(sh)
    new_lines=[tuple((a,b,d) for a in F) for b,d in product(F,F)]
    assert len(old_lines)==36 and len(new_lines)==9
    payne_lines=old_lines+new_lines
    point_line_degree=Counter(p for L in payne_lines for p in L)
    assert set(point_line_degree.values())=={5}
    payne=nx.Graph(); payne.add_nodes_from(coords)
    for L in payne_lines:
        for x,y in combinations(L,2): payne.add_edge(x,y)
    payne_sig=srg_signature(payne); assert payne_sig['parameters']==[27,10,1,5]
    sch=nx.complement(payne); sch_sig=srg_signature(sch); assert sch_sig['parameters']==[27,16,10,8]
    payload={'bt':'BT1789','title':'H27 Payne tuple extractor','anchor':list(anchor),'coordinate_model':'non-neighbours of anchor are (a,b,d) from projective vector (a,b,1,d) over F3','w33_collinearity':srg_signature(W),'local_shell':{'vertices':27,'raw_second_subconstituent':raw_sig,'interpretation':'raw affine H27 shell / AG(3,3) bulk; not yet Schlaefli or GQ(2,4)'},'payne_derivation':{'old_w33_lines_not_through_anchor':len(old_lines),'new_heisenberg_vertical_fibres':len(new_lines),'total_lines':len(payne_lines),'line_size':3,'point_line_degree_set':sorted(set(point_line_degree.values())),'payne_collinearity':payne_sig,'schlafli_complement':sch_sig,'new_fibre_template':'for fixed (b,d), {(0,b,d),(1,b,d),(2,b,d)}'},'tuple_lists':{'old_line_triples':[list(map(list,L)) for L in old_lines],'new_heisenberg_triples':[list(map(list,L)) for L in new_lines]},'conclusion':'The user H27 instinct is correct after the index correction: the raw 27 non-neighbour shell is 8-regular, but Payne derivation by adjoining the 9 Heisenberg vertical fibres turns it into GQ(2,4)=SRG(27,10,1,5); its complement is the Schlaefli graph SRG(27,16,10,8). This is a transformed local shell, not the raw dual of W(3,3) collinearity.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'raw':raw_sig['parameters'],'payne':payne_sig['parameters'],'schlafli':sch_sig['parameters'],'lines':{'old':36,'new':9,'total':45}},indent=2,sort_keys=True))
if __name__=='__main__': main()
