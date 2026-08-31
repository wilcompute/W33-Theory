#!/usr/bin/env python3
"""Multimode same-waist LG audit for q=1/2 versus q=3/2 q-plates.

The existing p=0 surrogate measures the overlap between the unchanged radial
envelope of an ideal thin phase-only q-plate output and the p=0 LG radial mode
associated with the shifted |ell|. This continuation resolves the entire
radial decomposition in the target-|ell| Laguerre-Gaussian basis.

With x=2 r^2/w^2, normalized radial functions are
  phi_{p,n}(x)=sqrt(p!/(p+n)!) x^(n/2) exp(-x/2) L_p^n(x).
For an incident p=0 mode with m=|ell_in| and a phase-only shift to
n=|ell_out|, the exact overlap probability obeys

  P_0 = Gamma((m+n)/2+1)^2/(Gamma(m+1) Gamma(n+1)),
  P_{p+1}/P_p = (p+(n-m)/2)^2 / ((p+1)(p+n+1)).

The infinite target-n radial basis is complete, so the total probability is
one in the ideal model. A coherent inverse phase plate therefore restores the
input exactly if radial coherence is retained. Loss appears only when the
receiver truncates/projects the radial basis.

This remains an engineering firewall model: no finite aperture, propagation,
retardance error, aberration, mode-sorter loss, p-dependent phase error, or
measured q-plate insertion loss is included.
"""
from __future__ import annotations
import json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_QPLATE_RADIAL_MULTIMODE_RECENTER.json'
CENTERED=(-1,0,1)
THRESHOLDS=(0.90,0.99,0.999,0.9999)
BUDGETS=(0,1,2,4,8,16,24,32,64,128,256,512,2048,8192,25000)
MAX_P=max(BUDGETS)

def p0_probability(m:int,n:int)->float:
    a=(m+n)/2.0
    return math.gamma(a+1.0)**2/(math.gamma(m+1.0)*math.gamma(n+1.0))

def radial_probabilities(m:int,n:int,max_p:int=MAX_P):
    p=[p0_probability(m,n)]
    b=(n-m)/2.0
    for k in range(max_p):
        p.append(p[-1]*((k+b)*(k+b))/((k+1)*(k+n+1)))
    return p

def audit_transition(ell:int,sigma:int,shift:int):
    target=ell+sigma*shift
    m,n=abs(ell),abs(target)
    probs=radial_probabilities(m,n)
    cum=[];s=0.0
    for v in probs:
        s+=v;cum.append(s)
    hits={}
    for t in THRESHOLDS:
        idx=next((i for i,x in enumerate(cum) if x+1e-15>=t),None)
        hits[str(t)]=idx
    assert all(v is not None for v in hits.values())
    assert all(cum[i+1]+1e-15>=cum[i] for i in range(len(cum)-1))
    assert cum[-1] <= 1.000000000001
    return {
      'helicitySign':sigma,'ellIn':ell,'ellOut':target,'deltaEll':sigma*shift,
      'absEllIn':m,'absEllOut':n,'p0Capture':probs[0],
      'radialModeThresholdPmax':hits,
      'captureByPmax':{str(k):cum[k] for k in BUDGETS},
      'tailBeyondP25000':1.0-cum[MAX_P]
    }

def audit(q:float):
    shift=int(round(2*q)); assert abs(2*q-shift)<1e-12
    rows=[audit_transition(ell,sigma,shift) for sigma in (-1,1) for ell in CENTERED]
    means={str(k):sum(r['captureByPmax'][str(k)] for r in rows)/len(rows) for k in BUDGETS}
    return {
      'q':q,'absDeltaEll':shift,'pureChiralityModulo3':shift%3==0,
      'states':rows,'meanCaptureByPmax':means,
      'meanP0Capture':means['0'],
      'meanTailBeyondP25000':sum(r['tailBeyondP25000'] for r in rows)/len(rows)
    }

def main():
    qhalf=audit(0.5); qthree=audit(1.5)
    assert not qhalf['pureChiralityModulo3'] and qthree['pureChiralityModulo3']
    assert abs(qhalf['meanP0Capture']-0.8181230868723421)<1e-12
    assert abs(qthree['meanP0Capture']-0.5460971604872884)<1e-12
    hard=[r for r in qthree['states'] if r['absEllIn']==0 and r['absEllOut']==3]
    assert len(hard)==2
    for r in hard:
        assert r['radialModeThresholdPmax']['0.99']==222
        assert r['radialModeThresholdPmax']['0.999']==2247
        assert r['radialModeThresholdPmax']['0.9999']==22497
    out={
      'schema':'w33.20260831.qplate-radial-multimode-recenter.v1','status':'PASS',
      'model':{
        'inputCode':'centered OAM qutrit ell=-1,0,+1, radial p=0',
        'qPlate':'ideal thin phase-only azimuthal shift Delta ell=+/-2q at fixed waist',
        'targetBasis':'complete same-waist LG radial basis at target |ell|',
        'probabilityRecurrence':'P0=Gamma((m+n)/2+1)^2/(Gamma(m+1)Gamma(n+1)); P[p+1]/P[p]=(p+(n-m)/2)^2/((p+1)(p+n+1))',
        'coherentInverse':'unit survival in the ideal model if the full radial superposition is retained; truncation/projection creates the reported loss'
      },
      'qHalf':qhalf,'qThreeHalves':qthree,
      'comparison':{
        'meanCaptureP0':{'qHalf':qhalf['meanCaptureByPmax']['0'],'qThreeHalves':qthree['meanCaptureByPmax']['0']},
        'meanCaptureP24':{'qHalf':qhalf['meanCaptureByPmax']['24'],'qThreeHalves':qthree['meanCaptureByPmax']['24']},
        'meanCaptureP256':{'qHalf':qhalf['meanCaptureByPmax']['256'],'qThreeHalves':qthree['meanCaptureByPmax']['256']},
        'meanCaptureP2048':{'qHalf':qhalf['meanCaptureByPmax']['2048'],'qThreeHalves':qthree['meanCaptureByPmax']['2048']}
      },
      'theorem':'In the declared ideal same-waist phase-only model, the q=3/2 modulo-3 chirality advantage is not intrinsically absorptive: its apparent p=0 loss is redistribution into a long radial LG tail. Full coherent radial retention makes the inverse conversion unitary. However the ell=0 to |ell|=3 channel is exceptionally broad: p<=222 is required for 99%, p<=2247 for 99.9%, and p<=22497 for 99.99% capture. Thus a practical q=3/2 interface needs explicit radial-mode engineering; a p=0-only receiver is inadequate.',
      'boundary':'Analytic ideal same-waist LG basis decomposition only. No finite aperture, propagation, q-plate retardance profile, aberration, radial-mode sorter/corrector loss, p-dependent phase control error, detector coupling, or measured insertion loss is modeled.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','qHalfP0':qhalf['meanP0Capture'],'qThreeP0':qthree['meanP0Capture'],
                      'qHalfP24':qhalf['meanCaptureByPmax']['24'],'qThreeP24':qthree['meanCaptureByPmax']['24'],
                      'qThreeHard99':hard[0]['radialModeThresholdPmax']['0.99'],
                      'qThreeHard999':hard[0]['radialModeThresholdPmax']['0.999'],
                      'qThreeHard9999':hard[0]['radialModeThresholdPmax']['0.9999']},sort_keys=True))

if __name__=='__main__': main()
