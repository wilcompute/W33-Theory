"""Anytime-valid, non-IID, setting-randomized qutrit entanglement e-process.

For each event-ready trial, choose the basis uniformly AFTER preparing
the two qutrits. A calibrated separable null has predictable probability
p_t <= p0=1/2+measurement_error+setting_leakage_TV.

For any predictable q_t>=p0, the factor
L_t=(q_t/p0)^Y_t * ((1-q_t)/(1-p0))^(1-Y_t)
has E[L_t|past]<=1 for arbitrary non-IID separable sources.
The nonnegative product is a supermartingale, so P(sup_t L_1..L_t
>=1/alpha)<=alpha by Ville's inequality, including optional stopping.

This gives sequential validation against adaptive drift and variable
heralded counts, NOT device-independent hardware or actual data.
"""
import json,math,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_qutrit_anytime_eprocess.json"

def check_factor(p0,q,p):
    """Conditional expectation under Bernoulli(p)."""
    if not 0<p0<1 or not p0<=q<1 or not 0<=p<=p0:
        raise ValueError("out of null range")
    expectation=p*q/p0+(1-p)*(1-q)/(1-p0)
    assert expectation<=1+1e-14
    return expectation

def eprocess(outcomes,epsilon=.01,setting_leakage_TV=0.,
             alpha=.01,adaptive=True,target_q=.65):
    if not(0<alpha<1 and 0<=epsilon and setting_leakage_TV>=0):
        raise ValueError("bad alpha or calibration")
    p0=.5+epsilon+setting_leakage_TV
    if not 0<p0<1:raise ValueError("invalid separable null upper probability")
    if not p0<=target_q<1:raise ValueError("target q must exceed p0 and <1")
    logE=0.
    successes=0
    first_crossing=None
    peak=0.
    history=[]
    for i,y in enumerate(outcomes,1):
        if y not in (0,1):raise ValueError("event-ready outcome must be 0 or 1")
        # Beta(1/2,1/2) posterior from ONLY earlier trials,
        # clipped above the separable-null upper probability.
        q=max(p0,min(.999999,(successes+.5)/(i))) if adaptive else target_q
        logE+=math.log(q/p0) if y else math.log((1-q)/(1-p0))
        successes+=y
        peak=max(peak,logE)
        if first_crossing is None and logE>=math.log(1/alpha):
            first_crossing=i
        if i in (10,50,100,200,500,1000,2000) or i==len(outcomes):
            history.append({"n":i,"click_matches":successes,
                "log_evidence":logE,
                "anytime_adjusted_p_upper_bound":math.exp(-peak) if peak<700 else 0.})
    return {"number_of_heralded_trials":len(outcomes),
      "click_matches":successes,"null_upper_bound_p0":p0,
      "log_evidence_final":logE,"log_evidence_peak":peak,
      "anytime_p_upper_bound":math.exp(-peak) if peak<700 else 0.,
      "reject_at_alpha":peak>=math.log(1/alpha),
      "first_crossing_trial":first_crossing,
      "adaptive_predictable_q":adaptive,"history":history}

def synth(kind,n,seed,eta=.70,visibility=.75):
    if kind not in ("coherent_drift","adaptive_separable","worst_case_separable"):
        raise ValueError("unsupported synthetic model")
    rng=random.Random(seed)
    prepared=0
    outcomes=[]
    for t in range(n):
        if kind=="coherent_drift":
            v=max(0.,min(1.,visibility+.05*math.sin(2*math.pi*t/97)))
            ideal=(1+2*v)/3
        elif kind=="worst_case_separable":
            ideal=.51  # exact calibrated null upper value for epsilon=.01
        else:
            if t%19==0:prepared=(prepared+t//19+1)%4
        setting=rng.randrange(4)
        if kind=="adaptive_separable":
            ideal=1 if setting==prepared else 1/3
        efficiency=max(0.,min(1.,eta+.05*math.cos(2*math.pi*t/173))) if kind!="worst_case_separable" else 1.
        prob=efficiency*ideal
        outcomes.append(int(rng.random()<prob))
    return outcomes

def verify():
    for p0 in (.5,.51,.55,.7):
        for q in (p0,.8,.9):
            if q>=p0:
                for p in (0,p0/2,p0):
                    check_factor(p0,q,p)
    coherent=eprocess(synth("coherent_drift",2500,20261116))
    adaptive=eprocess(synth("adaptive_separable",2500,20261116))
    worst=eprocess(synth("worst_case_separable",2500,20261116))
    assert coherent["reject_at_alpha"]
    assert not adaptive["reject_at_alpha"]
    assert not worst["reject_at_alpha"]
    # Optional-stopping validity follows exactly from conditional
    # supermartingale factors and Ville, not Monte Carlo.
    return {"status":"PASS_ANYTIME_NONIID_QUTRIT_SEQUENTIAL_ENTANGLEMENT_EPROCESS",
       "separable_null":"For each conditionally prepared separable two-qutrit state, randomized four-MUB click-match probability <= p0=1/2+epsilon+setting_TV.",
       "factor":"(q_t/p0)^Y * ((1-q_t)/(1-p0))^(1-Y), q_t>=p0 predictable from past only",
       "proof":"For p<=p0, E[factor]=p*q/p0+(1-p)*(1-q)/(1-p0)<=1, hence the product is a nonnegative supermartingale. Ville bounds P(ever cross 1/alpha)<=alpha.",
       "optional_stopping_valid":True,"hardware_data":False,
       "leakage_note":"Setting leakage TV is a conservative total-variation upper bound conditional on any adversarial source information. Unbounded or unknown leakage invalidates the proof.",
       "simulated_examples":{"coherent_drift":coherent,
                             "adaptive_separable":adaptive,
                             "worst_case_separable":worst}}
if __name__=="__main__":
    cert=verify()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(cert["status"],[(key,val["first_crossing_trial"],round(val["anytime_p_upper_bound"],6)) for key,val in cert["simulated_examples"].items()])
