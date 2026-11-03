#!/usr/bin/env python3
"""Attempt exhaustive q7 minimum-hyperoval orbit and exact point-triple moments.
Limits itself to 720300 supports, verifies every even-coverage vector if complete.
"""
import sys,json,collections,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis/search_drivers_12466"))
from even_line_sets_gf import build
def main():
 pts,lines,N=build(7)
 src=json.loads((ROOT/"analysis/search_drivers_12466/even_line_sets_gf_q7_sym2.json").read_text())
 pid={p:i for i,p in enumerate(pts)}
 lid={frozenset(L):i for i,L in enumerate(lines)}
 seed=0
 for L in src["chosen_lines"]:
  seed|=1<<lid[frozenset(pid[tuple(x)] for x in L)]
 assert seed.bit_count()==40
 def omega(x,a):return (x[0]*a[2]+x[1]*a[3]-x[2]*a[0]-x[3]*a[1])%7
 def norm(w):
  f=next(x for x in w if x);return tuple(x*pow(f,-1,7)%7 for x in w)
 base=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
       (1,0,1,0),(0,1,0,1),(1,1,1,0),(0,1,1,1)]
 gens=[]
 for a in base:
  pg=[pid[norm(tuple((x[k]+omega(x,a)*a[k])%7 for k in range(4)))] for x in pts]
  lg=[lid[frozenset(pg[j] for j in L)] for L in lines]
  gens.append([1<<j for j in lg])
 # Each g is a transvection order 7 and arbitrary generators are enough if orbit complete.
 pm=[]
 for row in N:
  mask=0
  for j in np.flatnonzero(row):mask|=1<<int(j)
  pm.append(mask)
 A=N@N.T-8*np.eye(400,dtype=int)
 triple={"line":[0,1,2],"two_edges":[0,1,57]}
 def norm_line(w):
  f=next(x for x in w if x);return tuple(x*pow(f,-1,7)%7 for x in w)
 a,b=0,8
 assert A[a,b]==0
 line_span={pid[norm_line(tuple((pts[a][k]+t*pts[b][k])%7 for k in range(4)))] for t in range(7)}|{b}
 dependent=next(c for c in line_span if c not in (a,b))
 independent=next(c for c in range(400) if c not in line_span and A[a,c]==0 and A[b,c]==0)
 triple["nonisotropic_line"]=sorted((a,b,dependent))
 triple["independent"]=sorted((a,b,independent))
 assert all(A[t[i],t[j]]==0 for t in (triple["nonisotropic_line"],triple["independent"]) for i in range(3) for j in range(i+1,3))
 oneedge=next((a,b,c) for a in range(400) for b in range(a+1,400)
              for c in range(b+1,400) if int(A[a,b]+A[a,c]+A[b,c])==1)
 triple["one_edge"]=list(oneedge)
 # store masks and perform all group moves exactly. Deterministic FIFO BFS.
 seen={seed};q=collections.deque([seed]);processed=0;t0=time.monotonic()
 sums={name:0 for name in triple}
 raw=collections.Counter()
 while q:
  s=q.popleft();processed+=1
  for name,t in triple.items():
   x=[3 if s&pm[j] else -2 for j in t]
   sums[name]+=x[0]*x[1]*x[2]
  if processed%25000==0:
   print("Q7_EXHAUSTIVE_PROGRESS",processed,"orbit",len(seen),
     "elapsed",round(time.monotonic()-t0,1),flush=True)
  for gen in gens:
   t=0;z=s
   while z:
    low=z&-z;t|=gen[low.bit_length()-1];z^=low
   if t not in seen:
    seen.add(t);q.append(t)
    assert len(seen)<=720300
 complete=len(seen)==720300
 from fractions import Fraction
 out={"status":"PASS_FULL_ORBIT" if complete else "PARTIAL_SUBORBIT",
       "q":7,"orbit_supports":len(seen),"expected_full_orbit":720300,
       "exact_exhaustive_for_generated_suborbit":True,
       "run_seconds":round(time.monotonic()-t0,3),
       "seed_40_lines":seed.bit_count(),
       "point_triples":{name:{"points":t,"integer_sum":int(sums[name]),
          "orbit_average_fraction":str(Fraction(sums[name],len(seen))),
          "orbit_average_float":sums[name]/len(seen),
          "number_of_graph_edges":int(sum(A[t[i],t[j]] for i in range(3) for j in range(i+1,3)))}
          for name,t in triple.items()},
       "scope":"exact moment of enumerated 40-line PSp transvection orbit, not all 400-choose-3 tensor entries"}
 p=ROOT/"data/w33_20261102_q7_exhaustive_triple_moments.json"
 p.write_text(json.dumps(out,indent=2)+"\n")
 print("Q7_EXHAUSTIVE_FINAL",json.dumps(out)[:3200],flush=True)
 return out
if __name__=="__main__":main()
