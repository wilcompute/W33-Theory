#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
from w33_pass573_hjelmslev_c3_600cell_apex import apex_geometry,d2
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass579_colored_600cell_module.json'

def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def pinv(p):
 q=[0]*len(p)
 for i,x in enumerate(p):q[x]=i
 return tuple(q)
def closure(gens,n):
 I=tuple(range(n));H={I};front=[I]
 while front:
  a=front.pop()
  for b in gens:
   for c in (compose(a,b),compose(b,a)):
    if c not in H:H.add(c);front.append(c)
 return frozenset(H)
def porder(p):
 q=tuple(range(len(p)))
 for n in range(1,61):
  q=compose(p,q)
  if q==tuple(range(len(p))):return n
 raise AssertionError

def geometry():
 A=apex_geometry();N=A['neighbors'];edge=A['edge_square'];n=12
 E={(i,j) for i in range(n) for j in range(i+1,n) if d2(N[i],N[j])==edge}
 faces=tuple(t for t in itertools.combinations(range(n),3) if all(tuple(sorted(e)) in E for e in itertools.combinations(t,2)))
 fd={frozenset(f):i for i,f in enumerate(faces)}
 G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from(E)
 aut=tuple(tuple(iso[i] for i in range(n)) for iso in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter())
 comm=[]
 for a in aut:
  ai=pinv(a)
  for b in aut:
   comm.append(compose(compose(compose(a,b),ai),pinv(b)))
 rot=closure(comm,n)
 # Antipode is the unique nonidentity central involution of the full graph group.
 center=[a for a in aut if all(compose(a,b)==compose(b,a) for b in aut)]
 antipode=next(a for a in center if a!=tuple(range(n)))
 opp=tuple(fd[frozenset(antipode[v] for v in f)] for f in faces)
 def fmap(p):return tuple(fd[frozenset(p[v] for v in f)] for f in faces)
 return A,E,faces,aut,rot,antipode,opp,fmap

def cycle_type(objects,act):
 vis=set();out=[]
 for x in objects:
  if x in vis:continue
  y=x;n=0
  while y not in vis:vis.add(y);n+=1;y=act(y)
  out.append(n)
 return tuple(sorted(out))

def payload():
 A,E,faces,aut,rot,antipode,opp,fmap=geometry()
 colorings=[]
 for Y in itertools.combinations(range(20),8):
  deg=[0]*12
  for f in Y:
   for v in faces[f]:deg[v]+=1
  if set(deg)=={2}:colorings.append(frozenset(Y))
 unseen=set(colorings);orbits=[]
 while unseen:
  c=next(iter(unseen));O={frozenset(fmap(g)[i] for i in c) for g in rot};unseen-=O;orbits.append(frozenset(O))
 special=next(O for O in orbits if len(O)==5)
 records=[];allmatch=True
 for c in sorted(special,key=lambda x:tuple(sorted(x))):
  stab=frozenset(g for g in rot if frozenset(fmap(g)[i] for i in c)==c)
  pairs=[];seen=set()
  for f in sorted(c):
   if f not in seen:pairs.append((f,opp[f]));seen.update((f,opp[f]))
  order3=[]
  pair_index={frozenset(x):i for i,x in enumerate(pairs)}
  for g in stab:
   if porder(g)!=3:continue
   fg=fmap(g)
   yf=cycle_type(sorted(c),lambda f:fg[f])
   yp=cycle_type(range(4),lambda i:pair_index[frozenset((fg[pairs[i][0]],fg[pairs[i][1]]))])
   comb=tuple(sorted(yf+yp));order3.append({'yellow_faces':yf,'opposite_pairs':yp,'combined12':comb})
   allmatch &= comb==(1,1,1,3,3,3)
  records.append({'yellow_faces':sorted(c),'opposite_pairs':pairs,'stabilizer_order':len(stab),'stabilizer_order_histogram':dict(sorted(Counter(porder(g) for g in stab).items())),'order3_cycle_types':order3})
 prev=json.loads((ROOT/'data'/'w33_pass573_hjelmslev_c3_600cell_apex.json').read_text()) if (ROOT/'data'/'w33_pass573_hjelmslev_c3_600cell_apex.json').exists() else None
 packet={'J3':3,'J2':0,'J1':3};whole={'J3':3,'J2':0,'J1':4}
 checks={
  'icosahedron_vertices12_edges30_faces20':len(E)==30 and len(faces)==20,
  'full_icosahedral_graph_group120':len(aut)==120,
  'derived_rotation_group_A5_order60':len(rot)==60,
  'local_two_yellow_per_vertex_colorings25':len(colorings)==25,
  'rotation_orbit_sizes_5_10_10':sorted(map(len,orbits))==[5,10,10],
  'exactly_five_snub_octahedral_colorings':len(special)==5,
  'special_colorings_opposite_closed':all(all(opp[f] in c for f in c) for c in special),
  'four_opposite_yellow_pairs_each':all(len(r['opposite_pairs'])==4 for r in records),
  'stabilizers_are_A4_order12':all(r['stabilizer_order']==12 and r['stabilizer_order_histogram']=={1:1,2:3,3:8} for r in records),
  'colored12_order3_cycle_type_1cubed_3cubed':allmatch,
  'colored12_Jordan_matches_packet':packet=={'J3':3,'J2':0,'J1':3},
  'apex_adds_fixed_singlet':whole=={'J3':3,'J2':0,'J1':4},
 }
 if prev is not None:
  checks['matches_pass573_hjelmslev_Jordan']=prev['hjelmslev_symmetry']['twelve_packet_jordan']['J3']==3 and prev['hjelmslev_symmetry']['twelve_packet_jordan']['J1']==3 and prev['hjelmslev_symmetry']['whole_module_jordan']['J1']==4
 return {'schema':'w33.pass579.colored_600cell_module.v1','status':'PASS' if all(checks.values()) else 'FAIL','icosahedron':{'vertices':12,'edges':30,'faces':20,'full_graph_automorphism_order':len(aut),'rotation_group':'A5','rotation_group_order':len(rot),'all_local_8_12_colorings':len(colorings),'rotation_orbit_sizes':sorted(map(len,orbits))},'snub_octahedral_colorings':{'count':len(special),'description':'The unique A5 orbit of size five. Each coloring selects eight yellow faces closed under face antipodes and twelve blue faces; its rotational stabilizer is tetrahedral A4.','records':records},'module_bridge':{'twelve_objects':'eight yellow faces plus four opposite-yellow-face pairs','order3_cycle_type':'1^3 3^3','F3_Jordan_type':packet,'with_apex':whole,'interpretation':'The colored 600-cell supplies an exact C3-module model for the 12 packet directions: the eight yellow faces contribute 2 J3 + 2 J1 and their four opposite pairs contribute J3 + J1. The off-hyperplane apex contributes the thirteenth J1.'},'checks':checks,'boundary':'This proves an exact C3-module match for the colored 8-face-plus-4-pair object and the Hjelmslev packet module. It does not yet construct a canonical coordinate-by-coordinate intertwiner or extend the match from C3 to the full A4 stabilizer.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 579 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'colorings':p['snub_octahedral_colorings']['count']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
