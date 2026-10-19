"""Predeclared experimental accept/reject rule for ideal 18-mode
interferometer, with MODE-RESOLVED multinomial shot noise, independent
Poisson dark clicks, sequential gate afterpulse correlations, a stable
nonideal input mixer and partially common-mode path-phase drift.

Every result is synthetic; NOT a measured optical system.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from w33_20261019_round9_photon_tomography_shots import Uref,echo,transfer
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round12_optical_falsification.json"
rng=np.random.default_rng(220919)
M=transfer(.16);W=echo();n=15000
# Stable calibrated imperfect mode preparation (coherently mixed).
H=np.zeros((9,9),complex)
for j in range(8):H[j,j+1]=H[j+1,j]=1
PREP=expm(1j*.01*H)
REF=Uref@PREP
def probs(T,j,ph):
    a=REF[:,j];b=np.exp(1j*ph)*T[:,j]
    plus=abs(a+b)**2/4;minus=abs(a-b)**2/4
    erase=max(0.,float(1-plus.sum()-minus.sum()))
    p=np.r_[plus,minus,erase]
    assert abs(sum(p)-1)<1e-11 and min(p)>=0
    return p
def measure(T,ph,d,prev):
    obs=np.zeros((9,9,2))
    for j in range(9):
      for k,phase in enumerate((0.,np.pi/2)):
        p=probs(T,j,phase+ph)
        c=rng.multinomial(n,p)
        b=rng.poisson(n*d/18,size=18)
        a=rng.poisson(.001*prev)
        obs[:,j,k]=((c[:9]+b[:9]+a[:9])-(c[9:18]+b[9:]+a[9:]))/n
        prev=c[:18]+b+a
    return (obs[:,:,0]-1j*obs[:,:,1])/np.conj(REF),prev
def trial(real):
    common=rng.normal(0,.03)
    driftref=rng.normal(0,.006)
    driftS=rng.normal(0,.006)
    driftN=rng.normal(0,.006)
    dbase=.0018
    dR=max(0,dbase+rng.normal(0,.00015))
    dS=max(0,dbase+rng.normal(0,.00015))
    dN=max(0,dbase+rng.normal(0,.00015))
    prev=np.zeros(18)
    R,prev=measure(M@PREP,driftref,dR,prev)
    S,prev=measure(M@(W if real else np.eye(9))@PREP,common+driftS,dS,prev)
    N,prev=measure(M@PREP,common+driftN,dN,prev)
    sig=1-np.trace(np.linalg.solve(R,S)).real/9
    ctrl=1-np.trace(np.linalg.solve(R,N)).real/9
    return float(sig-ctrl),float(sig),float(ctrl)
def run():
    training=[trial(False) for _ in range(90)]
    train=np.array(training)
    mu0=float(train[:,0].mean())
    sd0=float(train[:,0].std(ddof=1))
    # Design-level 5 sigma acceptance based ONLY on independent
    # pre-calibration null data. Two-sided gross-alignment control.
    threshold=mu0+5*sd0
    ctrl_limit=5*float(train[:,2].std(ddof=1))
    null=np.array([trial(False) for _ in range(100)])
    signal=np.array([trial(True) for _ in range(100)])
    false=int((null[:,0]>threshold).sum())
    true=int((signal[:,0]>threshold).sum())
    ctrl_false=int((abs(null[:,2])>ctrl_limit).sum())
    ctrl_signal=int((abs(signal[:,2])>ctrl_limit).sum())
    checks={"90_independent_null_training_runs":len(train)==90,
       "100_out_of_sample_null_and_signal":len(null)==len(signal)==100,
       "null_rate_no_overfit":false<=3,
       "W33_signal_detected":true>=95,
       "signal_mean_consistent_8_27":abs(signal[:,0].mean()-8/27)<.02,
       "trained_threshold_positive_finite":0<threshold<.1,
       "null_control_remains_near_zero":abs(signal[:,2].mean())<.02}
    out={"schema":"w33.round12.photon_falsification_preregistered_synthetic.v1",
       "experiment":"54 settings per trial: R calibration + S signal + N commuting control, each with 9 basis inputs and 2 phase quadratures, 19 possible outcomes (18 path-mode detections and erasure). Calibrated coherent input mode mixing exp(i0.01 H_chain), output loss/crosstalk M, independent per-gate 19-outcome multinomial photon records, Poisson dark clicks at ~0.18% source-photon fraction redistributed across 18 output detectors, 0.1% sequential afterpulse counts from previous gate's detector-bin totals, coherent correlated path phase sigma=0.03 rad plus per-condition sigma=0.006 rad, independent detector dark drift.",
       "photons_per_setting":n,"total_source_photons_per_trial":54*n,
       "acceptance_protocol":"TRAIN on 90 fresh NO-SIGNAL runs, predefine threshold=mean(delta_sig-delta_ctrl)+5*sampleSD(delta_sig-delta_ctrl). EVALUATE 100 held-out null (W=I) and 100 signal (W=W33) runs. Also monitor commuting control abs(delta_ctrl) below a training-derived 5-sigma limit. Do NOT use held-out outcomes to fit decision threshold.",
       "null_training":{"n":90,"paired_difference_mean":mu0,"paired_difference_std":sd0,
           "predeclared_positive_threshold":threshold,"control_abs5sd_limit":ctrl_limit},
       "held_out_null":{"n":100,"paired_difference_mean":float(null[:,0].mean()),
           "paired_difference_std":float(null[:,0].std(ddof=1)),"false_positive_count":false,
           "control_gross_outlier_count":ctrl_false},
       "held_out_signal":{"n":100,"paired_difference_mean":float(signal[:,0].mean()),
           "paired_difference_std":float(signal[:,0].std(ddof=1)),"detected_count":true,
           "control_gross_outlier_count":ctrl_signal},
       "ideal_W33_deficit":float(8/27),
       "limitations":"Synthetic shot model, not calibrated against fabricated source/detector data. Poisson additive clicks are a low-rate approximation, not a complete dead-time/saturation model. Thermal drift correlation, Raman scattering, pulse pileup and calibration gauge alignment require lab-specific measurements; 0/100 simulated false positives would not prove zero physical FPR.",
       "checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2,default=lambda x:x.item() if hasattr(x,'item') else str(x))+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"threshold":threshold,"sdnull":sd0,"false":false,"detections":true,"signal_mean":float(signal[:,0].mean())},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
