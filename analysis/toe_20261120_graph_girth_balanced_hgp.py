#!/usr/bin/env python3
"""Graph-girth/repetition-length balanced ternary HGP design.

For any finite connected simple graph G with at least one cycle:
  [[L*E + (L-1)*(V-1), E-V+1, dX=L, dZ=girth(G)]]_3.
Standard hypergraph-product construction; not a new QEC paradigm.
"""
import json
from pathlib import Path
import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix,eye,kron,hstack
from toe_20261120_mixed_levi_repetition_hgp import levi_graph

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261120_graph_girth_balanced_hgp.json"

def minimal_cycle(graph):
    G=graph.copy()
    best=None
    for u,v in list(G.edges()):
        G.remove_edge(u,v)
        if nx.has_path(G,u,v):
            path=nx.shortest_path(G,u,v)
            if best is None or len(path)<len(best):
                best=path
        G.add_edge(u,v)
    assert best is not None
    return best

def verify(graph,name,L=None):
    G=nx.convert_node_labels_to_integers(graph)
    assert nx.is_connected(G) and not G.is_multigraph() and nx.number_of_selfloops(G)==0
    cyc=minimal_cycle(G)
    if L is None: L=len(cyc)
    assert isinstance(L,int) and L>=2
    V=G.number_of_nodes()
    edges=sorted((min(u,v),max(u,v)) for u,v in G.edges())
    E=len(edges);idx={e:i for i,e in enumerate(edges)}
    a=np.zeros((V-1,E),dtype=np.int16)
    for j,(u,v) in enumerate(edges):
        if u<V-1:a[u,j]=1
        if v<V-1:a[v,j]=-1
    A=csr_matrix(a)
    b=np.eye(L-1,L,dtype=np.int16)-np.eye(L-1,L,k=1,dtype=np.int16)
    B=csr_matrix(b)
    I=lambda n:eye(n,dtype=np.int16,format="csr")
    HX=hstack((kron(A,I(L)),kron(I(V-1),B.T)),format="csr")
    HZ=hstack((kron(I(E),B),-kron(A.T,I(L-1))),format="csr")
    HX.eliminate_zeros(); HZ.eliminate_zeros()
    assert not np.any((HX@HZ.T).data%3)
    c=np.zeros(E,dtype=np.int16)
    for u,v in zip(cyc,cyc[1:]+cyc[:1]):
        pair=(min(u,v),max(u,v))
        c[idx[pair]]=1 if (u,v)==pair else -1
    assert not np.any((A@c)%3)
    e0=int(np.flatnonzero(c)[0])
    x=np.zeros(HX.shape[1],dtype=np.int16)
    x[e0*L:(e0+1)*L]=1
    z=np.zeros(HX.shape[1],dtype=np.int16)
    z[:E*L:L]=c
    assert np.count_nonzero(x)==L and np.count_nonzero(z)==len(cyc)
    assert not np.any((HZ@x)%3) and not np.any((HX@z)%3)
    assert int(x.astype(np.int32)@z.astype(np.int32)%3) in (1,2)
    n=L*E+(L-1)*(V-1);k=E-V+1
    assert n==HX.shape[1] and k==n-HX.shape[0]-HZ.shape[0]
    return {
      "name":name,"V":V,"E":E,"L":L,"girth":len(cyc),
      "N":n,"K":k,"dX":L,"dZ":len(cyc),"distance":min(L,len(cyc)),
      "rank_HX":HX.shape[0],"rank_HZ":HZ.shape[0],
      "CSS_commutator_mod3_zero":True,
      "logical_pair_nonzero":True,
      "max_HX_check_weight":int(max(np.diff(HX.indptr))),
      "max_HZ_check_weight":int(max(np.diff(HZ.indptr)))
    }

def run(write=True):
    pendant=nx.cycle_graph(4);pendant.add_edge(0,4)
    examples=[
      verify(nx.cycle_graph(4),"C4"),
      verify(pendant,"C4_with_bridge"),
      verify(nx.hypercube_graph(3),"Q3"),
      verify(nx.petersen_graph(),"Petersen"),
      verify(nx.heawood_graph(),"Heawood"),
      verify(levi_graph(),"W33_Levi")
    ]
    got=[(v["N"],v["K"],v["dX"],v["dZ"]) for v in examples]
    want=[(25,1,4,4),(32,1,4,4),(69,5,4,4),
          (111,6,5,5),(191,8,6,6),(1833,81,8,8)]
    assert got==want,(got,want)
    result={
      "status":"PASS_CONNECTED_GRAPH_REPETITION_BALANCED_CSS",
      "theorem":"Every finite connected simple graph G with a cycle and girth g, with L>=2, yields the ternary HGP code [[LE+(L-1)(V-1), E-V+1, dX=L, dZ=g]]_3.",
      "proof":"The HZ equation identifies each repetition slice modulo the image of the reduced oriented incidence transpose: a nontrivial X logical has a nonzero coset in every one of L slices; a nonbridge edge times the all-ones repetition vector witnesses weight L. Summing the L first-block coordinates of a Z logical gives a graph cycle; zero sum makes the vector an HZ stabilizer, while a nonzero cycle has weight at least girth and an oriented shortest cycle witnesses equality.",
      "cubic_growth":"For cubic V-vertex graphs, E=3V/2. With L=girth(G), N=(5V/2-1)g-V+1, K=V/2+1, symmetric d=g. High-girth bounded-degree families give inverse-logarithmic rate and logarithmic distance, not constant rate or polynomial distance. Check weights and qudit degrees remain bounded.",
      "examples":examples,
      "boundary":"Existing HGP mathematics; no noisy fault-tolerant threshold, optical realization, Einstein limit or new physics claim."
    }
    if write:OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    return result

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
