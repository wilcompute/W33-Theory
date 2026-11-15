#!/usr/bin/env python3
"""Calibration only for an endpoint GHZ witness CONTRAST, no circulant assumption.

This estimates the 16 numbers w^T C[:,j], not all 256 entries of
an unknown detector-confusion matrix C.  Hoeffding simultaneously bounds
the bias of the observable for ANY true rail distribution p, with
no assumption that the columns are translates of each other.
"""
import json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261115_direct_witness_contrast_calibration.json"

def run(seed=20151115,rad=.01,dflip=.005):
    rng=np.random.default_rng(seed)
    m=16
    I=np.eye(m)
    er=.023;el=.017;dk=.006
    C=(1-er-el-dk)*I+er*np.roll(I,1,axis=0)+el*np.roll(I,-1,axis=0)+dk*np.ones((m,m))/m
    v=np.zeros(16);v[[0,15]]=1
    w=np.linalg.solve(C.T,v)
    R=float(np.ptp(w))
    assert np.max(abs(C.sum(axis=0)-1))<1e-13
    assert np.allclose(w@C,v,atol=1e-12)
    # Joint 99% confidence: budget witness .005, contrast .0025, parity .0025.
    aC=.0025;aP=.0025;aW=.005
    nC=math.ceil(R*R*math.log(2*m/aC)/(2*rad*rad))
    nP=math.ceil(math.log(4/aP)/(2*dflip*dflip))
    assert 2*m*math.exp(-2*nC*rad*rad/(R*R))<=aC*(1+1e-12)
    assert 4*math.exp(-2*nP*dflip*dflip)<=aP*(1+1e-12)
    # Independent calibration for each rail, no pool across rails.
    sample_by_input=np.array([rng.multinomial(nC,C[:,j]) for j in range(16)])
    obsContrast=sample_by_input@w/nC
    deviations=np.abs(obsContrast-v)
    conditionalZbias=float(np.max(deviations)+rad)
    # Negative control: arbitrarily corrupt ONE readout column, without
    # changing other 15 columns. Contrast-specific calibration explicitly
    # detects that rail-specific defect; unverified cyclic pooling would not.
    Cbad=C.copy()
    Cbad[:,0]=np.roll(Cbad[:,0],3)
    assert np.allclose(Cbad.sum(axis=0),np.ones(16))
    anomaly_contrast=float(abs(w@Cbad[:,0]-v[0]))
    assert anomaly_contrast>.5

    ep=.025;em=.018
    epHat=float(rng.binomial(nP,ep)/nP)
    emHat=float(rng.binomial(nP,em)/nP)
    gHat=1-epHat-emHat;offHat=emHat-epHat
    assert gHat>0
    # Reproduce the prior synthetic signal with fresh independent clicks.
    depol=.03;phase=.08;sig=.1;drift=.07
    p=np.full(16,depol/16);p[[0,15]]+=(1-depol)/2
    A=(1-depol)*math.exp(-sig**2-drift**2/2)*math.cos(phase)
    Ftruth=(p[0]+p[15]+A)/2
    nZ=12000;nE=8000
    outcomesZ=rng.multinomial(nZ,C@p)
    pHat=float(w@outcomesZ/nZ)
    equat=[]
    for k in range(4):
        true_mu=(-1)**k*A
        obs= (1-ep-em)*true_mu +(em-ep)
        success=float((1+obs)/2)
        plus=rng.binomial(nE,success)
        mean=(2*plus/nE-1)
        equat.append((mean-offHat)/gHat)
    Ahat=float(sum((-1)**k*equat[k] for k in range(4))/4)
    Fhat=(pHat+Ahat)/2

    logfac=math.log(2*5/aW)
    radZ=R*math.sqrt(logfac/(2*nZ))
    radE=(2/gHat)*math.sqrt(logfac/(2*nE))
    statistical_half_width=.5*(radZ+radE)
    # Parity estimate error: for |mu|<=1, eps_p/m each within dflip,
    # |(o-oHat)+(g-gHat)*mu| <= 2*dflip
    # This bounds corrected +/- expectation error <=2*dflip/gHat.
    calib_half_width=.5*conditionalZbias+dflip/gHat
    lower=Fhat-statistical_half_width-calib_half_width
    assert 0<lower<=Fhat<=1
    totalCalibration=16*nC+2*nP
    # The bound holds regardless of any rail-to-rail translation symmetry.
    # For an adversarial unknown true C, the calibration empirical score
    # max_j|muhat_j-v_j| enters explicitly, unlike a "trusted matrix" bound.
    return {
      "status":"MODEL_FREE_16_RAIL_WITNESS_CONTRAST_JOINT_99PCT_CALIBRATION",
      "assumptions":"Can prepare all 16 known rail states, stationary memoryless column-stochastic readout for calibration/signal, independent calibration trials, and trusted parity reference preparations. Does NOT assume circulant or uniform crosstalk.",
      "observable_contrast":"v_j=delta(j,0)+delta(j,15), w=C_nominal^{-T} v",
      "end_to_end_confidence":"P(all rail contrast errors <= r, both parity flip errors <= d, all 5 witness means inside Hoeffding intervals) >= 0.99",
      "simulated_true_C_is_circulant_but_validity_does_not_require_it":True,
      "joint_failure_split":{"16_contrasts":aC,"2_parity_rates":aP,"5_witness_settings":aW},
      "sample_weight_range":R,
      "absolute_rail_contrast_tolerance_radius":rad,
      "parity_flip_error_radius":dflip,
      "accepted_rail_preparations_each":nC,
      "accepted_total_rail_calibration":16*nC,
      "accepted_parity_calibrations_each":nP,
      "accepted_total_calibration":totalCalibration,
      "previous_4class_pooled_calibration_accepted_total":6573041,
      "prior_unstructured_16x16_l1_calibration_accepted_total":153290096,
      "max_observed_contrast_deviation":float(max(deviations)),
      "single_corrupted_rail_analytic_contrast_anomaly":anomaly_contrast,
      "rail_specific_anomaly_detectable_without_circulant_assumption":True,
      "simultaneous_Z_observable_calibration_bias_bound":conditionalZbias,
      "parity_flip_estimates":[epHat,emHat],
      "observed_synthetic_witness_fidelity":Fhat,
      "true_synthetic_witness_fidelity":Ftruth,
      "statistical_half_width":statistical_half_width,
      "calibration_half_width":calib_half_width,
      "joint_99pct_corrected_fidelity_lower":lower,
      "limits":"Synthetic independent data, not a hardware measurement. Counts are sufficient accepted preparations. Genuine drift between calibration and signal, imperfect known rail preparations, and correlated detection invalidate bound."
    }

if __name__=="__main__":
    r=run()
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print("PASS",r["status"],"samples",r["accepted_total_calibration"],
          "lower",r["joint_99pct_corrected_fidelity_lower"],flush=True)
