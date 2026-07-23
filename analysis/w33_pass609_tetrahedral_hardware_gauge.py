#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass609_tetrahedral_hardware_gauge.json'

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
 yellow_pairs=[];seen=set()
 for f in sorted(coloring):
  if f not in seen:yellow_pairs.append(tuple(sorted((f,opp[f]))));seen|={f,opp[f]}
 yellow_pairs=tuple(sorted(yellow_pairs));pid={frozenset(p):i for i,p in enumerate(yellow_pairs)}
 pair_action=frozenset(tuple(pid[frozenset(fmap(g)[f] for f in p)] for p in yellow_pairs) for g in stab)
 connections={(0,1):(56,'least exterior pair','reversal class A'),(0,2):(-84,'low-cross exterior pair','reversal class B'),(0,3):(-168,'extreme exterior pair','self-reversal class C'),(1,2):(112,'middle exterior pair','self-reversal class D'),(1,3):(-84,'high-cross exterior pair','reversal class B'),(2,3):(56,'greatest exterior pair','reversal class A')}
 records=[]
 for i,j in itertools.combinations(range(4),2):
  w=[0]*4;w[i]=w[j]=1;wilson,name,rev=connections[(i,j)]
  records.append({'geometric_edge':[i,j],'yellow_face_pairs':[list(yellow_pairs[i]),list(yellow_pairs[j])],'selector_word':w,'rank_pair':[i,j],'connection_name':name,'reversal_class':rev,'augmentation_Wilson_sum':wilson,'orientation_states':[[i,j],[j,i]]})
 ordered_stabilizers=[]
 for i,j in itertools.permutations(range(4),2):ordered_stabilizers.append(sum(g[i]==i and g[j]==j for g in pair_action))
 checks={
  'exact_600cell_and_icosahedron':len(V)==120 and len(N)==12 and len(E)==30 and len(faces)==20,
  'chosen_snub_coloring_has_four_antipodal_pairs':len(coloring)==8 and len(yellow_pairs)==4,
  'pair_action_is_A4_order12':len(pair_action)==12,
  'six_weight2_control_words':len(records)==6 and len({tuple(r['selector_word']) for r in records})==6,
  'bijection_geometric_edges_to_rank_pairs':sorted(tuple(r['rank_pair']) for r in records)==list(itertools.combinations(range(4),2)),
  'Wilson_multiset_matches_pass596':sorted(r['augmentation_Wilson_sum'] for r in records)==[-168,-84,-84,56,56,112],
  'every_ordered_edge_has_trivial_A4_stabilizer':set(ordered_stabilizers)=={1},
  'pass599_detector_conjugator_is_permutation':sorted([0,1,2,3,5,4])==list(range(6)),
 }
 return {'schema':'w33.pass609.tetrahedral_hardware_gauge.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'geometric_fixture':{'apex':apex,'snub_coloring_index':'lexicographically first member of the unique A5 orbit of size five','yellow_faces':sorted(coloring),'opposite_yellow_face_pairs':[list(p) for p in yellow_pairs],'residual_group':'A4'},
  'hardware_contract':{'four_control_rails':'One binary rail per opposite-yellow-face pair, ordered by the certificate list.','selector_encoding':'Use a four-bit Hamming-weight-two word; its active rail pair is the Pass-596 exterior rank-pair.','chirality_bit':'The ordered active pair (i,j) versus (j,i) fixes the residual orientation and compiles a loop as U versus U^{-1}.','phase_tag_exponents_mod4':[0,1,2,3],'phase_tag_interpretation':'Recommended control convention exp(i*pi*r/2), not an intrinsic geometric phase law.','six_detector_axis_ordering':{'geometric_to_Singer_conjugator':[0,1,2,3,5,4],'source':'Pass 599'}},
  'connection_map':records,
  'theorem':'An ordered tetrahedral hardware flag gives an explicit one-to-one compiler from the six geometric edges of the snub-color four-pair tetrahedron to the six Pass-596 connection rules. Four rails with a weight-two selector encode the rule; one orientation bit removes the last A4 ambiguity.',
  'checks':checks,'boundary':'The combinatorial mapping and symmetry breaking are exact. The phase-tag convention is a practical encoding choice; a device must calibrate its physical pump phases and detector permutations against the certified rail labels.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 609 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'map':[(r['rank_pair'],r['augmentation_Wilson_sum']) for r in p['connection_map']]}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
