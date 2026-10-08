#!/usr/bin/env python3
"""Topological rank and independence of a found 45-cycle commuting center atlas."""
import json,sys
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_global_cycle_center_census import cycles
from w33_20261008_six_toe_frontier_followthrough import levi_graph
OUT=ROOT/"data"/"w33_20261008_cycle_atlas_homology_rank.json"
def rank_mod(matrix,p):
 A=[[x%p for x in row] for row in matrix]
 r=0
 for j in range(len(A[0])):
  k=next((i for i in range(r,len(A)) if A[i][j]),None)
  if k is None:continue
  A[r],A[k]=A[k],A[r]
  inv=pow(A[r][j],-1,p)
  A[r]=[(inv*x)%p for x in A[r]]
  for i in range(r+1,len(A)):
   if A[i][j]:
    m=A[i][j]
    A[i]=[(a-m*b)%p for a,b in zip(A[i],A[r])]
  r+=1
  if r==len(A):break
 return r
def main():
 C=cycles()
 atlas=json.loads((ROOT/"data"/"w33_20261008_cycle_center_atlas_constructive.json").read_text())["largest_found_cycle_indices"]
 G=levi_graph()
 # Bipartition fixed, each edge ordered (point,line) for chain signs.
 E=sorted((min(a,b),max(a,b)) for a,b in G.edges())
 ei={e:k for k,e in enumerate(E)}
 assert len(E)==160
 chains=[];unsigned=[]
 for cid in atlas:
  cy=C[cid]
  signed=[0]*160
  for u,v in zip(cy,cy[1:]+cy[:1]):
   assert G.has_edge(u,v)
   signed[ei[(min(u,v),max(u,v))]]+=(1 if u<40 else -1)
  assert sorted(abs(x) for x in signed).count(1)==8
  assert all(sum(signed[ei[(min(u,v),max(u,v))]]*(1 if v<40 else -1) for u in G.neighbors(v))==0 for v in G)
  chains.append(signed);unsigned.append([abs(x) for x in signed])
 ranks={"F2":rank_mod(unsigned,2),"F3":rank_mod(chains,3),"F5":rank_mod(chains,5)}
 char0=sp.Matrix(chains).T
 ker=char0.nullspace()
 assert len(ker)==1
 # Clear denominators and divide common gcd; this is a certified integer relation.
 z=ker[0];lcm=sp.ilcm(*[sp.denom(x) for x in z])
 ints=[int(lcm*x) for x in z]
 gcd=__import__("math").gcd(*ints)
 ints=[v//abs(gcd) for v in ints]
 assert all(sum(ints[i]*chains[i][j] for i in range(len(ints)))==0 for j in range(160))
 ranks["Q"]=int(char0.rank())
 # cycle class in 1D graph = 1-chain, there is no C2 boundary quotient
 x={"selected_apartments":len(atlas),"homology_ranks":ranks,
    "primitive_integral_relation_coefficients":ints,
    "primitive_relation_support_size":sum(v!=0 for v in ints),
    "primitive_relation_coefficient_histogram":dict(__import__("collections").Counter(ints)),
    "all_bipartite_oriented_boundaries_zero":True,
    "cycle_rank_full_Levi":160-80+1,
    "independent_selected_cycle_classes_over_Q_certified_if_some_modp_rank45":45 in ranks.values(),
    "message":"Pairwise commuting local center matrices are independent of cycle-space homology rank, no gravity/observable interpretation follows"}
 return x
if __name__=="__main__":
 x=main()
 OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print(json.dumps(x,indent=2),flush=True)
 print("ATLAS_HOMOLOGY_PASS",flush=True)
