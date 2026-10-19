"""Front4: a 9x9 full complex transfer-matrix calibration for the
18-mode single-photon W33 trace witness with coherent mode mixing.
A diagonal per-mode reference is insufficient when cross-talk occurs.
Measurement of complex transfer matrices is ASSUMED (tomography),
not implemented by fabricated photonic equipment.
"""
from __future__ import annotations
import json,numpy as np
from pathlib import Path
from scipy.linalg import expm
from w33_20261019_nextfive_optics_su9 import proj0,proj1,proj_null,I9
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round8_optics_crosstalk_tomography.json"
rng=np.random.default_rng(20261019)
def phase(P,t):return I9+(np.exp(1j*t)-1)*P
def W(P,Q):
    A=phase(P,np.pi/2);B=phase(Q,np.pi/2)
    return A@B@A.conj().T@B.conj().T
def attenuator(eps):
    H=np.zeros((9,9),complex)
    # Couple adjacent first-qutrit rails (j and j+3), holding the
    # second-qutrit mode fixed: this overlaps actual W off-diagonals.
    for j in range(6):
        H[j,j+3]=np.exp(1j*(j+1)*.47)
        H[j+3,j]=np.conj(H[j,j+3])
    U=expm(1j*eps*H)
    ell=np.linspace(.68,.96,9)
    return U@np.diag(ell)
def reconstructed(R,S):
    return np.linalg.solve(R,S)
def run():
    sig=W(proj0,proj1);null=W(proj0,proj_null)
    target=1-np.trace(sig).real/9
    model=[]
    for eps in (0,.03,.09,.16,.3):
        M=attenuator(eps)
        ref=M;signal=M@sig;ctrl=M@null
        # An interferometer with reference arm I yields path X_j =
        # Re <j|M W|j> at balanced path couplers.
        d0=np.diag(ref).real
        raw=np.diag(signal).real
        dnull=np.diag(ctrl).real
        naive=float(1-np.mean(raw/d0))
        null_naive=float(1-np.mean(dnull/d0))
        Wrec=reconstructed(ref,signal)
        nulrec=reconstructed(ref,ctrl)
        full=float(1-np.trace(Wrec).real/9)
        nulfull=float(1-np.trace(nulrec).real/9)
        model.append({"coherent_mixing_eps_rad":eps,
          "diagonal_reference_only_deficit":naive,
          "diagonal_reference_only_bias":naive-target,
          "diagonal_reference_only_null_deficit":null_naive,
          "full_complex_reference_transfer_inversion_deficit":full,
          "full_tomographic_null_deficit":nulfull,
          "full_matrix_reconstruction_error":float(np.linalg.norm(Wrec-sig)),
          "calibration_condition_number":float(np.linalg.cond(ref))})
    errors=[]
    M=attenuator(.16)
    R=M;S=M@sig
    for sigma in (0,.0005,.002,.005):
        gap=[];materr=[]
        for _ in range(300):
            err=lambda:(rng.normal(size=(9,9))+1j*rng.normal(size=(9,9)))*(sigma/np.sqrt(2))
            A=R+err(); B=S+err()
            w=reconstructed(A,B)
            gap.append(float(1-np.trace(w).real/9-target))
            materr.append(float(np.linalg.norm(w-sig)))
        errors.append({"complex_transfer_entry_noise_sigma":sigma,
            "simulated_trials":300,"trace_deficit_bias_mean":float(np.mean(gap)),
            "trace_deficit_RMSE":float(np.sqrt(np.mean(np.square(gap)))),
            "full_transfer_Frobenius_error_mean":float(np.mean(materr))})
    # coherent gain drift changes actual R versus S and cannot be
    # removed by inverting an earlier stale reference.
    stale=[]
    for delta in (.0,.005,.02):
        M0=attenuator(.16);M1=attenuator(.16+delta)
        wrong=reconstructed(M0,M1@sig)
        stale.append({"drift_eps_rad":delta,"uncalibrated_trace_bias":
            float(1-np.trace(wrong).real/9-target)})
    checks={
      "diagonal_calibration_unbiased_only_zero_mixing":abs(model[0]["diagonal_reference_only_bias"])<1e-12,
      "crosstalk_defeats_diagonal_calibration":max(abs(x["diagonal_reference_only_bias"]) for x in model)>.003,
      "full_transfer_inversion_recovers_W":max(x["full_matrix_reconstruction_error"] for x in model)<1e-12,
      "full_transfer_inversion_recovers_null":max(abs(x["full_tomographic_null_deficit"]) for x in model)<1e-12,
      "small_tomography_noise_beats_naive_crosstalk_bias":errors[2]["trace_deficit_RMSE"]<.01,
      "stale_reference_not_invariant_under_drift":abs(stale[-1]["uncalibrated_trace_bias"])>1e-4}
    out={"schema":"w33.round8.coherent_crosstalk_transfer_tomography.v1",
      "model":"Single 18-mode photon paths: reference arm identity, signal path implements M W; M=U_mix diag(ell), ell_j=.68..96 and U_mix=e^(i epsilon H_chain) coherently mixes neighbouring 9 internal modes AFTER W. Both signal and identity-calibration modes have same stationary M.",
      "why_diagonal_ratio_fails":"Measured balanced path port contrast for input j is Re[(M W)_jj]; reference is Re[M_jj]. Their ratio is not generally Re[W_jj] if M is non-diagonal.",
      "full_transfer_protocol":"Perform independent complex linear-optical transfer tomography of 9x9 R=M (identity reference) and S=M W (signal) using coherent input/output superpositions, two reference phases X/Y and output mode resolution; compute W_est=R^-1 S. This assumes the phase reference and mode-gauge alignment are controlled. No laboratory implementation or optimal shot count is asserted.",
      "ideal_W33_trace_deficit":float(target),
      "mode_mixing_series":model,
      "complex_transfer_gaussian_noise_simulation":errors,
      "stale_calibration_drift_examples":stale,
      "experimental_boundary":"Full complex transfer reconstruction requires MORE measurements than 9 diagonal contrasts. Phase reference drift, loss inside W, detector dark counts, time-dependent M and nonunitary postselection require extra controls. Gaussian matrix-entry noise is synthetic, NOT a calibrated photon-shot-noise model.",
      "checks":{k:bool(v) for k,v in checks.items()},
      "all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"biases":[round(x["diagonal_reference_only_bias"],6) for x in model],"drift":stale},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
