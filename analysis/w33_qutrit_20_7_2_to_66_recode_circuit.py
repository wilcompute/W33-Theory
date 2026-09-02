#!/usr/bin/env python3
"""Exact Clifford-tableau recode from [[20,7,2]]_3 to Pass79 [[66,8,3]]_3.

The logical bridge alone does not define a physical code switch.  This module
builds an explicit symplectic tableau circuit for the natural decode/re-encode
implementation:

  source [[20,7,2]] decoder tableau
    -> seven bare logical qutrit handoffs
    -> seven independent cyclic [[5,1,3]]_3 block encoder tableaus.

Each code tableau is completed exactly over GF(3): stabilizers S_i are paired
with destabilizers D_i, logical X/Z pairs are preserved, and the full 2n x 2n
row tableau satisfies M J M^T = J.  The transport of all seven source logical
X/Z generators into the target block logical generators is therefore an exact
Clifford statement, not a naming convention.

The fault result is decisive.  Every one of the 7*8=56 nontrivial Pauli faults
on the seven bare logical handoff qutrits becomes a zero-syndrome target logical
operator.  Hence the obvious decode -> bare handoff -> re-encode circuit is NOT
one-fault tolerant.  A physical FT recode must avoid that bare-logical window,
for example via encoded teleportation or direct gauge/stabilizer measurement.
"""
from __future__ import annotations

from collections import Counter
from itertools import product
import hashlib,json
import numpy as np

import w33_qutrit_20_7_2_packet_decoder as dec
import w33_qutrit_20_7_2_logical_quotient as logical
import w33_qutrit_20_7_2_to_66_bridge as bridge
import w33_pass79_full_closure as p79

Q=3
PAULIS=[(a,b) for a,b in product(range(Q),repeat=2) if (a,b)!=(0,0)]

def digest_json(v):return "sha256:"+hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def sp(u,v):
    u=np.asarray(u,dtype=np.int64)%Q;v=np.asarray(v,dtype=np.int64)%Q;n=len(u)//2
    return int((u[:n]@v[n:]-u[n:]@v[:n])%Q)

def rank(A):
    A=np.asarray(A,dtype=np.int64)%Q
    if A.size==0:return 0
    A=A.copy();m,n=A.shape;r=0
    for c in range(n):
        p=next((i for i in range(r,m) if int(A[i,c])%Q),None)
        if p is None:continue
        A[[r,p]]=A[[p,r]]
        if int(A[r,c])==2:A[r]=(2*A[r])%Q
        for i in range(m):
            if i!=r and int(A[i,c])%Q:A[i]=(A[i]-int(A[i,c])*A[r])%Q
        r+=1
        if r==m:break
    return r

def solve(A,b):
    A=np.asarray(A,dtype=np.int64)%Q;b=np.asarray(b,dtype=np.int64)%Q
    aug=np.concatenate([A,b.reshape(-1,1)],axis=1);m,n=A.shape;r=0;piv=[]
    for c in range(n):
        p=next((i for i in range(r,m) if int(aug[i,c])%Q),None)
        if p is None:continue
        aug[[r,p]]=aug[[p,r]]
        if int(aug[r,c])==2:aug[r]=(2*aug[r])%Q
        for i in range(m):
            if i!=r and int(aug[i,c])%Q:aug[i]=(aug[i]-int(aug[i,c])*aug[r])%Q
        piv.append(c);r+=1
    if any(not np.any(aug[i,:n]) and int(aug[i,n]) for i in range(m)):raise ValueError("inconsistent GF3 system")
    x=np.zeros(n,dtype=np.int64)
    for rr,c in enumerate(piv):x[c]=aug[rr,n]%Q
    if not np.array_equal((A@x)%Q,b%Q):raise RuntimeError("solve replay failed")
    return x

def constraint_row(u):
    u=np.asarray(u,dtype=np.int64)%Q;n=len(u)//2
    return np.concatenate([u[n:],(-u[:n])%Q])%Q

def full_x(row,n):return np.concatenate([np.asarray(row,dtype=np.int64)%Q,np.zeros(n,dtype=np.int64)])
def full_z(row,n):return np.concatenate([np.zeros(n,dtype=np.int64),np.asarray(row,dtype=np.int64)%Q])

def complete_tableau(stabilizers,LX,LZ,n):
    S=[np.asarray(x,dtype=np.int64)%Q for x in stabilizers]
    X=[np.asarray(x,dtype=np.int64)%Q for x in LX];Z=[np.asarray(x,dtype=np.int64)%Q for x in LZ]
    r=len(S);k=len(X)
    if r+k!=n:raise ValueError("r+k must equal n")
    if any(sp(a,b) for a in S for b in S):raise ValueError("stabilizers do not commute")
    if any(sp(s,l) for s in S for l in X+Z):raise ValueError("logical does not normalize stabilizer")
    if [[sp(X[i],Z[j]) for j in range(k)] for i in range(k)]!=np.eye(k,dtype=int).tolist():raise ValueError("logical pairing not identity")
    D=[]
    for i in range(r):
        refs=S+X+Z+D
        A=np.asarray([constraint_row(u) for u in refs],dtype=np.int64)%Q
        b=np.zeros(len(refs),dtype=np.int64);b[i]=1
        d=solve(A,b);D.append(d)
    M=np.asarray(D+X+S+Z,dtype=np.int64)%Q
    if M.shape!=(2*n,2*n) or rank(M)!=2*n:raise RuntimeError("tableau not full rank")
    J=np.block([[np.zeros((n,n),dtype=np.int64),np.eye(n,dtype=np.int64)],[2*np.eye(n,dtype=np.int64),np.zeros((n,n),dtype=np.int64)]])%Q
    if not np.array_equal((M@J@M.T)%Q,J):raise RuntimeError("tableau is not symplectic")
    return M,D

def source_tableau():
    _,Hx,Hz=dec.code_matrices();_,_,X,Z=logical.logical_basis();n=20
    S=[full_x(r,n) for r in Hx]+[full_z(r,n) for r in Hz]
    LX=[full_x(r,n) for r in X];LZ=[full_z(r,n) for r in Z]
    return complete_tableau(S,LX,LZ,n),S,LX,LZ

def target_block_tableau():
    n=5;S=[np.asarray(r,dtype=np.int64)%Q for r in p79.cyclic_5_code_rows()]
    lx,lz=bridge.block_logical_pair();LX=[np.asarray(lx,dtype=np.int64)%Q];LZ=[np.asarray(lz,dtype=np.int64)%Q]
    return complete_tableau(S,LX,LZ,n),S,LX,LZ

def canonical_pauli(n,q,a,b):
    v=np.zeros(2*n,dtype=np.int64);v[q]=a;v[n+q]=b;return v

def encode_canonical(v,M):
    # Row-vector Pauli coordinates: canonical coefficients multiply image rows.
    return (np.asarray(v,dtype=np.int64)@np.asarray(M,dtype=np.int64))%Q

def syndrome(v,S):return tuple(sp(v,s) for s in S)

def in_rowspace(v,M):return rank(np.vstack([np.asarray(M,dtype=np.int64),np.asarray(v,dtype=np.int64)]))==rank(np.asarray(M,dtype=np.int64))

def handoff_fault_census(M5,S5):
    out=[];classes=Counter()
    for block in range(7):
        for a,b in PAULIS:
            e=encode_canonical(canonical_pauli(5,4,a,b),M5)
            syn=syndrome(e,S5)
            cls="TARGET_ZERO_SYNDROME_LOGICAL" if not any(syn) and not in_rowspace(e,S5) else "UNEXPECTED"
            classes[cls]+=1;out.append({"block":block,"pauli":[a,b],"class":cls,"target_sparse":p79.sparse_row(e.tolist(),5)})
    return out,classes

def target_boundary_faults(M5,S5):
    classes=Counter();samples={}
    # Before block encoding: ancilla wires 0..3 are |0>, logical wire 4 is data.
    for q in range(5):
        for a,b in PAULIS:
            e=encode_canonical(canonical_pauli(5,q,a,b),M5);syn=syndrome(e,S5)
            if not any(syn):cls="STABILIZER_HARMLESS" if in_rowspace(e,S5) else "LOGICAL_MALIGNANT"
            else:cls="DETECTABLE"
            classes[f"preencode_{cls}"]+=1;samples.setdefault(f"preencode_{cls}",{"wire":q,"pauli":[a,b],"mapped":p79.sparse_row(e.tolist(),5),"syndrome":list(syn)})
    # After encoding: all single physical qutrit Paulis must be detected for d=3.
    for q in range(5):
        for a,b in PAULIS:
            e=canonical_pauli(5,q,a,b);syn=syndrome(e,S5)
            cls="postencode_DETECTABLE" if any(syn) else "postencode_UNDETECTED"
            classes[cls]+=1;samples.setdefault(cls,{"wire":q,"pauli":[a,b],"syndrome":list(syn)})
    return classes,samples

def verify():
    (M20,_),S20,LX20,LZ20=source_tableau();(M5,_),S5,LX5,LZ5=target_block_tableau()
    # In our canonical ordering source logical qutrits occupy positions 13..19;
    # target block logical input is canonical position 4.
    transport=[];transport_ok=True
    for j in range(7):
        sx=encode_canonical(canonical_pauli(20,13+j,1,0),M20);sz=encode_canonical(canonical_pauli(20,13+j,0,1),M20)
        tx=encode_canonical(canonical_pauli(5,4,1,0),M5);tz=encode_canonical(canonical_pauli(5,4,0,1),M5)
        ok=np.array_equal(sx,LX20[j]) and np.array_equal(sz,LZ20[j]) and np.array_equal(tx,LX5[0]) and np.array_equal(tz,LZ5[0])
        transport_ok=transport_ok and ok;transport.append({"logical":j,"source_canonical_wire":13+j,"target_block":j,"target_canonical_wire":4,"verified":bool(ok)})
    handoff,handclasses=handoff_fault_census(M5,S5);boundary,boundsamples=target_boundary_faults(M5,S5)
    checks={
      "source_tableau_symplectic":M20.shape==(40,40),
      "target_5q_tableau_symplectic":M5.shape==(10,10),
      "all_seven_logical_generators_transport_exactly":transport_ok,
      "all_56_bare_handoff_Paulis_are_target_logicals":len(handoff)==56 and handclasses==Counter({"TARGET_ZERO_SYNDROME_LOGICAL":56}),
      "target_ancilla_Z_only_faults_are_stabilizer_harmless":boundary["preencode_STABILIZER_HARMLESS"]==8,
      "target_ancilla_X_component_faults_are_detectable":boundary["preencode_DETECTABLE"]==24,
      "target_logical_input_faults_are_malignant":boundary["preencode_LOGICAL_MALIGNANT"]==8,
      "all_40_postencode_single_qutrit_faults_detected":boundary["postencode_DETECTABLE"]==40 and boundary["postencode_UNDETECTED"]==0,
    }
    checks={k:bool(v) for k,v in checks.items()}
    return {
      "schema":"w33.qutrit-20-7-2-to-66-recode-circuit.v1","status":"PASS" if all(checks.values()) else "FAIL","checks":checks,
      "circuit":{"stages":[{"stage":"SOURCE_TABLEAU_DECODE","physical_qutrits":20,"tableau_sha256":digest_json(M20.tolist())},{"stage":"BARE_LOGICAL_HANDOFF","logical_qutrits":7,"mapping":transport},{"stage":"SEVEN_PARALLEL_5Q_BLOCK_ENCODERS","blocks":7,"physical_qutrits":35,"tableau_sha256":digest_json(M5.tolist())},{"stage":"PASS79_PACKAGING","spare_5q_block":1,"frozen_Z_ancillas":26,"total_target_qutrits":66}]},
      "fault_census":{"bare_handoff":dict(handclasses),"target_block_boundary_per_block":dict(boundary),"target_boundary_samples":boundsamples,"bare_handoff_sample":handoff[:4]},
      "decision":"REFUSE_NAIVE_RECODE_AS_FAULT_TOLERANT",
      "theorem":"The decode/bare-handoff/re-encode tableau transports all seven logical Pauli pairs exactly, but every nontrivial single Pauli fault in the bare seven-qutrit handoff window becomes an undetected target logical fault. The natural recode is therefore not one-fault tolerant.",
      "boundary":"The tableaus are exact Clifford macro-circuits. They do not synthesize the source decoder into W33-local optical elementary gates, and they prove a no-go for the naive bare-handoff architecture rather than a fault-tolerant code-switch. An FT replacement must keep the information encoded throughout, e.g. encoded teleportation or direct gauge/stabilizer measurement.",
    }
if __name__=="__main__":
    out=verify();print(json.dumps(out,indent=2));raise SystemExit(0 if out["status"]=="PASS" else 1)
