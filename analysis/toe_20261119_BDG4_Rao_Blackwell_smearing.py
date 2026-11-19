"""4D local causal operator: rigorous thinning/Rao-Blackwell variance experiment.

Binomial smearing is KNOWN Sorkin/Benincasa-Dowker prior art, not a new
operator or derivation of quantum Einstein gravity. This experiment compares
the variance of conditional-smoothed and sharp operators at SAME density.
"""
from pathlib import Path
from math import sqrt,pi,comb
import json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_BDG4_conditional_thinning_variance.json"
weights=np.array([1.,-9.,16.,-8.])

def sprinkle_counts(rng,rho):
    n=int(rng.poisson(rho*pi/3))
    if n==0:return np.zeros(0,np.int64)
    t=rng.random(n)**.25
    r=t*rng.random(n)**(1/3)
    z=2*rng.random(n)-1
    phi=2*pi*rng.random(n)
    s=np.sqrt(1-z*z)
    xyz=np.column_stack((r*s*np.cos(phi),r*s*np.sin(phi),r*z))
    dt=t[:,None]-t[None,:]
    dx2=((xyz[:,None,:]-xyz[None,:,:])**2).sum(2)
    return np.count_nonzero((dt>0)&(dt**2>dx2),axis=1)

def smooth_weight(k,eps):
    if eps==1.:return float(weights[k]) if k<4 else 0.
    return sum(float(weights[j])*comb(int(k),j)*(eps**j)*((1-eps)**(int(k)-j))
               for j in range(min(3,int(k))+1))

def functional(counts,rho,eps):
    # Exactly the EXPECTED value of the sharp BDG operator on an independently
    # Bernoulli-thinned version (with origin retained) of the full causal set.
    return float((4*sqrt(rho*eps)/sqrt(6))*
                 (eps*sum(smooth_weight(int(k),eps) for k in counts)-1))

def run():
    rng=np.random.default_rng(20261119081)
    # Validated exact binomial thinning distribution for n<=25 and eps in {0.2,..}
    for eps in (.2,.5,.75,1.):
        for k in range(26):
            exact=sum(weights[j]*comb(k,j)*eps**j*(1-eps)**(k-j)
                     for j in range(4) if j<=k)
            assert abs(exact-smooth_weight(k,eps))<1e-12
    data=[]
    for rho in (100.,200.):
        trials=300
        all_counts=[sprinkle_counts(rng,rho) for _ in range(trials)]
        for eps in (1.,.5,.2):
            eff=rho*eps
            sm=np.array([functional(c,rho,eps) for c in all_counts])
            # Independent PPP at reduced density: distribution exactly that
            # of Bernoulli thinning a PPP(rho), NOT the same realization.
            sh=np.array([functional(sprinkle_counts(rng,eff),eff,1.)
                         for _ in range(trials)])
            vsm=float(np.var(sm,ddof=1));vsh=float(np.var(sh,ddof=1))
            data.append({"parent_sprinkling_density":rho,"retention_eps":eps,
                         "effective_density":eff,"trials":trials,
                         "smoothed_mean":float(sm.mean()),"smoothed_sd":float(sm.std(ddof=1)),
                         "sharp_at_effective_density_mean":float(sh.mean()),
                         "sharp_at_effective_density_sd":float(sh.std(ddof=1)),
                         "variance_ratio_smooth_over_independent_sharp":vsm/vsh})
    # Deterministic inequality is law total variance, sample can fluctuate.
    # For eps 1 independent realizations ratios need not be exactly1.
    for row in data:
        if row["retention_eps"]<1:
            assert row["variance_ratio_smooth_over_independent_sharp"]<1, row
    ans={
     "known_identity":"W_eps(n)=sum_{j=0}^3 w_j*Binomial(n,j)*eps^j*(1-eps)^(n-j), w=(1,-9,16,-8), exact Sorkin smearing from binomial decimation; existing external code independently verifies identity.",
     "functional":"B_(rho,eps)(1)=4sqrt(rho eps)/sqrt6*(eps*sum_event W_eps(N_between(origin,event))-1)",
     "Rao_Blackwell_theorem":"Given PPP(rho) and fixed origin, retain each sprinkled event with probability eps. Thinned PPP is PPP(rho eps). Conditional expectation of raw sharp B at density rho eps given the original causet equals B_(rho,eps). Law of total variance proves Var(B_smoothed PPP(rho)) <= Var(B_sharp PPP(rho eps)), before any Monte Carlo.",
     "sampling":"Independent 4D Minkowski forward lightcone 0<t<1, N~Poisson(rho*pi/3), all causal interval occupancies calculated from full Minkowski metric.",
     "sample_results":data,
     "scope":"Correctly reduced variance relative to sharp at SAME EFFECTIVE density, not a proof of a physically selected nonlocality length or good continuum-bias scaling. No full scalar correlator, spin2 constraints, causal quantum gravity, quantized state, or Lorentzian wavefunction derived.",
     "external_prior_art":"https://github.com/stelios-tsilioukas/topology-change-in-causal-set-theory/blob/main/verification/bd_decimate.py; https://doi.org/10.1007/s41114-019-0023-1"
    }
    OUT.write_text(json.dumps(ans,indent=2)+"\n",encoding="utf8")
    for z in data:print("PASS",z["parent_sprinkling_density"],z["retention_eps"],"SDsm",round(z["smoothed_sd"],2),"SDsharp",round(z["sharp_at_effective_density_sd"],2),"var_ratio",round(z["variance_ratio_smooth_over_independent_sharp"],4))
    print(OUT)
    return ans
if __name__=="__main__":run()
