"""Front4: explicit detector false-click contamination plus reference
phase drift in 36-setting single-photon 18-output tomography.
Dark-click replacement is a transparent toy channel, not hardware model.
"""
from __future__ import annotations
import json
import numpy as np
from pathlib import Path
from w33_20261019_round9_photon_tomography_shots import Uref,echo,transfer,probabilities,analytic_contrasts,invert_contrasts
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round10_optical_detector_and_drift.json"
W=echo();M=transfer(.16)
rng=np.random.default_rng(190610)
def detector(p,d):
    q=(1-d)*p.copy()
    q[:18]+=d/18
    assert np.all(q>=-1e-12) and abs(sum(q)-1)<1e-12
    return q
def tomography(T,n,dark):
    obs=np.empty((9,9,2))
    for j in range(9):
        for phiindex,phi in enumerate((0,np.pi/2)):
            p=detector(probabilities(T,j,phi),dark)
            cnt=rng.multinomial(n,p)
            obs[:,j,phiindex]=(cnt[:9]-cnt[9:18])/n
    return invert_contrasts(obs)
def run():
    ideal=1-np.trace(W).real/9
    baselines=[]
    for darkR,darkS,phase in ((0,0,0),(.005,.005,0),(.005,.015,0),(.005,.005,.03),(.005,.015,.03)):
        # Analytic reconstruction: detector dark replacement scales
        # both quadratures by 1-d (uniform added false clicks cancel).
        # Phase drift multiplies complex signal transfer by e^(i phase).
        Wr=np.linalg.solve((1-darkR)*M,(1-darkS)*M@W*np.exp(1j*phase))
        est=1-np.trace(Wr).real/9
        baselines.append({"false_click_R":darkR,"false_click_S":darkS,
            "uncalibrated_path_phase_drift_rad":phase,
            "idealized_observed_deficit":float(est),
            "contrast_bias":float(est-ideal)})
    trials=70;n=12000;shot=[]
    for darkR,darkS,phase in ((.005,.005,0),(.005,.015,0),(.005,.005,.03)):
        vals=[]
        for _ in range(trials):
            R=tomography(M,n,darkR)
            S=tomography(M@W*np.exp(1j*phase),n,darkS)
            z=np.linalg.solve(R,S)
            vals.append(float(1-np.trace(z).real/9))
        row=next(z for z in baselines if z["false_click_R"]==darkR and z["false_click_S"]==darkS and z["uncalibrated_path_phase_drift_rad"]==phase)
        shot.append({"false_click_R":darkR,"false_click_S":darkS,"path_drift":phase,
          "sample_mean":float(np.mean(vals)),"sample_std":float(np.std(vals,ddof=1)),
          "analytic_reference":row["idealized_observed_deficit"],
          "sample_vs_analytic":float(np.mean(vals)-row["idealized_observed_deficit"])})
    checks={
     "stationary_dark_false_clicks_cancel_by_ratio":abs(baselines[1]["contrast_bias"])<1e-12,
     "differential_false_clicks_shift_witness":abs(baselines[2]["contrast_bias"])>.005,
     "phase_drift_shifts_witness":abs(baselines[3]["contrast_bias"])>.0001,
     "MonteCarlo_near_analytic_expectation":all(abs(r["sample_vs_analytic"])<.012 for r in shot),
     "70_repetitions_3_conditions":len(shot)==3 and trials==70}
    out={"schema":"w33.round10.36setting_dark_replacement_and_phase_drift.v1",
     "detector_model":"An independent probability d per photon of a detector-background 'replacement event' assigned uniformly among 18 output ports, instead of the intended path/mode or erasure. Then measured path difference D -> (1-d) D. Equal calibration/signal d cancels on transfer-matrix inversion; differential d or path-reference phase drift does not. NOT a realistic independent-Poisson multi-click or afterpulsing model.",
     "ideal_trace_deficit":float(ideal),
     "analytic_cases":baselines,
     "synthetic_photon_statistics":{"n_per_setting":n,"settings_per_run":36,"source_photons_per_run":36*n,"repetitions_per_case":trials,"cases":shot},
     "falsification_controls":"Interleave R and S reference acquisitions, test phase-reversed W, commuting null, detector-off/sham, source power drift, and mode-mixing transfer tomography; timestamp all 36 settings.",
     "hardware_boundary":"Real dark count depends on gate duration and dead-time; this symmetric false-click toy channel does not reproduce multi-click events, erasure bias, correlated errors or path-dependent detector response. No physical photonic hardware constructed.",
     "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"biases":[x["contrast_bias"] for x in baselines],"shot":shot},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
