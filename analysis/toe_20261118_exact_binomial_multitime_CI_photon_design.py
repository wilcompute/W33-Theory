"""Exact one-sided binomial lower confidence bounds for the 2026
Beyer three-time-memory witness design gamma=.96 p=.45 eta=.95.

The resulting certificate is statistical DESIGN POINT only, not
observed photons, confidence under optional stopping, or a reconstructed
physical process tensor. Each setting uses IID accepted ±1 outcomes
and complete independent calibration of preparation and detector bias.
"""
from pathlib import Path
import math,json
from scipy.stats import beta,binom
ROOT=Path(__file__).resolve().parents[1]
ALPHA=.01
gamma=.96
eta=.95

def cp_one_sided_lower(n,k,alpha=ALPHA/3):
    return 0. if k==0 else float(beta.ppf(alpha,k,n-k+1))

def evaluate(n):
    # Deterministic design-point integer outcomes; counts selected to
    # match gamma=.96 and eta=.95 as closely as attainable.
    kg=round(n*(1+gamma)/2)
    ke=round(n*(1+eta)/2)
    pg=cp_one_sided_lower(n,kg)
    pe=cp_one_sided_lower(n,ke)
    g_lower=2*pg-1
    e_lower=2*pe-1
    if e_lower<0:
        raise ValueError("Not in the high-visibility regime")
    wu=2*math.sqrt(1-e_lower*e_lower)-g_lower
    return dict(n_per_setting=n,success_counts=[kg,ke,ke],
                one_sided_lower_Z_expectation=[g_lower,e_lower,e_lower],
                corrected_upper_bound_W3=wu,
                certificate_at_99pct_confidence=wu<0)

def run():
    threshold=(1-math.sqrt(1-gamma))/2
    assert .45>=threshold
    checks=[evaluate(n) for n in (400,420,450,500,750,3859)]
    s400,s420,s450,s500,s750,s3859=checks
    assert s400["corrected_upper_bound_W3"]>0
    assert s450["corrected_upper_bound_W3"]<-.02
    assert s450["n_per_setting"]*3==1350
    # Monotone in binomial counts k at fixed n, despite rounding
    # creating small nonmonotonicities across n.
    n=450;kg,ke,_=s450["success_counts"]
    ggood=2*cp_one_sided_lower(n,kg)-1
    gbad=2*cp_one_sided_lower(n,kg-1)-1
    assert ggood>gbad
    exact_null_bound_pgamma=float(binom.cdf(kg-1,n,(1+gamma)/2))
    out=dict(status="PASS",confidence=1-ALPHA,
        calibrated_design_parameters=dict(gamma=gamma,p=.45,eta2=eta,eta3=eta,
                                          pairwise_classical_p_threshold=threshold),
        proposed_fixed_stopping_n_per_setting=450,
        total_proposed_accepted_trials=1350,
        proposed_design_point_observations=s450,
        comparison_to_previous_uniform_Hoeffding_design=dict(n_per_setting=3859,
                                                              total=11577),
        rows=checks,
        certificate_definition="Three independent fixed-n Bernoulli settings. Each ±1 observable expectation theta=2p-1 has exact one-sided Clopper-Pearson lower limit L_i=2 BetaQuantile(alpha/3;k_i,n_i-k_i+1)-1. Bonferroni yields joint >=99% coverage. Since sqrt(1-e²) decreases with e in [0,1], W3<=sqrt(1-L_eta2²)+sqrt(1-L_eta3²)-L_gamma. Negative bound certifies the specified triple witness.",
        is_design_point_only=True,
        statistical_power_not_computed=True,
        detector_and_heralding_bias_not_calibrated=True,
        optional_stopping_not_allowed=True,
        proof_of_true_joint_three_time_process_missing=True,
        caution="The confidence statement is conditional on actual fixed-n accepted IID or otherwise rigorously binomial-dominated measurements, independent preparations/instruments and fair calibrated heralding; simulated rounded means cannot be treated as observed results. Pairwise-classical decompositions are model-verified by previous code, not empirically inferred merely from these three means.",
        literature="Beyer et al, Observation of Genuine Multi-Time Quantum Memory (2026), arXiv:2611.17268, gives the witness and pairwise-classical theorem. Clopper-Pearson exact inversion of binomial tails is classical statistics.",
        unused_exact_model_tail_diagnostic=exact_null_bound_pgamma)
    file=ROOT/"data/toe_20261118_exact_binomial_multitime_CI_photon_design.json"
    file.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS 99% exact one-sided CP design: n=450 each, success=[441,439,439], W3 upper",s450["corrected_upper_bound_W3"])
    return out
if __name__=="__main__":run()
