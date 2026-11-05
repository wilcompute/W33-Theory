#!/usr/bin/env python3
"""Physics-front 1: gauge-only two-loop threshold consistency + top Yukawa guard.

Jones/Machacek-Vaughn two-loop gauge coefficients including extra Dirac
vectorlike (3,2)1/6 or Majorana real SU2 adjoint at a common sharp mass.
Top Yukawa evolves at one loop; bottom/tau/BSM Yukawas and finite matching
omitted. A proton-decay dimension-6 normalization is displayed explicitly
as a free model-dependent parameter: it is NOT a universal exclusion.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_two_loop_threshold_proton_guard.json"
MZ=91.1876
B=np.array([4.1,-19/6,-7.],float)
BM=np.array([[199/50,27/10,44/5],[9/10,35/6,12],[11/10,9/2,-26]],float)
D=np.array([17/10,3/2,2],float)
AP=np.array([.6*(1-.23122)*127.955,.23122*127.955,1/.118],float)
YTOP=.936
SPECTRA={
  "Dirac_vectorlike_quark_doublet_3_2_1_6":{
     "kappa":1.,"dynkin":np.array([.1,1.5,1.]),"casimir":np.array([1/60,3/4,4/3])},
  "Majorana_weak_adjoint_1_3_0":{
     "kappa":.5,"dynkin":np.array([0.,2.,0.]),"casimir":np.array([0.,2.,0.])}}
def coefficients(s):
    k=s["kappa"];S=s["dynkin"];C=s["casimir"];CG=np.array([0.,2.,3.])
    b=(4/3)*k*S
    cross=4*k*np.outer(S,C)
    for i in range(3):cross[i,i]+=20/3*k*S[i]*CG[i]
    return b,cross

def rhs(s,bd,bmd):
    a=s[:3];y=s[3];g2=4*math.pi/a
    assert min(a)>0
    da=-(bd/(2*math.pi))-(bmd@g2-D*y*y)/(32*math.pi**3)
    dy=y/(16*math.pi**2)*(4.5*y*y-
               (17/20*g2[0]+9/4*g2[1]+8*g2[2]))
    return np.r_[da,dy]
def integrate(u,v,name,full=True):
    spec=SPECTRA[name]
    db,dB=coefficients(spec)
    y0=np.r_[AP,YTOP]
    if full:
        k1=solve_ivp(lambda t,y:rhs(y,B,BM),(0,u),y0,
                     rtol=3e-9,atol=3e-10)
        assert k1.success
        k2=solve_ivp(lambda t,y:rhs(y,B+db,BM+dB),
                     (u,u+v),k1.y[:,-1],rtol=3e-9,atol=3e-10)
    else:
        def one(y,b):return np.r_[-b/(2*math.pi),0.]
        k1=solve_ivp(lambda t,y:one(y,B),(0,u),y0)
        k2=solve_ivp(lambda t,y:one(y,B+db),(u,u+v),k1.y[:,-1])
    assert k2.success
    return k2.y[:,-1]
def solve_for(name,full=True):
    spec=SPECTRA[name]
    db,_=coefficients(spec)
    A=np.array([[B[0]-B[1],db[0]-db[1]],
                 [B[1]-B[2],db[1]-db[2]]])
    t,v=np.linalg.solve(A,2*math.pi*np.array([AP[0]-AP[1],AP[1]-AP[2]]))
    u=t-v
    initial=np.array([u,v])
    def residual(z):
        y=integrate(z[0],z[1],name,full)
        return [y[0]-y[1],y[1]-y[2]]
    solution=root(residual,initial,tol=1e-9)
    assert solution.success,solution.message
    u,v=solution.x
    assert 0<u and 0<v and u+v<math.log(1e19/MZ)
    y=integrate(u,v,name,full)
    assert max(abs(y[:3]-y[0]))<1e-8
    alpha_unif=1/float(np.mean(y[:3]))
    Mnew=MZ*math.exp(u);MGUT=MZ*math.exp(u+v)
    # Dim-6 kinematic scaling: tau = K * (MV/1e16)^4 *
    # (alpha0/alphaG)^2, where K is a FREE reference normalization.
    # Taking MV=MGUT is another free assumption (xi=1).
    ratio=(MGUT/1e16)**4*(.025/alpha_unif)**2
    minimum_K_years=2.4e34/ratio
    return {"threshold_mass_GeV":Mnew,"unification_scale_GeV":MGUT,
        "unified_inverse_alpha":1/alpha_unif,"yt_at_GUT":float(y[3]),
        "max_two_coupling_mismatch":float(max(abs(y[:3]-y[0]))),
        "proton_partial_lifetime_scaling_for_MV_equals_MGUT":ratio,
        "minimum_reference_K_years_for_p_to_e_pi0_limit":minimum_K_years,
        "example_tau_years_if_K_equals_1e35_years":1e35*ratio,
        "proton_decay_assumptions":"tau=K*(MV/10^16GeV)^4*(.025/alphaG)^2; here MV=MGUT, K unspecified. Experimental bound 2.4e34 yr 90%CL for e+pi0. No branching ratio, Wilson mixing or matrix elements computed."}
def main():
    rows={}
    for name,s in SPECTRA.items():
        db,dB=coefficients(s)
        if "quark" in name:
            assert max(abs(db-np.array([2/15,2,4/3])))<1e-14
            assert abs(dB[2,2]-76/3)<1e-13
            assert abs(dB[0,1]-3/10)<1e-14
        else:
            assert max(abs(db-np.array([0,4/3,0])))<1e-14
            assert abs(dB[1,1]-64/3)<1e-14
        one=solve_for(name,False)
        two=solve_for(name,True)
        assert abs(two["threshold_mass_GeV"]/one["threshold_mass_GeV"]-1)>.03
        assert two["threshold_mass_GeV"]>1000
        rows[name]={"one_loop_recomputed":one,"two_loop_gauge_with_top_yukawa_one_loop":two,
                    "extra_b":db.tolist(),"extra_B":dB.tolist()}
    # Independently scan no-threshold minimal SM two-loop at 3 reference
    # energies, showing its couplings do not simply triple meet.
    no_new=[]
    for power in (10,13,16):
        t=math.log(10**power/MZ)
        v=solve_ivp(lambda z,y:rhs(y,B,BM),(0,t),np.r_[AP,YTOP],
                    rtol=3e-9,atol=3e-10).y[:3,-1]
        no_new.append({"energy_GeV":10**power,"inverse_couplings":v.tolist(),
            "max_spread":float(max(v)-min(v))})
    assert all(k["max_spread"]>3 for k in no_new)
    out={"status":"PASS_TWOLOOP_GAUGE_TOP_YUKAWA_THRESHOLD_AND_CONDITIONAL_PROTON",
       "SM_b":B.tolist(),"SM_B":BM.tolist(),"SM_top_yukawa_gauge_d":D.tolist(),
       "MZ_inputs_inverse_alpha":AP.tolist(),"Y_top_MZ_assumption":YTOP,
       "reference_proton_limit_p_eplus_pi0_90pct_yr":2.4e34,
       "source_proton_decay":"Super-Kamiokande Phys Rev D102 112011 (2020), tested specific mode not all channels",
       "source_SM_two_loop":"Phys Rev D90 075006 app B",
       "source_extra_two_loop":"Jones Phys Rev D25 581 (1982), gauge group formula and Dirac/Weyl kappa convention",
       "scans":rows,"SM_no_new_particles_control":no_new,
       "scope":"Gauge couplings two-loop, yt one-loop. Neglect other Yukawas, BSM Yukawas, heavy matching, threshold uncertainty, 3-loop, Planck operators; not a consistent full grand unified UV theory. Proton scaling depends on free K and MV/MGUT."}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    for k,z in rows.items():
        print("TWO_LOOP",k, z["two_loop_gauge_with_top_yukawa_one_loop"],flush=True)
    print("CERTIFICATE",OUT,flush=True)
    return out
if __name__=="__main__":main()
