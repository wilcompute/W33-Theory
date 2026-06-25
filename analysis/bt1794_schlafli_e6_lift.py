#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1794_schlafli_e6_lift.json'
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
def srg(G):
    deg=sorted(set(dict(G.degree()).values())); lam=Counter(); mu=Counter()
    for u,v in combinations(G.nodes(),2):
        cn=len(set(G.neighbors(u)) & set(G.neighbors(v)))
        (lam if G.has_edge(u,v) else mu)[cn]+=1
    return {'vertices':G.number_of_nodes(),'edges':G.number_of_edges(),'degree_set':deg,'lambda_histogram':dict(sorted(lam.items())),'mu_histogram':dict(sorted(mu.items())),'parameters':[G.number_of_nodes(),deg[0],next(iter(lam)),next(iter(mu))] if len(deg)==1 and len(lam)==1 and len(mu)==1 else None}
def build():
    P=projective_points(); anchor=rep((1,0,0,0)); shell=set(p for p in P if p!=anchor and form(anchor,p)!=0)
    coords=sorted(shell_coord(p) for p in shell)
    lines=sorted({projective_line(u,v) for u,v in combinations(P,2) if form(u,v)==0}, key=lambda L: sorted(L))
    old=[]
    for L in lines:
        if anchor in L: continue
        sh=tuple(sorted(shell_coord(x) for x in L if x in shell)); assert len(sh)==3
        old.append(sh)
    new=[tuple((a,b,d) for a in F) for b,d in product(F,F)]
    gq=nx.Graph(); gq.add_nodes_from(coords)
    support=[tuple(sorted(L)) for L in old+new]
    for L in support:
        for x,y in combinations(L,2): gq.add_edge(x,y)
    return coords,support,gq,nx.complement(gq)
def main():
    coords,support,gq,sch=build()
    triangles=[tuple(sorted(c)) for c in combinations(gq.nodes(),3) if all(gq.has_edge(a,b) for a,b in combinations(c,2))]
    assert set(triangles)==set(support) and len(triangles)==45
    sixers=set(tuple(sorted(c)) for c in nx.find_cliques(sch) if len(c)==6)
    double_sixes=[]
    for A,B in combinations(sixers,2):
        if set(A)&set(B): continue
        cross=[(a,b) for a in A for b in B if sch.has_edge(a,b)]
        if len(cross)==6:
            da=Counter(a for a,b in cross); db=Counter(b for a,b in cross)
            if len(da)==6 and len(db)==6 and set(da.values())=={1} and set(db.values())=={1}:
                double_sixes.append((A,B,cross))
    assert len(sixers)==72 and len(double_sixes)==36
    vds=Counter()
    dprofile=Counter()
    for A,B,cross in double_sixes:
        for x in set(A)|set(B): vds[x]+=1
        H=sch.subgraph(set(A)|set(B)); dprofile[(H.number_of_nodes(),H.number_of_edges(),len(cross))]+=1
    tprofile=Counter()
    for T in support:
        counts=Counter(len(set(T)&(set(A)|set(B))) for A,B,c in double_sixes)
        tprofile[tuple(sorted(counts.items()))]+=1
    payload={'bt':'BT1794','title':'Schlaefli/E6 lift','graphs':{'gq24_intersection_graph':srg(gq),'schlaefli_skew_graph':srg(sch)},'tritangent_planes':{'count':len(support),'as_GQ_lines':len(support),'as_triangles_in_intersection_graph':len(triangles),'triangle_set_equal_to_H27_support':set(triangles)==set(support)},'sixers_and_double_sixes':{'sixers_K6_in_schlaefli':len(sixers),'double_sixes':len(double_sixes),'double_six_induced_profile':{str(k):v for k,v in dprofile.items()},'each_line_in_double_sixes_distribution':dict(Counter(vds.values()))},'double_six_tritangent_intersections':{'profile':{str(k):v for k,v in tprofile.items()}},'e6_reading':'The 27 H27 points are the 27 cubic-surface lines; GQ(2,4) collinearity is line-intersection/tritangent support, and the Schlaefli complement is the skew graph. NetworkX recovers the classical 36 double-sixes from the Schlaefli graph itself.'}
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'gq':srg(gq)['parameters'],'schlafli':srg(sch)['parameters'],'tritangents':len(support),'sixers':len(sixers),'double_sixes':len(double_sixes)},indent=2,sort_keys=True))
if __name__=='__main__': main()
