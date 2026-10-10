"""Round31: repeated qutrit check readout and verified-cat acceptance budget.
Exactly solvable independent classical report-flip model.
Physical quantum faults and time-varying syndrome are NOT represented.
"""
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe31_cat_detector_budget.json'
def run():
 gauges=[8]*80+[4]*79
 nchecks=len(gauges);nv=sum(w-1 for w in gauges)
 assert nchecks==159 and nv==797
 results=[]
 for p in (.0001,.001,.005,.01,.02):
  full=(1-p)**nv
  per_check=sum(1/(1-p)**(w-1) for w in gauges)
  majority_wrong=1.5*p*p-.5*p**3
  majority_erase=1.5*p*p*(1-p)
  probability_any_wrong_159=1-(1-majority_wrong)**159
  probability_any_erase_159=1-(1-majority_erase)**159
  data=dict(p=p,full_round_all_verifiers_clean_probability=full,
   mean_global_rounds_until_all_clean=1/full,
   mean_per_check_prep_attempts_for_159_accepted_checks=per_check,
   single_readout_any_check_corrupt_probability=1-(1-p)**159,
   three_round_majority_one_check_wrong_probability=majority_wrong,
   three_round_majority_one_check_no_strict_majority_probability=majority_erase,
   three_round_any_wrong_check_probability=probability_any_wrong_159,
   three_round_any_erased_check_probability=probability_any_erase_159)
  results.append(data)
  print('CAT BUDGET',p,'global attempts',round(1/full,3),'percheck attempts',round(per_check,3),
        'majority any wrong',round(probability_any_wrong_159,6),flush=True)
 assert results[1]['mean_global_rounds_until_all_clean']>2
 assert results[-1]['mean_global_rounds_until_all_clean']>1e6
 # Qutrit syndrome 0,0,1 where a late true data error switches from0
 # to1 after round2: majority will report0, despite NO readout noise.
 syndrome_history=[0,0,1]
 assert max(set(syndrome_history),key=syndrome_history.count)==0
 rec=dict(status='PASS',base_code='[[160,1,8]]_3',
  verification_measurements_per_extraction_attempt=nv,
  stabilizer_outcomes_per_round=nchecks,
  data_interactions_per_round=956,
  exact_model='Independent symmetric ternary report flips: with probability p a true ternary outcome is shifted by +1 or -1 equiprobably. Verifier acceptance model assumes every true verifier syndrome is zero; classical flips alone reject attempts. Does NOT represent quantum gate faults.',
  global_repeat_vs_per_check_reprep='If requiring ALL 797 verifier outcomes to be correctly reported in a single global batch, acceptance probability (1-p)^797. Expected global batches 1/(1-p)^797. Independent local preparation/retry of each check instead requires sum_{checks}(1-p)^-(weight-1) preparation attempts in expectation; must not infer this is necessarily a physically schedulable full FT protocol.',
  strict_majority3_wrong='For unchanged ternary syndrome read 3 independent times, strict majority returns incorrect value with probability (3/2)p² -(1/2)p³. Three distinct reports yield no strict majority, probability (3/2)p²(1-p). Neither counts data faults propagated during rounds.',
  time_varying_syndrome_counterexample='Even with noiseless measurement and true syndrome history [0,0,1], majority returns0 while current syndrome is1. Repeated readouts require a space-time detector-history decoder for evolving errors; raw majority cannot be treated as a fault-tolerant syndrome decoder.',
  sample_probabilities=results,
  scope='This is a precise resource and readout model to audit Round30, not a complete physical circuit-level noise simulator, verified GHZ scheme, decoder threshold, or experimental calibration.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 return rec
if __name__=='__main__':run()
