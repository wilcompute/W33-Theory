"""Event-ready 4-MUB qutrit Bell witness under adaptive non-IID drift.

Per trial: a heralded two-qutrit state is prepared, THEN an independent
uniform setting from {Z,X,XZ,XZ^2} is selected and a binary click-match
outcome observed. The separable bound E[Y | past] <= 1/2+epsilon holds
even for arbitrary history-dependent separable state preparations,
provided setting independence and a calibrated POVM envelope.

Hoeffding supermartingale tail:
 Pr(mean Y > 1/2+epsilon+t) <= exp(-2*M*t^2).
Not device-independent. Photonic circuit and errors are synthetic.
"""
import math,random,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_qutrit_randomized_memory_drift.json"

def null_p_value(successes,total,eps=0.):
    if total<1 or not 0<=successes<=total or eps<0:raise ValueError("bad input")
    delta=max(0.,successes/total-(.5+eps))
    return math.exp(-2*total*delta**2) if delta>0 else 1.

def power_plan(v,eta,eps=0.,alpha=.01,beta=.1):
    if not(0<=v<=1 and 0<=eta<=1 and eps>=0 and 0<alpha<1 and 0<beta<1):
        raise ValueError("parameters out of range")
    q=eta*(1+2*v)/3
    gap=q-.5-eps
    if gap<=0:return {"v":v,"eta":eta,"eps":eps,"required_heralded_trials":None}
    attempts=math.ceil((math.sqrt(math.log(1/alpha))+math.sqrt(math.log(1/beta)))**2/(2*gap**2))
    return {"v":v,"eta":eta,"eps":eps,"alpha":alpha,"beta":beta,
            "expected_clickmatch_probability":q,"separability_threshold":.5+eps,
            "required_heralded_trials":attempts,
            "scope":"Prespecified secret randomized bases; IID alt used only for power, not false-positive guarantee"}

def simulate(total=2500,seed=20261116,kind="coherent",v=.75,eta=.7,eps=.01):
    if kind not in ("coherent","adaptive_separable"):raise ValueError("invalid kind")
    if total<1 or not 0<=v<=1 or not 0<=eta<=1:raise ValueError("invalid parameters")
    rng=random.Random(seed)
    successes=0
    history=[]
    basis_prepared=0
    for t in range(total):
        # Prepare the state and all noise independent of CURRENT setting.
        if kind=="coherent":
            visibility=max(0.,min(1.,v+.08*math.sin(2*math.pi*t/173)))
            q_ideal=(1+2*visibility)/3
        else:
            # Product state |b,k> tensor |bar b,k>; preparation is
            # adaptive to prior settings but has no access to current b.
            basis_prepared=(basis_prepared+t//67+1)%4 if t%31==0 else basis_prepared
        efficiency=max(0.,min(1.,eta+.04*math.cos(2*math.pi*t/137)))
        setting=rng.randrange(4)  # fresh and independent AFTER preparation
        if kind=="adaptive_separable":
            q_ideal=1. if setting==basis_prepared else 1/3
        # A dark-count/crosstalk model with per-setting excess <=eps.
        q_click=min(1.,efficiency*q_ideal + .4*eps*(1-efficiency*q_ideal))
        outcome=int(rng.random()<q_click)
        successes+=outcome
        if t<20:history.append({"setting":setting,"click_match":outcome})
    p=null_p_value(successes,total,eps)
    return {"model":kind,"seed":seed,"trials":total,"click_matches":successes,
            "observed_rate":successes/total,"separable_null_supermartingale_p_bound":p,
            "reject_separability_at_one_percent":p<.01,
            "illustrative_first_20_trials":history,
            "no_physical_photon_data":True}

def verify():
    assert abs(null_p_value(10,10,0)-math.exp(-5))<1e-14
    assert null_p_value(1,10,.01)==1.
    baseline=power_plan(.75,.7,.01)
    assert baseline["required_heralded_trials"]==1248
    samples=[simulate(total=2500,seed=20261116,kind=kind)
             for kind in ("coherent","adaptive_separable")]
    assert samples[0]["observed_rate"]>.53
    assert samples[1]["observed_rate"]<.52
    assert samples[0]["reject_separability_at_one_percent"]
    assert not samples[1]["reject_separability_at_one_percent"]
    return {"status":"PASS_NONIID_RANDOM_SETTING_QUTRIT_SUPERMARTINGALE_WITNESS",
            "null_theorem":"Conditionally on any prior history, E[Y_t | history] <=1/2+epsilon for every separable prepared state, because the fresh basis is uniform and hidden until after state preparation.",
            "pvalue_bound":"exp(-2*M*max(0,S/M-1/2-epsilon)^2) valid even for non-IID adaptive separable sources",
            "measurement_requirement":"Current setting independent of prior hidden process; fair-sampling not assumed, all event-ready no-clicks count zero; click POVM dominated by ideal match + epsilon.",
            "scope":"Not device-independent; POVM calibration and independent setting choice must be checked; no experiment carried out.",
            "iid_power_example":baseline,"synthetic_samples":samples}
if __name__=="__main__":
    r=verify()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(r["status"],[(q["model"],q["separable_null_supermartingale_p_bound"]) for q in r["synthetic_samples"]])
