#!/usr/bin/env python3
"""Pass7376-7384 outside-box: repair the new E8 spectral descent and identify its local graphs.

A parallel commit correctly computes the nested local spectra
240 -> 56 -> 27 -> 16 -> 10 but then overreads 27+6=33 as a W33 vertex count.
This verifier keeps the spectral mathematics and closes the interpretation:

* the Coxeter/Eisenstein fibration has 40 six-root fibres, exactly as Pass1021;
* every six-root fibre is an A2 root hexagon (rank two, six roots);
* the 16-vertex local graph is the complement of the Clebsch graph;
* the 10-vertex next local graph is the complement of the Petersen graph;
* therefore 33 is not a W(3,3) vertex count. The W33 base remains 40 points.

It also exposes the representation-theoretic 27=1+16+10 split visible at the
Schlaefli level, matching the familiar E6 -> Spin(10) branching of the 27.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
import networkx as nx
import w33_pass7163_7170_e8_hexagonal_lift as e8

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7376_7384_E8_LOCAL_CHAIN_FIREWALL.json'

def spectrum(G):
    A=nx.to_numpy_array(G,nodelist=sorted(G.nodes()))
    return Counter(map(int,np.rint(np.linalg.eigvalsh(A))))

def clebsch():
    # Fold the 5-cube by antipodes: the standard Clebsch graph.
    Q=nx.hypercube_graph(5);rep={}
    for v in Q:
        w=tuple(1-b for b in v);rep[v]=min(v,w)
    reps=sorted(set(rep.values()));idx={r:i for i,r in enumerate(reps)}
    G=nx.Graph();G.add_nodes_from(range(16))
    for a,b in Q.edges():
        u,v=idx[rep[a]],idx[rep[b]]
        if u!=v:G.add_edge(u,v)
    assert set(dict(G.degree()).values())=={5}
    return G

def main():
    R,fib,phase,radj,base_adj,zero,twelve,diff=e8.e8_fibers()
    assert len(R)==240 and len(fib)==40 and set(map(len,fib))=={6}
    # Each Eisenstein fibre is literally an A2 root system in doubled coordinates.
    fibre_profiles=[]
    for F in fib:
        V=np.asarray([R[i] for i in F],dtype=int)
        assert np.linalg.matrix_rank(V.astype(float))==2
        ip=Counter(e8.dot(R[i],R[j]) for i,j in itertools.combinations(F,2))
        assert ip==Counter({4:6,-4:6,-8:3})
        fibre_profiles.append(ip)
    # The quotient is the actual W33 point graph.
    W=nx.Graph();W.add_nodes_from(range(40))
    for i in range(40):
        for j in base_adj[i]:
            if i<j:W.add_edge(i,j)
    assert set(dict(W.degree()).values())=={12}
    for i,j in itertools.combinations(range(40),2):
        c=len(set(W.neighbors(i))&set(W.neighbors(j)))
        assert c==(2 if W.has_edge(i,j) else 4)

    # E8 +1 root graph and deterministic nested local chain.
    G=nx.Graph();G.add_nodes_from(range(240))
    for i,j in itertools.combinations(range(240),2):
        if e8.dot(R[i],R[j])==4:G.add_edge(i,j)
    chain=[G]
    for _ in range(4):
        H=chain[-1];v=sorted(H.nodes())[0]
        chain.append(H.subgraph(list(H.neighbors(v))).copy())
    expected=[
      (240,56,{56:1,28:8,8:35,-2:112,-4:84}),
      (56,27,{27:1,9:7,-1:27,-3:21}),
      (27,16,{16:1,4:6,-2:20}),
      (16,10,{10:1,2:5,-2:10}),
      (10,6,{6:1,1:4,-2:5}),
    ]
    rows=[]
    for H,(n,k,sp) in zip(chain,expected):
        assert H.number_of_nodes()==n and set(dict(H.degree()).values())=={k}
        assert spectrum(H)==Counter(sp)
        rows.append({'vertices':n,'degree':k,'spectrum':sp})
    assert nx.is_isomorphic(chain[3],nx.complement(clebsch()))
    assert nx.is_isomorphic(chain[4],nx.complement(nx.petersen_graph()))

    # At the Schlaefli 27-level, choosing one vertex partitions the set as
    # 1 + 16 neighbors + 10 nonneighbors.
    Sch=chain[2];v=sorted(Sch.nodes())[0]
    assert 1+Sch.degree(v)+(Sch.number_of_nodes()-1-Sch.degree(v))==27
    assert (Sch.degree(v),Sch.number_of_nodes()-1-Sch.degree(v))==(16,10)

    out={'schema':'w33.pass7376_7384.e8_local_chain_firewall.v1','status':'PASS',
      'eisenstein_fibration':{'roots':240,'fibres':40,'fibre_size':6,'each_fibre':'A2 root hexagon','base':'W(3,3) point graph SRG(40,12,2,4)'},
      'local_chain':rows,
      'graph_identifications':{'16_vertex':'complement Clebsch','10_vertex':'complement Petersen'},
      'E6_branching_shadow':'Schlaefli 27 = 1 chosen vertex + 16 neighbors + 10 nonneighbors, mirroring 27 -> 1+16+10 under E6 -> Spin(10)',
      'parallel_claim_firewall':'27+6=33 is a true arithmetic sum of spectral multiplicities, not the W33 vertex count. The actual E8 Eisenstein quotient has 40 fibres/points.',
      'boundary':'Exact graph/root-system statements. The representation-branching comparison is structural context, not a particle-physics identification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','fibres':'40 A2','local':'Schlaefli->coClebsch->coPetersen','W33':40}))
if __name__=='__main__':main()
