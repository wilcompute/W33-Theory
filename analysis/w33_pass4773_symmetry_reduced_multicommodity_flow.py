#!/usr/bin/env python3
"""Pass 4773 — symmetry-reduced adversarial multicommodity flow on selected270.

For the intact router, PSp(4,3) has eleven nontrivial ordered-pair orbitals and
is transitive on each of the 1620 cold edges and 405 hot Petersen edges.  For
one representative target in each pair orbital we enumerate every nondominated
path signature (#cold,#hot).  Averaging a path over PSp gives uniform load on
each edge orbit.  Therefore the exact all-ordered-pairs concurrent-flow problem
reduces to a two-resource convex polygon: the Minkowski sum of the eleven path
signature polytopes, weighted by orbital sizes.

The integer lower convex frontier is frozen exactly.  For any rational hot-edge
capacity rho (cold capacity 1), the optimum is obtained by intersecting that
frontier with the balance ray H/C=rho/4 or by an endpoint.  Targeted shortcut
outages and full Petersen-fiber removals break transitivity, so for them we
report a canonical all-shortest-path feasible throughput and rigorous cut upper
bounds rather than pretending the intact symmetry reduction still applies.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from fractions import Fraction
from pathlib import Path
import networkx as nx
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4773_SYMMETRY_REDUCED_MULTICOMMODITY_FLOW.json'

def lower_hull(points):
    # nondominated southwest points then lower convex hull, exact integer coords
    best={}
    for x,y in points:
        if x not in best or y<best[x]:best[x]=y
    nd=[];m=None
    for x in sorted(best):
        y=best[x]
        if m is None or y<m:nd.append((x,y));m=y
    H=[]
    for p in nd:
        while len(H)>=2:
            a,b=H[-2],H[-1]
            cross=(b[0]-a[0])*(p[1]-b[1])-(b[1]-a[1])*(p[0]-b[0])
            if cross<=0:H.pop()
            else:break
        H.append(p)
    return H

def pareto_paths(G,cold,hot,s,t):
    labels=[set() for _ in G.nodes()];labels[s].add((0,0));Q=deque([(s,0,0)])
    while Q:
        u,c,h=Q.popleft()
        if (c,h) not in labels[u]:continue
        for v in G[u]:
            e=tuple(sorted((u,v)));nc=c+(e in cold);nh=h+(e in hot)
            S=labels[v]
            if any(a<=nc and b<=nh for a,b in S):continue
            rem=[q for q in S if nc<=q[0] and nh<=q[1]]
            for q in rem:S.remove(q)
            S.add((nc,nh));Q.append((v,nc,nh))
    return lower_hull(labels[t])

def optimum(frontier,rho):
    rho=Fraction(rho);cand=[]
    def add(C,H,where):
        q=max(C/Fraction(1620),H/(Fraction(405)*rho));cand.append((Fraction(1,1)/q,C,H,where))
    for i,(C,H) in enumerate(frontier):add(Fraction(C),Fraction(H),f'vertex{i}')
    for i,((C1,H1),(C2,H2)) in enumerate(zip(frontier,frontier[1:])):
        dC=C2-C1;dH=H2-H1;den=Fraction(405)*rho*dC-Fraction(1620)*dH
        if den==0:continue
        t=(Fraction(1620)*H1-Fraction(405)*rho*C1)/den
        if 0<=t<=1:
            C=Fraction(C1)+t*dC;H=Fraction(H1)+t*dH;add(C,H,f'edge{i}-{i+1}')
    return max(cand,key=lambda z:z[0])

def shortest_feasible(H):
    bc=nx.edge_betweenness_centrality(H,normalized=False,weight=None)
    mx=max(float(v) for v in bc.values())*2.0 # ordered unit demand
    lb=1.0/mx
    n=H.number_of_nodes();cutub=min(H.degree(v)/(2*(n-1)) for v in H.nodes())
    return {'vertices':n,'edges':H.number_of_edges(),'diameter':nx.diameter(H),'ordered_shortest_path_max_edge_load':mx,
            'feasible_concurrent_lambda':lb,'single_vertex_cut_upper_bound':cutub}

def main():
    D=build_all();B=build_bundle();hot={tuple(sorted(e)) for e in B['hot']};cold={tuple(sorted(e)) for e in B['cold']}
    Gnx=nx.Graph();Gnx.add_nodes_from(range(270));Gnx.add_edges_from(hot|cold);assert set(dict(Gnx.degree()).values())=={15}
    residues=D['residues'];phiR=D['phiR'];PG=D['G'];ridx={r:i for i,r in enumerate(residues)}
    invphi={v:k for k,v in phiR.items()};br=invphi[0]
    def ar(i,g):return ridx[tuple(sorted(g[x] for x in residues[i]))]
    H={g for g in PG if ar(br,g)==br};assert len(H)==96
    unseen=set(range(270));orbs=[]
    while unseen:
        r=min(unseen);O={ar(r,h) for h in H};orbs.append(sorted(O));unseen-=O
    orbs.sort(key=lambda O:(0 if br in O else 1,len(O),min(O)))
    non=[O for O in orbs if br not in O];assert sum(map(len,non))==269

    orbit_rows=[];poly=[(0,0)]
    for O in non:
        t=phiR[O[0]];P=pareto_paths(Gnx,cold,hot,0,t);d=len(O);mult=270*d
        orbit_rows.append({'subdegree':d,'ordered_pair_count':mult,'representative_target':t,'path_signature_frontier':[list(x) for x in P]})
        scaled=[(mult*c,mult*h) for c,h in P]
        poly=lower_hull([(a+c,b+h) for a,b in poly for c,h in scaled])
    assert sum(r['ordered_pair_count'] for r in orbit_rows)==270*269
    frontier=poly

    rhos=[Fraction(1,10),Fraction(1,4),Fraction(1,2),Fraction(1),Fraction(2),Fraction(4),Fraction(10),Fraction(36),Fraction(100)]
    samples=[]
    for rho in rhos:
        lam,C,Huse,where=optimum(frontier,rho)
        samples.append({'rho':str(rho),'lambda':str(lam),'lambda_float':float(lam),'aggregate_cold_usage_per_unit_lambda':str(C),
                        'aggregate_hot_usage_per_unit_lambda':str(Huse),'active':where})
    equal=next(r for r in samples if r['rho']=='1')
    slopes=[]
    for C,Huse in frontier:
        if C:slopes.append({'vertex':[C,Huse],'balance_rho':str(Fraction(4*Huse,C))})

    # Exact quotient all-pairs theorem: 27 vertices, degree10, diameter2, edge cap12.
    K5=B['K5'];qG=nx.Graph();qG.add_nodes_from(range(27))
    for a,b in itertools.combinations(range(27),2):
        if K5[a]&K5[b]:qG.add_edge(a,b)
    assert qG.number_of_edges()==135 and set(dict(qG.degree()).values())=={10} and nx.diameter(qG)==2
    totaldist=sum(nx.shortest_path_length(qG,u,v) for u in qG for v in qG if u!=v)
    assert totaldist==1134
    quotient_lambda=Fraction(135*12,totaldist);assert quotient_lambda==Fraction(10,7)

    # Failure cases at equal physical edge capacity. owner partitions the 270 router vertices into 27 Petersen fibers.
    owner=[]
    for T in B['projected']:
        hit=[i for i,S in enumerate(K5) if set(T)<=S];assert len(hit)==1;owner.append(hit[0])
    fibers=[set(i for i,a in enumerate(owner) if a==f) for f in range(27)];assert set(map(len,fibers))=={10}
    adj=next(iter(qG.edges()));nonadj=next((a,b) for a,b in itertools.combinations(range(27),2) if not qG.has_edge(a,b))
    failures={}
    cases=[('one_hot_outage',(0,),False),('two_hot_adjacent',adj,False),('two_hot_nonadjacent',nonadj,False),
           ('one_vertex_fiber_removed',(0,),True),('two_vertex_adjacent_removed',adj,True),('two_vertex_nonadjacent_removed',nonadj,True)]
    for name,F,node_remove in cases:
        F=tuple(F);R=set().union(*(fibers[f] for f in F));Hf=Gnx.copy()
        if node_remove:Hf.remove_nodes_from(R)
        else:
            rem=[e for e in hot if owner[e[0]] in F and owner[e[0]]==owner[e[1]]]
            Hf.remove_edges_from(rem)
        assert nx.is_connected(Hf);failures[name]=shortest_feasible(Hf)

    out={'pass':4773,'demand_convention':'unit demand for every ordered distinct vertex pair; cold edge capacity 1, hot edge capacity rho',
      'intact_router':{'pair_orbits':len(non),'orbit_data':orbit_rows,'aggregate_integer_usage_frontier':[list(x) for x in frontier],
        'balance_rho_at_frontier_vertices':slopes,'sample_optima':samples,'equal_capacity_exact_lambda':equal['lambda']},
      'quotient_27':{'graph':'SRG(27,10,1,5)','ordered_all_pairs_total_shortest_traversals':totaldist,'physical_cold_capacity_per_quotient_edge':12,
        'exact_concurrent_lambda':str(quotient_lambda),'proof':'total-capacity/distance upper bound is attained by automorphism-averaged shortest routing'},
      'failure_cases_equal_capacity':failures,
      'theorem':'PSp symmetry reduces intact selected270 all-ordered-pairs concurrent flow exactly to the integer lower convex frontier of aggregate cold/hot path usage across eleven pair orbitals. The frontier determines the exact throughput for every rational hot/cold capacity ratio. The 27-fiber quotient has exact all-pairs throughput 10/7 in the ordered-demand convention. Symmetry-breaking failure cases are supplied with explicit all-shortest-path feasible throughputs and rigorous single-vertex-cut upper bounds.',
      'boundary':'Exact fractional multicommodity-flow theorem for the intact symmetric router and quotient. Failure-case shortest routing is a certified feasible lower bound, not claimed optimal; no queueing, latency or measured hardware model is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
