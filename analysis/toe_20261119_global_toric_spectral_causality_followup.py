"""Five TOE next-step probes plus independent causal/quantum falsifiers.

Everything is CONDITIONAL mathematics on explicitly specified geometry, EFT,
gauge representation, vacuum or measurement operations; not a solved TOE.
"""
from pathlib import Path
from math import pi, sqrt, log, exp
import json
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.special import exp1
from toe_20261119_balanced_source_E8_cup_gate import sector_census
from toe_20261119_five_cracks_symmetry_adjoints_gravity_photons import su5_three_adjoint_completion

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_global_toric_spectral_causality_followup.json"


def e8_five_driver_full_singlet_vacuum():
    """Stable isolated branch of the eight charged-singlet TORIC quotient."""
    sector,_,_=sector_census()
    by={s["label"]:np.array(s["SU4_charge"],dtype=int)
        for s in sector if s["label"].startswith("S_")}
    names=["A","B","C","D","E","F","G1","G2"]
    charges=np.array([by["S_12"],-by["S_12"],by["S_13"],
                      by["S_14"],-by["S_14"],by["S_24"],
                      by["S_34"],by["S_34"]],int)
    invariants=[["A","B"],["D","E"],["A","F","E"],
                ["C","E","G1"],["C","E","G2"]]
    exponents=np.array([[a.count(n) for n in names] for a in invariants],int)
    assert np.array_equal(exponents@charges,np.zeros((5,3),int))
    assert int(sp.Matrix(exponents).rank())==5
    assert int(sp.Matrix(charges).rank())==3
    # A positive sum of the five neutral circuit exponent vectors
    # always solves the Abelian moment map with canonical Kähler metric.
    amplitude_squared=np.sum(exponents,axis=0)
    assert np.array_equal(amplitude_squared,[2,1,2,1,4,1,1,1])
    assert np.array_equal(charges.T@amplitude_squared,[0,0,0])
    vev=np.sqrt(amplitude_squared.astype(float))
    M=np.prod(vev[None,:]**exponents,axis=1)
    cutoff=10.
    suppress=np.array([cutoff**max(0,int(e.sum())-2) for e in exponents])
    # W=sum_i X_i (M_i(phi)-M_i(vev)) / cutoff^(degree(M_i)-2).
    # X_i neutral with R=2; all charged singlets have R=0.
    X=np.zeros(5,float)
    F_X=(M-M)/suppress
    # Hessian matrix of W at X=0: [[0,J^T],[J,0]];
    # J_ij = exponent_ij * M_i/(vev_j cutoff^k_i)
    J=(exponents*M[:,None]/vev[None,:])/suppress[:,None]
    H=np.zeros((13,13),float)
    H[:8,8:]=J.T
    H[8:,:8]=J
    rankJ=int(np.linalg.matrix_rank(J,tol=1e-10))
    rankH=int(np.linalg.matrix_rank(H,tol=1e-10))
    assert rankJ==5 and rankH==10
    # Complexified Abelian gauge tangent is in the kernel of J.
    tangents=vev[:,None]*charges
    assert np.linalg.norm(J@tangents)<1e-12
    assert int(np.linalg.matrix_rank(tangents))==3
    assert np.linalg.norm(H[:8,8:]@X)<1e-12
    # Baseline minimal supergravity modular gravitational anomaly =-21
    # from preceding 3x16 + 5x10 + 8xS plus Spin10+U1^3 gauginos;
    # each R=2 neutral driving field contributes +1.
    Agr=-21+5
    assert Agr%2==0
    # R(W)=2, including X_i products with neutral constants.
    return {
        "charged_field_order":names,
        "charge_matrix_rows":charges.tolist(),
        "five_monomials":["*".join(x) for x in invariants],
        "exponent_matrix":exponents.tolist(),
        "gauge_rank":int(np.linalg.matrix_rank(charges)),
        "invariant_exponent_rank":rankJ,
        "singlet_vev_magnitudes":vev.tolist(),
        "invariant_target_values":M.tolist(),
        "three_D_term_residual":(charges.T@amplitude_squared).tolist(),
        "F_driving_residual":F_X.tolist(),
        "F_charged_residual":(J.T@X).tolist(),
        "W_effective":"sum_{i=1}^5 X_i*(monomial_i(phi)-target_i)/Mcut^(degree_i-2)",
        "suppression_scales_from_chosen_cutoff":suppress.tolist(),
        "F_term_jacobian_rank":rankJ,
        "W_hessian_rank":rankH,
        "Hessian_kernel_gauge_dimension":13-rankH,
        "generic_complex_moduli_before_drivers":8-3,
        "local_complex_moduli_after_five_drivers":8-3-5,
        "linearized_gauge_orbit_coupling_norm":float(np.linalg.norm(J@tangents)),
        "Z4R_gravitational_coefficient_after_five_R2_neutral_drivers":Agr,
        "Z4R_gravitational_mod2":Agr%2,
        "conditional_result":"At this all-nonzero point five algebraically independent gauge invariants can be fixed by five R2-neutral drivers; all F,D vanish and the 13x13 superpotential Hessian has rank10, exactly 3 gauge-null directions. All local singlet-plus-driver moduli of this truncated toric model are lifted modulo complexified gauge.",
        "not_derived":"Five neutral driver fields, five nonzero target values, cutoff, global anomaly cancellation, compact E8/G2 origin, matter/Yukawa coupling coefficients, Kähler quantum corrections, gravitational superpotential and naturalness were inserted, not explained."
    }


def three_adjoint_radiative_sensitivity():
    """Use previous complete 3x24F one-loop solution, then perturb SU5 masses."""
    model=su5_three_adjoint_completion()
    mu=model["SU5_GUT_scale_chosen_GeV"]
    m3=np.array(model["SU2_triplet_masses_GeV"])
    m8=np.array(model["SU3_octet_masses_GeV"])
    mx=np.array(model["X_leptoquark_masses_GeV"])
    mz=91.1876; inv0=np.array([(3/5)*(1-.23122)*127.930,.23122*127.930,1/.1180])
    bsm=np.array([41/10,-19/6,-7.])
    b3=np.array([0.,4/3,0.]);b8=np.array([0.,0.,2.]);bx=np.array([10/3,2,4/3])
    def running(t,o,x):
        val=inv0-bsm*np.log(mu/mz)/(2*pi)
        for masses,b in ((t,b3),(o,b8),(x,bx)):
            val-=np.sum(np.log(mu/masses))*b/(2*pi)
        return val
    a0=running(m3,m8,mx)
    shifts=[]
    for eps in (1e-12,1e-10,1e-8,1e-6):
        delta=eps*mu
        t=m3+delta
        o=m8+delta
        x=mx+delta
        a=running(t,o,x)
        shifts.append({"heavy_matrix_additive_fraction":eps,
                       "delta_mass_GeV":delta,
                       "two_light_triplet_masses_GeV":t[:2].tolist(),
                       "light_octet_mass_GeV":float(o[2]),
                       "inverse_coupling_spread":float(np.ptp(a)),
                       "coupling_differences_12_13":[float(a[0]-a[1]),float(a[0]-a[2])]})
    # To hold octet mass within 10%, a common SU5-invariant mass
    # perturbation on its eigenvalue must be <= 0.1*m_oct, i.e.
    # much smaller than a generic order-one heavy mass shift.
    tolerance=0.1*min(m8)
    assert tolerance/mu<3e-13
    assert shifts[-1]["inverse_coupling_spread"]>1
    return {"original_three_adjoint_one_loop_spread":float(np.ptp(a0)),
            "original_low_octet_GeV":float(min(m8)),
            "original_light_triplet_GeV":float(min(m3)),
            "ten_percent_octet_absolute_shift_tolerance_GeV":tolerance,
            "ten_percent_octet_shift_relative_to_MU":tolerance/mu,
            "SU5_invariant_mass_shifts":shifts,
            "conclusion":"The one-loop three-adjoint counterexample exists, but a common perturbation of the SU5-invariant heavy mass matrix at merely 1e-6*MU destroys its light-octet and light-triplet thresholds. No protecting symmetry or full radiative stability is demonstrated."}


def spin_c_global_family_gate():
    """Spin^c CP2 index and charge-selective flat holonomy."""
    # On CP2 with generator H of H^2, signature sigma=1,
    # w2=H(mod2); determinant line c1(L)=kH therefore k MUST be odd.
    # Atiyah-Singer Spin^c index = (k^2 - signature)/8.
    vals=[]
    for k in range(-9,10):
        admissible=(k%2)==1
        index=(k*k-1)/8
        vals.append({"c1_coefficient":k,"Spin_c_admissible":admissible,
                     "formal_index":index if admissible else None})
        if admissible: assert float(index).is_integer()
    def twist_residue(alpha,q,theta):
        return float(((alpha+q*theta/(2*pi)+.5)%1)-.5)
    twists=[]
    for charge in (0,1,2,3):
        residue=twist_residue(.5,charge,pi)
        twists.append({"fermion_U1_charge":charge,
                       "antiperiodic_spin_and_pi_Wilson_residue_cycles":residue,
                       "zero_momentum_possible":abs(residue)<1e-12})
    assert [r["zero_momentum_possible"] for r in twists]==[False,True,False,True]
    return {
        "internal_base":"CP2 compact Euclidean four-manifold, NOT four-dimensional physical Lorentzian spacetime",
        "signature":1,
        "w2_generator_parity":1,
        "Spin_c_index_formula":"index D_L=(k^2-1)/8, only k odd because c1(L)=w2(TM) mod 2",
        "flux_index_table":vals,
        "k_plus5_index":3,
        "CP2_not_spin":True,
        "CP2_observed_families_NOT_derived":True,
        "charge_specific_torus_holonomy_cancellation":twists,
        "takeaway":"Global spin-gauge structure constrains which charged fermions exist and permits index 3 for the *chosen* flux k=5, but topology does not determine k, the SM representation, dynamics or whether a suitable 7D compactification contains this sector."
    }


def causal_link_valency_diagnostic():
    """Exact Poisson expected Hasse-link count and 4D lightcone nonlocality."""
    from scipy.special import exp1
    from numpy import euler_gamma
    density=[40,160,640,2560,10240,40960]
    out=[]
    kappa=pi/24
    for rho in density:
        # 1+1 Alexandrov null square (0<u<1,0<v<1), origin at (0,0).
        a=rho/2
        E2=float(euler_gamma+log(a)+exp1(a))
        # 3+1 future cone truncated by coordinate time T=1.
        # Integrate E[L]=rho int d^4x exp[-rho V4(0,x)].
        # s=t²-r²; integrate t analytically.
        def one(s):
            if s==0:return 1.
            if s>=1:return 0.
            z=sqrt(1-s)
            return z-s*log((1+z)/sqrt(s))
        E4=pi*rho*quad(lambda s:np.exp(-rho*kappa*s*s)*one(s),
                       0,1,epsabs=1e-9,epsrel=1e-9,limit=160)[0]
        # E4 -> pi sqrt(6)*sqrt(rho) for T=1.
        out.append({"rho":rho,"E_links_1plus1_diamond":E2,
                    "E_links_3plus1_truncated_cone":E4,
                    "E4_over_sqrt_rho":E4/sqrt(rho),
                    "E2_over_log_rho":E2/log(rho)})
    assert all(out[i+1]["E_links_3plus1_truncated_cone"]>out[i]["E_links_3plus1_truncated_cone"] for i in range(5))
    assert all(out[i+1]["E_links_1plus1_diamond"]>out[i]["E_links_1plus1_diamond"] for i in range(5))
    coeff=pi*sqrt(6)
    assert abs(out[-1]["E4_over_sqrt_rho"]/coeff-1)<.12
    return {"reference_intensity":"Poisson sprinkling intensity rho in fixed Minkowski coordinate regions",
            "E2_exact":"gamma_E+log(rho/2)+E1(rho/2), 1+1 null square with u,v in (0,1)",
            "E4_integral":"pi*rho*int_0^1 ds exp[-rho*pi*s^2/24]*(sqrt(1-s)-s*log((1+sqrt(1-s))/sqrt(s))), 3+1 future cone 0<t<1",
            "E4_large_rho_asymptotic":"pi*sqrt(6)*sqrt(rho) for T=1",
            "E4_asymptotic_coefficient":coeff,
            "sampled":out,
            "locality_implication":"Lorentz-invariant nearest-link causal graph has unbounded expected link valence as density grows even on fixed finite regions; naive fixed-degree local exchange/energy cost is not Lorentz invariant.",
            "limitation":"Known causal-set light-cone nonlocality, not a new gravity law or energy-consumption theorem. 1+1 and 3+1 cases use different stated regions and count links from a fixed origin."
    }


def pure_quantum_state_nonuniqueness():
    """Two-event causal commutator admits infinitely many distinct pure states."""
    delta=np.array([[0.,1.],[-1.,0.]])
    H=1j*delta
    records=[]
    for r in (0.,.2,.7,1.2):
        # <phi_a phi_b> = real symmetric V + i Delta/2.
        V=np.diag([exp(2*r),exp(-2*r)])/2
        W=V+H/2
        eig=np.linalg.eigvalsh(W)
        assert eig.min()>-1e-13
        assert abs(np.linalg.det(V)-.25)<1e-12  # pure Gaussian oscillator state
        assert np.max(abs(W-W.T-H))<1e-12
        assert abs(np.linalg.det(W))<1e-12 # rank-one pure complex covariance
        records.append({"squeezing_r":r,
                        "positive_W_eigenvalues":eig.tolist(),
                        "position_variance":float(V[0,0]),
                        "momentum_variance":float(V[1,1]),
                        "symmetrized_variance_det":float(np.linalg.det(V)),
                        "commutator_error":float(np.max(abs(W-W.T-H)))})
    assert records[0]["position_variance"]!=records[-1]["position_variance"]
    return {"two_event_causal_commutator":"iDelta where Delta=[[0,1],[-1,0]]",
            "pure_state_family":"W_r=diag(exp(2r),exp(-2r))/2 + iDelta/2",
            "state_samples":records,
            "Sorkin_Johnston_positive_part":"r=0 for the chosen counting Euclidean inner product",
            "counterexample":"Positivity + exact commutator + Gaussian purity DO NOT uniquely select a quantum vacuum. r varies continuously; a further metric, inner-product, stationarity, entropy or state-selection rule is needed.",
            "limitations":"Finite one-oscillator/quasifree CCR toy example, not a Hadamard relativistic continuum or interacting quantum dynamics. The established SJ prescription supplies an ADDITIONAL positive spectral-part selection once a counting inner product is chosen."
    }


def phase_noisy_two_copy_photons():
    """Exact Horodecki CHSH for dephased heralded two-copy dual-rail pair."""
    sx=np.array([[0,1],[1,0]],complex)
    sy=np.array([[0,-1j],[1j,0]],complex)
    sz=np.diag([1,-1]).astype(complex)
    pauli=(sx,sy,sz)
    results=[]
    for sigma in (0.,.2,.6,1.,2.):
        vis=exp(-sigma*sigma/2)
        rho=np.zeros((4,4),complex)
        rho[1,1]=rho[2,2]=.5
        rho[1,2]=rho[2,1]=vis/2
        white_weight=.82
        mixed=white_weight*rho+(1-white_weight)*np.eye(4)/4
        def CHSH_max(state):
            T=np.array([[float(np.trace(state@np.kron(A,B)).real)
                         for B in pauli] for A in pauli])
            s=np.linalg.svd(T,compute_uv=False)
            return 2*sqrt(s[0]**2+s[1]**2)
        raw=CHSH_max(rho);noisy=CHSH_max(mixed)
        assert abs(raw-2*sqrt(1+vis**2))<1e-12
        assert abs(noisy-2*white_weight*sqrt(1+vis**2))<1e-12
        results.append({"phase_difference_sigma_radians":sigma,
                        "visibility":vis,"ideal_conditional_CHSH_max":raw,
                        "CHSH_max_with_white_weight_0p82":noisy,
                        "minimum_white_weight_to_violate":1/sqrt(1+vis**2)})
    assert results[0]["CHSH_max_with_white_weight_0p82"]>2
    assert results[-1]["CHSH_max_with_white_weight_0p82"]<2
    return {
        "protocol":"two independent distributed one-photon copies with pre-setting one-photon-per-lab herald",
        "phase_assumption":"Gaussian relative phase difference phi1-phi2, mean 0 and standard deviation sigma; visibility E cos(delta phi)=exp(-sigma²/2)",
        "CHSH_formula":"Smax=2*w*sqrt(1+visibility²), w=white-noise Bell fraction",
        "samples":results,
        "transmission_eta_0p8_ideal_QND_herald_probability":.5*.8**2,
        "two_photons_consumed_per_emission_pair":2,
        "physical_cost":"Without coherence between the two sources, visibility vanishes and number-conserving Bell violation disappears. Shared timing/phase or indistinguishability is a measured resource, not an invisible free axiom.",
        "limitations":"No full loophole-free detector, QND herald, source independence, memory effects or asymmetric loss model; all correlation formulas are ordinary quantum mechanics."
    }


def main():
    out={
        "E8_full_singlet_driver_completion":e8_five_driver_full_singlet_vacuum(),
        "three_adjoint_GUT_stability":three_adjoint_radiative_sensitivity(),
        "global_Spin_c_chirality":spin_c_global_family_gate(),
        "causal_link_locality":causal_link_valency_diagnostic(),
        "quantum_pure_vacuum_nonuniqueness":pure_quantum_state_nonuniqueness(),
        "photonic_phase_visibility":phase_noisy_two_copy_photons()
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    for k in out:print("PASS",k)
    print("5-driver Hessian rank",out["E8_full_singlet_driver_completion"]["W_hessian_rank"])
    print("Gravity R parity",out["E8_full_singlet_driver_completion"]["Z4R_gravitational_mod2"])
    print("4D link ratio",out["causal_link_locality"]["sampled"][-1]["E4_over_sqrt_rho"])
    print("GUT 1e-6 shift",out["three_adjoint_GUT_stability"]["SU5_invariant_mass_shifts"][-1]["inverse_coupling_spread"])
    print(OUT)
    return out

if __name__=="__main__":main()
