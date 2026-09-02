#!/usr/bin/env python3
"""Logical bridge from [[20,7,2]]_3 into verified 66-qutrit stores.

The seven source logical qutrits can be recoded into seven independent logical
blocks of Pass79's explicit noncanonical [[66,8,3]]_3 store.  Separately, the
committed K12-labelled 44-face complex is now audited by
w33_k12_singular_css_closure: it is a singular pseudocomplex with raw chain CSS
[[66,13,3]]_3, and five explicit commuting Z-logical gauge constraints produce
a native K12-labelled [[66,8,3]]_3 code.

This module certifies logical symplectic compatibility.  It does not claim that
a decode/bare-handoff/re-encode implementation is fault tolerant; that physical
circuit question is handled by the recode-circuit witness.
"""
from __future__ import annotations

from itertools import combinations,product
from pathlib import Path
import hashlib,json,sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))

import w33_pass79_full_closure as p79
import w33_qutrit_20_7_2_logical_quotient as source
import w33_k12_singular_css_closure as k12css

Q=3
PAULIS=[(a,b) for a,b in product(range(Q),repeat=2) if (a,b)!=(0,0)]

def digest_json(v):return "sha256:"+hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def block_logical_pair():
    rows=p79.cyclic_5_code_rows();n=5;candidates=[]
    for weight in (1,2,3):
        for sites in combinations(range(n),weight):
            for labels in product(PAULIS,repeat=weight):
                v=[0]*(2*n)
                for site,(x,z) in zip(sites,labels):v[site]=x;v[n+site]=z
                if all(p79.symplectic(v,h,n)==0 for h in rows) and not p79.in_rowspace(v,rows):candidates.append(v)
        if candidates:break
    if not candidates:raise RuntimeError("five-qutrit logical operator not found")
    lx=candidates[0];lz=next((v for v in candidates if p79.symplectic(lx,v,n)==1),None)
    if lz is None:
        for sites in combinations(range(n),3):
            for labels in product(PAULIS,repeat=3):
                v=[0]*(2*n)
                for site,(x,z) in zip(sites,labels):v[site]=x;v[n+site]=z
                if all(p79.symplectic(v,h,n)==0 for h in rows) and not p79.in_rowspace(v,rows) and p79.symplectic(lx,v,n)==1:lz=v;break
            if lz is not None:break
    if lz is None:raise RuntimeError("five-qutrit logical partner not found")
    return lx,lz

def embed_block(v5,block,n=66):
    out=[0]*(2*n);off=5*int(block)
    for i in range(5):out[off+i]=v5[i]%Q;out[n+off+i]=v5[5+i]%Q
    return out

def target_logical_basis():
    witness=p79.build_66_stabilizer();stab=witness["stabilizer_matrix"];lx5,lz5=block_logical_pair()
    X=[embed_block(lx5,b) for b in range(7)];Z=[embed_block(lz5,b) for b in range(7)]
    pairing=[[p79.symplectic(X[i],Z[j],66) for j in range(7)] for i in range(7)]
    return witness,stab,X,Z,pairing,lx5,lz5

def verify():
    _,_,X20,Z20=source.logical_basis();witness,stab,X66,Z66,pairing,lx5,lz5=target_logical_basis();I7=np.eye(7,dtype=np.int64).tolist()
    topo=k12css.verify();native=topo.get("native_k8_gauge_fix",{})
    checks={
      "source_has_7_dual_logicals":X20.shape==(7,20) and np.array_equal((X20@Z20.T)%Q,np.eye(7,dtype=np.int64)),
      "pass79_target_is_verified_66_8_3":witness["distance_verified"] and witness["parameters"]=={"n":66,"rank_stabilizer":58,"k_logical":8,"distance":3},
      "seven_target_block_logicals_commute_with_stabilizer":all(p79.symplectic(v,h,66)==0 for v in X66+Z66 for h in stab),
      "seven_target_block_logicals_are_nonstabilizer":all(not p79.in_rowspace(v,stab) for v in X66+Z66),
      "source_target_logical_pairing_preserved":pairing==I7,
      "K12_singular_topology_audit_passes":topo.get("status")=="PASS",
      "K12_raw_chain_code_is_66_13_3":topo.get("raw_css",{}).get("parameters")=="[[66,13,3]]_3",
      "K12_native_five_constraint_gauge_fix_is_66_8_3":native.get("parameters")=="[[66,8,3]]_3",
    }
    checks={k:bool(v) for k,v in checks.items()}
    return {
      "schema":"w33.qutrit-20-7-2-to-66-storage-bridge.v2","status":"PASS" if all(checks.values()) else "FAIL","checks":checks,
      "bridge":{"type":"logical_decode_reencode","source":"[[20,7,2]]_3","target":"Pass79 explicit [[66,8,3]]_3 block-plus-ancilla stabilizer","source_logical_basis_sha256":digest_json({"X":X20.tolist(),"Z":Z20.tolist()}),"target_logical_X":[p79.sparse_row(v,66) for v in X66],"target_logical_Z":[p79.sparse_row(v,66) for v in Z66],"target_blocks_used":[0,1,2,3,4,5,6],"spare_target_logical_block":7,"pairing":pairing,"storage_distance_after_successful_recode":3,"source_distance_before_recode":2},
      "K12_native_code":{"raw_parameters":"[[66,13,3]]_3","gauge_fixed_parameters":"[[66,8,3]]_3","extra_Z_constraints_required":5,"extra_constraint_sha256":native.get("extra_constraint_sha256"),"topology":"singular pseudocomplex; normalization T^2 disjoint-union S^2","standard_genus6_surface_claim":False},
      "five_qutrit_base_logical":{"X":p79.sparse_row(lx5,5),"Z":p79.sparse_row(lz5,5)},
      "theorem":"The seven source logical qutrits have an exact symplectic recoding into seven independent logical blocks of the Pass79 distance-3 store. Independently, five explicit commuting Z-logical gauge constraints convert the native K12-labelled [[66,13,3]]_3 singular-chain code into an exact [[66,8,3]]_3 CSS code.",
      "boundary":"This is a logical/stabilizer compatibility theorem. It does not certify a one-fault-tolerant code-switch circuit. The K12-native code is gauge-fixed on a singular pseudocomplex, not a standard genus-6 surface code.",
    }
if __name__=="__main__":
    out=verify();print(json.dumps(out,indent=2));raise SystemExit(0 if out["status"]=="PASS" else 1)
