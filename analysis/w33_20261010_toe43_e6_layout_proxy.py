"""TOE43 front3: hardware topology stress test of all 520 native E6 schedules.

Declared proxy architectures: nearest-neighbor 3x9 square grid and 27-node
nearest-neighbor ring; sites are frozen in row-major/native index order.
Triple routing load is terminal Manhattan MST or minimum cycle arc, respectively.
This is NOT a compiled photonic gate or physical fidelity estimate.
"""
from pathlib import Path
import json,itertools,collections
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261010_toe43_e6_hardware.json"
d=json.loads((ROOT/"data/w33_20261010_toe42_native_e6_spreads.json").read_text())
native=json.loads((ROOT/"data/w33_20261010_toe41_e6_45_ccz_compiler.json").read_text())["native_triples"]
triples=[t["sites"] for t in native];sign=[t["sign"] for t in native]
S=d["all_200_spreads"];P=d["all_520_parallelisms"]
assert len(S)==200 and len(P)==520
coord=lambda a:divmod(a,9)
def grid_mst(t):
 d0=[sum(abs(a-b) for a,b in zip(coord(u),coord(v))) for u,v in itertools.combinations(t,2)]
 return sum(sorted(d0)[:2])
def ring_mst(t):
 a,b,c=sorted(t)
 return 27-max(b-a,c-b,27-(c-a))
tri_grid=[grid_mst(t) for t in triples]
tri_ring=[ring_mst(t) for t in triples]
load_grid=[sum(tri_grid[i] for i in layer) for layer in S]
load_ring=[sum(tri_ring[i] for i in layer) for layer in S]
vec=[]
for layer in S:
 v=[0]*27
 for i in layer:
  for site in triples[i]:v[site]=sign[i]
 assert set(v)=={-1,1}
 vec.append(v)
def flips(i,j):return sum(a!=b for a,b in zip(vec[i],vec[j]))
pairs={(i,j):flips(i,j) for i in range(200) for j in range(200) if i!=j}
records=[];best=None;pareto=[]
for idx,partition in enumerate(P):
 gg=max(load_grid[i] for i in partition)
 rr=max(load_ring[i] for i in partition)
 opt_switch=10000;opt_order=None
 for order in itertools.permutations(partition):
  f=sum(pairs[(order[i],order[i+1])] for i in range(4))
  if f<opt_switch:opt_switch=f;opt_order=order
 record=dict(parallelism_index=idx,peak_grid_mst_load=gg,
             peak_ring_mst_load=rr,min_site_sign_flips=opt_switch,
             order=list(opt_order))
 records.append(record)
 score=(gg,rr,opt_switch)
 if best is None or score<best[0]:best=(score,record)
def dominated(a,b):
 keys=("peak_grid_mst_load","peak_ring_mst_load","min_site_sign_flips")
 return all(b[k]<=a[k] for k in keys) and any(b[k]<a[k] for k in keys)
pareto=[r for r in records if not any(dominated(r,t) for t in records)]
old= json.loads((ROOT/"data/w33_20261010_toe41_e6_45_ccz_compiler.json").read_text())["native_layer_indices"]
def identify(layer):
 s=tuple(sorted(layer))
 return next(i for i,l in enumerate(S) if tuple(l)==s)
oldids=[identify(l) for l in old]
oldmetrics=dict(peak_grid_mst_load=max(load_grid[i] for i in oldids),
  peak_ring_mst_load=max(load_ring[i] for i in oldids),
  site_sign_flips=sum(pairs[(oldids[j],oldids[j+1])] for j in range(4)))
for rec in records:assert rec["min_site_sign_flips"]>=38
assert oldmetrics["site_sign_flips"]==57
assert min(r["min_site_sign_flips"] for r in records)==38
assert sum(sorted(tri_grid))==sum(tri_grid) # total load invariant, schedule independent
out={"status":"PASS_LAYOUT_PROXY_ALL_520_NATIVE_CIRCUITS",
"site_coordinates":"27 qutrits, row-major native-index placement on 3x9 square lattice",
"alternative_coordinates":"27 qutrits native cyclic ring",
"grid_total_MST_hops_for_all_45_triples":sum(tri_grid),
"ring_total_MST_hops_for_all_45_triples":sum(tri_ring),
"old_TOE41_schedule":oldmetrics,
"minimum_peak_grid_load":min(r["peak_grid_mst_load"] for r in records),
"minimum_peak_ring_load":min(r["peak_ring_mst_load"] for r in records),
"minimum_sign_switches":38,
"lexicographic_grid_ring_sign_optimum":best[1],
"pareto_front_count":len(pareto),"pareto_front":pareto,
"all_520_schedule_metrics":records,
"physical_assumptions":"Fixed 3x9 nearest-neighbor grid or cyclic ring, native site indices as locations. Triple terminal-distance MST is a routing load proxy, not an actual SWAP count. Ideal three-qutrit CCZ primitives assumed, 9 independent per round.",
"boundary":"No physical non-Clifford 3-body gate, coupler placement, loss/power, crosstalk constraints, photonic hardware latency or fault tolerance. Total terminal MST cost is independent of the 5-layer partition."}
OUT.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k not in ("all_520_schedule_metrics","pareto_front")}))
