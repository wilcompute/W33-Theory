#!/usr/bin/env python3
"""ADE-to-Q4 router lift from the SU2 level-12 D8 invariant.

This continues the D8 bridge and uses the single-photon/Q4-router hint from the
six TeX sources.  The key observation is that the D8 modular invariant matrix M
has Frobenius square 16, exactly the vertex count of the Q4 router.  Taking the
rank of M as the hypercube dimension gives all Q4 router counts exactly.

The verifier keeps the statement finite and operational:

  support(M) = 13
  diagonal support = 7
  off-diagonal support = 6
  sum(M) = 14
  sum(M^2 entrywise) = ||M||_F^2 = 16
  rank(M) = 4

Then Q_rank(M) has

  vertices 16, edges 32, square faces 24, face-edge incidences 96.

Finally, the existing minimal logical pairing count factors as

  |W(E6)| = 51840 = 40 * 16 * 81 = v * |V(Q4)| * H1.

So the D8 invariant supplies the binary router packet used by the single-photon
self-entanglement layer, while W33 supplies the 40 anchors and H1 supplies the
protected qutrit phase frame.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

q=3
k=12
kp2=14
Phi3=13
Phi6=7
g2=6
chi=4
v=40
H1=81
WE6=51840
mu=28
E2=16


def d8_modular_invariant()->np.ndarray:
    M=np.zeros((k+1,k+1),dtype=int)
    for j in (0,2,4):
        jp=k-j
        for a in (j,jp):
            for b in (j,jp):
                M[a,b]=1
    M[k//2,k//2]=2
    return M


def qn_graph(n:int)->np.ndarray:
    verts=list(itertools.product((0,1),repeat=n))
    idx={v:i for i,v in enumerate(verts)}
    A=np.zeros((len(verts),len(verts)),dtype=int)
    for a,u in enumerate(verts):
        for bit in range(n):
            w=list(u); w[bit]^=1; w=tuple(w)
            b=idx[w]
            A[a,b]=1
    return A


def hypercube_square_faces(n:int)->int:
    return (2**(n-2))*(n*(n-1)//2)


def build_payload()->dict:
    M=d8_modular_invariant()
    support=(M!=0)
    diag=np.eye(k+1,dtype=bool)
    support_count=int(support.sum())
    diag_support=int((support & diag).sum())
    offdiag_support=support_count-diag_support
    entry_sum=int(M.sum())
    frob_sq=int(np.sum(M*M))
    rank=int(np.linalg.matrix_rank(M,tol=1e-10))
    kernel=(k+1)-rank
    trace=int(np.trace(M))
    M2=M@M
    M2_entry_sum=int(M2.sum())

    Q=qn_graph(rank)
    q_vertices=int(Q.shape[0])
    q_degree=int(Q.sum(axis=1)[0])
    q_edges=int(Q.sum()//2)
    q_faces=hypercube_square_faces(rank)
    q_face_edge_inc=4*q_faces
    reye_points=q_faces//2
    reye_lines=q_edges//2
    reye_inc=q_face_edge_inc//2
    tomotope_flags=2*q_face_edge_inc
    per_anchor_packet=q_vertices*H1

    ids={
        "support_is_Phi3": support_count==Phi3,
        "diagonal_support_is_Phi6": diag_support==Phi6,
        "offdiag_support_is_g2": offdiag_support==g2,
        "entry_sum_is_k_plus_2": entry_sum==kp2,
        "frob_square_is_E2_and_Q4_vertices": frob_sq==E2==16,
        "rank_is_chi_and_Q_dimension": rank==chi==4,
        "kernel_is_q_squared": kernel==q*q,
        "trace_is_q_squared_minus_1": trace==q*q-1,
        "M2_is_2M": bool(np.array_equal(M2,2*M)),
        "M2_entry_sum_is_mu": M2_entry_sum==mu,
        "Q_vertices_from_frob": q_vertices==frob_sq,
        "Q_degree_from_rank": q_degree==rank,
        "Q_edges": q_edges==32,
        "Q_square_faces": q_faces==24,
        "Q_face_edge_incidence": q_face_edge_inc==96,
        "Reye_quotient_counts": reye_points==12 and reye_lines==16 and reye_inc==48,
        "tomotope_flags": tomotope_flags==192,
        "WE6_factorization": WE6==v*q_vertices*H1,
        "per_anchor_packet_1296": per_anchor_packet==1296,
    }

    return {
        "theorem":"ADE_Q4_router_lift",
        "D8_invariant_support_calculus":{
            "matrix_size":k+1,
            "support_count":support_count,
            "diagonal_support":diag_support,
            "offdiagonal_support":offdiag_support,
            "entry_sum":entry_sum,
            "frob_square":frob_sq,
            "rank":rank,
            "kernel_dimension":kernel,
            "trace":trace,
            "M2_entry_sum":M2_entry_sum,
            "minimal_polynomial":"M^2=2M"
        },
        "Q4_router_lift":{
            "dimension_from_rank_M":rank,
            "vertices_from_frob_square_M":q_vertices,
            "degree":q_degree,
            "edges":q_edges,
            "square_faces":q_faces,
            "face_edge_incidences":q_face_edge_inc,
            "reye_quotient":"12 points, 16 lines, 48 incidences",
            "tomotope_flags":tomotope_flags
        },
        "minimal_logical_factorization":{
            "WE6_nonzero_vector_pairings":WE6,
            "factorization":"51840 = 40 * 16 * 81",
            "W33_anchors":v,
            "router_vertices":q_vertices,
            "H1_phase_rank":H1,
            "per_anchor_packet":per_anchor_packet
        },
        "identities":ids,
        "all_identities_hold":bool(all(ids.values()))
    }


def main()->None:
    payload=build_payload()
    out=Path("data/w33_ade_q4_router_lift.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps(payload,indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
