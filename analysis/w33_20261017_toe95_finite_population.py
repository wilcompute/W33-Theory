"""TOE95 non-IID, finite-population classical sampling firewall for Witting QKD.

For a fixed, arbitrarily correlated pre-existing binary error pattern,
uniform random assignment of 4096 of 4292 positions to tests allows an
EXACT hypergeometric one-sided bound on remaining 196 errors. This
does not handle quantum phase observables or coherent quantum Eve:
those require an appropriate quantum-sampling/GEAT proof.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
from scipy.stats import hypergeom,beta
ROOT=Path(__file__).resolve().parents[1]
N_TEST=4096
N_KEY=196
N=N_TEST+N_KEY
EPS=.001

def upper_remaining(k):
    assert 0<=k<=N_TEST
    low,high=k,N
    # Find largest total error count K for which observing <=k test
    # errors is not yet an epsilon-rare event under random sampling.
    while low<high:
        mid=(low+high+1)//2
        if hypergeom.cdf(k,N,mid,N_TEST)>=EPS:low=mid
        else:high=mid-1
    K=low
    assert hypergeom.cdf(k,N,K,N_TEST)>=EPS-1e-12
    if K<N:assert hypergeom.cdf(k,N,K+1,N_TEST)<EPS+1e-12
    return min(N_KEY,K-k),K

def certificate():
    observations=[0,3,7,15,25,40,80]
    rows=[]
    for k in observations:
        max_key,whole=upper_remaining(k)
        iid=float(beta.ppf(1-EPS,k+1,N_TEST-k))
        rows.append({
          'observed_test_errors':k,'worst_total_errors_at_confidence':whole,
          'remaining_key_errors_upper':max_key,
          'remaining_key_error_fraction_upper':round(max_key/N_KEY,12),
          'IID_Clopper_Pearson_rate_for_comparison_only':round(iid,12)
        })
    assert [r['remaining_key_errors_upper'] for r in rows]==[2,3,4,5,6,8,11]
    # Attack when test locations are leaked before Eve fixes a pattern:
    # put ALL errors in the key positions. The test sample is perfectly
    # clean although every key round is wrong. A uniformly hidden
    # test subset meets that pattern with tiny probability.
    log_p=(-math.lgamma(N+1)+math.lgamma(N_KEY+1)+
           math.lgamma(N_TEST+1))/math.log(10)
    return {
      'population_rounds':N,'test_positions':N_TEST,
      'key_positions':N_KEY,'tail_failure':EPS,
      'mathematical_model':'Adversary fixes ANY 0/1 error pattern on all 4292 classical positions before a uniform 4096-position sample is secretly drawn without replacement.',
      'one_sided_confidence_inversion':'Kmax=max{K: Pr[Hypergeom(M=4292,K,n=4096)<=observed k] >= epsilon}; remaining errors <=Kmax-k except on an epsilon event.',
      'rows':rows,
      'nonIID_pattern_independence':'No assumption that error indicators are independent, identically distributed or even stochastic. Random sample assignment must be independent of the fixed error pattern.',
      'fully_leaked_test_schedule_counterexample':{
        'observed_test_errors':0,
        'actual_key_errors':N_KEY,
        'fraction_key_wrong':1,
        'log10_probability_of_no_test_errors_if_positions_were_uniformly_secret':round(log_p,3)
      },
      'quantum_boundary':'This is exact *classical* finite-population sampling only. Complementary-basis phase errors are not jointly pre-existing observable bits in an arbitrary quantum attack. A quantum sampling reduction, complementarity-based proof, or generalized entropy-accumulation min-tradeoff function is still required before composable Witting QKD.',
      'references':[
        'Metger and Renner, Security of quantum key distribution from generalised entropy accumulation, Nature Communications (2023), https://www.nature.com/articles/s41467-023-40920-8',
        'Kamin et al., Finite-Size Analysis of Prepare-and-Measure and Decoy-State QKD via Entropy Accumulation, PRX Quantum 6 020342 (2025)'
      ]
    }
if __name__=='__main__':
    z=certificate()
    print('TOE95 fixed-pattern hypergeometric',[(r['observed_test_errors'],r['remaining_key_errors_upper']) for r in z['rows']])
    (ROOT/'data/w33_20261017_toe95_finite_population.json').write_text(json.dumps(z,sort_keys=True,indent=2)+'\n')
