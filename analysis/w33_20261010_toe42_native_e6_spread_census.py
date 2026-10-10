"""Exploratory native E6/GQ(2,4) tritangent exact-cover spread census."""
import json,collections,time
from pathlib import Path
root=Path(__file__).resolve().parents[1]
tri=json.loads((root/"artifacts/canonical_su3_gauge_and_cubic.json").read_text())["solution"]["d_triples"]
triples=[tuple(map(int,t["triple"])) for t in tri]
assert len(triples)==45
marks=[sum(1<<x for x in t) for t in triples]
bypt={p:[i for i,b in enumerate(marks) if b>>p & 1] for p in range(27)}
all27=(1<<27)-1
spreads=[]
def visit(used,indices):
 if used==all27:
  spreads.append(tuple(sorted(indices)));return
 scores=[]
 for p in range(27):
  if (used>>p)&1:continue
  options=[i for i in bypt[p] if not marks[i]&used]
  scores.append((len(options),p,options))
 if not scores:return
 _,p,cands=min(scores)
 for i in cands: visit(used|marks[i],indices+(i,))
start=time.time();visit(0,())
spreads=sorted(set(spreads))
print("SPREADS",len(spreads),"seconds",round(time.time()-start,3),flush=True)
assert all(len(s)==9 for s in spreads)
byline={i:[j for j,s in enumerate(spreads) if i in s] for i in range(45)}
all45=(1<<45)-1;smasks=[sum(1<<i for i in s) for s in spreads]
parallel=[]
def solve(mask,ids):
 if mask==all45:
  parallel.append(tuple(sorted(ids)));return
 opts=[]
 for j in range(45):
  if mask>>j&1:continue
  cand=[i for i in byline[j] if not smasks[i]&mask]
  opts.append((len(cand),j,cand))
 if not opts:return
 _,j,cand=min(opts)
 for i in cand:solve(mask|smasks[i],ids+(i,))
solve(0,())
parallel=sorted(set(parallel))
print("PARALLELISMS",len(parallel),"seconds",round(time.time()-start,3),flush=True)
pairs=collections.Counter(len(set(a)&set(b)) for ia,a in enumerate(spreads) for b in spreads[ia+1:])
print("SPREAD_INTERSECTION",dict(sorted(pairs.items())),flush=True)
spread_degree=[sum(not(set(a)&set(b)) for b in spreads if b!=a) for a in spreads]
print("DISJOINT DEGREE ORBITS",dict(sorted(collections.Counter(spread_degree).items())),flush=True)
assert collections.Counter(spread_degree)=={40:40,31:160}
classical={i for i,d in enumerate(spread_degree) if d==40}
parallel_types=collections.Counter(sum(i in classical for i in part) for part in parallel)
appearance=collections.Counter(i for part in parallel for i in part)
appear_classical=collections.Counter(appearance[i] for i in classical)
appear_other=collections.Counter(appearance[i] for i in range(200) if i not in classical)
print("PARALLEL CLASSICAL SPREADS",dict(parallel_types),"APPEARANCES",dict(appear_classical),dict(appear_other),flush=True)
# Fixed native sign convention: each vertex participates in one signed CCZ per layer.
sign=[int(t["sign"]) for t in tri]
vectors=[]
for s in spreads:
 lab=[0]*27
 for j in s:
  for p in triples[j]:
   assert lab[p]==0
   lab[p]=sign[j]
 assert all(x in (-1,1) for x in lab)
 vectors.append(tuple(lab))
best_cost=10**6;best_example=None;cost_hist=collections.Counter()
for partition in parallel:
 groups=[vectors[i] for i in partition]
 mn=10**6;min_order=None
 for perm in __import__('itertools').permutations(range(5)):
  cost=sum(sum(a!=b for a,b in zip(groups[perm[j]],groups[perm[j+1]])) for j in range(4))
  if cost<mn:
   mn=cost;min_order=perm
 cost_hist[mn]+=1
 if mn<best_cost:
  best_cost=mn;best_example=dict(spread_ids=[partition[z] for z in min_order],
    triad_layers=[list(spreads[partition[z]]) for z in min_order],signed_transition_count=mn)
print("SIGN POLARITY MIN",best_cost, "BEST COST DIST",dict(sorted(cost_hist.items())),flush=True)
prior=json.loads((root/"data/w33_20261010_toe41_e6_45_ccz_compiler.json").read_text())
prior_layers=prior["native_layer_indices"]
def layer_vector(layer):
 v=[0]*27
 for j in layer:
  for p in triples[j]:
   assert v[p]==0;v[p]=sign[j]
 assert all(x in (-1,1) for x in v)
 return v
prior_vectors=[layer_vector(layer) for layer in prior_layers]
prior_cost=sum(sum(a!=b for a,b in zip(prior_vectors[t],prior_vectors[t+1])) for t in range(4))
assert prior_cost>=best_cost
print("PRIOR TOE41 NATIVE ORDER SITE SWITCHES",prior_cost,flush=True)
output=dict(status="PASS",native_triads=45,points=27,total_spreads=len(spreads),
total_parallelisms=len(parallel),spread_pair_line_intersections=dict(sorted(pairs.items())),
spread_disjoint_degree_distribution=dict(sorted(collections.Counter(spread_degree).items())),
classical_spread_count_in_five_layer_parallelisms=dict(sorted(parallel_types.items())),
appearances_per_classical_spread=dict(sorted(appear_classical.items())),
appearances_per_nonclassical_spread=dict(sorted(appear_other.items())),
signed_triad_counts=dict(sorted(collections.Counter(sign).items())),
minimum_site_pulse_sign_switches=best_cost,
original_TOE41_native_order_site_switches=prior_cost,
signed_switch_cost_distribution_over_520_parallelisms=dict(sorted(cost_hist.items())),
optimal_native_five_layer_schedule=best_example,
parallelism_example=[[list(spreads[i]) for i in parallel[0]]] if parallel else [],
all_200_spreads=[list(s) for s in spreads],all_520_parallelisms=[list(x) for x in parallel],
first_spread=list(spreads[0]),seconds=time.time()-start,
prior_art="The 200 spreads and 520 fans/parallelisms are known for GQ(2,4)/GQ(4,2); see Brouwer-Schlaefli tables and Saniga arXiv:1001.0659. TOE42 adds native triad indices and signed gate-order cost, not a discovery of the 200/520 totals.",
boundary="Sign-switch optimization is a toy hardware controller proxy in fixed native triad sign convention; it is not a physical resource cost or invariant of coordinate sign flips.")
(root/"data/w33_20261010_toe42_native_e6_spreads.json").write_text(json.dumps(output,indent=2)+"\n")
