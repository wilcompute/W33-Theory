"""TOE95 MZI calibration shot budget and randomized 40-setting control schedule.

Uses exact per-probe binomial confidence bounds under IID trusted
calibration shots. A rank-one-projective measurement premise then
converts basis-state wrong-output probability to a conservative
worst-case spectral operator bound. This is NOT device tomography,
lab data or a certificate against arbitrary SPAM/adversarial loss.
"""
from __future__ import annotations
import json,math
from pathlib import Path
from analysis.w33_20261015_toe94_mzi_drift import witness
ROOT=Path(__file__).resolve().parents[1]
BASES=40
PROBES=4*BASES
ALPHA=.001

def per_probe_zero_failure_upper(shots):
    # P(no wrong output)^shots = (1-p)^shots; union bound 160 probes.
    return 1-(ALPHA/PROBES)**(1/shots)

def spectral_matching_upper(p):
    # For ideal and actual rank-one PVM P,Q, the basis-state mismatch
    # probability ||P-Q||_op^2 is p. Each joint rank-one term differs
    # by at most 2 sqrt(p), four terms per setting -> 8 sqrt(p).
    return min(1.,.4+8*math.sqrt(p))

def certified_shots_for_ceiling(target):
    assert target>.4
    p=((target-.4)/8)**2
    return math.ceil(math.log(ALPHA/PROBES)/math.log1p(-p))

def certificate():
    # Coprime jump visits every tetrad exactly once and disperses
    # adjacent 40-setting calibrations across the measurement index.
    order=[(17*k)%40 for k in range(40)]
    assert len(set(order))==40
    records=[]
    for shots in (2048,16384,100000,500000):
        p=per_probe_zero_failure_upper(shots)
        records.append({'shots_per_ideal_basis_probe':shots,
            'total_40_setting_4_probe_shots':PROBES*shots,
            'zero_wrong_output_union_bound_per_probe_probability_upper':round(p,12),
            'conservative_rank_one_projector_based_separable_ceiling':round(spectral_matching_upper(p),12)})
    target=.44
    need=certified_shots_for_ceiling(target)
    assert spectral_matching_upper(per_probe_zero_failure_upper(need))<=target+1e-10
    assert spectral_matching_upper(per_probe_zero_failure_upper(need-1))>target-1e-10
    drift=[witness(.95,d) for d in (0.,.005,.01)]
    assert drift[-1]['trusted_no_background_separable_upper']>.4
    return {
      'number_of_tetrad_settings':BASES,'local_basis_probe_states_per_setting':4,
      'simulated_setting_schedule':order,
      'per_round':'Choose a uniformly randomized 40-setting order after sealed heralds; perform four independently prepared ideal basis-state calibration probes per setting, measure all including loss/no-click, and record raw wrong-output counts. Coprime 17-step order is a deterministic audit example only.',
      'union_failure_probability':ALPHA,
      'assumptions':'Each probe is trusted and pure, each calibrated receiver is a rank-one 4-output PVM in C^4, all calibration shots are independent Bernoulli, wrong output count is zero for the bound, and every setting remains stable until use.',
      'confidence_formula':'For 160 independent probe types, simultaneous per-probe wrong-output probability is <=1-(alpha/160)^(1/n) at confidence >=1-alpha when all n trials per probe have no wrong outputs.',
      'projective_operator_bound':'If each pure ideal basis probe returns its intended outcome with probability >=1-p for a trusted rank-one projective measurement, ||P_i-tilde P_i||_op<=sqrt(p). Joint Alice/Bob matched-operator perturbation <=8 sqrt(p); separable ceiling <=min(1,0.4+8sqrt(p)).',
      'zero_wrong_output_budget':records,
      'shots_per_probe_to_certify_separable_ceiling_at_most_0_44':need,
      'total_shots_for_that_conservative_target':need*PROBES,
      'full_40_analyzer_model_drift_census':drift,
      'engineering_limit':'The 8sqrt(p) bound is intentionally very loose. Real calibration needs informationally complete cross-setting probes, measured insertion loss, source SPAM, phase drift covariance, detector dead time, independent heralds and statistically validated stability.'
    }
if __name__=='__main__':
    z=certificate()
    print('TOE95 CALIBRATION',z['total_shots_for_that_conservative_target'])
    (ROOT/'data/w33_20261017_toe95_calibration.json').write_text(json.dumps(z,sort_keys=True,indent=2)+'\n')
