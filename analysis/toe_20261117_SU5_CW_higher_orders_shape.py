"""Quantum SU5 vacuum shape: full mirror log potential, exact 6th/8th
terms, local 3+2 angular curvatures, multi-start competitors.

The messenger threshold selects 3+2 locally for some soft splittings.
Here we do not replace the full E6 gauge/Higgs CW action, and we do
not claim a global EFT vacuum outside the heavy-messenger radius.
"""
import math,json,sys
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import minimize
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_soft_SU5_mirror_messenger_CW import F
OUT=ROOT/"data"/"toe_20261117_SU5_CW_sixth_order_local_shape_stability.json"
D=-.1
def f(s):
    return s*s*(np.log(s)-1.5)
def h(x):
    z=np.asarray(x,dtype=float)
    a=(1+z)**2;b=(1-z)**2
    assert np.all(a+D>0) and np.all(b+D>0)
    return (f(a+D)-f(a)+f(b+D)-f(b))/(16*math.pi**2)
def exact():
    z,d=sp.symbols("z d",positive=True)
    func=lambda w: w*w*(sp.log(w)-sp.Rational(3,2))
    g=func(z*z+d)-func(z*z)
    q4=sp.factor(sp.diff(g,z,4)/sp.factorial(4))
    q6=sp.factor(sp.diff(g,z,6)/sp.factorial(6))
    q8=sp.factor(sp.diff(g,z,8)/sp.factorial(8))
    assert sp.simplify(q4-(sp.log(1+d/z**2)-4*d*(2*d+z*z)/(3*(d+z*z)**2)))==0
    expected6=-d*(-d+z*z)*(d*d+10*d*z*z+z**4)/(15*z*z*(d+z*z)**4)
    assert sp.simplify(q6-expected6)==0
    vals={}
    for order,v in ((4,q4),(6,q6),(8,q8)):
        c=float(v.subs({z:1,d:sp.Rational(-1,10)}))/(8*math.pi**2)
        vals[str(order)]=c
    assert vals["4"]>0 and vals["6"]>0 and vals["8"]<0
    return {"quartic_coefficient":vals["4"],"sixth_coefficient":vals["6"],
     "eighth_coefficient":vals["8"],
     "exact_sixth_coefficient_unscaled":str(q6),
     "higher_order_warning":"The O(phi^8) coefficient is negative in the benchmark, so the positive quartic by itself is NOT a proof of global shape stability at arbitrary messenger-scale VEV."}
def shape(r=.2,restarts=64):
    x3=np.array([2.,2.,2.,-3.,-3.])*r/math.sqrt(30)
    x4=np.array([1.,1.,1.,1.,-4.])*r/math.sqrt(20)
    def V(vec):return float(np.sum(h(vec)))
    gap=V(x4)-V(x3)
    assert gap>0
    # High precision compare to the quartic+sextic predictions
    c=exact()
    sixth32=sum((x3/r)**6);sixth41=sum((x4/r)**6)
    pred=(c["quartic_coefficient"]*(13/20-7/30)*r**4+
          c["sixth_coefficient"]*(sixth41-sixth32)*r**6)
    assert abs((gap-pred)/gap)<.005
    # h'(x) and h''(x), computed by centered numerical finite
    # differences with stable precision for x ~0.1; use high precision
    # mpmath derivatives to avoid cancellation.
    import mpmath as mp
    mp.mp.dps=50
    dd=mp.mpf("-0.1")
    def ff(s):return s*s*(mp.log(s)-mp.mpf("1.5"))
    def hh(xx):
        return sum(ff((1+sign*xx)**2+dd)-ff((1+sign*xx)**2)
                   for sign in (1,-1))/(16*mp.pi**2)
    a=mp.mpf(2)*mp.mpf(str(r))/mp.sqrt(30)
    b=-mp.mpf(3)*mp.mpf(str(r))/mp.sqrt(30)
    mu=(mp.diff(hh,a)-mp.diff(hh,b))/(a-b)
    curv3=float(mp.diff(hh,a,2)-mu)
    curv2=float(mp.diff(hh,b,2)-mu)
    assert curv3>0 and curv2>0
    # All exact global minima over fixed norm are not proved.
    # Run multistart BFGS as a stress test, not as proof.
    rng=np.random.default_rng(20261117)
    best=1e99;converged32=0;other=0
    records=[]
    for j in range(restarts):
        u=rng.normal(size=4)
        def phi(v):
            w=np.r_[v,-sum(v)]
            if np.linalg.norm(w)<1e-14:return np.zeros(5)
            return r*w/np.linalg.norm(w)
        result=minimize(lambda v:V(phi(v)),u,method="BFGS",
                 options={"gtol":1e-11,"maxiter":700})
        best=min(best,float(result.fun))
        if abs(result.fun-V(x3))<1e-10:converged32+=1
        else:other+=1
        if j<5:records.append({"result_energy":float(result.fun),"succeeded":bool(result.success)})
    assert best>=V(x3)-1e-10
    assert converged32>0
    return {"fixed_vev_norm":r,
      "mirror_log_potential_3plus2":V(x3),
      "mirror_log_potential_4plus1":V(x4),
      "4plus1_minus_3plus2":gap,
      "quartic_sextic_predicted_difference":pred,
      "SU3_shape_scalar_curvature":curv3,
      "SU2_shape_scalar_curvature":curv2,
      "both_shape_curvatures_positive":True,
      "multistart_random_seed":20261117,
      "multistart_trials":restarts,"converged_to_3plus2_energy":converged32,
      "converged_other_stationary_energies":other,
      "lowest_multistart_energy":best,
      "first_five_optimizer_controls":records,
      "important_limitation":"A constrained fixed-norm 4-real-variable search in a toy SU5 CW potential. Other vacua, E6 degrees of freedom, gauge loops and finite temperature are NOT included; local curvature and finite multistart searches do not establish the full global minimum."}
def verify():
    a=exact();b=shape()
    return {"status":"PASS_SU5_FULL_LOG_QUARTIC_SIXTH_EIGHTH_AND_LOCAL_32_SHAPE",
            "series":a,"shape":b}
if __name__=="__main__":
    x=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(x["status"],x["shape"]["converged_to_3plus2_energy"],x["shape"]["4plus1_minus_3plus2"])
