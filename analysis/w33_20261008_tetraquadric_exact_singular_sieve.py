#!/usr/bin/env python3
"""Exact rational singular-point sieve of the explicit tetraquadric candidate.

This is a finite height-bounded search; a positive witness proves failure
of complex smoothness, while a negative search would NOT prove smoothness.
"""
import json,itertools,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];D=ROOT/"data";OUT=D/"w33_20261008_tetraquadric_exact_singular_sieve.json"
data=json.loads((D/"w33_20261008_h27_h13_five_frontiers.json").read_text())["flavor_polynomial_candidate"]
terms=[(int(c),tuple(e)) for c,orbit in zip(data["coefficients"],data["degree_vectors_in_each_orbit"]) for e in orbit]
def exact_eval(coords):
 bits=[0 if a else 1 for a,b in coords]
 x=[b if a else a for a,b in coords]
 y=0;der=[0]*4
 for c,e in terms:
  powers=[e[i] if bits[i]==0 else 2-e[i] for i in range(4)]
  f=[x[i]**powers[i] for i in range(4)]
  val=c
  for v in f:val*=v
  y+=val
  for i in range(4):
   if not powers[i]:continue
   u=c*powers[i]*x[i]**(powers[i]-1)
   for j in range(4):
    if i!=j:u*=f[j]
   der[i]+=u
 return y,der
def build():
 values=[(0,1),(1,0),(1,1),(1,-1),(1,2),(1,-2),(2,1),(2,-1),(1,3),(1,-3),(3,1),(3,-1)]
 sing=[];onsurface=0
 for z in itertools.product(values,repeat=4):
  f,df=exact_eval(z)
  if f==0:
   onsurface+=1
   if all(v==0 for v in df):
    sing.append({"projective_P1_coordinates":[list(t) for t in z],
                 "chart_gradient":df})
    if len(sing)>=16:break
 return {"sample_projective_P1_coordinates":values,"sampled_ambient_points":len(values)**4,
         "hypersurface_rational_points_encountered":onsurface,
         "exact_char0_singular_witnesses":sing,
         "singular_over_C_certified":bool(sing),
         "smooth_over_C_certified":False,
         "interpretation":"Positive exact zero of polynomial and chart derivatives is rigorous complex singularity witness; absence would be an inconclusive bounded search"}
if __name__=="__main__":
 x=build();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in x.items() if k!="sample_projective_P1_coordinates"},flush=True)
 print("TETRAQUADRIC_EXACT_SEARCH_PASS")
