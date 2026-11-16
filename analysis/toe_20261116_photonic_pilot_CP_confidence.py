"""Make the previously assumed photonic rail-population envelope an explicit
independent pilot-calibration sample with simultaneous exact binomial
Clopper-Pearson upper bounds and full 99% alpha spending.

All simulated preparation/counts are SYNTHETIC, not hardware data.
A fixed pilot n is chosen beforehand, avoiding optional-stopping bias.
"""
import json,sys,math
from pathlib import Path
import numpy as np
from scipy.stats import beta
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_photonic_weighted_rail_allocation import optimize
OUT=ROOT/"data"/"toe_20261116_photonic_pilot_certified_envelope_99pct.json"

def run(npilot=50000):
    prior=json.loads((ROOT/"data"/"toe_20261115_direct_witness_contrast_calibration.json").read_text())
    R=float(prior["sample_weight_range"]);eps=.01
    alpha_pilot=.001;alpha_contrast=.0015;alpha_parity=.0025;alpha_witness=.005
    assert alpha_pilot+alpha_contrast+alpha_parity+alpha_witness==.01
    pop=np.array([.48]+[.04/14]*14+[.48],dtype=float)
    assert abs(pop.sum()-1)<1e-12
    rng=np.random.default_rng(20261116)
    counts=rng.multinomial(npilot,pop)
    assert counts.sum()==npilot
    u=[float(beta.ppf(1-alpha_pilot/16,int(c)+1,npilot-int(c))) if c<npilot else 1.0
       for c in counts]
    assert len(u)==16 and sum(u)>1
    allocated=optimize(u,R,eps,alpha_contrast)
    assert allocated["aggregate_contrast_calibration_radius"]<=eps*(1+1e-12)
    pilot_checks=[{"rail":j,"synthetic_true_population":float(pop[j]),
                   "pilot_count":int(counts[j]),"one_sided_Clopper_Pearson_upper":u[j],
                   "synthetic_true_value_below_upper":bool(pop[j]<=u[j])}
                  for j in range(16)]
    assert all(x["synthetic_true_value_below_upper"] for x in pilot_checks)
    # The preparation envelope is random but independently estimated.
    # Union bound: 16 simultaneous one-sided CP intervals each alpha_p/16.
    # A separate conditional Hoeffding calibration then covers weighted
    # contrast bias up to eps with probability >=1-alpha_contrast.
    nominal_bias=.002*sum(u) # separate synthetic model bound, NOT observed.
    Fhat=prior["observed_synthetic_witness_fidelity"]
    Fstat=prior["statistical_half_width"]
    parity=prior["parity_flip_error_radius"]/(1-sum(prior["parity_flip_estimates"]))
    F99=Fhat-Fstat-.5*(nominal_bias+eps)-parity
    total= npilot+allocated["accepted_total_rail_calibration"]+2*prior["accepted_parity_calibrations_each"]
    old=16*math.ceil(R*R*math.log(2*16/.0025)/(2*eps**2))+2*prior["accepted_parity_calibrations_each"]
    assert old==1137384
    result={
      "status":"EXACT_BINOMIAL_PILOT_CERTIFIED_OCCUPANCY_WEIGHTED_CALIBRATION",
      "synthetic_not_hardware":True,
      "pilot_sample_size_prespecified":npilot,
      "pilot_rng_seed":20261116,
      "pilot_multinomial_counts":list(map(int,counts)),
      "pilot_rail_checks":pilot_checks,
      "exact_confidence_method":"One-sided Clopper-Pearson Beta(k+1, n-k) quantile 1-alpha_pilot/16; 16-rail Bonferroni.",
      "joint_failure_budget":{"pilot_occupancy":alpha_pilot,"contrast_calibration":alpha_contrast,
                            "parity_rates":alpha_parity,"five_witness_settings":alpha_witness},
      "conservative_upper_envelope":u,
      "pilot_upper_envelope_weighted_optimizer":allocated,
      "accepted_pilot_preparations":npilot,
      "accepted_rail_calibrations":allocated["accepted_total_rail_calibration"],
      "accepted_parity_reference_preparations":2*prior["accepted_parity_calibrations_each"],
      "total_synthetic_99pct_accepted_shots_including_pilot":int(total),
      "equal16_no_pilot_reference_99pct_accepted_shots":old,
      "net_fraction_saved_including_pilot":float(1-total/old),
      "assumed_nominal_contrast_mismatch_per_rail":.002,
      "synthetic_witness_99pct_lower_bound":F99,
      "scope":"Independent pilot bound is demonstrated ONLY using a synthetic multinomial draw. The same pilot is NOT reused for signal/contrast fits. The actual apparatus must justify i.i.d. known-rail preparation, binomial sampling, detector stationarity and the separate <=0.002 mismatch assumption. No physical measurements, no drift guarantee, no real fidelity confidence statement.",
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    return result

if __name__=="__main__":
    r=run()
    print("PASS",r["status"],"shots incl pilot",r["total_synthetic_99pct_accepted_shots_including_pilot"],
          "99 lower",r["synthetic_witness_99pct_lower_bound"])
