#!/usr/bin/env python3
"""Typed non-Clifford resource scheduler for the W33/Holonet packet machine.

FAULT_TOLERANT reservations require executable code/embedding/optics/decoder
checks plus the physical evidence gates: accepted W33 device calibration,
physical threshold, location-level fault coverage, and a fault-tolerant encoded
20->66 recode with no bare-logical window.  The current naive recode is proved
non-FT, so scheduling remains fail-closed.
"""
from __future__ import annotations
from dataclasses import asdict,dataclass
import hashlib,json
from typing import Any
import w33_qutrit_t_teleportation_port as tport
import w33_qutrit_20_7_2_adapter_attack as adapter2072
def canonical(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":")).encode()
def digest(v:Any)->str:return "sha256:"+hashlib.sha256(canonical(v)).hexdigest()
@dataclass(frozen=True)
class MagicResourceType:name:str;dimension:int;logical_gate:str;fault_tolerant:bool;evidence_class:str
HESSE_T_RAW=MagicResourceType("HESSE_T_RAW",3,"qutrit-T",False,"EXACT_STATEVECTOR_AND_PACKET_ABI")
@dataclass(frozen=True)
class FTAdapter:
    name:str;code_parameters:str;external_code_verified:bool;encoding_map_verified:bool;optical_compiler_verified:bool;hardware_calibration_verified:bool;decoder_verified:bool;circuit_noise_verified:bool;fault_location_verified:bool;threshold_certificate_verified:bool;physical_recode_verified:bool;audit_digest:str
    @property
    def enabled(self):return all((self.external_code_verified,self.encoding_map_verified,self.optical_compiler_verified,self.hardware_calibration_verified,self.decoder_verified,self.circuit_noise_verified,self.fault_location_verified,self.threshold_certificate_verified,self.physical_recode_verified))
@dataclass(frozen=True)
class MagicToken:token_id:str;resource_type:str;factory_batch:str;audit_digest:str
@dataclass(frozen=True)
class Reservation:reservation_id:str;token_id:str;packet_index:int;microframe_tick:int;logical_gate:str;assurance:str
class MagicFactoryScheduler:
    def __init__(self):self.inventory={};self.reserved=set();self.reservations=[];self.adapters={}
    def register_adapter(self,a):self.adapters[a.name]=a
    def mint_raw(self,count,batch,audit):
        if count<0 or not audit.startswith("sha256:"):raise ValueError("invalid mint")
        out=[]
        for i in range(count):
            tid=digest({"resource":HESSE_T_RAW.name,"batch":batch,"index":i,"audit":audit});tok=MagicToken(tid,HESSE_T_RAW.name,batch,audit);self.inventory[tid]=tok;out.append(tok)
        return out
    def _free_raw(self):
        f=sorted(k for k in self.inventory if k not in self.reserved)
        if not f:raise RuntimeError("no unreserved HESSE_T_RAW token available")
        return self.inventory[f[0]]
    def reserve_t(self,packet_index,assurance="EXACT_LOGICAL"):
        if packet_index<0:raise ValueError("packet index")
        if assurance not in {"EXACT_LOGICAL","FAULT_TOLERANT"}:raise ValueError("assurance")
        if assurance=="FAULT_TOLERANT" and not any(a.enabled for a in self.adapters.values()):raise PermissionError("fault-tolerant T reservation refused: evidence gates incomplete")
        tok=self._free_raw();self.reserved.add(tok.token_id);tick=packet_index*72+48;body={"token":tok.token_id,"packet_index":packet_index,"microframe_tick":tick,"logical_gate":"qutrit-T","assurance":assurance};r=Reservation(digest(body),tok.token_id,packet_index,tick,"qutrit-T",assurance);self.reservations.append(r);return r
    def consume(self,rid):
        r=next((x for x in self.reservations if x.reservation_id==rid),None)
        if r is None:raise KeyError("unknown reservation")
        tok=self.inventory.pop(r.token_id,None)
        if tok is None:raise PermissionError("magic token already consumed")
        self.reserved.discard(r.token_id);return tok
    def cancel(self,rid):
        r=next((x for x in self.reservations if x.reservation_id==rid),None)
        if r is None:raise KeyError("unknown reservation")
        self.reserved.discard(r.token_id);self.reservations=[x for x in self.reservations if x.reservation_id!=rid]
    def snapshot(self):return {"inventory":sorted(self.inventory),"reserved":sorted(self.reserved),"reservations":[asdict(r) for r in self.reservations],"adapters":{k:asdict(v)|{"enabled":v.enabled} for k,v in self.adapters.items()}}
def adapter_from_audit(audit):
    checks=audit.get("checks",{});r=audit.get("w33_adapter_audit",{});external=audit.get("status")=="PASS" and checks.get("published_puncture_gives_9x20_matrix") is True and checks.get("css_encodes_7_qutrits") is True and checks.get("weight2_Z_logical_exists") is True
    return FTAdapter("QUTRIT_TRIORTHOGONAL_20_7_2","[[20,7,2]]_3",external,r.get("general_nonlocal_symplectic_embedding_verified") is True,r.get("locality_optical_compiler_verified") is True,r.get("optical_hardware_calibration_verified") is True,r.get("mapped_packet_decoder_verified") is True,r.get("circuit_level_syndrome_noise_verified") is True,r.get("fault_location_census_verified") is True,r.get("mapped_threshold_certificate_present") is True,r.get("physical_20_to_66_recode_verified") is True,digest(audit))
def verify():
    teleport=tport.verify();audit=adapter2072.verify();ad=adapter_from_audit(audit);d=digest({"t":teleport.get("status")});s=MagicFactoryScheduler();tokens=s.mint_raw(2,"batch-demo",d);r0=s.reserve_t(0);r1=s.reserve_t(1);over=False
    try:s.reserve_t(2)
    except RuntimeError:over=True
    s.register_adapter(ad);repo=audit.get("w33_adapter_audit",{});refused=False
    try:s.cancel(r1.reservation_id);s.reserve_t(2,"FAULT_TOLERANT")
    except PermissionError:refused=True
    used=s.consume(r0.reservation_id);double=False
    try:s.consume(r0.reservation_id)
    except PermissionError:double=True
    checks={"exact_t_port_certificate_passes":teleport.get("status")=="PASS","external_code_passes":ad.external_code_verified,"symplectic_encoding_closed":ad.encoding_map_verified,"optical_compiler_closed":ad.optical_compiler_verified,"decoder_closed":ad.decoder_verified,"circuit_noise_closed":ad.circuit_noise_verified,"fault_location_census_closed":ad.fault_location_verified,"K12_native_gauge_fixed_code_recorded":repo.get("K12_native_gauge_fixed_66_8_3_verified") is True,"naive_recode_no_go_recorded":repo.get("naive_recode_FT_no_go_verified") is True,"hardware_calibration_currently_open":not ad.hardware_calibration_verified,"physical_threshold_currently_open":not ad.threshold_certificate_verified,"physical_encoded_recode_currently_open":not ad.physical_recode_verified,"inventory_cannot_be_overbooked":over,"ft_candidate_remains_fail_closed":refused and not ad.enabled,"token_double_spend_blocked":double,"reservation_consumes_exact_token":used.token_id==r0.token_id,"raw_tokens_content_addressed":len(tokens)==2}
    checks={k:bool(v) for k,v in checks.items()}
    return {"schema":"w33.magic-resource-scheduler.v6","status":"PASS" if all(checks.values()) else "FAIL","checks":checks,"candidate_adapter":asdict(ad)|{"enabled":ad.enabled},"adapter_audit_decision":audit.get("decision"),"interpretation":"Software gates, native K12 gauge-fixed [[66,8,3]]_3, and the naive-recode no-go are recorded. FT magic scheduling remains refused until actual W33 calibration, physical threshold, and an encoded no-bare-window recode all verify."}
if __name__=="__main__":
    out=verify();print(json.dumps(out,indent=2));raise SystemExit(0 if out["status"]=="PASS" else 1)
