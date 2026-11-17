"""SUSY obstruction: conventional N=1 SU5 adjoint cubic W has exactly
THREE inequivalent Hermitian D-flat F-flat orbit branches (including 0).
Both 3+2 and 4+1 have zero rigid-SUSY vacuum energy. Therefore neither
cubic W nor its F-term potential dynamically selects 3+2 by energy.

A small SOFT negative m_soft^2 Tr(Phi²) splits these branches to first
order; this is a conditional example, not an E6-derived soft sector.
"""
from pathlib import Path
import json
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261117_SUSY_SU5_adj_cubic_Fflat_soft_lift.json"

def exact():
    m,y=s.symbols("m y",nonzero=True,real=True)
    roots=[]
    for k in (1,2,3,4):
        n=5-k
        a=s.factor(-n*m/(y*(5-2*k)))
        b=s.factor(k*m/(y*(5-2*k)))
        x=[a]*k+[b]*n
        p2=s.simplify(sum(z*z for z in x))
        p3=s.simplify(sum(z*z*z for z in x))
        f=[s.factor(m*z+y*(z*z-p2/5)) for z in x]
        assert all(z==0 for z in f)
        W=s.simplify(m*p2/2+y*p3/3)
        branch="3+2" if min(k,n)==2 else "4+1"
        roots.append({"k":k,"eigenvalues":[str(v) for v in x],
                      "branch":branch,
                      "TrPhi2":str(p2),"TrPhi3":str(p3),
                      "W_value":str(W),"VF":0,"D_flat_if_Hermitian":True})
    # k and 5-k give same multiset for both two-eigenvalue branches
    for i in (0,1):
        assert sorted(roots[i]["eigenvalues"])==sorted(roots[3-i]["eigenvalues"])
    # Above string sorting OK for equal lists? k1 vs k4 representation identical.
    assert roots[0]["TrPhi2"]==str(s.Rational(20,9)*m*m/y**2)
    assert roots[1]["TrPhi2"]==str(30*m*m/y**2)
    assert s.simplify(s.sympify(roots[1]["W_value"],locals={"m":m,"y":y})-5*m**3/y**2)==0
    assert s.simplify(s.sympify(roots[0]["W_value"],locals={"m":m,"y":y})-s.Rational(10,27)*m**3/y**2)==0
    return {"model":"Rigid global N=1 SUSY, one traceless adjoint chiral Sigma, W=(m/2)TrSigma²+(y/3)TrSigma³",
      "F_eigenvalue_condition":"m*x_i + y*(x_i² - TrSigma²/5)=0",
      "two_roots_relation":"a+b=-m/y and k*a+(5-k)*b=0",
      "branches":roots,
      "physically_distinct_Hermitian_orbits":{"symmetric_origin":"Sigma=0, VF=VD=0",
         "SU4_U1":"TrSigma²=20m²/(9y²), VF=VD=0",
         "SU3_SU2_U1":"TrSigma²=30m²/y², VF=VD=0"},
      "no_unique_SUSY_vacuum":"The three branches are exactly degenerate in the rigid-SUSY F+D potential at V=0; different W values do not change rigid-SUSY energy.",
      "SUGRA_warning":"Supergravity vacuum energy depends on e^K(|D W|² -3|W|²/MPl²), as well as Kähler potential; do NOT select a branch simply by inserting -3|W|² while ignoring covariant F terms and uplift."}

def soft_lift():
    eps=s.symbols("eps",positive=True,real=True)
    m,y=s.symbols("m y",positive=True,real=True)
    ssm=30*m*m/y**2
    su4=s.Rational(20,9)*m*m/y**2
    diff=s.simplify(-eps*(ssm-su4))
    assert diff==-s.Rational(250,9)*eps*m*m/y**2
    assert ssm>su4 # symbolic relational true under positive m,y
    return {"soft_term":"deltaV=-epsilon TrSigma² with epsilon>0; NOT supersymmetric, treated perturbatively",
      "energy_shift_on_Fflat_SM":"-30 epsilon m²/y² + O(epsilon²)",
      "energy_shift_on_Fflat_SU4":"-(20/9)epsilon m²/y² + O(epsilon²)",
      "energy_SM_minus_SU4":str(diff),
      "prefers_SM_over_SU4_and_origin_at_first_order":True,
      "stability_warning":"The full soft-deformed potential must be minimized and tested for other branches and tachyons; leading-order splitting is not a complete global theorem. Soft tachyonic mass is phenomenological, not derived from the parent E6 sector."}

def verify():
    return {"status":"PASS_RIGID_SUSY_SU5_THREE_FFLAT_BRANCHES_NO_SELECTION_AND_SOFT_LIFT",
       "Fflat_branches":exact(),"soft_first_order":soft_lift(),
       "literature":["https://indico.desy.de/event/11392/attachments/3791/4359/Shirai.pdf",
                     "https://arxiv.org/abs/1202.2845"]}

if __name__=="__main__":
    x=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(x["status"])
