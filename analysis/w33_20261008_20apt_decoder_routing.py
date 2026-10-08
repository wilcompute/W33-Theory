"""Bounded-distance CSS lookup decoder and physical SWAP routing obligations.

Exact correction of all Z errors wt<=3 and X errors wt<=2 with
independent syndromes. Three rounds majority tolerates at most one flipped
measurement bit per check, NOT a circuit-level threshold.
"""
import itertools,collections,json,sys,networkx as nx
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology,add,reduce
OUT=ROOT/"data/w33_20261008_20apt_lookup_decoder_SWAP_routing.json"
def wt(x):return x.bit_count()
def make_lookup(rows,limit):
 n=60; cols=[sum((1<<i) for i,r in enumerate(rows) if r>>j&1) for j in range(n)]
 B={}
 for r in rows:add(r,B)
 lead={};inc=collections.Counter()
 for k in range(limit+1):
  for support in itertools.combinations(range(n),k):
   e=sum(1<<i for i in support)
   syn=0
   for j in support:syn^=cols[j]
   if syn not in lead:lead[syn]=e
   else:
    if lead[syn]!=e:
     inc[k]+=1
 return lead,cols,inc
def check_decode(limit,cols,table,stabilizer_basis):
 tot=0;nonunique=0
 for k in range(limit+1):
  for inds in itertools.combinations(range(60),k):
   e=0;syn=0
   for j in inds:e^=1<<j;syn^=cols[j]
   corr=table[syn]
   assert reduce(corr^e,stabilizer_basis)==0
   if e!=corr:nonunique+=1
   tot+=1
 return tot,nonunique
def main():
 V,E,F,stab,H,b1,b2=topology()
 bx={};bz={}
 for row in b1:add(row,bx)
 for row in b2:add(row,bz)
 Ztab,Zcols,Zinc=make_lookup(b1,3)
 Xtab,Xcols,Xinc=make_lookup(b2,2)
 Ztot,Znon=check_decode(3,Zcols,Ztab,bz)
 Xtot,Xnon=check_decode(2,Xcols,Xtab,bx)
 assert Ztot==1+60+1770+34220 and Xtot==1+60+1770
 # Deliberately bounded syndrome fault model.
 assert len(b1)==40 and len(b2)==20
 s=123456789%2**40
 bad1=s ^ (1<<0);bad2=s ^ (1<<5);bad3=s ^ (1<<10)
 def majority(a,b,c):return (a&b)|(a&c)|(b&c)
 assert majority(bad1,bad2,bad3)==s
 # permutation routing on line graph built from cubic W33 support.
 index={e:i for i,e in enumerate(E)}
 LG=nx.Graph();LG.add_nodes_from(range(60))
 incident=collections.defaultdict(list)
 for j,(u,v) in enumerate(E):
  incident[u].append(j);incident[v].append(j)
 for inc in incident.values():
  for u,v in itertools.combinations(inc,2):LG.add_edge(u,v)
 assert set(dict(LG.degree()).values())=={4}
 g=next(h for h in stab if order(h)==4)
 perm=[index[tuple(sorted((g[u],g[v])))] for u,v in E]
 assert len(set(perm))==60
 cycles=[];seen=set()
 for i in range(60):
  if i in seen:continue
  cyc=[];j=i
  while j not in seen:seen.add(j);cyc.append(j);j=perm[j]
  cycles.append(cyc)
 assert len(cycles)==15 and all(len(c)==4 for c in cycles)
 routes=dict(nx.all_pairs_shortest_path_length(LG))
 depths=[routes[i][perm[i]] for i in range(60)]
 return {"CSS_parameters":[60,2,6],
  "Z_error_lookup_weight_bound":3,"X_error_lookup_weight_bound":2,
  "Z_errors_exhaustively_corrected":Ztot,
  "X_errors_exhaustively_corrected":Xtot,
  "Z_distinct_syndromes":len(Ztab),"X_distinct_syndromes":len(Xtab),
  "Z_degenerate_same_syndrome_distinct_error_counts":dict(Zinc),
  "X_degenerate_same_syndrome_distinct_error_counts":dict(Xinc),
  "three_round_majority_tolerates_one_flipped_bit_per_check":True,
  "no_circuit_level_fault_tolerance_or_threshold_proven":True,
  "F20_order4_physical_edge_permutation_cycle_lengths":[len(c) for c in cycles],
  "F20_order4_physical_qubit_4cycles":15,
  "all_to_all_transpositions_for_permutation":45,
  "support_edge_qubit_line_graph_degree":4,
  "max_single_qubit_routing_graph_distance":max(depths),
  "average_single_qubit_routing_graph_distance":sum(depths)/60,
  "single_qubit_route_distance_histogram":dict(collections.Counter(depths)),
  "routing_graph_swaps_not_scheduled":True}
def order(p):
 I=tuple(range(len(p)));x=I
 for n in range(1,33):
  x=tuple(x[p[i]] for i in range(len(p)))
  if x==I:return n
 raise AssertionError
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print(json.dumps(x,indent=2),flush=True);print("BOUNDED_DECODER_PASS")
