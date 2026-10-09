"""Fast rational-point sieve and full geometric Groebner attempt over F3.

Invariant tetraquadrics under simultaneous sign/swap have 21 monomial
orbits. A unit affine Jacobian ideal on each of eight complementary
representative charts mod3 proves an explicit complex-smooth polynomial,
but finding no F3-rational critical points alone never does.
"""
from pathlib import Path
import itertools,random,sys,time,json
import numpy as np
import sympy as S
R=Path(__file__).resolve().parents[1];OUT=R/"data/w33_20261008_invariant_tetraquadric_21dim_mod3_exact_attempt.json"
xx=S.symbols("t0:4")
Ds=[d for d in itertools.product(range(3),repeat=4) if sum(z==1 for z in d)%2==0]
orb=[];seen=set()
for d in Ds:
 if d in seen:continue
 o=sorted({d,tuple(2-t for t in d)})
 orb.append(o);seen.update(o)
assert len(orb)==21
pts=list(itertools.product(range(4),repeat=4))
# p=3 projective finite coordinate t=0,1,2 or infinity represented x=1 y=0..2 and x=0 y=1
def coord(a):return (1,a) if a<3 else (0,1)
def terms(d,pt):
 pro=1
 for e,t in zip(d,pt):
  x,y=coord(t);pro*=x**e*y**(2-e)
 return pro%3
def partial(d,pt,j):
 p=1
 for i,(e,t) in enumerate(zip(d,pt)):
  x,y=coord(t)
  if i==j:
   v=((2-e)*x**e*y**(1-e)) if t<3 and (2-e)>0 else (e*x**(e-1)*y**(2-e) if t==3 and e>0 else 0)
  else:v=x**e*y**(2-e)
  p*=v
 return p%3
M=np.zeros((len(pts),5,21),dtype=np.int64)
for i,p in enumerate(pts):
 for k,o in enumerate(orb):
  M[i,0,k]=sum(terms(d,p) for d in o)%3
  for j in range(4):M[i,j+1,k]=sum(partial(d,p,j) for d in o)%3
def expr(coeff,chart):
 f=S.Integer(0)
 for c,o in zip(coeff,orb):
  if not c:continue
  for d in o:
   mon=S.Integer(c)
   for j,e in enumerate(d):mon*=xx[j]**(e if chart[j] else 2-e)
   f+=mon
 return S.Poly(f,*xx,modulus=3).as_expr()
def main():
 rng=random.Random(20261008);chosen=None;tried=0
 for i in range(1000):
  coeff=[rng.randrange(3) for _ in orb]
  # avoid zero constant body
  if not any(coeff):continue
  evals=np.tensordot(M,np.array(coeff,dtype=np.int64),axes=([2],[0]))%3
  num=int(np.count_nonzero(np.all(evals==0,axis=1)))
  tried+=1
  if num==0:chosen=coeff;break
 if chosen is None:
  return {"attempts":tried,"candidate_avoids_all_F3_projective_singular_points":False,
          "char0_smoothness_proven":False}
 data={"attempts":tried,"coefficients_21_orbits_F3":chosen,
  "projective_P1F3_fourfold_points_examined":256,
  "candidate_avoids_all_F3_projective_singular_points":True,
  "candidate_avoids_geometric_algebraic_closure_singular_points":"unknown",
  "char0_smoothness_proven":False,"unit_Groebner_charts":[],"failed_charts":[]}
 OUT.write_text(json.dumps(data,indent=2)+"\n")
 for chart in itertools.product((0,1),repeat=4):
  if chart>tuple(1-a for a in chart):continue
  f=expr(chosen,chart)
  start=time.perf_counter()
  G=S.groebner([f]+[S.diff(f,z) for z in xx],*xx,modulus=3,order="grevlex")
  good=len(G.polys)==1 and G.polys[0].total_degree()==0
  rec={"chart":list(chart),"Groebner_is_unit":good,"basis_length":len(G.polys),"wall_seconds":round(time.perf_counter()-start,3)}
  (data["unit_Groebner_charts"] if good else data["failed_charts"]).append(rec)
  OUT.write_text(json.dumps(data,indent=2)+"\n")
  print("GB",rec,flush=True)
  if not good:break
 data["char0_smoothness_proven"]=len(data["unit_Groebner_charts"])==8 and not data["failed_charts"]
 OUT.write_text(json.dumps(data,indent=2)+"\n")
 return data
if __name__=="__main__":
 r=main();print({k:v for k,v in r.items() if k!="coefficients_21_orbits_F3"},flush=True)
 print("TETRAQUADRIC_GOOD_REDUCTION_ATTEMPT_DONE")
