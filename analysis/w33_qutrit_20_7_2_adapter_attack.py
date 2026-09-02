#!/usr/bin/env python3
"""Exact reconstruction and fail-closed W33 audit for [[20,7,2]]_3.

Current evidence classes:
  * literal 20-edge CSS monomial embedding: impossible;
  * general GF(3)-linear symplectic embedding: exact;
  * W33 line-graph routing + optical candidate lowering: exact software;
  * mapped decoder, circuit-noise and fault-location censuses: executable;
  * W33 device optical calibration: accepted only through the measurement ABI;
  * Pass79 [[66,8,3]]_3 store: explicit noncanonical witness;
  * K12-labelled native code: raw [[66,13,3]]_3 singular-chain code, gauge
    fixed by five explicit Z-logical constraints to [[66,8,3]]_3;
  * naive decode/bare-handoff/re-encode: exact Clifford circuit, proved NOT
    one-fault tolerant (56/56 bare-handoff Paulis malignant).

No software result is promoted into physical fault tolerance.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from typing import Any
import w33_qutrit_20_7_2_edge_css_no_go as edge_nogo
import w33_qutrit_20_7_2_symplectic_embedding as symembed
ROOT=Path(__file__).resolve().parents[1]

def mod3_rank(rows):
    if not rows:return 0
    a=[[x%3 for x in row] for row in rows];r=0
    for c in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][c]%3),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r]
        if a[r][c]==2:a[r]=[(2*x)%3 for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][c]%3:
                f=a[i][c];a[i]=[(x-f*y)%3 for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r
def dot(a,b):return sum(x*y for x,y in zip(a,b))%3
def triple(a,b,c):return sum(x*y*z for x,y,z in zip(a,b,c))%3
def build_20_7_2()->dict[str,Any]:
    m,k,n0=3,7,27;w=[i%3 for i in range(n0)];vs=[]
    for a in range(1,3*m):
        row=[0]*n0
        for i in range(3*(a-1),3*a):row[i]=1
        for i in range(n0-3,n0):row[i]=2
        vs.append(row)
    punctured={3*j for j in range(k)};keep=[i for i in range(n0) if i not in punctured];restrict=lambda row:[row[i] for i in keep]
    h1=[restrict(v) for v in vs[:k]];h0=[restrict(w),restrict(vs[k])]
    return {"m":m,"k":k,"punctured_1_indexed":[i+1 for i in sorted(punctured)],"kept_1_indexed":[i+1 for i in keep],"H1":h1,"H0":h0,"H":h1+h0}
def z_logical_witnesses(h,h0):
    n=len(h[0]);result={"weight1":None,"weight2":None}
    for weight in (1,2):
        for support in itertools.combinations(range(n),weight):
            for values in itertools.product((1,2),repeat=weight):
                z=[0]*n
                for q,v in zip(support,values):z[q]=v
                if all(dot(row,z)==0 for row in h0) and any(dot(row,z)!=0 for row in h):result[f"weight{weight}"]={"support_0_indexed":list(support),"values":list(values),"vector":z};break
            if result[f"weight{weight}"] is not None:break
    return result
def _physical_threshold_certificate():
    p=ROOT/"data/w33_qutrit_20_7_2_physical_threshold.json"
    if not p.exists():return {"present":False,"verified":False,"path":str(p.relative_to(ROOT))}
    try:r=json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:return {"present":True,"verified":False,"error":str(e)}
    ok=r.get("status")=="PASS" and r.get("hardware_calibrated") is True and r.get("physical_fault_model") is not None
    return {"present":True,"verified":bool(ok),"certificate":r}
def _physical_recode_certificate():
    p=ROOT/"data/w33_qutrit_20_7_2_to_66_physical_recode.json"
    if not p.exists():return {"present":False,"verified":False,"path":str(p.relative_to(ROOT))}
    try:r=json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:return {"present":True,"verified":False,"error":str(e)}
    ok=r.get("status")=="PASS" and r.get("fault_tolerant_code_switch") is True and r.get("bare_logical_window") is False
    return {"present":True,"verified":bool(ok),"certificate":r}
def repo_adapter_audit():
    import w33_qutrit_20_7_2_w33_route_compiler as route_compiler
    import w33_qutrit_20_7_2_packet_decoder as packet_decoder
    import w33_qutrit_20_7_2_threshold as threshold_experiment
    import w33_qutrit_20_7_2_optical_primitive as optical
    import w33_qutrit_optical_calibration_ingest as cal
    import w33_qutrit_20_7_2_circuit_noise as circuit_noise
    import w33_qutrit_20_7_2_fault_location_census as locations
    import w33_qutrit_20_7_2_to_66_bridge as store_bridge
    import w33_qutrit_20_7_2_to_66_recode_circuit as recode_circuit
    import w33_k12_singular_css_closure as k12css
    literal=edge_nogo.verify();literal_ok=literal.get("status")=="PASS" and literal.get("decision")=="UNSAT_LITERAL_CSS_MONOMIAL_20_TO_240"
    sym=symembed.verify();sym_ok=sym.get("status")=="PASS" and sym.get("checks",{}).get("ABt_identity") is True
    route=route_compiler.verify();route_ok=route.get("status")=="PASS" and route.get("checks",{}).get("every_two_qutrit_primitive_is_line_graph_local") is True
    dec=packet_decoder.verify();dec_ok=dec.get("status")=="PASS"
    opt=optical.verify();opt_ok=opt.get("status")=="PASS" and opt.get("optical_compiler_verified") is True
    calv=cal.verify();hardware_cal=calv.get("effective_rate_source",{}).get("hardware_backed") is True
    noise=circuit_noise.verify();noise_ok=noise.get("status")=="PASS"
    loc=locations.verify();loc_ok=loc.get("status")=="PASS"
    pseudo=threshold_experiment.verify();pseudo_ok=pseudo.get("status")=="PASS"
    bridge=store_bridge.verify();bridge_ok=bridge.get("status")=="PASS"
    topo=k12css.verify();topo_ok=topo.get("status")=="PASS" and topo.get("native_k8_gauge_fix",{}).get("parameters")=="[[66,8,3]]_3"
    recirc=recode_circuit.verify();naive_nogo=recirc.get("status")=="PASS" and recirc.get("decision")=="REFUSE_NAIVE_RECODE_AS_FAULT_TOLERANT"
    phys=_physical_threshold_certificate();recode=_physical_recode_certificate()
    blockers=[]
    for ok,msg in [(sym_ok,"general symplectic W33 embedding did not verify"),(route_ok,"W33 route compiler did not verify"),(opt_ok,"optical candidate compiler did not verify"),(dec_ok,"mapped decoder did not verify"),(noise_ok,"circuit-noise census did not verify"),(loc_ok,"fault-location census did not verify"),(bridge_ok,"66-qutrit logical bridge did not verify"),(topo_ok,"native K12 gauge-fixed code did not verify"),(naive_nogo,"naive-recode FT no-go did not verify")]:
        if not ok:blockers.append(msg)
    if opt_ok and not hardware_cal:blockers.append("no accepted W33_DEVICE_MEASUREMENT optical calibration packet; external prior art is benchmark-only")
    if pseudo_ok and not phys["verified"]:blockers.append("no hardware-calibrated physical threshold certificate")
    if bridge_ok and not recode["verified"]:blockers.append("naive recode is provably non-FT and no encoded/teleported fault-tolerant replacement certificate exists")
    adapter_enabled=all((sym_ok,route_ok,opt_ok,hardware_cal,dec_ok,noise_ok,loc_ok,phys["verified"],recode["verified"]))
    return {"general_nonlocal_symplectic_embedding_verified":sym_ok,"topological_w33_route_compiler_verified":route_ok,"locality_optical_compiler_verified":opt_ok,"optical_calibration_ingest":calv,"optical_hardware_calibration_verified":hardware_cal,"mapped_packet_decoder_verified":dec_ok,"circuit_level_syndrome_noise_verified":noise_ok,"fault_location_census_verified":loc_ok,"mapped_pseudothreshold_experiment_verified":pseudo_ok,"mapped_threshold_certificate_present":phys["verified"],"protected_66_store_bridge_verified":bridge_ok,"K12_native_gauge_fixed_66_8_3_verified":topo_ok,"naive_recode_FT_no_go_verified":naive_nogo,"physical_20_to_66_recode_verified":recode["verified"],"literal_edge_css_monomial_class_impossible":literal_ok,"physical_threshold_certificate":phys,"physical_recode_certificate":recode,"blockers":blockers,"adapter_enabled":bool(adapter_enabled)}
def verify():
    code=build_20_7_2();h,h1,h0=code["H"],code["H1"],code["H0"];n=len(h[0]);rank_h=mod3_rank(h);rank_h0=mod3_rank(h0);logical_k=n-rank_h0-(n-rank_h);pairwise=all(dot(h[i],h[j])==0 for i in range(len(h)) for j in range(i+1,len(h)));triples=all(triple(h[i],h[j],h[k])==0 for i in range(len(h)) for j in range(i+1,len(h)) for k in range(j+1,len(h)));cubic=[sum(x**3 for x in row)%3 for row in h];lw=z_logical_witnesses(h,h0);audit=repo_adapter_audit()
    checks={"published_puncture_gives_9x20_matrix":len(h)==9 and n==20,"seven_logical_rows_two_x_stabilizer_rows":len(h1)==7 and len(h0)==2,"rank_H_is_9":rank_h==9,"rank_H0_is_2":rank_h0==2,"css_encodes_7_qutrits":logical_k==7,"H0_is_self_orthogonal":all(dot(a,b)==0 for a in h0 for b in h0),"distinct_rows_are_pairwise_orthogonal":pairwise,"distinct_triple_products_vanish":triples,"seven_logical_rows_have_nonzero_cubic_norm":cubic[:7]==[2]*7 and cubic[7:]==[0,0],"no_weight1_Z_logical":lw["weight1"] is None,"weight2_Z_logical_exists":lw["weight2"] is not None,"literal_edge_css_monomial_no_go":audit["literal_edge_css_monomial_class_impossible"],"embedding_route_optics_decoder_noise_locations_closed":all(audit[x] for x in ("general_nonlocal_symplectic_embedding_verified","topological_w33_route_compiler_verified","locality_optical_compiler_verified","mapped_packet_decoder_verified","circuit_level_syndrome_noise_verified","fault_location_census_verified")),"K12_native_66_8_3_closed":audit["K12_native_gauge_fixed_66_8_3_verified"],"naive_recode_nonFT_proved":audit["naive_recode_FT_no_go_verified"],"w33_ft_adapter_remains_fail_closed":not audit["adapter_enabled"]}
    checks={k:bool(v) for k,v in checks.items()}
    return {"schema":"w33.qutrit-20-7-2-adapter-audit.v7","status":"PASS" if all(checks.values()) else "FAIL","external_code":{"parameters":"[[20,7,2]]_3","source":"Prakash--Saha, Quantum 9, 1768 (2025)","logical_qutrits":logical_k,"cubic_norms":cubic,"weight2_logical_Z_witness":lw["weight2"]},"w33_adapter_audit":audit,"checks":checks,"decision":"REFUSE_FAULT_TOLERANT_ADAPTER_PENDING_W33_DEVICE_CALIBRATION_PHYSICAL_THRESHOLD_AND_ENCODED_RECODE","interpretation":"Software/algebraic routing, decoding, location-level fault census, K12 native gauge-fixed [[66,8,3]]_3 construction, and the no-go for naive bare-logical recoding are closed. Physical FT remains refused because no accepted W33 device calibration/threshold exists and the only concrete recode circuit is provably non-FT.","next_required_witness":"Hardware-backed W33 optical calibration, full physical threshold, and an encoded/teleported code-switch with no bare logical window."}
if __name__=="__main__":
    out=verify();print(json.dumps(out,indent=2));raise SystemExit(0 if out["status"]=="PASS" else 1)
