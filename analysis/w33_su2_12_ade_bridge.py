#!/usr/bin/env python3
"""ADE bridge for the SU(2)_12 even-sector projector.

For SU(2) level 12, the D-series ADE modular invariant is the D8 case.
The full 13-label invariant matrix M restricts on the seven even labels to
I+R, where R reverses 0,2,4,6,8,10,12. The previous H7 audit found
H H^T=(I+R)/2, so the ADE invariant is exactly twice that projector.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
import numpy as np

q=3
k=12
kp2=14
Phi6=7
chi=4
v=40
mu=v-k
E2=16
dX=3
dZ=4
H1=81


def su2_s(level:int=k)->np.ndarray:
    n=level+1
    den=level+2
    return np.array([[math.sqrt(2/den)*math.sin(math.pi*(a+1)*(b+1)/den) for b in range(n)] for a in range(n)],float)


def reversal(n:int=Phi6)->np.ndarray:
    R=np.zeros((n,n),float)
    for i in range(n):
        R[i,n-1-i]=1.0
    return R


def ade_matrix()->np.ndarray:
    M=np.zeros((k+1,k+1),int)
    for j in (0,2,4):
        jp=k-j
        for a in (j,jp):
            for b in (j,jp):
                M[a,b]=1
    M[k//2,k//2]=2
    return M


def dynkin_adjacency()->np.ndarray:
    n=8
    A=np.zeros((n,n),int)
    for i in range(n-3):
        A[i,i+1]=A[i+1,i]=1
    A[n-3,n-2]=A[n-2,n-3]=1
    A[n-3,n-1]=A[n-1,n-3]=1
    return A


def build_payload()->dict:
    S=su2_s()
    even=list(range(0,k+1,2))
    H=S[np.ix_(even,even)]
    R=reversal()
    M=ade_matrix()
    Me=M[np.ix_(even,even)].astype(float)
    A=dynkin_adjacency()
    deg=A.sum(axis=1).astype(int)
    h=np.array([j*(j+2)/(4*kp2) for j in range(k+1)],float)
    T=np.diag(np.exp(2j*math.pi*h))
    exponents=[1,3,5,7,7,9,11,13]
    expected=sorted([2*math.cos(math.pi*m/kp2) for m in exponents])
    actual=sorted(np.linalg.eigvalsh(A).tolist())
    ids={
        "level_12_is_D8_ADE_case": k==4*q and 2*q+2==8,
        "coxeter_equals_k_plus_2": kp2==14,
        "Me_equals_2HHt": bool(np.allclose(Me,2*(H@H.T),atol=1e-12)),
        "Me_equals_I_plus_R": bool(np.allclose(Me,np.eye(Phi6)+R,atol=1e-12)),
        "M2_equals_2M": bool(np.array_equal(M@M,2*M)),
        "M_commutes_with_S": float(np.max(np.abs(M@S-S@M)))<1e-12,
        "M_commutes_with_T": float(np.max(np.abs(M@T-T@M)))<1e-12,
        "M_rank_is_dZ": int(np.linalg.matrix_rank(M,tol=1e-10))==dZ,
        "M_trace_is_8": int(np.trace(M))==8,
        "M_entry_sum_is_14": int(M.sum())==kp2,
        "M_frobenius_square_is_16": int(np.sum(M*M))==E2,
        "graph_vertices_equal_trace": A.shape[0]==int(np.trace(M))==8,
        "graph_edges_equal_Phi6": int(A.sum()//2)==Phi6,
        "graph_degree_sum_equals_14": int(deg.sum())==kp2,
        "graph_degree_square_sum_equals_mu": int(np.sum(deg*deg))==mu,
        "graph_spectrum_matches_exponents": bool(np.allclose(actual,expected,atol=1e-12)),
        "distance_split": dX+dZ==Phi6 and dX*dZ==k,
        "H1_equals_q4": H1==q**4,
    }
    return {
        "theorem":"SU2_12_D8_ADE_bridge",
        "constants":{"q":q,"k":k,"k_plus_2":kp2,"Phi6":Phi6,"chi":chi,"v":v,"mu":mu,"E2":E2,"dX":dX,"dZ":dZ,"H1":H1},
        "modular_invariant":{"formula":"|chi0+chi12|^2 + |chi2+chi10|^2 + |chi4+chi8|^2 + 2|chi6|^2","rank":int(np.linalg.matrix_rank(M,tol=1e-10)),"spectrum":{"2":4,"0":9},"trace":int(np.trace(M)),"entry_sum":int(M.sum()),"frobenius_square_sum":int(np.sum(M*M)),"identity":"M^2=2M; M_even=2HHt=I+R"},
        "H7_bridge":{"even_labels":even,"H_rank":int(np.linalg.matrix_rank(H,tol=1e-10)),"H_nullity":Phi6-int(np.linalg.matrix_rank(H,tol=1e-10)),"identity":"HHt=(I+R)/2=M_even/2"},
        "dynkin_graph":{"vertices":int(A.shape[0]),"edges":int(A.sum()//2),"degree_sequence":deg.tolist(),"degree_sum":int(deg.sum()),"degree_square_sum":int(np.sum(deg*deg)),"coxeter_number":kp2,"exponents":exponents,"charpoly":"x^2*(x^6-7*x^4+14*x^2-7)","spectrum_rounded":[round(float(x),12) for x in np.linalg.eigvalsh(A)]},
        "identities":ids,
        "all_identities_hold":bool(all(ids.values())),
        "interpretation":"The corrected seven-sector TQC lead is the even block of the SU2 level-12 D8 ADE modular invariant. Its projector rank/nullity is the W33 CSS distance split 4/3, while the D8 graph has 7 edges, degree sum 14, and degree-square sum 28."
    }


def main()->None:
    payload=build_payload()
    out=Path("data/w33_su2_12_ade_bridge.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"all_identities_hold":payload["all_identities_hold"],"modular_invariant":payload["modular_invariant"],"dynkin_graph":payload["dynkin_graph"]},indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
