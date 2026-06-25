#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1790_h27_frontier_sheaf_solver.json'
F=range(3); FRONTIER_TYPES=['RC','RD','CD']
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
def srg(G):
    deg=sorted(set(dict(G.degree()).values())); lam=Counter(); mu=Counter()
    for u,v in combinations(G.nodes(),2):
        cn=len(set(G.neighbors(u)) & set(G.neighbors(v)))
        (lam if G.has_edge(u,v) else mu)[cn]+=1
    return {'vertices':G.number_of_nodes(),'edges':G.number_of_edges(),'degree_set':deg,'lambda_histogram':dict(sorted(lam.items())),'mu_histogram':dict(sorted(mu.items())),'parameters':[G.number_of_nodes(),deg[0],next(iter(lam)),next(iter(mu))] if len(deg)==1 and len(lam)==1 and len(mu)==1 else None}
def build_payne():
    pts=projective_points(); anchor=rep((1,0,0,0)); shell=set(p for p in pts if p!=anchor and form(anchor,p)!=0)
    coords=sorted(shell_coord(p) for p in shell)
    lines=sorted({projective_line(u,v) for u,v in combinations(pts,2) if form(u,v)==0}, key=lambda L: sorted(L))
    old=[]
    for L in lines:
        if anchor in L: continue
        sh=tuple(sorted(shell_coord(x) for x in L if x in shell)); assert len(sh)==3
        old.append(sh)
    new=[tuple((a,b,d) for a in F) for b,d in product(F,F)]
    G=nx.Graph(); G.add_nodes_from(coords)
    for L in old+new:
        for x,y in combinations(L,2): G.add_edge(x,y)
    return coords, old, new, old+new, G
def main():
    coords,old,new,all_lines,G=build_payne(); sch=nx.complement(G)
    assert srg(G)['parameters']==[27,10,1,5]
    assert srg(sch)['parameters']==[27,16,10,8]
    checks=0
    for p in coords:
        for L in all_lines:
            if p in L: continue
            hits=[q for q in L if G.has_edge(p,q)]
            checks+=1; assert len(hits)==1
    assert checks==1080
    vertical=[[f'{t}{u}{v}' for t in FRONTIER_TYPES] for u,v in product(F,F)]
    incident=defaultdict(list)
    for i,L in enumerate(old):
        for p in L: incident[p].append(('old',f'O{i:02d}'))
    for i,L in enumerate(new):
        for p in L: incident[p].append(('new',f'N{i:02d}'))
    pencil=Counter(len(v) for v in incident.values()); old_new=Counter((sum(k=='old' for k,_ in ls),sum(k=='new' for k,_ in ls)) for ls in incident.values())
    assert pencil=={5:27} and old_new=={(4,1):27}
    payload={'bt':'BT1790','title':'27-frontier H27 sheaf solver','frontier_identification':{'bt1788_pair_frontiers':'{RC,RD,CD} x F3 x F3 = 27','h27_coordinate':'(layer,u,v) in F3^3','vertical_fibres':vertical},'payne_sheaf':{'points':27,'old_W33_line_patches':36,'new_H27_vertical_patches':9,'total_line_patches':45,'line_size':3,'point_pencil_size_histogram':dict(pencil),'point_pencil_old_new_histogram':{f'old={k[0]},new={k[1]}':v for k,v in old_new.items()},'gq_axiom_checks':checks,'gq_axiom_failures':0},'graphs':{'gq24_collinearity':srg(G),'schlafli_dual_complement':srg(sch)},'conclusion':'The 27-frontier object is exactly the H27/Payne boundary: GQ(2,4)=SRG(27,10,1,5), with Schlaefli dual complement SRG(27,16,10,8).'}
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'gq':[27,10,1,5],'schlafli':[27,16,10,8],'gq_axiom_checks':checks,'patches':{'old':36,'new':9,'total':45}},indent=2,sort_keys=True))
if __name__=='__main__': main()
