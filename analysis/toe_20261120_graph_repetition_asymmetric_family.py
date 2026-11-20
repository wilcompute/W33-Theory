#!/usr/bin/env python3
"""Graph-to-asymmetric-qutrit code: any connected simple graph of minimum degree >=3.

Uses the conventional two-factor ternary hypergraph-product construction;
mathematical code parameters are exact, physical performance is untested.
"""
from itertools import pairwise
import json
from pathlib import Path
import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix,eye,kron,hstack
from toe_20261120_mixed_levi_repetition_hgp import levi_graph,shortest_cycle,no_low_weight_kernel

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261120_graph_repetition_asymmetric_family.json"

def verify_graph(source,name):
    G=nx.convert_node_labels_to_integers(source,ordering="sorted")
    assert nx.is_connected(G) and not G.is_multigraph() and not nx.number_of_selfloops(G) and not list(nx.bridges(G))
    assert min(dict(G.degree()).values())>=3
    V=G.number_of_nodes()
    edges=sorted(tuple(sorted((u,v))) for u,v in G.edges())
    E=len(edges); ix={e:i for i,e in enumerate(edges)}
    incidence=np.zeros((V,E),dtype=np.int32)
    for j,(u,v) in enumerate(edges):
        incidence[u,j]=1;incidence[v,j]=-1
    A=csr_matrix(incidence[:-1])
    B=csr_matrix([[1,-1,0],[0,1,-1]],dtype=np.int32)
    I=lambda n:eye(n,format="csr",dtype=np.int32)
    HX=hstack((kron(A,I(3)),kron(I(V-1),B.T)),format="csr")
    HZ=hstack((kron(I(E),B),-kron(A.T,I(2))),format="csr")
    HX.eliminate_zeros();HZ.eliminate_zeros()
    N=3*E+2*(V-1)
    K=E-V+1
    assert HX.shape==((V-1)*3,N)
    assert HZ.shape==(E*2,N)
    assert all(x%3==0 for x in (HX@HZ.T).data)
    assert no_low_weight_kernel(HZ)
    cyc=shortest_cycle(G) if name=="W33_Levi" else None
    if cyc is None:
        for u,v in edges:
            G.remove_edge(u,v)
            path=nx.shortest_path(G,u,v)
            G.add_edge(u,v)
            if cyc is None or len(path)<len(cyc):cyc=path
    girth=len(cyc)
    chain=np.zeros(E,dtype=np.int32)
    for u,v in pairwise(cyc+[cyc[0]]):
        e=(min(u,v),max(u,v))
        chain[ix[e]]=1 if (u,v)==e else -1
    assert np.count_nonzero(chain)==girth and not np.any((A@chain)%3)
    ei=next(i for i,a in enumerate(chain) if a)
    logical_X=np.zeros(N,dtype=np.int32)
    logical_X[3*ei:3*ei+3]=1
    logical_Z=np.zeros(N,dtype=np.int32)
    logical_Z[:3*E:3]=chain
    assert not np.any((HZ@logical_X)%3) and not np.any((HX@logical_Z)%3)
    assert np.count_nonzero(logical_X)==3 and np.count_nonzero(logical_Z)==girth
    pairing=int(logical_X@logical_Z%3)
    assert pairing
    return {
      "graph":name,"vertices":V,"edges":E,"girth":girth,
      "parameters":{"n":N,"k":K,"dX":3,"dZ":girth,"d":3},
      "check_weights":{"HX":int(max(np.diff(HX.indptr))),"HZ":int(max(np.diff(HZ.indptr)))},
      "check_degrees":{"HX":int(max(np.diff(HX.tocsc().indptr))),"HZ":int(max(np.diff(HZ.tocsc().indptr)))},
      "proof_checks":{"commuting_stabilizers":True,"HX_rank":3*(V-1),"HZ_rank":2*E,
       "no_zero_or_projectively_equal_HZ_columns":True,
       "anticommuting_logical_pair":pairing}
    }

def run(write=True):
    cases={
      "cube_Q3":nx.hypercube_graph(3),
      "Petersen":nx.petersen_graph(),
      "Heawood":nx.heawood_graph(),
      "W33_Levi":levi_graph()
    }
    examples=[verify_graph(g,name) for name,g in cases.items()]
    got=[(e["parameters"]["n"],e["parameters"]["k"],e["parameters"]["dX"],e["parameters"]["dZ"]) for e in examples]
    assert got==[(50,5,3,4),(63,6,3,5),(89,8,3,6),(638,81,3,8)]
    result={
      "status":"PASS_GRAPH_MIXED_HGP_GENERALIZATION",
      "theorem":"For a connected bridgeless simple graph with minimum degree >=3, V vertices, E edges, and girth g, its reduced signed incidence matrix hypergraph-product with the length-three ternary repetition check yields [[3E+2(V-1),E-V+1,dX=3,dZ=g]]_3.",
      "proof":"As in the Levi case: rank(A)=V-1, rank(B)=2, CSS checks commute; projection of Z first block along repetition all-ones gives a graph cycle of weight>=g; zero projection implies Z stabilizer. All HZ columns are nonzero, pairwise nonproportional for a simple graph min degree>=3; a single cycle edge times (1,1,1) gives weight3 X logical paired with cycle Z logical.",
      "cubic_graph_family":"For V even, E=3V/2: n=13V/2-2, k=V/2+1, asymptotic rate 1/13, dX=3, dZ=g. Large-girth cubic graph families imply unbounded phase-error (Z) distance only; symmetric distance remains 3.",
      "examples":examples,
      "caveat":"Standard hypergraph-product mechanism, no new coding-theory general framework, no noisy threshold or local physical photonic implementation."
    }
    if write:OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    return result

if __name__=="__main__": print(json.dumps(run(),indent=2))
