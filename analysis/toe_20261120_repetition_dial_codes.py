#!/usr/bin/env python3
"""Ternary W(3,3) Levi x variable-length repetition HGP codes.

Exact asymmetry theorem: [[239L-79,81,dX=L,dZ=8]]_3, L >= 2.
This is a specialization of established hypergraph-product CSS theory.
"""
from pathlib import Path
import json
import numpy as np
from scipy.sparse import csr_matrix, eye, kron, hstack
from toe_20261120_mixed_levi_repetition_hgp import levi_graph, shortest_cycle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/toe_20261120_repetition_dial_codes.json"

def build(L):
    assert isinstance(L,int) and L>=2
    graph = levi_graph()
    edges = sorted((min(u,v), max(u,v)) for u,v in graph.edges())
    index = {e:i for i,e in enumerate(edges)}
    V,E = graph.number_of_nodes(), len(edges)
    assert (V,E)==(80,160)
    D=np.zeros((V,E),dtype=np.int16)
    for i,(u,v) in enumerate(edges):
        D[u,i]=1
        D[v,i]=-1
    A=csr_matrix(D[:-1])
    B=csr_matrix(np.eye(L-1,L,dtype=np.int16)
                 - np.eye(L-1,L,k=1,dtype=np.int16))
    I=lambda n: eye(n,format="csr",dtype=np.int16)
    HX=hstack((kron(A,I(L)),kron(I(V-1),B.T)),format="csr")
    HZ=hstack((kron(I(E),B),-kron(A.T,I(L-1))),format="csr")
    assert (HX.shape,HZ.shape)==(((V-1)*L,239*L-79),
                                  (E*(L-1),239*L-79))
    orth=(HX@HZ.T).tocsr()
    assert all(int(v)%3==0 for v in orth.data)
    c=np.zeros(E,dtype=np.int16)
    cyc=shortest_cycle(graph)
    for u,v in zip(cyc,cyc[1:]+cyc[:1]):
        pair=(min(u,v),max(u,v))
        c[index[pair]]=1 if (u,v)==pair else -1
    assert np.count_nonzero(c)==8 and np.all((A@c)%3==0)
    e0=int(np.flatnonzero(c)[0])
    x=np.zeros(HX.shape[1],dtype=np.int16)
    x[e0*L:(e0+1)*L]=1
    z=np.zeros(HX.shape[1],dtype=np.int16)
    z[:E*L:L]=c
    assert np.count_nonzero(x)==L and np.count_nonzero(z)==8
    assert not np.any((HZ@x)%3) and not np.any((HX@z)%3)
    pair=int(np.dot(x.astype(np.int32),z.astype(np.int32))%3)
    assert pair in (1,2)
    n=E*L+(V-1)*(L-1)
    k=E-(V-1)
    check={
        "L":L,"physical_qutrits":n,"logical_qutrits":k,
        "dX":L,"dZ":8,"distance":min(L,8),
        "HX_shape":list(HX.shape),"HZ_shape":list(HZ.shape),
        "rank_HX_by_full_row_rank":(V-1)*L,
        "rank_HZ_by_full_row_rank":E*(L-1),
        "nonzero_logical_XZ_pair":pair,
        "HX_HZT_zero_mod3":True,
        "maximum_X_check_weight":int(np.max(np.diff(HX.indptr))),
        "maximum_Z_check_weight":int(np.max(np.diff(HZ.indptr))),
        "maximum_X_qudit_check_degree":int(np.max(np.diff(HX.tocsc().indptr))),
        "maximum_Z_qudit_check_degree":int(np.max(np.diff(HZ.tocsc().indptr))),
    }
    assert check["physical_qutrits"]-check["rank_HX_by_full_row_rank"]-check["rank_HZ_by_full_row_rank"]==81
    return check

def run(write=True):
    samples=[build(L) for L in (2,3,4,5,8,11)]
    assert [(v["physical_qutrits"],v["dX"],v["dZ"]) for v in samples] == [
        (399,2,8),(638,3,8),(877,4,8),(1116,5,8),(1833,8,8),(2550,11,8)]
    result={
        "status":"PASS_STANDARD_HGP_VARIABLE_REPETITION_DIAL",
        "source_prior_art":"analysis/toe_20261120_mixed_levi_repetition_hgp.py",
        "theorem":"For every L>=2: CSS [[239L-79,81,dX=L,dZ=8]]_3 using reduced 79x160 oriented Levi incidence A and (L-1)xL signed repetition check B.",
        "dX_proof":"HZ x=0 forces successive edge-column slices of x_first to differ by A^T rowspace vectors. All L slices have a common class in F3^E/im A^T. If class=0, x is HX stabilizer (A^T injective); otherwise each of L slices is nonzero, so X logical weight>=L. One nonbridge edge times all-ones length L is a paired weight-L X logical.",
        "dZ_proof":"For z in ker HX sum z_first over its L repetition columns; B^T sums to zero, giving a graph cycle s in ker A. If s=0, z is an HZ stabilizer because im B^T=zero-sum vectors and B^T injective. Otherwise graph girth 8 forces weight(z)>=8. A native Levi octagon in one repetition column is a paired weight-eight Z logical.",
        "symmetric_distance_caution":"L=8 balances dX and dZ at 8, but requires 1833 independently addressable physical qutrits. This is not a single-photon code or a threshold result.",
        "samples":samples}
    if write: OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    return result

if __name__=="__main__":print(json.dumps(run(),indent=2))
