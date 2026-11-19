#!/usr/bin/env python3
"""2026-11-19 independent physics-first research, v4.

1. Refit complete (two 24F) renormalizable SU5 thresholds at fixed MU.
2. Derive minimal type-III seesaw nonunitarity and naturalness correlations.
3. Positive Kallen-Lehmann spectral no-go for exponential UV damping proxy.
4. DESI DR2 13x13 BAO Bayesian *prior-sensitivity* via analytic q integration.
5. Two-copy single-photon local SSR entanglement activation with loss resource.

All external data originate in already committed DESI DR2 text files; no W33 input.
This is NOT a completed or viable GUT, TOE, or new physical discovery.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
from scipy.optimize import differential_evolution
from scipy.special import ndtr
from scipy.stats import qmc
from numpy.polynomial.legendre import leggauss

import toe_20261119_joint_physics_five_frontiers as old
import toe_20261119_physics_full_covariance_uv_operational as prior

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"data"/"toe_20261119_five_front_physics_v4.json"
PI=np.pi
MZ=91.1876
INVSM=np.array([3/5*(1-.23122)*127.930,.23122*127.930,1/.1180])
B_SM=np.array([41/10,-19/6,-7.])
B3=np.array([0,4/3,0.])
B8=np.array([0,0,2.])
BX=np.array([10/3,2,4/3])


def _adjoint_couplings(lt2,lo2,lmu,sgn1,sgn2):
    """Two diagonal 24_F fermions, first triplet/oct at prior fixed inputs.
    The adjoint Clebsch relation is MX=(signed M3 + signed M8)/2.
    All thresholds lie above MZ and at/below MU.
    """
    MT=old.gauge_bridge(2e16)["field_content"][0]["Mass_GeV"]
    MO=old.gauge_bridge(2e16)["field_content"][1]["Mass_GeV"]
    MU=10**lmu
    mt=np.array([MT,10**lt2]);mo=np.array([MO,10**lo2])
    mx=np.array([abs((MT+sgn1*MO)/2),abs((mt[1]+sgn2*mo[1])/2)])
    if min(mx)<MZ or min(mt)<MZ or min(mo)<MZ or max(mt)>MU or max(mo)>MU or MU<=max(MT,MO):
        return np.array([100.,100.]),mx
    inv=INVSM-B_SM*np.log(MU/MZ)/(2*PI)
    for m,delta in [(m,B3) for m in mt]+[(m,B8) for m in mo]+[(m,BX) for m in mx]:
        if m<MU:inv-=delta*np.log(MU/m)/(2*PI)
    return inv[:1]-inv[1:],mx


def adjoint_full_threshold_recheck():
    """Numerical scan, NOT a rigorous global no-go. Fixed 2e16 GeV crossing
    with first triplet/octet masses fixed at prior two-field toy values;
    second octet and triplet may vary from MZ up to MU.
    """
    MU=2e16
    lmu=np.log10(MU)
    sols=[]
    for s1 in (+1,-1):
        for s2 in (+1,-1):
            bounds=[(np.log10(MZ)+.001,lmu),
                    (np.log10(MZ)+.001,lmu)]
            f=lambda x: float(np.linalg.norm(_adjoint_couplings(
                     x[0],x[1],lmu,s1,s2)[0])**2)
            r=differential_evolution(f,bounds,seed=20261119,
                        popsize=10,maxiter=125,tol=1e-10,polish=True)
            mismatch,mx=_adjoint_couplings(*r.x,lmu,s1,s2)
            sols.append({
               "signed_octet_triplet_relative_signs":[s1,s2],
               "best_second_triplet_GeV":float(10**r.x[0]),
               "best_second_octet_GeV":float(10**r.x[1]),
               "X_fermion_masses_GeV":mx.tolist(),
               "inverse_alpha_differences":mismatch.tolist(),
               "Euclidean_inverse_alpha_mismatch_norm":float(np.linalg.norm(mismatch)),
               "search_bounds_GeV":[MZ,MU],
               "optimizer_success":bool(r.success)})
    minimum=min(s["Euclidean_inverse_alpha_mismatch_norm"] for s in sols)
    assert minimum>7.0
    complete_beta=B3+B8+BX
    assert np.allclose(complete_beta,[10/3]*3)
    return {
       "status":"PASS",
       "assumed_MU_GeV":MU,
       "fixed_old_masses":{"triplet_1_GeV":old.gauge_bridge(MU)["field_content"][0]["Mass_GeV"],
                           "octet_1_GeV":old.gauge_bridge(MU)["field_content"][1]["Mass_GeV"]},
       "all_components_included":[
           "(1,3,0) x2", "(8,1,0) x2","(3,2,-5/6)+(bar3,2,+5/6) x2"],
       "complete_24F_one_loop_beta":complete_beta.tolist(),
       "diagonal_two_24F_results":sols,
       "best_mismatch_norm":minimum,
       "conclusion":"The prior fixed benchmark matching is not restored by varying just second adjoint triplet/oct masses inside this diagonal two-24F renormalizable scan",
       "scope":["Numerical global optimization with multiple relative signs, not a formal all-real-algebraic proof.",
                "Fixed earlier M3_1,M8_1 and MU; other Higgs/scalar/SM thresholds, SU5 breaking dynamics not included.",
                "Complex off-diagonal generation mixing or higher-dimensional mass operators evade scanned subspace.",
                "No successful UV-complete GUT or physical proton decay calculation."]
    }


def type_iii_flavor_and_naturalness():
    G=old.gauge_bridge(2e16)
    M=G["field_content"][0]["Mass_GeV"]
    U=old.pmns(.3047,.0222,.4908,1.19*PI)
    m=np.array([0,np.sqrt(7.465e-5),np.sqrt(2.5093e-3)])*1e-9
    v=246.22
    mass_target=U.conj()@np.diag(m)@U.conj().T
    rows=[]
    for y in [0,.5,1,2,3]:
        z=1j*y
        R=np.array([[0,np.cos(z),np.sin(z)],
                    [0,-np.sin(z),np.cos(z)]],complex)
        Y=1j*np.sqrt(2*M)/v*R@np.diag(np.sqrt(m))@U.conj().T
        mnew=-v*v/(2*M)*Y.T@Y
        assert np.linalg.norm(mnew-mass_target)<1e-22
        # Theta = v Y^T/(sqrt2 M), low-energy non-unitarity / FCNC
        theta=v/(np.sqrt(2)*M)*Y.T
        epsilon=theta@theta.conj().T
        eps_trace=np.trace(epsilon).real
        eps_bound=sum(m)/M
        assert np.isclose(eps_trace,eps_bound*np.cosh(2*y),rtol=1e-11)
        # Higgs finite matching is scheme-dependent; display only a
        # convention-scaled threshold sensitivity, not a physical shift.
        sus=(3/(16*PI**2))*M**2*np.linalg.norm(Y)**2
        rows.append({"Im_Casas_Ibarra_angle":y,
                     "Tr_theta_theta_dagger":float(eps_trace),
                     "nonunitarity_e_mu_abs":float(abs(epsilon[0,1])),
                     "max_yukawa_abs":float(abs(Y).max()),
                     "reference_higgs_sensitivity_over_mh2":float(sus/125.25**2),
                     "light_mass_reconstruction_error_GeV":
                        float(np.linalg.norm(mnew-mass_target))})
    assert rows[0]["nonunitarity_e_mu_abs"]<1e-16
    assert rows[-1]["Tr_theta_theta_dagger"]>100*rows[0]["Tr_theta_theta_dagger"]
    return {
      "status":"PASS","M_triplet_GeV":M,
      "exact_trace_nonunitarity_lower_bound":float(sum(m)/M),
      "trace_formula":"Tr[theta theta†]=(m2+m3)/M*cosh(2 Im z)",
      "rows":rows,
      "interpretation":"One low-energy neutrino matrix permits exponentially different heavy-sector mixing and naturalness",
      "caveats":[
       "Type-III leptonic FCNC epsilon is not a branching-fraction or conversion-rate prediction without full Wilson matching.",
       "Experimental angles and splittings are inputs; heavy mass is chosen for illustrative unification.",
       "No thermal leptogenesis calculation; no inference of nonperturbative physics from this scan."]
    }


def spectral_positive_nonlocal():
    # Scalar positive-norm proxy: KL spectral representation
    # G_E(q)=Z/q+ integral rho(s)/(q+s) ds, Z>0, rho(s)>=0.
    # Thus q*G_E(q)>=Z for every q>0. Entire exponential damping
    # D(q)=Z exp(-q/M²)/q has qD/Z=exp(-q/M²)<1 for q>0:
    # no ordinary positive KL representation with the unit residue.
    qs=np.array([.001,.01,.1,1,2,10])
    qG=np.exp(-qs)
    violation=1-qG
    assert np.all(violation>0)
    # Compare a healthy massive scalar positive KL propagator, where
    # an extra positive pole only ENHANCES qG relative to massless Z.
    healthy=1+.35*qs/(qs+4)
    assert np.all(healthy>=1)
    return {
       "status":"PASS",
       "dimensionless_Euclidean_q_over_M2":qs.tolist(),
       "exponential_form_factor_q_times_propagator_over_residue":qG.tolist(),
       "minimal_KL_positivity_requirement":">=1",
       "strict_positivity_violations":violation.tolist(),
       "positive_extra_massive_state_comparator":healthy.tolist(),
       "analytic_proof":"If rho(s)>=0 and Z=1 then qG(q)=1+int q rho(s)/(q+s) ds >=1; exp(-q/M²)<1 contradicts for any q>0",
       "caveats":[
        "Only ordinary *scalar physical* KL positivity under Lorentz-invariant locality/tempered spectral assumptions; gauge-fixed gravitons are not positive-norm physical scalar propagators.",
        "A nonlocal action can evade standard KL assumptions, but no extra free poles is insufficient to establish interacting unitarity or reflection positivity.",
        "This does not disprove nonlocal quantum gravity or a fundamental TOE."]
    }


def _bao_arrays():
    z,y,kind,C=prior._source_bao()
    return np.asarray(z),np.asarray(y),np.asarray(kind),np.asarray(C)


def _templates_many(parameters,z,types):
    """Fully vectorized BAO shapes, excluding overall q=c/(H0 r_d)."""
    x=np.asarray(parameters)
    om=x[:,0,None,None]
    w0=x[:,1,None,None]
    wa=x[:,2,None,None]
    omrad=9e-5
    nodes,w=leggauss(48)
    unique=np.unique(z)
    zs=unique[None,:,None]
    zq=zs*(nodes[None,None,:]+1)/2
    one=1+zq
    expo=3*(1+w0+wa)*np.log(one)-3*wa*zq/one
    E2=om*one**3+omrad*one**4+(1-om-omrad)*np.exp(expo)
    E=np.sqrt(E2)
    integ=(unique[None,:]/2)*np.sum(w[None,None,:]/E,axis=-1)
    zz=unique[None,:]
    E2nodes=x[:,0,None]*(1+zz)**3+omrad*(1+zz)**4 + \
      (1-x[:,0,None]-omrad)*np.exp(
      3*(1+x[:,1,None]+x[:,2,None])*np.log1p(zz)
      -3*x[:,2,None]*zz/(1+zz))
    E_node=np.sqrt(E2nodes)
    d={float(k):j for j,k in enumerate(unique)}
    out=np.empty((len(x),len(z)),float)
    for i,(zi,typ) in enumerate(zip(z,types)):
        j=d[float(zi)]
        if typ=="DM_over_rs":out[:,i]=integ[:,j]
        elif typ=="DH_over_rs":out[:,i]=1/E_node[:,j]
        elif typ=="DV_over_rs":out[:,i]=(zi*integ[:,j]**2/E_node[:,j])**(1/3)
        else:raise ValueError(typ)
    return out


def _q_marginal_likelihood(theta,z,y,kind,C,qlo=20,qhi=40):
    t=_templates_many(theta,z,kind)
    Ci=np.linalg.inv(C)
    A=np.einsum("ni,ij,nj->n",t,Ci,t)
    B=t@(Ci@y)
    chi0=float(y@Ci@y)
    qhat=B/A
    chimin=np.maximum(chi0-B*B/A,0)
    upper=ndtr((qhi-qhat)*np.sqrt(A))
    lower=ndtr((qlo-qhat)*np.sqrt(A))
    weight=(upper-lower)
    # Physical evidence with uniform q prior, up to common data Gaussian
    L=np.sqrt(2*PI/A)/(qhi-qlo)*np.exp(-chimin/2)*weight
    assert np.all(np.isfinite(L)) and np.min(L)>=0
    return L


def bayes_BAO_prior_sensitivity():
    """True BAO-Gaussian model evidences, not combined cosmic posterior.
    Uniform priors [0.15,0.5] Omega_m; q [20,40], analytically integrated;
    w0,wa selected in two intervals. Nested QMC seeds report convergence.
    """
    z,y,kind,C=_bao_arrays()
    gauss,weights=leggauss(120)
    oms=.15+(.5-.15)*(gauss+1)/2
    base=np.c_[oms,-np.ones_like(oms),np.zeros_like(oms)]
    E_lcdm=float(np.dot(weights/2,
            _q_marginal_likelihood(base,z,y,kind,C)))
    assert E_lcdm>0
    priors=[
        {"name":"narrow_CPL","w0":[-1.5,-.5],"wa":[-2,2]},
        {"name":"broad_CPL","w0":[-2,0],"wa":[-4,4]},
        {"name":"phantom_free_canonical_CPL","w0":[-1,0],"wa":[0,2]}
    ]
    out=[]
    for prior in priors:
        ev=[]
        for seed in [7,13,29,41]:
            x=qmc.Sobol(d=3,scramble=True,seed=seed).random_base2(m=13)
            pars=np.column_stack([
              .15+.35*x[:,0],
              prior["w0"][0]+(prior["w0"][1]-prior["w0"][0])*x[:,1],
              prior["wa"][0]+(prior["wa"][1]-prior["wa"][0])*x[:,2],
            ])
            E=float(_q_marginal_likelihood(pars,z,y,kind,C).mean())
            ev.append(E)
        mean=float(np.mean(ev))
        out.append({
            "name":prior["name"],"prior_w0":prior["w0"],
            "prior_wa":prior["wa"],"evidence_rel_common_Gaussian_normalization":mean,
            "evidence_seed_samples":ev,"log_Bayes_factor_vs_LCDM":float(np.log(mean/E_lcdm)),
            "estimated_log_evidence_standard_error":
               float(np.std(ev,ddof=1)/(np.sqrt(len(ev))*mean)),
            "Sobol_points_per_scramble":8192})
    assert all(np.isfinite(x["log_Bayes_factor_vs_LCDM"]) for x in out)
    # For the canonical no-phantom CPL on z>=0, both w(a)>=-1:
    # w0>=-1, wa>=0. This is necessary but not sufficient for one scalar.
    return {
      "status":"PASS","data_source":"Cobaya public DESI DR2 13x13 compressed BAO Gaussian covariance",
      "only_BAO":True,"LCDM_evidence_rel_common_normalization":E_lcdm,
      "uniform_Omega_m_prior":[.15,.5],
      "uniform_q_c_over_H0rd_prior":[20,40],
      "results":out,
      "method":"Exact analytic integration of linear BAO distance scale q (truncated normal) and 4 scrambled Sobol sequences of 8192 points over Om,w0,wa",
      "limits":[
          "Not a full CMB/SNe/growth cosmological posterior or the DESI joint likelihood.",
          "Evidences depend strongly on chosen flat priors; these Bayes factors cannot be interpreted without explicit prior names.",
          "The q uniform prior is a modeling assumption, not a derived cosmological measure.",
          "48-point quadrature and radiation approximation; no massive neutrino Boltzmann transfer or DE perturbations.",
          "Nonphantom interval constrains only homogeneous CPL w(z>=0)>=-1, not full dynamical canonical scalar stability."
      ]
    }


def _pauli():
    X=np.array([[0,1],[1,0]],complex)
    Z=np.diag([1,-1]).astype(complex)
    return X,Z


def two_copy_photon_activation():
    # Four-mode Fock basis order (A1,B1,A2,B2), one photon per copy.
    state=np.zeros(16,complex)
    terms=[(1,0,1,0),(1,0,0,1),(0,1,1,0),(0,1,0,1)]
    def idx(bits):
        j=0
        for b in bits:j=2*j+b
        return j
    for bits in terms:state[idx(bits)]=.5
    assert np.isclose(np.vdot(state,state),1)
    # Locally allowed QND measurement of total occupancy at both labs,
    # before measurement settings. Accepted event is N_A=N_B=1.
    projected=np.zeros_like(state)
    for bits in terms:
        if bits[0]+bits[2]==1 and bits[1]+bits[3]==1:
            projected[idx(bits)]=state[idx(bits)]
    p_success=float(np.vdot(projected,projected).real)
    assert np.isclose(p_success,.5)
    projected/=np.sqrt(p_success)
    # Local dual rail basis: logical 0=(1,0), 1=(0,1).
    dual=np.zeros((2,2),complex)
    for bits in terms:
        a=(bits[0],bits[2]);b=(bits[1],bits[3])
        if sum(a)==sum(b)==1:
            ia=0 if a==(1,0) else 1
            ib=0 if b==(1,0) else 1
            dual[ia,ib]=projected[idx(bits)]
    assert np.allclose(dual,np.array([[0,1],[1,0]])/np.sqrt(2))
    X,Z=_pauli()
    ops_A=[X,Z]
    ops_B=[(X-Z)/np.sqrt(2),(X+Z)/np.sqrt(2)]
    psi=dual.ravel()
    E=np.array([[np.vdot(psi,np.kron(a,b)@psi).real
                     for b in ops_B] for a in ops_A])
    chsh=float(E[0,0]+E[0,1]+E[1,0]-E[1,1])
    assert abs(chsh-2*np.sqrt(2))<1e-12
    # Number-conserving local dual-rail beam splitters and phase shifters
    # can implement these logical Pauli measurements without a shared U(1)
    # phase reference; conditioned N_A=N_B=1 event is available locally.
    return {
       "status":"PASS","input":"two independent copies of (|10>+|01>)/sqrt2",
       "unconditional_local_number_herald_probability":p_success,
       "postselected_local_photon_numbers":[1,1],
       "conditional_2qubit_dualrail_wavefunction_real":dual.real.tolist(),
       "event_ready_ideal_CHSH":chsh,
       "correlation_matrix_E":E.tolist(),
       "ideal_two_photon_transmission_efficiency_cases":[.5,.8,.9,.95,1.],
       "herald_probability_with_independent_transmission_loss":[
          float(p_success*eta**2) for eta in [.5,.8,.9,.95,1.]],
       "resource_caveats":[
          "Accepted runs require local nondemolition number heralding before CHSH setting choices to avoid detection/postselection loophole.",
          "Source preparation, path coherence, interferometric stability, detector efficiency, finite statistics, cross-talk and extra modes ignored.",
          "This is known two-copy particle-entanglement activation (Wiseman/Vaccaro), not a new proof of Bell violations nor a TOE.",
          "Postselected CHSH says nothing about loophole-free Bell at finite loss unless all selection and measurement resources are accounted."
       ]
    }

def finite_statistical_photon_bell_resource():
    """Sixth cross-check: ideal CHSH game trials and a conservative
    Hoeffding local-realistic tail. Heralding must precede random settings.
    This is *not* a complete finite-sample Bell protocol or loophole audit.
    """
    target=1e-6
    p_quantum=.5+2*np.sqrt(2)/8
    p_local=.75
    delta=p_quantum-p_local
    n=int(np.ceil(np.log(1/target)/(2*delta**2)))
    bound=float(np.exp(-2*n*delta**2))
    assert 0<bound<=target
    eta=.8
    p_herald=.5*eta**2
    attempts=n/p_herald
    return {
      "status":"PASS",
      "ideal_CHSH_game_quantum_win_fraction":float(p_quantum),
      "local_game_win_fraction_bound":p_local,
      "one_sided_Hoeffding_pvalue_target":target,
      "minimum_ideal_valid_heralded_trials":n,
      "Hoeffding_upper_bound_at_target_N":bound,
      "independent_photon_transmission_eta":eta,
      "ideal_herald_success_probability":p_herald,
      "expected_source_pair_emissions_for_N":float(attempts),
      "caveats":[
       "Independent fair settings, independent Bernoulli wins and ideal detectors; expected win fraction is used as observed frequency.",
       "Hoeffding is a conservative null tail estimate, not an exact confidence interval nor actual experiment power calculation.",
       "QND herald occurs before settings and cannot reveal future settings; detection, memory, drift and postselection loopholes are unmodeled.",
       "Source emissions are expected counts under ideal Bernoulli survival, not worst-case high-probability counts."]
    }


def produce():
    r={
       "complete_2x24F_fixed_benchmark_threshold_scan":adjoint_full_threshold_recheck(),
       "typeIII_hidden_flavor_and_nonunitarity":type_iii_flavor_and_naturalness(),
       "nonlocal_form_factor_KL_positivity_gate":spectral_positive_nonlocal(),
       "DESI_DR2_bayesian_prior_sensitivity":bayes_BAO_prior_sensitivity(),
       "two_copy_photon_SSR_activation":two_copy_photon_activation()
    }
    assert all(x["status"]=="PASS" for x in r.values())
    return {"date":"2026-11-19","theory_of_everything_solved":False,
       "W33_used_as_physical_input":False,
       "description":"Five prior-art-aware physical consistency gates, one numerical benchmark scan and BAO model evidence under stated priors",
       "supplemental_event_ready_Bell_sample_resources":finite_statistical_photon_bell_resource(),
       "source_uris":[
        "https://github.com/CobayaSampler/bao_data/tree/master/desi_bao_dr2",
        "https://arxiv.org/abs/2504.18416",
        "https://doi.org/10.1103/PhysRevLett.91.097902",
        "https://doi.org/10.1038/s41550-025-02669-6",
        "https://www.sciencedirect.com/science/article/pii/S0370269307008775"
       ],
       "frontiers":r}


def main():
    result=produce()
    OUTPUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
    s=result["frontiers"]
    print(json.dumps({
       "status":"PASS",
       "fullSU5_mismatch":s["complete_2x24F_fixed_benchmark_threshold_scan"]["best_mismatch_norm"],
       "neutrino_e_mu_mixing":s["typeIII_hidden_flavor_and_nonunitarity"]["rows"][0]["nonunitarity_e_mu_abs"],
       "KL_spectral_positivity_violated":bool(min(s["nonlocal_form_factor_KL_positivity_gate"]["strict_positivity_violations"])>0),
       "BAO_prior_log_Bayes_factors":[x["log_Bayes_factor_vs_LCDM"] for x in s["DESI_DR2_bayesian_prior_sensitivity"]["results"]],
       "two_copy_photon_CHSH":s["two_copy_photon_SSR_activation"]["event_ready_ideal_CHSH"],
       "output":str(OUTPUT)}))


if __name__=="__main__":
    main()
