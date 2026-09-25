#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from itertools import combinations
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_bt1348_bt1349_errata.json"

W=np.exp(2j*np.pi/3)
X=np.array([[0,0,1],[1,0,0],[0,1,0]],dtype=complex)
Z=np.diag([1,W,W**2])
I3=np.eye(3,dtype=complex)

def idx(a,b,c):
    return 9*a+3*b+c

def basis_state(a,b,c):
    v=np.zeros(27,dtype=complex)
    v[idx(a,b,c)]=1
    return v

def main():
    # BT1348 Weyl convention.
    assert np.allclose(X@Z,(W**2)*(Z@X))
    assert not np.allclose(X@Z,W*(Z@X))

    rep=[basis_state(i,i,i) for i in range(3)]
    S1=np.kron(np.kron(Z,np.conj(Z)),I3)
    S2=np.kron(np.kron(I3,Z),np.conj(Z))
    assert all(np.allclose(S@v,v) for S in (S1,S2) for v in rep)

    psi=sum(rep)/np.sqrt(3)
    X0=np.kron(np.kron(X,I3),I3)
    Z0=np.kron(np.kron(Z,I3),I3)
    shifted=X0@rep[0]
    assert not np.allclose(S1@shifted,shifted)
    phased=Z0@psi
    assert np.allclose(S1@phased,phased)
    assert np.allclose(S2@phased,phased)
    assert not np.allclose(phased,psi)

    U=np.zeros((27,27),dtype=complex)
    for a in range(3):
        for b in range(3):
            for c in range(3):
                src=idx(a,b,c)
                if a==0:
                    dst=idx(a,b,c)
                elif a==1:
                    dst=idx(a,c,b)
                else:
                    dst=idx(a,(b+1)%3,(c+2)%3)
                U[dst,src]=1
    assert np.allclose(U.conj().T@U,np.eye(27))
    P=sum(np.outer(v,v.conj()) for v in rep)
    routed=U@psi
    weight=float(np.vdot(routed,P@routed).real)
    assert abs(weight-2/3)<1e-12

    # Shell arithmetic: the contextual count is not 12+27.
    assert 1+12+27==40
    assert 36!=12+27

    # BT1349 point adjacency by sharing a Fano line is K7.
    lines=[
      tuple(sorted((i%7,(i+1)%7,(i+3)%7)))
      for i in range(7)
    ]
    A=np.zeros((7,7),dtype=int)
    for L in lines:
        for i,j in combinations(L,2):
            A[i,j]=A[j,i]=1
    assert set(map(int,A.sum(axis=1)))=={6}
    eig=np.linalg.eigvalsh(A.astype(float))
    assert np.allclose(sorted(eig),[-1]*6+[6])

    # A later, genuinely quantum [[3,1,2]]_3 erasure code is distinct.
    later=json.loads(
        (ROOT/"data/PART_BT3715_BT3721_CARRIER_TOURNAMENT_PROCESS_BUDGET_IDENTIFICATION_SCHEDULER_TWIRL_results.json").read_text()
    )
    carrier=later["passes"]["3715_minimum_erasure_correcting_carrier"]
    assert carrier["code"]=="[[3,1,2]]_3"
    assert carrier["knill_laflamme_erasure_checks"]==27
    supports=carrier["logical_basis_supports"]
    assert supports["0"]!=[[0,0,0]]
    assert len(supports["0"])==3

    out={
      "schema":"w33.20260924.bt1348_bt1349_errata.v1",
      "status":"PASS_BT1348_BT1349_LEGACY_WITNESSES_REPAIRED_WITH_FIREWALLS",
      "BT1348":{
        "weyl_relation":"XZ=omega^-1 ZX for the declared X,Z convention",
        "repetition_subspace":"detects X shifts but not one-site Z phase",
        "full_quantum_code_claim":False,
        "routing_unitary":True,
        "routing_repetition_subspace_weight":"2/3",
        "routing_preserves_repetition_subspace":False,
        "shell_identity":"1+12+27=40",
        "contextual_36_equals_12_plus_27":False,
        "no_factory_inference_from_shell_counts":False,
      },
      "BT1349":{
        "point_graph":"K7",
        "degree":6,
        "spectrum":{"6":1,"-1":6},
        "diameter":1,
        "pair_channels":21,
        "old_3_regular_claim":False,
      },
      "later_code_boundary":{
        "valid_code":"BT3715 [[3,1,2]]_3 one-known-erasure code",
        "knill_laflamme_checks":27,
        "distinct_from_BT1348_repetition_basis":True,
      },
      "theorem":(
        "BT1348 and BT1349 contained independent legacy overclaims.  With the "
        "declared qutrit Pauli convention the Weyl relation has inverse phase; "
        "the BT1348 repetition subspace detects shifts but not all one-site "
        "Paulis, and BT1340 routing leaks one third of the tested state outside "
        "that subspace.  Separately, Fano point adjacency by sharing a line is "
        "K7, not a cubic graph.  The later BT3715 erasure code remains a valid "
        "[[3,1,2]]_3 construction and is not the BT1348 repetition basis."
      ),
      "boundary":(
        "These are repairs to legacy witnesses, not a rejection of later exact "
        "qutrit QEC or ADQC results.  In particular they reinforce the current "
        "resource boundary that non-Clifford magic is not obtained from shell "
        "counting alone."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":out["status"],"BT1348":out["BT1348"],"BT1349":out["BT1349"]},indent=2))

if __name__=="__main__":
    main()
