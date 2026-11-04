#!/usr/bin/env python3
"""Rideout--Sorkin transitive-percolation specialization, exactly normalized
precursor probabilities, Monte Carlo causal-dimension falsifier and tilted
4D interval-action diagnostic. No dynamical emergence of dimension implied.
"""
from __future__ import annotations
from itertools import product
from pathlib import Path
from math import comb,log,exp
import json,runpy
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'2026_11_03_causal_growth_action_competition.json'
older=runpy.run_path(str(ROOT/'analysis'/'2026_11_03_causal_set_dimension_nulls.py'))
sprinkled=older['sprinkled'];order=older['order'];rstat=older['rstat']
height=older['longest'];intervals=older['interval_census']
def percolate(n,p,seed):
    rng=np.random.default_rng(seed)
    C=np.zeros((n,n),bool) # i has past j if C[i,j]
    # New event i chooses each existing j with p. Transitive closure
    # incorporates every ancestor of each chosen event.
    for i in range(n):
        chosen=np.flatnonzero(rng.random(i)<p)
        for j in chosen:
            C[i,j]=True;C[i]|=C[j]
    assert np.all((C.astype(np.int32)@C.astype(np.int32)>0)<=C)
    return C
def downset_normalization(C,p):
    n=len(C);total=0.
    for bits in product((False,True),repeat=n):
        mark=np.array(bits,bool)
        if any(mark[i] and np.any(C[i]&~mark) for i in range(n)):continue
        w=int(mark.sum())
        m=int(sum(mark[i] and not any(mark[j] and C[j,i] for j in range(n)) for i in range(n)))
        weight=p**m*(1-p)**(n-w)
        total+=weight
    assert abs(total-1)<1e-12,(C,total)
    return total
def features(C):
    ic=intervals(C)
    return {"comparable_fraction":rstat(C),"longest_chain":height(C),
       "interval_histogram_first4":{str(i):ic.get(str(i),0) for i in range(4)},
       "bdg_4d_bracket_NminusN0plus9N1minus16N2plus8N3":
           C.shape[0]-ic.get('0',0)+9*ic.get('1',0)-16*ic.get('2',0)+8*ic.get('3',0)}
def embed(n,d,s):
    C=order(sprinkled(d,n,s))
    return features(C)
def population(p,n,num,seedoffset):
    return [features(percolate(n,p,seedoffset+i)) for i in range(num)]
def meanfeature(A,key):
    return float(np.mean([v[key] for v in A]))
def run():
    # Exact normalized down-set evolution on the 4-antichain,
    # 4-chain and 2+2 poset at four sizes, several coupling values.
    C0=np.zeros((4,4),bool)
    C1=np.tril(np.ones((4,4),bool),-1)
    C2=np.zeros((4,4),bool);C2[1,0]=True;C2[3,2]=True
    for p in (.05,.2,.5,.83):
        for C in (C0,C1,C2):
            downset_normalization(C,p)
    # Flat parameter control, NOT postselected against held-out observables.
    n=72
    target_train=[embed(n,4,20261103+i) for i in range(18)]
    target_hold=[embed(n,4,20262000+i) for i in range(22)]
    target_train_r=meanfeature(target_train,'comparable_fraction')
    pgrid=(.002,.004,.006,.008,.01,.015,.02,.025,.03,.04,.055,.075,.10,.15,.22)
    sweep=[]
    for p in pgrid:
        block=population(p,n,32,100000+int(p*1e6))
        sweep.append({"p":p,
          "train_mean_comparable":meanfeature(block,'comparable_fraction'),
          "train_mean_height":meanfeature(block,'longest_chain'),
          "train_density_abs_error":abs(meanfeature(block,'comparable_fraction')-target_train_r)})
    selected=min(sweep,key=lambda x:x['train_density_abs_error'])['p']
    # One statistic chosen in training, then other statistics tested blind.
    controls=population(selected,n,128,290000)
    def profile(A):
        s=meanfeature(A,'comparable_fraction');h=meanfeature(A,'longest_chain')
        cnt=np.array([[a['interval_histogram_first4'][str(i)] for i in range(4)] for a in A],float)
        return {"mean_density":s,"mean_height":h,
            "mean_counts_first4":cnt.mean(axis=0).tolist(),
            "mean_4d_BDG_bracket":meanfeature(A,'bdg_4d_bracket_NminusN0plus9N1minus16N2plus8N3')}
    train=profile(target_train);hold=profile(target_hold);null=profile(controls)
    # Optional discretized action reweighting: the chosen d=4 BDG coefficient
    # presupposes d=4. Not a demonstration of emergent dimension.
    actions=np.array([z['bdg_4d_bracket_NminusN0plus9N1minus16N2plus8N3'] for z in controls])
    tilted=[]
    for beta in (-.5,-.2,0.,.2,.5):
        logw=-beta*(actions-actions.mean())/n
        w=np.exp(logw-logw.max());w/=w.sum()
        ESS=float(1/np.dot(w,w))
        tilted.append({"beta":beta,
           "effective_sample_size":ESS,
           "weighted_density":float(np.dot(w,[a['comparable_fraction'] for a in controls])),
           "weighted_height":float(np.dot(w,[a['longest_chain'] for a in controls])),
           "weighted_action":float(np.dot(w,actions)),
           "action_formula":"4D input: N-N0+9N1-16N2+8N3"})
    out={"status":"PASS_EXACT_CSG_NORMALIZATION_AND_HELDOUT_CAUSAL_FALSIFIER",
      "source":"Rideout-Sorkin CSG transitive-percolation t_k=t**k, p=t/(1+t), λ(varpi,m)=t^m (1+t)^(varpi-m), λ(n,0)=(1+t)^n.",
      "exact_transition":"A specified precursor/downset of size varpi, with m maximal elements, has probability p**m*(1-p)**(n-varpi). Derived from independent prior-event links and transitive closure.",
      "normalized_exact_predecessor_posets":"4-element antichain, chain and 2+2, at 4 different p values; sums 1.",
      "scan_p_only_by_training_density":sweep,"frozen_p":selected,
      "sprinkling_dimension_4_supplied":True,"n":n,
      "target_train":train,"target_holdout":hold,
      "frozen_growth_model_holdout":null,
      "tilted_D4_BDG_like_action":tilted,
      "no_go_scope":"Transitive percolation obeys a classical general-covariant sequential-growth specialization, but choosing p by one causal-density metric does not ensure 4D manifoldlikeness. The 4D interval-action coefficients were chosen by assuming dimension four, so reweighting them cannot establish spontaneous dimension selection.",
      "sampling_scope":"Finite N=72, finite Monte Carlo ensembles; no finite-size extrapolation, Euclidean action integral, proof of intrinsic causet manifoldlikeness or continuum Einstein equation.",
      "prior":["https://doi.org/10.1103/PhysRevD.61.024002","https://doi.org/10.1007/s41114-019-0023-1"]
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print("CAUSAL CSG",{"train_r":train['mean_density'],"p_frozen":selected,"hold_r":hold['mean_density'],"null_r":null['mean_density'],"hold_height":hold['mean_height'],"null_height":null['mean_height'],"ESS_beta05":tilted[-1]['effective_sample_size']},flush=True)
if __name__=="__main__":run()
