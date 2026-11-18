"""EXACT separable bound for arbitrary BASIS-DEPENDENT (but
state-INDEPENDENT) efficiencies in all four qutrit MUBs.

Given basis b chosen uniformly, pair throughput a*w_b, w_b>=0,
and matched-conjugate outcomes, each product state satisfies
p_sep <= a*(sum_b w_b +2*max_b w_b)/12.
This is TIGHT for the conjugate pair of eigenvectors of a
maximum-throughput basis. Proof: four orthogonal 2D traceless
Hermitian MUB dephasing subspaces span the eight-dimensional
qutrit Bloch space; pure state's traceless squared norm is 2/3.
Weighted Cauchy gives correlation <=2/3*wmax.

Allows four independently measured efficiencies rather than
artificial assumption three have exactly identical loss.
Per-setting operator error epsilon and basis leaked TV beta
must be added to the separable bound, and source lower bound
must be reduced. Requires UNIFORM operator-level calibration
over all input states, not mean classical photon efficiencies.
"""
import json,sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_qutrit_four_MUB_loss_compiler import basis
from toe_20261117_qutrit_calibrated_loss_witness import rho_state,qperbasis
from toe_20261117_qutrit_calibration_anytime_DP import anytime_dp
OUT=ROOT/"data"/"toe_20261117_qutrit_nonuniform_four_MUB_tight_sep.json"
def exact_sep(weights,a=1):
    w=np.asarray(weights,dtype=float)
    assert w.shape==(4,) and np.all(w>=0) and a>=0
    return float(a*(np.sum(w)+2*np.max(w))/12)
def source_match(weights,a=1):
    vals=qperbasis()
    w=np.asarray(weights,dtype=float)
    return float(a*(w[0]*vals["q_Z"]+sum(w[1:])*vals["q_each_nonZ"])/4)
def raw_prob(a,b,U):
    return float(sum(abs(np.vdot(U[:,i],a))**2*
                     abs(np.vdot(U[:,i].conj(),b))**2 for i in range(3)))
def scenario(w,a=.62,delta_a=.005,delta_w=.007,
             operator_epsilon=.01,setting_leak_TV=.005):
    w=np.asarray(w,float)
    lo=np.maximum(0,w-delta_w);hi=w+delta_w
    a_lo=max(0,a-delta_a);a_hi=a+delta_a
    p0=exact_sep(hi,a_hi)+operator_epsilon+setting_leak_TV
    p1=source_match(lo,a_lo)-operator_epsilon
    return {"nominal_weights":w.tolist(),"nominal_common_a":a,
      "common_a_calibration_halfwidth":delta_a,
      "each_basis_weight_calibration_halfwidth":delta_w,
      "measurement_operator_error":operator_epsilon,
      "setting_leak_TV":setting_leak_TV,
      "conservative_separable_bound":p0,
      "conservative_source_match_lower":p1,
      "robust_positive_gap":p1-p0,
      "violates_if_source_matches_model":p1>p0}
def verify():
    B=list(basis().values())
    assert len(B)==4
    rng=np.random.default_rng(20261117)
    designs=[
      [1.,.995**6,.995**6,.995**6],
      [1.,.98,.96,.99],
      [.92,1.,.93,.88],
      [.6,.83,.71,1.],
      [.05,.1,.15,.2],
      [1.,1.,1.,1.]
    ]
    random_checked=0;equalities=[]
    for w in designs:
        target=exact_sep(w)
        maximum=int(np.argmax(w))
        for ix in range(3):
            a=B[maximum][:,ix]
            bb=a.conj()
            obs=sum(w[j]*raw_prob(a,bb,B[j]) for j in range(4))/4
            assert abs(obs-target)<1e-12
            equalities.append({"weights":w,"max_basis_index":maximum,
                               "saturation":obs,"bound":target})
        for j in range(250):
            a=rng.normal(size=3)+1j*rng.normal(size=3)
            b=rng.normal(size=3)+1j*rng.normal(size=3)
            a/=np.linalg.norm(a);b/=np.linalg.norm(b)
            obs=sum(w[i]*raw_prob(a,b,B[i]) for i in range(4))/4
            assert obs<=target+1e-12
            random_checked+=1
    # Bound recovers the previously derived exact (1+t)/4 case.
    t=.97
    assert abs(exact_sep([1,t,t,t])-(1+t)/4)<1e-15
    q=qperbasis()
    F=(4*q["q_uniform_average"]-1)/3
    rho=rho_state()
    bell=np.zeros(9,complex)
    for i in range(3):bell[4*i]=1/math.sqrt(3)
    assert abs(np.vdot(bell,rho@bell).real-F)<1e-12
    # Inverse-probability weighting of matched-clicks is an unbiased
    # estimate of Bell fidelity under known state-independent losses,
    # but cannot close an adversarial detection loophole.
    scenarios=[scenario(w) for w in designs[:4]]
    assert all(z["violates_if_source_matches_model"] for z in scenarios)
    nominal=scenarios[1]
    null=anytime_dp(nominal["conservative_separable_bound"],
                    nominal["conservative_source_match_lower"],steps=500)
    alternative=anytime_dp(nominal["conservative_separable_bound"],
                    nominal["conservative_source_match_lower"],steps=500,
                    truth=nominal["conservative_source_match_lower"])
    assert null["ever_crossed_prob"]<=.010000000001
    assert alternative["ever_crossed_prob"]>.99
    return {"status":"PASS_QUTRIT_FOUR_ARBITRARY_MUB_EFFICIENCIES_TIGHT_SEPARABLE_AND_EPROCESS",
      "tight_bound":"For w_b>=0, uniformly chosen four MUBs and trusted state-independent erasure a*w_b, p_sep<=a*(sum_b w_b+2*max_b w_b)/12, with equality for basis eigenstate product in a max-weight basis.",
      "proof":"Traceless qutrit Bloch operator has HS norm squared 2/3 for pure states; four MUB traceless subspaces are pairwise Hilbert-Schmidt orthogonal and span 8 dimensions. Weighted Cauchy bounds weighted matched correlations by wmax*2/3; identity contributes sum(w)/3.",
      "random_products_checked":random_checked,
      "independent_equality_checks":equalities,
      "nonuniform_calibrated_examples":scenarios,
      "exact_sequential_null_first_crossing_500":null,
      "exact_sequential_alternative_first_crossing_500":alternative,
      "Bell_fidelity_from_ideal_uniform_fourMUB":"F=(4*mean_match-1)/3",
      "model_Bell_fidelity":F,
      "loss_unbiasing":"Under known state-independent throughput a*w_b>0, E[X_b/w_b] averaged over uniform choices = a*(1+3F)/4. Dividing by small w_b inflates variance and is INVALID if efficiencies depend on input state.",
      "scope":"Ideal projective four-MUB and the stated operator-level erasure model only. Experimental qutrit process tomography, leakage bounds, per-setting drift and realistic time-bin routing remain absent."}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["random_products_checked"],
         z["nonuniform_calibrated_examples"][1]["robust_positive_gap"])
