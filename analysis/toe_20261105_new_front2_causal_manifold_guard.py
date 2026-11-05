#!/usr/bin/env python3
"""TOE front 2: match a causal statistic yet fail manifold reconstruction.

Generate Minkowski-4 Alexandrov sprinklings and metric-free transitive
percolation. Calibrate the latter's bond p ONLY to match whole-poset
order fraction ~0.1. Check local-interval Myrheim-Meyer dimensions and
chain statistics. Matching one graph statistic is not dynamical
selection of a 3+1-dimensional manifold.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_new_front2_causal_matching_no_manifold.json"
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261105_causal_growth_without_background import generate,intervals,prob,invert
from toe_20261105_physics_first_consistency_filters import sprinkle_interval

def interior_intervals(past,seed,attempts=4500):
    """Estimate d from interval INTERIOR, not fixed causal endpoints.

    Including a and b in each finite interval forces 2(m-2)+1
    extra comparable pairs and biases dimension downward.
    """
    rng=np.random.default_rng(seed);n=len(past)
    ds=[];sizes=[]
    for _ in range(attempts):
        a=int(rng.integers(0,n-1))
        b=int(rng.integers(a+1,n))
        if not ((past[b]>>a)&1):continue
        inside=[i for i in range(a+1,b) if (past[b]>>i)&1 and (past[i]>>a)&1]
        m=len(inside)
        if not 12<=m<=180:continue
        R=sum(sum((past[j]>>i)&1 for j in inside[k+1:]) for k,i in enumerate(inside))
        frac=2*R/(m*(m-1))
        dd=invert(frac)
        if dd is None:continue
        ds.append(dd);sizes.append(m)
    return ds,sizes


def matrix_minkowski(n,seed):
    t,x=sprinkle_interval(4,n,np.random.default_rng(seed))
    order=np.argsort(t)
    t=t[order];x=x[order]
    past=[];relations=0
    for j in range(n):
        earlier=t[j]-t[:j]
        dist2=np.sum((x[:j]-x[j])**2,axis=1)
        rel=(earlier**2)>=dist2
        bits=0
        for i in np.flatnonzero(rel):bits|=1<<int(i)
        past.append(bits);relations+=int(rel.sum())
    return past,relations

def summarize(past,seed):
    n=len(past)
    naive,_,_=intervals(past,seed,size_min=13,size_max=180,attempts=2000)
    dims,sz=interior_intervals(past,seed,attempts=4500)
    # Height via recurrence since temporal index is topological order.
    heights=[]
    for anc in past:
        h=1
        while anc:
            bit=anc&-anc;i=bit.bit_length()-1;anc-=bit
            if heights[i]+1>h:h=heights[i]+1
        heights.append(h)
    return {"whole_related_fraction":2*sum(b.bit_count() for b in past)/(n*(n-1)),
       "longest_causal_chain":max(heights),
       "local_interval_count":len(dims),
       "naive_endpoint_included_dimension_median":float(np.median(naive)) if naive else None,
       "local_interval_dimension_median":float(np.median(dims)) if dims else None,
       "local_interval_dimension_q20":float(np.quantile(dims,.2)) if dims else None,
       "local_interval_dimension_q80":float(np.quantile(dims,.8)) if dims else None,
       "median_interval_size":float(np.median(sz)) if sz else None}
def main():
    n=420
    target=prob(4)
    scan=[]
    for p in np.linspace(.002,.065,20):
        x=[]
        for k in range(3):
            past,direct,nrel=generate(n,float(p),260011+(k*179))
            x.append(2*nrel/(n*(n-1)))
        scan.append((float(p),float(np.mean(x))))
    order=sorted(scan)
    bracket=next((a,b) for a,b in zip(order[:-1],order[1:]) if a[1]<=target<=b[1])
    lo,hi=bracket[0][0],bracket[1][0]
    for _ in range(14):
        mid=(lo+hi)/2
        empirical=[]
        for k in range(3):
            _,_,rel=generate(n,mid,260011+(k*179))
            empirical.append(2*rel/(n*(n-1)))
        f=float(np.mean(empirical))
        scan.append((mid,f))
        if f<target:lo=mid
        else:hi=mid
    best=min(scan,key=lambda z:abs(z[1]-target))
    assert abs(best[1]-target)<.001
    records={"Minkowski_4_supplied":[],"causal_percolation_metric_free":[]}
    for k in range(5):
        past,_=matrix_minkowski(n,3200+k)
        records["Minkowski_4_supplied"].append(summarize(past,9000+k))
        pset,_,_=generate(n,best[0],6200+k)
        records["causal_percolation_metric_free"].append(summarize(pset,10000+k))
    means={}
    for name,group in records.items():
        means[name]={
          "related_fraction":float(np.mean([a["whole_related_fraction"] for a in group])),
          "chain_height":float(np.mean([a["longest_causal_chain"] for a in group])),
          "local_dimension":float(np.median([a["local_interval_dimension_median"]
                        for a in group if a["local_interval_dimension_median"] is not None])),
          "intervals_total":sum(a["local_interval_count"] for a in group)}
    print("CAUSAL_DEBUG_MATCH",best,"MEANS",means,flush=True)
    assert abs(means["Minkowski_4_supplied"]["related_fraction"]-target)<.018
    assert abs(means["causal_percolation_metric_free"]["related_fraction"]-target)<.06
    assert abs(means["Minkowski_4_supplied"]["local_dimension"]-4)<1.
    assert abs(means["causal_percolation_metric_free"]["local_dimension"]-4)>1.
    out={"status":"PASS_CAUSAL_GLOBAL_MATCH_LOCAL_MANIFOLD_FAIL",
       "n_events_each":n,"replicates_each":5,
       "target_Minkowski4_global_comparability":target,
       "calibration_grid":[{"p":p,"global_relation_fraction":f} for p,f in scan],
       "best_matched_metric_free_growth_probability":best[0],
       "independent_seed_replicates":records,"ensemble_summary":means,
       "interpretation":"Global causal ordering fraction can be tuned to match a supplied dimension-four Minkowski sprinkling while the local interval dimension and longest-chain distribution still disagree. No dynamical selection of a manifoldlike 3+1D quantum spacetime.",
       "scope":"Neither model has a quantum action; percolation is a known sequential growth toy. The dimension estimator assumes continuum Minkowski interval behavior even when testing nonmanifold causal growth.",
       "prior_art":["Rideout & Sorkin PRD61 024002 transitive percolation","Myrheim-Meyer dimension estimator","Meyer 2026 Phys Rev D doi:10.1103/klxp-f94q"]}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("CAUSAL_MATCH",best,"SUMMARIES",means,flush=True)
    return out
if __name__=="__main__":main()
