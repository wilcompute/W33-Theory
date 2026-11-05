#!/usr/bin/env python3
"""TOE front D: exact finite causal-history action and oscillatory interference.

All 2^(N choose 2) chronological-edge bit histories (N=6),
each transitive-closed to a causal partial order. This is a uniform
DAG-PRESENTATION measure, not uniform unlabeled/labeled posets.
Compute exact interval abundances N1...N4 (Ni has i-1 interior
elements) and the BDG *combinatorial brackets*:
 B2=N-2N1+4N2-2N3,
 B4=N-N1+9N2-16N3+8N4.
Physical BDG action has dimension-dependent normalization/boundary
terms/couplings; use these brackets only as finite interference
phase toys, NOT evidence for a quantum gravity continuum action.
"""
from __future__ import annotations
import collections,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_causal_bdg_exact_history_interference.json"
N=6
EDGES=[(i,j) for j in range(1,N) for i in range(j)]
HISTORIES=1<<len(EDGES)
def closure(mask):
    past=[0]*N
    for k,(i,j) in enumerate(EDGES):
        if (mask>>k)&1:past[j]|=1<<i
    for j in range(N):
        direct=past[j]
        for i in range(j):
            if (direct>>i)&1:
                past[j]|=past[i]  # earlier rows already transitively closed
    # Explicit verify every closure. Edge order by target index,
    # so all past[i] are already transitively closed when j processed.
    for j in range(N):
        anc=past[j]
        while anc:
            low=anc&-anc;i=low.bit_length()-1;anc-=low
            assert past[i]&~past[j]==0
    return past
def features(past):
    intervals=[0,0,0,0]
    heights=[1]*N
    related=0
    for j in range(N):
        anc=past[j]
        related+=anc.bit_count()
        while anc:
            low=anc&-anc;i=low.bit_length()-1;anc-=low
            inside=sum(1 for k in range(i+1,j) if (past[j]>>k)&1 and (past[k]>>i)&1)
            if inside<4:intervals[inside]+=1
            heights[j]=max(heights[j],heights[i]+1)
    n1,n2,n3,n4=intervals
    return {"N1_N4":intervals,"S2_bracket":N-2*n1+4*n2-2*n3,
        "S4_bracket":N-n1+9*n2-16*n3+8*n4,
        "longest_chain":max(heights),"related_pairs":related}
def main():
    vals=np.empty(HISTORIES,int)
    s2=np.empty(HISTORIES,int)
    heights=np.empty(HISTORIES,int)
    counts=collections.Counter()
    collision={}
    witness=None
    for mask in range(HISTORIES):
        x=features(closure(mask))
        vals[mask]=x["S4_bracket"];s2[mask]=x["S2_bracket"]
        heights[mask]=x["longest_chain"]
        counts[tuple(x["N1_N4"])]+=1
        key=x["S4_bracket"]
        if key in collision and collision[key][1]!=x["longest_chain"] and witness is None:
            witness={"same_S4_bracket":key,"histories":[collision[key][0],mask],
              "different_longest_chains":[collision[key][1],x["longest_chain"]]}
        if key not in collision:collision[key]=(mask,x["longest_chain"])
    assert witness is not None
    assert len(vals)==32768
    assert vals.min()<vals.max()
    assert len(set(vals.tolist()))<len(counts)
    records=[]
    for kappa in (0.,.1,.25,.5,1.,2.,3.,math.pi):
        z=complex(np.mean(np.exp(1j*kappa*vals)))
        records.append({"kappa":kappa,
          "Re_ensemble_amplitude":z.real,"Im_ensemble_amplitude":z.imag,
          "absolute_amplitude":abs(z),
          "effective_coherence_fraction_modulus_squared":abs(z)**2})
    assert abs(records[0]["absolute_amplitude"]-1)<1e-15
    assert records[4]["absolute_amplitude"]<.75
    euclid=[]
    for beta in (0.,.02,.1,.3,.6):
        weights=np.exp(-beta*(vals-vals.min()))
        denom=weights.sum()
        meanheight=float(np.dot(weights,heights)/denom)
        euclid.append({"beta":beta,"weighted_mean_chain_height":meanheight,
          "weighted_mean_S4_bracket":float(np.dot(weights,vals)/denom),
          "log_mean_e_minus_beta_S":float(-beta*vals.min()+math.log(float(denom)/HISTORIES))})
    # Barriers: same S4 bracket can represent different causal orders,
    # hence action scalar does not determine causal geometry.
    out={"status":"PASS_EXACT_FINITE_BDG_PHASE_SUM_AND_NONINJECTIVE_ACTION",
      "N_events":N,"chronological_edge_bits":len(EDGES),"edge_bit_histories":HISTORIES,
      "measure":"Uniform over 2^15 directed chronological-edge presentations; multiple different edge masks can close to SAME causal partial order, so NOT uniform over posets or diffeo-invariant histories.",
      "N_k_def":"N_k counts causally related pairs with k-1 interior elements, k=1,2,3,4.",
      "B2":"N-2N1+4N2-2N3",
      "B4":"N-N1+9N2-16N3+8N4",
      "count_unique_B4":len(set(vals.tolist())),
      "count_unique_interval_vectors":len(counts),
      "B4_min_max":[int(vals.min()),int(vals.max())],
      "histories_at_min_B4":int(np.sum(vals==vals.min())),
      "histories_at_max_B4":int(np.sum(vals==vals.max())),
      "histogram_B4":{str(v):int(n) for v,n in sorted(collections.Counter(vals.tolist()).items())},
      "same_action_different_chain_height_counterexample":witness,
      "unitary_phase_weighted_partition_averages":records,
      "positive_weight_toy_bias":euclid,
      "scientific_conclusion":"A six-event BDG action-bracket, even given oscillatory phase weights, neither selects 3+1D manifoldlike geometry nor uniquely determines causal order. This is a finite-order interference study not dynamical quantum gravity.",
      "limitations":"Bare action brackets, no BDG scale factors/nonlocal smearing/boundaries, no path-integral measure or causal-set dynamics, label/DAG-presentation overcounting, no continuum or semiclassical Einstein equations.",
      "prior_art":["Adamson Wallden PRResearch 8 023188 (2026), doi:10.1103/qdst-yrh6",
        "Benincasa Dowker PRL104 181301 (2010)",
        "Surya causal set review 2025 exact B2/B4 interval brackets"]}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("CAUSAL_BDG_PHASE_PASS",len(set(vals.tolist())),witness,"kappa1",records[4]["absolute_amplitude"],flush=True)
    return out
if __name__=="__main__":main()
