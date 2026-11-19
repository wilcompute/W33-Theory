"""Pascal/Sierpinski parity kinetic matrices, exact mass spectra, thermal
partition and mass-dispersive two-copy U1-SSR CHSH.

All exact identities from Lucas and matrix Kronecker algebra; PHENOMENOLOGY
is explicitly a counterexample, not a fundamental mass derivation.
"""
from __future__ import annotations
from collections import Counter
from math import comb, exp, log, pi, sqrt
from pathlib import Path
import json
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_pascal_sierpinski_mass_spectrum.json"
PHI=(1+sqrt(5))/2

def lucas_pascal(level):
    assert level>=1
    N=1<<level
    return np.array([[int((k & ~n)==0) for k in range(N)]
                     for n in range(N)],dtype=np.int64)

def exact_dyadic(level):
    # [[1,0],[1,1]] is the 2-adic Lucas digit transition.
    A=np.array([[1,0],[1,1]],dtype=np.int64)
    kron=np.array([[1]],dtype=np.int64)
    for _ in range(level): kron=np.kron(kron,A)
    M=lucas_pascal(level)
    assert np.array_equal(M,kron)
    assert np.all(np.diag(M)==1) and np.all(M==np.tril(M))
    # Singular values = φ^(2j-L), with binomial multiplicity C(L,j).
    spectrum=[]
    for j in range(level+1):
        mult=comb(level,j)
        spectrum.append({"j":j,"multiplicity":mult,
                         "mass_singular_value":PHI**(2*j-level),
                         "Gram_eigenvalue":PHI**(4*j-2*level)})
    assert sum(v["multiplicity"] for v in spectrum)==M.shape[0]
    measured=np.linalg.svd(M.astype(float),compute_uv=False)
    pred=sorted([v["mass_singular_value"] for v in spectrum
                 for _ in range(v["multiplicity"])],reverse=True)
    assert np.allclose(measured,pred,rtol=1e-10,atol=2e-12)
    assert abs(np.prod(measured)-1)<2e-8
    return {"level":level,"square_matrix_dimension":len(M),
            "ones_in_parity_mask":int(M.sum()),
            "Kronecker_Lucas_exact":True,
            "det_unimodular":1,"spectrum":spectrum,
            "extreme_mass_ratio":PHI**(2*level),
            "massless_min_singular":PHI**(-level),
            "spectral_binomial_degeneracy":True}

def finite_mass_determinant(level,m2):
    M=lucas_pascal(level).astype(float)
    eig=np.linalg.eigvalsh(M.T@M)
    direct=float(np.sum(np.log(eig+m2)))
    pred=sum(comb(level,j)*log(m2+PHI**(4*j-2*level))
             for j in range(level+1))
    assert abs(direct-pred)<1e-7
    return direct

def three_family_corner():
    M=s.Matrix([[1,0,0],[1,1,0],[1,0,1]])
    eigen=(M*M.T).eigenvals()
    assert eigen=={s.Integer(1):1,2-s.sqrt(3):1,2+s.sqrt(3):1}
    masses=[sqrt(2-sqrt(3)),1.,sqrt(2+sqrt(3))]
    ratio=masses[-1]/masses[0]
    # Charged lepton masses MEV from PDG 2025/2026 rounded reference
    observed={"electron_MeV":.51099895,"muon_MeV":105.6583755,
              "tau_MeV":1776.93}
    observed_ratio=observed["tau_MeV"]/observed["electron_MeV"]
    assert observed_ratio>3000 and ratio<4
    assert (observed["muon_MeV"]/observed["electron_MeV"])>200
    # Even restricting to three families inside an 8D dyadic Pascal
    # 2^3=8 all eigenpairs have degeneracies 1,3,3,1: no canonical
    # identification of three observed families by symmetry alone.
    return {"3x3_principal_corner_M":str(M),
      "3x3_Gram_exact_eigenvalues":["2-sqrt(3)","1","2+sqrt(3)"],
      "dimensionless_singular_values":masses,
      "max_to_min_ratio":ratio,
      "charged_leptons_input_MeV":observed,
      "charged_lepton_tau_e_ratio":observed_ratio,
      "charged_lepton_mu_e_ratio":observed["muon_MeV"]/observed["electron_MeV"],
      "naive_fixed_coefficients_3x3_pascal_spectrum_fails_mass_hierarchy":True,
      "dyadic_family_number_is_power_of_two_not_three":True}

def flavor_embedding_and_kinetic_nonidentifiability():
    M=lucas_pascal(3)
    one_hot=[1,2,4]
    corner=M[np.ix_(one_hot,one_hot)]
    assert np.array_equal(corner,np.eye(3,dtype=np.int64))
    # Any desired strictly positive 3-generation singular values can be
    # fitted by an *unconstrained* Hermitian positive right kinetic metric.
    # That is loss of predictivity, not a mechanism deriving lepton masses.
    P=s.Matrix([[1,0,0],[1,1,0],[1,0,1]])
    e,mu,tau=(.51099895,105.6583755,1776.93)
    D=s.diag(s.Rational(str(e))/s.Rational(str(tau)),
             s.Rational(str(mu))/s.Rational(str(tau)),1)
    KR=P.T*D.inv()**2*P
    assert KR==KR.T
    assert KR.det()>0
    # P KR^-1 P^T = D², exact after positive-metric canonical normalization.
    assert s.simplify(P*KR.inv()*P.T-D**2)==s.zeros(3,3)
    kn=np.array(KR,float)
    w=np.linalg.eigvalsh(kn)
    assert min(w)>0
    return {"one_hot_indices":one_hot,
            "one_hot_three_family_pascal_submatrix":corner.tolist(),
            "one_hot_mass_eigenvalues_identical":True,
            "kinetic_metric_construction":"K_R=P3^T D^-2 P3, D=diag(m_e/m_tau,m_mu/m_tau,1); Ycanon=P3 K_R^-1/2 has singular values EXACTLY D",
            "any_positive_target_spectrum_admits_a_fitted_positive_KR":True,
            "kinetic_metric_eigenvalues":w.tolist(),
            "kinetic_metric_condition_number":float(max(w)/min(w)),
            "physics_caution":"Off-diagonal kinetic mixing can be forbidden by family charges or localized gauge geometry; the algebraic fit does not prove such a kinetic metric is physically allowed. If one allows arbitrary positive wavefunction metrics, parity alone predicts no mass ratios."}

def weighted_odd_pascal(level,alpha,beta):
    # n<2^L and k subset-of-bits n; exactly 3 choices/digit.
    pred=1.
    for j in range(level):
        q=1<<j
        pred*=1+exp(-alpha*q)+exp(-(alpha+beta)*q)
    direct=sum(exp(-alpha*n-beta*k) for n in range(1<<level)
               for k in range(n+1) if k & ~n==0)
    assert abs(pred-direct)<1e-9*max(1,pred)
    return float(pred)

def gaussian_delta_chsh(x):
    # Relative phase Δ=(ΔE) (δt_1−δt_2) with independent timing jitters
    # δti~N(0,sigma_t²), x=(ΔE)*sigma_t in natural units.
    coherence=exp(-x*x)
    return 1+sqrt(1+coherence**2)

def two_copy_verification():
    # Each local-number-one sector is the 2-qubit maximally correlated
    # state with coherence c (a Bell diagonal mixture of ψ+ and ψ-).
    # Horodecki T eigenvalues 1,c,c => Smax=2sqrt(1+c²).
    # p=1/2 number-one, p=1/4 each classical 0 and 2 sectors -> 1+sqrt(1+c²).
    table=[]
    for x in (0.,.25,.5,1.,2.,3.):
        c=exp(-x*x)
        rho=np.zeros((4,4),dtype=complex)
        rho[1,1]=rho[2,2]=.5
        rho[1,2]=rho[2,1]=c/2
        X=np.array([[0,1],[1,0]])
        Y=np.array([[0,-1j],[1j,0]])
        Z=np.diag([1.,-1.])
        T=np.array([[np.trace(rho@np.kron(a,b)).real
                    for b in (X,Y,Z)] for a in (X,Y,Z)])
        e=np.linalg.eigvalsh(T.T@T)
        S=2*sqrt(e[-1]+e[-2])
        assert abs((1+S/2)-gaussian_delta_chsh(x))<1e-12
        table.append({"dimensionless_phase_jitter_DeltaE_sigma_t":x,
            "sector_coherence":c,"optimal_CHSH_under_strict_SSR":1+S/2,
            "maximally_correlated_sector_CHSH":S})
    assert abs(table[0]["optimal_CHSH_under_strict_SSR"]-(1+sqrt(2)))<1e-12
    assert abs(gaussian_delta_chsh(7)-2)<1e-12
    return {"table":table,"proof":"Two copies, independent phases, local U1 charge SSR, number sectors 0/2 classical with total weight1/2, number-one 2x2 Bell-diagonal sector of weight1/2. T^T T eigenvalues (1,c²,c²). S=1+sqrt(1+c²), c=exp[-(DeltaE*sigma_t)^2]. This is a known Horodecki-type two-qubit optimization, not a new quantum law.",
     "important_common_mode":"If phase noise is common to both copies, phi_1-phi_2=0 and CHSH remains exactly 1+sqrt2 no matter how broad the COMMON unknown phase is.",
     "mass_caution":"Photons have no established nonzero rest mass; DeltaE is an inserted modal energy splitting and sigma_t is independent timing jitter. If applied to massive interference modes, group velocity, propagation and detector models need independent calculations. The Pascal parity resource controls the ideal SSR sectors, not a mass derived from geometry."}

def run():
    dyadic=[exact_dyadic(L) for L in range(1,7)]
    determinants=[{"level":L,"mass_squared":m2,
                   "logdet_Gram_plus_m2":finite_mass_determinant(L,m2)}
                  for L in (2,3,4,5) for m2 in (0.,.01,.1,1.)]
    weighted=[{"L":L,"alpha":a,"beta":b,"Z":weighted_odd_pascal(L,a,b)}
            for L in (1,2,3,5,8)
            for a,b in ((0.,0.),(.1,.3),(.5,.0))]
    assert all(abs(z["Z"]-3**z["L"])<1e-12 for z in weighted
               if z["alpha"]==z["beta"]==0)
    three=three_family_corner()
    n_needed=next(l for l in range(1,30)
                  if PHI**(2*l)>=three["charged_lepton_tau_e_ratio"])
    assert n_needed==9
    result={"model":"Lucas parity matrix P_L[n,k]=C(n,k) mod2, 0<=n,k<2^L",
       "Kronecker_digit_matrix":"[[1,0],[1,1]]",
       "selfsimilar_singular_values":"s_j=phi^(2j-L) with multiplicity C(L,j); all have product1",
       "selfsimilar_Gram_eigenvalues":"lambda_j=phi^(4j-2L)",
       "massive_logdet":"sum_j C(L,j)log(m²+phi^(4j-2L)), with real dimensionless m inserted",
       "levels":dyadic,"three_family_raw_pascal":three,
       "flavor_kinetic_metric_nonidentifiability":flavor_embedding_and_kinetic_nonidentifiability(),
       "smallest_dyadic_level_with_large_enough_extreme_ratio":n_needed,
       "corresponding_2power_family_dimension":1<<n_needed,
       "fractal_weighted_odd_count_partition":"Z_L(alpha,beta)=prod_{j=0}^{L-1}(1+exp(-2^j alpha)+exp(-2^j(alpha+beta)))",
       "Hausdorff_dimension_of_ideal_binary_pascal_support":log(3)/log(2),
       "weighted_partition_examples":weighted,
       "massive_logdet_checks":determinants,
       "mass_dependent_two_copy_SSR":two_copy_verification(),
       "NO_GO":"Exact parity-only P_L has 2^L states, binomial degeneracies and at L<=3 far too little mass hierarchy for e/mu/tau; L>=9 reaches range at cost of >=512 states and nontrivial multiplicities. A mass scale, canonical kinetic metric, family projection, radiative corrections and interaction geometry must be supplied independently.",
       "not_the_same_as":"Spectral decimation of a Sierpinski gasket graph Laplacian requires a separately specified adjacency/hopping and boundary normalization; parity support alone does not define a physical Laplacian or particle rest masses. Do not mix these two spectral questions.",
       "sources":["Lucas theorem combinatorics; https://math.mit.edu/~rstan/ec/ec1.pdf",
                  "Repo previous conditional SSR CHSH law analysis/toe_20261119_multicopy_particle_ssr_pascal_chsh.py",
                  "Mass observations PDG https://pdg.lbl.gov/2026/listings/particle_properties.html",
                  "Sierpinski graph Laplacian spectral-decimation prior art https://arxiv.org/abs/1709.02031"]}
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print("PASS Pascal masses phi^(2j-L), weighted Sierpinski partition, 3gen hierarchy NO-GO, dephased SSR CHSH")
    print("P3 max ratio",three["max_to_min_ratio"],"tau/e",three["charged_lepton_tau_e_ratio"],"needed level",n_needed)
    print("mass-SSR CHSH",[(r["dimensionless_phase_jitter_DeltaE_sigma_t"],round(r["optimal_CHSH_under_strict_SSR"],6)) for r in result["mass_dependent_two_copy_SSR"]["table"]])
    print(OUT)
    return result
if __name__=="__main__":run()
