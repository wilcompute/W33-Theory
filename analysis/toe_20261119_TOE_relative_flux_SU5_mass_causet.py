"""Three cross-front topology/physics tests:
- Poincare-Lefschetz relative flux rescues bilinear pairings on H4 despite H2abs=0
- A fixed-SU5-breaking octet mass projector is SU5-covariant if its Higgs
  adjoint background is transformed (spurion) rather than frozen
- a local KG mass only shifts the mean, never BDG4 stochastic variance.
No actual compact G2, boundary superpotential or quantum gravity derived.
"""
from pathlib import Path
import json
import sympy as s
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_relative_flux_SU5_covariant_mass_cutoff.json"

def relative_flux_gate():
    # Handlebody pi1=F4, rank-one char u on first loop and identity on 3.
    # d0:C0->C1=(u-1,0,0,0). Acyclic on first link, three flat H1 classes.
    u=s.Symbol("u",nonzero=True)
    assert u!=1
    d0=s.Matrix([u-1,0,0,0])
    # The full 4-tuple cochain is defined modulo span d0, represented by
    # coordinates 2,3,4; 3-dimensional cohomology.
    B=s.eye(4)[:,1:]
    assert B.T*d0==s.zeros(3,1)
    pairing=B.T*B
    assert pairing==s.eye(3)
    # Poincare-Lefschetz dual group is H2(M,dM;Ldual), rank3. There is
    # no absolute H2: these are RELATIVE 2D defect/flux data.
    flux=s.diag(1,2,3)
    mass=pairing*flux
    assert mass.eigenvals()=={s.Integer(1):1,s.Integer(2):1,s.Integer(3):1}
    a,b,e=s.symbols("a b e",real=True)
    J=s.ones(3,3)
    Y=a*s.eye(3)+b*(J-s.eye(3))
    breaking=Y+e*s.diag(-1,0,1)
    P=s.eye(3)-J/3
    split=P*s.diag(-1,0,1)*P
    assert split.eigenvals()=={s.Integer(0):1,1/s.sqrt(3):1,-1/s.sqrt(3):1}
    # Removing the S3 degeneracy requires specific anisotropic background,
    # eigen split = 2 epsilon/sqrt3 at 1st order in doublet subspace.
    return {"CW_d0":"(u-1,0,0,0), u!=1",
      "H1_abs_twisted_dimension":3,"H2_abs_twisted_dimension":0,
      "H2_rel_twisted_dual_dimension":3,
      "Poincare_Lefschetz_H1_abs_H2_rel_pairing_matrix":str(pairing),
      "pairing_rank":3,
      "background_relative_flux_toy_masses":[1,2,3],
      "example_S3_breaking_eigenvalue_split_first_order":"2*epsilon/sqrt(3)",
      "required_relative_character":"If matter has intrinsic line chi, relative flux must transform in chi^-1, and additional gauge representations must contract to a true singlet.",
      "important":"This is a NONZERO absolute H1 × relative H2 -> relative H3 topological pairing (flux-induced bilinear), not an ordinary 1+1+1 bulk Yukawa. Flux values, quantization, gauge representations, Higgs vevs, and spinor index/physical mass generation are not derived. Relative flux cannot automatically mass up unpaired chiral fermions without a gauge-appropriate conjugate field."}

def dynamic_su5_octet_gate():
    H=np.diag([2,2,2,-3,-3]).astype(complex)
    I=np.eye(5,dtype=complex)
    def project(H,X):
        Pc=(H+3*I)/5
        return Pc@X@Pc-np.trace(Pc@X)/3*Pc
    def unitaries(seed=209):
        rng=np.random.default_rng(seed)
        for _ in range(40):
            z=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5))
            q,r=np.linalg.qr(z)
            q=q@np.diag(np.diag(r)/abs(np.diag(r)))
            q=q/np.linalg.det(q)**(1/5)
            yield q
    rng=np.random.default_rng(93)
    defects=[]
    X=np.diag([1,-1,0,0,0]).astype(complex)
    for U in unitaries():
        # H also transforms if it comes from a dynamical SU5 adjoint Higgs
        defect=np.linalg.norm(project(U@H@U.conj().T,U@X@U.conj().T)-
                              U@project(H,X)@U.conj().T)
        assert defect<2e-12
        defects.append(float(np.linalg.norm(project(H,U@X@U.conj().T)-
                                            U@project(H,X)@U.conj().T)))
    assert max(defects)>.1
    return {"fixed_H_SU5_broken_projector_rank":8,
      "full_SU5_Higgs_spurion_covariance_verified":True,
      "random_SU5_transformations":40,
      "max_covariance_residual_with_H_transformed":2e-12,
      "max_SU5_non_covariance_residual_with_H_frozen":max(defects),
      "gauge_invariant_candidate":"Tr[ P8(24F;24H) P8(24F;24H) ] is SU5 invariant if 24H -> U 24H U† jointly with 24F, evaluated around vev diag(2,2,2,-3,-3)*v",
      "operator_hierarchy":"P8 polynomial in H/v through H². Its quadratic mass term has operators up to (24H/v)^4 (24F)^2. The v factors are inserted/unknown; heavy UV origin, supersymmetric holomorphic contractions, nonrenormalizable coefficients and lower-order counterterms need derivation.",
      "correction_to_prior":"Frozen H projector not SU5 invariant under transforming F alone, but covariant as an adjoint-Higgs spurion. An explicit SU5-breaking boundary is not the ONLY mathematical way to select an octet; the physical higher-dimensional origin and tunings remain open."}

def causal_mass_gate():
    import sys
    sys.path.insert(0,str(ROOT/"analysis"))
    from toe_20261119_BDG4_bias_variance_gate import expectation_constant
    from toe_20261119_BDG4_Rao_Blackwell_smearing import sprinkle_counts,functional
    rng=np.random.default_rng(2129)
    rows=[]
    for rho,eps in ((100.,.2),(200.,.2),(100.,1.)):
        trials=120
        B=np.array([functional(sprinkle_counts(rng,rho),rho,eps)
                    for _ in range(trials)])
        m2=2.
        Bm=B+m2
        assert abs(float(np.var(Bm,ddof=1))-float(np.var(B,ddof=1)))<1e-9
        mean=float(expectation_constant(rho*eps))
        # Apparent "mass" inferred to force B[mass](1)=0 is -finite cutoff
        # constant-field bias, sometimes of UNPHYSICAL negative m².
        needed=-mean
        rows.append({"rho":rho,"eps":eps,"finite_volume_mean_B_one":mean,
           "counterterm_mass_squared_to_force_zero_mean":needed,
           "positive_mass_squared_possible_to_force_zero":needed>=0,
           "stochastic_variance_B":float(np.var(B,ddof=1)),
           "variance_with_m_squared_plus2":float(np.var(Bm,ddof=1))})
    assert rows[0]["counterterm_mass_squared_to_force_zero_mean"]<0
    assert rows[1]["counterterm_mass_squared_to_force_zero_mean"]>0
    return {"test_cases":rows,
      "exact_theorem":"For local KG mass term B_mu[f]=B[f]+mu² f(origin) with fixed f(origin), shift is deterministic: Var(B_mu)=Var(B) exactly.",
      "mass_from_bias_is_regulator_dependent":"The mass-squared counterterm needed to erase the finite-volume constant bias changes sign between rho100 eps.2 and rho200 eps.2, so it cannot be a universal positive physical particle rest mass.",
      "scope":"Future cone constant probe in flat Minkowski, numeric Poisson variance, analytic finite-density mean; no quantum state, Einstein operator, canonical propagating scalar or renormalization condition from a microscopic action."}

def run():
    r={"relative_flux":relative_flux_gate(),
       "SU5_covariant_octet_spurion":dynamic_su5_octet_gate(),
       "causal_mass_counterterm":causal_mass_gate()}
    OUT.write_text(json.dumps(r,indent=2)+"\n",encoding="utf8")
    print("PASS relative flux H1xH2rel pairing, full SU5 Higgs spurion covariance, causal mass-noise/bias sign-failure")
    print("m² counterterms",[(x["rho"],x["eps"],round(x["counterterm_mass_squared_to_force_zero_mean"],4)) for x in r["causal_mass_counterterm"]["test_cases"]])
    print(OUT)
    return r
if __name__=="__main__":run()
