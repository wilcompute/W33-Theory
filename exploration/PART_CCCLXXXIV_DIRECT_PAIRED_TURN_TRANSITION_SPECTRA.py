#!/usr/bin/env python3
"""PART CCCLXXXIV -- Direct / Paired Turn-Transition Spectra.

Builds the actual open-turn transition operators for:

1. the base W33 graph G,
2. the paired graph Gbar.

For a graph X, the open-turn operator O_X acts on directed edges a->b by

    (a,b) -> (b,c)

when c is adjacent to b, c != a, and c is not adjacent to a.

The compiler computes exact sparse invariants:
- directed-edge carrier sizes,
- row sums and total transitions,
- trace moments tr(O^p) for p=1..6,
- modular rank over a large prime,
- exact full Hashimoto spectra for B_G and B_Gbar by Ihara-Bass.

Dense eigenvalue computation for O_X is intentionally not required for CI; the
trace moments are spectral invariants of the actual transition matrices.
"""
from __future__ import annotations
import cmath, itertools, json, math
from pathlib import Path
from typing import Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
P=1000003
Vector=Tuple[int,int,int,int]
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def mul(a,u): return tuple((a*u[i])%MOD for i in range(4))
def omega(x,y): return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%MOD
def canon(v):
    for a in v:
        if a%MOD: return mul(1 if a==1 else 2,v)
    raise ValueError('zero')
def points():
    pts=[]; seen=set()
    for v in itertools.product(range(MOD), repeat=4):
        if v==(0,0,0,0): continue
        c=canon(v)
        if c not in seen:
            seen.add(c); pts.append(c)
    return pts
def build_graph():
    pts=points(); adj=[set() for _ in pts]
    for i,j in itertools.combinations(range(len(pts)),2):
        if omega(pts[i],pts[j])==0:
            adj[i].add(j); adj[j].add(i)
    return pts,adj
def paired_graph(adj):
    n=len(adj)
    return [set(j for j in range(n) if j!=i and j not in adj[i]) for i in range(n)]
def directed_edges(adj): return [(i,j) for i in range(len(adj)) for j in sorted(adj[i])]
def open_turn_operator(adj):
    de=directed_edges(adj); index={e:i for i,e in enumerate(de)}; rows=[[] for _ in de]
    for r,(a,b) in enumerate(de):
        for c in sorted(adj[b]):
            if c!=a and c not in adj[a]: rows[r].append(index[(b,c)])
    return rows,de
def row_sums(rows): return [len(r) for r in rows]
def trace_power(rows,power):
    n=len(rows); total=0
    for start in range(n):
        frontier={start:1}
        for _ in range(power):
            nxt={}
            for u,count in frontier.items():
                for v in rows[u]: nxt[v]=nxt.get(v,0)+count
            frontier=nxt
        total+=frontier.get(start,0)
    return total
def trace_moments(rows,max_power=6): return {str(p):trace_power(rows,p) for p in range(1,max_power+1)}
def rank_mod_sparse(rows,p=P):
    basis={}; rank=0
    for row in rows:
        d={j:1 for j in row}
        while d:
            pivot=min(d); coeff=d[pivot]%p
            if coeff==0:
                del d[pivot]; continue
            if pivot not in basis:
                inv=pow(coeff,p-2,p)
                d={k:(v*inv)%p for k,v in d.items() if (v*inv)%p}
                basis[pivot]=d; rank+=1; break
            factor=coeff; prow=basis[pivot]
            for k,v in prow.items():
                d[k]=(d.get(k,0)-factor*v)%p
                if d[k]==0: del d[k]
    return rank
def hashimoto_spectrum_summary(k,adj_spectrum,edges,vertices):
    entries=[]; total=0
    for lam,mult in adj_spectrum:
        disc=lam*lam-4*(k-1)
        root=cmath.sqrt(disc)
        for z in ((lam+root)/2,(lam-root)/2):
            entries.append({"real":round(z.real,12),"imag":round(z.imag,12),"multiplicity":mult,"source_lambda":lam})
            total+=mult
    extra=edges-vertices
    entries.append({"real":1.0,"imag":0.0,"multiplicity":extra,"source_lambda":"extra"}); total+=extra
    entries.append({"real":-1.0,"imag":0.0,"multiplicity":extra,"source_lambda":"extra"}); total+=extra
    radius=max(math.hypot(e['real'],e['imag']) for e in entries)
    return {"k":k,"dimension":2*edges,"total_multiplicity":total,"spectral_radius":radius,"extra_each":extra,"entries":entries}
def operator_summary(name,adj,k,adj_spectrum):
    rows,de=open_turn_operator(adj); rs=row_sums(rows); E=sum(len(a) for a in adj)//2
    return {"name":name,"directed_edge_states":len(de),"row_sum_set":sorted(set(rs)),"transition_count":sum(rs),"trace_moments":trace_moments(rows,6),"rank_mod_1000003":rank_mod_sparse(rows),"full_hashimoto_spectrum":hashimoto_spectrum_summary(k,adj_spectrum,E,len(adj))}
def build_results():
    pts,G=build_graph(); H=paired_graph(G)
    base=operator_summary('base',G,12,[(12,1),(2,24),(-4,15)])
    pair=operator_summary('paired',H,27,[(27,1),(-3,24),(3,15)])
    checks=[]
    checks.append(ok('base directed states 480',base['directed_edge_states']==480,base['directed_edge_states']))
    checks.append(ok('paired directed states 1080',pair['directed_edge_states']==1080,pair['directed_edge_states']))
    checks.append(ok('base open row sum 9',base['row_sum_set']==[9],base['row_sum_set']))
    checks.append(ok('paired open row sum 8',pair['row_sum_set']==[8],pair['row_sum_set']))
    checks.append(ok('base transitions 4320',base['transition_count']==4320,base['transition_count']))
    checks.append(ok('paired transitions 8640',pair['transition_count']==8640,pair['transition_count']))
    checks.append(ok('base trace moments p1-p6',base['trace_moments']=={'1':0,'2':0,'3':0,'4':12960,'5':51840,'6':518400},base['trace_moments']))
    checks.append(ok('paired trace moments p1-p6',pair['trace_moments']=={'1':0,'2':0,'3':0,'4':43200,'5':51840,'6':120960},pair['trace_moments']))
    checks.append(ok('base open operator modular rank 160',base['rank_mod_1000003']==160,base['rank_mod_1000003']))
    checks.append(ok('paired open operator modular rank full',pair['rank_mod_1000003']==1080,pair['rank_mod_1000003']))
    checks.append(ok('Hashimoto spectral radii 11 and 26',abs(base['full_hashimoto_spectrum']['spectral_radius']-11)<1e-12 and abs(pair['full_hashimoto_spectrum']['spectral_radius']-26)<1e-12,{"base":base['full_hashimoto_spectrum']['spectral_radius'],"paired":pair['full_hashimoto_spectrum']['spectral_radius']}))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXXXIV","title":"Direct / Paired Turn-Transition Spectra","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"base_operator":base,"paired_operator":pair,"comparison":{"state_ratio":"1080/480=9/4","transition_ratio":"8640/4320=2","rank_contrast":"base open rank 160 vs paired open rank 1080 over prime 1000003","moment_contrast":"trace moments separate the two systems already at p=4"},"architecture_upgrade":"Builds the actual open-turn transition matrices for the base graph and paired graph, then compares trace moments, modular ranks, and exact full Hashimoto spectra.","theorem":"The base open-turn operator has 480 states, row sum 9, 4320 transitions, trace moments (0,0,0,12960,51840,518400), and modular rank 160. The paired open-turn operator has 1080 states, row sum 8, 8640 transitions, trace moments (0,0,0,43200,51840,120960), and full modular rank 1080. Thus the paired dynamics is not merely a doubled copy of the base dynamics; it has distinct spectral-moment and rank signatures.","honesty_boundary":"These are exact sparse operator invariants and full Hashimoto spectra. Dense eigenvalues of the open-turn operators are not forced in CI and can be added as an optional numerical refinement.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXXXIV_direct_paired_turn_transition_spectra_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
