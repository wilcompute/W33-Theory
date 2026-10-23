#!/usr/bin/env python3
"""Second-order (two Z faults) expansion of native Pass12189 heralded magic.

Enumerates all 780 site pairs exactly by integer phase histograms of the
59,049 CSS codewords in each logical coset. No false finite-p threshold.
"""
from __future__ import annotations
from itertools import combinations, product
from pathlib import Path
import json, numpy as np
try:
 from analysis.w33_20261022_five_toe_frontiers import point_geometry
except ImportError:
 from w33_20261022_five_toe_frontiers import point_geometry

ROOT=Path(__file__).resolve().parents[1]

def run():
    _,B,C=point_geometry()
    assert C.shape==(10,40)
    u=np.zeros(40,dtype=np.uint8);u[:4]=1
    coeff=np.array(list(product(range(3),repeat=10)),dtype=np.uint8)
    words=(coeff.astype(np.int16)@C.astype(np.int16)%3).astype(np.uint8)
    N=len(words); assert N==59049
    cosets=np.array([(words+t*u)%3 for t in range(3)],dtype=np.uint8)
    phases=(cosets.sum(axis=2)%9).astype(np.uint8)
    zeta=np.exp(2j*np.pi/9)
    powers=zeta**np.arange(9)
    def instrument(fault_sites):
        counts=[]
        for t in range(3):
            h=phases[t].astype(np.int16).copy()
            for site in fault_sites:
                h+=3*cosets[t,:,site]
            hist=np.bincount(h%9,minlength=9)
            counts.append(hist.tolist())
        amplitudes=np.array([np.dot(h,powers)/N for h in counts])
        success=float(np.vdot(amplitudes,amplitudes).real/3)
        return counts,amplitudes,success
    counts0,a0,s0=instrument(())
    assert abs(s0-29/81)<1e-12,(s0,counts0,C.shape,words.shape,cosets.shape)
    ideal=a0/np.linalg.norm(a0)
    sing=[]
    for i in range(40):
        _,aa,s=instrument((i,))
        f=float(abs(np.vdot(ideal,aa))**2/(np.vdot(aa,aa).real)) if s>1e-20 else None
        sing.append((s,s*f if f is not None else 0.,f))
    previous=json.loads((ROOT/"data/w33_pass12189_12193_five_bridges.json").read_text())["magic"]
    for i,(s,_,f) in enumerate(sing):
        assert np.isclose(s,previous["single_Z_after_gate_controls"][i]["success"],atol=2e-12)
        ff=previous["single_Z_after_gate_controls"][i]["fidelity_to_ideal"]
        if ff is not None and s>1e-20:assert np.isclose(f,ff,atol=2e-12)
    doubles=[]
    for i,j in combinations(range(40),2):
        hist,aa,s=instrument((i,j))
        f=float(abs(np.vdot(ideal,aa))**2/(np.vdot(aa,aa).real)) if s>1e-19 else None
        remainders=[[h[a]-h[a+6] for a in range(3)]+
                    [h[a+3]-h[a+6] for a in range(3)] for h in hist]
        exact_nonzero=any(any(x!=0 for x in r) for r in remainders)
        assert exact_nonzero==(s>1e-12), (i,j,s,remainders)
        doubles.append({"sites":[i,j],"success":s,"fidelity":f,
                        "exact_cyclotomic_nonzero":exact_nonzero,
                        "cyclotomic_remainders":remainders if exact_nonzero else None,
                        "histograms":hist if exact_nonzero else None})
    accepted=[r for r in doubles if r["success"]>1e-12]
    S1=-40*s0+sum(s for s,_,_ in sing)
    S2=780*s0-39*sum(s for s,_,_ in sing)+sum(r["success"] for r in doubles)
    N1=-40*s0+sum(v for s,v,f in sing)
    N2=780*s0-39*sum(v for s,v,f in sing)+sum(r["success"]*r["fidelity"] for r in accepted)
    f1=(N1-S1)/s0
    f2=(N2-S2)/s0-f1*S1/s0
    assert abs(S1+128/9)<1e-10
    assert abs(f1+228/841)<1e-10
    by_support={}
    for r in accepted:
        count=sum(i<4 for i in r["sites"])
        name=f"{count}_of_two_in_u_support"
        if name not in by_support:by_support[name]={"count":0,"sum_success":0.,"sum_weighted_fidelity":0.}
        by_support[name]["count"]+=1
        by_support[name]["sum_success"]+=r["success"]
        by_support[name]["sum_weighted_fidelity"]+=r["success"]*r["fidelity"]
    return {"status":"EXACT_DOUBLE_SITE_Z_FROZEN_PHASE_CENSUS",
      "logical_codewords_per_coset":N,"all_double_site_pairs":len(doubles),
      "accepted_double_fault_pairs":len(accepted),
      "accepted_pair_classes":by_support,
      "all_accepted_pairs":[{"sites":r["sites"],"success":r["success"],
          "fidelity":r["fidelity"],"phase_histograms":r["histograms"],
          "Phi9_remainders":r["cyclotomic_remainders"]} for r in accepted],
      "exact_rejection_certificate":"A histogram h[0..8] evaluates to zero at zeta9 iff all six integers h_j-h_{j+6} (j=0,1,2), h_{j+3}-h_{j+6} (j=0,1,2) vanish, because Phi9(x)=x^6+x^3+1 is the minimal polynomial.",
      "P_success_series":{"constant":s0,"linear":S1,"quadratic":S2},
      "conditional_fidelity_series":{"constant":1.,"linear":f1,"quadratic":f2},
      "equations":"P=S0+S1*p+S2*p^2+O(p^3); F=1+f1*p+f2*p^2+O(p^3) for independent Bernoulli Z faults on each of 40 locations.",
      "boundary":"Exact 0,1,2 simultaneous Z faults; not a full physical error model, not a threshold; higher faults omitted."}

if __name__=="__main__":
 import sys
 out=json.dumps(run(),indent=2)+"\n"
 if len(sys.argv)>1:Path(sys.argv[1]).write_text(out,encoding="utf-8")
 else:print(out)
