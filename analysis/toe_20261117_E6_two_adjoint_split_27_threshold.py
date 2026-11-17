"""Split E6 27 messenger threshold with TWO adjoint backgrounds A,B.

Actual E6 invariant renormalizable messenger superpotential:
 W=sum_{s=+-1,t=+-1} Fbar_st [ M + s*y*A_78 + t*u*B_78 ] F_st.
Four vectorlike 27+bar27 pairs. Independent exchange parities
A->-A,s->-s and B->-B,t->-t protect the even A potential.
B's vacuum in the SU5-commuting U1psi,U1chi Cartan splits the
27 under SU5 while retaining full E6 covariance BEFORE B condenses:
27 = 10_(psi1,chi-1)+5bar_(1,3)+1_(1,-5)
     +5_(-2,2)+5bar_(-2,-2)+1_(4,0).

Trace identities for H in su5, p_n=sum h_i^n:
tr_10(H²)=3 p2, tr_10(H³)=p3,
tr_10(H^4)=3 p2²-3 p4.
Because the B-dependent loop coefficient differs by irrep,
kappa4=-3 C(B10)+C(B5bar16)+C(B5_10)+C(B5bar_10)
may be nonzero despite Tr27 H⁴=3p2² at B=0.
C(B)=y^4/(8pi²) [F(Delta/(M+B)^2)+F(Delta/(M-B)^2)]
for four s,t pairs; F(t)=log(1+t)-4t(2t+1)/(3(1+t)^2).

This produces an explicit *E6-gauge-invariant operator mechanism*
conditional on stabilized B vacuum and a soft spectrum. It is NOT a
calculated E6 full supersymmetric vacuum or proton-safe UV completion.
"""
import json,math,itertools,sys
from pathlib import Path
from fractions import Fraction
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_soft_SU5_mirror_messenger_CW import F
OUT=ROOT/"data"/"toe_20261117_E6_two_adjoint_split_messenger_threshold.json"
IRREPS=(("10_16",10,1,-1,-3,3),
        ("5bar_16",5,1,3,1,0),
        ("1_16",1,1,-5,0,0),
        ("5_10",5,-2,2,1,0),
        ("5bar_10",5,-2,-2,1,0),
        ("1_1",1,4,0,0,0))
def trace_identity():
    h=s.symbols("h0:5")
    hh=list(h[:4])+[-sum(h[:4])]
    p=lambda n:s.expand(sum(z**n for z in hh))
    wt=[hh[i]+hh[j] for i in range(5) for j in range(i+1,5)]
    ids={
     2:s.expand(sum(z*z for z in wt)-3*p(2)),
     3:s.expand(sum(z**3 for z in wt)-p(3)),
     4:s.expand(sum(z**4 for z in wt)-(3*p(2)**2-3*p(4))),
    }
    assert all(v==0 for v in ids.values())
    # 27 has 10, bar5,1,5,bar5,1:
    assert sum(row[1] for row in IRREPS)==27
    assert sum(row[4] for row in IRREPS)==0
    assert sum(row[5] for row in IRREPS)==3
    assert sum(row[4] for row in IRREPS if row[2]==1)==-2
    assert sum(row[4] for row in IRREPS if row[2]==-2)==2
    return {"tr10_H2":"3p2","tr10_H3":"p3","tr10_H4":"3p2²-3p4",
      "Tr27_full_H4":"3p2² independent of p4",
      "p4_irrep_coefficients":{x[0]:x[4] for x in IRREPS},
      "SU5_rep_branching_weights":[{"irrep":x[0],"dimension":x[1],
        "qpsi":x[2],"qchi":x[3],"p4_coeff":x[4],"p2_squared_coeff":x[5]} for x in IRREPS]}
def c(B,Delta,M=1,y=1):
    vals=[]
    for t in (-1,1):
        m=M+t*B
        if abs(m)<1e-8 or m*m+Delta<=0:return None
        vals.append(F(Delta/(m*m)))
    return (y**4)/(8*math.pi**2)*sum(vals)
def threshold(psi,chi,Delta,M=1):
    rows=[]
    p4=0
    for name,dim,qp,qc,k4,k22 in IRREPS:
        B=psi*qp+chi*qc
        C=c(B,Delta,M)
        if C is None:return None
        p4+=k4*C
        rows.append({"SU5_irrep":name,"qpsi":qp,"qchi":qc,
           "mass_split_B_over_M":B/M,
           "min_fermion_mass_abs":min(abs(M+B),abs(M-B)),
           "min_scalar_mass2":min((M+B)**2+Delta,(M-B)**2+Delta),
           "TrPhi4_quartic_coefficient":C*k4,
           "loop_scalar_irrep_weight":C})
    return {"vpsi":psi,"vchi":chi,"Delta":Delta,
       "kappa_SU5_TrPhi4":p4,
       "irrep":rows,
       "full_SUSY_heavy_scalars_positive":all(x["min_scalar_mass2"]>0 for x in rows),
       "exact_sign_protected":"s-messenger exchange A->-A retains even A powers at fixed B, unlike a single mirror parity broken by B VEV"}
def scan():
    vals=[]
    for Delta in (-.25,-.1,-.05,.05,.1,.25):
      for ps in (-.2,-.1,0,.1,.2):
       for ch in (-.2,-.1,0,.1,.2):
        z=threshold(ps,ch,Delta)
        if z is None:continue
        vals.append(z)
    positives=sorted((z for z in vals if z["kappa_SU5_TrPhi4"]>1e-8),
        key=lambda z:-z["kappa_SU5_TrPhi4"])
    negatives=sorted((z for z in vals if z["kappa_SU5_TrPhi4"]< -1e-8),
        key=lambda z:z["kappa_SU5_TrPhi4"])
    assert any(z["vchi"]!=0 for z in positives)
    assert any(z["vchi"]!=0 for z in negatives)
    assert all(abs(threshold(0,0,delta)["kappa_SU5_TrPhi4"])<1e-14
               for delta in (-.25,-.1,-.05,.05,.1,.25))
    return {"candidates_analyzed":len(vals),
       "positive_count":len(positives),"negative_count":len(negatives),
       "best_positive":positives[0] if positives else None,
       "best_negative":negatives[0] if negatives else None,
       "examples_positive":positives[:5],
       "no_background":"kappa4=0 identically for B=0 because full E6 27 has no degree-4 shape invariant.",
       "validity":"Loop expansion for A small relative to every 27 messenger mass |M+tB|, and positive scalar mass². The B vacuum is assumed, not derived."}
def verify():
    result={"status":"PASS_E6_TWO_ADJOINT_SPLIT_27_QUARTIC_SELECTOR_WITH_MIRROR_PARITY",
       "E6_branching_and_trace":trace_identity(),"loop_scan":scan(),
       "operator":"W=sum_{s,t=+-} Fbar_st(M+s*y*A78+t*u*B78)F_st. SU5-commuting <B>=psi Qpsi+chi Qchi; evaluate quartic in A's SU5 adjoint.",
       "separate_mirror_parities":"s<->-s with A->-A, t<->-t with B->-B; rank-four messenger flavor sector",
       "scope":"Exact representation identities and one-loop quartic coefficients, with illustrative positive-tachyon-free messenger spectra. Not a solved E6 F/D-flat Higgs vacuum, naturalness, anomaly-free full R symmetry, proton decay safety, or globally preferred vacuum.",
       "source_E6_branching":"https://link.aps.org/accepted/10.1103/PhysRevD.96.015026"}
    return result
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["loop_scan"]["candidates_analyzed"],
       z["loop_scan"]["positive_count"],z["loop_scan"]["negative_count"])
    print("best positive",{k:z["loop_scan"]["best_positive"][k] for k in ("vpsi","vchi","Delta","kappa_SU5_TrPhi4")})
