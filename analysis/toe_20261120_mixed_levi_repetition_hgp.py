#!/usr/bin/env python3
"""Explicit ternary CSS hypergraph product: W(3,3) Levi graph x length-three repetition.
Prior art: analysis/w33_20261009_toe28_hypergraph_product_rate_distance.py.
An asymmetric finite quantum code, NOT a single-photon implementation or physical TOE.
"""
from itertools import product
from pathlib import Path
import json
import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix,eye,kron,hstack

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261120_mixed_levi_repetition_hgp.json"

def normalize(v):
    v=tuple(int(z)%3 for z in v)
    first=next(a for a in v if a)
    scalar=1 if first==1 else 2
    return tuple((scalar*a)%3 for a in v)

def symplectic(x,y):
    return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3

def levi_graph():
    pts=sorted({normalize(v) for v in product(range(3),repeat=4) if any(v)})
    assert len(pts)==40
    ids={p:i for i,p in enumerate(pts)}
    lines=set()
    for i,x in enumerate(pts):
        for y in pts[i+1:]:
            if symplectic(x,y): continue
            line=frozenset(ids[normalize([(a*x[k]+b*y[k])%3 for k in range(4)])]
                            for a,b in product(range(3),repeat=2) if (a or b))
            assert len(line)==4
            lines.add(line)
    lines=sorted(tuple(sorted(line)) for line in lines)
    assert len(lines)==40
    g=nx.Graph()
    g.add_nodes_from(range(80))
    g.add_edges_from((p,40+j) for j,L in enumerate(lines) for p in L)
    assert nx.is_connected(g) and len(g.edges())==160
    assert set(dict(g.degree()).values())=={4}
    return g

def shortest_cycle(g):
    best=None
    for a,b in sorted(g.edges()):
        g.remove_edge(a,b)
        p=nx.shortest_path(g,a,b)
        g.add_edge(a,b)
        if best is None or len(p)<len(best): best=p
    assert len(best)==8
    return best

def no_low_weight_kernel(H):
    """No zero columns and no projectively equal columns over F3 -> min ker weight>=3."""
    C=H.tocsc()
    seen=set()
    for j in range(C.shape[1]):
        start,end=C.indptr[j:j+2]
        inds=C.indices[start:end]
        vals=C.data[start:end]%3
        if len(inds)==0:return False
        v=(vals*(1 if vals[0]==1 else 2))%3
        key=(tuple(int(x) for x in inds),tuple(int(x) for x in v))
        if key in seen:return False
        seen.add(key)
    return True

def run(write=True):
    graph=levi_graph()
    edges=sorted((min(u,v),max(u,v)) for u,v in graph.edges())
    ei={e:i for i,e in enumerate(edges)}
    D=np.zeros((80,160),dtype=np.int32)
    for i,(u,v) in enumerate(edges):
        D[u,i]=1;D[v,i]=-1
    A=csr_matrix(D[:-1])
    B=csr_matrix([[1,-1,0],[0,1,-1]],dtype=np.int32)
    m,n=A.shape
    I=lambda k:eye(k,dtype=np.int32,format="csr")
    HX=hstack([kron(A,I(3)),kron(I(m),B.T)],format="csr")
    HZ=hstack([kron(I(n),B),-kron(A.T,I(2))],format="csr")
    HX.eliminate_zeros();HZ.eliminate_zeros()
    overlap=(HX@HZ.T).tocsr()
    assert all(int(x)%3==0 for x in overlap.data)
    assert HX.shape==(237,638) and HZ.shape==(320,638)
    assert no_low_weight_kernel(HZ)
    cyc=shortest_cycle(graph)
    c=np.zeros(n,dtype=np.int32)
    for u,v in zip(cyc,cyc[1:]+cyc[:1]):
        edge=(min(u,v),max(u,v))
        c[ei[edge]]=1 if (u,v)==edge else -1
    assert np.all((A@c)%3==0) and np.count_nonzero(c)==8
    index=next(i for i,a in enumerate(c) if a)
    x=np.zeros(638,dtype=np.int32);x[3*index:3*index+3]=1
    z=np.zeros(638,dtype=np.int32);z[:480:3]=c
    assert np.all((HZ@x)%3==0) and np.count_nonzero(x)==3
    assert np.all((HX@z)%3==0) and np.count_nonzero(z)==8
    pairing=int(x@z%3)
    assert pairing!=0
    result={
      "status":"PASS_EXACT_ASYMMETRIC_TERNARY_CSS",
      "provenance":"Standard hypergraph product, mixed Levi and repetition factors",
      "base":{"vertices":80,"edges":160,"girth":8,"incidence_shape":[79,160],"repetition_shape":[2,3]},
      "CSS":{"physical_qutrits":638,"encoded_qutrits":81,"dX":3,"dZ":8,"HX_shape":[237,638],"HZ_shape":[320,638],"HX_rank":237,"HZ_rank":320,
        "max_X_check_weight":int(max(np.diff(HX.indptr))),
        "max_Z_check_weight":int(max(np.diff(HZ.indptr))),
        "max_X_qudit_degree":int(max(np.diff(HX.tocsc().indptr))),
        "max_Z_qudit_degree":int(max(np.diff(HZ.tocsc().indptr)))},
      "proof":{"CSS_orthogonality":True,"no_weight1_2_X_kernel":True,
        "X_logical_weight3":True,"Z_logical_weight8":True,"XZ_pairing_mod3":pairing,
        "dZ_lower":"For z in ker HX, sum the first-block triples: s in ker A. If s=0, z is an HZ-row stabilizer by rank(B)=2. Nontrivial s has weight >= girth(G)=8.",
        "dX_lower":"All HZ columns are nonzero and pairwise nonproportional over F3, excluding weight one and two X logicals."},
      "limitations":"638 distinct qutrit sites. No threshold, fault-tolerant syndrome extraction, photon realization, or derivation of spacetime/SM dynamics."
    }
    if write:
        OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    return result

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
