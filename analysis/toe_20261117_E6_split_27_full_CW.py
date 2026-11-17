"""High-precision full-log test of E6-gauge-invariant TWO-adjoint
split-27 mirror messenger threshold after a B background.

No truncated polynomial in A is used for the vacuum-comparator.
We sum all four messenger pairs over the full 27 SU5 weights,
including 10=Lambda^2 5 and conjugate 5s.
The effective V is a one-loop messenger-only contribution; fixed A
norm is imposed externally. Compute 3+2 vs 4+1 and two shape
curvatures at .03,.05,.1 in M units. Verify quartic coefficient.
"""
from pathlib import Path
import json,math,sys
import mpmath as mp
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_E6_two_adjoint_split_27_threshold import threshold,IRREPS
OUT=ROOT/"data"/"toe_20261117_E6_split_27_full_log_vacuum_shapes.json"
mp.mp.dps=65
QPSI=mp.mpf("-0.2")
QCHI=mp.mpf("0.2")
DELTA=mp.mpf(".25")
def weights(h):
    assert len(h)==5
    return {"10_16":[h[i]+h[j] for i in range(5) for j in range(i+1,5)],
            "5bar_16":[-x for x in h],"1_16":[mp.mpf(0)],
            "5_10":list(h),"5bar_10":[-x for x in h],
            "1_1":[mp.mpf(0)]}
def V(h,subtract=True):
    r=mp.mpf(0);R=weights(h);I=mp.mpf(1)
    f=lambda a:a*a*(mp.log(a)-mp.mpf("1.5"))
    for name,dim,qp,qc,_,__ in IRREPS:
        b=QPSI*qp+QCHI*qc
        assert len(R[name])==dim
        for eig in R[name]:
            for s in (-1,1):
                for t in (-1,1):
                    mass=I+s*eig+t*b
                    msq=mass**2
                    assert msq>0 and msq+DELTA>0
                    r+=f(msq+DELTA)-f(msq)
                    if subtract:
                        m0=(I+t*b)**2
                        r-=f(m0+DELTA)-f(m0)
    return r/(16*mp.pi**2)
def normalized_patterns(rad):
    x=mp.mpf(str(rad))
    a=[2*x/mp.sqrt(30)]*3+[-3*x/mp.sqrt(30)]*2
    b=[x/mp.sqrt(20)]*4+[-4*x/mp.sqrt(20)]
    return a,b
def angular_curvature(a,idx1,idx2):
    rad=mp.sqrt(sum(x*x for x in a))
    v=[mp.mpf(0)]*5
    v[idx1]=1/mp.sqrt(2);v[idx2]=-1/mp.sqrt(2)
    u=[x/rad for x in a]
    assert abs(sum(u[i]*v[i] for i in range(5)))<mp.mpf("1e-50")
    def fun(z):
        den=mp.sqrt(1+z*z)
        return V([rad*(u[i]+z*v[i])/den for i in range(5)])
    return mp.diff(fun,mp.mpf(0),2)
def verify():
    prior=threshold(-.2,.2,.25)
    kappa=mp.mpf(str(prior["kappa_SU5_TrPhi4"]))
    assert kappa>0
    data=[]
    for rs in (".015",".03",".05",".1"):
        a,b=normalized_patterns(rs)
        eps=mp.mpf(rs)
        va=V(a);vb=V(b)
        gap=vb-va
        leading=kappa*mp.mpf(5)/12*eps**4
        assert gap>0
        # Higher-order terms are visible at r/M=.1; at smaller r they
        # approach the independently derived exact quartic coefficient.
        assert abs(gap/leading-1)<mp.mpf(".13")
        c3=angular_curvature(a,0,1)
        c2=angular_curvature(a,3,4)
        assert c3>0 and c2>0
        assert abs(V([-x for x in a])-va)<mp.mpf("1e-45")
        assert abs(V([-x for x in b])-vb)<mp.mpf("1e-45")
        data.append({"norm_r_over_M":rs,"V_SM3plus2":str(va),
         "V_SU4plus1":str(vb),"V4plus1_minus_V3plus2":str(gap),
         "quartic_leading_prediction":str(leading),
         "relative_correction":float(gap/leading-1),
         "3fold_shape_curvature":str(c3),
         "2fold_shape_curvature":str(c2),
         "all_messenger_fermion_and_scalar_masses_positive":True})
    # The B background breaks SO10 but commutes with SU5. 27 complete
    # before the background; full shape potential is gauge invariant
    # under surviving SU5, and mirror s protects sign A.
    return {"status":"PASS_E6_SPLIT_27_FULL_108_MESSENGER_LOG_VACUUM_COMPARATOR",
      "field_content":"4 vectorlike 27+bar27 messenger pairs = 108 Dirac 27-component channels, SU5-adjoint A, SU5 commuting adjoint B",
      "benchmark":{"M":1,"y":1,"u":1,"psi":-.2,"chi":.2,"Delta_positive":.25,
          "kappa_SU5_TrPhi4":float(kappa)},
      "fixed_norm_comparators":data,
      "selected_3plus2_locally_on_fixed_norm":True,
      "critical_scope":"The full logarithm includes all SU5 27 weights and mirror flavors and is unexpanded in A. A's norm and B's VEV are imposed; the full E6 Higgs F/D potential, gauge/gaugino modes, loop counterterms, tunnelling, proton decay and global vacuum minimization remain uncomputed."}
if __name__=="__main__":
    x=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(x["status"])
    print([(a["norm_r_over_M"],a["V4plus1_minus_V3plus2"],a["relative_correction"]) for a in x["fixed_norm_comparators"]])
