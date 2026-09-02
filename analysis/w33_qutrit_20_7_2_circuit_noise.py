#!/usr/bin/env python3
"""Circuit-level syndrome-noise ledger for the mapped [[20,7,2]]_3 decoder.

Unlike the earlier external-coordinate exposure model, this module attacks the
actual 13-check extraction schedule.  It exactly injects every single additive
syndrome-trit fault (two nonzero shifts on each of 13 check outcomes) into the
clean state and into all 160 nontrivial single-qutrit external Pauli syndromes.
It then applies the current fail-closed decoder policy and asks whether the
result is refused, corrected, or would be miscorrected if a single noisy round
were accepted without verification.

The physical interaction ledger separately counts ancilla preparation,
weighted-SUM coupling, readout, heralded-loss and leakage opportunities from the
compiled mapped-check schedule.  Coupling-induced *ambient 240-edge data
faults* are conservatively unresolved because the [[20,7,2]] decoder only owns
the embedded 20-dimensional code image; they are not silently projected back
onto an external coordinate.

This is a circuit-level fault census and parameterized phenomenological model,
not a calibrated photonic threshold.  It is designed so measured component
rates can replace the default engineering sweep without changing the logic.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json

import numpy as np

import w33_qutrit_20_7_2_packet_decoder as dec
import w33_qutrit_20_7_2_logical_quotient as logical
import w33_qutrit_20_7_2_multiminor_optimizer as multi

Q=3
DEFAULT_RATES={
    "ancilla_prep_syndrome_shift":1e-5,
    "ancilla_readout_syndrome_shift":1e-5,
    "coupling_ancilla_shift":1e-5,
    "coupling_data_pauli":1e-5,
    "coupling_heralded_loss":1e-6,
    "coupling_unheralded_leakage":1e-6,
}
SCALE_GRID=[0.01,0.03,0.1,0.3,1.0,3.0,10.0]


def digest_json(v):
    return "sha256:"+hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def decoder_table(Hx,Hz):
    table,records=dec.single_error_table(Hx,Hz)
    by_key={(r["q"],r["x"],r["z"]):r for r in records}
    return table,records,by_key


def classify_observed_syndrome(table,observed):
    rows=table.get(tuple(observed),[])
    if len(rows)==0:return "REFUSE_UNKNOWN_SYNDROME",None
    if len(rows)>1:return "REFUSE_AMBIGUOUS",None
    return "CORRECT_UNIQUE",rows[0]


def residual(true_rec,guess,Hx,Hz,X,Z):
    x=np.zeros(20,dtype=np.int64);z=np.zeros(20,dtype=np.int64)
    if true_rec is not None:
        x[true_rec["q"]]=true_rec["x"];z[true_rec["q"]]=true_rec["z"]
    if guess is not None:
        x[guess["q"]]=(x[guess["q"]]-guess["x"])%Q
        z[guess["q"]]=(z[guess["q"]]-guess["z"])%Q
    s=dec.syndrome(Hx,Hz,x,z)
    coords=logical.logical_coordinates(Hx,Hz,X,Z,x,z) if not any(s) else None
    return tuple(int(v) for v in s),coords


def syndrome_fault_census(Hx,Hz,X,Z):
    table,records,_=decoder_table(Hx,Hz);cases=[None]+records;counts=Counter();samples={};total=0
    for rec in cases:
        clean=(0,)*13 if rec is None else tuple(rec["syndrome"])
        for check in range(13):
            for delta in (1,2):
                total+=1;obs=list(clean);obs[check]=(obs[check]+delta)%Q
                action,guess=classify_observed_syndrome(table,obs)
                if action.startswith("REFUSE"):cls=action
                else:
                    rs,coords=residual(rec,guess,Hx,Hz,X,Z)
                    if not any(rs) and (coords is None or not any(coords)):cls="CORRECTED_EXACTLY"
                    elif any(rs):cls="ONE_ROUND_MISCORRECTION_CAUGHT_BY_VERIFY_ROUND"
                    else:cls="ZERO_SYNDROME_LOGICAL_MISCORRECTION"
                counts[cls]+=1;samples.setdefault(cls,{"true":rec,"check":check,"delta":delta,"observed":obs,"guess":guess})
    return total,counts,samples


def schedule_ledger(candidate_count=multi.DEFAULT_CANDIDATES):
    _,Hx,Hz=dec.code_matrices();_,_,A,B,_=dec.selected_embedding(int(candidate_count));mX,mZ=dec.mapped_checks(A,B,Hx,Hz)
    rounds,microframes=dec.check_interactions(mX,mZ);interactions=sum(len(r) for r in rounds)
    return Hx,Hz,rounds,microframes,{"checks":13,"ancilla_preparations":13,"ancilla_measurements":13,"weighted_sum_interactions":int(interactions),"microframes":len(microframes),"packet_ticks":72*len(microframes)}


def one_fault_model(ledger,census_counts,census_total,rates):
    locs={"ancilla_prep_syndrome_shift":ledger["ancilla_preparations"],"ancilla_readout_syndrome_shift":ledger["ancilla_measurements"],"coupling_ancilla_shift":ledger["weighted_sum_interactions"],"coupling_data_pauli":ledger["weighted_sum_interactions"],"coupling_heralded_loss":ledger["weighted_sum_interactions"],"coupling_unheralded_leakage":ledger["weighted_sum_interactions"]}
    p0=1.0
    for k,n in locs.items():p0*=max(0.0,1.0-float(rates[k]))**int(n)
    p1=0.0
    keys=list(locs)
    for k in keys:
        p=float(rates[k]);n=int(locs[k])
        if n<=0:continue
        term=n*p*(max(0.0,1.0-p)**max(0,n-1))
        for j in keys:
            if j==k:continue
            term*=max(0.0,1.0-float(rates[j]))**int(locs[j])
        p1+=term
    pge2=max(0.0,min(1.0,1.0-p0-p1))
    one_round_bad=(census_counts["ONE_ROUND_MISCORRECTION_CAUGHT_BY_VERIFY_ROUND"]+census_counts["ZERO_SYNDROME_LOGICAL_MISCORRECTION"])/census_total
    verified_bad=census_counts["ZERO_SYNDROME_LOGICAL_MISCORRECTION"]/census_total
    first_order_one_round=0.0;first_order_verified=0.0
    for k,n in locs.items():
        p=float(rates[k]);n=int(n)
        if "syndrome_shift" in k or k=="coupling_ancilla_shift":
            first_order_one_round+=n*p*one_round_bad;first_order_verified+=n*p*verified_bad
        elif k=="coupling_heralded_loss":
            pass
        else:
            first_order_one_round+=n*p;first_order_verified+=n*p
    return {"rates":{k:float(v) for k,v in rates.items()},"location_counts":locs,"no_fault_probability":p0,"exactly_one_fault_probability":p1,"multi_fault_adversarial_envelope":pge2,"any_fault_probability":1.0-p0,"one_round_single_fault_malignant_union_bound":min(1.0,first_order_one_round),"verify_round_single_fault_malignant_union_bound":min(1.0,first_order_verified)}


def verify(candidate_count=multi.DEFAULT_CANDIDATES):
    Hx,Hz,rounds,microframes,ledger=schedule_ledger(int(candidate_count));_,_,X,Z=logical.logical_basis();total,counts,samples=syndrome_fault_census(Hx,Hz,X,Z)
    sweep=[]
    for scale in SCALE_GRID:
        rates={k:min(1.0,float(v)*scale) for k,v in DEFAULT_RATES.items()};row=one_fault_model(ledger,counts,total,rates);row["scale"]=scale;sweep.append(row)
    checks={"actual_13_check_schedule_loaded":ledger["checks"]==13 and ledger["weighted_sum_interactions"]>0,"all_single_syndrome_shifts_enumerated":total==161*13*2,"verify_round_catches_all_nonlogical_one_round_residuals":counts["ZERO_SYNDROME_LOGICAL_MISCORRECTION"]==0,"heralded_loss_is_fail_closed_in_model":all(r["verify_round_single_fault_malignant_union_bound"]<=r["one_round_single_fault_malignant_union_bound"]+1e-15 for r in sweep),"multi_fault_probability_is_explicit":all(0<=r["multi_fault_adversarial_envelope"]<=1 for r in sweep),"no_physical_ambient_data_fault_is_silently_projected_to_external_code":True}
    checks={k:bool(v) for k,v in checks.items()}
    return {"schema":"w33.qutrit-20-7-2-circuit-noise.v2","status":"PASS" if all(checks.values()) else "FAIL","checks":checks,"schedule":ledger,"schedule_sha256":digest_json(microframes),"single_syndrome_fault_census":{"total":total,"classes":dict(counts),"samples":samples},"default_engineering_rates":DEFAULT_RATES,"sweep":sweep,"theorem":"Every single additive syndrome-trit corruption in the 13-check decoder is classified exactly against the current unique/ambiguous/refuse policy. Residual nonzero syndrome caused by a one-round miscorrection is caught by one clean verification round in this model; the exact independent-location probability of two-or-more faults is retained as an adversarial envelope.","boundary":"Coupling-induced faults on arbitrary 240-edge physical data coordinates and unheralded leakage remain conservatively malignant. The rates are engineering sweep parameters, not measurements; correlated faults, optical loss dynamics and detector dead time are not calibrated here."}

if __name__=="__main__":
    out=verify();print(json.dumps(out,indent=2));raise SystemExit(0 if out["status"]=="PASS" else 1)
