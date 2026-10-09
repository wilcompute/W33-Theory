"""Pre-registered detector-glitch certification plan: independent
Bernoulli glitch flags in a reference calibration then prospective
N-shot optical test allowing <=m arbitrary corrupted weighted readings.

With zero glitches in M independent calibration shots, exact one-sided
Clopper-Pearson p_upper=1-alpha_cal**(1/M). The prospective binomial
count tail at N,m is bounded by alpha_count if p<=p_upper. Existing
clipped randomized treatment test has alpha_test conditional on count.
Therefore TOTAL unconditional false-rejection probability for the
calibration+test procedure <= alpha_cal+alpha_count+alpha_test.
"""
from pathlib import Path
import json,math
from scipy.stats import binom
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
def certificate():
 N=240000;m=40
 ac=0.001;ag=0.001;at=0.008
 assert ac+ag+at==.01
 pstar=brentq(lambda p:binom.sf(m,N,p)-ag,1e-10,.001,xtol=1e-16)
 M_min=math.ceil(math.log(ac)/math.log1p(-pstar))
 rows=[]
 for M in (25000,50000,75000,100000,250000,1000000,M_min):
  pu=-math.expm1(math.log(ac)/M)
  tail=binom.sf(m,N,pu)
  rows.append(dict(calibration_shots=M,observed_calibration_glitches=0,
      exact_p_upper99p9=pu,worst_prospective_count_tail=tail,
      three_component_aggregate_fpr_upper=ac+tail+at,
      count_budget_approved=bool(tail<=ag)))
 assert rows[-1]['count_budget_approved']
 assert binom.sf(m,N,-math.expm1(math.log(ac)/(M_min-1)))>ag
 # glitched fractions / the protected 0.008 test threshold
 bound=2*m*2.
 return dict(status='PASS',
    target_optical_shots=N,max_unbounded_glitches=m,
    calibration_confidence=1-ac,calibration_failure_allocation=ac,
    future_count_exceedance_allocation=ag,
    randomized_clipped_test_failure_allocation=at,
    combined_false_positive_limit=ac+ag+at,
    largest_certifiable_single_shot_bernoulli_glitch_probability=pstar,
    minimum_zero_glitch_calibration_samples=M_min,
    independent_calibration_designs=rows,
    deterministic_clipped_score_penalty_for_40_outliers_at_T2=bound,
    statistical_theorem='Given independent identically distributed per-shot Bernoulli glitch flags with fixed unknown rate p, zero flags among M calibration shots is an exact one-sided (1-alpha_cal) event of p<=1-alpha_cal^(1/M). Conditional on this bound, prospective count X~Binomial(N,p) obeys P(X>m)<=P(Bin(N,p_upper)>m). Combining the prior conditional clipped sharp-null randomization test at alpha_test via a union bound gives a joint calibration-and-test Type-I error <=alpha_cal+alpha_count+alpha_test. Apply the optical test only after observing no calibration glitches.',
    strong_limitation='The result is NOT valid for correlated glitches, adversarial bursts, unobservable electronic corruption not captured by calibration labels, instrument drift between calibration and experimental runs, compromised Q-weights, or systematic good-shot detector-reference mismatch beyond d. A hardware watchdog or burst model must separately address these.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_photonic_glitch_calibration_plan.json').write_text(json.dumps(d,indent=2)+'\n')
 print('CAL',d['minimum_zero_glitch_calibration_samples'],d['largest_certifiable_single_shot_bernoulli_glitch_probability'],[(x['calibration_shots'],x['worst_prospective_count_tail']) for x in d['independent_calibration_designs']])
