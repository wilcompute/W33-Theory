#!/usr/bin/env python3
"""Typed non-Clifford resource scheduler for the W33/Holonet packet machine.

Fault-tolerant admission now has six independent gates:
  1. external [[20,7,2]]_3 code verified;
  2. exact W33 symplectic encoding;
  3. explicit optical candidate compiler for W33-local primitives;
  4. measured hardware calibration for those optical primitives;
  5. mapped decoder + circuit-level syndrome fault census;
  6. hardware-calibrated physical threshold certificate.

The software/compiler gates can close without manufacturing physical evidence.
FAULT_TOLERANT reservations remain refused until the measured gates close.
"""
from __future__ import annotations
from dataclasses import asdict,dataclass
import hashlib,json
from typing import Any
import w33_qutrit_t_teleportation_port as tport
import w33_qutrit_20_7_2_adapter_attack as adapter2072

def canonical(value:Any)->bytes:return json.dumps(value,sort_keys=True,separators=(",",":")).encode()
def digest(value:Any)->str:return "sha256:"+hashlib.sha256(canonical(value)).hexdigest()

@dataclass(frozen=True)
class MagicResourceType:
    name:str; dimension:int; logical_gate:str; fault_tolerant:bool; evidence_class:str
HESSE_T_RAW=MagicResourceType("HESSE_T_RAW",3,"qutrit-T",False,"EXACT_STATEVECTOR_AND_PACKET_ABI")

@dataclass(frozen=True)
class FTAdapter:
    name:str; code_parameters:str; external_code_verified:bool; encoding_map_verified:bool
    optical_compiler_verified:bool; hardware_calibration_verified:bool; decoder_verified:bool
    circuit_noise_verified:bool; threshold_certificate_verified:bool; audit_digest:str
    source_class:str="EXTERNAL_PRIOR_ART_CANDIDATE"
    @property
    def enabled(self)->bool:
        return all((self.external_code_verified,self.encoding_map_verified,self.optical_compiler_verified,
                    self.hardware_calibration_verified,self.decoder_verified,self.circuit_noise_verified,
                    self.threshold_certificate_verified))

@dataclass(frozen=True)
class MagicToken:
    token_id:str; resource_type:str; factory_batch:str; audit_digest:str
@dataclass(frozen=True)
class Reservation:
    reservation_id:str; token_id:str; packet_index:int; microframe_tick:int; logical_gate:str; assurance:str

class MagicFactoryScheduler:
    def __init__(self):self.inventory={};self.reserved=set();self.reservations=[];self.adapters={}
    def register_adapter(self,adapter):self.adapters[adapter.name]=adapter
    def mint_raw(self,count,factory_batch,audit_digest):
        if count<0 or not audit_digest.startswith("sha256:"):raise ValueError("invalid magic factory mint")
        out=[]
        for i in range(count):
            tid=digest({"resource":HESSE_T_RAW.name,"batch":factory_batch,"index":i,"audit":audit_digest})
            tok=MagicToken(tid,HESSE_T_RAW.name,factory_batch,audit_digest);self.inventory[tid]=tok;out.append(tok)
        return out
    def _free_raw(self):
        free=sorted(k for k in self.inventory if k not in self.reserved)
        if not free:raise RuntimeError("no unreserved HESSE_T_RAW token available")
        return self.inventory[free[0]]
    def reserve_t(self,packet_index,assurance="EXACT_LOGICAL"):
        if packet_index<0:raise ValueError("packet index must be nonnegative")
        if assurance not in {"EXACT_LOGICAL","FAULT_TOLERANT"}:raise ValueError("unknown assurance class")
        if assurance=="FAULT_TOLERANT" and not any(a.enabled for a in self.adapters.values()):raise PermissionError("fault-tolerant T reservation refused: W33 FT evidence gates incomplete")
        token=self._free_raw();self.reserved.add(token.token_id);tick=packet_index*72+48
        body={"token":token.token_id,"packet_index":packet_index,"microframe_tick":tick,"logical_gate":"qutrit-T","assurance":assurance}
        row=Reservation(digest(body),token.token_id,packet_index,tick,"qutrit-T",assurance);self.reservations.append(row);return row
    def consume(self,reservation_id):
        row=next((r for r in self.reservations if r.reservation_id==reservation_id),None)
        if row is None:raise KeyError("unknown reservation")
        token=self.inventory.pop(row.token_id,None)
        if token is None:raise PermissionError("magic token already consumed")
        self.reserved.discard(row.token_id);return token
    def cancel(self,reservation_id):
        row=next((r for r in self.reservations if r.reservation_id==reservation_id),None)
        if row is None:raise KeyError("unknown reservation")
        self.reserved.discard(row.token_id);self.reservations=[r for r in self.reservations if r.reservation_id!=reservation_id]
    def snapshot(self):return {"inventory":sorted(self.inventory),"reserved":sorted(self.reserved),"reservations":[asdict(r) for r in self.reservations],"adapters":{k:asdict(v)|{"enabled":v.enabled} for k,v in sorted(self.adapters.items())}}

def adapter_from_audit(audit):
    checks=audit.get("checks",{});repo=audit.get("w33_adapter_audit",{})
    external=audit.get("status")=="PASS" and checks.get("published_puncture_gives_9x20_matrix") is True and checks.get("css_encodes_7_qutrits") is True and checks.get("weight2_Z_logical_exists") is True
    return FTAdapter(
        name="QUTRIT_TRIORTHOGONAL_20_7_2",code_parameters="[[20,7,2]]_3",external_code_verified=external,
        encoding_map_verified=repo.get("general_nonlocal_symplectic_embedding_verified") is True,
        optical_compiler_verified=repo.get("locality_optical_compiler_verified") is True,
        hardware_calibration_verified=repo.get("optical_hardware_calibration_verified") is True,
        decoder_verified=repo.get("mapped_packet_decoder_verified") is True,
        circuit_noise_verified=repo.get("circuit_level_syndrome_noise_verified") is True,
        threshold_certificate_verified=repo.get("mapped_threshold_certificate_present") is True,
        audit_digest=digest(audit))

def verify():
    teleport=tport.verify();code_audit=adapter2072.verify();audit_digest=digest({"tport_status":teleport.get("status"),"checks":teleport.get("checks",{})})
    sched=MagicFactoryScheduler();tokens=sched.mint_raw(2,"batch-demo",audit_digest);r0=sched.reserve_t(0);r1=sched.reserve_t(1)
    overbook=False
    try:sched.reserve_t(2)
    except RuntimeError:overbook=True
    candidate=adapter_from_audit(code_audit);sched.register_adapter(candidate);repo=code_audit.get("w33_adapter_audit",{})
    ft_refused=False
    try:sched.cancel(r1.reservation_id);sched.reserve_t(2,"FAULT_TOLERANT")
    except PermissionError:ft_refused=True
    consumed=sched.consume(r0.reservation_id);double=False
    try:sched.consume(r0.reservation_id)
    except PermissionError:double=True
    snap=sched.snapshot()
    checks={
      "exact_t_port_certificate_passes":teleport.get("status")=="PASS",
      "external_20_7_2_code_reconstruction_passes":code_audit.get("status")=="PASS" and candidate.external_code_verified,
      "symplectic_encoding_gate_is_closed":candidate.encoding_map_verified,
      "optical_candidate_compiler_gate_is_closed":candidate.optical_compiler_verified,
      "hardware_calibration_gate_remains_open":not candidate.hardware_calibration_verified,
      "mapped_decoder_gate_is_closed":candidate.decoder_verified,
      "circuit_noise_gate_is_closed":candidate.circuit_noise_verified,
      "pseudothreshold_is_not_promoted_to_physical_threshold":repo.get("mapped_pseudothreshold_experiment_verified") is True and not candidate.threshold_certificate_verified,
      "threshold_gate_remains_open":not candidate.threshold_certificate_verified,
      "distance3_store_bridge_is_recorded":repo.get("protected_66_store_bridge_verified") is True,
      "standard_K12_k8_no_go_is_recorded":repo.get("standard_K12_surface_code_k8_no_go") is True,
      "adapter_status_is_derived_from_executable_audit":candidate.audit_digest==digest(code_audit),
      "raw_tokens_content_addressed":len(tokens)==2 and all(t.token_id.startswith("sha256:") for t in tokens),
      "packet_slots_are_72_tick_aligned":r0.microframe_tick==48 and r1.microframe_tick==120,
      "inventory_cannot_be_overbooked":overbook,"ft_candidate_remains_fail_closed":ft_refused and not candidate.enabled,
      "reservation_consumes_exact_token":consumed.token_id==r0.token_id,"token_double_spend_blocked":double,
      "scheduler_keeps_assurance_explicit":all(r["assurance"] in {"EXACT_LOGICAL","FAULT_TOLERANT"} for r in snap["reservations"]),
    }
    return {"schema":"w33.magic-resource-scheduler.v5","status":"PASS" if all(checks.values()) else "FAIL","checks":checks,
            "candidate_adapter":asdict(candidate)|{"enabled":candidate.enabled},"adapter_audit_decision":code_audit.get("decision"),
            "interpretation":"The optical candidate compiler and circuit-level decoder/noise gates now close in software. FAULT_TOLERANT T scheduling remains refused because measured optical calibration and a hardware-calibrated physical threshold certificate remain absent. The explicit Pass79 distance-3 store bridge is recorded separately from the standard K12 k=12 no-go."}

if __name__=="__main__":
    payload=verify();print(json.dumps(payload,indent=2));raise SystemExit(0 if payload["status"]=="PASS" else 1)
