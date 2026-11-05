#!/usr/bin/env python3
"""Petersen + five-duad structure of Witting ten-fold loss-of-identity tetrads.

The actual native class1 A5 subgroup has exactly two orbits on forty
Witting orthogonal tetrads: 10 (collision) and 30 (injective).
For ten bad contexts, a pair is a successful 440-state decoder exactly
when both labelled outcomes together separate all 440 root labels.
Show its 15-edge graph is Petersen KG(5,2), recover five-set duad
labels, and certify ALL 60 native A5 actions lift to even permutations
of that same five set. Check whether ten lines partition all 40 rays
(an invariant GQ spread), not inferred from one-shot information.
"""
from __future__ import annotations
import itertools,collections,json,sys,math
from pathlib import Path
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT,ROOT/"analysis"):sys.path.insert(0,str(p))
import w33_pass999_a5_double_class_census as prior
from exploration.w33_witting_srg_bridge import witting_to_symplectic_isomorphism,witting_orthogonal_tetrads
OUT=ROOT/"data/toe_20261105_petersen_tetrad_duad_spread_certificate.json"
def even(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2==0
def main():
 data=json.loads((ROOT/"data/toe_20261105_a5_tetrad_orbits_bhattacharyya.json").read_text())
 orbit=data["A5_tetrad_orbit_details"]
 bad=data["bad_basis_indices"];good=data["good_basis_indices"]
 pairs=data["two_bad_tetrad_pair_classification"]
 assert len(bad)==10 and len(good)==30 and len(pairs)==45
 E=nx.Graph();E.add_nodes_from(bad)
 for pair in pairs:
  if pair["distinct_440root_probability_classes"]==440:E.add_edge(*pair["tetrads"])
 assert E.number_of_edges()==15 and nx.is_connected(E)
 assert all(k==3 for _,k in E.degree())
 assert nx.girth(E)==5
 assert nx.is_isomorphic(E,nx.petersen_graph())
 assert np.allclose(sorted(np.linalg.eigvalsh(nx.to_numpy_array(E))),[-2]*4+[1]*5+[3])
 duads=list(itertools.combinations(range(5),2))
 K=nx.Graph()
 K.add_nodes_from(duads)
 K.add_edges_from((u,v) for u,v in itertools.combinations(duads,2) if not(set(u)&set(v)))
 matcher=nx.algorithms.isomorphism.GraphMatcher(E,K)
 assert matcher.is_isomorphic()
 mp=dict(matcher.mapping)
 assert len(set(mp.values()))==10
 inv={v:k for k,v in mp.items()}
 bad_tet=[tuple(sorted(x)) for x in witting_orthogonal_tetrads()]
 assert len(bad_tet)==40
 bad_ray_counts=collections.Counter(k for i in bad for k in bad_tet[i])
 spread=all(z==1 for z in bad_ray_counts.values()) and len(bad_ray_counts)==40
 assert spread
 assert all(sum(len(set(bad_tet[i])&set(bad_tet[j])) for j in bad) == 4 for i in good)
 # Class1 A5 group acts on tetrads by ray permutations. Verify same
 # Kneser duad action under some EVEN p on five base slots.
 native=prior.core_objects()
 w2s=witting_to_symplectic_isomorphism()
 s2w={v:k for k,v in w2s.items()}
 lookup={x:i for i,x in enumerate(bad_tet)}
 permutations=sorted(itertools.permutations(range(5)))
 even5=[p for p in permutations if even(p)]
 assert len(even5)==60
 matching=[]
 for gg in native["A5_classes"][1]:
  observed={i:lookup[tuple(sorted(s2w[gg[w2s[k]]] for k in bad_tet[i]))] for i in bad}
  found=[]
  for p in even5:
   if all(inv[tuple(sorted((p[u],p[v])))]==observed[i] for i,(u,v) in mp.items()):found.append(p)
  assert len(found)==1
  matching.append(found[0])
 assert len(set(matching))==60
 # compare incident number of good contexts per pair of spread lines,
 # use this as extra rooted incidence fingerprint independent of the
 # probability collision table (not assumed to equal Petersen).
 related={}
 for i,j in itertools.combinations(bad,2):
  common=sum(bool(set(bad_tet[i])&set(bad_tet[k])) and bool(set(bad_tet[j])&set(bad_tet[k])) for k in good)
  related[f"{i},{j}"]=common
 classes=collections.defaultdict(list)
 for i,j in itertools.combinations(bad,2):
  classes["decoder_injective" if E.has_edge(i,j) else "decoder_noninjective"].append(related[f"{i},{j}"])
 result=dict(status="PASS_TEN_BAD_WITTING_TETRADS_FORM_A5_INVARIANT_SPREAD_AND_PETERSEN_DUADS",
   native_A5_order=60,
   bad_contexts_form_ray_partition_of_40_points=spread,
   Witting_line_spread_size=10,
   bad_tetrad_indices=bad,
   other_30_tetrads_each_meet_4_spread_lines_in_distinct_rays=True,
   decoder_full_identifiability_pair_graph_edges=15,
   decoder_graph_regular_degree=3,
   decoder_graph_girth=5,
   decoder_graph_is_petersen_KG_5_2=True,
   duad_labels_for_bad_tetrad={str(i):list(pair) for i,pair in sorted(mp.items())},
   native_A5_tetrad_action_equals_even_permutations_on_five_duad_slots=True,
   native_A5_five_slot_permutation_count=len(set(matching)),
   all60_induced_five_slot_permutations=[list(x) for x in matching],
   good_tetrad_incidence_pair_counts_by_decoder_class={k:dict(collections.Counter(v)) for k,v in classes.items()},
   exact_source="Actual PSp4(3) A5 native permutation core, independently established graph isomorphism to Witting40, explicit 440 E8-mixed-state Born distributions. Group match to KG(5,2) graph is a CHOSEN relabeling, not new natural physics.",
   scope="A5/Kneser/Petersen and GQ(3,3) line-spread arithmetic are classical. This identifies a concrete 10+30 readout loss pattern and a 15-pair recovery schedule; no new quantum gravity, particle multiplets or temporal entanglement.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(result["status"],"spread",spread,"incidence",result["good_tetrad_incidence_pair_counts_by_decoder_class"],flush=True)
 return result
if __name__=="__main__":main()
