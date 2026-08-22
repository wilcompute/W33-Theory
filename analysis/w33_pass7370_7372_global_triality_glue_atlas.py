#!/usr/bin/env python3
"""Pass7370-7372: globally resolve the 45 orthogonal D4-pair glue maps in the Coxeter-phase gauge."""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import networkx as nx
import w33_pass7163_7170_e8_hexagonal_lift as e8
import w33_pass7182_d4_glue_spread_code as d4m
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'PART_W33_PASS7370_7372_GLOBAL_TRIALITY_GLUE_ATLAS.json'

def main():
 R,fib,phase,radj,adj,zero,twelve,diff=e8.e8_fibers();I={r:i for i,r in enumerate(R)};neg={i:I[tuple(-x for x in R[i])] for i in range(240)};rep=sorted({min(i,neg[i]) for i in range(240)})
 rf={v:f for f,F in enumerate(fib) for v in F};lf=[rf[r] for r in rep];lp=[phase[rf[r]][r]%3 for r in rep]
 O=[set() for _ in range(120)]
 for i,j in itertools.combinations(range(120),2):
  if e8.dot(R[rep[i]],R[rep[j]])==0:O[i].add(j);O[j].add(i)
 frames=[]
 for a in range(120):
  for b in sorted(x for x in O[a] if x>a):
   X=O[a]&O[b]
   for c in sorted(x for x in X if x>b):
    for d in sorted(x for x in X&O[c] if x>c):frames.append((a,b,c,d))
 RS=set(R);by=defaultdict(list)
 for F in frames:
  V=[R[rep[x]] for x in F];ok=False
  for tail in itertools.product((1,-1),repeat=3):
   sg=(1,)+tail;n=[sum(sg[t]*V[t][k] for t in range(4)) for k in range(8)]
   if all(x%2==0 for x in n) and tuple(x//2 for x in n) in RS:ok=True;break
  if not ok:continue
  S=tuple(i for i,r in enumerate(R) if sum(e8.dot(r,v)**2 for v in V)==64);by[S].append(F)
 assert len(by)==3150 and set(map(len,by.values()))=={3}
 selected={}
 for S,Fs in by.items():
  fsets=[tuple(sorted(lf[x] for x in F)) for F in Fs]
  if len(set(fsets))!=1 or len(set(fsets[0]))!=4:continue
  q=frozenset(fsets[0]);rows=[]
  for F in Fs:
   order=tuple(sorted(F,key=lambda x:lf[x]));sig=tuple(lp[x] for x in order);rows.append((sum(sig)%3,sig,order))
  assert sorted(x[0] for x in rows)==[0,1,2];selected[q]=(S,sorted(rows))
 assert len(selected)==90
 Q,partner=d4m.cqs(adj);P=d4m.pairs(partner);assert len(P)==45 and all(q in selected for q in Q)
 typ=Counter();pairtyp=Counter();records=[];ph=Counter();bytyp=defaultdict(Counter)
 match={frozenset((0,1)):0,frozenset((2,3)):0,frozenset((0,2)):1,frozenset((1,3)):1,frozenset((0,3)):2,frozenset((1,2)):2}
 supports=[];flat_indices=[]
 def tau0(q):return next((sig,F) for t,sig,F in selected[q][1] if t==0)
 def cls(r,F):
  s=frozenset(i for i,x in enumerate(F) if e8.dot(R[r],R[rep[x]])!=0);assert len(s)==2;return match[s]
 for z,(a,b) in enumerate(P):
  qa,qb=Q[a],Q[b];Sa=selected[qa][0];Sb=selected[qb][0];sa,Fa=tau0(qa);sb,Fb=tau0(qb)
  ta='flat' if len(set(sa))==1 else 'split';tb='flat' if len(set(sb))==1 else 'split';assert ta==tb;typ[ta]+=2;pairtyp[ta]+=1
  outside=[r for r in range(240) if r not in set(Sa) and r not in set(Sb)];C=[[0]*3 for _ in range(3)]
  for r in outside:C[cls(r,Fa)][cls(r,Fb)]+=1
  assert all(sorted(row)==[0,0,64] for row in C) and all(sorted(C[i][j] for i in range(3))==[0,0,64] for j in range(3))
  perm=tuple(max(range(3),key=lambda j:C[i][j]) for i in range(3));ph[perm]+=1;bytyp[ta][perm]+=1
  supports.append(frozenset(qa|qb));
  if ta=='flat':flat_indices.append(z)
  records.append({'pair_index':z,'type':ta,'tau0_phase_A':list(sa),'tau0_phase_B':list(sb),'glue_permutation':list(perm)})
 assert typ==Counter({'split':66,'flat':24}) and pairtyp==Counter({'split':33,'flat':12})
 assert ph==Counter({(2,0,1):14,(0,1,2):14,(0,2,1):11,(1,0,2):4,(2,1,0):2})
 assert bytyp['flat']==Counter({(0,1,2):12})
 G=nx.Graph();G.add_nodes_from(range(45))
 for i,j in itertools.combinations(range(45),2):
  if supports[i].isdisjoint(supports[j]):G.add_edge(i,j)
 H=G.subgraph(flat_indices);comps=sorted(len(c) for c in nx.connected_components(H));assert comps==[4,4,4] and H.number_of_edges()==18 and set(dict(H.degree()).values())=={3}
 out={'schema':'w33.pass7370_7372.global_triality_glue_atlas.v1','status':'PASS','selected_D4':90,'D4_phase_types':{'split':66,'flat':24},'orthogonal_pairs':45,'pair_types':{'split_split':33,'flat_flat':12,'mixed':0},'gauge':'For each D4 choose tau=0 frame; order its four root lines by Coxeter-fiber id; identify the three D4 discriminant labels with the three perfect matchings 01|23, 02|13, 03|12.','mixed_root_glue_law':'For every orthogonal D4 pair the 192 E8 roots outside the two D4 root systems give 64 copies of each of three matched discriminant classes and zero off the matching; hence a 3x3 permutation matrix records the actual diagonal glue.','glue_permutation_histogram':{str(k):v for k,v in sorted(ph.items())},'flat_pairs_all_identity':True,'flat_coordinate_subgraph':'3 K4 under the selected-45 disjoint-support/tritangent relation','records':records,'boundary':'The atlas is canonical relative to the fixed Coxeter phase origin and fiber ordering. Renaming the three perfect matchings globally renames v/s/c; the pairwise E8 glue permutations themselves are exact.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','pairs':45,'flat':12,'split':33,'flat_graph':'3K4'}))
if __name__=='__main__':main()
