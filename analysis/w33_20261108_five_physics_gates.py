#!/usr/bin/env python3
"""Five-front adversarial W33 physics/computation workbench, 2026-11-08.

Each front reports its exact or numerical evidentiary status. Neither failed
root finding nor an algebraically allowed EFT term proves a physical vacuum.
"""
from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parents[1]

def _import(root):
    sys.path.insert(0,str(root/"analysis"))

def gauge_maxwell(root=ROOT):
    _import(root)
    import w33_20261108_s4_harmonic_qdual as S
    edges,faces,ei,B1,B2=S.complex27()
    Pgrad=B1.T@np.linalg.pinv(B1@B1.T,rcond=1e-12)@B1
    Pco=B2@B2.T/3
    Ph=np.eye(108)-Pgrad-Pco
    K=B2@B2.T
    e=np.linalg.eigvalsh(K)
    counts={"zero":int(np.count_nonzero(abs(e)<1e-9)),
            "three":int(np.count_nonzero(abs(e-3)<1e-9))}
    assert counts=={"zero":72,"three":36}
    assert abs(np.trace(Pgrad)-26)<1e-9
    assert abs(np.trace(Pco)-36)<1e-9
    assert abs(np.trace(Ph)-46)<1e-9
    assert np.max(abs(K@Ph))<1e-9
    assert np.max(abs(K@B1.T))<1e-9
    rng=np.random.default_rng(20261108)
    A=rng.normal(size=108);chi=rng.normal(size=27)
    err=abs(np.linalg.norm(B2.T@A)**2-np.linalg.norm(B2.T@(A+B1.T@chi))**2)
    Adot=rng.normal(size=108);A0=rng.normal(size=27);chidot=rng.normal(size=27)
    E=Adot-B1.T@A0
    E_gauge=Adot+B1.T@chidot-B1.T@(A0+chidot)
    electric_err=float(np.max(abs(E-E_gauge)))
    assert max(err,electric_err)<1e-10
    momentum={}
    for k in S.V:
        n0=sum(sum(k[j]*d[j] for j in range(3))%3==0 for d in S.DIRS) if hasattr(S,"DIRS") else sum(
            sum(k[j]*d[j] for j in range(3))%3==0 for d in ((1,0,0),(0,0,1),(1,1,1),(1,2,1)))
        grad=0 if k==(0,0,0) else 1
        co=n0
        harm=4-co-grad
        moment=momentum.setdefault(str((co,harm,grad)),0);momentum[str((co,harm,grad))]=moment+1
    assert momentum=={"(4, 0, 0)":1,"(2, 1, 1)":12,
                      "(1, 2, 1)":8,"(0, 3, 1)":6}
    return {"status":"EXACT_DISCRETE_CURL_MAXWELL_OBSTRUCTION_AND_NUMERICAL_CERTIFICATE",
      "vertices":27,"edges":108,"triangles":36,
      "orthogonal_chain_dimensions":{"gradient_gauge":26,"harmonic":46,"coexact":36},
      "magnetic_curvature_operator_eigenvalue_multiplicity":counts,
      "coexact_angular_frequency":"sqrt(3) in chosen unit kinetic normalization",
      "magnetic_gradient_shift_error":float(err),
      "temporal_gauge_covariant_electric_error":electric_err,
      "H1_zero_curvature_residual":float(np.max(abs(K@Ph))),
      "momentum_fibers_coexact_harmonic_gradient":momentum,
      "no_two_dispersing_photons_from_this_unmodified_action":True,
      "proof":"Use A0 as temporal 0-cochain and E=dot A-B1^T A0, B=B2^T A, S=int(1/2||E||^2-1/2||B||^2)dt. Under A->A+B1^T chi and A0->A0+dot chi, E and B are invariant because B1 B2=0. Gauss constraint is B1 E=0. Edge Hodge decomposition C1=im B1^T(26) + im B2(36) + H1(46); B2^T B2=3I yields K=B2B2^T=3Pcoexact.",
      "physical_limit":"This is a gauge-invariant quadratic DEC Maxwell fixture with A0 enforcing Gauss law, but it lacks a physical continuum/dispersion, photon selection, electric charges or coupling normalization. Other kinetic terms and matter representations may evade its spectral obstruction."}

def local_hamiltonians():
    """Two results: exact stability bound, and an explicitly non-exhaustive q5 search."""
    p=5
    directions=[(1,x,x*x%p) for x in range(p)]+[(0,0,1)]
    orbit=[]
    for v in directions:
        A=np.zeros((p,p,p))
        for s in range(1,p):A[tuple((s*x)%p for x in v)]=1
        orbit.append(A)
    sumO=np.sum(orbit,axis=0)
    a,b,c=np.indices((p,p,p))
    null=((a*c-b*b)%p==0)
    null[0,0,0]=False
    assert np.array_equal(sumO,null.astype(float))
    frequencies=np.array([np.fft.fftn(z).real for z in orbit])
    flat=p**-3
    def calc(w):
        phase=np.tensordot(w,frequencies,axes=(0,0))
        U=np.fft.ifftn(np.exp(-1j*phase))
        return abs(U)**2
    def objective(w):return float(np.mean((calc(w)-flat)**2))
    results=[]
    for seed in range(8):
        init=np.random.default_rng(seed).uniform(-math.pi,math.pi,size=6)
        sol=minimize(objective,init,method="BFGS",
                     options={"maxiter":140,"gtol":1e-9})
        results.append((float(objective(sol.x)),sol.x))
    best=min(results,key=lambda z:z[0])
    error=calc(best[1])-flat
    delta=p**(-1.5)-2*p**-2
    prob_gap=p**-3-4*p**-4
    assert delta>0 and prob_gap>0
    assert best[0]>0
    return {"status":"RIGOROUS_STABLE_NULL_LOCAL_COVARIANCE_BOUND_PLUS_BOUNDED_ANISOTROPY_FALSIFIER",
      "exact_theorem":"For a strictly null-supported, translation- and SL2(q)-congruence-covariant Hermitian H0, q odd prime power>=5, the earlier orbit theorem implies |exp(-itH0)_(0,d)| <=2/q^2. For H=H0+E, Duhamel gives |exp(-itH)_(0,d)| <= 2/q^2 + |t| ||E||op. Perfect flatness forces |t| ||E||op >= q^-3/2-2/q^2.",
      "q5_unitary_amplitude_deficit":delta,
      "q5_unitary_probability_deficit":prob_gap,
      "q5_6_null_direction_hopping_orbits":len(orbit),
      "q5_6_parameter_BFGS_seed_count":len(results),
      "q5_local_anisotropic_best_mean_squared_probability_error":best[0],
      "q5_local_anisotropic_best_max_probability_error":float(np.max(abs(error))),
      "q5_local_anisotropic_best_couplings":list(map(float,best[1])),
      "scope":"The BFGS run is not global, its nonzero residual is NOT a no-go, and a compact logical Clifford circuit is not a null-local continuous-time generator."}

def e6_spurions(root=ROOT):
    _import(root)
    import w33_pass11261_g26_cartan_coordinate_map as P
    old=P._load(root/"analysis/w33_pass11218_e8_cubic_cartan_kernel.py","fivefront_spurions")
    rec=old.load_parent().build_records()
    assert len(rec)==1620
    rng=np.random.default_rng(14062026)
    phi=rng.normal(size=81)+1j*rng.normal(size=81)
    M=np.zeros((81,81),complex)
    for u,x,o,c in rec:M[o,x]+=c*phi[u]
    assert np.max(abs(M+M.T))<1e-12
    assert np.linalg.matrix_rank(M,tol=1e-8)==78
    coeff=.4
    phin=phi/np.linalg.norm(phi)
    Bphi=np.outer(phin.conj(),phin.conj())
    assert np.linalg.matrix_rank(M+coeff*Bphi,tol=1e-8)==79
    # Distinct scalar multiplets Xi transforming in the same 81-dimensional
    # unitary representation can form separately invariant bilinears
    # (Xi^dagger chi)(Xi^dagger psi), if full matter-sector charges permit.
    spur=[]
    ranks=[78]
    sample=M.copy()
    for j in range(3):
        z=rng.normal(size=81)+1j*rng.normal(size=81)
        z/=np.linalg.norm(z)
        spur.append(z)
        sample+=coeff*np.outer(z.conj(),z.conj())
        ranks.append(int(np.linalg.matrix_rank(sample,tol=1e-8)))
    assert ranks==[78,79,80,81]
    det_phase=float(np.angle(np.linalg.slogdet(sample)[0]))
    assert math.isfinite(det_phase)
    return {"status":"NATIVE_E6_COVARIANT_FORMAL_SPURION_RANK_THREE_WITNESS",
      "signed_native_tensor_records":len(rec),"native_dimension":81,
      "native_rank":78,"rank_with_three_repetitions_of_one_scalar":[78,79],
      "rank_with_three_independent_extra_scalar_directions":ranks,
      "generic_complex_mass_determinant_phase_radians":det_phase,
      "spurion_form":"Sum_a (c_a/Lambda) (Xi_a^dagger chi)(Xi_a^dagger psi) + h.c., a=1,2,3; under a compact unitary common representation each factor is an invariant inner product.",
      "scope":"A representation-covariant EFT bilinear IF each Xi has the stated 81 representation and extra charges permit it. The three Xi are independently chosen generic vectors; no F/D-flat vacuum, SM chirality/anomaly assignment, selection rules, CP-real UV theory, observed masses or Nelson-Barr loop protection has been demonstrated.",
      "cp_warning":"Generic complex full-rank synthetic determinant has a phase: lifting zero modes does not solve strong CP. This determinant is NOT the physical down/up-quark determinant and is not theta-bar."}

def photonic_magic():
    w=np.exp(2j*np.pi/3)
    zeta9=np.exp(2j*np.pi/9)
    T=np.diag([1,zeta9,zeta9.conjugate()])
    psi=T@np.ones(3)/math.sqrt(3)
    X=np.roll(np.eye(3),1,axis=0)
    Z=np.diag([w**j for j in range(3)])
    image=T@X@T.conj().T
    matches=[]
    for a in range(3):
        for b in range(3):
            P=np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b)
            matches.append(abs(np.trace(P.conj().T@image)/3))
    max_clifford_pauli_overlap=float(max(matches))
    assert abs(max_clifford_pauli_overlap-1/math.sqrt(3))<1e-12
    assert np.max(abs(np.linalg.matrix_power(T,9)-np.eye(3)))<1e-12
    assert np.max(abs(T@Z@T.conj().T-Z))<1e-12
    W={}
    for q in range(3):
        for p in range(3):
            A=np.zeros((3,3),complex)
            for a in range(3):
                for b in range(3):
                    if (a+b-2*q)%3==0:A[a,b]=w**(p*(a-b)%3)
            W[str((q,p))]=float(np.real(np.vdot(psi,A@psi))/3)
    assert abs(sum(W.values())-1)<1e-12
    minW=min(W.values())
    mana=float(math.log(sum(abs(x) for x in W.values())))
    assert minW<-0.09 and mana>.4
    # Synthetic i.i.d. relative phase-error control on 27 rails.
    modes=27
    sigma=.05
    rng=np.random.default_rng(20261108)
    phase_errors=rng.normal(scale=sigma,size=(4000,modes))
    observed=np.abs(np.mean(np.exp(1j*phase_errors),axis=1))**2
    analytic=1/modes+(1-1/modes)*math.exp(-sigma*sigma)
    mean=float(np.mean(observed))
    assert abs(mean-analytic)<.001
    return {"status":"NON_CLIFFORD_CUBIC_NINTH_ROOT_MAGIC_WITH_SYNTHETIC_OPTICAL_PHASE_TEST",
      "cubic_phase":"diag(1,zeta9,zeta9^-1) from zeta9^(x^3), x=0,1,2",
      "third_root_cubic_phase_is_only_Pauli":"zeta3^(x^3)=zeta3^x for x in F3, so a third-root cubic phase alone is NOT a magic gate",
      "T9_is_identity":True,
      "best_pauli_normalizer_overlap":max_clifford_pauli_overlap,
      "T_is_nonclifford":True,
      "injected_state_qutrit_discrete_wigner":W,
      "wigner_minimum":minW,"wigner_L1":float(sum(abs(x) for x in W.values())),
      "log_wigner_negativity_mana":mana,
      "synthetic_independent_rail_phase_noise_sigma_rad":sigma,
      "synthetic_samples":len(observed),"analytic_expected_process_fidelity":analytic,
      "synthetic_mean_process_fidelity":mean,
      "phase_budget_limit":"Independent normal per-rail phase errors after an otherwise ideal unitary; NOT a complete propagation/fabrication/correlated-error loss model.",
      "physical_limit":"This is an algebraically injected non-Clifford resource and synthetic fidelity calculation, not a demonstrated photonic magic-state generator, efficient fault tolerance or a fabricated chip.",
      "prior_owners":["papers/forty_points/sec04_time.tex (cubic phase and Clifford boundary)",
                      "analysis/PASS20261108_ODD_PRIME_CLIFFORD_COMPILER.md"]}

def cosmology_audit(root=ROOT):
    uv=root/"analysis/toe_uv"
    sc=json.loads((uv/"scorecard.json").read_text(encoding="utf8"))
    survey={}
    for name,file in (("des_dovekie","shear_ppd.json"),
                      ("des_desy5","shear_ppd_desy5.json"),
                      ("kids_dovekie","shear_ppd_kids_dovekie.json")):
        data=json.loads((uv/file).read_text(encoding="utf8"))
        survey[name]={model:float(row["elpd_shear"]-data["LCDM"]["elpd_shear"])
                      for model,row in data.items()}
    assert all(survey[x]["CPL"]<survey[x]["free_neg"]<0 for x in survey)
    diffs={}
    for model,key in (("fading_cneg","free_neg"),("CPL","CPL")):
        base=sc[model]["oos_gain_dovekie"]
        des=survey["des_dovekie"][key]
        kids=survey["kids_dovekie"][key]
        combined=base+des+kids
        published=sc[model]["oos_gain_dovekie_plus_des_kids_shear"]
        assert abs(combined-published)<1e-10
        diffs[model]={"oos_bao_sn_heldout_gain":base,
             "des_shear_gain":des,"kids_shear_gain":kids,
             "combined_gain":combined}
    k2=json.loads((uv/"klt2_check.json").read_text(encoding="utf8"))
    ks=json.loads((uv/"klt2_scan.json").read_text(encoding="utf8"))
    kf=json.loads((uv/"klt_fit.json").read_text(encoding="utf8"))
    invalid=[key for d in (k2,ks) for key,v in d.items()
             if isinstance(v,dict) and "error" in v]
    assert len(invalid)>=5
    assert all("root must be bracketed" in v["error"]
               for d in (k2,ks) for v in d.values() if "error" in v)
    control=float(k2["control_f0.25"]["chi2"])
    ref=float(kf["klt_f0.25"]["chi2"])
    assert abs(control-ref)<.001
    ds=diffs["fading_cneg"]["combined_gain"]-diffs["CPL"]["combined_gain"]
    assert ds>4.3
    return {"status":"INDEPENDENT_LEDGER_ARITHMETIC_AND_IDENTIFIABILITY_AUDIT_NOT_RAW_LIKELIHOOD_REPLICATION",
      "survey_heldout_elpd_vs_LCDM":survey,
      "combined_Dovekie_decomposition":diffs,
      "fading_minus_CPL_combined":ds,
      "fading_exceeds_LCDM_in_both_individual_shear_holdouts":False,
      "klt_control_absolute_chi2_difference":abs(control-ref),
      "klt_root_bracketing_failures":invalid,
      "solver_error_is_proof_of_no_physical_solution":False,
      "uncertainty_calibration_available_in_committed_aggregates":False,
      "caveats":["Only 20 truncated Fisher samples per model reported; score uncertainties and full independent likelihood covariance are not in these aggregates.",
       "DES and KiDS have some overlapping survey footprint; simple elpd addition is a modelling approximation.",
       "The frozen S1 shear test favors fading relative to CPL but does not independently favor fading over LCDM.",
       "klt2_check f<=0.12 failures are root-bracketing errors; they do not show a mathematical nonexistence theorem.",
       "The gauge-discrete Z_N quality threshold is conditional on UV operator content, charges and coefficients; no discrete anomaly audit is supplied."],
      "external_independent_context":"KiDS-Legacy extended analysis arXiv:2512.11041 reports no significant w0wa improvement over LambdaCDM from KiDS shear + CMB lensing; this is background, not a validation of the repo's custom likelihood.",
      "physical_limit":"No rerun from raw KiDS/DES catalogues, no new CLASS likelihood fit, no observational significance or empirical TOE validation."}

def produce(root=ROOT):
    return {"schema":"w33.20261108.five_physics_gates.v1",
      "gauge":gauge_maxwell(root),
      "local_hamiltonian":local_hamiltonians(),
      "E6_three_scalar_spurions":e6_spurions(root),
      "photonic_nonclifford":photonic_magic(),
      "cosmology":cosmology_audit(root),
      "scope":"Five conditional constructive/falsification fronts. Exact finite proofs separated from numerical fixtures; no complete TOE or measured physical coupling."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--out",type=Path,default=Path("data/w33_20261108_five_physics_gates.json"))
    x=p.parse_args()
    d=produce(x.root)
    x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({"gauge_spectrum":d["gauge"]["magnetic_curvature_operator_eigenvalue_multiplicity"],
      "E6_ranks":d["E6_three_scalar_spurions"]["rank_with_three_independent_extra_scalar_directions"],
      "magic_mana":d["photonic_nonclifford"]["log_wigner_negativity_mana"],
      "KLT_solver_errors":len(d["cosmology"]["klt_root_bracketing_failures"]),
      "best_q5_local_mse":d["local_hamiltonian"]["q5_local_anisotropic_best_mean_squared_probability_error"]}))
if __name__=="__main__":main()
