#!/usr/bin/env python3
"""Bridge the [[20,7,2]]_3 logical block to the explicit [[66,8,3]]_3 store.

Two issues that had been conflated in the architecture are separated here.

(1) Pass 79 already proves an explicit finite [[66,8,3]]_3 stabilizer: eight
    cyclic [[5,1,3]]_3 blocks plus 26 frozen Z ancillas.  We derive a logical
    X/Z pair for the five-qutrit block and use seven of the eight blocks as a
    distance-3 storage target for the seven logical qutrits of [[20,7,2]]_3.
    The resulting bridge is a *logical recode* (decode/code-switch/re-encode),
    not a monomial embedding of 20 physical qutrits into 66 physical qutrits.

(2) The repo's oriented K12 completion has V=12,E=66,F=44 and genus 6.  The
    standard closed orientable homological surface code on those 66 edges has

        k = E - rank(d1) - rank(d2) = 66 - 11 - 43 = 12 = 2g,

    over GF(3), not 8.  Therefore the phrase "[[66,8,3]]_3 genus-6 K12 surface
    code" cannot mean the *standard* K12 surface code unless four additional
    independent commuting stabilizer/gauge constraints are explicitly supplied.
    This is a finite parameter no-go, not an argument from missing files.
"""
from __future__ import annotations

from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))

import w33_pass79_full_closure as p79
import w33_reye_k12_orientable_horizon_completion as k12
import w33_qutrit_20_7_2_logical_quotient as source
import w33_qutrit_20_7_2_symplectic_embedding as base

Q=3
PAULIS=[(a,b) for a,b in product(range(Q),repeat=2) if (a,b)!=(0,0)]


def digest_json(v):
    return "sha256:"+hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def block_logical_pair():
    rows=p79.cyclic_5_code_rows(); n=5
    candidates=[]
    for weight in (1,2,3):
        for sites in combinations(range(n),weight):
            for labels in product(PAULIS,repeat=weight):
                v=[0]*(2*n)
                for site,(x,z) in zip(sites,labels): v[site]=x; v[n+site]=z
                if all(p79.symplectic(v,h,n)==0 for h in rows) and not p79.in_rowspace(v,rows):
                    candidates.append(v)
        if candidates: break
    if not candidates: raise RuntimeError("five-qutrit logical operator not found")
    lx=candidates[0]
    lz=next((v for v in candidates if p79.symplectic(lx,v,n)==1),None)
    if lz is None:
        # The first weight shell may contain one projective logical line only;
        # continue the weight-3 census until a symplectic partner is found.
        for sites in combinations(range(n),3):
            for labels in product(PAULIS,repeat=3):
                v=[0]*(2*n)
                for site,(x,z) in zip(sites,labels): v[site]=x; v[n+site]=z
                if all(p79.symplectic(v,h,n)==0 for h in rows) and not p79.in_rowspace(v,rows) and p79.symplectic(lx,v,n)==1:
                    lz=v; break
            if lz is not None: break
    if lz is None: raise RuntimeError("five-qutrit logical symplectic partner not found")
    return lx,lz


def embed_block(v5,block,n=66):
    out=[0]*(2*n); off=5*int(block)
    for i in range(5): out[off+i]=v5[i]%Q; out[n+off+i]=v5[5+i]%Q
    return out


def target_logical_basis():
    witness=p79.build_66_stabilizer(); stab=witness["stabilizer_matrix"]
    lx5,lz5=block_logical_pair()
    X=[embed_block(lx5,b) for b in range(7)]
    Z=[embed_block(lz5,b) for b in range(7)]
    pairing=[[p79.symplectic(X[i],Z[j],66) for j in range(7)] for i in range(7)]
    return witness,stab,X,Z,pairing,lx5,lz5


def k12_boundary_matrices():
    faces=list(k12.oriented_horizon_faces())
    edges=list(combinations(range(12),2)); ei={e:i for i,e in enumerate(edges)}
    d1=np.zeros((12,66),dtype=np.int64)
    for j,(u,v) in enumerate(edges): d1[u,j]=2; d1[v,j]=1
    d2=np.zeros((66,len(faces)),dtype=np.int64)
    for f,(a,b,c) in enumerate(faces):
        for u,v in ((a,b),(b,c),(c,a)):
            e=tuple(sorted((u,v))); sign=1 if u<v else 2
            d2[ei[e],f]=(d2[ei[e],f]+sign)%Q
    return faces,edges,d1%Q,d2%Q


def verify():
    Hx,Hz,X20,Z20=source.logical_basis()
    witness,stab,X66,Z66,pairing,lx5,lz5=target_logical_basis()
    I7=np.eye(7,dtype=np.int64).tolist()
    target_commutes=all(p79.symplectic(v,h,66)==0 for v in X66+Z66 for h in stab)
    target_nonstab=all(not p79.in_rowspace(v,stab) for v in X66+Z66)

    faces,edges,d1,d2=k12_boundary_matrices()
    r1=base.rank(d1); r2=base.rank(d2)
    chain_zero=not np.any((d1@d2)%Q)
    k_surface=66-r1-r2
    extra_constraints_needed=k_surface-8

    checks={
        "source_has_7_dual_logicals":X20.shape==(7,20) and np.array_equal((X20@Z20.T)%Q,np.eye(7,dtype=np.int64)),
        "pass79_target_is_verified_66_8_3":witness["distance_verified"] and witness["parameters"]=={"n":66,"rank_stabilizer":58,"k_logical":8,"distance":3},
        "seven_target_block_logicals_commute_with_stabilizer":target_commutes,
        "seven_target_block_logicals_are_nonstabilizer":target_nonstab,
        "source_target_logical_pairing_preserved":pairing==I7,
        "K12_chain_complex_closes_over_GF3":chain_zero,
        "K12_boundary_ranks_are_11_and_43":r1==11 and r2==43,
        "standard_genus6_K12_surface_code_encodes_12_not_8":k_surface==12 and extra_constraints_needed==4,
    }
    checks={k:bool(v) for k,v in checks.items()}
    bridge={
        "type":"logical_decode_reencode","source":"[[20,7,2]]_3","target":"Pass79 explicit [[66,8,3]]_3 block-plus-ancilla stabilizer",
        "source_logical_basis_sha256":digest_json({"X":X20.tolist(),"Z":Z20.tolist()}),
        "target_logical_X":[p79.sparse_row(v,66) for v in X66],
        "target_logical_Z":[p79.sparse_row(v,66) for v in Z66],
        "target_blocks_used":[0,1,2,3,4,5,6],"spare_target_logical_block":7,"frozen_ancilla_sites":[40,65],
        "pairing":pairing,
        "storage_distance_after_successful_recode":3,
        "source_distance_before_recode":2,
        "effect":"removes the distance-2 storage bottleneck after successful logical recoding; it does not make source-side gates fault tolerant before the recode",
    }
    k12audit={
        "V":12,"E":66,"F":44,"genus":6,"rank_d1_GF3":int(r1),"rank_d2_GF3":int(r2),"standard_surface_code_k":int(k_surface),
        "claimed_k":8,"additional_independent_constraints_required_for_k8":int(extra_constraints_needed),
        "decision":"NO_GO_FOR_STANDARD_CLOSED_K12_SURFACE_CODE_AS_[[66,8,3]]_3",
        "repair_options":["specify four additional independent commuting stabilizers/gauge-fixing constraints","or label the Pass79 block-plus-ancilla code as the [[66,8,3]]_3 store and keep K12 as a separate 66-edge compiler surface"],
    }
    return {
        "schema":"w33.qutrit-20-7-2-to-66-storage-bridge.v1","status":"PASS" if all(checks.values()) else "FAIL","checks":checks,
        "bridge":bridge,"K12_surface_code_audit":k12audit,
        "five_qutrit_base_logical":{"X":p79.sparse_row(lx5,5),"Z":p79.sparse_row(lz5,5)},
        "theorem":"The seven logical qutrits of [[20,7,2]]_3 admit a symplectic logical recoding into seven independent logical blocks of the explicit Pass79 [[66,8,3]]_3 store, gaining distance 3 after recoding. Separately, the standard closed genus-6 K12 edge surface code has k=12 over GF(3), so it is not the cited k=8 code without four extra constraints.",
        "boundary":"No physical code-switch circuit, ancilla factory, or threshold is asserted. The Pass79 target is explicit but noncanonical; the K12 no-go applies to the standard homological surface-code construction, not to every possible stabilizer code supported on 66 K12-labelled sites.",
    }

if __name__=="__main__":
    out=verify(); print(json.dumps(out,indent=2)); raise SystemExit(0 if out["status"]=="PASS" else 1)
