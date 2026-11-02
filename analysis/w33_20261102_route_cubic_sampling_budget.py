#!/usr/bin/env python3
"""Distribution-free classical-sampling budget for W33 route cubic tomography.

This applies to iid *uniform route-support samples* and their complete
40-coordinate incidence labels. It does NOT assume a quantum device can
jointly measure incompatible projective observables.
"""
from __future__ import annotations
import math
import json
from pathlib import Path

def bound(delta=0.01, flips=0.0):
    if not (0<delta<1 and 0<=flips<0.5):
        raise ValueError("require 0<delta<1 and 0<=flips<1/2")
    triples=math.comb(40,3)
    # Means: 1/2 for a W33 line triple, <=1/18 for any other triple.
    gap=0.5-1/18
    attenuation=(1-2*flips)**3
    margin=(gap/2)*attenuation
    # Hoeffding for [-1,1]-valued independent observations:
    # Pr(|mean-estimate| >= margin) <= 2 exp(-n*margin^2/2).
    n=math.ceil(2*math.log(2*triples/delta)/(margin**2))
    p=2*triples*math.exp(-n*margin**2/2)
    assert p<=delta+1e-12
    if n>0:
        assert 2*triples*math.exp(-(n-1)*margin**2/2)>delta-1e-12
    return dict(delta=delta, flips=flips, triples=triples,
        exact_true_mean="1/2",exact_max_false_mean="1/18",
        exact_threshold="5/18 (times attenuation)",
        gap=gap,attenuation=attenuation,margin=margin,
        iid_uniform_support_samples=n,union_bound_failure_probability=p,
        scope="Classical full-label oracle only; not quantum measurement feasibility")

if __name__=="__main__":
    b0=bound()
    assert b0["iid_uniform_support_samples"]==588
    b1=bound(flips=0.05)
    print("CLASSICAL_CUBIC_TOMOGRAPHY_HOEFFDING_PASS",b0["iid_uniform_support_samples"],b1["iid_uniform_support_samples"])
    out=Path(__file__).resolve().parents[1]/"data"/"w33_20261102_route_cubic_sampling_budget.json"
    out.write_text(json.dumps({"ideal":b0,"bit_flip_0p05":b1},indent=2)+"\n")
