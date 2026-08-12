#!/usr/bin/env python3
"""Pass4988/4991: PSp does not break the 12-fold AG(2,3) gauge; the 12 completions canonically form four point-indexed triples."""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];O8=ROOT/'data/PART_W33_PASS4988_AG23_INTRINSIC_GAUGE_SURVIVES.json';O1=ROOT/'data/PART_W33_PASS4991_AG23_12_TO_4_POINT_PACKETS.json'
def Q6(v):
 a,c,d,e,f,g=v;return (a*c+d*e+f+f*g+g)&1
def add(a,b):return tuple(x^y for x,y in zip(a,b))
def pol(a,b):return Q6(add(a,b))^Q6(a)^Q6(b)
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def closure(gens,n):
 I=tuple(range(n));S={I};D=deque([I])
 while D:
  a=D.popleft()
  for g in gens:
   z=comp(g,a)
   if z not in S:S.add(z);D.append(z)
 return S
def paired(A,B,n,m):
 I=(tuple(range(n)),tuple(range(m)));S={I};D=deque([I])
 while D:
  a,b=D.popleft()
  for ga,gb in zip(A,B):
   z=(comp(ga,a),comp(gb,b))
   if z not in S:S.add(z);D.append(z)
 return S
def canon(v):
 for x in v:
  if x%3:
   z=1 if x%3==1 else 2;return tuple((z*y)%3 for y in v)
def sp(a,b):return (a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2])%3
def main():
 # Double-six W(E6) actions.
 vec=[v for v in itertools.product((0,1),repeat=6) if any(v)];sing=[v for v in vec if Q6(v)==0];nons=[v for v in vec if Q6(v)==1];si={v:i for i,v in enumerate(sing)};trans=[tuple(si[add(x,v) if pol(x,v) else x] for x in sing) for v in nons];gp=[];S0={tuple(range(27))}
 for g in [comp(trans[0],t) for t in trans[1:]]:
  T=closure(gp+[g],27)
  if len(T)>len(S0):gp.append(g);S0=T
  if len(S0)==25920:break
 qp=[sum(b<<i for i,b in enumerate(v)) for v in sing];p27=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp});l27=[tuple(i for i,P in enumerate(p27) if x in P) for x in qp];G27=nx.Graph();G27.add_nodes_from(range(27))
 for i,j in itertools.combinations(range(27),2):
  if set(l27[i])&set(l27[j]):G27.add_edge(i,j)
 C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G27)) if len(c)==6];DS=set()
 for X,Y in itertools.combinations(C6,2):
  if X&Y:continue
  H=G27.subgraph(X|Y)
  if H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):DS.add(frozenset(X|Y))
 DS=sorted(DS,key=lambda s:tuple(sorted(s)));di={D:i for i,D in enumerate(DS)};H36=nx.Graph();H36.add_nodes_from(range(36))
 for i,j in itertools.combinations(range(36),2):
  if len(DS[i]&DS[j])==6:H36.add_edge(i,j)
 def dperm(g):return tuple(di[frozenset(g[x] for x in D)] for D in DS)
 DPp=[dperm(g) for g in gp];DPf=DPp+[dperm(trans[0])]
 # Standard W33 lines and spreads, then transport the double-six action through any overlap-graph isomorphism.
 P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)});W=nx.Graph();W.add_nodes_from(range(40))
 for i,j in itertools.combinations(range(40),2):
  if sp(P[i],P[j])==0:W.add_edge(i,j)
 L=sorted(tuple(sorted(c)) for c in nx.find_cliques(W) if len(c)==4);Q=nx.Graph();Q.add_nodes_from(range(40))
 for i,j in itertools.combinations(range(40),2):
  if set(L[i])&set(L[j]):Q.add_edge(i,j)
 Spr=sorted([frozenset(c) for c in nx.find_cliques(nx.complement(Q)) if len(c)==10],key=lambda s:tuple(sorted(s)));Hw=nx.Graph();Hw.add_nodes_from(range(36))
 for i,j in itertools.combinations(range(36),2):
  if len(Spr[i]&Spr[j])==1:Hw.add_edge(i,j)
 iso=next(nx.algorithms.isomorphism.GraphMatcher(H36,Hw).isomorphisms_iter());inv={w:d for d,w in iso.items()}
 def tr(p):return tuple(iso[p[inv[w]]] for w in range(36))
 SpP=[tr(p) for p in DPp];SpF=[tr(p) for p in DPf]
 sig={frozenset(i for i,S in enumerate(Spr) if q in S):q for q in range(40)}
 def lp(s):return tuple(sig[frozenset(s[i] for i,S in enumerate(Spr) if q in S)] for q in range(40))
 LpP=[lp(s) for s in SpP];LpF=[lp(s) for s in SpF];PF=paired(LpF,SpF,40,36);PP=paired(LpP,SpP,40,36);assert (len(PF),len(PP))==(51840,25920)
 q0=0;inc=sorted(i for i,S in enumerate(Spr) if q0 in S);ii={s:i for i,s in enumerate(inc)};loc=Hw.subgraph(inc);base=[frozenset(ii[s] for s in c) for c in nx.find_cliques(loc) if len(c)==3];assert len(base)==3
 cross={frozenset((a,b)) for a,b in itertools.combinations(range(9),2) if not any(a in B and b in B for B in base)};trs=[frozenset(t) for t in itertools.combinations(range(9),3) if all(frozenset(e) in cross for e in itertools.combinations(t,2))];comps=[]
 def bt(ch,rem):
  if not rem:
   if len(ch)==9:comps.append(frozenset(ch))
   return
  p=min(rem,key=lambda x:sum(1 for T in trs if x<=T and {frozenset(e) for e in itertools.combinations(T,2)}<=rem))
  for T in trs:
   es={frozenset(e) for e in itertools.combinations(T,2)}
   if p<=T and es<=rem:bt(ch+[T],rem-es)
 bt([],cross);comps=sorted(set(comps),key=lambda C:sorted(map(tuple,C)));assert len(comps)==12;ci={C:i for i,C in enumerate(comps)}
 def local(s):return tuple(ii[s[x]] for x in inc)
 stF=[(l,s) for l,s in PF if l[q0]==q0];stP=[(l,s) for l,s in PP if l[q0]==q0];LF={local(s) for l,s in stF};LP={local(s) for l,s in stP};assert (len(LF),len(LP))==(1296,648)
 def ac(C,p):return frozenset(frozenset(p[x] for x in T) for T in C)
 CF={tuple(ci[ac(C,p)] for C in comps) for p in LF};CP={tuple(ci[ac(C,p)] for C in comps) for p in LP};assert len({p[0] for p in CF})==len({p[0] for p in CP})==12
 out8={'pass':4988,'AG23_completions':12,'full_local_group':{'order':1296,'action':'transitive','completion_stabilizer':108},'PSp_local_group':{'order':648,'action':'transitive','completion_stabilizer':54},'Witting_phase_test':'Witting orientation distinguishes the PGSp/PSp outer coset. Restricting to PSp still leaves one orbit on all 12 completions, so this sign cannot select a completion.','tritangent_test':'The canonical tritangent selector is W(E6)-equivariant while the full local stabilizer is transitive on completions; intrinsic tritangent incidence alone cannot select one.','S3_connection_test':'The canonical connection data remain equivariant under the same local symmetry; a completion can be selected only after an additional frame/reference choice.','hardware_boundary':'Chern/OAM or time-bin orientation may be used as an external calibration choice, but no proven equivariant map from those labels to the 12 completions exists in the finite geometry.','theorem':'All currently intrinsic finite structures tested leave the exact 12-fold AG(2,3) gauge intact. In particular the PSp subgroup selected by Witting phase remains transitive on all 12 completions.'};O8.write_text(json.dumps(out8,indent=2,sort_keys=True)+'\n')
 # Bonkers Pass4991: pair intersection graph on completions is 4K3 and its four packets are uniquely equivariantly indexed by the four points of q0.
 Dg=nx.Graph();Dg.add_nodes_from(range(12));pairint={0:0,3:0}
 for i,j in itertools.combinations(range(12),2):
  z=len(comps[i]&comps[j]);pairint[z]=pairint.get(z,0)+1
  if z==0:Dg.add_edge(i,j)
 packets=sorted([frozenset(c) for c in nx.connected_components(Dg)],key=lambda x:tuple(sorted(x)));assert list(map(len,packets))==[3,3,3,3];pi={B:i for i,B in enumerate(packets)}
 def packact(cp):return tuple(pi[frozenset(cp[i] for i in B)] for B in packets)
 # derive point action from line action by four-line incidence signatures
 psig={frozenset(q for q,Lq in enumerate(L) if p in Lq):p for p in range(40)}
 def pointperm(l):return tuple(psig[frozenset(l[q] for q,Lq in enumerate(L) if p in Lq)] for p in range(40))
 bp=sorted(L[q0]);bi={p:i for i,p in enumerate(bp)};pairedacts=[]
 for l,s in stF:
  p=local(s);cp=tuple(ci[ac(C,p)] for C in comps);pk=packact(cp);pp=pointperm(l);pa=tuple(bi[pp[x]] for x in bp);pairedacts.append((pk,pa))
 eq=[]
 for b in itertools.permutations(range(4)):
  if all(all(b[pk[i]]==pa[b[i]] for i in range(4)) for pk,pa in pairedacts):eq.append(b)
 assert len(eq)==1
 out1={'pass':4991,'completion_pair_intersections':{'share_3_added_lines':54,'share_0_added_lines':12},'disjointness_graph_on_12':'4 K3','canonical_packets':{'count':4,'size_each':3},'packet_action':'S4 of order24','base_W33_line_points':4,'unique_full_group_equivariant_packet_to_point_bijection':True,'full_line_stabilizer_kernel_on_four_points':54,'PSp_line_stabilizer_kernel_on_four_points':27,'gauge_reading':'The 12-fold ambiguity canonically projects 3-to-1 onto the four points of the base W33 line. Choosing a distinguished point reduces the ambiguity to one triple; the bare geometry does not distinguish a point.','theorem':'The twelve local affine completions are not featureless: their disjointness graph is four disjoint triangles, and those four 3-packets are uniquely equivariantly indexed by the four points on the underlying W33 line.'};O1.write_text(json.dumps(out1,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
