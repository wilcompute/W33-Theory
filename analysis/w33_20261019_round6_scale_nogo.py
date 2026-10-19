"""Round6 front5: mathematically exact scale-covariance firewall.
Finite dimensionless W33/Clifford incidence alone does not calibrate
an absolute energy, time, speed, Newton constant or Planck constant.
Explicit numerical Gibbs/fermion/unitary invariance and null candidate
parameter-free optical ratios (ordinary quantum mechanics).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from w33_20261019_tick_operator_frame_majorization import points,build_projectors
from w33_20261019_round4_fermions_global import specC,specN
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round6_scale_nogo.json"
rng=np.random.default_rng(20261019)
P=build_projectors(points());I=np.eye(9)
def Gibbs(H,T):
    x=-np.linalg.eigvalsh(H)/T
    q=x.max()
    return float(-T*(q+np.log(np.exp(x-q).sum())))
def Ferm(H,T,mu):
    e=np.linalg.eigvalsh(H)
    return float(-T*np.logaddexp(0,(mu-e)/T).sum())
def C(w):
    from w33_20261019_tick_operator_frame_majorization import symp
    pts=points()
    s=w.reshape(40,3).sum(axis=1)
    return float((2/3)*sum(s[i]*s[j] for i in range(40) for j in range(40) if i!=j and symp(pts[i],pts[j])!=0))
def run():
    w=rng.dirichlet(np.ones(120))
    Q=np.tensordot(w,P,axes=1)
    H=I-Q
    T=.37;kappa=-.22
    F=Gibbs(H,T)+kappa*C(w)
    Omega=Ferm(I-(P[0]+P[3])/2,T,.5)
    t=.73
    errors=[]
    for s in (.001,.25,1.,2.,10.,100.):
        F2=Gibbs(s*H,s*T)+s*kappa*C(w)
        O2=Ferm(s*(I-(P[0]+P[3])/2),s*T,s*.5)
        U=expm(-1j*H*t);V=expm(-1j*(s*H)*(t/s))
        errors.append({"scale":s,"Gibbs_dimensionless_action_residual":abs(F2/s-F),
            "Fermion_Omega_residual":abs(O2/s-Omega),
            "unitary_time_scaling_residual":float(np.linalg.norm(U-V)),
            "dimensionless_kappa_over_T":kappa/T})
    # Dimensionless geometric C max 4/7, count 40 and 120 set no
    # conversion factor to joules, seconds, metric curvature.
    # Generic master parameter transformation:
    # E->sE, T->sT, kappa->s*kappa, t->t/s
    # leaves normalized Gibbs weights, quantum propagators and all
    # binary projective incidence observables unchanged.
    checks={
      "Gibbs_interaction_energy_scale_covariant":max(x["Gibbs_dimensionless_action_residual"] for x in errors)<1e-11,
      "fermion_thermodynamic_scale_covariant":max(x["Fermion_Omega_residual"] for x in errors)<1e-11,
      "Schrodinger_dynamics_energy_time_scale_covariant":max(x["unitary_time_scaling_residual"] for x in errors)<1e-10,
      "kappa_T_ratio_invariant":all(abs(x["dimensionless_kappa_over_T"]-kappa/T)<1e-13 for x in errors)
    }
    out={"schema":"w33.round6.absolute_scale_nogo.v1",
      "statement":"For the currently specified finite W33 model, H->sH, T->sT, kappa->s*kappa and t->t/s for s>0 leave all dimensionless Gibbs distributions, projector incidence and quantum propagators invariant. Therefore this model ALONE cannot determine an energy or time scale, c, G, hbar, or any dimensional particle mass.",
      "proof":"Exp[-(sH)/(sT)]=exp[-H/T]. F_{sT}(sH)=sF_T(H). Fermionic Omega_{sT,s_mu}(sH)=s Omega_{T,mu}(H). U_{sH}(t/s)=U_H(t). The dimensionless ratio kappa/T remains fixed, but numerical conversion to SI units is undetermined.",
      "scope":"This is a no-absolute-scale statement for the CURRENT finite dimensionless Hamiltonian; theories with additional dimensionful dynamics, reference clock, renormalization-scale anomaly or boundary conditions can in principle establish a physical scale. It is NOT a universal theorem ruling out emergent dimensional constants.",
      "candidate_W33_signal":"The ideal commutator echo contrast 8/27 and the 240:540 commuting census are parameter-free, but are exactly predicted by textbook two-qutrit quantum mechanics, so do not distinguish a TOE.",
      "physical_next_requirement":"Provide independently normalized field action, operational units, light-cone/metric coupling, source and target observable; freeze coefficients before comparing against measured mass or optical data.",
      "rescaling_factors":errors,
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"maxerr":max(x["unitary_time_scaling_residual"] for x in errors)},indent=2))
    assert out["all_checks_pass"]
if __name__=="__main__":run()
