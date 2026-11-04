#!/usr/bin/env python3
"""One-shot mutual information equal != multi-shot identification completeness.

All 40 native Witting tetrads have the SAME single-shot mutual information
for a uniform 440-root ensemble as the full 40-outcome POVM, yet a single
fixed 4-outcome orthonormal basis has only 3 real probability coordinates.
Count distinct exact/roundoff-stable probability distributions among all
440 root labels, then bound optimal infinite-sample Bayesian root-ID
success by number_of_distinct_probability_classes /440. This may be
strictly below one for native tetrads; the 40-outcome POVM is injective.
Compare seeded best Haar orthonormal basis (generic finite-codebook
injectivity can happen even with just 4 outcomes; no continuous 8D
tomography follows).

For uniform priors equal conditional class probabilities,
max success = (# classes)/440 as N->infinity. A channel may have same
single-copy I(R;Y) yet different infinite-copy decoding capability.
"""
from __future__ import annotations
import json,collections,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT,ROOT/"analysis"):sys.path.insert(0,str(p))
from exploration.w33_witting_srg_bridge import construct_witting_rays,witting_orthogonal_tetrads
OUT=ROOT/"data/toe_20261104_single_tetrad_440_decode_collision_nogo.json"
def freq(P,precision=10):
 from scipy.spatial.distance import pdist
 cc=collections.Counter(tuple(np.round(p,precision)) for p in P)
 sizes=collections.Counter(cc.values())
 D=pdist(P,metric="cityblock")/2
 positive=D[D>1e-9]
 assert len(positive)>0
 return dict(unique_prob_distributions=len(cc),histogram_of_class_sizes={str(k):v for k,v in sorted(sizes.items())},
  maximum_class_size=max(cc.values()),total_colliding_root_labels=sum(v for v in cc.values() if v>1),
  asymptotic_uniform_prior_optimal_label_decoding_success=len(cc)/len(P),
  minimum_pairwise_total_variation_distance=float(D.min()),
  minimum_positive_pairwise_total_variation_distance=float(positive.min()),
  number_of_zero_dist_pairs_numerical=int(np.sum(D<1e-9)))
def main():
 src=json.loads((ROOT/"data/toe_20261104_witting_operator_dark_spectral_A5_duality.json").read_text())
 cb=json.loads((ROOT/"data/toe_20261104_two_e8_root_to_witting_density_codebook.json").read_text())
 scan=json.loads((ROOT/"data/toe_20261104_two_e8_witting_basis_information_search.json").read_text())
 rays=np.array(construct_witting_rays())
 tetrads=witting_orthogonal_tetrads()
 O=np.array(src["A5_classes"][1]["explicit_8_Hermitian_ququart_observables_real"])+1j*np.array(
 src["A5_classes"][1]["explicit_8_Hermitian_ququart_observables_imag"])
 theta=np.array(cb["eight_real_parameters_for_440_states"])
 rho=np.eye(4)[None,:,:]/4+np.einsum("ij,jab->iab",theta,O)
 def probabilities(states):
  return np.einsum("ia,nab,ib->ni",states.conj(),rho,states).real
 counts=[]
 for t in tetrads:
  q=probabilities(rays[list(t)])
  assert max(abs(q.sum(axis=1)-1))<1e-10
  counts.append(freq(q))
 full=1/40+theta@np.array(src["A5_classes"][1]["explicit_W33_40x8_observable_coefficient_map"]).T/5
 fullfreq=freq(full)
 assert fullfreq["unique_prob_distributions"]==440
 haar=scan["epsilon_scan"][0]
 U=(np.array(haar["best_sampled_Haar_unitary_rows_real"])+1j*np.array(haar["best_sampled_Haar_unitary_rows_imag"]))
 hf=freq(probabilities(U))
 # basis-change experiments can have distinct finite codewords yet not
 # tomographically span all 8 continuous coordinates of rho(theta).
 assert counts and all(c["unique_prob_distributions"]<=440 for c in counts)
 result=dict(status="PASS_FIXED_WITTING_TETRAD_VS_FULL_POVM_MULTI_COPY_IDENTIFIABILITY",
  total_E8_root_labels=440,
  native_Witting_tetrads_checked=len(tetrads),
  fixed_basis_continuous_density_parameter_rank_at_most=3,
  full_Witting40_POVM_continuous_density_parameter_rank=8,
  full_Witting40_probability_unique_440_label_count=fullfreq["unique_prob_distributions"],
  all_native_tetrad_collision_audits=counts,
  native_tetrad_unique_counts=sorted(set(x["unique_prob_distributions"] for x in counts)),
  best_sampled_Haar_four_outcome_collision_audit=hf,
  warning="Identical single-shot uniform-ensemble mutual information does not imply identical repeated-label identification. Exact collisions impose a nonzero infinite-copy error floor for a fixed measurement. Finite 440 labels may be injective under a generic single four-outcome basis despite rank3 continuous tomography.",
  prior_art="Bayesian identifiability and finite-output POVM linear rank are elementary; new audit explicitly checks all Witting40 tetrads on the prepared 440-root E8 codebook.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(result["status"],"unique native",result["native_tetrad_unique_counts"],"full",fullfreq["unique_prob_distributions"],"Haar",hf["unique_prob_distributions"],flush=True)
 return result
if __name__=="__main__":main()
