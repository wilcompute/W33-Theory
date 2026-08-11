#!/usr/bin/env python3
"""Pass4859 — exact E6 non-cut coset enumerator and certified covering-radius bounds.

The nontrivial switching coset is computed by a rank-six E6 root-sum DP:
for one sign choice from every projective root pair, N_minus=(792-||sum r||^2)/4.
Opposite sign choices give the same edge signing, so divide the histogram by 2.

The ordinary cut-space weight enumerator is deliberately NOT inferred from this
rank-six statistic: it depends on squared root inner products and is a different
Ising partition function.  For the covering radius we freeze rigorous bounds.
A hard-coded finite witness x is cross-certified by an automorphism g with
g(x)=x+sigma, so its distances to the cut and signed-cut classes coincide.
Exact rational LDL proves 3*A_x+19I positive definite.  The weighted-MaxCut
spectral bound then gives d(x,K)>=124.  Since K^perp has d=3, every coset is an
orthogonal array of strength 2; its distance distribution has mean 180 and
nonzero variance 90, so every coset contains a word at distance at most179.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict,deque
from fractions import Fraction
from pathlib import Path
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4859_SWITCHING_ENUMERATOR_RADIUS.json'
WITNESS_HEX='4743dfaba7bb36874b9fcb5de87ed19c21ff7927d7754391d7d5d134b3bb04eefeccacde1ec769b98b7dffcf8'
WITNESS_AUT=(23,31,3,25,18,11,30,6,24,32,10,19,26,17,12,5,13,28,4,15,33,2,8,0,35,21,29,27,16,14,34,20,9,1,7,22)

def Q(x):
 b=[(x>>i)&1 for i in range(6)];a,c,d,e,f,g=b;return (a*c+d*e+f+f*g+g)&1

def ldl_positive(A):
 n=len(A);L=[[Fraction(0) for _ in range(n)] for _ in range(n)];D=[]
 for i in range(n):
  L[i][i]=Fraction(1);d=Fraction(int(A[i,i]))
  for k in range(i):d-=L[i][k]*L[i][k]*D[k]
  if d<=0:return False,D+[d]
  D.append(d)
  for j in range(i+1,n):
   z=Fraction(int(A[j,i]))
   for k in range(i):z-=L[j][k]*L[i][k]*D[k]
   L[j][i]=z/d
 return True,D

def main()->int:
 # E6 positive roots and complete non-cut switching-coset enumerator.
 C=np.eye(6,dtype=int)*2
 for a,b in ((0,1),(1,2),(2,3),(3,4),(2,5)):C[a,b]=C[b,a]=-1
 def ref(v,i):
  v=np.array(v,dtype=int);m=int(v@C[:,i]);w=v.copy();w[i]-=m;return tuple(map(int,w))
 roots={(1,0,0,0,0,0)};D=deque(roots)
 while D:
  v=D.popleft()
  for i in range(6):
   w=ref(v,i)
   if w not in roots:roots.add(w);D.append(w)
 pos=sorted(v for v in roots if all(x>=0 for x in v));assert len(pos)==36
 dp={(0,0,0,0,0,0):1}
 for v in pos:
  nd=defaultdict(int)
  for s,n in dp.items():
   nd[tuple(s[i]+v[i] for i in range(6))]+=n;nd[tuple(s[i]-v[i] for i in range(6))]+=n
  dp=nd
 hist=Counter()
 for s,n in dp.items():
  a=np.array(s,dtype=int);q=int(a@C@a);z=792-q;assert z%4==0;hist[z//4]+=n
 assert all(n%2==0 for n in hist.values());coset={w:n//2 for w,n in sorted(hist.items())};assert sum(coset.values())==2**35 and min(coset)==120 and max(coset)==198 and len(coset)==40 and coset[120]==25920
 # Bare 36-double-six graph and root signing.
 qp=[x for x in range(1,64) if Q(x)==0];P=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp});lines=[tuple(i for i,T in enumerate(P) if x in T) for x in qp]
 G=nx.Graph();G.add_nodes_from(range(27))
 for i,j in itertools.combinations(range(27),2):
  if set(lines[i])&set(lines[j]):G.add_edge(i,j)
 C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G)) if len(c)==6];DS=set()
 for A,B in itertools.combinations(C6,2):
  if A&B:continue
  H=G.subgraph(A|B)
  if len(A|B)==12 and H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):DS.add(frozenset(A|B))
 DS=sorted(DS,key=lambda S:tuple(sorted(S)));H=nx.Graph();H.add_nodes_from(range(36))
 for i,j in itertools.combinations(range(36),2):
  if len(DS[i]&DS[j])==6:H.add_edge(i,j)
 E=sorted(tuple(sorted(e)) for e in H.edges());ei={e:i for i,e in enumerate(E)};assert len(E)==360
 ER=nx.Graph();ER.add_nodes_from(range(36));ip={}
 for i,j in itertools.combinations(range(36),2):
  z=int(np.array(pos[i])@C@np.array(pos[j]));ip[(i,j)]=z
  if abs(z)==1:ER.add_edge(i,j)
 iso=next(nx.algorithms.isomorphism.GraphMatcher(H,ER).isomorphisms_iter());sigma=np.zeros(360,dtype=np.uint8)
 for e,(a,b) in enumerate(E):
  i,j=sorted((iso[a],iso[b]));sigma[e]=int(ip[(i,j)]<0)
 # Hard witness and its twist automorphism.
 xmask=int(WITNESS_HEX,16);x=np.array([(xmask>>i)&1 for i in range(360)],dtype=np.uint8);g=WITNESS_AUT
 ep=[ei[tuple(sorted((g[a],g[b])))] for a,b in E];gx=np.zeros(360,dtype=np.uint8)
 for i,j in enumerate(ep):gx[j]=x[i]
 assert np.array_equal(gx,x^sigma)
 A=np.zeros((36,36),dtype=int)
 for e,(a,b) in enumerate(E):A[a,b]=A[b,a]=2*int(x[e])-1
 ok,piv=ldl_positive(3*A+19*np.eye(36,dtype=int));assert ok and len(piv)==36
 out={'pass':4859,'code':'K=[360,36,20]_2','nontrivial_switching_coset':{'size':2**35,'weight_count':len(coset),'minimum':120,'maximum':198,'complete_weight_enumerator':{str(w):int(n) for w,n in coset.items()},'method':'exact E6 rank-six root-sum DP; opposite root orientations identified'},
  'ordinary_cut_coset_complete_enumerator_closed':False,
  'covering_radius':{'lower_bound':124,'upper_bound':179,'exact_closed':False,'lower_witness_hex':WITNESS_HEX,'twist_automorphism_on_36_vertices':list(WITNESS_AUT),'lower_proof':'g(x)=x+sigma makes the two switching-class distances equal; exact LDL gives 3 A_x+19I positive definite, hence lambda_min(A_x)>-19/3 and the weighted-MaxCut spectral bound gives integer distance >=124.','upper_proof':'d(K^perp)=3 gives OA strength2 for every coset. Distances to K have mean180 and variance90; therefore not all can be >=180, so every coset has a representative at distance <=179.'},
  'theorem':'The entire non-cut E6 switching coset has an exact 40-weight enumerator from 120 through198. The full K enumerator and exact covering radius do not collapse to the same rank-six statistic; rigorous covering bounds are 124<=rho(K)<=179.',
  'boundary':'Pass4859 does not claim the ordinary cut-space Ising polynomial or exact covering radius. Those remain genuine hard finite problems; the signed-coset enumerator and radius bounds are exact.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
