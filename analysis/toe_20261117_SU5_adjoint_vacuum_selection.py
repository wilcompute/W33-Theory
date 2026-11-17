"""Independent 2026-11-17 theory of 3+2 vacuum selection.

NOT derived from W33. Builds on ordinary SU(5) adjoint Higgs invariant
quartics, finite global A5/S5 symmetry, and eigenvalue rearrangement.

Results:
(i) exact global quartic invariant bound on traceless Hermitian 5x5;
(ii) explicit renormalizable parameter region selecting 3+2;
(iii) distinction between 10 gauge-equivalent placements versus
10 physically distinct choices under global discrete permutation;
(iv) independent dynamical rank-two projector field provides a
gauge-invariant RELATIVE alignment mechanism;
(v) Z2 sign-domain-wall warning and cubic sign bias.
"""
import itertools,json,math,sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261117_SU5_adjoint_quartic_context_selector.json"

def even(p):
    return sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2==0

def quartic_extrema():
    # At constrained critical points sum xi=0, sum xi^2=1:
    # 4xi^3 - 2lambda xi -mu=0. Hence <=3 distinct roots.
    # If 3 distinct roots, the cubic lacks x^2 term, so a+b+c=0.
    # With positive multiplicities n1+n2+n3=5, solving sum ni ri=0
    # gives one root zero and two opposite. Only (3,1,1) or (2,2,1)
    # partitions occur, yielding Q=1/2 or 1/4 respectively.
    # Two-root extrema of multiplicities k,5-k yield Q below.
    two={}
    for k in range(1,5):
        Q=F((5-k)**3+k**3,25*k*(5-k))
        two[k]=Q
    assert two=={1:F(13,20),2:F(7,30),3:F(7,30),4:F(13,20)}
    three={"3_1_1":F(1,2),"2_2_1":F(1,4)}
    vals=list(two.values())+list(three.values())
    assert min(vals)==F(7,30) and max(vals)==F(13,20)
    # The compact normalized traceless sphere has extrema;
    # all extrema lie in the enumerated critical patterns.
    u=np.array([2,2,2,-3,-3],dtype=float)/math.sqrt(30)
    assert math.isclose(sum(u),0,abs_tol=1e-15)
    q=sum(u**4)
    assert math.isclose(q,7/30,rel_tol=0,abs_tol=1e-14)
    lam=2*s.Rational(7,30)
    tangent_eigs=[12*s.Rational(4,30)-2*lam,
                  12*s.Rational(9,30)-2*lam]
    assert tangent_eigs==[s.Rational(2,3),s.Rational(8,3)]
    return {"exact_critical_point_classification":{
              "two_distinct_eigenvalues_Q_by_multiplicity":{str(k):str(v) for k,v in two.items()},
              "three_distinct_eigenvalues_Q_by_partition":{k:str(v) for k,v in three.items()},
              "proof":"Lagrange stationarity gives cubic in each xi with vanishing quadratic coefficient. Thus at most three roots. If three distinct, their sum is zero; trace and multiplicity constraints force a zero root and opposite remaining roots, with patterns (3,1,1) or (2,2,1). Two-root partitions give Q=((5-k)^3+k^3)/(25*k*(5-k)). Compactness proves the bound.",
              "global_minimum_Q":"7/30","global_maximum_Q":"13/20"},
            "normalized_3plus2_eigenvalues":["2/sqrt(30)"]*3+["-3/sqrt(30)"]*2,
            "angular_constrained_hessian_eigenvalues":{"SU3_traceless_2_modes":"2/3",
                                                       "SU2_traceless_1_mode":"8/3"},
            "all_local_shape_eigenvalues_positive":True}

def landau_potential(mass2=1,lam=0.35,kappa=0.75):
    assert mass2>0 and kappa>0 and lam+kappa*7/30>0
    def energy(Q):
        g=lam+kappa*float(Q)
        return -(mass2**2)/(4*g)
    Q32=F(7,30);Q41=F(13,20); Q221=F(1,4)
    rsq=mass2/(2*(lam+kappa*float(Q32)))
    assert energy(Q32)<energy(Q221)<energy(Q41)
    assert rsq>0
    return {"potential":"V=-m²Tr(Phi²)+lambda(TrPhi²)²+kappa TrPhi⁴; Phi traceless Hermitian; no cubic",
      "parameter_region_sufficient":"m²>0, kappa>0, lambda+(7/30)kappa>0",
      "example":{"m2":mass2,"lambda":lam,"kappa":kappa,"VEV_norm_squared":rsq,
                 "energy_SU3_SU2_U1":energy(Q32),
                 "energy_2_2_1":energy(Q221),"energy_SU4_U1":energy(Q41),
                 "SU4_minus_SM_energy_gap":energy(Q41)-energy(Q32)},
      "broken_generator_count":12,
      "SU5_adjoint_dimension":24,"SM_subalgebra_dimension":12,
      "gauge_mass_squared_ratio":"m_X² proportional to g5²*v²*(5/sqrt30)² (convention-dependent)",
      "nonsupersymmetric_caveat":"A legitimate renormalizable bosonic SU5 adjoint potential; not derived as the scalar potential of the repo's F/D-flat supersymmetric E6 superpotential."}

def contextual_orbits():
    G=[p for p in itertools.permutations(range(5)) if even(p)]
    pairs=list(itertools.combinations(range(5),2))
    assert len(G)==60 and len(pairs)==10
    for p in pairs:
        orb={tuple(sorted((g[p[0]],g[p[1]]))) for g in G}
        assert len(orb)==10
        stab=sum(tuple(sorted((g[p[0]],g[p[1]])))==p for g in G)
        assert stab==6
    # Every permutation matrix (including odd) has an SU5 representative
    # for conjugation of diagonal Phi: for odd P, multiply by a diagonal
    # determinant -1 sign matrix D to make PD in SU5. D commutes with
    # diagonal Phi, and PD conjugates Phi exactly like P.
    return {"A5_order":60,"distinct_unordered_two_subsets":10,
      "A5_stabilizer_each":6,
      "Z2_even_potential_3plus2_diagonal_minima":20,
      "SU5_gauge_orbit_statement":"All 10 placements of fixed-sign (2,2,2,-3,-3) are conjugate by SU5, hence gauge-equivalent if SU5 is gauged; 10 physical domain types do not follow from a gauge-Weyl orbit.",
      "global_discrete_case":"If labels instead transform under a genuinely global A5, 10 placements of each sign are physically distinct degenerate minima. A macroscopic system may spontaneously choose one and form interfaces/domain walls; this does not prove such a global A5 exists.",
      "Z2_warning":"Because V is Phi->-Phi even, opposite-sign eigenvalue multisets are NOT conjugate by SU5. Imposing this exact global Z2 introduces two gauge-inequivalent vacuum orbits; TrPhi³ term explicitly biases sign and can lift the degeneracy.",
      "theory_sources":["https://www.scholarpedia.org/article/Grand_unification",
                        "https://doi.org/10.1103/PhysRevD.12.3978",
                        "https://doi.org/10.1103/PhysRevD.62.123506"]}

def relative_rank2_alignment(VEV=1,bias=0.2):
    assert VEV>0 and bias>0
    phi=np.array([2,2,2,-3,-3],dtype=float)*VEV/math.sqrt(30)
    # Q is a second dynamical Hermitian rank-2 projector, e.g. Q=S S^dagger
    # from a Stiefel 5x2 frame S. It transforms Q->U Q U^-1 under SU5.
    # Vportal=+bias Tr(Phi Q). Von Neumann/Ky Fan variational principle:
    # global minimum is sum two lowest eigenvalues. Unique negative-eig
    # two-plane for Phi with 3+2 spectrum.
    cases=[]
    for inds in itertools.combinations(range(5),2):
        nlow=sum(i>=3 for i in inds)
        tr=float(sum(phi[i] for i in inds))
        cases.append({"two_plane_indices":list(inds),"low_eigen_occupancy":nlow,
                      "portal_energy":bias*tr})
    counts=dict(sorted(CounterLike(r["low_eigen_occupancy"] for r in cases).items()))
    assert counts=={0:3,1:6,2:1}
    E=np.array([r["portal_energy"] for r in cases])
    ground=float(min(E))
    assert sum(abs(e-ground)<1e-12 for e in E)==1
    gap=bias*5*VEV/math.sqrt(30)
    assert math.isclose(sorted(set(np.round(E,12)))[1]-sorted(set(np.round(E,12)))[0],gap,rel_tol=1e-9)
    # For continuous rotation mixing one negative eigenvector with
    # positive eigenvector, DeltaV=gap*sin²(theta), exact.
    for th in (0,.2,.5,1.1,math.pi/2):
        qrot=np.array([math.sin(th),0,0,math.cos(th),0])
        Q=np.outer(qrot,qrot)+np.diag([0,0,0,0,1])
        delta=bias*np.trace(np.diag(phi)@Q)-ground
        assert math.isclose(delta,gap*math.sin(th)**2,rel_tol=1e-12,abs_tol=1e-14)
    return {"dynamical_field":"Q=S S†, S complex 5x2 with S†S=I2; Q²=Q=Q† and TrQ=2",
      "gauge_invariant_portal":"V_align = +epsilon Tr(Phi Q); Phi and Q transform by common SU5 conjugation",
      "Ky_Fan_ground_state":"Unique rank-two projector onto the doubly degenerate smallest eigenvalue (-3v/sqrt30) subspace of Phi",
      "counts_for_a_fixed_diagonal_Phi":counts,
      "fixed_gauge_relative_orientations":cases,
      "unique_relative_orbit_minimum":True,
      "smallest_discrete_excitation_energy":gap,
      "continuous_misalignment_cost":"Delta V = (5 epsilon v/sqrt30) sin(theta)^2 when one weak eigenvector rotates into a colour eigenvector",
      "physical_interpretation":"Relative orientation of TWO dynamical Higgs/order-parameter fields is gauge invariant. This mechanism aligns them; it does not turn SU5 gauge-related placements of both fields into physically distinct vacua.",
      "open_E6_tasks":"Find a gauge-invariant E6 or supersymmetric completion giving a positive kappa adjoint shape potential and a dynamical rank2 field, with all F/D equations, proton and triplet masses, and radiative/thermal consistency."}

def CounterLike(items):
    from collections import Counter
    return Counter(items)

def optimize_restarts(seed=20261117,restarts=60):
    # Independent non-symbolic search across traceless R4 sphere.
    from scipy.optimize import minimize
    rng=np.random.default_rng(seed)
    values=[]
    for _ in range(restarts):
        start=rng.normal(size=4)
        def objective(v):
            x=np.r_[v,-sum(v)]
            return float(sum(x**4)/sum(x*x)**2)
        res=minimize(objective,start,method="BFGS",
                     options={"gtol":1e-8,"maxiter":1000})
        if abs(res.fun-7/30)>1e-7:
            # Homogeneous objective occasionally causes BFGS precision
            # loss; retry the same start with derivative-free refinement.
            res=minimize(objective,res.x,method="Nelder-Mead",
                options={"xatol":1e-9,"fatol":1e-12,"maxiter":10000})
        assert abs(res.fun-7/30)<1e-7
        values.append(float(res.fun))
    return {"optimizer":"SciPy BFGS with 4 free diagonal coordinates and an exactly imposed traceless fifth coordinate",
            "random_seed":seed,"independent_restarts":restarts,
            "min_Q_observed":min(values),"max_Q_observed":max(values),
            "all_restarts_reached_7_over_30":True,
            "not_a_substitute_for_exact_global_proof":True}

def verify():
    a=quartic_extrema();b=landau_potential();c=contextual_orbits()
    e=relative_rank2_alignment();f=optimize_restarts()
    return {"status":"PASS_SU5_ADJOINT_3PLUS2_GLOBAL_VACUUM_AND_RELATIVE_CONTEXT_ALIGNMENT",
      "exact_global_quartic_bounds":a,
      "landau_vacuum":b,"gauge_vs_global_orbit":c,
      "second_projector_alignment":e,"numerical_multistart_stress":f,
      "claim_level":"Exact bosonic SU5 adjoint and projector toy-model mechanism; not derived from E6 dynamics, does not prove Standard Model masses/couplings or any TOE."}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["landau_vacuum"]["example"]["SU4_minus_SM_energy_gap"])
