"""Compare central-commutativity with the previously proved chamber apartment Steinberg basis."""
import sys,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_global_cycle_center_census import cycles
from w33_20261008_six_toe_frontier_followthrough import levi_graph
C=cycles();g=levi_graph()
edge=tuple(sorted(g.edges()))[0]
# sorted of tuple pairs sorted by (u,v), exact edge orientation bipartite.
through=[(i,c) for i,c in enumerate(C) if all(v in c for v in edge)]
assert len(through)==81,(edge,len(through))
bad=0;dist=Counter()
for ix,(i,a) in enumerate(through):
 for j,b in through[ix+1:]:
  inter=set(a)&set(b);pp=sum(x<40 for x in inter);ll=sum(x>=40 for x in inter)
  dist[(pp,ll)]+=1
  if pp!=ll:bad+=1
print("CHAMBER",edge,"APARTMENTS",len(through),"PAIRS",81*80//2,"NONCOMMUTING",bad,"DISTRIBUTION",dict(dist))
