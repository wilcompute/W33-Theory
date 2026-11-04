#!/usr/bin/env python3
"""Precommitted, density-trained comparison of two very different random
causal growth laws against held-out 4D Minkowski-diamond statistics.

Training fits ONE causal pair-density scalar. Chain height, connected
components and interval profiles are held out; input d=4 is not emergent.
"""
from __future__ import annotations
from pathlib import Path
import json,runpy
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OLD=runpy.run_path(str(ROOT/'analysis'/'2026_11_03_causal_set_dimension_nulls.py'))
CSG=runpy.run_path(str(ROOT/'analysis'/'2026_11_03_csg_action_heldout.py'))
OUT=ROOT/'data'/'2026_11_03_blind_two_growth_causal_competition.json'
n=72
def chains(n,k,seed):
    rng=np.random.default_rng(seed)
    assign=rng.integers(0,k,size=n)
    C=np.zeros((n,n),bool)
    for j in range(n):
        C[j,:j]=assign[:j]==assign[j]
    return C
def feat(C):
    density=OLD['rstat'](C)
    h=OLD['longest'](C)
    cnt=OLD['interval_census'](C)
    total=max(1,int(C.sum()))
    G=nx.from_numpy_array(C|C.T)
    return {"pair_fraction":density,"longest_chain":h,
       "comparability_components":nx.number_connected_components(G),
       "interval_frequency_first_four":[cnt.get(str(i),0)/total for i in range(4)]}
def spr(seed):
    return OLD['order'](OLD['sprinkled'](4,n,seed))
def grow(seed,p):return CSG['percolate'](n,p,seed)
def ensemble(model,param,count,seed):
    return [feat(model(n,param,seed+i) if model==chains else grow(seed+i,param)) for i in range(count)]
def means(data):
    return {"pair_fraction":float(np.mean([x['pair_fraction'] for x in data])),
       "longest_chain":float(np.mean([x['longest_chain'] for x in data])),
       "comparability_components":float(np.mean([x['comparability_components'] for x in data])),
       "interval_frequency_first_four":np.mean([x['interval_frequency_first_four'] for x in data],axis=0).tolist()}
def run():
    train=[feat(spr(39000+i)) for i in range(15)]
    held=[feat(spr(49000+i)) for i in range(36)]
    target=means(train)['pair_fraction']
    candidates={"transitive_percolation":[.005,.01,.015,.02,.025,.03,.035,.04,.045,.05,.06,.08,.1],
                "disjoint_independent_chains":list(range(4,24))}
    selection={};train_metrics={}
    for kind,grid in candidates.items():
        for param in grid:
            model=chains if kind.startswith('disjoint') else grow
            data=ensemble(model,param,22,100000+(int(param*1e5) if kind.startswith('transitive') else param*300))
            value=means(data)["pair_fraction"]
            train_metrics[f"{kind}:{param}"]=value
        selected=min(grid,key=lambda par:abs(train_metrics[f"{kind}:{par}"]-target))
        selection[kind]=selected
    holdout=means(held)
    nulls={}
    for i,(key,p) in enumerate(selection.items()):
        data=ensemble(chains if key.startswith('disjoint') else grow,p,100,230000+i*8000)
        row=means(data)
        row['L1_interval_profile_discrepancy']=float(np.sum(abs(np.array(row['interval_frequency_first_four'])-
                                                           np.array(holdout['interval_frequency_first_four']))))
        row['mean_chain_height_difference']=row['longest_chain']-holdout['longest_chain']
        row['mean_connected_component_difference']=row['comparability_components']-holdout['comparability_components']
        nulls[key]=row
        assert abs(row['pair_fraction']-holdout['pair_fraction'])<.025,(key,p,row,holdout)
        assert abs(row['mean_chain_height_difference'])>.8,(key,p,row,holdout)
    output={"status":"PASS_TWO_GROWTH_BLINDED_CAUSAL_NULLS",
      "N":n,
      "target_dimension_supplied":4,
      "only_training_observable":"Mean comparable-pair fraction from 15 independent 4D diamond sprinklings.",
      "target_training_density":target,
      "growth_candidate_parameters":candidates,
      "frozen_selected_params":selection,
      "heldout_36_target_sprinklings":holdout,
      "heldout_null_100_each":nulls,
      "independent_heldout_observables":["longest_chain","comparability_components","first_four_interval_frequency"],
      "disjoint_chain_null_description":"Each event independently samples one of k preexisting chains and is after all earlier events of that chain, incomparable to other chains. k fitted only on pair density, not geometry or interval data.",
      "CSG_null_description":"Rideout-Sorkin transitive-percolation specialization; new event selects each prior event with probability p, then takes transitive closure. p fitted only by training density.",
      "selection_warning":"Both candidate null families are separately calibrated to the 4D target on a single statistic; no candidate 4D dimension emerges in their microscopic dynamics. These are explicit out-of-sample statistical challenges for future dynamics, not a full Bayes model selection or proof no alternative growth law works.",
      "references":["https://doi.org/10.1103/PhysRevD.61.024002"]}
    OUT.write_text(json.dumps(output,indent=2)+"\n")
    print("BLIND",{"target":holdout,"selected":selection,"nulls":nulls},flush=True)
if __name__=="__main__":run()
