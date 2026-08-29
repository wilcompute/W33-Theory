#!/usr/bin/env python3
"""Quantitative radial-mode surrogate for q=1/2 versus q=3/2 q-plates.

A thin ideal q-plate contributes an azimuthal phase exp(+-i 2 q phi), changing
ell by +-2q while leaving the incident radial envelope unchanged at the plate.
If the receiver insists on the p=0 Laguerre-Gaussian radial profile associated
with the shifted |ell| at the same waist, the phase-only conversion therefore
has a nontrivial radial capture penalty.  For normalized p=0 LG radial modes,

  |<R_0^m,R_0^n>|^2 = Gamma((m+n)/2+1)^2/(Gamma(m+1)Gamma(n+1)).

We apply this declared surrogate to the centered qutrit ell={-1,0,+1}, both
helicities, and report single-pass p=0 capture plus a hard-project/recenter
round trip.  This is an engineering firewall calculation, not a q-plate device
simulation: it omits finite aperture, retardance errors, propagation, radial
p>0 coherent recombination, aberrations, and measured loss.
"""
from __future__ import annotations
import json,math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_QPLATE_RADIAL_RECENTER_SURROGATE.json'
CENTERED=(-1,0,1)


def p0_capture(m:int,n:int)->float:
    a=math.gamma((m+n)/2+1.0)
    return (a*a)/(math.gamma(m+1.0)*math.gamma(n+1.0))


def audit(q:float):
    shift=int(round(2*q));assert abs(2*q-shift)<1e-12
    rows=[]
    for sigma in (-1,1):
        for ell in CENTERED:
            target=ell+sigma*shift
            p=p0_capture(abs(ell),abs(target))
            rows.append({'helicitySign':sigma,'ellIn':ell,'deltaEll':sigma*shift,'ellOut':target,
                         'absEllIn':abs(ell),'absEllOut':abs(target),
                         'singlePassP0Capture':p,'singlePassRadialLeakage':1-p,
                         'hardProjectThenInverseRecenterP0Survival':p*p})
    ps=[r['singlePassP0Capture'] for r in rows]
    rt=[r['hardProjectThenInverseRecenterP0Survival'] for r in rows]
    return {'q':q,'absDeltaEll':shift,'pureChiralityModulo3':shift%3==0,
            'states':rows,'meanSinglePassP0Capture':sum(ps)/len(ps),
            'worstSinglePassP0Capture':min(ps),'meanSinglePassRadialLeakage':1-sum(ps)/len(ps),
            'meanHardProjectRecenterSurvival':sum(rt)/len(rt),'worstHardProjectRecenterSurvival':min(rt)}


def main():
    qhalf=audit(0.5);qthree=audit(1.5)
    assert not qhalf['pureChiralityModulo3'] and qthree['pureChiralityModulo3']
    out={'schema':'w33.20260829.qplate-radial-recenter-surrogate.v1','status':'PASS',
         'model':{'inputCode':'centered OAM qutrit ell=-1,0,+1','radialFamily':'same-waist LG p=0',
                  'qPlate':'phase-only ideal azimuthal shift Delta ell = +/-2q',
                  'captureFormula':'Gamma((m+n)/2+1)^2 / (Gamma(m+1) Gamma(n+1)), m=|ell_in|, n=|ell_out|',
                  'recenterScenario':'hard projection into shifted p=0 radial mode, followed by phase-only inverse OAM recenter and p=0 projection'},
         'qHalf':qhalf,'qThreeHalves':qthree,
         'comparison':{'meanCaptureRatioQ3over2ToQ1over2':qthree['meanSinglePassP0Capture']/qhalf['meanSinglePassP0Capture'],
                       'extraMeanSinglePassLeakage':qthree['meanSinglePassRadialLeakage']-qhalf['meanSinglePassRadialLeakage'],
                       'meanRoundTripSurvivalRatio':qthree['meanHardProjectRecenterSurvival']/qhalf['meanHardProjectRecenterSurvival']},
         'reading':'q=3/2 is algebraically cleaner for the mod-3 chirality interface because +/-3 is invisible modulo 3, but in this same-waist phase-only p=0 surrogate it pays a substantially larger radial-mode capture penalty than q=1/2. A real design therefore needs radial-mode engineering/recentering rather than treating the modulo-3 selection rule as lossless.',
         'boundary':'Analytic LG p=0 overlap surrogate only. No calibrated q=3/2 device, finite-aperture propagation, q-plate retardance profile, radial p>0 coherent recovery, or measured insertion loss is modeled.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
