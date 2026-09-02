#!/usr/bin/env python3
"""Typed non-Clifford resource scheduler for the W33/Holonet packet machine.

The scheduler now treats fault-tolerance evidence as four independent gates:
  1. an exact W33 encoding/intertwiner;
  2. a locality/optical compilation certificate for that encoding;
  3. a mapped syndrome/decoder implementation;
  4. a mapped noise/threshold certificate.

The general nonlocal [[20,7,2]]_3 -> [[240,81,3]]_3 symplectic embedding now
closes gate (1), but the scheduler intentionally keeps FAULT_TOLERANT assurance
refused until the other three gates close.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
import hashlib, json
from typing import Any
import w33_qutrit_t_teleportation_port as tport
import w33_qutrit_20_7_2_adapter_attack as adapter2072

def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()

def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()

@dataclass(frozen=True)
class MagicResourceType:
    name: str
    dimension: int
    logical_gate: str
    fault_tolerant: bool
    evidence_class: str

HESSE_T_RAW = MagicResourceType("HESSE_T_RAW", 3, "qutrit-T", False, "EXACT_STATEVECTOR_AND_PACKET_ABI")

@dataclass(frozen=True)
class FTAdapter:
    name: str
    code_parameters: str
    external_code_verified: bool
    encoding_map_verified: bool
    locality_compiler_verified: bool
    decoder_verified: bool
    threshold_certificate_verified: bool
    audit_digest: str
    source_class: str = "EXTERNAL_PRIOR_ART_CANDIDATE"

    @property
    def enabled(self) -> bool:
        return all((
            self.external_code_verified,
            self.encoding_map_verified,
            self.locality_compiler_verified,
            self.decoder_verified,
            self.threshold_certificate_verified,
        ))

@dataclass(frozen=True)
class MagicToken:
    token_id: str
    resource_type: str
    factory_batch: str
    audit_digest: str

@dataclass(frozen=True)
class Reservation:
    reservation_id: str
    token_id: str
    packet_index: int
    microframe_tick: int
    logical_gate: str
    assurance: str

class MagicFactoryScheduler:
    def __init__(self) -> None:
        self.inventory: dict[str, MagicToken] = {}
        self.reserved: set[str] = set()
        self.reservations: list[Reservation] = []
        self.adapters: dict[str, FTAdapter] = {}

    def register_adapter(self, adapter: FTAdapter) -> None:
        self.adapters[adapter.name] = adapter

    def mint_raw(self, count: int, factory_batch: str, audit_digest: str) -> list[MagicToken]:
        if count < 0 or not audit_digest.startswith("sha256:"):
            raise ValueError("invalid magic factory mint")
        out=[]
        for i in range(count):
            tid=digest({"resource":HESSE_T_RAW.name,"batch":factory_batch,"index":i,"audit":audit_digest})
            tok=MagicToken(tid,HESSE_T_RAW.name,factory_batch,audit_digest)
            self.inventory[tid]=tok; out.append(tok)
        return out

    def _free_raw(self) -> MagicToken:
        free=sorted(k for k in self.inventory if k not in self.reserved)
        if not free: raise RuntimeError("no unreserved HESSE_T_RAW token available")
        return self.inventory[free[0]]

    def reserve_t(self, packet_index: int, assurance: str = "EXACT_LOGICAL") -> Reservation:
        if packet_index < 0: raise ValueError("packet index must be nonnegative")
        if assurance not in {"EXACT_LOGICAL","FAULT_TOLERANT"}: raise ValueError("unknown assurance class")
        if assurance == "FAULT_TOLERANT" and not any(a.enabled for a in self.adapters.values()):
            raise PermissionError("fault-tolerant T reservation refused: W33 FT evidence gates incomplete")
        token=self._free_raw(); self.reserved.add(token.token_id)
        tick=packet_index*72+48
        body={"token":token.token_id,"packet_index":packet_index,"microframe_tick":tick,"logical_gate":"qutrit-T","assurance":assurance}
        row=Reservation(digest(body),token.token_id,packet_index,tick,"qutrit-T",assurance)
        self.reservations.append(row); return row

    def consume(self, reservation_id: str) -> MagicToken:
        row=next((r for r in self.reservations if r.reservation_id==reservation_id),None)
        if row is None: raise KeyError("unknown reservation")
        token=self.inventory.pop(row.token_id,None)
        if token is None: raise PermissionError("magic token already consumed")
        self.reserved.discard(row.token_id); return token

    def cancel(self, reservation_id: str) -> None:
        row=next((r for r in self.reservations if r.reservation_id==reservation_id),None)
        if row is None: raise KeyError("unknown reservation")
        self.reserved.discard(row.token_id)
        self.reservations=[r for r in self.reservations if r.reservation_id!=reservation_id]

    def snapshot(self) -> dict[str,Any]:
        return {"inventory":sorted(self.inventory),"reserved":sorted(self.reserved),"reservations":[asdict(r) for r in self.reservations],"adapters":{k:asdict(v)|{"enabled":v.enabled} for k,v in sorted(self.adapters.items())}}

def adapter_from_audit(audit: dict[str,Any]) -> FTAdapter:
    checks=audit.get("checks",{}); repo=audit.get("w33_adapter_audit",{})
    external=(audit.get("status")=="PASS" and checks.get("published_puncture_gives_9x20_matrix") is True and checks.get("css_encodes_7_qutrits") is True and checks.get("weight2_Z_logical_exists") is True)
    return FTAdapter(
        name="QUTRIT_TRIORTHOGONAL_20_7_2",
        code_parameters="[[20,7,2]]_3",
        external_code_verified=external,
        encoding_map_verified=repo.get("general_nonlocal_symplectic_embedding_verified") is True,
        locality_compiler_verified=repo.get("locality_optical_compiler_verified") is True,
        decoder_verified=repo.get("mapped_packet_decoder_present") is True,
        threshold_certificate_verified=repo.get("mapped_threshold_certificate_present") is True,
        audit_digest=digest(audit),
    )

def verify() -> dict[str,Any]:
    teleport=tport.verify(); code_audit=adapter2072.verify()
    audit_digest=digest({"tport_status":teleport.get("status"),"checks":teleport.get("checks",{})})
    sched=MagicFactoryScheduler(); tokens=sched.mint_raw(2,"batch-demo",audit_digest)
    r0=sched.reserve_t(0,"EXACT_LOGICAL"); r1=sched.reserve_t(1,"EXACT_LOGICAL")
    overbook=False
    try: sched.reserve_t(2,"EXACT_LOGICAL")
    except RuntimeError: overbook=True
    candidate=adapter_from_audit(code_audit); sched.register_adapter(candidate)
    ft_refused=False
    try:
        sched.cancel(r1.reservation_id); sched.reserve_t(2,"FAULT_TOLERANT")
    except PermissionError: ft_refused=True
    consumed=sched.consume(r0.reservation_id)
    double=False
    try: sched.consume(r0.reservation_id)
    except PermissionError: double=True
    snap=sched.snapshot()
    checks={
      "exact_t_port_certificate_passes":teleport.get("status")=="PASS",
      "external_20_7_2_code_reconstruction_passes":code_audit.get("status")=="PASS" and candidate.external_code_verified,
      "nonlocal_symplectic_encoding_gate_is_closed":candidate.encoding_map_verified,
      "locality_gate_remains_open":not candidate.locality_compiler_verified,
      "decoder_gate_remains_open":not candidate.decoder_verified,
      "threshold_gate_remains_open":not candidate.threshold_certificate_verified,
      "adapter_status_is_derived_from_executable_audit":candidate.audit_digest==digest(code_audit),
      "raw_tokens_content_addressed":len(tokens)==2 and all(t.token_id.startswith("sha256:") for t in tokens),
      "packet_slots_are_72_tick_aligned":r0.microframe_tick==48 and r1.microframe_tick==120,
      "inventory_cannot_be_overbooked":overbook,
      "ft_candidate_remains_fail_closed":ft_refused and not candidate.enabled,
      "reservation_consumes_exact_token":consumed.token_id==r0.token_id,
      "token_double_spend_blocked":double,
      "scheduler_keeps_assurance_explicit":all(r["assurance"] in {"EXACT_LOGICAL","FAULT_TOLERANT"} for r in snap["reservations"]),
    }
    return {
      "schema":"w33.magic-resource-scheduler.v3",
      "status":"PASS" if all(checks.values()) else "FAIL",
      "checks":checks,
      "candidate_adapter":asdict(candidate)|{"enabled":candidate.enabled},
      "adapter_audit_decision":code_audit.get("decision"),
      "interpretation":"The exact nonlocal W33 symplectic encoding now closes the encoding gate. FAULT_TOLERANT T scheduling remains refused because locality/optical compilation, the mapped decoder, and the mapped threshold certificate are still absent.",
    }

if __name__=="__main__":
    payload=verify(); print(json.dumps(payload,indent=2)); raise SystemExit(0 if payload["status"]=="PASS" else 1)
