#!/usr/bin/env python3
"""2026-11-19: Five linked TOE fronts + two cross-sector tests.

Constructive spatial causal-nerve topology; SU2 reflection-positive transfer
kernels that remain non-unique; causal/thermal state ambiguity; oscillatory KR
entropy versus coherence; generation-dependent hypercharge anomaly families.
All structures are explicitly conditional. THIS DOES NOT SOLVE A TOE.
"""
from __future__ import annotations
from itertools import combinations
from math import comb, cos, exp, isclose, log, log10, pi, sin
from pathlib import Path
import cmath
import json
import numpy as np
import sympy as sp
from scipy.integrate import quad

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261119_causal_nerve_transfer_interference_flavor_v6.json"

def gf2rank(matrix):
    a=np.array(matrix,dtype=np.uint8).copy()%2
    row=0
    for col in range(a.shape[1]):
        if row>=a.shape[0]:break
        sel=np.flatnonzero(a[row:,col])
        if not len(sel):continue
        idx=row+int(sel[0])
        a[[row,idx]]=a[[idx,row]]
        for j in range(row+1,a.shape[0]):
            if a[j,col]:a[j]^=a[row]
        row+=1
    return row

def causal_ring_order(n,r):
    """Bipartite causal order of spacelike A at t=0 and future witness W.
    Use cylinder metric only to GENERATE R; topology algorithm gets R alone.
    """
    R=np.zeros((2*n,2*n),dtype=np.uint8)
    for a in range(n):
        for w in range(n):
            if min((a-w)%n,(w-a)%n)<=r:
                R[a,n+w]=1
    assert not np.any(np.diag(R))
    return R

def betti_from_nerve_order(R,n):
    """Dowker nerve of future witness past-shadows, computed FROM R alone.

    Each witnessed antichain point selects a maximal simplex consisting
    of the future events whose past shadows contain it.
    Only 0/1 Betti numbers need k<=2 simplices.
    """
    maxsimp=[tuple(n+w for w in range(n) if R[a,n+w]) for a in range(n)]
    faces=[]
    for k in (1,2,3):
        faces.append(sorted(set(s for maximal in maxsimp for s in combinations(maximal,k))))
    ranks=[]
    for k in (1,2):
        small={v:i for i,v in enumerate(faces[k-1])}
        B=np.zeros((len(faces[k-1]),len(faces[k])),dtype=np.uint8)
        for col,s in enumerate(faces[k]):
            for t in combinations(s,k):
                B[small[t],col]=1
        ranks.append(gf2rank(B))
    b0=len(faces[0])-ranks[0]
    b1=len(faces[1])-ranks[0]-ranks[1]
    return {"betti_H0_H1_mod2":[int(b0),int(b1)],
            "nerve_face_counts_0_1_2":[len(x) for x in faces],
            "GF2_boundary_ranks_1_2":ranks,
            "maximal_shadow_sizes":[len(x) for x in maxsimp]}

def causal_spin_topology_gate():
    n=12;rows=[]
    for r in range(6):
        order=causal_ring_order(n,r)
        ans=betti_from_nerve_order(order,n)
        rows.append({"future_lightcone_shadow_radius_in_antichain_spacings":r,
                     "inferred_from_order_only":ans,
                     "candidate_Z2_spin_holonomy_sectors":2**ans["betti_H0_H1_mod2"][1]})
    b1=[x["inferred_from_order_only"]["betti_H0_H1_mod2"][1] for x in rows]
    assert b1==[0,1,1,0,0,0]
    # Fermion boundary twists are assigned after recovering H1; topology
    # classifies choices but DOES NOT choose a physical spin structure.
    spectra=[]
    for twist in (0.,pi):
        ks=2*pi*np.arange(n)/n+twist/n
        # anti-Hermitian central lattice derivative's spectrum is sin k.
        zero=sum(abs(sin(float(k)))<1e-12 for k in ks)
        spectra.append({"spin_winding_pi":twist,
                        "naive_derivative_zero_modes":zero,
                        "minimum_squared_massless_Dirac_eigenvalue":float(np.min(np.sin(ks)**2))})
    assert [x["naive_derivative_zero_modes"] for x in spectra]==[2,0]
    return {"status":"PASS",
        "synthetic_space":"1+1 Lorentzian cylinder A spatial circle, periodic n=12; coordinates only generate the bipartite relation",
        "order_based_Dowker_nerve_at_shadow_scales":rows,
        "stable_H1_plateau_radii":[1,2],
        "two_supplementary_spin_transport_spectra":spectra,
        "analysis":"An order-only thickened-antichain nerve CAN recover H1 when the whole bounded-order complex is contractible. The spin lift and charged parallel transport are still independent choices.",
        "known_prior_art":"Major et al 2007, stable homology of causal sets 2009; Tsilioukas arXiv:2611.06102 with full causal-neighborhood topology-changing numerical implementation.",
        "limit":"This is a synthetically embedded 1+1 cylinder with a chosen distinguished antichain/landmarks and resolution, not a Lorentzian fermion theory or intrinsic 3+1 manifold-selection algorithm."}

def sf(phi):return 1.-cos(phi)
def s_mixed(phi,lam):
    sfv=sf(phi)
    return sfv-.5*lam*sfv*sfv

def transfer_coeff(beta,lam,n):
    # χ_(n/2)(U)=sin[(n+1)phi]/sin(phi) and Haar dμ=(2/pi)sin²phi dphi.
    return quad(lambda t:(2/pi)*sin(t)*sin((n+1)*t)*exp(-beta*s_mixed(t,lam)),
                0,pi,epsabs=1e-13)[0]

def gauge_transfer_gate():
    # n = 2j, j SU2 spin.  c_j>=0 is positive type and sufficient
    # for a positive plaquette-crossing transfer kernel; numerical values
    # cross-check analytic positive type proof below.
    rows=[]
    for lam in (0.,.25,.5,.75,1.):
        coeff=[transfer_coeff(2.,lam,n) for n in range(9)]
        assert coeff[0]>.0
        assert min(coeff)>-1e-11
        transfer=[float(c/((n+1)*coeff[0])) for n,c in enumerate(coeff)]
        assert all(x>=-1e-11 for x in transfer)
        rows.append({"lambda_adj_mixture":lam,
             "character_coefficients_n_0_to_8":coeff,
             "normalized_transfer_eigenvalues_n_0_to_8":transfer,
             "fundamental_Wilson_mean":float(coeff[1]/(2*coeff[0])),
             "admissible_nonnegative_character_coefficients_tested":True})
    assert rows[0]["fundamental_Wilson_mean"]>.43
    assert abs(rows[-1]["fundamental_Wilson_mean"])<1e-13
    # Sign-invariant center-blind action excludes all half-integer channels.
    for n in (1,3,5,7):
        assert abs(rows[-1]["character_coefficients_n_0_to_8"][n])<2e-12
    # Exact positive-type argument: weight ∝ exp[β(1−λ)χ_1/2/2]
    #                                  exp[βλχ_1/8],
    # both factors have nonnegative character-product series at β>=0
    # and 0<=λ<=1. The product is still positive type.
    for phi in (.1,.8,2.9):
        for lam in (0.,.25,.5,.75,1.):
            lhs=-2*s_mixed(phi,lam)
            # remove center-independent constant
            rhs=2*((1-lam)*cos(phi)+(lam/4)*cos(2*phi))+(-2+1.5*lam)
            assert abs(lhs-rhs)<1e-12
    return {"status":"PASS","SU2_Haar_spins_n":"j=n/2, n=0..8",
      "fixed_bare_beta":2,"reflection_positive_mixed_action_family":rows,
      "exact_all_angle_action":"S_lambda=S_fund-lambda S_fund²/2; identical θ²/8 to leading order for all lambda",
      "positive_type_factorization":"w_lambda(U) proportional to exp[beta(1-lambda) χ_f(U)/2] exp[beta lambda χ_adj(U)/8]; because representations and their tensor products have nonnegative fusion multiplicities, coefficients are nonnegative for 0<=lambda<=1.",
      "main_new_test":"Nonnegative character/transfer spectra for all five sampled lambda show positivity does not uniquely select fundamental vs adjoint or the center sector.",
      "limit":"A one-plaquette SU2 transfer/character test, not a proof of Osterwalder-Schrader positivity for arbitrary coupled dynamical fermion/gravity lattice systems."}

def thermal_states_from_transfer_gate(gauge):
    # One fixed microscopic transfer kernel induces representation-sector
    # energies E_j=-log(lambda_j), but different allowed lambda give
    # different spectra and quantum states despite same weak-field action.
    rows=[]
    for rec in gauge["reflection_positive_mixed_action_family"]:
        eig=rec["normalized_transfer_eigenvalues_n_0_to_8"]
        j1=eig[1]
        energy_fund=float(-log(j1)) if j1>1e-13 else None
        # For adjoint-only action the spin-1/2 sector has ZERO weight,
        # rather than a finite-energy charged state.
        rows.append({"lambda_adj_mixture":rec["lambda_adj_mixture"],
                     "fundamental_transfer_eigenvalue":j1,
                     "effective_one_step_spin_half_energy_if_allowed":energy_fund,
                     "fundamental_sector_is_absent_in_strict_adjoint":j1<1e-13})
    assert rows[0]["effective_one_step_spin_half_energy_if_allowed"] is not None
    assert rows[-1]["effective_one_step_spin_half_energy_if_allowed"] is None
    # fixed retarded oscillator Green function and variable KMS state
    w=1.7;t=.41
    quantum=[]
    for beta in (.4,2.,10.):
        n=1/np.expm1(beta*w)
        ret=sin(w*t)/w
        sym=(n+.5)*cos(w*t)/w
        quantum.append({"inverse_temperature":beta,"retarded_G":ret,
                        "KMS_noise":float(sym),"oscillator_energy":float(w*(n+.5))})
    assert len({x["retarded_G"] for x in quantum})==1
    assert quantum[0]["KMS_noise"]>3*quantum[-1]["KMS_noise"]
    return {"status":"PASS","transfer_derived_effective_sector_energies":rows,
      "same_causal_response_distinct_KMS_states":quantum,
      "cross_sector_conclusion":"Reflection-positive transfer matrices CAN produce candidate Hamiltonians, but a continuum of admissible microscopic actions gives inequivalent spectra, center-sensitive Hilbert sectors, and state-selection rules; positivity alone does not fix the Born/physical vacuum.",
      "limitation":"Transfer energies are per arbitrary lattice time step, not measured particle masses or unique relativistic clocks."}

def interference_entropy_gate():
    # Three-layer KR-like labeled family with M=N²/4 independent
    # adjacent-layer relations, S=theta L.
    theta=2.5
    rows=[]
    for N in (8,16,32,64):
        M=N*N//4
        absolute_base=2*abs(cos(theta/2))
        ratio_base=abs(cos(theta/2))
        logabs=M*log10(absolute_base)
        logrelative=M*log10(ratio_base)
        incoherent_log10=M*log10(2)
        rows.append({"N":N,"independent_links_M":M,
            "log10_number_of_labeled_histories":incoherent_log10,
            "log10_absolute_coherent_partition_magnitude":logabs,
            "log10_coherent_vs_unsigned_amplitude_ratio":logrelative,
            "coherence_shortfall_max_log10_for_total_weight_below_1":-incoherent_log10,
            "coherent_absolute_amplitude_falls_with_size":logabs<0})
    assert all(x["coherent_absolute_amplitude_falls_with_size"] for x in rows)
    # exact finite sum 65536 histories at N=8 by binomial degeneracies.
    M=16
    brute=sum(comb(M,k)*cmath.exp(1j*theta*k) for k in range(M+1))
    closed=(1+cmath.exp(1j*theta))**M
    assert abs(brute-closed)<1e-10
    # The quantum decoherence functional D=(1-gamma)I+gamma vv† is
    # positive for 0<=gamma<=1 on each finite finite set of histories.
    # Yet any finite incoherence component contributes (1-gamma)*2^M
    # to the all-histories event, and overwhelms coherent cancellation
    # as M grows: NO classical probability interpretation of the phase sum.
    klist=[0,1,3,5,8,13]
    v=np.array([cmath.exp(1j*theta*k) for k in klist])
    decoh=[]
    for gamma in (0.,.5,1.):
        D=(1-gamma)*np.eye(len(v))+gamma*np.outer(v,v.conj())
        ev=np.linalg.eigvalsh(D)
        assert np.min(ev)>-1e-12
        decoh.append({"coherent_fraction_gamma":gamma,
                      "minimum_eigenvalue":float(np.min(ev)),
                      "all_histories_weight_small_sample":float((np.ones(len(v))@D@np.ones(len(v))).real)})
    # Note if all unlabelled histories are identified differently, correct
    # automorphism weights and coherence of histories must be addressed.
    return {"status":"PASS","theta_radians_per_link":theta,
       "critical_phase_for_absolute_suppression_radians":2*pi/3,
       "closed_form_Z":"Z_N(theta)=(1+exp(i theta))^{N²/4}",
       "coherent_interference_condition":"2*abs(cos(theta/2))<1 for absolute amplitude suppression in this toy family",
       "size_scaling_records":rows,
       "N8_direct_complex_sum_real_imag":[brute.real,brute.imag],
       "N8_closed_sum_real_imag":[closed.real,closed.imag],
       "partial_decoherence_PSD_certificates":decoh,
       "decoherence_full_family_identity":"For D=(1-gamma)I+gamma vv†, A(all histories)=(1-gamma)2^M+gamma*abs(Z_N(theta))². Unless 1-gamma is exponentially small in M, incoherent history entropy survives.",
       "qualifier":"Exact KR-like 3-layer labeled subclass, linear link-phase ansatz, coherent/decohered family model only. DOES NOT show 3+1 Einstein phase dominance or a physical consistent-histories quantum measure."}

def species():
    fields=[]
    # left-handed Weyl fields with integer y=6Y.
    specs=[("Q",6,1,1,1),("uc",3,-4,-1,0),("dc",3,2,-1,0),
           ("L",2,-3,0,1),("ec",1,6,0,0),("nc",1,0,0,0)]
    for f in range(3):
        for name,mult,y,t,s in specs:
            # X=L_mu-L_tau, Nc and ec are charge-conjugate fields.
            sign=(1 if f==1 else (-1 if f==2 else 0))
            X=sign*(1 if name=="L" else -1 if name in ("ec","nc") else 0)
            fields.append({"generation":f,"multiplet":name,
                "multiplicity":mult,"y":y,"triality":t,"weak_doublet":s,"X":X})
    return fields

def anomalies(fields,k):
    z=[(r,sp.Integer(r["y"])+6*k*r["X"]) for r in fields]
    return {
      "U1_cube":sp.expand(sum(r["multiplicity"]*y**3 for r,y in z)),
      "grav_U1":sp.expand(sum(r["multiplicity"]*y for r,y in z)),
      "SU2_squared_U1":sp.expand(sum(3*y if r["multiplet"]=="Q" else y if r["multiplet"]=="L" else 0 for r,y in z)),
      "SU3_squared_U1":sp.expand(sum((2*y if r["multiplet"]=="Q" else y if r["multiplet"] in ("uc","dc") else 0) for r,y in z)),
    }

def matter_flavor_gate():
    rows=species()
    k=sp.symbols("k",integer=True)
    symbolic=anomalies(rows,k)
    assert all(sp.simplify(v)==0 for v in symbolic.values())
    cases=[]
    for K in (-2,-1,0,1,2):
        for f in rows:
            y=f["y"]+6*K*f["X"]
            # 2t+3s+y mod6: familiar (3,2) etc.
            assert (2*f["triality"]+3*f["weak_doublet"]+y)%6==0
        for v in anomalies(rows,sp.Integer(K)).values():assert v==0
        # Physical Qem = T3+y/6 given y_H=3 unchanged.
        mu_neutrino=sp.Rational(1,2)+sp.Rational(-3+6*K,6)
        tau_neutrino=sp.Rational(1,2)+sp.Rational(-3-6*K,6)
        cases.append({"k":K,"mu_neutrino_electric_charge":str(mu_neutrino),
                      "tau_neutrino_electric_charge":str(tau_neutrino),
                      "all_Z6_center_residues_zero":True,
                      "all_local_anomalies_zero":True,
                      "diagonal_charged_lepton_Yukawas_allowed":True,
                      "offdiagonal_charged_lepton_Yukawas_all_allowed":K==0})
    assert cases[2]["mu_neutrino_electric_charge"]=="0"
    assert cases[3]["mu_neutrino_electric_charge"]=="1"
    # Even WITHOUT sterile neutrinos, Lmu-Ltau remains anomaly-free.
    sub=[r for r in rows if r["multiplet"]!="nc"]
    assert all(sp.simplify(v)==0 for v in anomalies(sub,k).values())
    return {"status":"PASS","symbolic_integer_parameter":"k",
      "charge_deformation":"y_new = y_SM + 6 k (L_mu-L_tau), y=6Y",
      "symbolic_three_generation_all_perturbative_anomalies":{p:str(v) for p,v in symbolic.items()},
      "global_Z6_and_anomaly_cases":cases,
      "same_anomaly_free_without_nu_c":True,
      "main_new_insight":"Even without right-handed neutrinos, 3-generation anomalies + global Z6 + DIAGONAL Yukawas allow charge dequantization by Lmu-Ltau. Earlier one-generation uniqueness with no nu_c implicitly assumed generation-universal charges/full flavor connectivity.",
      "physical_falsifier":"Observed neutral neutrinos require k=0 in this simple one-Higgs branch. Generic offdiagonal lepton Yukawas also force k=0 unless extra flavor-breaking fields are supplied.",
      "missing_ingredients":"The nonabelian SM multiplets, Higgs and flavor pattern are inputs; local/global anomalies alone do not select observed Y or 3 families."}

def spin_gauge_topology_change_gate(n=12):
    """Conditionally combine a new spatial spin 1-cycle with SU2 central holonomy.

    One charged fundamental sees (-1)^(s+z), whereas a neutral singlet
    sees only (-1)^s. No dynamics chooses either topological sector.
    """
    rows=[]
    for spin_twist in (0,1):
        for center_twist in (0,1):
            charged=(spin_twist+center_twist)%2
            neutral=spin_twist
            kcharged=(2*pi*np.arange(n)+pi*charged)/n
            kneutral=(2*pi*np.arange(n)+pi*neutral)/n
            rows.append({"spin_Z2_twist":spin_twist,
                "SU2_central_minus_identity_twist":center_twist,
                "effective_fundamental_twist":charged,
                "gauge_singlet_twist":neutral,
                "fundamental_massless_naive_zero_modes":int(np.sum(abs(np.sin(kcharged))<1e-12)),
                "neutral_massless_naive_zero_modes":int(np.sum(abs(np.sin(kneutral))<1e-12))})
    assert [x["fundamental_massless_naive_zero_modes"] for x in rows]==[2,0,0,2]
    assert [x["neutral_massless_naive_zero_modes"] for x in rows]==[2,2,0,0]
    return {"status":"PASS",
      "prior_S3_b1":0,"after_S1xS2_b1":1,
      "prior_number_of_spin_structures":1,"after_number_of_spin_structures":2,
      "spin_and_center_twist_combination":"(s,z) -> s+z modulo 2 on SU2 fundamental; a gauge singlet sees s alone.",
      "four_conditional_after_transition_sectors":rows,
      "physical_distinction":"A charged doublet alone cannot distinguish a spin twist from an SU2 center twist, but adding an appropriate gauge singlet can.",
      "cobordism_warning":"Homology does not fix which spin structure extends through the specific spacetime cobordism, nor whether the SU2 center holonomy sector is physically populated.",
      "scope":"Conditional bundle/flat-holonomy effect on S1xS2 in a finite 1D spectral model; not an emergent SM particle family or an actual spin quantum field on the causal set."}

def wilson_circle_operator(n, mass, twist):
    """1D Wilson fermion (r=1): D=(1+m)I-T_theta with T^n=e^{-i twist}.
    This is a Euclidean 1D toy determinant, NOT a full 3+1 Dirac operator.
    """
    T=np.zeros((n,n),complex)
    for j in range(1,n):
        T[j,j-1]=1.
    T[0,n-1]=np.exp(-1j*twist)
    D=(1.+mass)*np.eye(n)-T
    return D


def fermion_backreaction_selects_spin_center_gate():
    """Dynamical conditional selection: topology + Wilson fermion determinants.

    SU2 fundamental has 2 color components, spin twist s and center
    twist z -> total holonomy (-1)^(s+z).  Neutral singlet sees s.
    """
    n=12
    sectors=[]
    for mass in (0.,.005,.02,.1,1.):
        W=[]
        for s in (0,1):
            for z in (0,1):
                charge_twist=np.pi*((s+z)%2)
                singlet_twist=np.pi*s
                dcharged=np.linalg.det(wilson_circle_operator(n,mass,charge_twist))
                dneutral=np.linalg.det(wilson_circle_operator(n,mass,singlet_twist))
                a=1+mass
                charge_exact=a**n-(-1)**(s+z)
                neutral_exact=a**n-(-1)**s
                assert abs(dcharged-charge_exact)<1e-9
                assert abs(dneutral-neutral_exact)<1e-9
                # Two identical color components for an SU2 doublet.
                w_only=abs(dcharged)**2
                w_with=abs(dcharged)**2*abs(dneutral)
                W.append({"spin_twist_s":s,"SU2_center_twist_z":z,
                    "charged_fund_twist_s_plus_z_mod2":(s+z)%2,
                    "fundamental_doublet_determinant_magnitude_squared_color":float(w_only),
                    "neutral_singlet_determinant_magnitude":float(abs(dneutral)),
                    "total_unnormalized_absolute_fermion_weight":float(w_with)})
        sums=sum(x["total_unnormalized_absolute_fermion_weight"] for x in W)
        sums_without=sum(x["fundamental_doublet_determinant_magnitude_squared_color"] for x in W)
        for row in W:
            row["normalized_toy_probability_with_singlet"]=row["total_unnormalized_absolute_fermion_weight"]/sums
            row["normalized_toy_probability_without_singlet"]=row["fundamental_doublet_determinant_magnitude_squared_color"]/sums_without
        sectors.append({"mass":mass,"n":n,"spin_center_sectors":W})
    z=sectors[0]["spin_center_sectors"]
    assert [x["normalized_toy_probability_with_singlet"] for x in z]==[0,0,1,0]
    assert [x["normalized_toy_probability_without_singlet"] for x in z]==[0,.5,.5,0]
    # Check the lattice transport operator is gauge covariant, and determinant
    # gauge invariant under arbitrary site-dependent frame changes.
    D=wilson_circle_operator(n,.037,np.pi)
    phases=np.exp(1j*np.random.default_rng(20261119).uniform(0,2*np.pi,n))
    G=np.diag(phases)
    DG=G@D@G.conj().T
    from scipy.optimize import linear_sum_assignment
    aev=np.linalg.eigvals(D);bev=np.linalg.eigvals(DG)
    inds,matched=linear_sum_assignment(abs(aev[:,None]-bev[None,:]))
    assert np.linalg.norm(aev[inds]-bev[matched])<1e-9
    assert abs(np.linalg.det(D)-np.linalg.det(DG))<1e-9
    # A sharper continuum gate: hold the dimensionless physical mass-times-
    # circumference μ fixed while refining n, so m_lattice=μ/n.
    # The relative P/AP determinant is tanh(μ/2) in the continuum.
    physical_scaling=[]
    for mu in (0.,.1,1.,5.,20.):
        refinement=[]
        for N in (12,24,96,256):
            a=(1+mu/N)**N
            r=(a-1)/(a+1)
            refinement.append({"N":N,"lattice_mass_mu_over_N":mu/N,
               "periodic_to_antiperiodic_determinant_ratio":r,
               "deviation_from_continuum_tanh_mu_over_2":r-np.tanh(mu/2)})
        continuum_r=float(np.tanh(mu/2))
        norm=(1+continuum_r)*(1+continuum_r**2)
        probabilities=[continuum_r**3/norm,continuum_r/norm,
                       1/norm,continuum_r**2/norm]
        assert abs(sum(probabilities)-1)<1e-12
        physical_scaling.append({"dimensionless_mass_times_circle_length_mu":mu,
          "continuum_ratio_detP_to_detAP":continuum_r,
          "continuum_spin_center_sectors_00_01_10_11":probabilities,
          "finite_n_refinements":refinement})
    assert physical_scaling[0]["continuum_spin_center_sectors_00_01_10_11"]==[0,0,1,0]
    assert physical_scaling[-1]["continuum_spin_center_sectors_00_01_10_11"][2]<.251

    return {"status":"PASS",
      "exact_lattice_Dirac_determinant":"det D_n(m,theta)=(1+m)^n-exp(-i theta) for one 1D Wilson r=1 fermion",
      "spin_and_SU2_center_rule":"charged doublet spin boundary = (-1)^(s+z); neutral gauge singlet=(-1)^s",
      "mass_zero_selection":"Only (s,z)=(1,0) has nonzero zero-source determinant when a massless SU2 doublet and neutral singlet are included; with doublet alone both (0,1) and (1,0) survive.",
      "sectors_by_mass":sectors,
      "mass_length_continuum_limit":"det D_P/det D_AP -> tanh(mu/2) for lattice mass m=mu/n as n->infinity",
      "normalized_continuum_sector_probability_formula":"(r^3,r,1,r^2)/[(1+r)(1+r^2)] for (s,z)=00,01,10,11 with r=tanh(mu/2)",
      "continuum_mass_length_gate":physical_scaling,
      "determinant_local_gauge_frame_covariance_error":float(abs(np.linalg.det(D)-np.linalg.det(DG))),
      "scope":"Exact determinant and *toy* nonnegative weights with equal a priori topological sector factors. This does NOT derive dynamical spin selection for the original 3+1 topology-changing spacetime, a physical 4D chiral gauge theory, the Born rule, or a unique microscopic action.",
      "caveat":"A fermion zero mode zeros the vacuum partition determinant at zero Grassmann sources, but correlators with insertions may saturate zero modes. Dynamical mass, gauge integration over continuous SU2 holonomy, cobordism spin extension and spin-statistics may change this selection."}


def normalized_decoherence_relative_to_manifold_gate():
    """Use an explicitly provided competing 'good' manifold amplitude 1.

    This defines an illustrative *two-class* normalized quantum measure,
    with D(bad,good)=0. It is NOT an unbiased gravity path integral.
    """
    theta=2.5;gamma=.999
    out=[]
    for N in (8,16,32,64):
        M=N*N//4
        good=1.
        incoherent=(1-gamma)*2.**M if M<1024 else np.inf
        # avoid enormous 2**1024 conversions
        log_incoh=np.log10(1-gamma)+M*np.log10(2)
        log_coh=2*M*np.log10(2*abs(np.cos(theta/2)))
        # stable log-sum-exp in base 10, pbad=10^u/(1+10^u).
        largest=max(log_coh,log_incoh)
        log_bad=largest+np.log10(10**(log_incoh-largest)+10**(log_coh-largest))
        p_bad=(1./(1.+10.**(-log_bad))) if abs(log_bad)<100 else (1. if log_bad>0 else 0.)
        out.append({"N":N,"history_bits_M":M,"gamma":gamma,
           "log10_bad_incoherent_branch_weight":float(log_incoh),
           "log10_bad_coherent_branch_weight":float(log_coh),
           "normalized_bad_sector_probability_against_unit_good_reference":float(p_bad)})
    assert out[-1]["normalized_bad_sector_probability_against_unit_good_reference"]>1-1e-12
    M=1024
    threshold= -M*np.log10(2)
    return {"status":"PASS","conditional_competing_good_spacetime_weight":1,
       "normalized_two_sector_measure_records":out,
       "log10_incoherent_fraction_threshold_for_bad_weight_below_one_at_N64":float(threshold),
       "physical_honesty":"The good manifoldlike class has been assigned unit weight and no cross terms by hand. Normalization alone does not turn the raw complex sum into a physical causal-set probability.",
       "relationship_to_v6_gate_IV":"D_bad=(1-gamma) I+gamma vv† in a labeled KR subfamily gives D_bad(B,B)=(1-gamma)2^M+gamma|Z|². With a separate orthogonal good class of weight 1, p_bad=D_bad(B,B)/(1+D_bad(B,B)).",
       "no_observed_4D_quantum_gravity_phase_selected":True}

def combined():
    first=causal_spin_topology_gate()
    second=gauge_transfer_gate()
    third=thermal_states_from_transfer_gate(second)
    fourth=interference_entropy_gate()
    fifth=matter_flavor_gate()
    sixth=spin_gauge_topology_change_gate()
    seventh=fermion_backreaction_selects_spin_center_gate()
    eighth=normalized_decoherence_relative_to_manifold_gate()
    assert all(x["status"]=="PASS" for x in (first,second,third,fourth,fifth,sixth,seventh,eighth))
    return {"date":"2026-11-19","status":"PASS five research fronts plus three cross-sector gates, not a fundamental completion",
      "TOE_solved":False,"Lorentzian_4D_GR_derived":False,"SM_spectrum_derived":False,
      "Born_rule_derived":False,
      "sources":[
       "https://arxiv.org/abs/2611.06102",
       "https://github.com/stelios-tsilioukas/topology-change-in-causal-set-theory",
       "https://arxiv.org/abs/gr-qc/0604124",
       "https://doi.org/10.1088/0264-9381/26/17/175008",
       "https://www.scholarpedia.org/article/Lattice_gauge_theories",
       "https://doi.org/10.1088/1361-6382/acc50c",
       "https://doi.org/10.1007/s10714-024-03281-1",
       "https://doi.org/10.1016/S0550-3213(99)00115-7"],
      "gates":{
        "I_intrinsic_order_based_spatial_nerve_H1_and_spin_torsor":first,
        "II_SU2_positive_type_transfer_action_nonuniqueness":second,
        "III_transfer_Hilbert_sectors_and_quantum_state_choice":third,
        "IV_oscillatory_KR_entropy_and_coherence_quantum_measure":fourth,
        "V_3generation_global_quotient_flavor_charge_freedom":fifth,
        "VI_spin_center_compensation_on_topology_change":sixth,
        "VII_fermion_determinant_dynamic_spin_center_selection":seventh,
        "VIII_normalized_two_class_decoherence_control":eighth}}
def main():
    result=combined()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    gates=result["gates"]
    print(json.dumps({"status":"PASS","gates":len(gates),
      "nerve_b1":[x["inferred_from_order_only"]["betti_H0_H1_mod2"][1] for x in gates["I_intrinsic_order_based_spatial_nerve_H1_and_spin_torsor"]["order_based_Dowker_nerve_at_shadow_scales"]],
      "SU2_transfer_fund_Wilson":[x["fundamental_Wilson_mean"] for x in gates["II_SU2_positive_type_transfer_action_nonuniqueness"]["reflection_positive_mixed_action_family"]],
      "KR_N64_absolute_log10":gates["IV_oscillatory_KR_entropy_and_coherence_quantum_measure"]["size_scaling_records"][-1]["log10_absolute_coherent_partition_magnitude"],
      "flavor_mu_charge":[x["mu_neutrino_electric_charge"] for x in gates["V_3generation_global_quotient_flavor_charge_freedom"]["global_Z6_and_anomaly_cases"]],
      "output":str(OUT)}))
if __name__=="__main__":main()
