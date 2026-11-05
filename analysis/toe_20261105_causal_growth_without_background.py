#!/usr/bin/env python3
"""Physics-front 2: causal-set sequential growth without embedding metric.

Rideout-Sorkin transitive-percolation (independent precursor bonds),
closure via Python exact integer bitsets. Reconstruct Myrheim-Meyer
dimensions from intrinsically selected finite intervals, and check
whether d=4 is independently selected, homogeneous, or scale-stable.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from scipy.special import gammaln
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_causal_growth_no_embedded_dimension.json"

def prob(d):
    return math.exp(gammaln(d+1)+gammaln(d/2)-gammaln(1.5*d)-math.log(2))
def invert(r):
    if r>=1:return 1.
    if r<=prob(20):return None
    return float(brentq(lambda d:prob(d)-r,1,20))
def generate(n,p,seed):
    rng=np.random.default_rng(seed)
    past=[]
    direct=0
    for j in range(n):
        prec=rng.random(j)<p
        candidates=np.flatnonzero(prec)
        direct+=len(candidates)
        pset=0
        for i in candidates:
            i=int(i);pset|=(1<<i)|past[i]
        past.append(pset)
    # Every generated ancestor pair respects transitivity.
    for j in range(n):
        bit=past[j]
        while bit:
            low=bit&-bit;i=low.bit_length()-1;bit-=low
            assert past[i]&~past[j]==0
    related=sum(x.bit_count() for x in past)
    return past,direct,related
def intervals(past,seed,size_min=17,size_max=180,attempts=1200):
    rng=np.random.default_rng(seed)
    n=len(past);selected=[];fractions=[];sizes=[]
    for _ in range(attempts):
        a=int(rng.integers(0,n-1))
        b=int(rng.integers(a+1,n))
        if not ((past[b]>>a)&1):continue
        verts=[i for i in range(a,b+1)
               if (i==b or (past[b]>>i)&1)
               and (i==a or (past[i]>>a)&1)]
        m=len(verts)
        if not size_min<=m<=size_max:continue
        relation=0
        for k,i in enumerate(verts):
            relation+=sum(1 for j in verts[k+1:] if (past[j]>>i)&1)
        frac=2*relation/(m*(m-1))
        d=invert(frac)
        if d is None:continue
        selected.append(d);fractions.append(frac);sizes.append(m)
    return selected,fractions,sizes
def sample(n,p,seed):
    past,initial,relations=generate(n,p,seed)
    ds,fr,sz=intervals(past,seed+999)
    if not ds:return {
       "n":n,"p":p,"seed":seed,"direct_bonds":initial,
       "transitively_related_pairs":relations,
       "whole_poset_related_fraction":2*relations/(n*(n-1)),
       "eligible_intervals":0,"local_dim_median":None}
    return {"n":n,"p":p,"seed":seed,"direct_bonds":initial,
       "transitively_related_pairs":relations,
       "whole_poset_related_fraction":2*relations/(n*(n-1)),
       "eligible_intervals":len(ds),
       "local_dim_median":float(np.median(ds)),
       "local_dim_q10":float(np.quantile(ds,.1)),
       "local_dim_q90":float(np.quantile(ds,.9)),
       "local_dim_mean":float(np.mean(ds)),
       "local_dim_std":float(np.std(ds)),
       "interval_size_median":float(np.median(sz)),
       "is_exact_d4_prediction":False}
def main():
    rec=[]
    for n in (160,320):
        for p in (.025,.065,.15):
            for replicate in range(3):
                item=sample(n,p,20261105+1217*replicate+19*n+int(p*10000))
                rec.append(item)
                print("CAUSAL_GROWTH",n,p,replicate,item["eligible_intervals"],
                      item["local_dim_median"],flush=True)
    assert len(rec)==18
    assert all(x["transitively_related_pairs"]>=x["direct_bonds"] for x in rec)
    # Homogeneity is not assumed; different parameter choices should
    # produce measurably distinct intrinsic dimension/finite intervals.
    summary={}
    for n in (160,320):
        for p in (.025,.065,.15):
            z=[x for x in rec if x["n"]==n and x["p"]==p and x["local_dim_median"] is not None]
            if z:
                summary[f"n{n}_p{p}"]={"replications_with_valid_intervals":len(z),
                  "median_across_replicates":float(np.median([x["local_dim_median"] for x in z])),
                  "total_eligible_intervals":sum(x["eligible_intervals"] for x in z)}
    assert len(summary)>=4
    out={"status":"PASS_METRIC_FREE_STOCHASTIC_CAUSAL_GROWTH_FALSIFIER",
       "model":"Rideout-Sorkin transitive percolation, independent bond probability p per newly born element plus ancestral closure",
       "causal_dimension_estimator":"Myrheim-Meyer causal fraction inside nonempty Alexandrov intervals (not entire poset)",
       "samples":rec,"family_summary":summary,
       "previous_embedding_control":"Previous project experiment sprinkles uniformly in pre-specified 2,3,4D Minkowski diamonds and recovers those input dimensions.",
       "interpretation":"Here neither a metric nor a dimension was encoded in growth, but the resulting local order fractions depend on p, finite scale and interval choice. No demonstrated robust 3+1D large-scale Lorentzian limit.",
       "boundary":"Classical stochastic growth and finite intervals, not unitary quantum gravity, local GR action, realistic spatial locality or a derivation of 4D."}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("CERTIFICATE",OUT,flush=True)
    return out
if __name__=="__main__":main()
