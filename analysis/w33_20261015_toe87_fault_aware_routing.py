"""TOE87: reproducible stochastic syndrome and gate-fault exposure study.

Ideal Clifford wire routing with a clearly declared post-SWAP X Pauli
fault model, correlated two-wire fault branch, local inversion faults,
and independent qutrit syndrome digit readout noise. No threshold claim.
"""
from __future__ import annotations
import collections, json
import math
import random
import numpy as np
from analysis.w33_20261015_toe85_h2_relation_module import ROOT,geometry
from analysis.w33_20261015_toe86_geometry_integral_routing import perm_cycles

SEED=871527
SHOTS=192
SWAP_ERROR=2e-4
LOCAL_INVERSION_ERROR=2e-4
SYNDROME_READOUT_ERROR=1e-3
CORRELATED_GIVEN_FAULT=.10

def all_to_all_schedule(q):
    plan=[]
    for cycle in perm_cycles(q):
        for j in cycle[1:]:
            plan.append((cycle[0],j))
    return plan

def simulate_plan(q, plan):
    tok=list(range(135))
    for a,b in plan:tok[a],tok[b]=tok[b],tok[a]
    assert all(q[tok[i]]==i for i in range(135))
    return True

def one_sample(rng,plan,inversion_targets,H,syndrome_map):
    error=[0]*135
    fault_swaps=0;fault_inversions=0;fault_correlated=0
    for a,b in plan:
        error[a],error[b]=error[b],error[a]
        if rng.random()<SWAP_ERROR:
            fault_swaps+=1
            pos=a if rng.randrange(2)==0 else b
            error[pos]=(error[pos]+rng.choice((1,2)))%3
            if rng.random()<CORRELATED_GIVEN_FAULT:
                pos2=b if pos==a else a
                error[pos2]=(error[pos2]+rng.choice((1,2)))%3
                fault_correlated+=1
    for j in inversion_targets:
        error[j]=(-error[j])%3
        if rng.random()<LOCAL_INVERSION_ERROR:
            fault_inversions+=1
            error[j]=(error[j]+rng.choice((1,2)))%3
    syndrome=np.mod(H@np.asarray(error,dtype=np.int16),3)
    clean_syndrome=bool(np.any(syndrome))
    observed=syndrome.copy()
    readout_errors=0
    for i in range(99):
        if rng.random()<SYNDROME_READOUT_ERROR:
            observed[i]=(observed[i]+rng.choice((1,2)))%3
            readout_errors+=1
    # A deliberately simple one-site lookup decoder, not a fault-
    # tolerant decoder or claim of logical correction.
    key=observed.tobytes()
    candidate=syndrome_map.get(key)
    corrected=error[:]
    if candidate is not None:
        loc,coeff=candidate
        corrected[loc]=(corrected[loc]-coeff)%3
    return {"any_gate_fault":fault_swaps+fault_inversions>0,
            "faulty_swaps":fault_swaps,"correlated_faults":fault_correlated,
            "faulty_inversions":fault_inversions,
            "true_X_error":any(error),
            "true_syndrome_detected":clean_syndrome,
            "measured_syndrome_nonzero":bool(np.any(observed)),
            "readout_faults":readout_errors,
            "zero_physical_error_after_one_site_decoder":not any(corrected),
            "error_with_zero_true_syndrome":any(error) and not clean_syndrome}

def syndrome_dictionary(H):
    d={}
    for pos in range(135):
        for coeff in (1,2):
            k=np.mod(coeff*H[:,pos],3).astype(np.int16).tobytes()
            if k in d: d[k]=None
            else:d[k]=(pos,coeff)
    return d

def certificate():
    _,rows,_=geometry()
    H=np.mod(np.asarray(rows,dtype=np.int16),3)
    assert H.shape==(99,135)
    single=syndrome_dictionary(H)
    frozen=json.loads((ROOT/"data/w33_20261015_toe86_geometry_integral_routing.json").read_text())["encoded_clifford_permutation_compiler"]["compiled_generators"]
    result=[]
    for i,info in enumerate(frozen):
        q=info["edge_destination"]
        inversion_targets=[q[j] for j,s in enumerate(info["edge_orientation_sign"]) if s==-1]
        alltoall=all_to_all_schedule(q)
        assert len(alltoall)==90
        simulate_plan(q,alltoall)
        nn=[(k,k+1) for layer in info["nearest_neighbor_layers_start_positions"] for k in layer]
        simulate_plan(q,nn)
        assert len(nn)==info["linear_nearest_neighbor_SWAP_count_optimal"]
        for model,plan in (("all_to_all",alltoall),("linear_nearest_neighbor",nn)):
            rng=random.Random(SEED+100*i+(0 if model=="all_to_all" else 1))
            samples=[one_sample(rng,plan,inversion_targets,H,single) for _ in range(SHOTS)]
            metrics={}
            for key in samples[0]:
                vals=[s[key] for s in samples]
                metrics[key+"_per_shot_mean"]=sum(vals)/SHOTS
            circuit_no_gate_fault=(1-SWAP_ERROR)**len(plan)*(1-LOCAL_INVERSION_ERROR)**len(inversion_targets)
            result.append({"H27_generator":info["generator"],"model":model,
                           "shots":SHOTS,"SWAP_count":len(plan),
                           "inversion_count":len(inversion_targets),
                           "analytic_expected_faulty_SWAPS":SWAP_ERROR*len(plan),
                           "analytic_prob_zero_gate_fault":circuit_no_gate_fault,
                           "metrics":metrics})
            print("FAULT",info["generator"],model,"SWAP",len(plan),
                  "P0",round(circuit_no_gate_fault,5),
                  "observed any fault",metrics["any_gate_fault_per_shot_mean"],
                  "decoder",metrics["zero_physical_error_after_one_site_decoder_per_shot_mean"],flush=True)
    return {"status":"SIMULATED_AND_SOME_ANALYTIC","shots_per_case":SHOTS,
            "seed":SEED,"p_swap_pauli_X":SWAP_ERROR,
            "p_local_inversion_pauli_X":LOCAL_INVERSION_ERROR,
            "p_readout_digit_shift":SYNDROME_READOUT_ERROR,
            "conditional_correlated_two_qudit_fault":CORRELATED_GIVEN_FAULT,
            "single_site_syndrome_patterns":len(single),
            "ambiguous_single_site_syndrome_patterns":sum(v is None for v in single.values()),
            "cases":result,
            "boundaries":"Stochastic chosen errors and fixed layouts, no native gate noise data, no repeated stabilizer measurement cycles, no quantum threshold or full decoder, zero physical residual stricter than logical success."}

if __name__=="__main__":
    d=certificate()
    p=ROOT/"data/w33_20261015_toe87_fault_aware_routing.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("FROZEN",p)
