#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1792_true_tuple_recovery_audit.json'
F=range(3)
COUNTS=[528,562,578,528,612,580,528,528,480,528,612,564,562,528,578,562,562,560]
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
    raw=nx.Graph(); raw.add_nodes_from(coords)
    for x,y in combinations(coords,2):
        if form((x[0],x[1],1,x[2]),(y[0],y[1],1,y[2]))==0: raw.add_edge(x,y)
    gq=nx.Graph(); gq.add_nodes_from(coords)
    for L in old+new:
        for x,y in combinations(L,2): gq.add_edge(x,y)
    return raw,gq,nx.complement(gq),old,new

def main():
    raw,gq,sch,old,new=build()
    payload={
        'bt':'BT1792',
        'title':'true BT1781 tuple recovery audit',
        'status':'blocked_missing_predicate',
        'searched_sources':['analysis/BT1779_BT1781_summary.md','analysis/BT1781_consistency_census.md','analysis/BT1784_relational_solver_frontier.md','analysis/BT1787_solver_materialization_note.md','analysis/BT1788_hesse_relation_materializer.md','GitHub code search: 9980, accepted local triples, BT1781, 528/612 counts'],
        'found_artifacts':{'table_counts':COUNTS,'accepted_entries':sum(COUNTS),'raw_entries':18*12**3,'actual_tuple_lists_found':False,'acceptance_predicate_found':False},
        'networkx_reconstruction':{'raw_local_27_shell':srg(raw),'payne_gq24':srg(gq),'schlaefli_complement':srg(sch),'old_w33_triples':len(old),'new_heisenberg_fibres':len(new),'total_h27_support_triples':len(old)+len(new)},
        'index_html_constraint':'live index says raw 27 is 8-regular affine H27 shell; nine central-fibre triples give GQ(2,4) and the Schlaefli complement.',
        'decision':'Do not fabricate true tuple lists from counts. The recoverable executable object is the H27/Payne target geometry and the projection scaffold; the real BT1781 acceptance predicate or tuple lists remain the next missing source artifact.'
    }
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'status':payload['status'],'accepted_entries':sum(COUNTS),'raw27':srg(raw)['degree_set'],'gq':srg(gq)['parameters'],'schlafli':srg(sch)['parameters']},indent=2,sort_keys=True))
if __name__=='__main__': main()
