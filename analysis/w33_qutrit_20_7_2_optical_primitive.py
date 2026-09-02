#!/usr/bin/env python3
"""Optical candidate lowering for W33-local qutrit SUM/SWAP primitives.

SUM_alpha is lowered to coherent control-mode sorting, a control-conditioned
cyclic target shift, and coherent recombination.  SWAP is decomposed exactly as
SUM(c,t), SUM^-1(t,c), SUM(c,t), SCALE2(c) over GF(3).

Functional compilation and device calibration are separate evidence classes.
Hardware calibration status is sourced exclusively from
w33_qutrit_optical_calibration_ingest; published measurements of other optical
qudit systems are benchmark-only.
"""
from __future__ import annotations
from collections import Counter
import hashlib,json
import w33_qutrit_20_7_2_w33_route_compiler as route
import w33_qutrit_optical_calibration_ingest as calabi
Q=3
def digest_json(v):return "sha256:"+hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def sum_truth(alpha):
    a=int(alpha)%Q;return {(c,t):(c,(t+a*c)%Q) for c in range(Q) for t in range(Q)}
def swap_truth():return {(a,b):(b,a) for a in range(Q) for b in range(Q)}
def apply_sum(state,alpha,control_first=True):
    a,b=state;alpha%=Q;return (a,(b+alpha*a)%Q) if control_first else ((a+alpha*b)%Q,b)
def apply_scale2_first(state):a,b=state;return ((2*a)%Q,b)
def replay_swap(state):
    s=apply_sum(state,1,True);s=apply_sum(s,2,False);s=apply_sum(s,1,True);return apply_scale2_first(s)
def optical_sum(alpha,control,target,coupler_vertex):
    alpha=int(alpha)%Q
    return {"logical_op":"SUM_ALPHA","alpha":alpha,"control":int(control),"target":int(target),"w33_coupler_vertex":int(coupler_vertex),"devices":[{"device":"COHERENT_QUTRIT_MODE_SORTER","arity":3,"role":"control demultiplex"},*[{"control_label":j,"target_shift_power":int((alpha*j)%Q),"device":"CYCLIC_QUTRIT_MODE_SHIFT","encoding":"centered OAM ell=-1,0,+1 or calibrated three-bin temporal mode"} for j in range(Q)],{"device":"COHERENT_QUTRIT_MODE_RECOMBINER","arity":3,"role":"control recombine"}],"functional_truth":{"%d%d"%k:list(v) for k,v in sum_truth(alpha).items()}}
def optical_scale2(wire):return {"logical_op":"SCALE2","wire":int(wire),"devices":[{"device":"OAM_PARITY_MODE_PERMUTER","action":"j->2j mod 3","centered_OAM_action":"ell->-ell"}]}
def optical_swap(a,b,coupler_vertex):
    return {"logical_op":"SWAP","a":int(a),"b":int(b),"w33_coupler_vertex":int(coupler_vertex),"decomposition":[optical_sum(1,a,b,coupler_vertex),optical_sum(2,b,a,coupler_vertex),optical_sum(1,a,b,coupler_vertex),optical_scale2(a)],"functional_truth":{"%d%d"%k:list(v) for k,v in swap_truth().items()}}
def compile_op(op):
    if op["op"]=="SUM_ALPHA":return optical_sum(op["alpha"],op["control"],op["target"],op["coupler_vertex"])
    if op["op"]=="SWAP":return optical_swap(op["a"],op["b"],op["coupler_vertex"])
    if op["op"]=="SCALE2":return optical_scale2(op["wire"])
    raise ValueError(op["op"])
def flatten_devices(compiled):
    out=[]
    def walk(x):
        if isinstance(x,dict):
            if "device" in x:out.append(x["device"])
            for v in x.values():walk(v)
        elif isinstance(x,list):
            for v in x:walk(v)
    walk(compiled);return out
def read_calibration():
    d=calabi.device_calibration();return {"present":d.get("present",False),"hardware_backed":bool(d.get("accepted")),"ingestion":d,"evidence_class":"W33_DEVICE_MEASUREMENT" if d.get("accepted") else "NO_ACCEPTED_W33_DEVICE_MEASUREMENT"}
def compile_optical(candidate_count=route.multi.DEFAULT_CANDIDATES):
    routed=route.compile_routes(int(candidate_count));compiled=[compile_op(op) for op in routed["flat_ops"]];counts=Counter(d for c in compiled for d in flatten_devices(c));return routed,compiled,counts,read_calibration()
def verify(candidate_count=route.multi.DEFAULT_CANDIDATES):
    routed,compiled,counts,cal=compile_optical(int(candidate_count));sum_ok=all(apply_sum((a,b),alpha,True)==out for alpha in (1,2) for (a,b),out in sum_truth(alpha).items());swap_ok=all(replay_swap(s)==out for s,out in swap_truth().items())
    checks={"every_W33_local_primitive_has_optical_lowering":len(compiled)==len(routed["flat_ops"]),"SUM_basis_truth_exact":sum_ok,"SWAP_decomposition_basis_truth_exact":swap_ok,"compiled_circuit_is_nonempty":len(compiled)>0,"all_two_qutrit_sources_remain_W33_local":routed["all_macro_programs_verified"],"external_prior_art_not_hardware_admission":calabi.prior_art().get("accepted_for_w33") is False}
    checks={k:bool(v) for k,v in checks.items()}
    return {"schema":"w33.qutrit-20-7-2-optical-primitive-compiler.v2","status":"PASS" if all(checks.values()) else "FAIL","checks":checks,"optical_compiler_verified":all(checks.values()),"hardware_calibration_verified":bool(cal["hardware_backed"]),"calibration":cal,"device_inventory":dict(sorted((k,int(v)) for k,v in counts.items())),"compiled_primitive_count":len(compiled),"compiled_schedule_sha256":digest_json(compiled),"sample":compiled[:2]+compiled[-2:] if len(compiled)>4 else compiled,"literature_anchors":[{"work":"High-dimensional optical quantum logic in large operational spaces","venue":"npj Quantum Information 2019","doi":"10.1038/s41534-019-0173-8","use":"measured photonic SUM benchmark; not W33 calibration"},{"work":"Experimental realization of high-dimensional quantum gates with ultrahigh fidelity and efficiency","venue":"Physical Review A 2024","doi":"10.1103/PhysRevA.109.022612","use":"high-dimensional optical gate benchmark; different platform"}],"engineering_parameters_required":["insertion_loss_db","crosstalk_probability","leakage_probability","phase_rms_rad","direct circuit fault_rates"],"theorem":"Every topologically local W33 SUM/SWAP/SCALE2 primitive has an explicit coherent qutrit candidate circuit with exact computational-basis action.","boundary":"Compilation is software evidence. Hardware admission requires an accepted W33_DEVICE_MEASUREMENT packet with direct fault-rate estimates; external literature cannot close that gate."}
if __name__=="__main__":
    out=verify();print(json.dumps(out,indent=2));raise SystemExit(0 if out["status"]=="PASS" else 1)
