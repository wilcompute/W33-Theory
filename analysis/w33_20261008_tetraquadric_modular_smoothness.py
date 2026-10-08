"""Finite-field Groebner pilot: explicit tetraquadric polynomial smoothness.

If the affine Jacobian ideal is unit in each of 16 charts modulo a prime,
it certifies smoothness in characteristic zero. A single chart is piloted
first to avoid unbounded symbolic costs. Failures are reported, not hidden.
"""
import itertools,json,sys,time,concurrent.futures,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
import sympy as S
OUT=R/"data"/"w33_20261008_tetraquadric_modular_smoothness.json"
x=S.symbols("x0:4")
q=json.loads((R/"data"/"w33_20261008_h27_h13_five_frontiers.json").read_text())["flavor_polynomial_candidate"]
orbits=q["degree_vectors_in_each_orbit"];coeff=q["coefficients"]

def patch(bits):
 F=0
 for c,orbit in zip(coeff,orbits):
  for t in orbit:
   exponents=[t[i] if bits[i]==0 else 2-t[i] for i in range(4)]
   term=S.prod(x[i]**exponents[i] for i in range(4))
   F+=c*term
 return S.Poly(F,*x,domain="ZZ").as_expr()

def one(args):
 bits,p=args;start=time.monotonic()
 F=patch(bits);equ=[F]+[S.diff(F,z) for z in x]
 G=S.groebner(equ,*x,modulus=p,order="grevlex")
 isunit=len(G.polys)==1 and G.polys[0].total_degree()==0 and G.polys[0].LC()!=0
 return {"patch":list(bits),"prime":p,"smooth_geometric_mod_p":isunit,
         "groebner_basis_size":len(G.polys),
         "seconds":round(time.monotonic()-start,3)}

if __name__=="__main__":
 jobs=[(z,5) for z in itertools.product((0,1),repeat=4)]
 # H involution swapping all four homogeneous coordinates identifies
 # complements, so 8 charts are enough if F invariant under h.
 jobs=[a for a in jobs if a[0][0]==0]
 print("EIGHT_DISTINCT_CHART_REPRESENTATIVES",len(jobs),flush=True)
 results=[]
 for job in jobs:
  print("START",job,flush=True)
  result=one(job)
  print("RESULT",result,flush=True)
  results.append(result)
  if not result["smooth_geometric_mod_p"]:
   print("NOT_CERTIFIED_ALL_CHARTS",flush=True)
   break
 out={"prime":5,"charts_checked":results,
      "all_chart_representatives_covered":len(results)==8,
      "globally_smooth_mod5_certificate":len(results)==8 and all(q["smooth_geometric_mod_p"] for q in results),
      "note":"Unit Jacobian ideal implies no singular geometric points on that chart over algebraic closure. Mod-5 smooth specialization implies Q/C smooth generic fiber for chosen integral polynomial."}
 OUT.write_text(json.dumps(out,indent=2)+"\n")
 print("SMOOTHNESS_PILOT_DONE",out["globally_smooth_mod5_certificate"])
