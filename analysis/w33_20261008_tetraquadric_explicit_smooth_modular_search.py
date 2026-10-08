"""Attempt explicit invariant tetraquadric smooth-good-reduction certificate.

Search in the 21 invariant monomial orbits. For fixed prime p=3, a unit
Groebner Jacobian ideal in every affine chart proves geometric smoothness
of reduction, hence characteristic-zero smoothness. We do not infer
smoothness from an Fp point sieve. Up to 3 candidates, 16 charts each.
"""
from pathlib import Path
import itertools,random,json,time,sys
import sympy as S
R=Path(__file__).resolve().parents[1];D=R/"data";OUT=D/"w33_20261008_tetraquadric_explicit_smooth_modular_search.json"
x=S.symbols("x0 x1 x2 x3")
ds=[d for d in itertools.product(range(3),repeat=4) if sum(j==1 for j in d)%2==0]
orbits=[];seen=set()
for d in ds:
 if d in seen:continue
 c=tuple(2-v for v in d)
 orb=sorted({d,c});orbits.append(orb);seen.update(orb)
assert len(orbits)==21
def poly(coefs,chart):
 f=S.Poly(0,*x,modulus=3)
 expr=0
 for a,orb in zip(coefs,orbits):
  for d in orb:
   p=1
   for j in range(4):
    p*=x[j]**(d[j] if chart[j]==0 else 2-d[j])
   expr+=a*p
 return S.Poly(expr,*x,modulus=3)
def singular_in_small_rational_chart(coeffs):
 for pat in itertools.product(range(4),repeat=4):
  coords=[(1,t) if t<3 else (0,1) for t in pat]
  ch=tuple(0 if t<3 else 1 for t in pat)
  args=[t if t<3 else 0 for t in pat]
  ff=poly(coeffs,ch)
  if int(ff.eval(dict(zip(x,args))))%3:continue
  if all(int(S.diff(ff.as_expr(),v).subs(dict(zip(x,args))))%3==0 for v in x):return list(pat)
 return None
def main():
 outcomes=[]
 for seed in range(20261008,20261038):
  r=random.Random(seed);coef=[r.randrange(3) for _ in orbits]
  # force nonzero corner orbit coefficients, necessary to avoid
  # fixed points of simultaneous diagonal sign change.
  for k,o in enumerate(orbits):
   if all(all(t in (0,2) for t in d) for d in o) and coef[k]==0:coef[k]=1
  point=singular_in_small_rational_chart(coef)
  if point is not None:
   outcomes.append({"seed":seed,"skip":"mod3 F3-rational singularity","witness":point})
   continue
  start=time.perf_counter()
  good=[];failure=None
  for ch in itertools.product((0,1),repeat=4):
   if ch>(tuple(1-v for v in ch)):continue
   f=poly(coef,ch)
   polys=[f.as_expr()]+[S.diff(f.as_expr(),u) for u in x]
   gb=S.groebner(polys,*x,order="grevlex",modulus=3)
   if not (len(gb.polys)==1 and gb.polys[0].total_degree()==0):
    failure={"chart":list(ch),"groebner_length":len(gb.polys)}
    break
   good.append(list(ch));print("PASS chart",seed,ch,"elapsed",round(time.perf_counter()-start,2),flush=True)
  rec={"seed":seed,"coefficients":coef,"modulus":3,"certified_char3_chart_representatives":good,
      "all_16_charts_smooth_if_no_failure":failure is None and len(good)==8,
      "first_chart_failure":failure,
      "runtime_seconds":time.perf_counter()-start}
  outcomes.append(rec)
  if rec["all_16_charts_smooth_if_no_failure"]:break
 return {"attempts":outcomes,"char0_smooth_polynomial_certified":any(x.get("all_16_charts_smooth_if_no_failure") for x in outcomes),
   "basis_orbits":orbits,
   "geometry_scope":"If all eight h-paired affine Jacobian ideals are unit over F3, smooth mod3 implies smooth characteristic zero. Need separately certify avoiding all 48 Klein fixed points for free quotient."}
if __name__=="__main__":
 a=main();OUT.write_text(json.dumps(a,indent=2,sort_keys=True)+"\n");print(json.dumps({"attempts":[{"seed":x["seed"],"smooth":x.get("all_16_charts_smooth_if_no_failure"),"failure":x.get("first_chart_failure"),"skip":x.get("skip")} for x in a["attempts"]],"found":a["char0_smooth_polynomial_certified"]},indent=2));print("MODULAR_GROEBNER_SEARCH_END")
