"""TOE93 event-ready Witting experiment: herald-before-setting and count losses.

Pre-register every source-heralded trial before the secret tetrad is
sampled. Count all failed/no-detection outcomes as non-matches rather
than discarding them. Under ideal trusted POVMs and independent secret
tetrads, *any adaptive separable source* has conditional match <=2/5.
A binomial upper tail remains a valid supermartingale null test.
"""
from __future__ import annotations
import json,random
from scipy.stats import binom
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT
from analysis.w33_20261015_toe93_mzi_bill import certificate as mesh
N=8192
ALPHA=.001
def ledger(v=.95):
    eta=mesh()['pessimistic_two_photon_survival']
    sep=.4
    true=(1+3*v)/4
    observed=eta*true
    threshold=int(binom.isf(ALPHA,N,sep))+1
    assert binom.sf(threshold-1,N,sep)<=ALPHA
    assert binom.sf(threshold-2,N,sep)>ALPHA
    false=float(binom.sf(threshold-1,N,sep))
    power=float(binom.sf(threshold-1,N,observed))
    return {'heralds_committed_before_basis_choice':N,
      'null_separable_per_herald_match_upper':sep,
      'isotropic_visibility_assumed':v,
      'pair_detection_probability_assumed':eta,
      'alternative_match_if_no_loss':true,
      'alternative_per_herald_counting_loss_as_mismatch':round(observed,12),
      'rejection_count_or_higher':threshold,
      'conditional_adaptive_separable_false_alarm_at_most':round(false,12),
      'synthetic_independent_alternative_power':round(power,12),
      'loss_budget_criterion':'eta_pair * (1+3 v)/4 must exceed 2/5 to permit separable-state witness violation under loss-counted-as-mismatch.'}
def attack_control():
    # separable product state: 4 Witting bases have success 1, 36 have 1/3.
    # Outcome-conditioned attacker accepts only matching outcomes while
    # keeping EXACT 1/3 acceptance each basis, per TOE92 attack.
    basis_priors=[1.]*4+[1/3]*36
    accepted_each=[(1/3)/p*p for p in basis_priors]
    assert all(abs(x-1/3)<1e-12 for x in accepted_each)
    accepted_matches=sum(accepted_each)/40
    assert abs(accepted_matches-1/3)<1e-12
    return {'separable_unconditional_match_before_attack':.4,
        'attacker_matched_fraction_given_acceptance':1.,
        'fraction_of_all_precommitted_heralds_accepted_and_matching':1/3,
        'null_test_rejection_inequality':False,
        'lesson':'Even a joint result-informed coincident filter yielding 100% on accepted trials cannot inflate the fraction of ALL previously committed heralds matched when rejected trials count as failures.'}
def certificate():
    report=ledger()
    control=attack_control()
    assert report['synthetic_independent_alternative_power']>.99
    return {
      'finite_state_order':['source emits authenticated unique trial_id and event-ready herald at t0',
                            'commitment log seals herald/expected detector window at t1',
                            'Alice and Bob independently sample secret uniform basis among 40 at t2',
                            'perform basis rotations and photon detection at t3',
                            'record all 16 joint outcomes plus incomplete/no-click/timing failures under original trial_id at t4',
                            'audit hashes and authenticated reveal of settings after detection at t5',
                            'count MATCH among ALL heralded trial IDs; only then perform hypothesis test'],
      'timing_requirement':'t0<t1<t2<t3<t4<t5 verified using independent trusted timestamp/commitment and secure setting RNG; mere software clock timestamps do not certify quantum spacelike separation.',
      'trusted_device_assumptions':'Same 40 projective POVMs per setting, known analyzer behavior, trusted measurement outcomes and source herald, no basis leaks prior to commitment, all heralded trials reported, and no detector-output fabrication.',
      'martingale_null':'With uniform fresh basis chosen after event-ready herald, each adaptive separable conditional source yields Pr(match|past)<=2/5. Uniform-coin coupling bounds N matched heralds by Binomial(N,2/5), even if the source adapts to past trials.',
      'simulated_physical_channel':report,'selected_attacker_control':control,
      'remaining_loopholes':'An attacker could forge herald IDs, influence preselection source, compromise basis RNG, manipulate trusted detector output records, or exploit basis-dependent POVM miscalibration. Neither this code nor timestamp receipts prevent these physically.',
      'scope':'Preregistered protocol and mathematical adversarial thought experiment, not implemented authenticated hardware time stamping or a loophole-free Bell demonstration.'}
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261015_toe93_event_ready_herald.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
 print('HERALD',d['simulated_physical_channel'],flush=True)
