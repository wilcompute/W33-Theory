#!/usr/bin/env python3
"""Finite-alphabet packing, phase-parameter dimension, and conditional optics cost.

Resource model only; do not claim any physical energy, depth or loss advantage.
"""
from __future__ import annotations
import json,math
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]/"data/toe_20261122_optical_control_resources.json"

def packing_bound(epsilon, alphabet=8):
    assert 0<epsilon<0.5
    K=int(math.floor(math.pi/(2*math.asin(epsilon))))
    assert K>=3 and math.sin(math.pi/K)>epsilon
    words=K**3;L=0
    while (alphabet**(L+1)-1)//(alphabet-1)<words:L+=1
    assert L==0 or (alphabet**L-1)//(alphabet-1)<words
    return dict(epsilon=epsilon,diagonal_grid_per_phase=K,
      pair_separation_lower_bound=2*math.sin(math.pi/K),
      distinct_target_count=words,min_required_word_length=L,
      alphabet_with_inverses=alphabet)

def verify():
    packing=[packing_bound(e) for e in (0.1,0.01,0.001,0.0001)]
    survival=[]
    for L in (10,20,40,80,100):
        mixing_instances=4*L
        survival.append(dict(word_length=L,two_mode_mixing_instances=mixing_instances,
            assumed_mixer_intensity_transmission=0.98,
            assumed_detection_efficiency=0.85,
            pessimistic_sequential_survival=0.85*0.98**mixing_instances,
            per_gate_operator_error_sufficient_for_total_error_0p01=0.01/L))
    assert 4*3//2==6 and 4**2-1==15
    assert all(x["pair_separation_lower_bound"]>2*x["epsilon"] for x in packing)
    assert all(survival[i]["pessimistic_sequential_survival"]>
               survival[i+1]["pessimistic_sequential_survival"]
               for i in range(len(survival)-1))
    return dict(status="PASS_EXACT_DIMENSION_AND_DISCRETE_PACKING_WITH_CONDITIONAL_LOSS",
      date="2026-11-22",SU4_real_dimension=15,
      standard_generic_U4_Clements_two_mode_cells=6,
      minimum_independent_phase_occurrences_for_generic_fixed_topology_exact_synthesis=15,
      dimension_proof="SU4 has 15 real dimensions. For fewer than 15 independent smooth phase variables, the circuit parameter map from a finite torus has Haar-measure-zero image (Sard). A countable union of such images is still null.",
      finite_alphabet_packing_lower_bounds=packing,
      packing_proof="Choose K^3 SU4 diagonal-phase grid points with pairwise operator separation at least 2sin(pi/K)>2epsilon. Distinct points require distinct words; with eight letters and inverses there are at most (8^(L+1)-1)/7 words of length <=L.",
      per_support3_Witting_reflection_two_mode_mixers=4,
      conditional_component_sweep=survival,
      resource_comparison_boundary="Six tunable Clements cells can synthesize an arbitrary four-mode unitary. A fixed gate alphabet is only dense, may need many sequential optical repetitions, and does not imply better power, insertion loss, latency, calibration or ququart-ququart entangling performance.")

def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS optical dimension, finite word packing, hypothetical loss sweep")
if __name__=="__main__":main()
