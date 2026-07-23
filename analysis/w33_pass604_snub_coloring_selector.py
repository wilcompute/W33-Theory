#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass604_snub_coloring_selector.json'

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
def porder(p):
 q=tuple(range(len(p)))
 for n in range(1,61):
  q=comp(p,q)
  if q==tuple(range(len(p))):return n
 raise AssertionError
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
def action_orbits(group,n):
 rem=set(range(n));out=[]
 while rem:
  x=min(rem);O={g[x] for g in group};out.append(sorted(O));rem-=O
 return out

def payload():
 Z=(0,0);apex=((2,0),Z,Z,Z);edge=(8,-4);V=vertices600();N=tuple(v for v in V if d2(v,apex)==edge)
 E={(i,j) for i in range(12) for j in range(i+1,12) if d2(N[i],N[j])==edge};G=nx.Graph();G.add_nodes_from(range(12));G.add_edges_from(E)
 faces=tuple(t for t in itertools.combinations(range(12),3) if all(tuple(sorted(e)) in E for e in itertools.combinations(t,2)));fd={frozenset(f):i for i,f in enumerate(faces)}
 aut=tuple(tuple(iso[i] for i in range(12)) for iso in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter());comm=[]
 for a in aut:
  ai=inv(a)
  for b in aut:comm.append(comp(comp(comp(a,b),ai),inv(b)))
 rot=closure(comm);center=[a for a in aut if all(comp(a,b)==comp(b,a) for b in aut)];antipode=next(a for a in center if a!=tuple(range(12)))
 opp=tuple(fd[frozenset(antipode[v] for v in f)] for f in faces)
 def fmap(g):return tuple(fd[frozenset(g[v] for v in f)] for f in faces)
 colorings=[]
 for Y in itertools.combinations(range(20),8):
  deg=[0]*12
  for f in Y:
   for v in faces[f]:deg[v]+=1
  if set(deg)=={2}:colorings.append(frozenset(Y))
 unseen=set(colorings);orbits=[]
 while unseen:
  c=next(iter(unseen));O={frozenset(fmap(g)[i] for i in c) for g in rot};unseen-=O;orbits.append(frozenset(O))
 special=next(O for O in orbits if len(O)==5);coloring=sorted(special,key=lambda x:tuple(sorted(x)))[0];stab=frozenset(g for g in rot if frozenset(fmap(g)[i] for i in coloring)==coloring)
 dist=dict(nx.all_pairs_shortest_path_length(G));axes=[];seen=set()
 for i in range(12):
  j=next(j for j in range(12) if dist[i][j]==3)
  if i not in seen:axes.append(frozenset((i,j)));seen|={i,j}
 aid={a:i for i,a in enumerate(axes)};axis_action=frozenset(tuple(aid[frozenset(g[v] for v in a)] for a in axes) for g in stab)
 yellow_pairs=[];seen=set()
 for f in sorted(coloring):
  if f not in seen:yellow_pairs.append(frozenset((f,opp[f])));seen|={f,opp[f]}
 pid={p:i for i,p in enumerate(yellow_pairs)};pair_action=frozenset(tuple(pid[frozenset(fmap(g)[f] for f in p)] for p in yellow_pairs) for g in stab)
 k4edges=list(itertools.combinations(range(4),2));kid={frozenset(e):i for i,e in enumerate(k4edges)}
 edge_action=frozenset(tuple(kid[frozenset((g[a],g[b]))] for a,b in k4edges) for g in pair_action)
 marked=frozenset(g for g in pair_action if g[0]==0);marked_edge_action=frozenset(tuple(kid[frozenset((g[a],g[b]))] for a,b in k4edges) for g in marked)
 ordered_flag=frozenset(g for g in pair_action if g[0]==0 and g[1]==1)
 checks={
  'exact_600cell120_vertex_figure_icosahedron':len(V)==120 and len(N)==12 and len(E)==30 and len(faces)==20,
  'snub_coloring_orbit_size5':len(special)==5,
  'snub_stabilizer_A4_order12':len(stab)==12 and Counter(porder(g) for g in pair_action)==Counter({1:1,2:3,3:8}),
  'six_Singer_axes_remain_transitive':action_orbits(axis_action,6)==[list(range(6))],
  'four_yellow_antipodal_pairs_tetrahedral':len(yellow_pairs)==4 and len(pair_action)==12 and action_orbits(pair_action,4)==[list(range(4))],
  'six_transporter_edges_remain_transitive':len(edge_action)==12 and action_orbits(edge_action,6)==[list(range(6))],
  'mark_one_yellow_pair_leaves_C3':len(marked)==3 and Counter(porder(g) for g in marked)==Counter({1:1,3:2}),
  'marked_pair_splits_transporters_3_plus_3':[len(x) for x in action_orbits(marked_edge_action,6)]==[3,3],
  'ordered_tetrahedral_edge_selects_uniquely':len(ordered_flag)==1,
 }
 return {'schema':'w33.pass604.snub_coloring_selector.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'geometry':{'600cell_vertices':len(V),'vertex_figure_vertices':len(N),'icosahedron_faces':len(faces),'snub_colorings':len(special)},
  'residual_symmetry':{'group':'A4','order':len(stab),'six_axis_orbits':action_orbits(axis_action,6),'four_opposite_yellow_pair_orbits':action_orbits(pair_action,4),'six_tetrahedral_edge_orbits':action_orbits(edge_action,6)},
  'selector_ladder':[
   {'data':'apex plus snub coloring','residual':'A4','transporter_orbits':[6],'selection':'none'},
   {'data':'plus one marked opposite-yellow pair','residual':'C3','transporter_orbits':[3,3],'selection':'binary chirality class, not one rule'},
   {'data':'plus an ordered adjacent yellow-pair flag','residual':'identity','transporter_orbits':[1,1,1,1,1,1],'selection':'unique transporter edge'}],
  'theorem':'A Pass-579 snub coloring does not fix the Pass-599 selector no-go: its A4 stabilizer remains transitive on all six Singer axes and on all six tetrahedral transporter edges. A marked yellow pair leaves two three-element families; an ordered tetrahedral edge is the first datum that selects uniquely.',
  'checks':checks,'boundary':'The tetrahedral six-edge set is canonically isomorphic to the six rank-pairs of Pass 596, but identifying a particular geometric edge with a particular rank-pair still requires the ordered flag recorded by the selector ladder.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 604 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'selector_ladder':p['selector_ladder']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
