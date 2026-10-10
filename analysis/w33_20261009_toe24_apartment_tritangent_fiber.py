"""Check if Round23's 45 overlap-3 apartment hopping components are precisely
the already-known 45 Pass4585/4659 apartment fibers/tritangent supports."""
from pathlib import Path
from collections import defaultdict,Counter
import sys,json
import numpy as np
from scipy.sparse.csgraph import connected_components
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe23_dynamic_apartment_frame import build
from w33_h1_det_apartment_phase_bridge import POINTS,om
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
OUT=ROOT/'data/w33_20261009_toe24_apartment_tritangent_fiber.json'
def run():
 ap,A3,A2=build()
 n,lab=connected_components(A3,directed=False)
 pts,pidx,lines,lidx,_,Astar,edge_line,oldapt,_=build_geometry()
 oldapt={tuple(sorted(map(int,a))) for a in oldapt}
 # Older fiber code labels the DUAL 40 GQ lines, not our 40 points.
 # Use each apartment's 4 collinear point edges to obtain its 4 GQ lines.
 def dualize(square):
  pp=[pidx[POINTS[i]] for i in square]
  incident=[edge_line[(min(u,v),max(u,v))] for u,v in __import__('itertools').combinations(pp,2) if (min(u,v),max(u,v)) in edge_line]
  return tuple(sorted(set(incident)))
 dual_apartments=[dualize(a) for a in ap]
 assert len(set(dual_apartments))==1620 and set(dual_apartments)==oldapt
 Astar=np.asarray(Astar,dtype=np.uint8)
 cols=[]
 for c in range(40):
  mask=0
  for r in np.flatnonzero(Astar[:,c]):mask|=1<<int(r)
  cols.append(mask)
 allmask=(1<<40)-1
 def rep(x):return min(x,x^allmask)
 def fib(ap):
  x=0
  for v in ap:x^=cols[v]
  return rep(x)
 fvals=sorted({fib(a) for a in dual_apartments})
 print('CHECK DUAL FIBER labels',len(fvals),'simple old',len({fib(a) for a in oldapt}),flush=True)
 assert len(fvals)==135
 fibers=defaultdict(list)
 for j,a in enumerate(dual_apartments):fibers[fib(a)].append(j)
 assert {len(v) for v in fibers.values()}=={12}
 # Each of the 135 labels yields a 16-line support; 3 labels share
 # each of the 45 protected tritangent supports, hence 36 apartments.
 by_support=defaultdict(set)
 for label,ids in fibers.items():
  support=frozenset(x for k in ids for x in dual_apartments[k])
  by_support[support].update(ids)
 assert len(by_support)==45 and {len(v) for v in by_support.values()}=={36}
 comps={frozenset(np.flatnonzero(lab==i)) for i in range(n)}
 fiber_partition={frozenset(v) for v in by_support.values()}
 same=comps==fiber_partition
 # Pair 45 objects by ALL 16-point unions of their apartment rays.
 comp_support={frozenset(x for k in indexes for x in dual_apartments[k]) for indexes in comps}
 fib_support={frozenset(x for k in indexes for x in dual_apartments[k]) for indexes in fiber_partition}
 assert len(comp_support)==45 and len(fib_support)==45
 print('FIBER CROSSCHECK',same,'supports',len(comp_support&fib_support),flush=True)
 assert same
 res=dict(status='PASS',apartment_count=1620,n_components=45,size_each=36,
  group= 'PSp(4,3), order 25920',
  component_partition_equals_prior_Pass4585_4659_fiber_partition=True,
  explicit_45_to_45_equivariant_map='Each A3-connected component of 36 point C4 apartments maps via unique Levi lift to 36 dual line C4 apartments grouped into THREE sets of 12 of the prior Pass4659 XOR labels; each of those sets has the SAME protected 16-line support. This identifies the component with a previously proven E6 tritangent. Existing Pass4616 and Pass4659 prove its PSp-equivariant equivalence to the 45 E6 tritangents.',
  protected_support_count=45,points_per_support=16,expected_PSp_stabilizer=576,
  no_novelty_claim='Pass4585/4616 and Pass4659 ALREADY proved 45 fibers and their equivalence to E6 tritangent supports, with stabilizer 576. The NEW finding is that the Round23 one-ray-change hopping graph has exactly these 45 fibers as its 45 connected components.',
  new_physical_scope='The conditional hopping selection graph realizes a previously known E6 G-set as invariant quantum dynamical sectors when and only when A2 tunneling and other inter-fiber transitions are absent. No physical selection rule excludes them.')
 OUT.write_text(json.dumps(res,indent=2)+'\n')
 return res
if __name__=='__main__':run()
