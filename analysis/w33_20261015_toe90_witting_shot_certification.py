"""TOE90 operational four-outcome QKD tomography witness shot calculator.

Noise model: EACH Alice/Bob detector reports true symbol with 1-e and
one of other three symbols uniformly with probability e. The same-basis
match statistic is a Bernoulli observable only under independent iid
uniformly randomized tetrad choices and stationary events. Strictly
device-trusted entanglement witness; NOT a QKD security proof.
"""
from __future__ import annotations
import json
from fractions import Fraction
from scipy.stats import binom
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT, calculate

def certificate():
    d=calculate()
    assert d["entanglement_witness"]["separable_joint_matching_upper_bound"]=="2/5"
    e=Fraction(1,50)  # declared 2% per-party ternary wrong-symbol model
    # p(obs Alice=Bob | true agree) vs (true disagree).
    same=(1-e)**2+e**2/3
    different=2*e*(1-e)/3+2*e**2/9
    assert same>different
    null=Fraction(2,5)
    v=Fraction(1,4)
    alternative=(1+3*v)/4
    null_observed=different+(same-different)*null
    alternative_observed=different+(same-different)*alternative
    assert null_observed<alternative_observed
    n=8192
    alpha=1e-3
    threshold=next(k for k in range(n+1) if binom.sf(k-1,n,float(null_observed))<=alpha)
    tail=float(binom.sf(threshold-1,n,float(null_observed)))
    power=float(binom.sf(threshold-1,n,float(alternative_observed)))
    assert tail<=alpha and power>0.999
    # The 40-basis protocol's full measurement setting can be selected
    # secretly and independently.  Revealing the setting AFTER each run
    # does not make an EB witness device-independent.
    return {
       "source":"Witting 40 projective rays and 40 contexts (Vlasov arXiv:2503.18431) plus TOE90 2-design proof.",
       "device_model":"two trusted ideal ququart measurements with independent known symmetric four-outcome classical readout confusion",
       "per_side_readout_error":str(e),
       "true_agreement_to_reported_agreement":str(same),
       "true_disagreement_to_reported_agreement":str(different),
       "separable_true_match_bound":str(null),
       "isotropic_visibility_model":str(v),
       "coherent_isotropic_true_match":str(alternative),
       "calibrated_separable_reported_match_upper_bound":str(null_observed),
       "calibrated_isotropic_reported_match":str(alternative_observed),
       "n_independent_accepted_pairs":n,
       "uniform_secret_Witting_basis_per_pair":True,
       "reject_separability_at_reported_match_count_at_least":threshold,
       "exact_iid_binomial_false_positive_probability":round(tail,12),
       "exact_iid_binomial_model_detection_power":round(power,12),
       "limitations":"Hypothetical IID detector-calibration model, no basis-dependent loss, no source drift, no SPAM deviations beyond declared confusion, no device independence, no finite-key QKD security or privacy amplification theorem."
    }
if __name__=="__main__":
    d=certificate()
    p=ROOT/"data/w33_20261015_toe90_witting_shot_certification.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("TOE90 SHOTS",d["reject_separability_at_reported_match_count_at_least"],
          d["exact_iid_binomial_false_positive_probability"],
          d["exact_iid_binomial_model_detection_power"])
