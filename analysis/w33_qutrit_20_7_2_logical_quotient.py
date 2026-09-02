#!/usr/bin/env python3
"""Explicit seven-logical-qutrit quotient basis for the [[20,7,2]]_3 code.

This module closes a subtle gap in the routed pseudothreshold work: a zero
syndrome error is not merely "logical/nonlogical".  The CSS normalizer quotient
has seven X and seven Z coordinates.  We construct canonical complements

    ker(Hz) = row(Hx) + <X_L0,...,X_L6>
    ker(Hx) = row(Hz) + <Z'_L0,...,Z'_L6>

and then dualize the Z basis so X_L Z_L^T = I_7 over GF(3).  Every zero-syndrome
Pauli can therefore be resolved to an exact logical (x_0..x_6 | z_0..z_6)
vector rather than being divided by seven heuristically.

The verifier exhaustively classifies all C(20,2)*8^2 = 12,160 weight-2 Paulis
and, by default, all C(20,3)*8^3 = 583,680 weight-3 Paulis.  Set
W33_WEIGHT3_EXHAUSTIVE=0 to skip the latter in a fast local smoke test.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import hashlib
import json
import os

import numpy as np

import w33_qutrit_20_7_2_packet_decoder as dec
import w33_qutrit_20_7_2_symplectic_embedding as base

Q = 3
PAULIS = [(a,b) for a,b in product(range(Q), repeat=2) if (a,b)!=(0,0)]


def digest_json(v):
    return "sha256:" + hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def gf3_inv(M):
    A = np.asarray(M, dtype=np.int64) % Q
    if A.shape[0] != A.shape[1]:
        raise ValueError("matrix must be square")
    n=A.shape[0]
    aug=np.concatenate([A, np.eye(n,dtype=np.int64)], axis=1)
    r=0
    for c in range(n):
        piv=next((i for i in range(r,n) if int(aug[i,c])%Q), None)
        if piv is None:
            raise ValueError("singular GF(3) matrix")
        aug[[r,piv]]=aug[[piv,r]]
        if int(aug[r,c])%Q==2:
            aug[r]=(2*aug[r])%Q
        for i in range(n):
            if i!=r and int(aug[i,c])%Q:
                aug[i]=(aug[i]-int(aug[i,c])*aug[r])%Q
        r+=1
    return aug[:,n:]%Q


def complement(subspace, ambient):
    basis=[np.asarray(r,dtype=np.int64)%Q for r in np.asarray(subspace,dtype=np.int64)]
    rank=base.rank(np.asarray(basis,dtype=np.int64)) if basis else 0
    out=[]
    for row in np.asarray(ambient,dtype=np.int64):
        trial=np.asarray(basis+[row%Q],dtype=np.int64)
        nr=base.rank(trial)
        if nr>rank:
            out.append(row%Q)
            basis.append(row%Q)
            rank=nr
    return np.asarray(out,dtype=np.int64)%Q


def solve_row_coeffs(v, rows):
    """Solve c rows = v over GF(3); rows are independent and v is in their span."""
    rows=np.asarray(rows,dtype=np.int64)%Q
    v=np.asarray(v,dtype=np.int64)%Q
    # Solve rows.T c.T = v.T by RREF on augmented 20 x (m+1).
    A=np.concatenate([rows.T, v.reshape(-1,1)], axis=1)%Q
    m=rows.shape[0]
    r=0; piv=[]
    for c in range(m):
        p=next((i for i in range(r,A.shape[0]) if int(A[i,c])%Q),None)
        if p is None:
            continue
        A[[r,p]]=A[[p,r]]
        if int(A[r,c])%Q==2:
            A[r]=(2*A[r])%Q
        for i in range(A.shape[0]):
            if i!=r and int(A[i,c])%Q:
                A[i]=(A[i]-int(A[i,c])*A[r])%Q
        piv.append(c); r+=1
    # Inconsistent row: all coefficient columns zero but augmented nonzero.
    for i in range(A.shape[0]):
        if not np.any(A[i,:m]%Q) and int(A[i,m])%Q:
            raise ValueError("vector not in row span")
    if len(piv)!=m:
        raise ValueError("rows are not independent")
    x=np.zeros(m,dtype=np.int64)
    for rr,c in enumerate(piv):
        x[c]=A[rr,m]%Q
    if not np.array_equal((x@rows)%Q,v%Q):
        raise RuntimeError("GF(3) coefficient solve replay failed")
    return x


def logical_basis():
    _, Hx, Hz = dec.code_matrices()
    ker_hz=base.nullspace(Hz)%Q
    ker_hx=base.nullspace(Hx)%Q
    X=complement(Hx,ker_hz)
    Z0=complement(Hz,ker_hx)
    if X.shape!=(7,20) or Z0.shape!=(7,20):
        raise RuntimeError(f"unexpected logical complement shapes X={X.shape} Z={Z0.shape}")
    P=(X@Z0.T)%Q
    Pinv=gf3_inv(P)
    Z=(Pinv.T@Z0)%Q
    if not np.array_equal((X@Z.T)%Q,np.eye(7,dtype=np.int64)):
        raise RuntimeError("logical dualization failed")
    return Hx,Hz,X,Z


def logical_coordinates(Hx,Hz,X,Z,x,z):
    x=np.asarray(x,dtype=np.int64)%Q; z=np.asarray(z,dtype=np.int64)%Q
    s=dec.syndrome(Hx,Hz,x,z)
    if any(s):
        return None
    cx=solve_row_coeffs(x,np.vstack([Hx,X]))
    cz=solve_row_coeffs(z,np.vstack([Hz,Z]))
    lx=tuple(int(v) for v in cx[len(Hx):])
    lz=tuple(int(v) for v in cz[len(Hz):])
    return lx+lz


def classify_weight(weight,Hx,Hz,X,Z):
    total=0; detected=0; stabilizer=0; logical=0
    logical_vectors=Counter()
    supports=Counter()
    for sites in combinations(range(20),weight):
        for labels in product(PAULIS,repeat=weight):
            total+=1
            x=np.zeros(20,dtype=np.int64); z=np.zeros(20,dtype=np.int64)
            for q,(a,b) in zip(sites,labels): x[q]=a; z[q]=b
            coords=logical_coordinates(Hx,Hz,X,Z,x,z)
            if coords is None:
                detected+=1; continue
            if not any(coords):
                stabilizer+=1; continue
            logical+=1
            logical_vectors[coords]+=1
            supports[tuple(sites)]+=1
    return {
        "weight":weight,"total":total,"detected":detected,"zero_syndrome_stabilizer":stabilizer,
        "zero_syndrome_logical":logical,"distinct_logical_vectors":len(logical_vectors),
        "logical_vector_histogram":{"".join(map(str,k)):int(v) for k,v in sorted(logical_vectors.items())},
        "malignant_support_count":len(supports),
    }


def verify():
    Hx,Hz,X,Z=logical_basis()
    w2=classify_weight(2,Hx,Hz,X,Z)
    exhaustive=os.environ.get("W33_WEIGHT3_EXHAUSTIVE","1") not in ("0","false","False")
    w3=classify_weight(3,Hx,Hz,X,Z) if exhaustive else None
    checks={
        "seven_logical_X": X.shape==(7,20),
        "seven_logical_Z": Z.shape==(7,20),
        "logical_pairing_identity": np.array_equal((X@Z.T)%Q,np.eye(7,dtype=np.int64)),
        "logical_X_commutes_with_Z_stabilizers": not np.any((X@Hz.T)%Q),
        "logical_Z_commutes_with_X_stabilizers": not np.any((Hx@Z.T)%Q),
        "weight2_exact_count": w2["total"]==12160,
        "weight2_has_logical_events": w2["zero_syndrome_logical"]>0,
        "weight3_exact_count_if_enabled": (not exhaustive) or w3["total"]==583680,
    }
    checks={k:bool(v) for k,v in checks.items()}
    basis_payload={"X":X.tolist(),"Z":Z.tolist()}
    return {
        "schema":"w33.qutrit-20-7-2-logical-quotient.v1",
        "status":"PASS" if all(checks.values()) else "FAIL",
        "checks":checks,
        "logical_basis":{"X":X.tolist(),"Z":Z.tolist(),"sha256":digest_json(basis_payload)},
        "weight2":w2,
        "weight3":w3,
        "weight3_exhaustive":bool(exhaustive),
        "theorem":"The CSS normalizer quotient is resolved into seven dual logical X/Z coordinates. Every enumerated zero-syndrome weight-2/3 Pauli is assigned either the stabilizer class or one exact 14-trit logical Pauli vector.",
        "boundary":"This is an exact algebraic quotient classifier. It does not assume seven logical channels are statistically identical and therefore does not divide a block error rate by seven.",
    }

if __name__=="__main__":
    out=verify(); print(json.dumps(out,indent=2)); raise SystemExit(0 if out["status"]=="PASS" else 1)
