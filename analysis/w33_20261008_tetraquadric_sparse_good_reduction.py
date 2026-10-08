"""Sparse explicit free Klein-four tetraquadric: exact good reduction test.

Candidate F = product(x_i^2+y_i^2) + 2 product(x_i^2-y_i^2)
            + 3 product(2*x_i*y_i).
It is invariant under simultaneous diag(1,-1) and simultaneous swap.
All 48 ambient nonidentity fixed points are avoided over Q (and mod7).
If every Jacobian ideal over F7 in 8 h-paired charts is unit, smoothness
over Q/C is rigorously certified by good reduction.
"""
from pathlib import Path
import itertools,json,time,sys
import sympy as S
R=Path(__file__).resolve().parents[1];D=R/"data";OUT=D/"w33_20261008_tetraquadric_sparse_good_reduction.json"
z=S.symbols('z0:4')
def chart_poly(bits):
 s=[];d=[];t=[]
 for i,b in enumerate(bits):
  x,y=(1,z[i]) if not b else (z[i],1)
  s.append(x*x+y*y);d.append(x*x-y*y);t.append(2*x*y)
 return S.expand(S.prod(s)+2*S.prod(d)+3*S.prod(t))
def fixed_point_audit():
 # Direct exact complex evaluations of all 48 actual fixed ambient points.
 allsets=[]
 for vals in ((S.Integer(0),S.oo),(S.Integer(1),S.Integer(-1)),(S.I,-S.I)):
  for signs in itertools.product(vals,repeat=4):
   coords=[(S.Integer(0),S.Integer(1)) if t==S.oo else (S.Integer(1),t) for t in signs]
   sa=S.prod(u*u+v*v for u,v in coords)
   da=S.prod(u*u-v*v for u,v in coords)
   ta=S.prod(2*u*v for u,v in coords)
   value=S.simplify(sa+2*da+3*ta)
   assert value!=0,(signs,value)
   allsets.append(value)
 assert len(allsets)==48
 return {"fixed_points_checked":len(allsets),"nonzero_values":[str(v) for v in sorted(set(allsets),key=str)]}
def main():
 audit=fixed_point_audit()
 result={"fixed_point_audit":audit,"polynomial":"prod_i(x_i^2+y_i^2)+2*prod_i(x_i^2-y_i^2)+3*prod_i(2*x_i*y_i)",
    "coefficient_triple_s_d_t":[1,2,3],
    "Z2xZ2_invariant":True,"all_48_ambient_fixed_points_avoided_over_Q":True,
    "all_48_ambient_fixed_points_avoided_mod7":True,
    "fixed_point_nonzero_checks":{"g_values":["1+2","1-2"],"h_values":["16*(1+3)","16*(1-3)"],
       "gh_values":["16*(2+3)","16*(2-3)"]},
    "prime":7,"unit_jacobian_chart_representatives":[],"nonunit_chart":None,
    "all_16_projective_charts_unit_Jacobian_ideal_mod7":False,
    "complex_smoothness_proven":False,"smooth_free_quotient_constructed":False}
 start=time.perf_counter()
 for bits in itertools.product(range(2),repeat=4):
  if bits>tuple(1-b for b in bits):continue
  f=chart_poly(bits)
  deriv=[S.diff(f,v) for v in z]
  print("TRY_CHART",bits,"elapsed",round(time.perf_counter()-start,2),flush=True)
  gb=S.groebner([f]+deriv,*z,modulus=7,order="grevlex")
  unit=len(gb.polys)==1 and gb.polys[0].total_degree()==0
  if not unit:
   result["nonunit_chart"]={"chart_bits":bits,"basis_len":len(gb.polys),
    "interpretation":"Nonunit modular Jacobian cannot certify this candidate's smoothness over C"}
   break
  result["unit_jacobian_chart_representatives"].append(list(bits))
 if len(result["unit_jacobian_chart_representatives"])==8:
  result["all_16_projective_charts_unit_Jacobian_ideal_mod7"]=True
  result["complex_smoothness_proven"]=True
  result["smooth_free_quotient_constructed"]=True
 result["elapsed_seconds"]=time.perf_counter()-start
 return result
if __name__=="__main__":
 v=main();OUT.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n")
 print(json.dumps(v,indent=2),flush=True);print("SPARSE_JACOBIAN_END")
