"""F20 action on torus H^1(F3) and H^2(F3): equivariance firewall.

Uses exact cellular action, Maschke (3 does not divide 20) to compute
H^1(X;F3)^F20 from invariant cochains and its H^2 orientation character.
"""
import collections,json,sys
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261008_early_torus_singer_quotient import objects,orbit_partition
from w33_20261008_cycle_atlas_homology_rank import rank_mod
D=R/"data";OUT=D/"w33_20261008_F20_torus_mod3_equivariance.json"

def compute():
 C,faces,stab,H=objects()
 V=sorted({v for f in faces for v in f})
 E=sorted({tuple(sorted((u,v))) for f in faces for u,v in zip(f,f[1:]+f[:1])})
 F=[tuple(f) for f in faces]
 ix={frozenset(f):i for i,f in enumerate(F)}
 Eix={e:i for i,e in enumerate(E)}
 assert (len(V),len(E),len(F))==(40,60,20)
 B2=np.zeros((20,60),dtype=int)
 for i,f in enumerate(F):
  for a,b in zip(f,f[1:]+f[:1]):
   B2[i,Eix[tuple(sorted((a,b)))]]+=(1 if a<40 else -1)
 # Note B2 is coboundary delta^1, maps edge cochains to face cochains.
 def all_orbits(gens):
  vo=orbit_partition(V,gens,lambda g,v:g[v])
  eo=orbit_partition(E,gens,lambda g,e:tuple(sorted((g[e[0]],g[e[1]]))))
  fo=orbit_partition(set(map(frozenset,F)),gens,lambda g,f:frozenset(g[v] for v in f))
  M=np.zeros((len(eo),60),dtype=int)
  for i,o in enumerate(eo):
   for e in o:M[i,Eix[e]]=1
  # rank of coboundary restricted to invariant one-cochains
  r=rank_mod((B2@M.T).T.tolist(),3)
  # H0 invariants dimension 1, rank of d0 invariant is dim(C0^G)-1
  dim=len(eo)-r-(len(vo)-1)
  return {"vertex_orbit_sizes":sorted(map(len,vo)),
          "edge_orbit_sizes":sorted(map(len,eo)),
          "face_orbit_sizes":sorted(map(len,fo)),
          "dim_invariant_C0":len(vo),"dim_invariant_C1":len(eo),
          "rank_coboundary_C1inv_to_C2":r,
          "dim_H1_F3_invariant_under_group":dim}
 result={"C5":all_orbits(H),"F20":all_orbits(stab)}
 assert result["C5"]["dim_H1_F3_invariant_under_group"]==2
 # Orientation on single H2 integral relation: compare transformed chain.
 cert=json.loads((D/"w33_20261008_cycle_atlas_homology_rank.json").read_text())
 c45=json.loads((D/"w33_20261008_cycle_center_atlas_constructive.json").read_text())
 weights={frozenset(C[i]):int(a) for i,a in zip(c45["largest_found_cycle_indices"],cert["primitive_integral_relation_coefficients"]) if a}
 assert len(weights)==20
 signs=collections.Counter()
 for g in stab:
  eps=None
  for i,f in enumerate(F):
   mapped=frozenset(g[x] for x in f)
   j=ix[mapped]
   row=np.zeros(60,dtype=int)
   for a,b in zip(f,f[1:]+f[:1]):
    edge=tuple(sorted((g[a],g[b])))
    row[Eix[edge]]+=(1 if a<40 else -1)
   match=int(np.array_equal(row,B2[j]))
   reverse=int(np.array_equal(row,-B2[j]))
   assert match+reverse==1
   e=(1 if match else -1)*weights[frozenset(f)]*weights[mapped]
   if eps is None:eps=e
   assert eps==e
  signs[eps]+=1
 result["H2_Z_orientation_character_element_histogram"]=dict(signs)
 result["F20_invariant_H2_F3_dimension"]=1 if set(signs)=={1} else 0
 result["F20_H1_no_order_three_character_if_zero"]=result["F20"]["dim_H1_F3_invariant_under_group"]==0
 result["physics_boundary"]="Only topological cohomology and invariants under selected exact point-symplectic subgroup; no Standard Model matter charge or anomaly derived."
 return result
if __name__=="__main__":
 x=compute();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print(json.dumps(x,indent=2),flush=True);print("F20_COHOMOLOGY_PASS")
