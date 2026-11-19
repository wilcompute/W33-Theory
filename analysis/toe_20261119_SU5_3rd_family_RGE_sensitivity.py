"""Two-loop MSSM gauge beta with one-loop third-family Yukawas, sensitivity test.

Not a 2-loop Yukawa system, threshold fit or realistic G2 proton prediction.
"""
from pathlib import Path
from math import log,pi
import json
import numpy as np
from scipy.integrate import solve_ivp
from toe_20261119_SU5_brane_projector_two_loop_RGE import beta_for_vectorlike_pair,solve_RGE
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_SU5_yukawa_two_loop_sensitivity.json"
bM=np.array([33/5,1,-3],float)
BM=np.array([[199/25,27/5,88/5],[9/5,25,24],[11/5,9,14]],float)
Yc=np.array([[26/5,14/5,18/5],[6,6,2],[4,4,0]],float)
T, BT=beta_for_vectorlike_pair("triplet")
T=np.asarray(T,float).reshape(3)
BT=np.asarray(BT,float)

def low_scale_inverse_alpha():
    mZ=91.1876;alphaEM=1/127.95;sin2=.23122
    a=np.array([1/((5/3)*alphaEM/(1-sin2)),1/(alphaEM/sin2),1/.1181])
    return a-np.array([41/10,-19/6,-7])/(2*pi)*log(1000/mZ)

def step(y,mu_low,mu_high,addtriplet=False):
    b=bM+(T if addtriplet else 0)
    B=BM+(BT if addtriplet else 0)
    def rhs(t,x):
        inv=x[:3];yt,yb,ytau=x[3:]
        a=1/inv;g2=4*pi*a
        dy=np.array([
          yt*(6*yt*yt+yb*yb-(13/15*g2[0]+3*g2[1]+16/3*g2[2])),
          yb*(yt*yt+6*yb*yb+ytau*ytau-(7/15*g2[0]+3*g2[1]+16/3*g2[2])),
          ytau*(3*yb*yb+4*ytau*ytau-(9/5*g2[0]+3*g2[1]))])/(16*pi*pi)
        db=-b/(2*pi)-(B@a-Yc@np.square(x[3:])/(4*pi))/(8*pi*pi)
        return np.r_[db,dy]
    sol=solve_ivp(rhs,(log(mu_low),log(mu_high)),y,method="DOP853",
                  rtol=2e-11,atol=2e-12)
    assert sol.success
    return sol.y[:,-1]

def run():
    cases=[]
    baseline=solve_RGE()["scenarios"]
    for triplet_mass in (None,1e14,1e16):
        for yu0 in ((0.,0.,0.),(.8,.1,.08),(.8,.5,.4)):
            y=np.r_[low_scale_inverse_alpha(),yu0]
            if triplet_mass is None:
                end=step(y,1000,2e16)
            else:
                end=step(y,1000,triplet_mass)
                end=step(end,triplet_mass,2e16,True)
            cases.append({"extra_triplet_threshold_GeV":triplet_mass,
                          "yt_yb_ytau_at_1TeV":list(yu0),
                          "alpha_inverse_at_2e16":end[:3].tolist(),
                          "Yukawa_at_2e16":end[3:].tolist(),
                          "mismatch_12_13_23":[float(end[0]-end[1]),float(end[0]-end[2]),float(end[1]-end[2])]})
    for index,base in ((0,baseline[0]),(3,baseline[1]),(6,baseline[2])):
        # no Yukawas must reproduce the independently integrated gauge-only system
        assert np.max(abs(np.array(cases[index]["alpha_inverse_at_2e16"])-base["alpha_inverse_at_MU"]))<5e-8
    out={"two_loop_MSSM_Yukawa_coefficients":Yc.tolist(),
         "one_loop_yt_yb_ytau_run":True,
         "completely_zero_Yukawa_reproduces_other_two_loop_gauge_only_integrator":True,
         "grid":cases,
         "third_family_Yukawa_input_status":"Illustrative y_t,y_b,y_tau values supplied by hand at 1TeV, NOT derived from observed running fermion masses, tan(beta), supersymmetric thresholds, G2 geometry or source overlap.",
         "limits":"2-loop gauge beta with 1-loop third-family Yukawas, not all 2-loop Yukawa beta, third-generation SUSY thresholds, full KK, proton matrix elements, complete G2 or unification prediction.",
         "reference":"https://www.sciencedirect.com/science/article/pii/S0370269301014344; standard MSSM 2-loop gauge Yukawa coefficients also listed at https://inspirehep.net/files/73fc41f9fd2eb27542b4b5807e72e758"}
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    for x in cases:print("SENSITIVITY",x["extra_triplet_threshold_GeV"],x["yt_yb_ytau_at_1TeV"],np.round(x["mismatch_12_13_23"],4))
    print("PASS 2-loop gauge + 1-loop Yukawa sensitivity; zero-Yukawa exactly matches independent baseline")
    print(OUT)
    return out
if __name__=="__main__":run()
