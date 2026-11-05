#!/usr/bin/env python3
"""Front 4: exact causal-set measure ambiguity and transitive-closure bias.

For all 2^15 forward-edge DAG presentations on chronological labels
N=6, deduplicate equal transitive closures to naturally labelled
causal posets. For each poset count redundant transitive edges R-L
where L=#covers in Hasse diagram. Exactly 2^(R-L) DAG presentations
close to it (all covers mandatory, all others optional).
Compare uniform-over-presentations vs uniform-over-distinct-posets
BDG phase sum and chain-height distribution. Neither is the correct
unlabeled diffeo-invariant quantum-gravity measure.
"""
from __future__ import annotations
import collections,json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_causal_exact_measure_entropy_bias.json"
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261105_causal_bdg_history_interference import N,HISTORIES,closure,features
def covers_count(p):
    ret=0
    for j in range(N):
        for i in range(j):
            if not (p[j]>>i)&1:continue
            intermediate=any(((p[j]>>k)&1) and ((p[k]>>i)&1) for k in range(i+1,j))
            if not intermediate:ret+=1
    return ret
def main():
    counter=collections.Counter()
    for mask in range(HISTORIES):
        counter[tuple(closure(mask))]+=1
    assert sum(counter.values())==HISTORIES
    reps=[]
    for tup,mult in counter.items():
        f=features(list(tup))
        R=f["related_pairs"];L=covers_count(tup)
        assert mult==2**(R-L), (tup,mult,R,L)
        reps.append({"multiplicity":mult,"related":R,"covers":L,
          "chain_height":f["longest_chain"],"B4":f["S4_bracket"]})
    vals=np.array([r["B4"] for r in reps],float)
    weights=np.array([r["multiplicity"] for r in reps],float)
    chains=np.array([r["chain_height"] for r in reps],float)
    assert np.sum(weights)==HISTORIES
    samples=[]
    for kappa in (0,.1,.25,.5,1,2,math.pi):
        ph=np.exp(1j*kappa*vals)
        Z_dag=complex(np.sum(weights*ph)/sum(weights))
        Z_pos=complex(np.mean(ph))
        samples.append({"kappa":kappa,
           "presentation_measure_abs_amplitude":abs(Z_dag),
           "distinct_naturally_labeled_poset_measure_abs_amplitude":abs(Z_pos),
           "absolute_complex_amplitude_disagreement":abs(Z_dag-Z_pos),
           "presentation_measure_amplitude_real_imag":[Z_dag.real,Z_dag.imag],
           "poset_measure_amplitude_real_imag":[Z_pos.real,Z_pos.imag]})
    assert abs(samples[0]["absolute_complex_amplitude_disagreement"])<1e-15
    assert max(x["absolute_complex_amplitude_disagreement"] for x in samples[1:])>.03
    multi=collections.Counter(r["multiplicity"] for r in reps)
    heights=collections.Counter()
    for r in reps:
        z=heights[r["chain_height"]]
        heights[r["chain_height"]]=(z[0]+1,z[1]+r["multiplicity"]) if z else (1,r["multiplicity"])
    meanDAG=float(np.average(chains,weights=weights))
    meanPos=float(np.mean(chains))
    assert abs(meanDAG-meanPos)>.05
    # Unweighted poset ensemble is only a partial correction:
    # every chronological total order has many natural labels, and
    # isomorphic unlabeled posets still receive different weights.
    out={"status":"PASS_EXACT_SIX_EVENT_PRESENTATION_TO_POSET_MEASURE_OBSTRUCTION",
      "N":N,"DAG_forward_edge_presentations":HISTORIES,
      "unique_transitively_closed_posets_with_fixed_natural_chronological_labels":len(counter),
      "exact_multiplicity_law":"m(C)=2^(R(C)-L(C)); R=#related pairs, L=#Hasse cover relations",
      "multiplicity_distribution":{str(k):v for k,v in sorted(multi.items())},
      "maximum_presentation_multiplicity":int(max(weights)),
      "most_common_multiplicity":multi.most_common(1)[0][0],
      "mean_chain_height_DAG_presentation_measure":meanDAG,
      "mean_chain_height_unique_naturally_labeled_poset_measure":meanPos,
      "chain_height_histogram":{"height_"+str(k):{"unique_posets":v[0],"DAG_presentations":v[1]} for k,v in sorted(heights.items())},
      "phase_partition_function_measure_comparison":samples,
      "scientific_result":"Transitive-closure representation inserts an exact exponentially varying entropy factor into the path sum. Even after removing that multiplicity the naturally-labelled uniform measure still is not a covariant/unlabeled causal-set gravity measure. No 4D selection or continuum established.",
      "pitfalls":"These are partial orders on a fixed chronological index; dedup by closure is NOT quotient by all relabelings or automorphism groups. No BDG boundary term/action normalization, no quantum measure or causality constraints chosen by an action.",
      "prior_art":["Rideout Sorkin causal sequential growth 2000","Causal sets and an emerging continuum GRG 2024","Adamson Wallden PRResearch 8 023188 2026"]}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("CAUSAL_MEASURE_PASS posets",len(counter),"multmax",int(max(weights)),
      "Z1",samples[4], "heights",meanDAG,meanPos,flush=True)
    return out
if __name__=="__main__":main()
