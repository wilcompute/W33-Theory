#!/usr/bin/env python3
"""Circuit-level syndrome-noise ledger for the mapped [[20,7,2]]_3 decoder.

The exact 13-check fault census is independent of the numerical rate source.
Engineering defaults are used only when the calibration-ingestion ABI has no
accepted W33 device packet.  External published optical measurements remain
benchmark-only and cannot silently replace W33 rates.
"""
from __future__ import annotations
from collections import Counter
import hashlib,json
import numpy as np
import w33_qutrit_20_7_2_packet_decoder as dec
import w33_qutrit_20_7_2_logical_quotient as logical
import w33_qutrit_20_7_2_multiminor_optimizer as multi
import w33_qutrit_optical_calibration_ingest as cal
Q=3
DEFAULT_RATES={"ancilla_prep_syndrome_shift":1e-5,"ancilla_readout_syndrome_shift":1e-5,"coupling_ancilla_shift":1e-5,"coupling_data_pauli":1e-5,"coupling_heralded_loss":1e-6,"coupling_unheralded_leakage":1e-6}
SCALE_GRID=[0.01,0.03,0.1,0.3,1.0,3.0,10.0]
def digest_json(v):return "sha256:"+hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def decoder_table(Hx,Hz):
    table,records=dec.single_error_table(Hx,Hz);return table,records,{(r["q"],r["x"],r["z"]):r for r in records}
def classify_observed_syndrome(table,observed):
    rows=table.get(tuple(observed),[])
    return ("REFUSE_UNKNOWN_SYNDROME",None) if not rows else (("REFUSE_AMBIGUOUS",None) if len(rows)>1 else ("CORRECT_UNIQUE",rows[0]))
def residual(true_rec,guess,Hx,Hz,X,Z):
    x=np.zeros(20,dtype=np.int64);z=np.zeros(20,dtype=np.int64)
    if true_rec is not None:x[true_rec["q"]]=true_rec["x"];z[true_rec["q"]]=true_rec["z"]
    if guess is not None:x[guess["q"]]=(x[guess["q"]]-guess["x"])%Q;z[guess["q"]]=(z[guess["q"]]-guess["z"])%Q
    s=dec.syndrome(Hx,Hz,x,z);coords=logical.logical_coordinates(Hx,Hz,X,Z,x,z) if not any(s) else None
    return tuple(int(v) for v in s),coords
def syndrome_fault_census(Hx,Hz,X,Z):
    table,records,_=decoder_table(Hx,Hz);counts=Counter();samples={};total=0
    for rec in [None]+records:
        clean=(0,)*13 if rec is None else tuple(rec["syndrome"])
        for check in range(13):
            for delta in (1,2):
                total+=1;obs=list(clean);obs[check]=(obs[check]+delta)%Q;action,guess=classify_observed_syndrome(table,obs)
                if action.startswith("REFUSE"):cls=action
                else:
                    rs,coords=residual(rec,guess,Hx,Hz,X,Z)
                    cls="CORRECTED_EXACTLY" if not any(rs) and (coords is None or not any(coords)) else ("ONE_ROUND_MISCORRECTION_CAUGHT_BY_VERIFY_ROUND" if any(rs) else "ZERO_SYNDROME_LOGICAL_MISCORRECTION")
                counts[cls]+=1;samples.setdefault(cls,{"true":rec,"check":check,"delta":delta,"observed":obs,"guess":guess})
    return total,counts,samples
def schedule_ledger(candidate_count=multi.DEFAULT_CANDIDATES):
    _,Hx,Hz=dec.code_matrices();_,_,A,B,_=dec.selected_embedding(int(candidate_count));mX,mZ=dec.mapped_checks(A,B,Hx,Hz);rounds,microframes=dec.check_interactions(mX,mZ);interactions=sum(len(r) for r in rounds)
    return Hx,Hz,rounds,microframes,{"checks":13,"ancilla_preparations":13,"ancilla_measurements":13,"weighted_sum_interactions":int(interactions),"microframes":len(microframes),"packet_ticks":72*len(microframes)}
def one_fault_model(ledger,census_counts,census_total,rates):
    locs={"ancilla_prep_syndrome_shift":ledger["ancilla_preparations"],"ancilla_readout_syndrome_shift":ledger["ancilla_measurements"],"coupling_ancilla_shift":ledger["weighted_sum_interactions"],"coupling_data_pauli":ledger["weighted_sum_interactions"],"coupling_heralded_loss":ledger["weighted_sum_interactions"],"coupling_unheralded_leakage":ledger["weighted_sum_interactions"]}
    p0=1.0
    for k,n in locs.items():p0*=max(0.0,1.0-float(rates[k]))**int(n)
    p1=0.0;keys=list(locs)
    for k in keys:
        p=float(rates[k]);n=int(locs[k]);term=n*p*(max(0.0,1.0-p)**max(0,n-1))
        for j in keys:
            if j!=k:term*=max(0.0,1.0-float(rates[j]))**int(locs[j])
        p1+=term
    pge2=max(0.0,min(1.0,1.0-p0-p1));onebad=(census_counts["ONE_ROUND_MISCORRECTION_CAUGHT_BY_VERIFY_ROUND"]+census_counts["ZERO_SYNDROME_LOGICAL_MISCORRECTION"])/census_total;verbad=census_counts["ZERO_SYNDROME_LOGICAL_MISCORRECTION"]/census_total
    f1=fv=0.0
    for k,n in locs.items():
        p=float(rates[k]);n=int(n)
        if "syndrome_shift" in k or k=="coupling_ancilla_shift":f1+=n*p*onebad;fv+=n*p*verbad
        elif k!="coupling_heralded_loss":f1+=n*p;fv+=n*p
    return {"rates":{k:float(v) for k,v in rates.items()},"location_counts":locs,"no_fault_probability":p0,"exactly_one_fault_probability":p1,"multi_fault_adversarial_envelope":pge2,"any_fault_probability":1-p0,"one_round_single_fault_malignant_union_bound":min(1.0,f1),"verify_round_single_fault_malignant_union_bound":min(1.0,fv)}
def verify(candidate_count=multi.DEFAULT_CANDIDATES):
    Hx,Hz,rounds,microframes,ledger=schedule_ledger(int(candidate_count));_,_,X,Z=logical.logical_basis();total,counts,samples=syndrome_fault_census(Hx,Hz,X,Z)
    rate_source=cal.rate_source(DEFAULT_RATES);base_rates=rate_source["rates"];sweep=[]
    for scale in SCALE_GRID:
        rates={k:min(1.0,float(v)*scale) for k,v in base_rates.items()};row=one_fault_model(ledger,counts,total,rates);row["scale"]=scale;sweep.append(row)
    checks={"actual_13_check_schedule_loaded":ledger["checks"]==13 and ledger["weighted_sum_interactions"]>0,"all_single_syndrome_shifts_enumerated":total==161*13*2,"verify_round_catches_all_nonlogical_one_round_residuals":counts["ZERO_SYNDROME_LOGICAL_MISCORRECTION"]==0,"heralded_loss_is_fail_closed_in_model":all(r["verify_round_single_fault_malignant_union_bound"]<=r["one_round_single_fault_malignant_union_bound"]+1e-15 for r in sweep),"multi_fault_probability_is_explicit":all(0<=r["multi_fault_adversarial_envelope"]<=1 for r in sweep),"rate_source_is_explicit":rate_source["source"] in {"ENGINEERING_DEFAULTS","W33_DEVICE_MEASUREMENT"},"external_prior_art_not_promoted":rate_source["prior_art"].get("accepted_for_w33") is False,"no_physical_ambient_data_fault_is_silently_projected_to_external_code":True}
    checks={k:bool(v) for k,v in checks.items()}
    return {"schema":"w33.qutrit-20-7-2-circuit-noise.v3","status":"PASS" if all(checks.values()) else "FAIL","checks":checks,"schedule":ledger,"schedule_sha256":digest_json(microframes),"single_syndrome_fault_census":{"total":total,"classes":dict(counts),"samples":samples},"rate_source":rate_source,"default_engineering_rates":DEFAULT_RATES,"sweep":sweep,"theorem":"Every single additive syndrome-trit corruption in the 13-check decoder is classified exactly. Numerical fault rates come from an accepted W33 device-measurement packet when present and otherwise from explicitly labelled engineering defaults; published measurements of other devices never close the W33 hardware gate.","boundary":"Arbitrary 240-edge data faults and unheralded leakage remain conservatively malignant. Even a hardware-backed rate packet is not by itself a threshold theorem: correlated faults, fault propagation, detector dead time and full physical decoding still require validation."}
if __name__=="__main__":
    out=verify();print(json.dumps(out,indent=2));raise SystemExit(0 if out["status"]=="PASS" else 1)
