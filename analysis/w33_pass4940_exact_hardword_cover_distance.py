#!/usr/bin/env python3
"""Pass4940 — exact distance of the Pass4859 covering-radius hard word.

Pass4859 used an exact spectral certificate to prove d(x,K)>=124 for a 360-bit
received word x, together with an automorphism g satisfying g(x)=x+sigma so
its distances to the ordinary and E6-switched cut classes are equal.  Here the
remaining cut-class minimization is solved exactly as a 36-Boolean CP-SAT
problem.  OPTIMAL is required; FEASIBLE is never promoted to a certificate.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np,networkx as nx
from ortools.sat.python import cp_model
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4940_EXACT_HARDWORD_COVER_DISTANCE.json'
WITNESS_HEX='4743dfaba7bb36874b9fcb5de87ed19c21ff7927d7754391d7d5d134b3bb04eefeccacde1ec769b98b7dffcf8'
WITNESS_AUT=(23,31,3,25,18,11,30,6,24,32,10,19,26,17,12,5,13,28,4,15,33,2,8,0,35,21,29,27,16,14,34,20,9,1,7,22)

def Q(x):
    b=[(x>>i)&1 for i in range(6)];a,c,d,e,f,g=b;return (a*c+d*e+f+f*g+g)&1

def main()->int:
    qp=[x for x in range(1,64) if Q(x)==0]
    P=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    lines=[tuple(i for i,T in enumerate(P) if x in T) for x in qp]
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if set(lines[i])&set(lines[j]):G.add_edge(i,j)
    C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G)) if len(c)==6]
    DS=set()
    for A,B in itertools.combinations(C6,2):
        if A&B:continue
        H=G.subgraph(A|B)
        if H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):DS.add(frozenset(A|B))
    DS=sorted(DS,key=lambda S:tuple(sorted(S)));assert len(DS)==36
    H=nx.Graph();H.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H.add_edge(i,j)
    E=sorted(tuple(sorted(e)) for e in H.edges());ei={e:i for i,e in enumerate(E)};assert len(E)==360
    xmask=int(WITNESS_HEX,16);x=[(xmask>>i)&1 for i in range(360)]
    g=WITNESS_AUT
    # Reconstruct the intrinsic E6 signing exactly as in Pass4859 only to cross-check the twist relation.
    C=np.eye(6,dtype=int)*2
    for a,b in ((0,1),(1,2),(2,3),(3,4),(2,5)):C[a,b]=C[b,a]=-1
    def ref(v,i):
        v=np.array(v,dtype=int);m=int(v@C[:,i]);w=v.copy();w[i]-=m;return tuple(map(int,w))
    roots={(1,0,0,0,0,0)};D=list(roots)
    while D:
        v=D.pop()
        for i in range(6):
            w=ref(v,i)
            if w not in roots:roots.add(w);D.append(w)
    pos=sorted(v for v in roots if all(z>=0 for z in v));assert len(pos)==36
    ER=nx.Graph();ER.add_nodes_from(range(36));ip={}
    for i,j in itertools.combinations(range(36),2):
        z=int(np.array(pos[i])@C@np.array(pos[j]));ip[(i,j)]=z
        if abs(z)==1:ER.add_edge(i,j)
    iso=next(nx.algorithms.isomorphism.GraphMatcher(H,ER).isomorphisms_iter())
    sigma=[0]*360
    for e,(a,b) in enumerate(E):
        i,j=sorted((iso[a],iso[b]));sigma[e]=int(ip[(i,j)]<0)
    ep=[ei[tuple(sorted((g[a],g[b])))] for a,b in E];gx=[0]*360
    for i,j in enumerate(ep):gx[j]=x[i]
    assert gx==[a^b for a,b in zip(x,sigma)]

    model=cp_model.CpModel();y=[model.NewBoolVar(f'y{i}') for i in range(36)];z=[]
    model.Add(y[0]==0) # quotient the cut/complement symmetry
    terms=[]
    for e,(u,v) in enumerate(E):
        q=model.NewBoolVar(f'z{e}');z.append(q)
        # y_u xor y_v xor not(q) = 1  <=>  q = y_u xor y_v
        model.AddBoolXOr([y[u],y[v],q.Not()])
        terms.append(q if x[e]==0 else 1-q)
    model.Minimize(sum(terms))
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=8;solver.parameters.max_time_in_seconds=1800.0
    status=solver.Solve(model);assert status==cp_model.OPTIMAL,solver.StatusName(status)
    assignment=[solver.Value(v) for v in y]
    cut=[assignment[u]^assignment[v] for u,v in E]
    distance=sum(a^b for a,b in zip(x,cut));assert distance==round(solver.ObjectiveValue())
    # The twist automorphism makes d(x,Cut)=d(x,sigma+Cut), so this is d(x,K).
    out={'pass':4940,'code':'K=[360,36,20]_2','witness_hex':WITNESS_HEX,
      'cp_sat':{'status':'OPTIMAL','Boolean_vertex_variables':36,'edge_parities':360,'symmetry_fix':'y0=0',
        'objective_distance':distance,'best_bound':round(solver.BestObjectiveBound()),'wall_time_seconds':solver.WallTime()},
      'exact_cut_representative_vertices':[i for i,b in enumerate(assignment) if b],
      'twist_cross_certificate':{'g_x_equals_x_plus_sigma':True,'therefore_two_switching_class_distances_equal':True},
      'covering_radius_update':{'certified_lower_bound':distance,'previous_lower_bound':124,'upper_bound':179,'exact_radius_closed':distance==179},
      'theorem':f'The Pass4859 hard received word has exact distance {distance} from the ordinary cut class by an OPTIMAL CP-SAT certificate. Its certified twist automorphism sends x to x+sigma, so the switched class has the same distance. Hence d(x,K)={distance} and the covering radius lower bound rises from 124 to {distance}.',
      'boundary':'This certifies one hard coset exactly. Unless the objective reaches the independent universal upper bound 179, it does not by itself close the global covering radius.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
