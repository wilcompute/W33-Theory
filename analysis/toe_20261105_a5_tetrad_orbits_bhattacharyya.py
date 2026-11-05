#!/usr/bin/env python3
"""Native A5 orbit/collision classification and Hellinger discrimination of 40 Witting tetrads.

Uses ACTUAL PSp4(3) 40-point subgroup and known Witting ray relabeling.
Investigates whether native A5 symmetry organizes the exactly 10 collision
tetrads, and whether pairs of bad bases can recover 440 distinct root labels.
Compare worst-case Bhattacharyya pair-distance with full Witting40 POVM
and previously optimized single SU4 basis. Finite 440 classical labels;
does not claim 8-real-parameter tomography with one 4-outcome basis.
"""
from __future__ import annotations
import itertools,json,sys,collections
from pathlib import Path
import numpy as np
from scipy.spatial.distance import pdist
ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT,ROOT/"analysis"):sys.path.insert(0,str(p))
from exploration.w33_witting_srg_bridge import construct_witting_rays,witting_orthogonal_tetrads,witting_to_symplectic_isomorphism
import w33_pass999_a5_double_class_census as prior
OUT=ROOT/"data/toe_20261105_a5_tetrad_orbits_bhattacharyya.json"
def key_classes(p):
 groups=collections.Counter(tuple(np.round(z,11)) for z in p)
 return len(groups),dict(collections.Counter(groups.values()))
def dist_score(p):
 assert np.min(p)>0
 D=pdist(np.sqrt(p),"sqeuclidean")
 assert np.min(D)>-1e-12
 D=np.maximum(D,0)
 # ∑ sqrt(pq)=1-1/2||sqrt(p)-sqrt(q)||²
 bcmax=1-np.min(D)/2
 return dict(minimum_squared_Hellinger_separation=float(np.min(D)),
  nearest_pair_Bhattacharyya_coefficient=float(bcmax),
  worst_pair_Bhattacharyya_error_exponent=float(-np.log(bcmax)) if bcmax<1 else 0.)
def main():
 rays=np.asarray(construct_witting_rays())
 tetrads=[tuple(sorted(x)) for x in witting_orthogonal_tetrads()]
 assert len(tetrads)==len(set(tetrads))==40
 labels={t:i for i,t in enumerate(tetrads)}
 native=prior.core_objects()
 w2s=witting_to_symplectic_isomorphism()
 s2w={v:k for k,v in w2s.items()}
 H=native["A5_classes"][1]
 assert len(H)==60
 perms=[]
 for g in H:
  P=tuple(labels[tuple(sorted(s2w[g[w2s[x]]] for x in t))] for t in tetrads)
  assert len(set(P))==40
  perms.append(P)
 pending=set(range(40));orbits=[]
 while pending:
  x=min(pending);orbit=sorted({p[x] for p in perms})
  assert set(orbit)<=pending
  orbits.append(orbit);pending-=set(orbit)
 assert sum(map(len,orbits))==40
 basis_json=json.loads((ROOT/"data/toe_20261104_single_tetrad_440_decode_collision_nogo.json").read_text())
 counts=[q["unique_prob_distributions"] for q in basis_json["all_native_tetrad_collision_audits"]]
 assert collections.Counter(counts)=={440:30,109:10}
 E_json=json.loads((ROOT/"data/toe_20261104_witting_operator_dark_spectral_A5_duality.json").read_text())
 cb=json.loads((ROOT/"data/toe_20261104_two_e8_root_to_witting_density_codebook.json").read_text())
 theta=np.asarray(cb["eight_real_parameters_for_440_states"])
 Ops=np.asarray(E_json["A5_classes"][1]["explicit_8_Hermitian_ququart_observables_real"])+1j*np.asarray(E_json["A5_classes"][1]["explicit_8_Hermitian_ququart_observables_imag"])
 rho=np.eye(4)[None,:,:]/4+np.einsum("ij,jab->iab",theta,Ops)
 def basis_p(t):
  V=rays[list(t)]
  return np.einsum("ia,nab,ib->ni",V.conj(),rho,V).real
 probs=[basis_p(t) for t in tetrads]
 singles=[dist_score(q) for q in probs]
 assert all(abs(np.sum(q,axis=1)-1).max()<1e-11 for q in probs)
 orbit_records=[]
 for o in orbits:
  value=collections.Counter(counts[i] for i in o)
  orbit_records.append(dict(tetrad_indices=o,orbit_size=len(o),
    distinct_440root_probability_counts=dict(value),
    uniform_root_codebook_440_identifiability=all(counts[i]==440 for i in o)))
 bad=[i for i,c in enumerate(counts) if c==109]
 good=[i for i,c in enumerate(counts) if c==440]
 # Exact distribution collision test on two labeled tetrad settings.
 # Each setting is chosen with probability 1/2 and its setting label logged.
 two_bad=[]
 for i,j in itertools.combinations(bad,2):
  q=np.column_stack((probs[i]/2,probs[j]/2))
  num,classes=key_classes(q)
  two_bad.append(dict(tetrads=[i,j],distinct_440root_probability_classes=num,
    largest_collision_class=max(classes),
    min_probability_pair_Bhattacharyya_exponent=dist_score(q)["worst_pair_Bhattacharyya_error_exponent"]))
 full=np.asarray(cb["eight_real_parameters_for_440_states"])
 E=np.asarray(E_json["A5_classes"][1]["explicit_W33_40x8_observable_coefficient_map"])
 full_p=1/40+full@E.T/5
 assert full_p.shape==(440,40)
 assert len(set(map(tuple,np.round(full_p,11))))==440
 full_score=dist_score(full_p)
 sample=[next(x for x in single if x["worst_pair_Bhattacharyya_error_exponent"]>0) for single in [singles]]
 # Worst-case actual six/generic? compare previous optimized readout.
 opt=json.loads((ROOT/"data/toe_20261104_ququart_povm_local_unitary_optimizer.json").read_text())
 oi=opt["epsilon_results"][0]
 best=max(oi["local_restart_optimization_results"],key=lambda x:x["information_bits"])
 U=np.asarray(best["physical_ququart_basis_columns_real"])+1j*np.asarray(best["physical_ququart_basis_columns_imag"])
 qopt=np.einsum("ai,nab,bi->ni",U.conj(),rho,U).real
 opt_score=dist_score(qopt)
 result=dict(status="PASS_NATIVE_A5_WITTING_TETRAD_ORBITS_AND_PAIR_DISCRIMINATION",
  native_A5_order=len(H),native_40ray_tetrad_count=len(tetrads),
  A5_tetrad_orbit_sizes=sorted(map(len,orbits)),
  A5_tetrad_orbit_details=orbit_records,
  full_Witting40_POVM_closest_pair_Bhattacharyya=full_score,
  optimized_single_4outcome_basis_closest_pair_Bhattacharyya=opt_score,
  native_30_injective_tetrad_min_pair_exponent_range=[min(singles[i]["worst_pair_Bhattacharyya_error_exponent"] for i in good),max(singles[i]["worst_pair_Bhattacharyya_error_exponent"] for i in good)],
  native_10_collision_tetrads_all_exponent_zero=all(singles[i]["worst_pair_Bhattacharyya_error_exponent"]==0 for i in bad),
  two_distinct_bad_tetrad_pairs_checked=len(two_bad),
  two_bad_tetrad_pair_classification=two_bad,
  bad_basis_indices=bad,good_basis_indices=good,
  note="Bhattacharyya exponent -ln(maxpair sum_o sqrt(p_o q_o)) gives a worst-pair discrimination BOUND, not optimal many-hypothesis Bayes error exponent. Classification on finite 440 roots only.",
  prior_art="A5 subgroup already identified in repo; present calculation classifies the specific 30/10 Witting measurement codebook split and setting-dependent capacity.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
 print(result["status"],"orbits",result["A5_tetrad_orbit_sizes"],"bad pairs",collections.Counter(x["distinct_440root_probability_classes"] for x in two_bad),"BC exponents",full_score["worst_pair_Bhattacharyya_error_exponent"],opt_score["worst_pair_Bhattacharyya_error_exponent"],flush=True)
 return result
if __name__=="__main__":main()
