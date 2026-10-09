"""Reproducible toy search of integral equivariant rank5 line-bundle sums
on explicitly smooth Klein tetraquadric X23. Testing *necessary*
topological SU5 GUT and chiral-index constraints is NOT a HYM/heterotic
vacuum or anomaly-free model. Select Li O(l_i) with sum l_i=0,
each sum_j l_ij=0 for equal-positive-moduli zero slope, and each
degree sum even for Klein equivariance. Euler(V) index=-12 gives
downstairs net index=-3 if equivariant descent achieved.
Only checks Bianchi c2(TX)-c2(V) pairings with four nef Hi >=0;
not effective-cycle sufficiency or global anomaly cancellation.
"""
from pathlib import Path
import itertools,json,random,collections
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"data/w33_20261008_Klein_CY_SU5_linebundles_index3_candidates.json"
T=list(itertools.combinations(range(4),3))
def index(L):
 return 2*sum(sum(row[i]*row[j]*row[k] for i,j,k in T) for row in L)
def c2diff(L):
 # c2TX.H_i=24; c2(V).H_i=-2 sum_a sum_{j<k!=i} l_aj*l_ak
 return [24+2*sum(sum(v[j]*v[k] for j,k in itertools.combinations([z for z in range(4) if z!=i],2)) for v in L) for i in range(4)]
def main():
 pool=[v for v in itertools.product(range(-2,3),repeat=4) if sum(v)==0 and any(v)]
 assert len(pool)>50
 rng=random.Random(20261008);selected=None;tested=0;counts=collections.Counter()
 for it in range(300000):
  v=[rng.choice(pool) for _ in range(4)]
  w=tuple(-sum(x[j] for x in v) for j in range(4))
  if max(map(abs,w))>3 or not any(w):continue
  if w in v or len(set(v))<4:continue
  rows=v+[w];tested+=1
  chi=index(rows);counts["valid_c1_polystable"]+=1
  if chi not in (-12,12):continue
  counts["three_gen_index"]+=1
  d=c2diff(rows)
  if min(d)<0:continue
  counts["four_nonnegative_nef_pairings"]+=1
  if selected is None or (max(abs(x) for v in rows for x in v),sum(abs(x) for v in rows for x in v)) < (selected["max_abs_component"],selected["sum_abs_components"]):
   selected={"line_bundles_multidegree":rows,"upstairs_Dirac_index":chi,
    "downstairs_net_index_if_equivariant_free_quotient":chi//4,
    "c1V_zero":all(sum(row[j] for row in rows)==0 for j in range(4)),
    "each_slope_zero_at_equal_t":True,
    "each_line_bundle_Klein_linearization_parity_even":True,
    "Bianchi_c2TX_minus_c2V_nef_pairings":d,
    "max_abs_component":max(abs(x) for v in rows for x in v),
    "sum_abs_components":sum(abs(x) for v in rows for x in v)}
  if selected["max_abs_component"]<=2 and selected["sum_abs_components"]<=24:break
 assert selected is not None,("no_candidate",tested,counts)
 assert all(sum(v)==0 for v in selected["line_bundles_multidegree"])
 assert index(selected["line_bundles_multidegree"])==selected["upstairs_Dirac_index"]
 assert min(c2diff(selected["line_bundles_multidegree"]))>=0
 return {"trials":it+1,"valid_distinct_SUn_linebundle_sums_examined":tested,"count_stages":dict(counts),
  "chosen":selected,
  "Chern_index_formula":"chi(V)=2 sum_{a=1..5} sum_{i<j<k} n_ai*n_aj*n_ak, using integral_X H_i H_j H_k=2",
  "slope_formula_at_t_equal":"mu(L_i) proportional sum_j n_ij at t=(1,1,1,1)",
  "required_rank5_structure_group":"S(U1^5) subset SU5; topological candidate not verified poly-stable on quotient nor full E8 physical GUT",
  "bundle_total_c1_zero":True,
  "effective_fivebrane_or_Mori_sufficiency_not_proved":True,
  "actual_anomaly_cancellation_and_physical_Z6_not_proved":True,
  "downstairs_index_assumes_equivariant_descent_and_induced_cohomology_action":True,
  "Yukawas_metrics_and_particle_spectrum_not_calculated":True,
  "scientific_boundary":"Existential finite-integer topological tri-generation *candidate*, not a heterotic Standard Model or derived TOE. Check stability walls, all Chern/anomaly constraints, free equivariant lifts, exotics, Green-Schwarz, Yukawas."}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(r,flush=True);print("CY_SU5_TOPOLOGICAL_INDEX_THREE_SEARCH_PASS")
