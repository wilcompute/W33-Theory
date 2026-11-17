"""New trusted efficiency-aware, basis-dependent qutrit entanglement witness.

Four MUB measurement settings b selected uniformly. Computational
Z analyzer needs zero mixing stages; 3 other bases use 3 Givens stages
per arm, with per-coupler transmission c, so relative coincidence
throughput t=c^6.

Under a trusted state-independent erasure measurement with common
throughput a and analyzers (1,t,t,t), exact separable bound:
p_sep <= a*(1+t)/4, attained by computational product states.
Proof: 4-MUB complex projective 2-design yields
sum_b matched_b = 1+|<alpha*|beta>|² <= 2.
Z contribution <=1, so S_weighted=t*S_total+(1-t)S_Z <=1+t.

This bound is NOT robust to arbitrary state/setting-dependent loss.
It must be certified as an OPERATOR-level POVM throughput bound for
all input qutrits, not merely an average on reference pulses. This
assumption can be more demanding than the original conservative
event-ready p0=.51 rule.

Physical source model: isotropic visibility v and computational-basis
dephasing E=exp(-sigma²) in the two-qutrit maximally entangled state.
q_Z=(1+2v)/3; q_nonZ=(1+2v E)/3. Average matches the prior q(v,sigma).
"""
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_qutrit_four_MUB_loss_compiler import basis
from toe_20261117_memory_2026_real_reference_qutrit import q,dkl
OUT=ROOT/"data"/"toe_20261117_qutrit_efficiency_aware_MUB_witness.json"
def rho_state(v=.75,sigma=.15):
    E=math.exp(-sigma*sigma)
    bell=np.zeros(9,complex)
    for j in range(3):bell[3*j+j]=1/math.sqrt(3)
    diagonal=np.zeros((9,9),complex)
    for j in range(3):diagonal[3*j+j,3*j+j]=1/3
    coh=E*np.outer(bell,bell.conj())+(1-E)*diagonal
    rho=(1-v)*np.eye(9)/9+v*coh
    assert abs(np.trace(rho)-1)<1e-13
    assert np.min(np.linalg.eigvalsh(rho))>=-1e-13
    return rho
def qperbasis():
    B=basis();rho=rho_state()
    qs={}
    for key,U in B.items():
        score=0.
        for j in range(3):
            a=U[:,j];pr=np.kron(np.outer(a,a.conj()),np.outer(a.conj(),a))
            score+=float(np.trace(rho@pr).real)
        qs[key]=score
    qz=(1+2*.75)/3
    qother=(1+2*.75*math.exp(-.15**2))/3
    assert abs(qs["Z_computational"]-qz)<1e-12
    assert all(abs(qs[k]-qother)<1e-12 for k in qs if k!="Z_computational")
    assert abs(sum(qs.values())/4-q())<1e-12
    return {"q_Z":qz,"q_each_nonZ":qother,"q_uniform_average":q(),
            "density_matrix_physical_positive":True,
            "explicit_four_basis_probabilities":qs}
def witness(c=.995,eta_mem=.902,n_mem=2,router=.995,path=.95,
            det_each=.9,calibration_error=0.):
    assert all(0<vv<=1 for vv in (c,eta_mem,router,path,det_each))
    assert n_mem in (1,2) and calibration_error>=0
    t=c**6
    common=det_each**2*eta_mem**n_mem*router**2*path
    qz=(1+2*.75)/3
    qn=(1+2*.75*math.exp(-.15**2))/3
    p_sep=common*(1+t)/4+calibration_error
    p_alt=common*(qz+3*t*qn)/4
    qthreshold=(1-qz)/(3*qn-1)
    # Guaranteed physical entanglement witness violation only when
    # actual calibrated p0 is a source-independent upper bound.
    if p_sep>=1:information=None
    elif p_alt>p_sep:
        information=math.log(100)/dkl(p_alt,p_sep)
    else:information=None
    return {"coupler_eff":c,"relative_noncomputational_basis_pair_throughput":t,
      "eta_common_trusted_state_independent":common,
      "memory_efficiency":eta_mem,"memory_arms":n_mem,
      "router_eff_each":router,"assumed_source_v":.75,"assumed_phase_sigma_rad":.15,
      "calibrated_separable_upper":p_sep,
      "expected_entangled_match":p_alt,
      "expected_violation":p_alt>p_sep,
      "minimum_relative_t_when_calibration_error_zero":qthreshold,
      "oracle_log_evalue100_heuristic_n":information,
      "calibration_error_absolute":calibration_error}
def verify():
    qs=qperbasis()
    # Exact MUB 2-design operator check, not just random samples:
    B=basis()
    Sum=np.zeros((9,9),complex)
    for U in B.values():
        for j in range(3):
            v=U[:,j];u=np.kron(v,v.conj())
            Sum+=np.outer(u,u.conj())
    bell=np.zeros(9,complex)
    for j in range(3):bell[4*j]=1/math.sqrt(3)
    assert np.allclose(Sum,np.eye(9)+3*np.outer(bell,bell.conj()),atol=1e-12)
    # Exact separable bound saturated by a=b=e0 for any 0<=t<=1.
    rng=np.random.default_rng(20261117)
    sampler=0.
    for _ in range(1000):
        a=rng.normal(size=3)+1j*rng.normal(size=3)
        b=rng.normal(size=3)+1j*rng.normal(size=3)
        a/=np.linalg.norm(a);b/=np.linalg.norm(b)
        for t in (.05,.35,.7,.97,1.):
            matched=[]
            for key,U in B.items():
                prob=sum(abs(np.vdot(U[:,j],a))**2 *
                         abs(np.vdot(U[:,j].conj(),b))**2
                         for j in range(3))
                matched.append((1 if key=="Z_computational" else t)*prob/4)
            obs=float(sum(matched))
            assert obs<=(1+t)/4+1e-12
            sampler=max(sampler,obs)
    for t in (0.,.1,.5,1.):
        a=b=np.array([1,0,0],complex)
        observed=0.
        for key,U in B.items():
            observed+=(1 if key=="Z_computational" else t)*sum(
                abs(np.vdot(U[:,j],a))**2*
                abs(np.vdot(U[:,j].conj(),b))**2 for j in range(3))/4
        assert abs(observed-(1+t)/4)<1e-12
    hard=witness()
    conservative=.51
    assert hard["expected_violation"]
    assert hard["expected_entangled_match"]<conservative
    assert hard["calibrated_separable_upper"]<conservative
    assert not witness(calibration_error=.3)["expected_violation"]
    weak=witness(eta_mem=.392,n_mem=2)
    assert weak["expected_violation"]
    rows=[]
    for mem,n in ((.902,1),(.902,2),(.392,1),(.392,2)):
        for c in (.95,.99,.995,.999):
            rows.append(witness(c=c,eta_mem=mem,n_mem=n))
    return {"status":"PASS_QUTRIT_4MUB_CALIBRATED_LOSS_WITNESS_RECOILS_FROM_CONSERVATIVE_NO_GO",
      "MUB_exact_2design_identity":"sum_b sum_j |u_bj,u_bj*> <u_bj,u_bj*| = I_9 + 3|Phi_3><Phi_3|",
      "exact_loss_aware_separable_bound":"With trusted state-independent common throughput a and computational/noncomputational basis pair throughputs (1,t,t,t), p_sep<=a*(1+t)/4. Equality for |0> tensor |0>. For arbitrary separable mixtures, convexity preserves bound.",
      "model_qb":qs,"random_product_controls":1000,
      "largest_random_weighted_score":sampler,
      "conservative_vs_calibrated_two_memory_99p5":hard,
      "weak_memory_loss_aware_case":weak,
      "scenario_grid":rows,
      "critical_measurement_assumption":"The quantum instruments including memories, detectors and setting switches must be trusted and characterized as state-independent erasure proportional to target projective POVM for ALL input states at each setting, with bounded preparation-correlated drift, side channels and calibration error. A marginal efficiency measured only on bright classical pulses is insufficient. If this is not verified, retain p0=.51 conservative protocol; no detector loophole can be claimed closed.",
      "not_an_experiment":"Provides a protocol-level alternative with stricter trust assumptions. No actual qutrit storage, qutrit interferometer, source, setting secrecy, device calibration or time-tag data was produced.",
      "martingale_caveat":"Use p0=certified sequential conditional separable upper bound in the existing predictable e-process. The oracle KL count is only an information scale, not guaranteed sample complexity or statistical certification."}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["conservative_vs_calibrated_two_memory_99p5"]["calibrated_separable_upper"],
       z["conservative_vs_calibrated_two_memory_99p5"]["expected_entangled_match"],
       z["conservative_vs_calibrated_two_memory_99p5"]["oracle_log_evalue100_heuristic_n"])
