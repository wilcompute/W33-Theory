"""Front4: explicit 36-configuration, photon-count multinomial process
tomography for COMPLEX 9x9 transfer R and S, balanced Mach-Zehnder
with known nonzero full-complex reference F3 tensor F3.
This is an optical experiment SPECIFICATION and synthetic test,
not a built chip or independent experimental verification.
"""
from __future__ import annotations
import json
import numpy as np
from pathlib import Path
from scipy.linalg import expm
from w33_20261019_nextfive_optics_su9 import F,proj0,proj1,I9
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round9_photon_tomography_shots.json"
rng=np.random.default_rng(20261019)
Uref=np.kron(F,F)
def echo():
    A=I9+(1j-1)*proj0;B=I9+(1j-1)*proj1
    return A@B@A.conj().T@B.conj().T
def transfer(eps):
    H=np.zeros((9,9),complex)
    for j in range(6):
        H[j,j+3]=np.exp(.47j*(j+1))
        H[j+3,j]=H[j,j+3].conjugate()
    return expm(1j*eps*H)@np.diag(np.linspace(.68,.96,9))
def probabilities(T,j,phase):
    r=Uref[:,j];t=T[:,j]*np.exp(1j*phase)
    pp=np.abs(r+t)**2/4
    pm=np.abs(r-t)**2/4
    loss=max(0.,float(1-pp.sum()-pm.sum()))
    v=np.r_[pp,pm,loss]
    assert abs(v.sum()-1)<1e-10 and min(v)>=0
    return v
def analytic_contrasts(T):
    obs=np.empty((9,9,2))
    for j in range(9):
        for k in range(9):
            r=Uref[k,j];t=T[k,j]
            obs[k,j,0]=(r.conjugate()*t).real
            obs[k,j,1]=-(r.conjugate()*t).imag
    return obs
def invert_contrasts(observed):
    z=observed[:,:,0]-1j*observed[:,:,1]
    return z/Uref.conj()
def shot_tomography(T,n):
    obs=np.zeros((9,9,2))
    for j in range(9):
        for index,phase in enumerate((0.,np.pi/2)):
            counts=rng.multinomial(n,probabilities(T,j,phase))
            obs[:,j,index]=(counts[:9]-counts[9:18])/n
    return invert_contrasts(obs)
def run():
    W=echo()
    ideal=float(1-np.trace(W).real/9)
    M=transfer(.16)
    ana_R=invert_contrasts(analytic_contrasts(M))
    ana_S=invert_contrasts(analytic_contrasts(M@W))
    analytic_err=max(float(np.linalg.norm(ana_R-M)),float(np.linalg.norm(ana_S-M@W)))
    n=40000;trials=120
    deltas=[];reconstruction=[]
    for _ in range(trials):
        R=shot_tomography(M,n)
        S=shot_tomography(M@W,n)
        est=np.linalg.solve(R,S)
        deltas.append(float(1-np.trace(est).real/9))
        reconstruction.append(float(np.linalg.norm(est-W)))
    vals=np.array(deltas)
    # A photon detector must resolve 2 path signs times 9 internal
    # modes plus a no-click/erasure outcome, all in one setting.
    # Each phase-setting probes ALL 9 outputs simultaneously.
    drift=[]
    for e in (0.,.002,.01,.03):
        est=np.linalg.solve(M,transfer(.16+e)@W)
        drift.append({"additional_mixing_phase":e,
            "calibration_staleness_deficit_bias":float(1-np.trace(est).real/9-ideal)})
    checks={
      "reference_has_all_81_nonzero_entries":np.min(abs(Uref))>.33-.001,
      "complex_XY_quadrature_exact_reconstruction":analytic_err<1e-12,
      "multinomial_shot_delta_approximately_unbiased":abs(float(vals.mean())-ideal)<.008,
      "multinomial_shot_precision_within_two_percent":float(np.std(vals,ddof=1))<.02,
      "nonzero_calibration_drift_bias":abs(drift[-1]["calibration_staleness_deficit_bias"])>1e-4,
      "36_distinct_photon_shot_settings":2*9*2==36}
    out={"schema":"w33.round9.full_photon_count_trace_tomography.v1",
      "protocol":"Send a single photon into a balanced 2-path interferometer with initial internal |j>, j=0..8. The reference path applies Uref=F3 tensor F3 (all 81 elements have |r_kj|=1/3). The test path applies unknown lossy 9x9 T, either R=M or S=M W. For each j and path phase phi in {0,pi/2}, resolve 18 outputs (9 plus and 9 minus) and erasure. Measured path difference D_phi(k,j)=p_plus-p_minus=Re[exp(i phi) conj(r_kj) T_kj]. Thus T_kj=(D0-i Dpi/2)/conj(r_kj). After 36 settings, compute W=R^-1 S.",
      "reference_matrix":"F3 tensor F3 (two 3-mode Fourier meshes; phase elements known)",
      "input_states":list(range(9)),
      "path_quadratures_radians":[0.,float(np.pi/2)],
      "conditions":["Identity loop with M: R","Noncommuting W33 loop with M: S"],
      "detector_outcomes_per_configuration":19,
      "settings":36,
      "photons_per_setting":n,
      "photons_per_full_run":36*n,
      "independent_multinomial_MonteCarlo_runs":trials,
      "analytic_complex_transfer_error":analytic_err,
      "ideal_trace_deficit":ideal,
      "estimated_deficit_mean":float(vals.mean()),
      "estimated_deficit_standard_deviation":float(vals.std(ddof=1)),
      "estimated_deficit_RMSE":float(np.sqrt(np.mean((vals-ideal)**2))),
      "mean_W_transfer_Frobenius_error":float(np.mean(reconstruction)),
      "stale_reference_drift":drift,
      "resource_boundary":"1.44 million synthetic input photons per independent reference+signal calibration under this noise-free-except-shot-multinomial model. Actual chip source brightness, detector loss/afterpulsing, independent stage tomography, integrated component count, thermal phase stability and path reference phase lock not demonstrated. The photon-number accounting includes source photons even when erased.",
      "checks":{k:bool(v) for k,v in checks.items()},
      "all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"ideal":ideal,"mean":vals.mean(),"std":vals.std(ddof=1),"nphotons":36*n},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
