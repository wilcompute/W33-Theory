#!/usr/bin/env python3
"""Pass 4685 — mixed-technology optimizer on the exact base/Petersen split.

The selected270 graph is treated as two technology classes: 1620 robust-base
edges and 405 Petersen shortcut edges.  Multiobjective path search records
(base hops, shortcut hops) exactly for every pair, then scalarizes with arbitrary
positive per-edge cost ratio r=c_shortcut/c_base.  There are exactly four policy
regions separated at r=1,3/2,2.

A sensitivity example puts a 4-stage degree-12 MZI fabric on base edges and a
2-stage degree-3 EO fabric on Petersen edges, plus a common 1-cm SiN path.  The
component numbers are deliberately drawn from separate demonstrations and are
not claimed as one integrated stack.
"""
from __future__ import annotations
import heapq,itertools,json,math
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
from w33_pass4595_concrete_d4_triality_w33_lifts import max_generators
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4685_MIXED_TECH_PETERSEN_OPTIMIZER_REGEN.json'

def pareto_labels(G,hotset,source):
    labs=[set() for _ in G];labs[source].add((0,0));Q=[(0,0,source)]
    while Q:
        b,s,u=heapq.heappop(Q)
        if (b,s) not in labs[u]:continue
        for v in G[u]:
            hot=tuple(sorted((u,v))) in hotset;z=(b+(0 if hot else 1),s+(1 if hot else 0))
            if any(x<=z[0] and y<=z[1] for x,y in labs[v]):continue
            labs[v]={p for p in labs[v] if not(z[0]<=p[0] and z[1]<=p[1])};labs[v].add(z);heapq.heappush(Q,(z[0],z[1],v))
    return labs

def main():
    _,_,_,_,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    j=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]]);V=set(span(B9));rep=lambda x:min(int(x),int(x)^j);q=lambda x:(rep(x).bit_count()//4)&1;polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    singular=sorted(x for x in {rep(v) for v in V} if x and q(x)==0);sidx={x:i for i,x in enumerate(singular)}
    def fib(ap):
        x=0
        for i in ap:x^=cols[int(i)]
        return rep(x)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(ap) for ap in apartments});selsets=[set(L) for L in selected]
    N=np.zeros((135,270),dtype=np.int64)
    for c,L in enumerate(selected):
        for x in L:N[sidx[x],c]=1
    Al=N.T@N-3*np.eye(270,dtype=np.int64);G=nx.from_numpy_array(Al)
    O27=[]
    for X in max_generators(singular,rep,q,polar):
        I=frozenset(i for i,L in enumerate(selsets) if L.issubset(X))
        if len(I)==10:O27.append(I)
    comp={}
    for a,S in enumerate(O27):
        for v in S:comp[v]=a
    hotset={tuple(sorted((u,v))) for u,v in G.edges if comp[u]==comp[v]};assert len(hotset)==405

    expected={
      ((2,1),(3,0)):96,((2,0),):64,((1,1),(3,0)):48,
      ((1,2),(3,1),(4,0)):24,((1,2),(3,0)):16,
      ((1,0),):12,((0,2),(2,1),(4,0)):6,((0,1),(2,0)):3,((0,0),):1}
    profiles=[]
    for u in range(270):
        L=pareto_labels(G,hotset,u);C=Counter(tuple(sorted(z)) for z in L);assert C==Counter(expected);profiles.append(C)

    regions=[('R0_shortcut_favor',0.5,'0<r<1'),('R1_mixed',1.2,'1<r<3/2'),('R2_base_favor',1.7,'3/2<r<2'),('R3_base_only',3.0,'r>2')]
    policy={}
    cats=[(n,list(k)) for k,n in expected.items() if k!=((0,0),)]
    for name,r,interval in regions:
        B=S=0;chosen=[]
        for n,alts in cats:
            z=min(alts,key=lambda p:p[0]+r*p[1]);B+=n*z[0];S+=n*z[1];chosen.append({'destinations':n,'options':[list(x) for x in alts],'chosen':list(z)})
        policy[name]={'ratio_interval':interval,'base_traversals_per_source':B,'shortcut_traversals_per_source':S,'mean_base_hops':B/269,'mean_shortcut_hops':S/269,'unordered_pair_base_traversals':135*B,'unordered_pair_shortcut_traversals':135*S,'choice_table':chosen}
    assert [(policy[x]['base_traversals_per_source'],policy[x]['shortcut_traversals_per_source']) for x,_,_ in regions]==[(420,239),(548,111),(620,63),(746,0)]

    # Mixed component sensitivity anchors + explicit switch-depth assumptions.
    wave_db_m=1.77;edge_m=.01;ng=1.4642;c0=299792458.0;det=.98
    base={'switch':'MZI','degree':12,'stages':4,'switch_il_db':.38,'switch_time_s':14e-6}
    short={'switch':'EO','degree':3,'stages':2,'switch_il_db':1.05,'switch_time_s':1.27e-9}
    Lb=base['stages']*base['switch_il_db']+wave_db_m*edge_m;Ls=short['stages']*short['switch_il_db']+wave_db_m*edge_m
    Tb=base['stages']*base['switch_time_s']+ng*edge_m/c0;Ts=short['stages']*short['switch_time_s']+ng*edge_m/c0
    # Loss and latency choose different exact combinatorial regions.
    assert 1 < Ls/Lb < 1.5 and Ts/Tb < 1
    for name,_,_ in regions:
        p=policy[name];B=p['base_traversals_per_source'];S=p['shortcut_traversals_per_source']
        p['sensitivity_mean_loss_db']=(B*Lb+S*Ls)/269;p['sensitivity_mean_latency_s']=(B*Tb+S*Ts)/269
        # exact destination-class average success, not exp(-mean loss)
        succ=0.0
        for row in p['choice_table']:
            b,s=row['chosen'];succ+=row['destinations']*det*10**(-(b*Lb+s*Ls)/10)
        p['sensitivity_mean_success']=succ/269
    assert policy['R0_shortcut_favor']['sensitivity_mean_success'] < policy['R1_mixed']['sensitivity_mean_success']
    # With these anchors R0 is fastest, R1 has best transmission; R2/R3 are dominated.

    out={'pass':4685,
      'exact_path_frontier':{'uniform_over_270_sources':True,'destination_profile':{str(k):v for k,v in expected.items()},'scalar_cost_ratio':'r=c_shortcut/c_base','breakpoints':[1,1.5,2],'regions':policy},
      'reliability_mapping':'For independent edge survivals q_b,q_s, set c_b=-ln(q_b), c_s=-ln(q_s); the same exact breakpoints apply to maximum-survival routing.',
      'sensitivity_model':{'base':base,'shortcut':short,'waveguide_loss_db_per_m':wave_db_m,'edge_length_m':edge_m,'group_index_assumption':ng,'detector_efficiency_benchmark':det,'base_edge_loss_db':Lb,'shortcut_edge_loss_db':Ls,'base_edge_latency_s':Tb,'shortcut_edge_latency_s':Ts,'loss_ratio_shortcut_over_base':Ls/Lb,'latency_ratio_shortcut_over_base':Ts/Tb,'loss_optimal_region':'R1_mixed','latency_optimal_region':'R0_shortcut_favor','pareto_regions_for_these_anchors':['R0_shortcut_favor','R1_mixed'],'warning':'component-mixed published anchors plus explicit architecture assumptions; not a demonstrated integrated stack'},
      'theorem':'The exact selected270 base/Petersen graph has four all-pairs path policies separated only by c_s/c_b=1,3/2,2. Distinct base and shortcut technologies therefore admit analytic crossover regions rather than one architecture-wide winner.',
      'boundary':'Exact finite multiobjective routing plus parameter sensitivity. Published component values come from separate platforms; no measured Holonet performance is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
