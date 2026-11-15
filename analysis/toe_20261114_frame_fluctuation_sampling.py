#!/usr/bin/env python3
"""Recover W33 symplectic orthogonality from random apartment-frame couplings.

Prior art: 1620 apartment ↔ projective symplectic frame (Pass4474, TOE23).
This is a separate measurement/sample-complexity falsifier of the
new exact apartment two-neighbor covariance census.
"""
from itertools import product,combinations
from collections import Counter
from pathlib import Path
from math import log,ceil
import numpy as np
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261114_frame_fluctuation_sampling.json"

def run(n_samples=10000,seed=20261114):
    field=list(product(range(3),repeat=4))
    nonzero=[v for v in field if any(v)]
    def ray(x):
        i=next(k for k,c in enumerate(x) if c)
        return x if x[i]==1 else tuple(2*v%3 for v in x)
    rays=sorted(set(ray(v) for v in nonzero))
    def omega(a,b):
        return (a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1])%3
    frames=[]
    for four in combinations(range(40),4):
        bad=[(i,j) for i,j in combinations(range(4),2) if omega(rays[four[i]],rays[four[j]])]
        if len(bad)==2 and len({u for p in bad for u in p})==4:
            frames.append({tuple(s*v%3 for v in rays[k]) for k in four for s in (1,2)})
    assert len(frames)==1620
    V={v:i for i,v in enumerate(nonzero)}
    inc=np.zeros((len(frames),80),dtype=np.int8)
    for n,S in enumerate(frames):
        for v in S:inc[n,V[v]]=1
    assert (inc.sum(axis=0)==162).all()
    rng=np.random.default_rng(seed)
    draws=rng.integers(0,1620,size=n_samples)
    M=inc[draws].astype(np.int32)
    counts=M.T@M
    pred=Counter(); truth=Counter(); errs=Counter()
    thresh_high=(.1+1/60)/2
    thresh_low=(1/60+1/270)/2
    labels={"opposite":0,"orthogonal":1,"nonorthogonal":2}
    for i in range(80):
        for j in range(i+1,80):
            a,b=nonzero[i],nonzero[j]
            exact=("opposite" if ray(a)==ray(b) else
                  "orthogonal" if omega(a,b)==0 else "nonorthogonal")
            freq=float(counts[i,j])/n_samples
            classification=("opposite" if freq>thresh_high else
                            "orthogonal" if freq>thresh_low else "nonorthogonal")
            truth[exact]+=1;pred[classification]+=1
            if exact!=classification:errs[f"{exact}->{classification}"]+=1
    assert truth=={"opposite":40,"orthogonal":960,"nonorthogonal":2160}
    # A universal IID Hoeffding union bound for all 3160 pair statistics:
    delta=(1/60-1/270)/2
    guaranteed=ceil(log(2*3160/.01)/(2*delta**2))
    assert guaranteed==158972
    result={
      "status":"FINITE_SAMPLE_FRAME_COVARIANCE_RECONSTRUCTION",
      "n_apartments":1620,"n_nonzero_displacements":80,
      "n_random_frames_with_replacement":n_samples,
      "random_seed":seed,
      "true_pair_counts":dict(truth),
      "classified_pair_counts":dict(pred),
      "misclassification_counts":dict(errs),
      "empirical_accuracy":1-sum(errs.values())/3160,
      "separation_gap_orthogonal_vs_nonorthogonal":1/60-1/270,
      "threshold_high":thresh_high,"threshold_low":thresh_low,
      "Hoeffding_union_sufficient_frames_99pct_all_pairs":guaranteed,
      "limits":"10,000-frame run is a seeded Monte Carlo, not a 99% proof. 158,972 is a conservative IID sufficient bound for all 3160 simultaneous pair classifications, not a tight sample optimum. Model assumes directly observable frame-selecting couplings."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(result["status"],"accuracy",result["empirical_accuracy"],
          "errors",result["misclassification_counts"],flush=True)
    return result

if __name__=="__main__":run()
