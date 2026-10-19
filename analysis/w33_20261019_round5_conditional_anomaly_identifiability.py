"""Front 5: quantify distinguishability of a *hypothetical* extra
commutator-generated unitary from unknown optical phase offset.
η is neither fixed nor derived by a TOE, so NO novel parameter-free
prediction is claimed.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from w33_20261019_nextfive_optics_su9 import proj0 as P,proj1 as Q,proj_null as R,I9 as I
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261019_round5_conditional_anomaly_identifiability.json"
K=1j*(P@Q-Q@P)
def U(A,t):return I+(np.exp(1j*t)-1)*A
def loop(A,B,t,s):
    X=U(A,t);Y=U(B,s)
    return X@Y@X.conj().T@Y.conj().T
def contrast(t,phase_offset,eta,control=False):
    B=R if control else Q
    W=loop(P,B,t,t+phase_offset)
    K0=1j*(P@B-B@P)
    W=expm(1j*eta*K0)@W
    return float(1-np.trace(W).real/9)
def run():
    angles=np.array([.35,.7,1.05,1.4,np.pi/2,1.9,2.25,2.7])
    h=1e-5
    model=np.array([contrast(t,0,0) for t in angles])
    exact=np.array([(32/27)*np.sin(t/2)**4 for t in angles])
    jac=np.array([[(contrast(t,h,0)-contrast(t,-h,0))/(2*h),
        (contrast(t,0,h)-contrast(t,0,-h))/(2*h)] for t in angles])
    sing=np.linalg.svd(jac,compute_uv=False)
    one=np.linalg.svd(jac[[4],:],compute_uv=False)
    # Standard two-outcome path interferometer: P(port0)=(2-delta)/2.
    # Measurement Fisher information per angle (one shot) for model params
    # eta and phase offset; this is LOCAL, conditional on hypothetical eta.
    # p=1-delta/2 and dp=-d(delta)/2.
    p=1-model/2
    weights=1/(4*p*(1-p))
    FI=jac.T@(weights[:,None]*jac)
    ev=np.linalg.eigvalsh(FI)
    sigma_eta_100000=float(np.sqrt(np.linalg.inv(FI)[1,1]/100000))
    # Calibration-only finite offset can masquerade as eta at one theta.
    at=int(np.argmin(abs(angles-np.pi/2)))
    mimic=float(.01*jac[at,1]/jac[at,0])
    # Paired null control is exactly insensitive to these hypothetical
    # commutator-dependent deformations and hence cannot identify eta.
    control_null=max(abs(contrast(t,.04,.05,True)) for t in angles)
    checks={
      "one_angle_cannot_identify_two_unknowns":len(one)==1,
      "multi_angle_local_identifiability":sing[-1]>0.01 and ev[0]>0,
      "ideal_QM_curve":np.max(abs(model-exact))<1e-12,
      "null_commuting_control_insensitive":control_null<1e-12,
      "fisher_positive_semidefinite":ev.min()>0
    }
    out={"schema":"w33.round5.conditional_commutator_anomaly.v1",
      "extra_hypothesis":"W_eta = exp(i eta K)*[U_P(theta) U_Q(theta+epsilon) U_P(-theta) U_Q(-theta-epsilon)], K=i[P,Q] Hermitian. eta supplied, not derived. Entire model STILL quantum mechanics with an extra gate; not TOE-exclusive.",
      "eta_and_epsilon_are":"two unknown parameters; epsilon is optical calibration offset, eta is hypothetical additional dynamics",
      "angles_rad":angles.tolist(),"delta_standard_QM":model.tolist(),
      "jacobian_columns":["phase_offset_epsilon","conditional_eta"],
      "jacobian":jac.tolist(),
      "one_angle_singular_values":one.tolist(),
      "multi_angle_singular_values":sing.tolist(),
      "fisher_per_one_shot_per_angle":FI.tolist(),
      "fisher_eigenvalues":ev.tolist(),
      "hypothetical_eta_precision_for_100000_independent_shots_each_angle":sigma_eta_100000,
      "single_angle_epsilon_to_mimic_eta_0_point_01":mimic,
      "max_null_control_amplitude":control_null,
      "conclusion":"Single angle cannot separate eta from miscalibrated phase. Multi-angle scan is locally identifiable for this SPECIFIED eta-shape; still needs externally fixed eta, real optical calibration, drift controls, and a theory that predicts eta without fitting.",
      "literature":"Standard 9-level QM and DQC1 single-photon trace measurement already imply baseline delta; experiment would test instrument + added Hamiltonian, not uniqueness of a TOE.",
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"svals":out["multi_angle_singular_values"],
       "conditional_eta_sigma_100k":sigma_eta_100000},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
