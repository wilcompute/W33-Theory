#!/usr/bin/env python3
"""Eight independent TOE/frontier falsifiers (5 continuations + 3 orthogonal controls).

All results are idealized mathematical/toy-model computations. Established
physics and prior art are stated in the accompanying research note.
"""
from __future__ import annotations
from collections import Counter
from itertools import product
from pathlib import Path
import json
import math
import numpy as np
from scipy.stats import binom
from scipy.special import logsumexp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261105_eight_fronts_controlled.json"

def gauge_dynamics():
    """One-particle Z2 ring Wilson-flux gap; full-field dynamics not inferred."""
    rows=[]
    for n in (3,4,6,8,12,20):
        def ground(flux):
            angles=(2*np.pi*np.arange(n)+flux)/n
            return float(np.min(-2*np.cos(angles)))
        e0,epi=ground(0),ground(np.pi)
        gap=epi-e0
        expected=2*(1-np.cos(np.pi/n))
        assert np.isclose(gap,expected,atol=1e-12)
        rows.append(dict(n=n,E_zero=e0,E_pi=epi,delta=gap,
                         n2_delta=n*n*gap))
    assert all(x["delta"]>0 for x in rows)
    assert rows[-1]["delta"]<rows[0]["delta"]
    # As n grows, n^2 delta -> pi^2, so bare matter selection weakens.
    assert abs(rows[-1]["n2_delta"]-np.pi**2)<.021
    return {"status":"PASS_CONDITIONAL_AHARONOV_BOHM_FLUX_GAP",
            "model":"one mobile matter excitation, Z2 background ring Wilson flux; hopping J=1",
            "rows":rows,"lim_n2_gap":"pi^2",
            "boundary":"Background flux only; no dynamical photon, SM vacuum, cosmological selection"}

def spectral_continuum():
    """2D locality control vs q=3,5,7 fully-connected null shell graphs."""
    n=64
    z=(2-2*np.cos(2*np.pi*np.arange(n)/n))/4
    torus=(z[:,None]+z[None,:]).reshape(-1)
    def ds(spectrum, multiplicities, t):
        eig=np.array(spectrum,dtype=float)
        mul=np.array(multiplicities,dtype=float)
        terms=np.log(mul)-t*eig
        weights=np.exp(terms-logsumexp(terms))
        return float(2*t*np.dot(weights,eig))
    torus_ds={str(t):ds(torus,np.ones(len(torus)),t) for t in (4,8,16,32)}
    assert abs(torus_ds["32"]-2)<.1
    rows=[]
    for q in (3,5,7,11):
        eig=[0,q*(q-1)/q**2,1,q*(q+1)/q**2]
        mul=[1,q*(q*q-1)//2,q*q-1,q*(q-1)**2//2]
        assert sum(mul)==q**3
        rows.append({"q":q,"d_s_t4":ds(eig,mul,4),
                     "d_s_t16":ds(eig,mul,16),
                     "normalized_gap":min(eig[1:])})
    assert all(r["normalized_gap"]>0.6 for r in rows)
    return {"status":"PASS_LOCALITY_CONTROL_NOT_GRAVITY",
            "torus_2d_n64_normalized_heat_dimension":torus_ds,
            "affine_null_graphs":rows,
            "boundary":"A weighted local graph requires chosen embedding and neighborhood; no dynamically emergent curvature"}

def quantum_memory():
    """Exact binomial witness for trusted entanglement-breaking reset protocol."""
    p=.35; eta=.85
    ideal=(1+8*p)/9
    observed=eta*ideal+(1-eta)/9
    null=1/3
    n=3000
    threshold=int(binom.isf(.01,n,null))+1
    alpha=float(binom.sf(threshold-1,n,null))
    power=float(binom.sf(threshold-1,n,observed))
    eta_critical=1/(4*p)
    assert eta>eta_critical and observed>null
    assert alpha<=.01 and power>.99
    return {"status":"PASS_TRUSTED_RESET_WITNESS_POWER",
            "reference":"qutrit R; E quantum storage; S reset; R-S Bell-projector readout",
            "depolarizing_survival_p":p,"all_trials_efficiency":eta,
            "fidelity_ideal":ideal,"fidelity_with_random_assigned_noclick":observed,
            "separable_null_fidelity":null, "minimum_efficiency_to_beat_null":eta_critical,
            "shots":n,"reject_if_Bell_hits_at_least":threshold,
            "exact_one_sided_false_alarm":alpha,"true_positive_power":power,
            "boundary":"Trusted reference/reset and no quantum bypass are indispensable; not an experiment"}

def chirality_vacuum():
    """Finite Ising CP symmetry forbids nonzero sign expectation at zero bias."""
    L=4; N=L*L
    bits=np.arange(1<<N,dtype=np.uint32)
    spin=1-2*((bits[:,None]>>np.arange(N,dtype=np.uint32))&1).astype(np.int8)
    bonds=[(x*L+y,x*L+(y+1)%L) for x in range(L) for y in range(L)]
    bonds +=[(x*L+y,((x+1)%L)*L+y) for x in range(L) for y in range(L)]
    interaction=np.zeros(len(bits),dtype=int)
    for i,j in bonds: interaction+=spin[:,i]*spin[:,j]
    mag=spin.sum(axis=1).astype(float)
    assert len(mag)==65536
    assert int(np.sum(mag))==0
    def expected(beta,field):
        lw=beta*(interaction+field*mag)
        w=np.exp(lw-logsumexp(lw))
        return float(np.dot(w,mag)/N), float(np.dot(w,np.abs(mag))/N)
    mean0,abs0=expected(.55,0)
    mean_pos,abs_pos=expected(.55,.03)
    mean_neg,abs_neg=expected(.55,-.03)
    assert abs(mean0)<1e-13 and abs(mean_pos+mean_neg)<1e-12
    assert mean_pos>0 and mean_neg<0 and abs(abs_pos-abs_neg)<1e-12
    return {"status":"PASS_FINITE_CP_DEGENERACY_NO_UNIQUE_SIGN",
            "finite_4x4_partition_states":65536,"beta":.55,
            "zero_bias_signed_order":mean0,"zero_bias_abs_order":abs0,
            "positive_bias_signed_order":mean_pos,
            "negative_bias_signed_order":mean_neg,
            "boundary":"Proves no unique preferred sign in finite CP-symmetric ensemble, not a SM chirality vacuum"}

def optical_falsifier():
    """Native W33/Witting 40-ray POVM readout vs Helstrom optimum for ray mixtures."""
    V=[]
    for vec in product(range(3),repeat=4):
        if not any(vec):continue
        k=next(i for i,x in enumerate(vec) if x)
        if vec[k]==1:V.append(vec)
    assert len(V)==40
    A=np.array([[int(u!=v and
        (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%3==0)
        for v in V] for u in V],dtype=int)
    J=np.ones((40,40),dtype=int);I=np.eye(40,dtype=int)
    assert np.all(A.sum(axis=0)==12)
    assert np.array_equal(A@A,12*I+2*A+4*(J-I-A))
    G=(2*I+J-A)/3
    assert np.max(np.abs(G.sum(axis=1)-10))<1e-12
    eps=.2
    rows=[]
    for adjacent in (True,False):
        i,j=next((i,j) for i in range(40) for j in range(i+1,40)
                 if bool(A[i,j])==adjacent)
        prob_i=(1-eps)/40+eps*G[i]/10
        prob_j=(1-eps)/40+eps*G[j]/10
        assert abs(sum(prob_i)-1)<1e-12 and min(prob_i)>=0
        tv=.5*sum(abs(prob_i-prob_j))
        hel_dist=eps*math.sqrt(1-G[i,j])
        assert tv<=hel_dist+1e-12
        rows.append({"adjacent":adjacent,"projector_overlap":float(G[i,j]),
                     "Witting_POVM_total_variation":float(tv),
                     "POVM_optimal_decision_success":float((1+tv)/2),
                     "Helstrom_optimal_success":float((1+hel_dist)/2),
                     "fraction_of_optimal_trace_dist":float(tv/hel_dist)})
    assert abs(rows[0]["Witting_POVM_total_variation"]-2*eps/5)<1e-12
    assert abs(rows[1]["Witting_POVM_total_variation"]-eps/3)<1e-12
    return {"status":"PASS_NATIVE_WITTING_BINARY_READOUT_GAP",
            "ray_count":40,"hilbert_dimension":4,"mixture_epsilon":eps,
            "Witting_effects":"E_j=P_j/10", "comparisons":rows,
            "boundary":"Ideal projective 40-effect POVM; no chip, calibration, finite hardware data"}

def nonhermitian_skin():
    """Off-diagonal hopping asymmetry makes PBC winding and OBC edge skin."""
    n=40; r=1.5; l=.5
    H=np.zeros((n,n))
    for i in range(n-1):
        H[i,i+1]=r;H[i+1,i]=l
    E,R=np.linalg.eig(H)
    norms=np.sum(np.abs(R)**2,axis=0)
    cm=float(np.mean(np.sum(np.arange(n)[:,None]*np.abs(R)**2,axis=0)/norms))
    k=np.linspace(0,2*np.pi,401)
    z=r*np.exp(1j*k)+l*np.exp(-1j*k)
    winding=float((np.unwrap(np.angle(z))[-1]-np.unwrap(np.angle(z))[0])/(2*np.pi))
    assert abs(winding-1)<1e-12
    assert max(abs(E.imag))<1e-12 and cm<3
    # OBC matrix is positive-similar to a Hermitian hopping model.
    scale=(math.sqrt(l/r))**np.arange(n)
    symmetric=np.diag(np.full(n-1,math.sqrt(r*l)),1)
    symmetric+=np.diag(np.full(n-1,math.sqrt(r*l)),-1)
    assert np.max(abs(H-scale[:,None]*symmetric/scale[None,:]))<1e-12
    _,phi=np.linalg.eigh(symmetric)
    right=scale[:,None]*phi
    left=phi/scale[:,None]
    assert np.max(abs(left*right-phi**2))<1e-12
    biorth_center=float(np.mean(np.sum(np.arange(n)[:,None]*(left*right),axis=0)))
    assert abs(biorth_center-(n-1)/2)<1e-11
    return {"status":"PASS_HATANO_NELSON_SKIN_CONTROL","sites":n,"right_hopping":r,
            "left_hopping":l,"PBC_point_gap_winding":winding,
            "OBC_max_abs_imag_eigenvalue":float(max(abs(E.imag))),
            "OBC_mean_right_eigenstate_center":cm,"symmetric_control_center":(n-1)/2,
            "OBC_biorthogonal_mean_center":biorth_center,
            "OBC_similarity_condition_number":float(scale.max()/scale.min()),
            "OBC_similarity_to_real_symmetric_verified":True,
            "boundary":"Known non-Hermitian skin effect; physical metric must be specified before fundamental inference"}

def quasiperiodic_localization():
    """Aubry-Andre spectral IPR across subcritical/critical/supercritical."""
    golden=(math.sqrt(5)-1)/2
    rows=[]
    for n in (55,89,144):
        record={"sites":n}
        for lam in (1.,2.,3.):
            j=np.arange(n)
            H=np.diag(lam*np.cos(2*np.pi*golden*j))
            H+=np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1)
            vals,V=np.linalg.eigh(H)
            inds=np.argsort(abs(vals))[:max(10,n//4)]
            record[f"mean_IPR_lambda_{lam:g}"]=float(np.mean(np.sum(np.abs(V[:,inds])**4,axis=0)))
        assert record["mean_IPR_lambda_3"]>record["mean_IPR_lambda_2"]>record["mean_IPR_lambda_1"]
        rows.append(record)
    assert rows[-1]["mean_IPR_lambda_1"]<rows[0]["mean_IPR_lambda_1"]
    scales=np.log([rec["sites"] for rec in rows])
    exponents={str(lam):float(-np.polyfit(scales,
         np.log([rec[f"mean_IPR_lambda_{lam}"] for rec in rows]),1)[0])
         for lam in (1,2,3)}
    assert exponents["1"]>exponents["2"]>exponents["3"]
    assert exponents["3"]<.2
    return {"status":"PASS_AUBRY_ANDRE_FINITE_SIZE_LOCALIZATION",
            "model":"irrational golden-frequency onsite cosine, open chain, nearest hopping=1",
            "rows":rows,"effective_IPR_decay_exponents":exponents,
            "boundary":"Aubry-Andre self-duality at lambda=2 is prior art; effective exponents from three finite sizes are not thermodynamic critical exponents"}

def postselection_collider():
    """Purely local hidden-variable toy PR box created by joint herald."""
    correlations={};raw={};eff={}
    for x,y in product((0,1),repeat=2):
        accepted=[]
        allterms=[]
        for u,v in product((0,1),repeat=2):
            parity=(-1)**(u^v)
            allterms.append(parity)
            if (u^v)==(x*y):accepted.append(parity)
        assert len(accepted)==2
        correlations[f"{x}{y}"]=float(np.mean(accepted))
        raw[f"{x}{y}"]=float(np.mean(allterms))
        eff[f"{x}{y}"]=len(accepted)/4
    CHSH=lambda d:d["00"]+d["01"]+d["10"]-d["11"]
    conditional=CHSH(correlations)
    all_trial=CHSH({k:eff[k]*correlations[k] for k in correlations})
    assert conditional==4 and all_trial==2 and CHSH(raw)==0
    # A pre-settings central herald that keeps only u=v has CHSH=2, not 4.
    setting_independent_correlations={key:1.0 for key in correlations}
    assert CHSH(setting_independent_correlations)==2
    # Stronger detection-loophole example with *strictly local* detectors:
    # shared lambda=(target_x,target_y,u); A emits u, B emits u xor target_x*target_y.
    # A clicks iff x==target_x; B clicks iff y==target_y; no inter-party message.
    fully_local_corr={}
    fully_local_eff={}
    for x,y in product((0,1),repeat=2):
        accepted=[]
        for target_x,target_y,u in product((0,1),repeat=3):
            a=u
            b=u^(target_x*target_y)
            if x==target_x and y==target_y:
                accepted.append((-1)**(a^b))
        assert len(accepted)==2
        fully_local_corr[f"{x}{y}"]=float(np.mean(accepted))
        fully_local_eff[f"{x}{y}"]=len(accepted)/8
    assert CHSH(fully_local_corr)==4
    assert all(v==.25 for v in fully_local_eff.values())
    assert CHSH({k:fully_local_eff[k]*fully_local_corr[k] for k in fully_local_corr})==1
    return {"status":"PASS_FAKE_PR_BY_SETTING_DEPENDENT_SELECTION",
            "hidden_bits":"u,v independent uniform; Alice output u, Bob output v; joint herald accepts iff u xor v=x*y",
            "conditional_correlations":correlations,
            "conditional_CHSH":conditional,"detection_efficiency_each_setting":eff,
            "all_trials_random_noclick_CHSH":all_trial,
            "unconditioned_CHSH":CHSH(raw),
            "setting_independent_herald_control_CHSH":CHSH(setting_independent_correlations),
            "fully_local_detector_conditional_CHSH":CHSH(fully_local_corr),
            "fully_local_detector_joint_efficiency":fully_local_eff,
            "fully_local_detector_randomized_alltrials_CHSH":CHSH({k:fully_local_eff[k]*fully_local_corr[k] for k in fully_local_corr}),
            "boundary":"Two distinct local-output selection controls: centralized joint herald and fully local setting-dependent detectors; neither certifies Bell nonlocality"}

FRONTS=[
    ("1_native_gauge_action",gauge_dynamics),
    ("2_continuum_locality",spectral_continuum),
    ("3_temporal_memory",quantum_memory),
    ("4_chirality_vacuum",chirality_vacuum),
    ("5_optical_falsifier",optical_falsifier),
    ("6_orthogonal_nonhermitian_skin",nonhermitian_skin),
    ("7_orthogonal_quasiperiodic_localization",quasiperiodic_localization),
    ("8_orthogonal_postselection_collider",postselection_collider)
]
def main():
    results={label:func() for label,func in FRONTS}
    report={"version":"2026-11-05.eight_fronts.v1","base":"independent idealized falsifiers; no TOE solved",
            "prior_art_boundary":"Each constituent model is known; this combined regression atlas is repo-specific.",
            "results":results}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf8")
    for key,val in results.items():
        print("PASS",key,val["status"])
    print("CERTIFICATE",OUT)
    return report
if __name__=="__main__":
    main()
