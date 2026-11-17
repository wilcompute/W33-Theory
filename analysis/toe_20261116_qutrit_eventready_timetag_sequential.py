"""Event-ready qutrit hardware acceptance test with asymmetric time-bin routers.

This is a synthetic photon detector model with explicit loss, noise,
settings and sequential e-process. It is NOT an optical experiment.
Every pre-setting-heralded trial is counted: no-click -> Y=0.
Spurious accidental matches are conservatively included in p0
via a calibrated POVM error epsilon; hidden source-side settings
are bounded by setting-selection TV.

Use prior exact four-MUB Bell witness and anytime-valid
Bernoulli test supermartingale, with an alternative q selected
before data collection. Do not optimize q on the same trial.
"""
import sys,math,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_qutrit_anytime_eprocess import eprocess
from toe_20261116_qutrit_temporal_router_loophole import budget
OUT=ROOT/"data"/"toe_20261116_qutrit_eventready_full_timetag_acceptance.json"
ALPHA=.01
def plan(fR=.95,fS=.95,v=.75,sigma=.15,etaR=.9,etaS=.9,
         etaMem=.95,etaPath=.95,epsilon=.01,tv=0.,dark=.0001):
    if not all(0<=a<=1 for a in (fR,fS,v,etaR,etaS,etaMem,etaPath,dark)):
        raise ValueError("probabilities must be in [0,1]")
    if epsilon<0 or tv<0:raise ValueError("bad calibration")
    F=v*(1+2*math.exp(-sigma*sigma))/3+(1-v)/9
    ideal=(1+3*F)/4
    eta=etaR*etaS*etaMem*etaPath*fR*fS
    p=eta*ideal+(1-eta)*dark/3
    p0=.5+epsilon+tv
    kl=(p*math.log(p/p0)+(1-p)*math.log((1-p)/(1-p0))) if p>p0 else 0.
    min_fS=p0/(etaR*etaS*etaMem*etaPath*fR*ideal)
    return {"router_reference":fR,"router_signal":fS,
        "calibrated_pair_detection":eta,"bell_fidelity":F,
        "ideal_matched_probability_given_pair":ideal,
        "accidental_dark_match_probability_when_no_pair":dark/3,
        "expected_gross_click_match":p,"separable_null_upper":p0,
        "has_positive_witness_gap":p>p0,
        "fixed_alternative_KL_per_heralded_trial":kl,
        "KL_expected_trial_scale_log_100_over_D":(math.log(100)/kl if kl>0 else None),
        "required_signal_router_efficiency_at_fixed_reference":min_fS,
        "setting_TV":tv,"POVM_error_epsilon":epsilon,
        "measurement_bases":"one uniform secret basis from Z,F3,D1*F3,D2*F3 chosen after herald",
        "causal_protocol":"herald timestamp < secret basis draw < routing and analyzer settings < detector time-tag capture; all heralded trials included",
        "no_click_label":0}
def synth(P,n,seed):
    rng=random.Random(seed)
    eta=P["calibrated_pair_detection"]
    ideal=P["ideal_matched_probability_given_pair"]
    dark=3*P["accidental_dark_match_probability_when_no_pair"]
    outcomes=[]
    counts=[0,0,0,0]
    for i in range(n):
        b=rng.randrange(4)
        counts[b]+=1
        if rng.random()<eta:
            y=int(rng.random()<ideal)
        else:
            y=int(rng.random()<dark and rng.randrange(3)==0)
        outcomes.append(y)
    return outcomes,counts
def verify():
    high=plan(fR=.95,fS=.95)
    weak=plan(fR=.9,fS=.9)
    asym=plan(fR=.99,fS=.90)
    assert high["has_positive_witness_gap"]
    assert not weak["has_positive_witness_gap"]
    assert asym["has_positive_witness_gap"]
    assert high["required_signal_router_efficiency_at_fixed_reference"]<.95
    assert high["required_signal_router_efficiency_at_fixed_reference"]>.88
    runs=[]
    for seed in range(20261116,20261132):
        ys,settings=synth(high,12000,seed)
        assert sum(settings)==12000
        r=eprocess(ys,epsilon=.01,setting_leakage_TV=0,
                   alpha=ALPHA,adaptive=False,target_q=high["expected_gross_click_match"])
        runs.append({"seed":seed,"counts_by_basis":settings,
                     "first_evidence_crossing":r["first_crossing_trial"],
                     "anytime_p_upper":r["anytime_p_upper_bound"]})
    assert sum(x["first_evidence_crossing"] is not None for x in runs)>=14
    # Monotonic under exposure/calibration tightening
    assert plan(epsilon=.02)["separable_null_upper"]>.51
    assert plan(fR=.90,fS=.95)["expected_gross_click_match"]<high["expected_gross_click_match"]
    return {"status":"PASS_QUTRIT_TIMETAG_DETECTOR_MONTECARLO_WITH_ANYTIME_VALID_EPROCESS",
      "nominal_symmetric_95_percent_router":high,
      "symmetric_90_percent_router":weak,
      "asymmetric_99_90_percent_routers":asym,
      "sixteen_seed_synthetic_trials":runs,
      "success_count_16":sum(x["first_evidence_crossing"] is not None for x in runs),
      "calibration_acceptance":"Each physical setting b must have herald-independent time tags and a trusted POVM calibration whose worst-case source-adversarial overcount is <=epsilon; source-hidden random basis TV<=tv; all independent triggers included. Premature coincidence-triggered selection invalidates the null.",
      "hardware_not_built":True}
if __name__=="__main__":
    r=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(r["status"],r["success_count_16"],round(r["nominal_symmetric_95_percent_router"]["KL_expected_trial_scale_log_100_over_D"]))
