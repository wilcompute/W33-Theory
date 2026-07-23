#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass599_600cell_singer_axis_transport.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def closure(gens):
 I=tuple(range(len(gens[0])));H={I};front=[I]
 while front:
  a=front.pop()
  for b in gens:
   for c in (comp(a,b),comp(b,a)):
    if c not in H:H.add(c);front.append(c)
 return frozenset(H)
def cyc(n,c):
 p=list(range(n))
 for a,b in zip(c,c[1:]+c[:1]):p[a]=b
 return tuple(p)
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
def qadd(x,y):return (x[0]+y[0],x[1]+y[1])
def qneg(x):return (-x[0],-x[1])
def qsub(x,y):return qadd(x,qneg(y))
def qmul(x,y):return (x[0]*y[0]+x[1]*y[1],x[0]*y[1]+x[1]*y[0]+x[1]*y[1])
def qsq(x):return qmul(x,x)
def d2(v,w):
 z=(0,0)
 for a,b in zip(v,w):z=qadd(z,qsq(qsub(a,b)))
 return z
def parity4(p):return sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2
def vertices600():
 Z=(0,0);V=set()
 for i in range(4):
  for s in (-1,1):
   x=[Z]*4;x[i]=(2*s,0);V.add(tuple(x))
 for ss in itertools.product((-1,1),repeat=4):V.add(tuple((s,0) for s in ss))
 base=(Z,(-1,1),(1,0),(0,1))
 for p in itertools.permutations(range(4)):
  if parity4(p):continue
  for ss in itertools.product((-1,1),repeat=3):
   x=[];k=0
   for j in p:
    a=base[j]
    if a!=Z:a=(ss[k]*a[0],ss[k]*a[1]);k+=1
    x.append(a)
   V.add(tuple(x))
 return tuple(sorted(V))
def singer_A5():
 S5=list(itertools.permutations(range(5)));subs=set()
 for tail in itertools.permutations((1,2,3,4)):subs.add(closure((cyc(5,(0,)+tail),)))
 subs=tuple(sorted(subs,key=lambda H:sorted(H)));idx={H:i for i,H in enumerate(subs)}
 def conj(g,H):
  gi=inv(g);return frozenset(comp(comp(g,h),gi) for h in H)
 return frozenset(tuple(idx[conj(g,H)] for H in subs) for g in S5 if parity(g)==0)

def payload():
 Z=(0,0);apex=((2,0),Z,Z,Z);edge=(8,-4);V=vertices600();N=tuple(v for v in V if d2(v,apex)==edge)
 E={(i,j) for i in range(12) for j in range(i+1,12) if d2(N[i],N[j])==edge}
 G=nx.Graph();G.add_nodes_from(range(12));G.add_edges_from(E)
 aut=tuple(tuple(iso[i] for i in range(12)) for iso in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter())
 comm=[]
 for a in aut:
  ai=inv(a)
  for b in aut:comm.append(comp(comp(comp(a,b),ai),inv(b)))
 rot=closure(comm);dist=dict(nx.all_pairs_shortest_path_length(G));axes=[];seen=set()
 for i in range(12):
  j=next(j for j in range(12) if dist[i][j]==3)
  if i not in seen:axes.append(frozenset((i,j)));seen|={i,j}
 axes=tuple(axes);aid={a:i for i,a in enumerate(axes)}
 axis_action=frozenset(tuple(aid[frozenset(g[v] for v in a)] for a in axes) for g in rot)
 singer=singer_A5();conjugator=None
 for c in itertools.permutations(range(6)):
  ci=inv(c)
  if frozenset(comp(comp(c,g),ci) for g in axis_action)==singer:conjugator=c;break
 cone=nx.Graph(G);cone.add_node(12);cone.add_edges_from((12,i) for i in range(12))
 cone_aut=tuple(nx.algorithms.isomorphism.GraphMatcher(cone,cone).isomorphisms_iter())
 fixed_axes=[i for i in range(6) if all(g[i]==i for g in axis_action)]
 stabilizer=[g for g in axis_action if g[0]==0]
 checks={
  '600cell_vertices120':len(V)==120,
  'apex_neighbors12':len(N)==12,
  'vertex_figure_icosahedron':len(E)==30 and set(dict(G.degree()).values())=={5},
  'icosahedral_graph_group120':len(aut)==120,
  'rotation_group_A5_order60':len(rot)==60,
  'six_antipodal_axes':len(axes)==6,
  'axis_action_A5_order60':len(axis_action)==60,
  'Singer_action_A5_order60':len(singer)==60,
  'axis_action_conjugate_to_Singer':conjugator is not None,
  'axis_orbit_transitive6':len({g[0] for g in axis_action})==6,
  'axis_stabilizer_D10_order10':len(stabilizer)==10,
  'cone_apex_fixed_by_all_automorphisms':len(cone_aut)==120 and all(a[12]==12 for a in cone_aut),
  'deep_anchor_selects_no_axis':fixed_axes==[],
 }
 return {'schema':'w33.pass599.600cell_singer_axis_transport.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'exact_600cell':{'coordinate_ring':'Z[phi], phi^2=phi+1','vertices':len(V),'chosen_apex':apex,'neighbor_count':len(N),'vertex_figure':'icosahedron','vertex_figure_edges':len(E)},
  'six_axis_transport':{'geometric_objects':'six antipodal vertex pairs of the icosahedral vertex figure','geometric_A5_order':len(axis_action),'Singer_objects':'six Sylow-5 pentagons / P1(F5)','Singer_A5_order':len(singer),'conjugating_permutation':list(conjugator) if conjugator else None,'axis_stabilizer_order':len(stabilizer)},
  'deep_anchor_test':{'cone_automorphism_order':len(cone_aut),'apex_fixed':all(a[12]==12 for a in cone_aut),'A5_axis_orbit_size':len({g[0] for g in axis_action}),'globally_fixed_axes':fixed_axes,'conclusion':'The thirteenth off-hyperplane apex is an A5-singlet. It canonically exposes the six-axis fibre but cannot choose one axis or one Pass-594 transporter gauge.'},
  'theorem':'The Singer P1(F5) fibre is exactly the A5 permutation representation on the six fivefold axes of an actual 600-cell vertex-figure icosahedron. The deep anchor preserves, rather than breaks, that sixfold symmetry.',
  'checks':checks,'boundary':'This is an exact A5-equivariant objectwise transport. It proves a selector no-go: extra orientation or coloring data is required to choose a fibre axis or edge rule; the apex alone cannot do so.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 599 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'axis_action':p['six_axis_transport']['geometric_A5_order']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
