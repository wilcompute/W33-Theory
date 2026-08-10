#!/usr/bin/env python3
"""Pass 4660 — topology-aware Holonet routing/congestion optimizer.

This replaces Pass4652's common-hop shell score with exact graph routing plus an
explicit switch-fabric model. Four finite routers are reconstructed from W33:
W33 itself, the selected 135-point and 270-line graphs, and the 160-flag Levi
line graph. Fractional all-shortest-path edge betweenness is computed exactly.

Hardware sensitivity uses two published component archetypes, deliberately not
claimed as one integrated stack: (i) 0.38 dB / 14 us MZI switches; (ii) 1.05 dB
/ 1.27 ns EO switches. Waveguide propagation is 1.77 dB/m. A 98% SNSPD system
efficiency is used as a detector benchmark. The design assumptions are a 1 cm
edge and ceil(log2 degree) binary switch stages per graph hop.

The main new topology result is independent of those hardware assumptions: the
270-router's 2025 edges split into exact all-pairs-betweenness classes 1620+405.
The 405 high-load edges form 27 disjoint Petersen graphs, exactly on the ten
selected lines contained in each of the 27 internal Schlaefli generators.
Deleting that entire shortcut orbit leaves a connected 12-regular graph of
diameter 4 and edge connectivity 12.
"""
from __future__ import annotations
import itertools, json, math
from collections import Counter, defaultdict
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span
from w33_pass4595_concrete_d4_triality_w33_lifts import max_generators
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4660_TOPOLOGY_AWARE_HOLONET_OPTIMIZER_REGEN.json'

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry(); Astar=np.asarray(Astar,dtype=np.uint8)
    n=40; j=(1<<n)-1
    cols=[]
    for c in range(n):
        m=0
        for r in np.flatnonzero(Astar[:,c]): m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(n) for k in range(i+1,n) if Astar[i,k]])
    V=set(span(B9)); rep=lambda x:min(int(x),int(x)^j)
    q=lambda x:(rep(x).bit_count()//4)&1
    polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    singular=sorted(x for x in {rep(v) for v in V} if x and q(x)==0)
    def ap_fiber(ap):
        x=0
        for i in ap:x^=cols[int(i)]
        return rep(x)
    def ap_line(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        s=rep(cols[opp[0][0]]^cols[opp[0][1]]); t=rep(cols[opp[1][0]]^cols[opp[1][1]])
        return tuple(sorted((s,t,ap_fiber(ap))))
    selected=sorted({ap_line(ap) for ap in apartments}); assert len(selected)==270
    sidx={x:i for i,x in enumerate(singular)}
    N=np.zeros((135,270),dtype=np.int64)
    for c,L in enumerate(selected):
        for x in L:N[sidx[x],c]=1
    Ap=N@N.T-6*np.eye(135,dtype=np.int64); Al=N.T@N-3*np.eye(270,dtype=np.int64)

    GW=nx.from_numpy_array(Astar); GP=nx.from_numpy_array(Ap); GL=nx.from_numpy_array(Al)
    flags=[(p,li) for li,L in enumerate(lines) for p in sorted(L)]; GF=nx.Graph(); GF.add_nodes_from(range(160))
    byp=defaultdict(list); byl=defaultdict(list)
    for i,(p,li) in enumerate(flags): byp[p].append(i); byl[li].append(i)
    for S in list(byp.values())+list(byl.values()): GF.add_edges_from(itertools.combinations(S,2))
    graphs={'W33':GW,'selected135':GP,'selected270':GL,'Levi160':GF}

    graph_metrics={}
    for name,G in graphs.items():
        eb=nx.edge_betweenness_centrality(G,normalized=False); vals=list(eb.values()); nn=G.number_of_nodes(); mm=G.number_of_edges()
        graph_metrics[name]={
          'vertices':nn,'edges':mm,'degree':next(iter(dict(G.degree()).values())),'diameter':nx.diameter(G),
          'mean_distance':nx.average_shortest_path_length(G),'edge_connectivity':nx.edge_connectivity(G),
          'fractional_shortest_path_edge_load_min':min(vals),'fractional_shortest_path_edge_load_max':max(vals),
          'fractional_shortest_path_edge_load_mean':sum(vals)/mm,
          'normalized_max_load_per_unordered_pair':max(vals)/math.comb(nn,2),
          'edge_load_census':{str(k):v for k,v in sorted(Counter(round(x,12) for x in vals).items())}}

    assert graph_metrics['W33']['edge_load_census']=={'5.5':240}
    assert graph_metrics['selected135']['edge_load_census']=={'26.833333333333':810}
    assert graph_metrics['selected270']['edge_load_census']=={'38.377777777778':1620,'66.155555555556':405}
    assert graph_metrics['Levi160']['edge_load_census']=={'88.0':480}

    # Identify the 405 hot edges with the 27 internal ten-line carriers.
    eb270=nx.edge_betweenness_centrality(GL,normalized=False); vmax=max(eb270.values())
    hot=[e for e,v in eb270.items() if abs(v-vmax)<1e-9]; assert len(hot)==405
    H=nx.Graph(); H.add_nodes_from(GL); H.add_edges_from(hot)
    comps=[frozenset(c) for c in nx.connected_components(H)]
    assert len(comps)==27 and all(len(c)==10 for c in comps)
    assert all(nx.is_isomorphic(H.subgraph(c),nx.petersen_graph()) for c in comps)
    MG=max_generators(singular,rep,q,polar); O27=[]
    selsets=[set(L) for L in selected]
    for X in MG:
        I=frozenset(i for i,L in enumerate(selsets) if L.issubset(X))
        if len(I)==10: O27.append(I)
    assert len(O27)==27 and set(O27)==set(comps)
    cold=[e for e,v in eb270.items() if abs(v-vmax)>=1e-9]
    C=nx.Graph(); C.add_nodes_from(GL); C.add_edges_from(cold)
    assert nx.is_connected(C) and set(dict(C.degree()).values())=={12}
    assert nx.diameter(C)==4 and nx.edge_connectivity(C)==12

    # Component-mixed hardware sensitivity anchors.
    waveguide_db_per_m=1.77; edge_length_m=0.01; group_index=1.4642; detector=0.98; c0=299792458.0
    techs={'MZI_thermal':{'switch_il_db':0.38,'switch_time_s':14e-6},'EO_fast':{'switch_il_db':1.05,'switch_time_s':1.27e-9}}
    physical={}
    for tech,t in techs.items():
        per={}
        for name,G in graphs.items():
            degree=next(iter(dict(G.degree()).values())); stages=math.ceil(math.log2(degree)); hopdb=stages*t['switch_il_db']+waveguide_db_per_m*edge_length_m
            hoplat=stages*t['switch_time_s']+group_index*edge_length_m/c0
            lengths=dict(nx.all_pairs_shortest_path_length(G)); nn=G.number_of_nodes()
            ds=[lengths[u][v] for u in range(nn) for v in range(u+1,nn)]
            success=[detector*10**(-hopdb*d/10) for d in ds]
            per[name]={'switch_stages_per_graph_hop':stages,'hop_loss_db':hopdb,'hop_latency_s':hoplat,
              'mean_end_to_end_success':sum(success)/len(success),'aggregate_unordered_pair_success':sum(success),
              'worst_shortest_path_success':detector*10**(-hopdb*nx.diameter(G)/10),
              'mean_end_to_end_latency_s':(sum(ds)/len(ds))*hoplat,
              'max_fractional_shortest_path_edge_load':graph_metrics[name]['fractional_shortest_path_edge_load_max']}
        physical[tech]=per

    out={'pass':4660,'exact_topology':graph_metrics,
      'selected270_shortcut_layer':{'high_load_edges':405,'low_load_edges':1620,'high_load_components':27,'component_vertices':10,'component_graph':'Petersen','components_equal_internal_degree27_ten-line_carriers':True,'after_removing_high_orbit':{'connected':True,'degree':12,'diameter':4,'edge_connectivity':12}},
      'hardware_model':{'design_assumptions':{'edge_length_m':edge_length_m,'binary_router_switch_depth':'ceil(log2 degree)','group_index':group_index},'published_sensitivity_anchors':{'waveguide_loss_db_per_m':waveguide_db_per_m,'detector_efficiency':detector,'MZI':'0.38 dB, 14 us','EO':'1.05 dB model midpoint of 1.04/1.06 dB, 1.27 ns fall-time'},'warning':'component-mixed benchmarks; not a demonstrated integrated stack'},
      'physical_sensitivity':physical,
      'theorem':'Topology-aware routing exposes a 405-edge high-load shortcut orbit in the selected270 router: it is exactly 27 disjoint Petersen graphs carried by the internal 27 Schlaefli objects. The base 1620-edge graph remains connected and 12-edge-connected without it. Hardware sensitivity preserves a Pareto frontier rather than a universal winner.',
      'boundary':'Exact finite routing/congestion plus parameterized component sensitivity. Edge length and router depth are explicit design assumptions; no measured Holonet performance is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps(out,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
