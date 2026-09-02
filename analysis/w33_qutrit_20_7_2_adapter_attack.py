#!/usr/bin/env python3
"""Exact reconstruction and fail-closed W33 audit for the [[20,7,2]]_3 code.

Evidence classes are deliberately separated:
  * literal 20-edge CSS monomial embedding: impossible;
  * general GF(3)-linear symplectic embedding: exact;
  * W33 line-graph routing: exact;
  * optical candidate primitive compiler: exact basis-state lowering;
  * mapped decoder + circuit-level syndrome fault census: executable;
  * measured optical calibration + physical threshold: still external hardware gates;
  * Pass79 [[66,8,3]]_3 protected-store bridge: exact at logical recode level;
  * standard closed genus-6 K12 edge surface code as [[66,8,3]]_3: finite no-go (k=12).

No software certificate is promoted into measured photonic fault tolerance.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Any

import w33_qutrit_20_7_2_edge_css_no_go as edge_nogo
import w33_qutrit_20_7_2_symplectic_embedding as symembed

ROOT=Path(__file__).resolve().parents[1]


def mod3_rank(rows:list[list[int]])->int:
    if not rows:return 0
    a=[[x%3 for x in row] for row in rows]; r=0
    for c in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][c]%3),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r]
        if a[r][c]==2:a[r]=[(2*x)%3 for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][c]%3:
                f=a[i][c]; a[i]=[(x-f*y)%3 for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r


def dot(a,b):return sum(x*y for x,y in zip(a,b))%3

def triple(a,b,c):return sum(x*y*z for x,y,z in zip(a,b,c))%3


def build_20_7_2()->dict[str,Any]:
    m,k,n0=3,7,27; w=[i%3 for i in range(n0)]; vs=[]
    for a in range(1,3*m):
        row=[0]*n0
        for i in range(3*(a-1),3*a):row[i]=1
        for i in range(n0-3,n0):row[i]=2
        vs.append(row)
    punctured={3*j for j in range(k)}; keep=[i for i in range(n0) if i not in punctured]
    restrict=lambda row:[row[i] for i in keep]
    h1=[restrict(v) for v in vs[:k]]; h0=[restrict(w),restrict(vs[k])]
    return {"m":m,"k":k,"punctured_1_indexed":[i+1 for i in sorted(punctured)],"kept_1_indexed":[i+1 for i in keep],"H1":h1,"H0":h0,"H":h1+h0}


def z_logical_witnesses(h,h0):
    n=len(h[0]); result={"weight1":None,"weight2":None}
    for weight in (1,2):
        for support in itertools.combinations(range(n),weight):
            for values in itertools.product((1,2),repeat=weight):
                z=[0]*n
                for q,value in zip(support,values):z[q]=value
                if all(dot(row,z)==0 for row in h0) and any(dot(row,z)!=0 for row in h):
                    result[f"weight{weight}"]={"support_0_indexed":list(support),"values":list(values),"vector":z}; break
            if result[f"weight{weight}"] is not None:break
    return result


def _physical_threshold_certificate():
    path=ROOT/"data/w33_qutrit_20_7_2_physical_threshold.json"
    if not path.exists():return {"present":False,"verified":False,"path":str(path.relative_to(ROOT))}
    try: raw=json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:return {"present":True,"verified":False,"path":str(path.relative_to(ROOT)),"error":str(e)}
    ok=raw.get("status")=="PASS" and raw.get("hardware_calibrated") is True and raw.get("physical_fault_model") is not None
    return {"present":True,"verified":bool(ok),"path":str(path.relative_to(ROOT)),"certificate":raw}


def _physical_recode_certificate():
    path=ROOT/"data/w33_qutrit_20_7_2_to_66_physical_recode.json"
    if not path.exists():return {"present":False,"verified":False,"path":str(path.relative_to(ROOT))}
    try: raw=json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:return {"present":True,"verified":False,"path":str(path.relative_to(ROOT)),"error":str(e)}
    ok=raw.get("status")=="PASS" and raw.get("fault_tolerant_code_switch") is True
    return {"present":True,"verified":bool(ok),"path":str(path.relative_to(ROOT)),"certificate":raw}


def repo_adapter_audit()->dict[str,Any]:
    import w33_qutrit_20_7_2_w33_route_compiler as route_compiler
    import w33_qutrit_20_7_2_packet_decoder as packet_decoder
    import w33_qutrit_20_7_2_threshold as threshold_experiment
    import w33_qutrit_20_7_2_optical_primitive as optical
    import w33_qutrit_20_7_2_circuit_noise as circuit_noise
    import w33_qutrit_20_7_2_to_66_bridge as store_bridge

    literal=edge_nogo.verify(); literal_impossible=literal.get("status")=="PASS" and literal.get("decision")=="UNSAT_LITERAL_CSS_MONOMIAL_20_TO_240"
    sym=symembed.verify(); sym_ok=sym.get("status")=="PASS" and sym.get("checks",{}).get("ABt_identity") is True
    route=route_compiler.verify(); route_ok=route.get("status")=="PASS" and route.get("checks",{}).get("every_two_qutrit_primitive_is_line_graph_local") is True
    dec=packet_decoder.verify(); dec_ok=dec.get("status")=="PASS"
    pseudo=threshold_experiment.verify(); pseudo_ok=pseudo.get("status")=="PASS"
    opt=optical.verify(); opt_ok=opt.get("status")=="PASS" and opt.get("optical_compiler_verified") is True
    hardware_cal=opt.get("hardware_calibration_verified") is True
    noise=circuit_noise.verify(); noise_ok=noise.get("status")=="PASS"
    bridge=store_bridge.verify(); bridge_ok=bridge.get("status")=="PASS" and bridge.get("checks",{}).get("pass79_target_is_verified_66_8_3") is True
    k12_nogo=bridge.get("checks",{}).get("standard_genus6_K12_surface_code_encodes_12_not_8") is True
    phys=_physical_threshold_certificate(); recode=_physical_recode_certificate()

    blockers=[]
    if not sym_ok:blockers.append("general symplectic [[20,7,2]]_3 -> W33 edge embedding did not verify")
    if not route_ok:blockers.append("W33 shared-point nearest-neighbour route compiler did not verify")
    if not opt_ok:blockers.append("explicit optical candidate primitive compiler did not verify")
    if opt_ok and not hardware_cal:blockers.append("optical primitive circuit exists, but measured loss/crosstalk/leakage/phase calibration packet is absent or not hardware-backed")
    if not dec_ok:blockers.append("mapped syndrome/decoder certificate did not verify")
    if not noise_ok:blockers.append("circuit-level syndrome fault census did not verify")
    if pseudo_ok and not phys["verified"]:blockers.append("software pseudothreshold/fault census exists, but no hardware-calibrated physical threshold certificate exists")
    if not bridge_ok:blockers.append("logical recode into the explicit Pass79 [[66,8,3]]_3 store did not verify")
    if bridge_ok and not recode["verified"]:blockers.append("distance-3 storage bridge is logical only; no fault-tolerant physical code-switch/recode circuit certificate exists")
    if k12_nogo:blockers.append("standard closed genus-6 K12 edge surface code has k=12, not k=8; four extra independent constraints are required for a K12-native k=8 claim")

    adapter_enabled=sym_ok and route_ok and opt_ok and hardware_cal and dec_ok and noise_ok and phys["verified"]
    return {
        "explicit_encoding_map_present":sym_ok,
        "general_nonlocal_symplectic_embedding_verified":sym_ok,"general_nonlocal_symplectic_embedding":sym,
        "topological_w33_route_compiler_verified":route_ok,"topological_w33_route_certificate":route,
        "locality_optical_compiler_verified":opt_ok,"optical_primitive_certificate":opt,
        "optical_hardware_calibration_verified":hardware_cal,
        "mapped_packet_decoder_verified":dec_ok,"mapped_packet_decoder_certificate":dec,
        "circuit_level_syndrome_noise_verified":noise_ok,"circuit_level_syndrome_noise":noise,
        "mapped_pseudothreshold_experiment_verified":pseudo_ok,"mapped_pseudothreshold_experiment":pseudo,
        "mapped_threshold_certificate_present":phys["verified"],"physical_threshold_certificate":phys,
        "protected_66_store_bridge_verified":bridge_ok,"protected_66_store_bridge":bridge,
        "physical_20_to_66_recode_verified":recode["verified"],"physical_recode_certificate":recode,
        "standard_K12_surface_code_k8_no_go":k12_nogo,
        "literal_edge_css_monomial_no_go":literal,"literal_edge_css_monomial_class_impossible":literal_impossible,
        "closed_embedding_class":"20-edge monomial/zero-extension CSS X->X",
        "surviving_ft_frontier":"measure the compiled optical primitive, calibrate a physical circuit-level fault model to threshold, and build a fault-tolerant logical code-switch into the explicit distance-3 store; treat standard K12 surface code as k=12 unless four extra constraints are specified",
        "blockers":blockers,"adapter_enabled":bool(adapter_enabled),
    }


def verify()->dict[str,Any]:
    code=build_20_7_2(); h,h1,h0=code["H"],code["H1"],code["H0"]; n=len(h[0])
    rank_h=mod3_rank(h); rank_h0=mod3_rank(h0); logical_k=n-rank_h0-(n-rank_h)
    pairwise=all(dot(h[i],h[j])==0 for i in range(len(h)) for j in range(i+1,len(h)))
    triples=all(triple(h[i],h[j],h[k])==0 for i in range(len(h)) for j in range(i+1,len(h)) for k in range(j+1,len(h)))
    cubic=[sum(x**3 for x in row)%3 for row in h]; logical=z_logical_witnesses(h,h0); audit=repo_adapter_audit()
    checks={
        "published_puncture_gives_9x20_matrix":len(h)==9 and n==20,
        "seven_logical_rows_two_x_stabilizer_rows":len(h1)==7 and len(h0)==2,
        "rank_H_is_9":rank_h==9,"rank_H0_is_2":rank_h0==2,"css_encodes_7_qutrits":logical_k==7,
        "H0_is_self_orthogonal":all(dot(a,b)==0 for a in h0 for b in h0),
        "distinct_rows_are_pairwise_orthogonal":pairwise,"distinct_triple_products_vanish":triples,
        "seven_logical_rows_have_nonzero_cubic_norm":cubic[:7]==[2]*7 and cubic[7:]==[0,0],
        "no_weight1_Z_logical":logical["weight1"] is None,"weight2_Z_logical_exists":logical["weight2"] is not None,
        "literal_edge_css_monomial_class_closed_by_no_go":audit["literal_edge_css_monomial_class_impossible"],
        "general_nonlocal_symplectic_embedding_exists":audit["general_nonlocal_symplectic_embedding_verified"],
        "topological_w33_routing_exists":audit["topological_w33_route_compiler_verified"],
        "optical_candidate_compiler_exists":audit["locality_optical_compiler_verified"],
        "mapped_decoder_exists_and_verifies":audit["mapped_packet_decoder_verified"],
        "circuit_noise_census_exists_and_verifies":audit["circuit_level_syndrome_noise_verified"],
        "distance3_store_bridge_exists":audit["protected_66_store_bridge_verified"],
        "standard_K12_k8_claim_is_not_silently_retained":audit["standard_K12_surface_code_k8_no_go"],
        "w33_ft_adapter_remains_fail_closed":not audit["adapter_enabled"],
    }
    checks={k:bool(v) for k,v in checks.items()}
    return {
        "schema":"w33.qutrit-20-7-2-adapter-audit.v6","status":"PASS" if all(checks.values()) else "FAIL",
        "external_code":{"parameters":"[[20,7,2]]_3","source":"Prakash--Saha, Quantum 9, 1768 (2025), construction T_m with m=3,k=7","punctured_coordinates_1_indexed":code["punctured_1_indexed"],"rank_H":rank_h,"rank_H0":rank_h0,"logical_qutrits":logical_k,"cubic_norms":cubic,"weight2_logical_Z_witness":logical["weight2"]},
        "w33_adapter_audit":audit,"checks":checks,
        "decision":"REFUSE_FAULT_TOLERANT_ADAPTER_PENDING_MEASURED_OPTICAL_CALIBRATION_AND_PHYSICAL_THRESHOLD",
        "interpretation":"Algebraic embedding, W33 routing, optical candidate compilation, mapped decoding, circuit-level syndrome fault census, and logical recoding into an explicit distance-3 66-qutrit store now verify. Fault-tolerant admission remains refused because the optical circuit has not been hardware-calibrated and no physical threshold certificate exists. The standard genus-6 K12 surface code is separately audited as k=12, not k=8.",
        "next_required_witness":"Measured primitive calibration and a hardware-calibrated threshold certificate; then a fault-tolerant physical code-switch if the distance-3 store is part of the runtime FT path.",
    }

if __name__=="__main__":
    payload=verify(); print(json.dumps(payload,indent=2)); raise SystemExit(0 if payload["status"]=="PASS" else 1)
