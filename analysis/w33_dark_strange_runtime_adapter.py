#!/usr/bin/env python3
"""Typed runtime adapter for the dark qutrit Strange channel.

The dark H27 multiplicity ray is
    |D> = (1,-omega,0)/sqrt(2) = Z X^2 |S>
with |S>=(0,1,-1)/sqrt(2) the repository's Strange reference.

Therefore the exact decode
    X Z^2 |D> = |S>
is Clifford-only. This file gives the dark channel its own runtime type:
    DARK_STRANGE_Q3_RAW -> STRANGE_Q3_RAW -> STRANGE_Q3_FIXED_POINT_VALIDATED.

The Pass416 five-qutrit code supplies only a fixed-point audit for Strange
(acceptance 1/36); it is not used here as a claimed production distiller.
Direct qutrit-T injection is refused because Strange and the HESSE_T_RAW
T-state are different resources. M36_Q4_RAW remains a separate ququart lane.
"""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/"analysis") not in sys.path:sys.path.insert(0,str(ROOT/"analysis"))
OUT=ROOT/"data/w33_dark_strange_runtime_adapter.json"

from w33_exact_eisenstein import ONE,OMEGA,ZERO,identity_matrix,matrix_multiply,omega_power

def matpow(A,n):
    out=identity_matrix(len(A))
    for _ in range(n):out=matrix_multiply(out,A)
    return out
def matvec(A,v):
    return [sum((A[i][j]*v[j] for j in range(len(v))),ZERO) for i in range(len(A))]
def digest(v):return "sha256:"+hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()

X=[[ZERO,ZERO,ONE],[ONE,ZERO,ZERO],[ZERO,ONE,ZERO]]
Z=[[ONE,ZERO,ZERO],[ZERO,OMEGA,ZERO],[ZERO,ZERO,omega_power(2)]]

def packet_schedule():
    rows=[]
    for tick in range(48):rows.append({"tick":tick,"region":"Q6_BODY"})
    roles=("DARK_TO_STRANGE_CLIFFORD_DECODE","STRANGE_FIXED_POINT_AUDIT","RESOURCE_HANDOFF_DECISION")
    tick=48
    for role in roles:
      for word_tick in range(8):
        rows.append({"tick":tick,"region":"DARK_STRANGE_EPILOGUE","role":role,"word_tick":word_tick});tick+=1
    assert tick==72
    return rows

def main(write=True):
    bridge=json.loads((ROOT/"data/w33_hesse36_dark_schrodinger_strange_state.json").read_text())
    p416=json.loads((ROOT/"data/w33_pass416_qutrit_distillation_search.json").read_text())
    sched=(ROOT/"analysis/w33_magic_resource_scheduler.py").read_text()
    m36=(ROOT/"analysis/bt2767_m36_factory.py").read_text()

    assert bridge["strange_bridge"]["exact_Clifford_word"]=="Z X^2"
    assert bridge["M36_firewall"]["same_resource_as_M36_Q4_RAW"] is False
    assert p416["reference_validation"]["Strange_state_definition"]=="(|1>-|2>)/sqrt(2)"
    assert p416["checks"]["strange_state_reference_fixed"] is True
    assert abs(p416["reference_validation"]["acceptance_probability"]-1/36)<1e-12
    assert 'HESSE_T_RAW=MagicResourceType("HESSE_T_RAW",3,"qutrit-T"' in sched
    assert "36 ququart/two-qubit Witting rays" in m36

    dark=[ONE,-OMEGA,ZERO]
    strange=[ZERO,ONE,-ONE]
    decode=matrix_multiply(X,matpow(Z,2))
    assert matvec(decode,dark)==strange

    schedule=packet_schedule()
    token_body={"resource":"DARK_STRANGE_Q3_RAW","state":["1","-omega","0"],"decode":"X Z^2","source":"rank73_dark8"}
    token=digest(token_body)

    out={
      "schema":"w33.dark_strange_runtime_adapter.v1",
      "status":"PASS_DARK_STRANGE_Q3_HAS_EXACT_CLIFFORD_RUNTIME_HANDOFF_WITH_T_AND_M36_FAIL_CLOSED",
      "headline":"The rank-73 dark magic ray is now operationally typed. DARK_STRANGE_Q3_RAW decodes exactly to the repository Strange reference by X Z^2, can enter the existing Strange fixed-point audit, and occupies a 24-tick epilogue in the 72-tick packet. Direct qutrit-T reservation is refused because the Strange and T resources are distinct, and M36_Q4_RAW remains a separate ququart/two-qubit resource.",
      "resource":{
        "type":"DARK_STRANGE_Q3_RAW",
        "dimension":3,
        "state_unnormalized":["1","-omega","0"],
        "token_id":token,
        "evidence_class":"EXACT_H27_DARK_RAY_AND_CLIFFORD_EQUIVALENCE"
      },
      "exact_handoff":{
        "target_type":"STRANGE_Q3_RAW",
        "reference_state_unnormalized":["0","1","-1"],
        "decode_word":"X Z^2",
        "identity":"X Z^2 (1,-omega,0)^T = (0,1,-1)^T",
        "Clifford_only":True
      },
      "validation":{
        "five_qutrit_reference_fixed_point":True,
        "pure_reference_acceptance_probability":"1/36",
        "meaning":"Pass416 fixed-point sanity check only; not promoted here to a Strange production/distillation threshold"
      },
      "packet":{
        "ticks":72,
        "body_ticks":48,
        "epilogue_ticks":24,
        "epilogue_roles":["DARK_TO_STRANGE_CLIFFORD_DECODE","STRANGE_FIXED_POINT_AUDIT","RESOURCE_HANDOFF_DECISION"]
      },
      "fail_closed":{
        "can_reserve_as_HESSE_T_RAW":False,
        "reason_T":"Strange-class magic is not the order-nine qutrit T-state resource used by the T teleportation port",
        "can_cast_to_M36_Q4_RAW":False,
        "reason_M36":"M36 is a four-dimensional ququart/two-qubit Witting resource",
        "fault_tolerant_injection_enabled":False
      },
      "physics_bridge":"Published qutrit magic-state literature contains dedicated Strange-state distillation protocols (including the 11-qutrit ternary Golay route), so the exact dark-to-Strange Clifford decode exposes a standard resource-theory handoff. No such external protocol is silently treated as implemented hardware here.",
      "boundary":"This operationalizes typing, exact Clifford conversion, packet scheduling, and fail-closed handoffs. It does not certify a physical Strange-state factory, a device threshold, or deterministic T-gate injection from the dark state.",
      "parents":[
        "data/w33_hesse36_dark_schrodinger_strange_state.json",
        "data/w33_pass416_qutrit_distillation_search.json",
        "analysis/w33_magic_resource_scheduler.py"
      ],
      "checks":{
        "dark_to_Strange_decode_exact":True,
        "decode_is_Clifford":True,
        "Pass416_Strange_fixed_point_loaded":True,
        "packet_48_plus_24":True,
        "T_crosscast_refused":True,
        "M36_crosscast_refused":True,
        "FT_injection_remains_disabled":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":
    print(json.dumps(main(True),indent=2))
