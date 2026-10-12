#!/usr/bin/env python3
"""Soft-supertrace essential hierarchy at the radiative Witting vacuum.

Study the dimensionless mixed spectral selector
    V_r = F + r G,
    F = sum e^2 log e,  G = sum e log e,
on the normalized Vinberg Cartan.  F is the bosonic Coleman-Weinberg
shape of Pass 11884; G is the soft-mass shape isolated in Pass 11892.

The result is intentionally an effective-potential statement.  The UV theory
does not yet predict the relative coefficient r.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261011_soft_supertrace_hierarchy.json"
sys.path.insert(0,str(ROOT/"analysis"))

import w33_pass11890_11892_vacuum_phase_diagram as V
import w33_pass11884_11886_one_loop_trinification as CW
import w33_pass11923_stabiliser_higgs_lock as H23
import w33_pass11924_residual_s3_and_misaligned_flavon as H24
import w33_pass11925_w33_on_the_flavour_qutrit as H25

def sha(rel):
    return hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()

def FG(c):
    c=np.asarray(c,complex)
    e=V.spec(c)
    return CW.F_of(e),V.G_of(e),e

C0=np.array([1,0,0,0],complex)
F0,G0,_=FG(C0)

def along(t,u):
    return FG(np.r_[1+0j,t*np.asarray(u,complex)])

def local_coefficients(u,t):
    f,g,e=along(t,u)
    slopes=e[:24]/t**2
    sum_a=float(np.sum(slopes))
    kappa=float(2*(f-F0)/t**2)
    Cg=float((g-G0-sum_a*t*t*np.log(t*t))/t**2)
    return kappa,Cg,slopes

def radial_minimum(r,u,kappa,Cg):
    # Leading asymptotic stationary point:
    # log t = -kappa/(4 A r) - 1/2 - Cg/(2 A), A=sum a_i=8.
    pred=-kappa/(32*r)-0.5-Cg/16
    lo=max(np.log(2e-5),pred-3)
    hi=min(np.log(0.4),pred+3)
    def dv(y):
        t=np.exp(y);f,g,_=along(t,u)
        return (f-F0)+r*(g-G0)
    z=minimize_scalar(dv,bounds=(lo,hi),method="bounded",
                      options=dict(xatol=2e-10))
    return dict(r=float(r),t=float(np.exp(z.x)),log_t=float(z.x),
                predicted_log_t=float(pred),log_error=float(z.x-pred),
                deltaV=float(z.fun))
def endpoints_and_witness(t=2e-4):
    stab=np.array(H23.STAB[0],complex)
    strange=np.array([0,1,-1],complex)/np.sqrt(2)
    z9=np.exp(2j*np.pi/9)
    tstate=np.array([1,z9,np.conj(z9)],complex)/np.sqrt(3)
    # Deterministic explicit intermediate-magic witness found in the angular
    # search.  It is a witness only; no global CP2 minimum is claimed.
    mid=np.array([0.02336648-0.63503864j,
                  -0.50266647+0.37383305j,
                  -0.39282280-0.22236331j],complex)
    mid/=np.linalg.norm(mid)
    states={"stabiliser":stab,"strange":strange,"T_state":tstate,
            "intermediate_witness":mid}
    out={}
    for name,u in states.items():
        k,cg,sl=local_coefficients(u,t)
        out[name]=dict(C_G=cg,sum_zero_slopes=float(np.sum(sl)),
                       opened_zero_modes=int(np.sum(sl>1e-4)),
                       magic_M2=float(H23.magic(u)),
                       pauli_max=float(H23.pauli_max(u)))
    g=np.array([1,.1,.1],complex)
    els,cov=H24.elements(g)
    sg=H24.stabgroup(els,mid)
    sv=np.linalg.svd(H23.Y(mid,g),compute_uv=False)
    out["intermediate_witness"].update(
        residual_Delta54_projective_order=len(sg),
        up_singular_values_normalised=[float(x/sv[0]) for x in sv],
        up_gap=float(H23.gap(H23.Y(mid,g))),
        covariance_control=float(cov),
        max_fidelity_to_stabiliser=float(max(abs(np.vdot(mid,s))**2 for s in H23.STAB)))
    return out

def payload():
    stab=np.array(H23.STAB[0],complex)
    ts=[2e-4,3e-4,5e-4,8e-4]
    loc=[]
    for t in ts:
        k,c,sl=local_coefficients(stab,t)
        loc.append(dict(t=t,kappa_F=k,C_G=c,
                        slope_sum=float(np.sum(sl)),
                        remain_zero=int(np.sum(abs(sl)<1e-3)),
                        slope_one_third=int(np.sum(abs(sl-1/3)<1e-3)),
                        slope_one=int(np.sum(abs(sl-1)<1e-3))))
    kappa=float(np.median([x["kappa_F"] for x in loc]))
    Cg=float(np.median([x["C_G"] for x in loc]))
    A=float(np.median([x["slope_sum"] for x in loc]))
    radial=[radial_minimum(r,stab,kappa,Cg) for r in (.035,.04,.05,.06)]
    ep=endpoints_and_witness()
    result={
      "schema":"w33.20261011.soft-supertrace-hierarchy.v1",
      "potential":"V_r = F + r G, F=sum e^2 log e, G=sum e log e",
      "Witting_values":{"F":F0,"G":G0},
      "local_stabiliser_tangent":loc,
      "asymptotic":{
        "A_zero_mode_sum":A,
        "kappa_F":kappa,
        "C_G":Cg,
        "DeltaF":"(kappa_F/2) t^2 + 4 t^4 log(t^2) + O(t^4)",
        "DeltaG":"8 t^2 log(t^2) + 4 t^2 + o(t^2)",
        "stationary_but_not_minimum_for_r_positive":True,
        "reason":"t^2 log(t^2) has zero first derivative at t=0 but dominates every finite positive t^2 curvature negatively for r>0.",
        "essential_scaling":"log t_* = -kappa_F/(32 r) - 1/2 - C_G/16 + o(1)",
        "leading_exponent":-kappa/32,
        "cusp_weld":"Pass11891 gives epsilon proportional to projective displacement delta. With delta~t_*, this effective branch gives epsilon proportional to exp[-kappa_F/(32 r)] up to a non-universal prefactor."
      },
      "radial_checks":radial,
      "angular_witnesses":ep,
      "interpretation":{
        "firewall_consistency":"The G32-invariant loop potential does not exert a linear force at the Witting ray. The ray remains stationary. The escape is a nonanalytic bifurcation through the logarithmic opening of massless gauge modes.",
        "flavour_bridge":"The explicit lower-C_G witness has intermediate qutrit magic, trivial projective Delta54 residual symmetry, and a nondegenerate up Yukawa. It lies between the stabiliser and Strange endpoints of Pass11925.",
        "scope":"The relative coefficient r is supplied, not derived. This is not a UV prediction of quark masses, a complete 1PI potential, or a proof of the global minimum for every r. Gauge/Goldstone/ghost and renormalisation bookkeeping remain required for a physical off-shell effective potential."
      },
      "sources":{p:sha(p) for p in [
        "analysis/w33_pass11884_11886_one_loop_trinification.py",
        "analysis/w33_pass11890_11892_vacuum_phase_diagram.py",
        "analysis/w33_20261011_witting_displacement_firewall.py",
        "analysis/w33_pass11923_stabiliser_higgs_lock.py",
        "analysis/w33_pass11924_residual_s3_and_misaligned_flavon.py",
        "analysis/w33_pass11925_w33_on_the_flavour_qutrit.py"]},
    }
    # Fail-closed checks.
    result["checks"]={
      "zero_mode_pattern_4_18_2":all(x["remain_zero"]==4 and x["slope_one_third"]==18 and x["slope_one"]==2 for x in loc),
      "zero_mode_sum_is_8":max(abs(x["slope_sum"]-8) for x in loc)<2e-4,
      "F_curvature_converges":max(x["kappa_F"] for x in loc)-min(x["kappa_F"] for x in loc)<1e-4 and 7.20<kappa<7.22,
      "G_finite_coefficient_converges_to_4":max(abs(x["C_G"]-4) for x in loc)<1e-4,
      "essential_scaling_directly_resolved":max(abs(x["log_error"]) for x in radial[:3])<5e-3 and all(x["deltaV"]<0 for x in radial),
      "intermediate_beats_three_endpoint_directions":ep["intermediate_witness"]["C_G"]<ep["T_state"]["C_G"]<ep["stabiliser"]["C_G"]<ep["strange"]["C_G"],
      "intermediate_magic_is_strict":0<ep["intermediate_witness"]["magic_M2"]<np.log(2),
      "intermediate_breaks_residual_symmetry":ep["intermediate_witness"]["residual_Delta54_projective_order"]==1,
      "intermediate_unlocks_up_pair":ep["intermediate_witness"]["up_gap"]>0.05,
    }
    result["all_checks_pass"]=all(result["checks"].values())
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true")
    a=ap.parse_args()
    p=payload()
    txt=json.dumps(p,indent=2,sort_keys=True,default=lambda o:o.item() if isinstance(o,np.generic) else str(o))+"\n"
    if a.check:
        if not OUT.exists() or OUT.read_text()!=txt:
            raise SystemExit("certificate drift")
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(txt)
    print(json.dumps({"all_checks_pass":p["all_checks_pass"],
                      "leading_exponent":p["asymptotic"]["leading_exponent"],
                      "radial_checks":p["radial_checks"],
                      "angular_CG":{k:v["C_G"] for k,v in p["angular_witnesses"].items()}},indent=2))
    return 0 if p["all_checks_pass"] else 1
if __name__=="__main__":
    raise SystemExit(main())
