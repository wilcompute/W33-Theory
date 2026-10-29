#!/usr/bin/env python3
"""Fixed-port W33-vs-dual three-photon experiment: global binomial budgets.

Independent per-emission model: with probability eta**3 the whole triple
survives and has the previously proved event probability; otherwise a
hypothesis-independent false-registration event occurs with probability beta.
No detector calibration, drift, or mode-dependent loss is simulated.
"""
import json
import numpy as np
from scipy.stats import binom

DEN=15**6

def ideal(s):
    w=(17496+52488*s*s+34992*s**3)/DEN
    d=(3376+1328*s*s-2048*s**3)/DEN
    assert 0<=d<w<=1
    return w,d

def global_budget(pw,pd,alpha=.001,nmax=85000):
    # Enumerate EVERY integer trial count, not just N-1 at a proposed candidate.
    N=np.arange(1,nmax+1)
    # Smallest threshold k for dual false-positive < alpha.
    k=binom.isf(alpha,N,pd).astype(np.int64)+1
    falsepositive=binom.sf(k-1,N,pd)
    # Protect against rare floating-point equality at the threshold.
    k=k+(falsepositive>=alpha)
    fp=binom.sf(k-1,N,pd)
    fn=binom.cdf(k-1,N,pw)
    good=(fp<alpha)&(fn<alpha)&(k<=N)
    if not good.any():
        return {"status":"NO_FEASIBLE_BUDGET_IN_RANGE","max_N":nmax}
    i=int(np.flatnonzero(good)[0])
    assert not good[:i].any()
    return dict(N=int(N[i]),cutoff=int(k[i]),false_positive=float(fp[i]),
                false_negative=float(fn[i]),all_smaller_N_checked=True)

def scenario(s,eta,beta):
    w,d=ideal(s);survive=eta**3
    pw=survive*w+(1-survive)*beta
    pd=survive*d+(1-survive)*beta
    return dict(overlap=s,per_photon_eta=eta,false_event_on_failed_triple=beta,
                threefold_survival=survive,observed_W33=pw,observed_dual=pd,
                observed_gap=pw-pd,**global_budget(pw,pd))

def main():
    grid=[scenario(s,e,b) for s in (0,.5,.8,1) for e,b in ((1,0),(.9,0),(.7,0),(.9,.0001))]
    ideal0=next(z for z in grid if z['overlap']==0 and z['per_photon_eta']==1)
    assert ideal0['N']==19427 and ideal0['cutoff']==15
    ideal5=next(z for z in grid if z['overlap']==.5 and z['per_photon_eta']==1)
    ideal8=next(z for z in grid if z['overlap']==.8 and z['per_photon_eta']==1)
    ideal1=next(z for z in grid if z['overlap']==1 and z['per_photon_eta']==1)
    assert [(z['N'],z['cutoff']) for z in (ideal5,ideal8,ideal1)]==[(6881,9),(2437,5),(1413,4)]
    out={"status":"PASS","correction":"Earlier claimed globally minimal s=0 N=20333,k=16 is FALSE; N=19427,k=15 works, and all smaller N are checked.",
         "source_probability_coefficients":{"W33":[17496,52488,34992],"dual":[3376,1328,-2048],"denominator":DEN},
         "scenarios":grid,
         "limitations":"Independent registered triple survival eta^3 and hypothesis-independent false-event beta only. Source efficiency, mode-dependent losses, correlated dark counts, detector drift, and adversarial calibration absent."}
    print(json.dumps(out,indent=2))
    return out

if __name__=="__main__":main()
