#!/usr/bin/env python3
"""Resolve the local U5(2) degree-165 carrier under 3 x U4(2).

The ATLAS degree-165 standard generators are vendored below as permutations.
The ATLAS straight-line program for the maximal subgroup 3 x U4(2) is applied
exactly.  Its U4(2) factor has orbits 45+120.  The 45 orbit is identified
objectwise with the cubic-surface tritangent carrier by the SRG(45,12,3,3)
'intersect in one cubic line' graph.  The 120 orbit is a near twin of the
classical Steiner trihedral-pair action: its unordered-pair orbit sizes are the
same 120,1620,2160,3240 and its central C3 gives forty 3-blocks, but the 2160
K3,3 lift quotients to the STANDARD W33 point action (rank_F3(A+I)=11), whereas
Pass4870 proves the Steiner quotient is Q(4,3) (rank 15).  Therefore the full
45+120 carrier is not tritangents + classical Steiner pairs.

External input: ATLAS U5(2), degree-165 permutation representation and maximal
subgroup 3 x U4(2), checked independently by ATLAS.
"""
from __future__ import annotations
import importlib.util,itertools,json
from collections import deque,Counter
from pathlib import Path
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_u52_165_e6_45_120_split.json'

A=[2,1,5,7,3,10,4,13,15,6,18,20,8,23,9,16,17,11,28,12,29,31,14,34,36,26,39,19,21,30,22,45,47,24,50,25,41,52,27,55,37,43,42,59,32,62,33,65,49,35,51,38,69,70,40,56,58,57,44,77,79,46,81,64,48,84,86,88,53,54,83,91,73,74,82,76,60,78,61,80,63,75,71,66,85,67,96,68,102,104,72,107,99,109,111,87,97,114,93,100,117,89,120,90,123,124,92,115,94,127,95,112,113,98,108,133,101,118,119,103,125,122,105,106,121,136,110,130,139,128,141,132,116,134,135,126,137,138,129,140,131,149,143,151,145,153,155,148,142,158,144,159,146,154,147,161,157,150,152,160,156,162,163,164,165]
B=[3,4,6,8,9,11,12,14,16,17,19,21,22,20,24,25,26,27,1,2,30,32,33,35,37,38,40,41,42,43,44,46,48,49,51,29,5,53,54,56,57,58,7,60,61,63,64,45,66,67,68,55,10,71,72,73,74,75,76,78,23,80,13,82,83,85,87,15,89,59,90,92,18,93,36,94,95,86,96,91,47,97,98,99,100,31,101,102,103,105,106,108,28,110,112,113,81,115,116,34,118,119,121,122,39,125,126,52,79,70,128,129,130,131,132,134,84,50,123,104,127,135,133,114,62,137,69,138,140,109,142,65,88,117,143,144,145,146,147,77,148,150,120,152,151,154,141,156,157,124,107,160,161,111,136,139,162,159,153,155,163,164,158,165,149]
A=tuple(x-1 for x in A);B=tuple(x-1 for x in B)
SLP=[(2,1,3),(3,3,4),(3,4,5),(4,5,6),(3,6,7),(7,1,4),(4,6,1),(2,2,4),(2,4,5),(5,3,4),(4,5,2)]

def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def invp(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def ppow(p,n):
 if n<0:return ppow(invp(p),-n)
 z=tuple(range(len(p)));x=p
 while n:
  if n&1:z=comp(z,x)
  x=comp(x,x);n//=2
 return z
def order(p):
 z=tuple(range(len(p)))
 for n in range(1,1000):
  z=comp(z,p)
  if z==tuple(range(len(p))):return n
 raise AssertionError
def run_slp():
 r={1:A,2:B}
 for x,y,z in SLP:r[z]=comp(r[x],r[y])
 return r[1],r[2]
def orbits(gens,n):
 unseen=set(range(n));out=[]
 while unseen:
  s=min(unseen);O={s};q=deque([s])
  while q:
   x=q.popleft()
   for g in gens:
    y=g[x]
    if y not in O:O.add(y);q.append(y)
  out.append(sorted(O));unseen-=O
 return sorted(out,key=len)
def restrict(g,O):
 d={x:i for i,x in enumerate(O)};return tuple(d[g[x]] for x in O)
def pair_orbits(gens,n):
 unseen=set(itertools.combinations(range(n),2));out=[]
 while unseen:
  s=min(unseen);O={s};q=deque([s])
  while q:
   i,j=q.popleft()
   for g in gens:
    z=tuple(sorted((g[i],g[j])))
    if z not in O:O.add(z);q.append(z)
  out.append(O);unseen-=O
 return sorted(out,key=len)
def rankp(M,p=3):
 X=np.asarray(M,dtype=np.int64).copy()%p;r=0
 for c in range(X.shape[1]):
  z=next((i for i in range(r,X.shape[0]) if X[i,c]),None)
  if z is None:continue
  X[[r,z]]=X[[z,r]];X[r]=X[r]*pow(int(X[r,c]),-1,p)%p
  for i in range(X.shape[0]):
   if i!=r and X[i,c]:X[i]=(X[i]-X[i,c]*X[r])%p
  r+=1
 return r
def srg(A):
 deg=set(map(int,A.sum(1)));la=set();mu=set();n=len(A)
 for i,j in itertools.combinations(range(n),2):
  z=int(np.logical_and(A[i],A[j]).sum());(la if A[i,j] else mu).add(z)
 assert len(deg)==len(la)==len(mu)==1
 return [n,next(iter(deg)),next(iter(la)),next(iter(mu))]

def main(write=True):
 assert (order(A),order(B),order(comp(A,B)))==(2,5,11)
 h1,h2=run_slp();assert (order(h1),order(h2))==(2,15)
 z=ppow(h2,5);u4=[h1,ppow(h2,6)]
 assert (order(z),order(u4[0]),order(u4[1]),order(comp(*u4)))==(3,2,5,9)
 O=orbits(u4,165);assert list(map(len,O))==[45,120]
 assert sum(z[x]==x for x in O[0])==45 and sum(z[x]==x for x in O[1])==0
 zcycles=orbits([restrict(z,O[1])],120);assert Counter(map(len,zcycles))=={3:40}

 g45=[restrict(g,O[0]) for g in u4];po45=pair_orbits(g45,45);assert list(map(len,po45))==[270,720]
 G45=np.zeros((45,45),dtype=bool)
 for i,j in po45[0]:G45[i,j]=G45[j,i]=1
 assert srg(G45)==[45,12,3,3]
 # Independent cubic carrier: tritangents share one of the 27 cubic lines.
 p=ROOT/'analysis'/'w33_pass4992_4999_common.py';sp=importlib.util.spec_from_file_location('cubic',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
 base=m.build_base();T=base['tritangents'];C=np.zeros((45,45),dtype=bool)
 for i,j in itertools.combinations(range(45),2):
  if len(set(T[i])&set(T[j]))==1:C[i,j]=C[j,i]=1
 assert srg(C)==[45,12,3,3]
 iso45=next(nx.algorithms.isomorphism.GraphMatcher(nx.from_numpy_array(G45),nx.from_numpy_array(C)).isomorphisms_iter())
 assert len(iso45)==45

 g120=[restrict(g,O[1]) for g in u4];po120=pair_orbits(g120,120);sizes=list(map(len,po120));assert sizes==[120,1620,2160,3240]
 R0=po120[0];H0=nx.Graph();H0.add_nodes_from(range(120));H0.add_edges_from(R0)
 blocks=[tuple(sorted(c)) for c in nx.connected_components(H0)];assert len(blocks)==40 and {len(c) for c in blocks}=={3}
 bi={v:i for i,Cb in enumerate(blocks) for v in Cb};Q=np.zeros((40,40),dtype=bool);cross=Counter()
 for i,j in po120[2]:
  a,b=bi[i],bi[j]
  if a!=b:cross[tuple(sorted((a,b)))]+=1
 assert set(cross.values())=={9} and len(cross)==240
 for a,b in cross:Q[a,b]=Q[b,a]=1
 assert srg(Q)==[40,12,2,4]
 rank11=rankp(Q.astype(int)+np.eye(40,dtype=int),3);assert rank11==11
 old=(ROOT/'analysis'/'PASS4870_steiner_w33_quadratic_bridge_insert.tex').read_text()
 assert 'rank}_{\\mathbb F_3}(A_Q+I)=15' in old and 'ne11' in old
 out={'schema':'w33.u52_165_e6_45_120_split.v1','status':'PASS',
 'headline':'Under the ATLAS maximal subgroup 3 x U4(2), the local U5(2) degree-165 carrier splits 45+120. The 45 orbit is concretely isomorphic to the cubic tritangent SRG(45,12,3,3). The 120 orbit has the same pair-orbit sizes and 40x3 block system as the classical Steiner trihedral-pair action, but its 2160 K3,3 lift quotient is the standard W33 point graph (rank_F3(A+I)=11), whereas Pass4870 proves the Steiner quotient is Q(4,3) with rank 15. Thus only the 45 half is the old cubic carrier; the 120 half is a distinct Steiner-twin action.',
 'atlas':{'ambient':'U5(2) degree 165','maximal_subgroup':'3 x U4(2)','orbit_sizes':[45,120],'central_C3_fixed_points':45,'central_C3_cycles_on_120':40},
 'orbit45':{'pair_orbits':[270,720],'small_orbital_srg':[45,12,3,3],'cubic_intersection_graph_isomorphic':True,'explicit_graph_isomorphism':[iso45[i] for i in range(45)]},
 'orbit120':{'pair_orbits':sizes,'central_blocks':'40 K3','2160_relation':'complete K3,3 over quotient edges','quotient_srg':[40,12,2,4],'quotient_rank_F3_A_plus_I':rank11,'identification':'standard W33 point action'},
 'classical_Steiner_control':{'pair_orbits':[120,1620,2160,3240],'blocks':'40 K3','quotient':'Q(4,3) line action','rank_F3_A_plus_I':15,'source':'PASS4870'},
 'boundary':'The 45 carrier has an explicit graph intertwiner to cubic tritangents. The 120 carrier is NOT identified with classical Steiner pairs; the rank-11/rank-15 separator proves they are nonisomorphic degree-120 covers despite matching coarse orbit data.',
 'checks':{'atlas_generator_orders':True,'split_45_120':True,'45_cubic_intertwiner':True,'120_pair_orbits_match':True,'120_quotient_rank11':True,'Steiner_rank15_control':True}}
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
