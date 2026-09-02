#!/usr/bin/env python3
"""Exact fault-location census for the current [[20,7,2]]_3 -> W33 -> 66 path.

Endpoint Pauli weight is not a circuit fault model.  This module names the
actual locations currently present in executable certificates:

* 13 ancilla preparations in the mapped syndrome extractor;
* every scheduled weighted-SUM data/ancilla coupling;
* 13 ancilla readouts;
* seven bare logical handoff locations in the naive 20->66 recode;
* each canonical input boundary and each physical output boundary of the seven
  target [[5,1,3]]_3 block encoders.

Syndrome-line additive trit faults are evaluated against the exact decoder.
Data-side Pauli faults at a W33 physical edge are projected back to the external
20-qutrit code ONLY when the physical unit vector is provably in the row span of
A (X) and/or B (Z).  Otherwise the event is explicitly classified
AMBIENT_W33_PARENT_DECODER_REQUIRED.  Recode boundary faults use the exact
symplectic tableau census and expose the 56/56 malignant bare-handoff no-go.

Internal elementary-gate faults inside the source decoder and target tableau
encoders remain unresolved until those tableaus are synthesized into a physical
primitive sequence.  That omission is explicit rather than hidden in an
endpoint-weight approximation.
"""
from __future__ import annotations

from collections import Counter
from itertools import product
import hashlib,json
import numpy as np

import w33_qutrit_20_7_2_packet_decoder as dec
import w33_qutrit_20_7_2_logical_quotient as logical
import w33_qutrit_20_7_2_multiminor_optimizer as multi
import w33_qutrit_20_7_2_circuit_noise as noise
import w33_qutrit_20_7_2_to_66_recode_circuit as recode
import w33_qutrit_20_7_2_symplectic_embedding as base

Q=3
PAULIS=[(a,b) for a,b in product(range(Q),repeat=2) if (a,b)!=(0,0)]

def digest_json(v):return "sha256:"+hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def in_rowspan(v,M):return base.rank(np.vstack([M,v]))==base.rank(M)

def coeffs(v,M):return logical.solve_row_coeffs(v,M)

def classify_external_pauli(x,z,Hx,Hz,X,Z):
    s=dec.syndrome(Hx,Hz,x,z)
    if any(s):return "EXTERNAL_DETECTED",{"syndrome":list(s)}
    c=logical.logical_coordinates(Hx,Hz,X,Z,x,z)
    if c is None:raise RuntimeError("zero syndrome did not resolve")
    return ("EXTERNAL_STABILIZER" if not any(c) else "EXTERNAL_LOGICAL_MALIGNANT"),{"logical":list(c)}

def mapped_data_faults(candidate_count=multi.DEFAULT_CANDIDATES):
    _,Hx,Hz=dec.code_matrices();_,_,A,B,_=dec.selected_embedding(int(candidate_count));_,_,X,Z=logical.logical_basis()
    mX,mZ=dec.mapped_checks(A,B,Hx,Hz);rounds,_=dec.check_interactions(mX,mZ)
    rows=[];counts=Counter();samples={}
    for r,items in enumerate(rounds):
        for slot,item in enumerate(items):
            edge=int(item["data_edge"])
            ex=np.zeros(240,dtype=np.int64);ex[edge]=1
            x_in=in_rowspan(ex,A);z_in=in_rowspan(ex,B)
            for a,b in PAULIS:
                needx=a!=0;needz=b!=0
                if (needx and not x_in) or (needz and not z_in):
                    cls="AMBIENT_W33_PARENT_DECODER_REQUIRED";detail={"X_unit_in_A_image":bool(x_in),"Z_unit_in_B_image":bool(z_in)}
                else:
                    x=(a*coeffs(ex,A))%Q if needx else np.zeros(20,dtype=np.int64)
                    z=(b*coeffs(ex,B))%Q if needz else np.zeros(20,dtype=np.int64)
                    cls,detail=classify_external_pauli(x,z,Hx,Hz,X,Z)
                key={"round":r,"slot":slot,"check":item["check"],"data_edge":edge,"pauli":[a,b],"class":cls,**detail}
                rows.append(key);counts[cls]+=1;samples.setdefault(cls,key)
    return rounds,rows,counts,samples

def syndrome_location_faults(candidate_count=multi.DEFAULT_CANDIDATES):
    Hx,Hz,rounds,_,_=noise.schedule_ledger(int(candidate_count));_,_,X,Z=logical.logical_basis();table,_,_=noise.decoder_table(Hx,Hz)
    rows=[];counts=Counter();samples={}
    # On clean data a prep/readout/coupling-ancilla additive fault shifts exactly
    # one final check trit.  This is the single-location transfer function used
    # by the current extraction model.
    for kind in ("ANCILLA_PREP","ANCILLA_READOUT"):
        for check in range(13):
            for delta in (1,2):
                obs=[0]*13;obs[check]=delta;action,guess=noise.classify_observed_syndrome(table,obs)
                cls=action if action.startswith("REFUSE") else "FALSE_CORRECTION_ATTEMPT"
                row={"kind":kind,"check_index":check,"delta":delta,"class":cls,"guess":guess};rows.append(row);counts[cls]+=1;samples.setdefault(cls,row)
    for r,items in enumerate(rounds):
        for slot,item in enumerate(items):
            check=int(item["check"][1:]) if item["check"].startswith("X") else 2+int(item["check"][1:])
            for delta in (1,2):
                obs=[0]*13;obs[check]=delta;action,guess=noise.classify_observed_syndrome(table,obs)
                cls=action if action.startswith("REFUSE") else "FALSE_CORRECTION_ATTEMPT"
                row={"kind":"COUPLING_ANCILLA_SHIFT","round":r,"slot":slot,"check":item["check"],"data_edge":item["data_edge"],"delta":delta,"class":cls,"guess":guess};rows.append(row);counts[cls]+=1;samples.setdefault(cls,row)
    return rows,counts,samples

def recode_locations():
    c=recode.verify();fc=c["fault_census"];per=fc["target_block_boundary_per_block"]
    counts=Counter()
    counts["BARE_HANDOFF_LOGICAL_MALIGNANT"]=fc["bare_handoff"].get("TARGET_ZERO_SYNDROME_LOGICAL",0)
    for k,v in per.items():counts[f"TARGET7_{k}"]=7*int(v)
    counts["SOURCE_DECODER_INTERNAL_UNRESOLVED_MACRO"]=1
    counts["TARGET_ENCODER_INTERNAL_UNRESOLVED_MACROS"]=7
    return c,counts

def verify(candidate_count=multi.DEFAULT_CANDIDATES):
    synrows,syncounts,synsamples=syndrome_location_faults(int(candidate_count));rounds,datarows,datacounts,datasamples=mapped_data_faults(int(candidate_count));rc,recounts=recode_locations()
    total_couplings=sum(len(x) for x in rounds)
    checks={
      "syndrome_prep_and_readout_locations_explicit":sum(1 for x in synrows if x["kind"] in {"ANCILLA_PREP","ANCILLA_READOUT"})==13*2*2,
      "every_weighted_SUM_has_two_ancilla_shift_faults":sum(1 for x in synrows if x["kind"]=="COUPLING_ANCILLA_SHIFT")==total_couplings*2,
      "every_weighted_SUM_has_eight_data_Pauli_faults":len(datarows)==total_couplings*8,
      "ambient_W33_faults_are_not_silently_projected":datacounts["AMBIENT_W33_PARENT_DECODER_REQUIRED"]>0,
      "naive_recode_has_exactly_56_malignant_handoff_faults":recounts["BARE_HANDOFF_LOGICAL_MALIGNANT"]==56,
      "target_postencode_single_faults_all_detected":recounts["TARGET7_postencode_DETECTABLE"]==7*40 and recounts["TARGET7_postencode_UNDETECTED"]==0,
      "internal_tableau_fault_locations_remain_explicitly_open":recounts["SOURCE_DECODER_INTERNAL_UNRESOLVED_MACRO"]==1 and recounts["TARGET_ENCODER_INTERNAL_UNRESOLVED_MACROS"]==7,
    }
    checks={k:bool(v) for k,v in checks.items()}
    return {
      "schema":"w33.qutrit-20-7-2-fault-location-census.v1","status":"PASS" if all(checks.values()) else "FAIL","checks":checks,
      "syndrome_locations":{"events":len(synrows),"classes":dict(syncounts),"samples":synsamples},
      "weighted_SUM_data_locations":{"couplings":total_couplings,"events":len(datarows),"classes":dict(datacounts),"samples":datasamples},
      "recode_locations":{"classes":dict(recounts),"decision":rc.get("decision")},
      "census_sha256":digest_json({"syndrome":synrows,"data":datarows,"recode":dict(recounts)}),
      "decision":"PHYSICAL_FT_REFUSED_AT_LOCATION_LEVEL",
      "theorem":"The current executable syndrome and recode architecture has an explicit single-fault location census. The naive recode contains 56 malignant bare-logical handoff faults, and many W33-edge coupling faults are outside the embedded 20-qutrit image and therefore require the parent W33 decoder rather than an invented projection.",
      "boundary":"The location census covers the current packet-level weighted-SUM transfer function and tableau boundaries. Elementary faults internal to the source/target tableau synthesis, correlated optical faults, loss dynamics and detector dead time remain open until a physical primitive sequence is supplied.",
    }
if __name__=="__main__":
    out=verify();print(json.dumps(out,indent=2));raise SystemExit(0 if out["status"]=="PASS" else 1)
