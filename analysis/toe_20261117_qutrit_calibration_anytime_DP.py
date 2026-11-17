"""Finite-horizon exact (not Monte Carlo) anytime-valid qutrit MUB
witness with bounded measurement-operator errors and setting leakage.

Trusted 4-MUB calibrated effects satisfy W_actual=W_ideal+DeltaW,
operator norm ||DeltaW||<=epsilon on 9D joint input space at every
trial conditional on the past. Setting leakage to prep conditional
distribution is bounded by total variation beta, conservatively
increasing separable null by beta.

Then p0 <= a(1+t)/4 +epsilon+beta; source model p1 >=
 a(qZ+3tqN)/4 -epsilon. The nonIID sequential likelihood factor is
e_i=(p1/p0)^X ((1-p1)/(1-p0))^(1-X) for p1>p0, with p0 and p1
fixed before each trial. Under conditional null success probability
<=p0, E[e_i|past]<=1. Ville gives Pr(sup e_total>=1/alpha)<=alpha.

For a pre-declared constant pair p0,p1 we compute EXACT crossing
probabilities under Bernoulli(p0) and Bernoulli(p1) over 100/200/500
trials via absorbing binomial dynamic programming. No experiment.
"""
from pathlib import Path
import json,math,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_qutrit_calibrated_loss_witness import witness
from toe_20261117_memory_2026_real_reference_qutrit import dkl
OUT=ROOT/"data"/"toe_20261117_qutrit_operator_calibration_anytime_eprocess.json"
def scenario(epsilon,beta=0,eta=.902,nmem=2,c=.995,router=.995):
    ref=witness(c=c,eta_mem=eta,n_mem=nmem,router=router)
    p0=ref["calibrated_separable_upper"]+epsilon+beta
    p1=ref["expected_entangled_match"]-epsilon
    gap=p1-p0
    n_info=math.log(100)/dkl(p1,p0) if gap>0 else None
    return {"epsilon_operator_norm_bound":epsilon,"beta_setting_leak_TV":beta,
      "max_separable_success_p0":p0,"min_entangled_source_success_p1":p1,
      "robust_gap":gap,"robust_certification_possible":gap>0,
      "oracle_log_evalue_100_information_n":n_info,
      "prior_probability_baseline_psep":ref["calibrated_separable_upper"],
      "prior_probability_baseline_pent":ref["expected_entangled_match"]}
def anytime_dp(p0,p1,steps=200,alpha=.01,truth=None):
    assert 0<p0<p1<1 and steps>=1
    if truth is None:truth=p0
    log_success=math.log(p1/p0)
    log_fail=math.log((1-p1)/(1-p0))
    cutoff=math.log(1/alpha)
    safe={0:1.0}
    crossed=0.
    at={}
    for t in range(1,steps+1):
        new={}
        for k,pr in safe.items():
            for x,weight in ((0,1-truth),(1,truth)):
                m=k+x
                w=pr*weight
                log_e=m*log_success+(t-m)*log_fail
                if log_e>=cutoff-1e-12:
                    crossed+=w
                else:
                    new[m]=new.get(m,0.)+w
        safe=new
        if t in (25,50,75,100,200,500):
            at[t]={"probability_crossed_at_any_time":crossed,"noncrossing_mass":sum(safe.values())}
        assert abs(crossed+sum(safe.values())-1)<2e-12
    return {"horizon":steps,"truth_success_probability":truth,
      "p0_predeclared":p0,"p1_predeclared":p1,
      "crossing_threshold":1/alpha,"ever_crossed_prob":crossed,
      "crossing_by_horizon":at}
def verify():
    ref=witness()
    baseline_gap=ref["expected_entangled_match"]-ref["calibrated_separable_upper"]
    epsmax=baseline_gap/2
    assert .09<epsmax<.1
    rows=[scenario(e, beta) for e,beta in ((0,0),(.01,.002),(.03,.01),(.05,.015),(.08,.02),(.09,.03),(.1,0))]
    assert rows[0]["robust_certification_possible"]
    assert rows[2]["robust_certification_possible"]
    assert not rows[-1]["robust_certification_possible"]
    assert not rows[-2]["robust_certification_possible"]
    # Exact Bernoulli dynamic programming, not pseudorandom tests.
    null=anytime_dp(rows[0]["max_separable_success_p0"],
                     rows[0]["min_entangled_source_success_p1"],steps=500)
    alternate=anytime_dp(rows[0]["max_separable_success_p0"],
                     rows[0]["min_entangled_source_success_p1"],steps=500,
                     truth=rows[0]["min_entangled_source_success_p1"])
    assert null["ever_crossed_prob"]<=.0100000000001
    assert alternate["ever_crossed_prob"]>.99
    # Test more conservative measurement operator bound epsilon=.03
    row=rows[2]
    nullpert=anytime_dp(row["max_separable_success_p0"],
                  row["min_entangled_source_success_p1"],steps=500)
    altpert=anytime_dp(row["max_separable_success_p0"],
                  row["min_entangled_source_success_p1"],steps=500,
                  truth=row["min_entangled_source_success_p1"])
    assert nullpert["ever_crossed_prob"]<=.0100000000001
    assert altpert["ever_crossed_prob"]>.75
    return {"status":"PASS_QUTRIT_OPERATOR_NORM_CALIBRATION_ROBUST_ANYTIME_EPROCESS",
     "operator_effect_theorem":"If averaged matched-click effect differs from ideal a-weighted MUB operator by operator norm <=epsilon for all states and conditional histories, |Tr rho DeltaW|<=epsilon. Setting leakage TV<=beta increases separable null by beta. Robust gap if 2epsilon+beta<p_ent_ideal-p_sep_ideal.",
     "original_ideal_gap":baseline_gap,"largest_symmetric_epsilon_at_zero_leakage":epsmax,
     "calibration_scenarios":rows,
     "exact_DP_no_noise_null":null,"exact_DP_no_noise_alternative":alternate,
     "exact_DP_eps03_beta01_null":nullpert,"exact_DP_eps03_beta01_alternative":altpert,
     "nonIID_proof":"For each trial, conditional null p<=p0 and predictable p1>p0: E[(p1/p0)^X((1-p1)/(1-p0))^(1-X)|past]<=1. Product is nonnegative supermartingale. Ville bound holds under arbitrary correlated/adaptive null with certified per-trial bounds.",
     "scope":"Mathematically exact trusted POVM+sequential inference under operator-norm and setting-leakage premises. The premises are not experimentally calibrated and no photon data were taken."}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["largest_symmetric_epsilon_at_zero_leakage"],
          z["exact_DP_no_noise_null"]["ever_crossed_prob"],
          z["exact_DP_no_noise_alternative"]["ever_crossed_prob"])
