#!/usr/bin/env python3
from __future__ import annotations
import collections, hashlib, itertools, json, math
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
ARCH=ROOT/'archive/dirs/TOE_tomotope_flag_model_conjugacy_v01_20260228_bundle/TOE_tomotope_flag_model_conjugacy_v01_20260228/flag_adjacency_r0_r3_permutations.json'
OUT=ROOT/'data/w33_pass2473_tomotope_rank_colour_quotient_obstruction.json'
Q=3
PACK={"residual_to_duad_index":{"10":9,"11":5,"16":6,"18":11,"20":1,"21":4,"26":13,"30":14,"31":12,"38":8,"4":0,"40":2,"42":10,"6":3,"8":7},"residual_vertices":[4,6,8,10,11,16,18,20,21,26,30,31,38,40,42]}

def normalize(v):
 w=tuple(int(x)%Q for x in v)
 for x in w:
  if x:
   z=pow(x,-1,Q);return tuple((z*y)%Q for y in w)
 raise ValueError

def symp(u,v):return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%Q

def build_selected_192():
 points=sorted({normalize(v) for v in itertools.product(range(Q),repeat=4) if any(v)});pidx={p:i for i,p in enumerate(points)}
 A=np.zeros((40,40),dtype=np.int8)
 for i,u in enumerate(points):
  for j in range(i+1,40):
   if symp(u,points[j])==0:A[i,j]=A[j,i]=1
 line_sets=set()
 for i in range(40):
  for j in range(i+1,40):
   if not A[i,j]:continue
   u,v=points[i],points[j];span=set()
   for a,b in itertools.product(range(3),repeat=2):
    w=tuple((a*u[k]+b*v[k])%3 for k in range(4))
    if any(w):span.add(pidx[normalize(w)])
   line_sets.add(tuple(sorted(span)))
 lines=sorted(line_sets)
 octets=[];seen=set()
 for left in itertools.combinations(range(40),4):
  if any(A[a,b] for a,b in itertools.combinations(left,2)):continue
  right=tuple(v for v in range(40) if all(A[v,u] for u in left))
  if len(right)!=4 or any(A[a,b] for a,b in itertools.combinations(right,2)):continue
  key=tuple(sorted((tuple(left),tuple(right))))
  if key not in seen:seen.add(key);octets.append((tuple(left),tuple(right)))
 octets=sorted(octets);res=PACK['residual_vertices'];octs=[set(octets[r][0])|set(octets[r][1]) for r in res]
 labels={};layer={};center={};events=[]
 for tt in itertools.combinations(range(40),3):
  if any(A[x,y] for x,y in itertools.combinations(tt,2)):continue
  c=set(range(40))-set(tt)
  for x in tt:c&={y for y in range(40) if A[x,y]}
  if len(c)!=1:continue
  e=tuple(sorted((next(iter(c)),)+tt));events.append(e)
  deg={x:sum(int(A[x,y]) for y in e if x!=y) for x in e};cc=[x for x,v in deg.items() if v==3];assert len(cc)==1;center[e]=cc[0]
  z=[len(set(e)&o) for o in octs];m=max(z);ix=tuple(i for i,v in enumerate(z) if v==m)
  k='unique' if (m,len(ix))==(3,1) else 'tie2' if (m,len(ix))==(2,2) else 'tie3' if (m,len(ix))==(3,2) else None;assert k
  labels[e]=ix;layer[e]=k
 events=sorted(set(events));assert len(events)==2880
 S=sorted(e for e in events if layer[e] in ('tie2','tie3') and 0 in labels[e]);assert len(S)==192
 return A,S,center,layer

def comp(p,q):return tuple(p[q[i]] for i in range(192))
def order(p):
 seen=set();o=1
 for i in range(192):
  if i in seen:continue
  j=i;n=0
  while j not in seen:seen.add(j);n+=1;j=p[j]
  o=math.lcm(o,n)
 return o

def digest(d):return hashlib.sha256(json.dumps(d,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main(output:Path=OUT):
 A,S,center,layer=build_selected_192();G=nx.Graph();G.add_nodes_from(range(192))
 for i,j in itertools.combinations(range(192),2):
  if len(set(S[i])&set(S[j]))==3:G.add_edge(i,j)
 assert all(center[S[i]]==center[S[j]] for i,j in G.edges())
 local={'vertices':192,'edges':G.number_of_edges(),'degree_histogram':dict(sorted(collections.Counter(dict(G.degree()).values()).items())),
        'component_sizes':sorted(map(len,nx.connected_components(G))),
        'component_edge_counts':sorted(G.subgraph(c).number_of_edges() for c in nx.connected_components(G)),
        'component_layer_profiles':sorted([dict(collections.Counter(layer[S[i]] for i in c)) for c in nx.connected_components(G)],key=str),
        'interpretation':'Two events are adjacent exactly when they share the distinguished center and replace one leaf.'}
 R=json.loads(ARCH.read_text());arch=[]
 for k in range(1,5):
  for names in itertools.combinations(sorted(R),k):
   H=nx.Graph();H.add_nodes_from(range(192))
   for n in names:H.add_edges_from((i,R[n][i]) for i in range(192))
   arch.append({'colors':list(names),'edges':H.number_of_edges(),'degree_histogram':dict(sorted(collections.Counter(dict(H.degree()).values()).items())),'component_sizes':sorted(map(len,nx.connected_components(H)))})
 I=tuple(range(192));group={I};q=collections.deque([I]);gens=[tuple(R[x]) for x in sorted(R)]
 while q:
  x=q.popleft()
  for g in gens:
   y=comp(g,x)
   if y not in group:group.add(y);q.append(y)
 mon={'order':len(group),'order_spectrum':dict(sorted(collections.Counter(map(order,group)).items()))}
 no_match=all(z['degree_histogram']!=local['degree_histogram'] or z['component_sizes']!=local['component_sizes'] for z in arch)
 cert={'schema':'w33.pass2473.tomotope_rank_colour_quotient_obstruction.v1','status':'PASS_NATURAL_CENTER_PRESERVING_EVENT_CHANGE_IS_NOT_A_TOMOTOPE_RANK_COLOUR_QUOTIENT','local_elementary_event_change_graph':local,'archived_rank_colour_unions':arch,'archived_rank_monodromy':mon,
 'ledger_reconciliation':{'archived_flag_file_description':'tomotope-like rank-4 maniplex extracted inside the order-192 axis-line stabilizer','archived_axis_Hplus_spectrum':{'1':1,'2':15,'3':32,'4':24,'8':24},'actual_tomotope_edge_group_spectrum_from_part_CXCIII':{'1':1,'2':27,'3':32,'4':36},'groups_are_not_isomorphic':True},
 'checks':{'local_edges_336':local['edges']==336,'local_degree_biregular_2_5':local['degree_histogram']=={2:96,5:96},'eight_center_components_24':local['component_sizes']==[24]*8,'each_component_42_edges':local['component_edge_counts']==[42]*8,'each_component_12_plus_12':all(x=={'tie2':12,'tie3':12} for x in local['component_layer_profiles']),'all_15_rank_unions_tested':len(arch)==15,'all_rank_unions_regular':all(len(x['degree_histogram'])==1 for x in arch),'no_rank_union_match':no_match,'monodromy_order192':mon['order']==192},
 'theorem':'The canonical local elementary-change relation on the curved-event 192 is the center-preserving one-leaf replacement graph: eight 24-vertex components, each with 42 edges and degree split 2^12 5^12. Every nonempty union of the four archived rank involutions is regular, and exhaustive enumeration of all 15 rank-colour unions yields no matching degree/component profile. Thus the natural center-retaining event-change quotient cannot be the archived tomotope-like rank adjacency system.',
 'boundary':'This rules out the principled quotient that retains event centers and elementary one-leaf changes. It does not rule out an arbitrary coarsening that forgets those intrinsic structures. The archived axis H+ symmetry and the actual tomotope edge group P must remain separately named.'}
 assert all(cert['checks'].values());cert['sha256_without_hash_field']=digest(cert);output.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':cert['status'],'sha256':cert['sha256_without_hash_field']},sort_keys=True))
if __name__=='__main__':main()
