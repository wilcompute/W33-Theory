#!/usr/bin/env python3
"""Phase-referenced Witting interferometer: optimal quadrature Fisher and finite-shot tests.

Compare X/intensity-style quadratic phase readout to Y/linear quadrature
under symmetric SPAM and iid Gaussian phase jitter. Hardware assumptions
are illustrative, no measured device data.
"""
from __future__ import annotations
import math,json
from pathlib import Path
from scipy.stats import binom
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_further_photonic_quadrature_fisher.json'

def probs(theta,confusion=0.01,sigma=0.03):
    visibility=(1-2*confusion)*math.exp(-sigma*sigma/2)
    # X-minus ideal phase=0 causes zero; symmetric bit flip creates baseline q.
    pX0=(1-visibility)/2
    pX1=(1-visibility*math.cos(theta))/2
    # Y quadrature has p0=1/2, linear slope around theta=0.
    pY0=.5
    pY1=(1+visibility*math.sin(theta))/2
    return dict(visibility=visibility,X=(pX0,pX1),Y=(pY0,pY1))

def min_shots(p0,p1,alpha=.05,power=.95):
    assert 0<p0<p1<1
    def decision(n):
        # Smallest integer threshold k with P_null(K>=k)<=alpha.
        k=int(binom.isf(alpha,n,p0))+1
        fp=float(binom.sf(k-1,n,p0))
        tp=float(binom.sf(k-1,n,p1))
        assert fp<=alpha+1e-12
        return k,fp,tp
    lo,hi=0,32
    while decision(hi)[2]<power:
        lo=hi;hi*=2
        if hi>20000000:raise ValueError('Shot budget too large')
    while hi-lo>1:
        mid=(hi+lo)//2
        if decision(mid)[2]>=power:hi=mid
        else:lo=mid
    k,fp,tp=decision(hi)
    assert tp>=power and (hi==1 or decision(hi-1)[2]<power)
    return dict(detected_photons=hi,rejection_threshold_counts=k,
         actual_typeI_error=fp,actual_statistical_power=tp)

def verify():
    q=.01;sigma=.03
    rows=[]
    for theta in (.1,.3,math.pi/3):
        p=probs(theta,q,sigma)
        X=min_shots(*p['X']);Y=min_shots(*p['Y'])
        survival=.85*.98**(4*5+1) # five gates + one readout interferometer, toy loss
        X['input_pulses_lower_ceil']=math.ceil(X['detected_photons']/survival)
        Y['input_pulses_lower_ceil']=math.ceil(Y['detected_photons']/survival)
        rows.append(dict(test_phase_rad=theta,detected_photon_transmission_assumed=survival,
          X_readout_probabilities=p['X'],Y_readout_probabilities=p['Y'],X=X,Y=Y,
          detected_shot_reduction_ratio=X['detected_photons']/Y['detected_photons']))
    vis=probs(0,q,sigma)['visibility']
    fisherY0=vis**2
    # Quantum Fisher information of balanced |0>+|1> under P0 phase generator is 1.
    assert 0<fisherY0<1
    assert rows[0]['X']['detected_photons']>rows[0]['Y']['detected_photons']
    assert rows[0]['Y']['detected_photons']>100
    return dict(status='PASS_OPTIMAL_QUADRATURE_FISHER_AND_LOSSY_SHOT_TESTS',date='2026-11-22',
      measurement_design='After calibrated U^-1 prep, probe (|0>+|1>)/sqrt2; apply D_theta; output X-minus and Y-minus interferometers, with independent phase reference.',
      ideal_X_minus_probability='sin^2(theta/2); quadratic phase response near zero',
      ideal_Y_quadrature_probability='(1+sin(theta))/2; linear phase response near zero',
      output_visibility='(1-2e)*exp(-sigma^2/2)',e_symmetric_confusion=q,gaussian_phase_jitter_sigma=sigma,
      Fisher_information_per_detected_photon_at_zero=fisherY0,
      ideal_quantum_Fisher_information_per_photon=1,
      experiment='Exact one-sided binomial false-positive <=0.05, power>=0.95, calibrated e and sigma',
      measured_shot_budget_rows=rows,
      caveat='Only a single coherent diagonal phase-error alternative. Requires an independent phase reference, trusted SPAM/jitter and iid samples. Input attempt estimates assume independent loss and ignore switching, dark counts, dead time, source imperfections, and multiphoton effects. No physical device measured.')

def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(d,indent=2)+'\n');print(d['status'])
    for r in d['measured_shot_budget_rows']:
        print(round(r['test_phase_rad'],5),'X',r['X']['detected_photons'],'Y',r['Y']['detected_photons'],'ratio',round(r['detected_shot_reduction_ratio'],2))
if __name__=='__main__':main()
