"""Front3: mode-resolved loss calibration for explicit single-photon
18-mode W33 echo, with 3-outcome photon/loss shot statistics and
hardware phase/mixer settings.

No experiment was built. No correlated phase noise or manufacturing
tolerance proof is implied.
"""
from __future__ import annotations
import json
import numpy as np
from pathlib import Path
from w33_20261019_nextfive_optics_su9 import proj0,proj1,proj_null,F,I9,G
from w33_20261019_round6_optics_component_budget import givens
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round7_optical_mode_loss.json"
I=np.eye(9,dtype=complex)
T=np.pi/2
rng=np.random.default_rng(20261019)
def U(P,t):return I+(np.exp(1j*t)-1)*P
def W(P,Q,t=T):
    A=U(P,t);B=U(Q,t)
    return A@B@A.conj().T@B.conj().T
def shots(V,j,n):
    ej=np.eye(9,dtype=complex)[:,j]
    p0=np.vdot(ej+V@ej,ej+V@ej).real/4
    p1=np.vdot(ej-V@ej,ej-V@ej).real/4
    p2=1-p0-p1
    assert min(p0,p1,p2)>-1e-12
    return np.array([p0,p1,p2])
def run():
    sig=W(proj0,proj1);nul=W(proj0,proj_null)
    ell=np.linspace(.68,.96,9) # intensity? AMPLITUDE; below explicitly
    # ell is signal ARM AMPLITUDE transmission; intensity=ell^2
    L=np.diag(ell)
    # Reference measurement W=I gives exactly ell_j path difference,
    # even when losses are mode-resolved and nonuniform.
    raw=np.array([shots(L@sig,j,1)[:2].dot([1,-1]) for j in range(9)])
    ref=np.array([shots(L,j,1)[:2].dot([1,-1]) for j in range(9)])
    control=np.array([shots(L@nul,j,1)[:2].dot([1,-1]) for j in range(9)])
    ideal=1-np.trace(sig).real/9
    calibrated=1-np.mean(raw/ref)
    global_ref=1-raw.mean()/ref.mean()
    calibrated_null=1-np.mean(control/ref)
    n=3500
    reps=800
    vals_sig=[];vals_null=[]
    for _ in range(reps):
        reference=np.array([rng.multinomial(n,shots(L,j,n)) for j in range(9)])
        sample=np.array([rng.multinomial(n,shots(L@sig,j,n)) for j in range(9)])
        sham=np.array([rng.multinomial(n,shots(L@nul,j,n)) for j in range(9)])
        denom=(reference[:,0]-reference[:,1])/n
        # These losses large enough that the reference has positive contrast
        assert min(denom)>.2
        S=(sample[:,0]-sample[:,1])/n
        B=(sham[:,0]-sham[:,1])/n
        vals_sig.append(float(1-np.mean(S/denom)))
        vals_null.append(float(1-np.mean(B/denom)))
    vals_sig=np.array(vals_sig);vals_null=np.array(vals_null)
    _,_,steps,_=givens(F)
    couplers=[]
    for a,b,M in steps:
        block=M[np.ix_([a,b],[a,b])]
        couplers.append({"modes_of_F3":[a,b],
          "amplitudes_2_by_2":[[{"re":float(z.real),"im":float(z.imag)} for z in line] for line in block]})
    checks={
      "per_mode_amplitude_reference_calibration_exact":max(abs(ref-ell))<1e-12,
      "loss_calibrated_noncommuting_deficit_exact":abs(calibrated-ideal)<1e-12,
      "loss_calibrated_commuting_null_exact":abs(calibrated_null)<1e-12,
      "nonuniform_mode_loss_global_visibility_calibration_biased":abs(global_ref-ideal)>1e-5,
      "ideal_noncommuting_eight_over_27":abs(ideal-8/27)<1e-12,
      "800_trinary_shot_experiments_detect_witness":np.mean(vals_sig>ideal/2)>.98,
      "800_trinary_shot_experiments_no_null_false_alarm":np.mean(vals_null>ideal/2)<.02,
      "3_structured_F3_coupler_settings":len(couplers)==3}
    out={"schema":"w33.round7.18mode_mode_resolved_loss_calibration.v1",
      "experimental_status":"IDEAL circuit and synthetic photon/loss Monte Carlo, no real optical chip, single-photon source or detector data.",
      "path_register":"two coherent paths, each 9 internal spatial modes. W33 echo one-arm nontrivial operation.",
      "frequency_bin_phase_logic":"For W at theta=pi/2 use four P phases on three modes with signs +,+,-,- interleaved with G=CZ(F3 x I3),Gdag; two global 50/50 path couplers. Mesh settings below implement F3 via 3 complex two-mode couplers repeated across other qutrit index b=0,1,2.",
      "F3_complex_Givens_two_mode_settings":couplers,
      "CZ_phase_mask_modes":"Four |a,b> with a,b in {1,2} receive omega^(a*b), all other 5 zero",
      "projector_mask":"Local |a=0,b> for b=0,1,2; theta=+/-pi/2",
      "loss_model":"Signal arm output-mode amplitude transmission ell_j (intensity ell_j²) following W, reference arm lossless, identical stationary ell_j for calibration, signal and commuting null; loss channel includes an erasure outcome.",
      "amplitude_transmission_9_modes":ell.tolist(),
      "ideal_deficit":float(ideal),
      "raw_signal_mode_differences":raw.tolist(),
      "reference_mode_differences":ref.tolist(),
      "mode_by_mode_corrected_deficit":float(calibrated),
      "commuting_control_corrected_deficit":float(calibrated_null),
      "incorrect_global_reference_corrected_deficit":float(global_ref),
      "global_calibration_bias":float(global_ref-ideal),
      "shot_statistics":{"photons_per_input_per_condition":n,
         "conditions":["W=identity calibration","W=noncommuting","W=commuting null"],
         "total_photons_per_repetition":3*9*n,
         "Monte_Carlo_repetitions":reps,
         "detected_signal_fraction":float(np.mean(vals_sig>ideal/2)),
         "false_positive_null_fraction":float(np.mean(vals_null>ideal/2)),
         "signal_mean":float(np.mean(vals_sig)),
         "signal_std":float(np.std(vals_sig,ddof=1)),
         "null_mean":float(np.mean(vals_null)),
         "null_std":float(np.std(vals_null,ddof=1))},
      "boundary":"Calibration assumes loss applied AFTER the ideal W and loss diagonal in chosen output modes. Coherent mode mixing, phase drift, detector dark counts, shot correlations and mode-dependent loss inside W are not corrected by this simple ratio. Must measure transfer matrix and source/crosstalk independently.",
      "literature":"2026 local variance-based calibration https://arxiv.org/abs/2607.14759 and real 8x8 Clements photonic processor https://www.nature.com/articles/s41566-026-01997-x",
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"calibrated":out["mode_by_mode_corrected_deficit"],
       "global_bias":out["global_calibration_bias"],
       "shots":out["shot_statistics"]},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
