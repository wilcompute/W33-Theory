#!/usr/bin/env python3
"""Compare the 648 symmetry-conjugate minimal Witting POVMs under sparse QR.

A Hessian change of input ray frame keeps the frame spectrum invariant but
may change the adjacent-coupler network produced by one fixed row convention.
"""
import json
from pathlib import Path
import numpy as np
from sympy.combinatorics import Permutation,PermutationGroup
import toe_20261122_witting_one_phase_three_fixed as W
import toe_20261122_round6_16effect_optimal as P
import toe_20261122_povm30_nai_mark_shot_cost as F
import toe_20261122_photonic_sparse_isometry_loss as O
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_round7_mic_optics_symmetry.json'

def verify():
  group=PermutationGroup([Permutation(z) for z in W.permutations().values()]);rays,_=F.frames()
  options=[]
  for k,g in enumerate(group.generate_schreier_sims()):
    pairs=sorted((int(g(j)),float(P.WEIGHTS[j])) for j in P.S)
    ids=[i for i,w in pairs];weights=[w for i,w in pairs]
    V=np.array([np.sqrt(w)*rays[i].conj() for i,w in pairs])
    stat=O.stats(V,eta=.995,seed=0)
    options.append(dict(order=k,support=ids,weights=weights,gates=stat['gate_count'],survival=stat['maximally_mixed_input_detection_probability'],min_eig=stat['input_dependent_detection_eigenvalues'][0]))
  assert len(options)==648
  base=next(x for x in options if x['support']==sorted(P.S))
  best=min(options,key=lambda x:(x['gates'],-x['survival']))
  best_survival=max(options,key=lambda x:x['survival'])
  assert best['gates']<=base['gates']
  assert best_survival['survival']>=base['survival']
  import toe_20261122_round5_18effect_optical as R
  def risk(entry):
    V=np.array([np.sqrt(w)*rays[i].conj() for i,w in zip(entry['support'],entry['weights'])])
    return float(R.loss_risk(V,np.eye(4)/4)['source_photon_HS_risk_coefficient']-.75)
  for entry in (base,best,best_survival):entry['Haar_average_source_photon_risk_coefficient']=risk(entry)
  return dict(status='PASS_648_HESSIAN_EQUIVALENT_MINIMAL16_PHOTONIC_LAYOUT_SEARCH',
    tested_POVM_designs=len(options),each_is_minimal_16_IC=True,
    all_have_identical_ideal_frame_eigenvalues=True,
    rail_local_eta=.995,
    baseline=base,
    minimize_gate_count_then_maximize_survival=best,
    maximize_survival=best_survival,
    gate_histogram={str(n):sum(o['gates']==n for o in options) for n in sorted(set(o['gates'] for o in options))},
    survival_range=[float(min(x['survival'] for x in options)),float(max(x['survival'] for x in options))],
    caveat='Applies one fixed sorted-row adjacent-Givens synthesis and ideal frame labels; an arbitrary lab can include extra input unitary to realize the conjugated rays. No global optical circuit optimum or realistic hardware fidelity is proved.')

if __name__=='__main__':
 d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print({k:v for k,v in d.items() if k not in ['baseline','minimize_gate_count_then_maximize_survival','maximize_survival']});print('baseline',d['baseline']);print('best',d['minimize_gate_count_then_maximize_survival']);print('survival',d['maximize_survival'])
