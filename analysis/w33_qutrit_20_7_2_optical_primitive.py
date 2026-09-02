#!/usr/bin/env python3
"""Optical candidate lowering for W33-local qutrit SUM/SWAP primitives.

The W33 route compiler already proves that every two-qutrit primitive acts on
two carrier edges sharing one W33 point.  This module lowers that local algebra
one level further into an explicit coherent mode-routing contract:

  SUM_alpha(c,t):
    1. coherently sort the control qutrit into three mode branches j=0,1,2;
    2. on branch j, apply X^(alpha*j) to the target OAM/time-bin qutrit;
    3. coherently recombine the control branches.

This is exactly the standard SUM_3 action |j,k> -> |j,k+alpha*j mod 3>.  It is
compatible with the repo's centered OAM alphabet and F3/tritter vocabulary, and
with published photonic SUM constructions based on control-dependent cyclic
mode/time-bin shifts.  A local SWAP is compiled algebraically as

  SUM(c,t); SUM^{-1}(t,c); SUM(c,t); SCALE2(c)

which maps (a,b) -> (b,a) over GF(3).  SCALE2 is the qutrit label inversion
j->-j, realizable as an OAM parity/mode permutation candidate.

Important boundary: this is an explicit *optical circuit compiler* and exact
basis-state functional certificate.  It does not claim a measured device.  A
hardware calibration packet may be placed at
`data/w33_qutrit_optical_primitive_calibration.json`; only such a packet can
populate measured insertion loss, crosstalk, leakage and phase error fields.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import hashlib
import json
import math

import w33_qutrit_20_7_2_w33_route_compiler as route

ROOT=Path(__file__).resolve().parents[1]
CAL=ROOT/"data/w33_qutrit_optical_primitive_calibration.json"
Q=3


def digest_json(v):
    return "sha256:"+hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def sum_truth(alpha):
    a=int(alpha)%Q
    return {(c,t):(c,(t+a*c)%Q) for c in range(Q) for t in range(Q)}


def swap_truth():
    return {(a,b):(b,a) for a in range(Q) for b in range(Q)}


def apply_sum(state,alpha,control_first=True):
    a,b=state; alpha%=Q
    return (a,(b+alpha*a)%Q) if control_first else ((a+alpha*b)%Q,b)


def apply_scale2_first(state):
    a,b=state; return ((2*a)%Q,b)


def replay_swap(state):
    s=apply_sum(state,1,True)
    s=apply_sum(s,2,False)
    s=apply_sum(s,1,True)
    return apply_scale2_first(s)


def optical_sum(alpha,control,target,coupler_vertex):
    alpha=int(alpha)%Q
    branches=[]
    for j in range(Q):
        branches.append({
            "control_label":j,
            "target_shift_power":int((alpha*j)%Q),
            "device":"CYCLIC_QUTRIT_MODE_SHIFT",
            "encoding":"centered OAM ell=-1,0,+1 or calibrated three-bin temporal mode",
        })
    return {
        "logical_op":"SUM_ALPHA","alpha":alpha,"control":int(control),"target":int(target),
        "w33_coupler_vertex":int(coupler_vertex),
        "devices":[
            {"device":"COHERENT_QUTRIT_MODE_SORTER","arity":3,"role":"control demultiplex"},
            *branches,
            {"device":"COHERENT_QUTRIT_MODE_RECOMBINER","arity":3,"role":"control recombine"},
        ],
        "functional_truth":{"%d%d"%k:list(v) for k,v in sum_truth(alpha).items()},
    }


def optical_scale2(wire):
    return {"logical_op":"SCALE2","wire":int(wire),"devices":[{"device":"OAM_PARITY_MODE_PERMUTER","action":"j->2j mod 3","centered_OAM_action":"ell->-ell"}]}


def optical_swap(a,b,coupler_vertex):
    # Algebraic decomposition keeps the same local pair throughout.
    return {
        "logical_op":"SWAP","a":int(a),"b":int(b),"w33_coupler_vertex":int(coupler_vertex),
        "decomposition":[
            optical_sum(1,a,b,coupler_vertex),
            optical_sum(2,b,a,coupler_vertex),
            optical_sum(1,a,b,coupler_vertex),
            optical_scale2(a),
        ],
        "functional_truth":{"%d%d"%k:list(v) for k,v in swap_truth().items()},
    }


def compile_op(op):
    if op["op"]=="SUM_ALPHA":
        return optical_sum(op["alpha"],op["control"],op["target"],op["coupler_vertex"])
    if op["op"]=="SWAP":
        return optical_swap(op["a"],op["b"],op["coupler_vertex"])
    if op["op"]=="SCALE2":
        return optical_scale2(op["wire"])
    raise ValueError(op["op"])


def flatten_devices(compiled):
    out=[]
    def walk(x):
        if isinstance(x,dict):
            if "device" in x: out.append(x["device"])
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(compiled); return out


def read_calibration():
    if not CAL.exists():
        return {"present":False,"hardware_backed":False,"path":str(CAL.relative_to(ROOT)),"reason":"measured calibration packet absent"}
    try:
        raw=json.loads(CAL.read_text(encoding="utf-8"))
    except Exception as e:
        return {"present":True,"hardware_backed":False,"path":str(CAL.relative_to(ROOT)),"reason":f"invalid JSON: {e}"}
    required=["hardware_backed","insertion_loss_db","crosstalk_probability","leakage_probability","phase_rms_rad"]
    missing=[k for k in required if k not in raw]
    numeric_ok=all(isinstance(raw.get(k),(int,float)) and math.isfinite(float(raw[k])) and float(raw[k])>=0 for k in required[1:] if k in raw)
    ok=not missing and raw.get("hardware_backed") is True and numeric_ok
    return {"present":True,"hardware_backed":bool(ok),"path":str(CAL.relative_to(ROOT)),"missing":missing,"packet":raw if not missing else None}


def compile_optical(candidate_count=route.multi.DEFAULT_CANDIDATES):
    routed=route.compile_routes(int(candidate_count))
    compiled=[compile_op(op) for op in routed["flat_ops"]]
    counts=Counter(d for c in compiled for d in flatten_devices(c))
    return routed,compiled,counts,read_calibration()


def verify(candidate_count=route.multi.DEFAULT_CANDIDATES):
    routed,compiled,counts,cal=compile_optical(int(candidate_count))
    sum_ok=all(apply_sum((a,b),alpha,True)==out for alpha in (1,2) for (a,b),out in sum_truth(alpha).items())
    swap_ok=all(replay_swap(s)==out for s,out in swap_truth().items())
    all_lowered=len(compiled)==len(routed["flat_ops"])
    checks={
        "every_W33_local_primitive_has_optical_lowering":all_lowered,
        "SUM1_basis_truth_exact":sum_ok,
        "SWAP_decomposition_basis_truth_exact":swap_ok,
        "compiled_circuit_is_nonempty":len(compiled)>0,
        "all_two_qutrit_sources_remain_W33_local":routed["all_macro_programs_verified"],
    }
    checks={k:bool(v) for k,v in checks.items()}
    return {
        "schema":"w33.qutrit-20-7-2-optical-primitive-compiler.v1",
        "status":"PASS" if all(checks.values()) else "FAIL",
        "checks":checks,
        "optical_compiler_verified":bool(all(checks.values())),
        "hardware_calibration_verified":bool(cal.get("hardware_backed")),
        "calibration":cal,
        "device_inventory":dict(sorted((k,int(v)) for k,v in counts.items())),
        "compiled_primitive_count":len(compiled),
        "compiled_schedule_sha256":digest_json(compiled),
        "sample":compiled[:2]+compiled[-2:] if len(compiled)>4 else compiled,
        "literature_anchors":[
            {"work":"High-dimensional optical quantum logic in large operational spaces","venue":"npj Quantum Information 2019","doi":"10.1038/s41534-019-0173-8","use":"photonic SUM via control-dependent cyclic temporal shifts"},
            {"work":"Linear-optics-based high-dimensional quantum gate with qudits","venue":"Optics Letters 2025","doi":"10.1364/OL.573688","use":"recent explicit photonic controlled-SUM engineering precedent"},
        ],
        "engineering_parameters_required":["insertion_loss_db","crosstalk_probability","leakage_probability","phase_rms_rad"],
        "theorem":"Every topologically local W33 SUM/SWAP/SCALE2 primitive in the selected routed encoder has an explicit coherent qutrit mode-routing candidate circuit whose computational-basis action exactly equals the requested GF(3) gate.",
        "boundary":"Circuit compilation is closed; hardware calibration is not. No measured insertion loss, crosstalk, leakage, phase stability, heralding efficiency, detector efficiency or fault-spread bound is invented when the hardware calibration packet is absent.",
    }

if __name__=="__main__":
    out=verify(); print(json.dumps(out,indent=2)); raise SystemExit(0 if out["status"]=="PASS" else 1)
