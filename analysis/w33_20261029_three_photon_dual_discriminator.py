#!/usr/bin/env python3
"""Complete three-photon W33/dual quadrangle discrimination with exact
integer permanents. All 3240 independent input triples per graph are tested
against all 9880 distinct-output triples. Also proves dual CSS [[40,20,4]].
Standard indistinguishable-boson quantum mechanics, not beyond-QM physics.
"""
from collections import Counter,defaultdict
from itertools import combinations,permutations
from pathlib import Path
import json
import numpy as np
from w33_20261029_rectangular_optical_mesh import graph
from w33_incidence_even_line_resolution_20261029 import make_geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261029_three_photon_dual_discriminator.json"
TRIPLES=np.array(list(combinations(range(40),3)),dtype=np.int16)
PERMS=tuple(permutations(range(3)))
def two_graphs():
 pts,lines,*_=make_geometry(3)
 A=graph().astype(np.int64)
 sets=[set(x) for x in lines]
 assert len(sets)==40 and all(len(x)==4 for x in sets)
 B=np.array([[int(i!=j and bool(x&y)) for j,y in enumerate(sets)]
             for i,x in enumerate(sets)],dtype=np.int64)
 eye=np.eye(40,dtype=np.int64);J=np.ones((40,40),dtype=np.int64)
 for M in (A,B):
  assert np.all(M.sum(axis=0)==12)
  assert np.array_equal(M@M,8*eye-2*M+4*J)
 return A,B
def binary_basis(M):
 basis={}
 for i in range(40):
  v=sum(int(M[i,j])<<j for j in range(40))
  while v:
   k=v.bit_length()-1
   if k in basis:v^=basis[k]
   else:basis[k]=v;break
 return basis
def dual_css(B):
 rows=[sum(int(B[i,j])<<j for j in range(40)) for i in range(40)]
 basis=binary_basis(B)
 assert len(basis)==10
 def outside(v):
  while v:
   k=v.bit_length()-1
   if k in basis:v^=basis[k]
   else:return True
  return False
 assert all(rows[i]^rows[j] for i,j in combinations(range(40),2))
 words=[]
 for quad in combinations(range(40),4):
  if rows[quad[0]]^rows[quad[1]]^rows[quad[2]]^rows[quad[3]]==0:
   assert outside(sum(1<<k for k in quad))
   words.append(quad)
 assert len(words)==270
 stabilizers=[0]
 for v in basis.values():stabilizers.extend([x^v for x in stabilizers[:]])
 assert min(x.bit_count() for x in stabilizers if x)==12
 return {"parameters":"[[40,20,4]]_2","binary_adjacency_rank":10,
         "weight4_logicals":270,"minimum_stabilizer_weight":12,
         "example_logical_support":list(words[0])}
def two_hist(A):
 H=2*np.ones((40,40),dtype=np.int64)-5*(np.eye(40,dtype=np.int64)+A)
 hist=Counter();pairs=list(combinations(range(40),2))
 for i,j in pairs:
  category=int(A[i,j])
  for k,l in pairs:
   x=int(H[k,i]*H[l,j]);y=int(H[k,j]*H[l,i])
   hist[(category,(x+y)**2,x*x+y*y)]+=1
 assert sum(hist.values())==780**2
 return hist
def triple_signature(H,abc):
 X=H[TRIPLES[:,:,None],np.array(abc)[None,None,:]]
 amp=np.zeros(len(TRIPLES),dtype=np.int64)
 for i,j,k in PERMS:amp+=X[:,0,i]*X[:,1,j]*X[:,2,k]
 vals,cnt=np.unique(amp*amp,return_counts=True)
 return tuple((int(v),int(c)) for v,c in zip(vals,cnt))
def all_independent_triples(A):
 H=2*np.ones((40,40),dtype=np.int64)-5*(np.eye(40,dtype=np.int64)+A)
 class_counts=Counter();sigs=defaultdict(set);examples={};maxdata={}
 for a,b,c in TRIPLES:
  a,b,c=int(a),int(b),int(c)
  if A[a,b] or A[a,c] or A[b,c]:continue
  t=int(sum(A[a]*A[b]*A[c]))
  signature=triple_signature(H,(a,b,c))
  class_counts[t]+=1;sigs[t].add(signature)
  examples.setdefault(t,[a,b,c])
  maxdata[t]={"numerator":signature[-1][0],
              "denominator":3375**2,"max_probability_output_count":signature[-1][1]}
 assert sum(class_counts.values())==3240
 assert all(len(value)==1 for value in sigs.values())
 return {"input_common_neighbor_counts":{str(k):v for k,v in sorted(class_counts.items())},
         "max_distinct_output_probabilities":{str(k):maxdata[k] for k in sorted(maxdata)},
         "class_example_input_modes":{str(k):v for k,v in sorted(examples.items())},
         "single_permanent_signature_per_class":True}
def main():
 A,B=two_graphs()
 assert (len(binary_basis(A)),len(binary_basis(B)))==(16,10)
 assert two_hist(A)==two_hist(B)
 p=all_independent_triples(A);d=all_independent_triples(B)
 assert p["input_common_neighbor_counts"]=={"1":2880,"4":360}
 assert d["input_common_neighbor_counts"]=={"0":1080,"2":2160}
 assert p["max_distinct_output_probabilities"]["4"]["numerator"]==26244
 assert all(t["numerator"]<=11664 for t in d["max_distinct_output_probabilities"].values())
 result={"status":"PASS","point_binary_rank":16,"dual_binary_rank":10,
  "dual_CSS":dual_css(B),"both_srg":"(40,12,2,4)",
  "global_two_photon_pair_histograms_equal":True,"two_photon_input_output_pairs":608400,
  "three_photon_independent_inputs_per_graph":3240,
  "all_distinct_output_triples_per_input":9880,"point":p,"dual":d,
  "W33_exclusive_distinct_output_event_probability":"26244/11390625 = 0.002304",
  "dual_maximum_probability":"11664/11390625 = 0.001024",
  "physical_scope":"Ideal identical bosons, no photon loss/detector effects; conventional quantum mechanics. Not a fundamental-physics prediction."}
 OUT.write_text(json.dumps(result,indent=2)+"\n")
 print("PASS three-photon discrimination and dual [[40,20,4]]")
if __name__=="__main__":main()
