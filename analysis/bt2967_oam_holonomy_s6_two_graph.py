#!/usr/bin/env python3
"""Pass 2967: exact OAM spread-router gauge curvature and S6 two-graph closure."""
from __future__ import annotations
import collections,itertools,json
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT2967_OAM_HOLONOMY_S6_TWO_GRAPH_results.json'

def norm(v):
 v=tuple(int(x)%3 for x in v);i=next(i for i,x in enumerate(v) if x)
 return tuple(2*x%3 for x in v) if v[i]==2 else v
POINTS=[v for v in itertools.product(range(3),repeat=4) if any(v) and norm(v)==v]
PIN={p:i for i,p in enumerate(POINTS)}
J=np.array([[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]],dtype=int)
def symp(p,q):return int(np.array(p)@J@np.array(q)%3)
LS=set()
for i,j in itertools.combinations(range(40),2):
 if symp(POINTS[i],POINTS[j]):continue
 p=np.array(POINTS[i]);q=np.array(POINTS[j])
 LS.add(tuple(sorted({PIN[norm(a*p+b*q)] for a,b in itertools.product(range(3),repeat=2) if a or b})))
LINES=sorted(LS);BY={p:[] for p in range(40)}
for li,line in enumerate(LINES):
 for p in line:BY[p].append(li)
def spreads():
 out=[]
 def walk(covered,chosen):
  if len(covered)==40:out.append(tuple(sorted(chosen)));return
  rem=set(range(40))-covered
  p=min(rem,key=lambda x:sum(1 for li in BY[x] if not(set(LINES[li])&covered)))
  for li in BY[p]:
   line=set(LINES[li])
   if line&covered:continue
   walk(covered|line,chosen+[li])
 walk(set(),[]);return sorted(set(out))
def compose(p,q):return tuple(p[q[a]] for a in range(4))
def parity(p):return sum(p[a]>p[b] for a in range(4) for b in range(a+1,4))%2
def ctype(p):
 seen=set();lens=[]
 for a in range(4):
  if a in seen:continue
  b=a;n=0
  while b not in seen:seen.add(b);n+=1;b=p[b]
  lens.append(n)
 return tuple(sorted(lens,reverse=True))
def transport(ids):
 spread=[LINES[i] for i in ids];slot={p:s for line in spread for s,p in enumerate(line)};g={}
 for i,j in itertools.permutations(range(10),2):
  perm=[]
  for p in spread[i]:
   target=[q for q in spread[j] if symp(POINTS[p],POINTS[q])==0]
   assert len(target)==1;perm.append(slot[target[0]])
  g[i,j]=tuple(perm);assert sorted(g[i,j])==list(range(4))
 return g
def incidence(blocks):
 G=nx.Graph()
 for p in range(10):G.add_node(('p',p),kind='point')
 for bi,b in enumerate(sorted(blocks)):
  G.add_node(('b',bi),kind='block')
  for p in b:G.add_edge(('p',p),('b',bi))
 return G
def pkey(s):
 s=frozenset(s);c=frozenset(set(range(6))-set(s));return min(tuple(sorted(s)),tuple(sorted(c)))
PARTS=sorted({pkey(s) for s in itertools.combinations(range(6),3)});PI={p:i for i,p in enumerate(PARTS)}
ACTIONS=set()
for sigma in itertools.permutations(range(6)):
 ACTIONS.add(tuple(PI[pkey({sigma[x] for x in p})] for p in PARTS))
assert len(ACTIONS)==720
unseen=set(itertools.combinations(range(10),3));orbits=[]
while unseen:
 seed=min(unseen);orb={tuple(sorted(a[i] for i in seed)) for a in ACTIONS};orbits.append(orb);unseen-=orb
orbits.sort(key=lambda o:min(o));assert [len(o) for o in orbits]==[60,60]
CANON=orbits[0];CIG=incidence(CANON)
def analyze(ids):
 g=transport(ids);edge={(i,j):parity(g[i,j]) for i,j in itertools.combinations(range(10),2)};odd=set();hist=collections.Counter()
 for i,j,k in itertools.combinations(range(10),3):
  h=compose(g[k,i],compose(g[j,k],g[i,j]));hist[ctype(h)]+=1
  cur=parity(h);assert cur==(edge[i,j]+edge[i,k]+edge[j,k])%2
  if cur:odd.add((i,j,k))
 pc=collections.Counter(p for b in odd for p in b);qc=collections.Counter(tuple(sorted(e)) for b in odd for e in itertools.combinations(b,2))
 design=len(odd)==60 and set(pc.values())=={18} and set(qc.values())=={4}
 bianchi=all(sum(tuple(sorted(f)) in odd for f in itertools.combinations(t,3))%2==0 for t in itertools.combinations(range(10),4))
 gauge=True
 for bits in itertools.product(range(2),repeat=10):
  sw={(i,j):(edge[i,j]+bits[i]+bits[j])%2 for i,j in itertools.combinations(range(10),2)}
  rebuilt={(i,j,k) for i,j,k in itertools.combinations(range(10),3) if (sw[i,j]+sw[i,k]+sw[j,k])%2}
  if rebuilt!=odd:gauge=False;break
 iso=nx.algorithms.isomorphism.GraphMatcher(incidence(odd),CIG,node_match=lambda a,b:a['kind']==b['kind']).is_isomorphic()
 R=nx.Graph();R.add_nodes_from(range(10));R.add_edges_from([e for e,v in edge.items() if v])
 return {'hist':hist,'design':design,'bianchi':bianchi,'gauge':gauge,'iso':iso,'edges':R.number_of_edges(),'degrees':tuple(sorted(dict(R.degree()).values())),'petersen':nx.is_isomorphic(R,nx.petersen_graph())}
def main():
 assert len(POINTS)==len(LINES)==40;ss=spreads();assert len(ss)==36;rs=[analyze(s) for s in ss]
 assert all(r['hist']==collections.Counter({(2,1,1):60,(2,2):60}) for r in rs)
 assert all(r['design'] and r['bianchi'] and r['gauge'] and r['iso'] for r in rs);assert rs[0]['petersen']
 aut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(CIG,CIG,node_match=lambda a,b:a['kind']==b['kind']).isomorphisms_iter());assert aut==720
 assert all({tuple(sorted(a[i] for i in b)) for b in CANON}==CANON for a in ACTIONS)
 rh=collections.Counter((r['edges'],r['degrees'],r['petersen']) for r in rs)
 checks={'w33_40_points_40_lines':True,'all_36_spreads_enumerated':True,'every_spread_has_60_transposition_and_60_double_transposition_triangles':True,'odd_holonomies_form_2_10_3_4_design_on_every_spread':True,'tetrahedral_bianchi_identity_on_every_spread':True,'curvature_is_invariant_under_all_1024_vertex_sign_gauges':True,'all_spread_curvatures_are_the_same_s6_two_graph':True,'canonical_switching_representative_is_petersen':True,'two_graph_automorphism_group_order_720':True,'explicit_s6_degree10_action_preserves_curvature_blocks':True}
 result={'schema':'w33.pass2967.oam_holonomy_s6_two_graph.v1','status':'COMPLETE_EXACT_FINITE_GAUGE_CLASSIFICATION','checks':checks,'check_count':10,'spreads':36,'triangle_holonomy':{'transpositions':60,'double_transpositions':60,'odd_curvature_blocks':60,'even_curvature_blocks':60},'odd_curvature_design':{'parameters':'2-(10,3,4)','point_replication':18,'pair_replication':4,'two_graph_axiom':'Every four-mode tetrahedron contains an even number of odd-curvature faces.'},'gauge_field':{'connection':'sign of each S4 inter-line transport permutation','gauge_group_seen_by_parity':'C2^10 / diagonal C2','curvature':'triangle coboundary of the edge-sign 1-cochain','bianchi':'delta^2=0 on every one of the 210 tetrahedra'},'classification':{'switching_class_contains':'Petersen graph','automorphism_group_order':720,'automorphism_group':'PΣL(2,9) ≅ S6','degree10_model':'S6 acting on the ten unordered 3+3 partitions of a six-set','s6_triple_orbits':[60,60]},'raw_slot_gauge_representative_histogram':[{'spread_count':n,'edge_count':k[0],'degree_multiset':list(k[1]),'is_petersen':k[2]} for k,n in sorted(rh.items())],'headline':'The 10x4 OAM spread router carries a spread-independent Z2 curvature: its 60 odd triangle holonomies are the exceptional 10-point S6 two-graph, with the Petersen graph as a switching representative and an exact tetrahedral Bianchi identity.','claim_boundary':'Exact for finite routing permutations; not a measured optical Berry phase or continuum gauge field.'}
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS 10 / 10',result['headline'])
if __name__=='__main__':main()
