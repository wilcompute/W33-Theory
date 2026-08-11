#!/usr/bin/env python3
"""Pass 4820 — exact symmetry-broken all-pairs fractional flow after fiber failures.

Pass4773 left six failure cases bracketed by an all-shortest-path feasible lower
bound and a vertex-cut upper bound.  Here each failure stabilizer H is computed
inside PSp(4,3).  Ordered commodities and surviving edges are reduced to H
orbits.  Instead of a huge arc-flow LP, solve the exact metric dual by constraint
generation:

  minimize sum_R |R| y_R
  subject to sum_K |K| d_K >= 1,
             d_K <= length_y(P) for every representative path P.

Shortest-path separation adds violated path signatures until closure.  The
resulting finite path set is then used for the matching symmetry-averaged primal.
All floating HiGHS outputs are rationally reconstructed and rechecked exactly:
commodity sums, edge-orbit capacities, dual normalization, every final shortest
path inequality, and equality of primal/dual objectives.
"""
from __future__ import annotations
import itertools,json,math
from collections import defaultdict,deque
from fractions import Fraction
from pathlib import Path
import networkx as nx
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4820_EXACT_OUTAGE_MULTICOMMODITY.json'
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle

def path_sig(path,er,r):
    z=[0]*r
    for u,v in zip(path,path[1:]):z[er[tuple(sorted((u,v)))]]+=1
    return tuple(z)

def solve_case(D,B,F,node_remove,expected):
    Gp=D['G'];res=D['residues'];phi=D['phiR'];ridx={r:i for i,r in enumerate(res)};invphi={v:k for k,v in phi.items()}
    def ar(i,g):return ridx[tuple(sorted(g[x] for x in res[i]))]
    def av(v,g):return phi[ar(invphi[v],g)]
    hot={tuple(sorted(e)) for e in B['hot']};cold={tuple(sorted(e)) for e in B['cold']};allE=hot|cold
    K5=B['K5'];owner=[]
    for T in B['projected']:
        h=[i for i,S in enumerate(K5) if set(T)<=S];assert len(h)==1;owner.append(h[0])
    fibers=[set(i for i,a in enumerate(owner) if a==f) for f in range(27)];assert {len(C) for C in fibers}=={10}
    def fp(g):return tuple(owner[av(min(fibers[f]),g)] for f in range(27))
    FF=set(F);H=[g for g in Gp if {fp(g)[f] for f in FF}==FF]
    rem=set().union(*(fibers[f] for f in FF)) if node_remove else set()
    V=sorted(set(range(270))-rem);E=set(allE)
    if node_remove:E={e for e in E if not (set(e)&rem)}
    else:E={e for e in E if not (e in hot and owner[e[0]] in FF)}
    acts=[tuple(av(i,g) for i in range(270)) for g in H]
    # edge and ordered-pair H-orbits
    unseen=set(E);EO=[]
    while unseen:
        u,v=next(iter(unseen));O={tuple(sorted((a[u],a[v]))) for a in acts};assert O<=E;EO.append(O);unseen-=O
    er={e:i for i,O in enumerate(EO) for e in O};r=len(EO)
    unseen={(u,v) for u in V for v in V if u!=v};PO=[]
    while unseen:
        s,t=next(iter(unseen));O={(a[s],a[t]) for a in acts};PO.append(O);unseen-=O
    reps=[next(iter(O)) for O in PO];K=len(PO)
    G=nx.Graph();G.add_nodes_from(V);G.add_edges_from(E)
    # initial one shortest path per pair orbit
    paths=[set() for _ in range(K)];bys=defaultdict(list)
    for k,(s,t) in enumerate(reps):bys[s].append((k,t))
    for s,kt in bys.items():
        P=nx.single_source_shortest_path(G,s)
        for k,t in kt:paths[k].add(path_sig(P[t],er,r))
    iterations=0
    while True:
        n=r+K;c=np.zeros(n);c[:r]=[len(O) for O in EO]
        Au=[];bu=[]
        row=np.zeros(n);row[r:]=[-len(O) for O in PO];Au.append(row);bu.append(-1.)
        for k,PS in enumerate(paths):
            for sg in PS:
                row=np.zeros(n);row[:r]=-np.array(sg,float);row[r+k]=1;Au.append(row);bu.append(0.)
        dual=linprog(c,A_ub=np.array(Au),b_ub=np.array(bu),bounds=[(0,None)]*n,method='highs');assert dual.success
        y=dual.x[:r];dd=dual.x[r:]
        for e in G.edges():G.edges[e]['weight']=y[er[tuple(sorted(e))]]
        adds=0
        for s,kt in bys.items():
            dist,P=nx.single_source_dijkstra(G,s,weight='weight')
            for k,t in kt:
                if dd[k]>dist[t]+1e-9:
                    sg=path_sig(P[t],er,r)
                    if sg not in paths[k]:paths[k].add(sg);adds+=1
        iterations+=1
        if not adds:break
        assert iterations<40
    # matching finite path primal
    plist=[list(P) for P in paths];off=[];tot=0
    for P in plist:off.append(tot);tot+=len(P)
    nv=tot+1;zidx=tot;cp=np.zeros(nv);cp[zidx]=1
    Aeq=np.zeros((K,nv));beq=np.ones(K)
    for k,P in enumerate(plist):Aeq[k,off[k]:off[k]+len(P)]=1
    Aup=np.zeros((r,nv))
    for rr,O in enumerate(EO):
        for k,P in enumerate(plist):
            coef=len(PO[k])/len(O)
            for j,sg in enumerate(P):Aup[rr,off[k]+j]=coef*sg[rr]
        Aup[rr,zidx]=-1
    primal=linprog(cp,A_ub=Aup,b_ub=np.zeros(r),A_eq=Aeq,b_eq=beq,bounds=[(0,None)]*nv,method='highs');assert primal.success
    # exact rational reconstruction/certificate
    den=10**9
    q=lambda x:Fraction(float(x)).limit_denominator(den)
    yr=[q(x) for x in dual.x[:r]];dr=[q(x) for x in dual.x[r:]];lam=q(dual.fun);zr=q(primal.fun);xr=[q(x) for x in primal.x[:-1]]
    assert lam==expected and zr==1/expected
    assert sum(len(EO[i])*yr[i] for i in range(r))==lam
    assert sum(len(PO[k])*dr[k] for k in range(K))==1
    # exact shortest-path separation using integer-scaled rational lengths
    L=1
    for x in yr:L=math.lcm(L,x.denominator)
    for e in G.edges():G.edges[e]['iw']=int(yr[er[tuple(sorted(e))]]*L)
    for s,kt in bys.items():
        dist=nx.single_source_dijkstra_path_length(G,s,weight='iw')
        for k,t in kt:assert dr[k]<=Fraction(dist[t],L)
    for k,P in enumerate(plist):assert sum(xr[off[k]+j] for j in range(len(P)))==1
    loads=[]
    for rr,O in enumerate(EO):
        z=Fraction(0)
        for k,P in enumerate(plist):
            coef=Fraction(len(PO[k]),len(O))
            for j,sg in enumerate(P):z+=coef*sg[rr]*xr[off[k]+j]
        loads.append(z)
    assert max(loads)<=zr and max(loads)==zr
    return {'failed_fibers':list(F),'node_removal':node_remove,'surviving_vertices':len(V),'surviving_edges':len(E),
      'failure_stabilizer_order':len(H),'edge_orbits':len(EO),'ordered_pair_orbits':len(PO),'path_constraints_at_closure':sum(map(len,paths)),
      'cutting_plane_iterations':iterations,'exact_lambda':str(lam),'exact_congestion':str(zr),'rational_primal_dual_certificate':True}

def main():
    D=build_all();B=build_bundle();K5=B['K5'];qG=nx.Graph();qG.add_nodes_from(range(27))
    for a,b in itertools.combinations(range(27),2):
        if K5[a]&K5[b]:qG.add_edge(a,b)
    adj=next(iter(qG.edges()));non=next((a,b) for a,b in itertools.combinations(range(27),2) if not qG.has_edge(a,b))
    specs=[
      ('one_hot',(0,),False,Fraction(67,5952)),
      ('two_hot_adjacent',adj,False,Fraction(665,59746)),
      ('two_hot_nonadjacent',non,False,Fraction(133,11946)),
      ('one_vertex_fiber_removed',(0,),True,Fraction(189,16538)),
      ('two_vertex_adjacent_removed',adj,True,Fraction(1767,153094)),
      ('two_vertex_nonadjacent_removed',non,True,Fraction(351,30670))]
    cases={name:solve_case(D,B,F,nr,ex) for name,F,nr,ex in specs}
    intact=Fraction(15,1318)
    out={'pass':4820,'demand_convention':'unit demand for every ordered distinct surviving vertex pair, unit surviving-edge capacities',
      'intact_reference':str(intact),'cases':cases,
      'theorem':'All six Pass4773 symmetry-breaking failure cases are now exact fractional multicommodity optima. Stabilizer orbit reduction plus shortest-path separation yields matching exact rational primal and metric-dual certificates in every case.',
      'boundary':'Exact fractional-flow values under the stated post-failure demand sets and unit capacities. No queueing, latency, integer unsplittable-flow or measured-hardware claim is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
