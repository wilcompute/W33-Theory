#!/usr/bin/env python3
"""Fixed-label ideal three-photon W33-vs-dual hypothesis test.

Input triple is independent in BOTH graphs, preventing a hidden labeling
assumption. Purely ordinary quantum optics, not a new physical law.
"""
from __future__ import annotations
import json
from fractions import Fraction
from itertools import combinations,permutations
from pathlib import Path
import numpy as np
from scipy.stats import binom
from w33_20261029_three_photon_dual_discriminator import two_graphs

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261029_three_photon_1500_trial_protocol.json"
INPUT=(0,7,9)
SHOTS=1500
THRESHOLD=4

def event_numerators(M,inputs,outputs):
    H=2*np.ones((40,40),dtype=np.int64)-5*(np.eye(40,dtype=np.int64)+M)
    result=[]
    for out in outputs:
        amp=sum(int(np.prod([H[out[j],inputs[p[j]]] for j in range(3)]))
                for p in permutations(range(3)))
        result.append(amp*amp)
    return result

def main():
    A,B=two_graphs()
    assert all(A[i,j]==B[i,j]==0 for i,j in combinations(INPUT,2))
    neighbors=tuple(k for k in range(40) if all(A[k,j] for j in INPUT))
    assert neighbors==(4,14,23,32),neighbors
    events=tuple(combinations(neighbors,3))
    point=event_numerators(A,INPUT,events)
    dual=event_numerators(B,INPUT,events)
    assert point==[26244]*4,point
    assert dual==[784,1024,784,64],dual
    denominator=3375**2
    pW=Fraction(sum(point),denominator)
    pD=Fraction(sum(dual),denominator)
    assert pW==Fraction(144,15625)
    assert pD==Fraction(2656,11390625)
    fp=float(binom.sf(THRESHOLD-1,SHOTS,float(pD)))
    fn=float(binom.cdf(THRESHOLD-1,SHOTS,float(pW)))
    assert fp<0.001 and fn<0.001
    out={"status":"PASS",
      "scope":"Ideal port-labeled W(3,3) vs port-labeled dual, ordinary three-boson quantum optics",
      "input_ports":list(INPUT),"independent_in_both_graphs":True,
      "point_common_neighbor_ports":list(neighbors),
      "designated_output_triplets":[list(x) for x in events],
      "point_probability_numerators":point,"dual_probability_numerators":dual,
      "common_probability_denominator":denominator,
      "W33_event_probability":str(pW),"dual_event_probability":str(pD),
      "ideal_registered_three_photon_trials":SHOTS,
      "decision_rule":f"Choose W33 if event count >= {THRESHOLD}; else dual",
      "dual_false_W33_probability":fp,"W33_false_dual_probability":fn,
      "experimental_assumptions":"Exactly three perfectly indistinguishable input photons in each trial; lossless unitary; labeled modes and phase calibrations fixed; ideal number-resolving detection. All three-photon outcomes including output bunching count as trials.",
      "limits":"No physical hardware experiment, no beyond-quantum-mechanics prediction. Detection loss, distinguishability, systematic mode relabelings and uncertain calibration alter error rates."}
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS W33 probability",pW,"dual",pD,"n",SHOTS,
          "FP",fp,"FN",fn)
    return out
if __name__=="__main__":main()
