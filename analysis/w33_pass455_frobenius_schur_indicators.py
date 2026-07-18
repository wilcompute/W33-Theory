#!/usr/bin/env python3
"""Pass 455: ordinary and center-inverting twisted FS indicators."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass455_frobenius_schur_indicators.json'

def hmul(g,h):return ((g[0]+h[0])%3,(g[1]+h[1])%3,(g[2]+h[2]-g[0]*h[1]+h[0]*g[1])%3)
def htau(g):return (g[0],-g[1]%3,-g[2]%3)

def rmul(g,h,e=4):return ((g[0]+h[0]*pow(e,g[1],9))%9,(g[1]+h[1])%3)
def rtau(g):return (-g[0]%9,g[1])

def build_payload():
    z3=np.exp(2j*np.pi/3);z9=np.exp(2j*np.pi/9)
    H=[(a,b,c) for a in range(3) for b in range(3) for c in range(3)]
    R=[(a,b) for a in range(9) for b in range(3)]
    results={};checks={}
    checks['H_tau_automorphism']=all(htau(hmul(g,h))==hmul(htau(g),htau(h)) for g in H for h in H)
    checks['H_tau_involution']=all(htau(htau(g))==g for g in H)
    checks['R_tau_automorphism']=all(rtau(rmul(g,h))==rmul(rtau(g),rtau(h)) for g in R for h in R)
    checks['R_tau_involution']=all(rtau(rtau(g))==g for g in R)
    for t in (1,2):
        def chiH(g):return 3*z3**(t*g[2]) if g[0]==0 and g[1]==0 else 0j
        ordinary=sum(chiH(hmul(g,g)) for g in H)/27
        twisted=sum(chiH(hmul(g,htau(g))) for g in H)/27
        results[f'H3_faithful_{t}']={'ordinary':float(round(float(np.real_if_close(ordinary).real))),'twisted_tau':float(round(float(np.real_if_close(twisted).real)))}
        checks[f'H3_{t}_ordinary_zero']=abs(ordinary)<1e-9
        checks[f'H3_{t}_twisted_plus_one']=abs(twisted-1)<1e-9
    for r in (1,2):
        orbit=(r,4*r%9,7*r%9)
        def chiR(g):return sum(z9**(a*g[0]) for a in orbit) if g[1]==0 else 0j
        ordinary=sum(chiR(rmul(g,g)) for g in R)/27
        twisted=sum(chiR(rmul(g,rtau(g))) for g in R)/27
        results[f'R9_faithful_{r}']={'ordinary':float(round(float(np.real_if_close(ordinary).real))),'twisted_tau':float(round(float(np.real_if_close(twisted).real)))}
        checks[f'R9_{r}_ordinary_zero']=abs(ordinary)<1e-9
        checks[f'R9_{r}_twisted_plus_one']=abs(twisted-1)<1e-9
    checks['indicator_profiles_identical']=len({(round(v['ordinary']),round(v['twisted_tau'])) for v in results.values()})==1
    return {
      'schema':'w33.pass455.frobenius_schur_indicators.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'canonical_involutions':{
        'H3':'tau(a,b,c)=(a,-b,-c), an involution inverting the center',
        'R9':'tau(x^a y^b)=x^(-a)y^b, an involution inverting <x^3>',
      },
      'results':results,
      'theorem':(
        'Every faithful degree-three irrep in both extraspecial groups has ordinary FS indicator 0 and '
        'center-inverting twisted indicator +1. Ordinary non-self-duality and twisted real structure are '
        'therefore identical on the exponent-three and exponent-nine sides.'),
      'resolution':(
        'The exp-3/exp-9 distinction is absent not only from the PDS image spectrum but also from these '
        'canonical ordinary/twisted Frobenius-Schur indicators. Any remaining distinction must use finer '
        'monoidal, integral, or extension data.'),
      'checks':{k:bool(v) for k,v in checks.items()},
    }
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 455 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
