#!/usr/bin/env python3
"""Exact PSp(4,3) stabilizer of the selected 20-apartment torus-homology carrier.

This checks an E6 45-count claim against *actual* equivariance, without
identifying an orbit just from the number of faces.
"""
import itertools,collections,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_five_physics_frontiers import projective_points_and_lines
from w33_20261008_dual_27_electrical_transport import pairing,normalize
from w33_20261008_global_cycle_center_census import cycles
OUT=ROOT/"data"/"w33_20261008_apartment_torus_symmetry.json"
def main():
 pts,lines=projective_points_and_lines()
 ix={p:i for i,p in enumerate(pts)}
 li={frozenset(L):i for i,L in enumerate(lines)}
 vectors=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,1,0),(1,1,1,1)]
 perms=[]
 for v in vectors:
  g=tuple(ix[normalize(tuple((p[k]+pairing(p,v)*v[k])%3 for k in range(4)))] for p in pts)
  assert len(set(g))==40
  perms.append(g)
 identity=tuple(range(40));S={identity};queue=[identity]
 for x in queue:
  for g in perms:
   y=tuple(x[g[k]] for k in range(40))
   if y not in S:S.add(y);queue.append(y)
 assert len(S)==25920,len(S)
 C=cycles()
 select=json.loads((ROOT/"data/w33_20261008_cycle_center_atlas_constructive.json").read_text())
 relation=json.loads((ROOT/"data/w33_20261008_cycle_atlas_homology_rank.json").read_text())
 all45={frozenset(C[c]) for c in select["largest_found_cycle_indices"]}
 sub20={frozenset(C[c]) for c,w in zip(select["largest_found_cycle_indices"],relation["primitive_integral_relation_coefficients"]) if w}
 assert len(all45)==45 and len(sub20)==20
 # To map (point,line) vertices g moves the 40 projective points then all 40 lines.
 def induced(g):
  lineperm=tuple(li[frozenset(pts[g[ix[p]]] for p in L)] for L in lines)
  return g+tuple(40+i for i in lineperm)
 p45=[];p20=[]
 for g in queue:
  h=induced(g)
  act=lambda face: frozenset(h[v] for v in face)
  if all(act(f) in all45 for f in all45):p45.append(g)
  if all(act(f) in sub20 for f in sub20):p20.append(g)
 assert len(p45)>0 and len(p20)>0
 def order(g):
  t=tuple(range(40));j=0
  while True:
   t=tuple(t[g[i]] for i in range(40));j+=1
   if t==identity:return j
 def composed(g,h):
  return tuple(g[h[i]] for i in range(40))
 shape=collections.Counter(order(g) for g in p20)
 abelian=all(composed(g,h)==composed(h,g) for g in p20 for h in p20)
 inverse={g:next(h for h in p20 if composed(g,h)==identity) for g in p20}
 commutators={composed(composed(composed(g,h),inverse[g]),inverse[h]) for g in p20 for h in p20}
 subgroup={identity};front=[identity]
 for z in front:
  for q in commutators:
   y=composed(z,q)
   if y not in subgroup:subgroup.add(y);front.append(y)
 # The commutator subgroup is C5 and the quotient C4.
 assert len(subgroup)==5 and set(order(g) for g in subgroup)=={1,5}
 # Independent normalizer test connects this copy to the old
 # Pass2474 Sylow-5 normalizer theorem in PSp4(3), not merely |F20|.
 g5=next(g for g in subgroup if order(g)==5)
 N5=[g for g in queue if all(any(composed(g,h)==composed(q,g) for q in subgroup) for h in [g5])]
 assert len(N5)==20 and set(N5)==set(p20)
 assert shape==collections.Counter({1:1,2:5,4:10,5:4})
 assert not abelian
 reference_face=next(iter(sub20))
 faceorbit={frozenset(induced(g)[v] for v in reference_face) for g in p20}
 assert len(faceorbit)<=20
 out={"projective_symplectic_group_order":len(S),
      "support_stabilizer_element_order_distribution":dict(shape),
      "support_stabilizer_abelian":abelian,
      "support_stabilizer_derived_subgroup_order":len(subgroup),
      "support_stabilizer_derived_subgroup_is_C5":True,
      "support_stabilizer_is_normalizer_of_its_Sylow5_in_PSp4_3":True,
      "full_PSp4_3_normalizer_order":len(N5),
      "prior_repo_identification":"Pass2474: Sylow-5 normalizer in PSp4(3) is F20, full symplectic lift is nonsplit 5:8; this pass proves chosen torus support stabilizer is exactly that type of normalizer in PSp, not a shared-order guess.",
      "support_stabilizer_abelianization":"C4",
      "support_stabilizer_is_affine_F20_C5_semidirect_C4":True,
      "tetraquadric_Klein_four_is_subgroup_of_support_stabilizer":False,
      "no_Z3_character_of_support_stabilizer":True,
      "support_stabilizer_face_orbit_of_selected_face":len(faceorbit),
      "ambient_1620_apartments_one_orbit":"previous BT744, not new",
      "constructed_45_cycle_setwise_stabilizer":len(p45),
      "constructed_20_cycle_relation_support_setwise_stabilizer":len(p20),
      "orbit_size_of_45_selected_atlas":25920//len(p45),
      "orbit_size_of_20_cycle_support":25920//len(p20),
      "45_tritangent_planes_canonical_equivalence_proven":False,
      "note":"Exact subgroup stabilizers of chosen combinatorial subsets, not E6 action intertwiners. A 45-object count alone is not equivalence."}
 return out
if __name__=="__main__":
 a=main();OUT.write_text(json.dumps(a,indent=2,sort_keys=True)+"\n")
 print(json.dumps(a,indent=2),flush=True)
 print("TORUS_SYMMETRY_PASS")
