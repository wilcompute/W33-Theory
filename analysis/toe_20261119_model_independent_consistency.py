#!/usr/bin/env python3
"""Model-independent TOE constraint sieve: six testable physics fronts.

This script does NOT solve the theory of everything. It establishes ordinary
field-theory and empirical consistency constraints that any proposed
unification must reproduce. Values are labelled by source and scheme.
"""
from __future__ import annotations
import itertools
import json
import math
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.constants import G, c, hbar, k, pi
from scipy.constants import physical_constants

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/"data"/"toe_20261119_model_independent_TOE_sieve.json"


def anomaly_ambiguity():
    t=sp.symbols("t", real=True)
    R=sp.Rational
    # All fields are LEFT-handed Weyl. Conjugate right-handed states
    # have opposite Abelian hypercharge and B-L charges.
    fields=[
      ("Q",6,R(1,6),R(1,3),2,3),
      ("u^c",3,-R(2,3),-R(1,3),1,3),
      ("d^c",3,R(1,3),-R(1,3),1,3),
      ("L",2,-R(1,2),-R(1,1),2,1),
      ("e^c",1,R(1,1),R(1,1),1,1),
      ("nu^c",1,R(0),R(1,1),1,1)
    ]
    charge={n:sp.expand(Y+t*BL) for n,_,Y,BL,_,_ in fields}
    nonab_su3=sp.expand(2*charge["Q"]+charge["u^c"]+charge["d^c"])
    nonab_su2=sp.expand(3*charge["Q"]+charge["L"])
    gravitational=sp.expand(sum(mult*charge[name] for name,mult,*_ in fields))
    cubic=sp.expand(sum(mult*charge[name]**3 for name,mult,*_ in fields))
    assert all(sp.simplify(x)==0 for x in (nonab_su3,nonab_su2,gravitational,cubic))
    # Check gauge invariance of Yukawas. Use left-handed antifundamental
    # conjugates with Higgs hypercharge H=1/2 and B-L(H)=0.
    H=R(1,2)
    yukawa=[
       sp.expand(charge["Q"]+H+charge["u^c"]),
       sp.expand(charge["Q"]-H+charge["d^c"]),
       sp.expand(charge["L"]-H+charge["e^c"]),
       sp.expand(charge["L"]+H+charge["nu^c"])
    ]
    assert all(v==0 for v in yukawa)
    # An SU2 global/Witten anomaly is absent: 3 quark doublets+1 lepton.
    assert (3+1)%2==0
    # Without a right-handed neutrino B-L has gravitational and cubic
    # anomalies; the extra species is essential for this ambiguity.
    without_nu_grav=sp.simplify(gravitational-charge["nu^c"])
    without_nu_cubic=sp.expand(cubic-charge["nu^c"]**3)
    assert without_nu_grav==-t
    assert sp.simplify(without_nu_cubic)!=0
    # Physical bridge: an uncharged bare right-handed-neutrino Majorana
    # mass or Weinberg (LH)^2 operator demands t=0, unless a new charged
    # scalar/spurion breaks the B-L admixture. This is known charge-
    # quantization physics, not a new theorem of this project.
    charge_RH_majorana=sp.expand(2*charge["nu^c"])
    charge_Weinberg=sp.expand(2*(charge["L"]+H))
    assert charge_RH_majorana==2*t and charge_Weinberg==-2*t
    assert sp.solve(charge_RH_majorana,t)==[0]
    assert sp.solve(charge_Weinberg,t)==[0]
    return {
       "status":"PASS",
       "claim":"Anomaly and Yukawa consistency allow continuous Y+t(B-L) with nu_R",
       "gauge_group":"SU(3)c x SU(2)L x U(1)Y",
       "left_Weyl_generation":[{"field":n,"multiplicity":m,"Y":str(y),"B_minus_L":str(bl)}
                                for n,m,y,bl,_,_ in fields],
       "anomaly_polynomials":{"SU3_squared_U1":str(nonab_su3),
         "SU2_squared_U1":str(nonab_su2),"gravity_squared_U1":str(gravitational),
         "U1_cubed":str(cubic)},
       "Yukawa_charge_residuals":[str(v) for v in yukawa],
       "SU2_Witten_number_doublets_per_generation":4,
       "without_nuR_gravity_B_minus_L_mixing_anomaly":str(without_nu_grav),
       "without_nuR_U1_cubed_mixed_anomaly":str(without_nu_cubic),
       "bare_nuR_Majorana_mass_U1_charge":str(charge_RH_majorana),
       "Weinberg_LH_squared_U1_charge":str(charge_Weinberg),
       "Majorana_mass_or_unspurioned_Weinberg_operator_forces_mixing_t":0,
       "Majorana_charge_quantization_prior_art":"Phys Rev Lett 63, 938 (1989)",
       "limitation":"charges are known from observation; anomaly equations alone do not derive them; new B-L breaking scalars can evade the simple t=0 criterion"
    }


def gauge_unification():
    # Illustrative 2025 PDG MS-bar inputs, canonical SU5 hypercharge.
    alpha_em_inv=127.930
    s2=0.23122
    alpha_s=0.1180
    mz=91.1876
    inv=np.array([3/5*alpha_em_inv*(1-s2),alpha_em_inv*s2,1/alpha_s],float)
    bSM=np.array([41/10,-19/6,-7.])
    bMSSM=np.array([33/5,1.,-3.])
    L12=2*pi*(inv[0]-inv[1])/(bSM[0]-bSM[1])
    mu12=mz*np.exp(L12)
    running=inv-bSM*L12/(2*pi)
    residual=float(running[0]-running[2])
    assert residual>5 and abs(running[0]-running[1])<1e-12
    # Hypothetical sharp SM -> MSSM threshold at Ms: solve exactly
    # the two linear pairwise matching conditions for log intervals.
    A=np.array([[(bSM[0]-bSM[j])/(2*pi),(bMSSM[0]-bMSSM[j])/(2*pi)]
                for j in (1,2)])
    B=np.array([inv[0]-inv[j] for j in (1,2)])
    logMS,logUM=np.linalg.solve(A,B)
    inferredMS=float(mz*np.exp(logMS))
    inferredMU=float(mz*np.exp(logMS+logUM))
    assert inferredMS<mz # sharp-threshold fit is outside its assumed regime
    # If the MSSM full threshold is forcibly fixed at 1 TeV, match 1 and2
    # and calculate predicted alpha3(M_Z). Not precision phenomenology.
    fixedMS=1000.
    t=np.log(fixedMS/mz)
    u=(2*pi*(inv[0]-inv[1])-(bSM[0]-bSM[1])*t)/(bMSSM[0]-bMSSM[1])
    inv3pred=inv[0]-((bSM[0]-bSM[2])*t+(bMSSM[0]-bMSSM[2])*u)/(2*pi)
    predicted_alpha_s=float(1/inv3pred)
    assert predicted_alpha_s<alpha_s
    return {
      "status":"PASS",
      "scheme":"one-loop SM MS-bar, SU5-normalized U1, no thresholds or two-loop corrections",
      "input":{"alpha_em_inv_MZ":alpha_em_inv,"sin2_thetaW_MZ":s2,
               "alpha_s_MZ":alpha_s,"MZ_GeV":mz},
      "beta_coefficients_SM":list(map(float,bSM)),
      "initial_inverse_couplings":list(map(float,inv)),
      "U1_SU2_crossing_GeV":float(mu12),
      "inverse_couplings_at_U1_SU2_crossing":list(map(float,running)),
      "U1_SU3_inverse_mismatch_at_crossing":residual,
      "simple_sharp_SM_MSSM_extrapolation":{
        "best_equal_meeting_threshold_GeV":inferredMS,
        "unification_GeV":inferredMU,
        "invalid_with_threshold_below_MZ":True
      },
      "MSSM_sharp_threshold_1TeV":{
         "predicted_alpha_s_MZ":predicted_alpha_s,
         "unification_GeV":float(fixedMS*np.exp(u))
      },
      "warning":"No claim of SM or MSSM exclusion: thresholds, particles and two-loop effects matter."
    }


def neutrino_spectrum():
    # Source: independent Bari global fit release 2026.a (preliminary)
    # https://global-nu.org/results.html
    dm21_NO=7.465e-5  # eV²
    dm31_NO=2.5093e-3
    dm21_IO=7.439e-5
    absdm32_IO=2.5182e-3
    m_NO=[0.,np.sqrt(dm21_NO),np.sqrt(dm31_NO)]
    # IO convention |dm32|=m2²-m3² ; m3=0 and m1²=m2²-dm21
    m_IO=[np.sqrt(absdm32_IO-dm21_IO),np.sqrt(absdm32_IO),0.]
    minNO=float(sum(m_NO));minIO=float(sum(m_IO))
    assert .058<minNO<.060 and .098<minIO<.102
    v_GeV=246.22
    reference_m_eV=.050
    # mnu=kappa*v²/(2Lambda), hence Lambda/kappa=v²/(2mnu)
    Lam_over_kappa=v_GeV**2/(2*reference_m_eV*1e-9)
    # See exact RGE crossings to make comparison, NOT identity.
    rge=gauge_unification()
    sm_cross=rge["U1_SU2_crossing_GeV"]
    mssm_ideal=rge["simple_sharp_SM_MSSM_extrapolation"]["unification_GeV"]
    kappa_at_sm=sm_cross/Lam_over_kappa
    kappa_at_mssm=mssm_ideal/Lam_over_kappa
    assert kappa_at_sm<1 and kappa_at_mssm>1
    return {
      "status":"PASS",
      "input_source":"Bari global neutrino fit 2026.a, preliminary, normal/inverted ordering central splittings",
      "input_delta_m_squared_eV2":{"NO_21":dm21_NO,"NO_31":dm31_NO,
                                   "IO_21":dm21_IO,"IO_abs32":absdm32_IO},
      "minimum_masses_NO_eV":list(map(float,m_NO)),
      "minimum_masses_IO_eV":list(map(float,m_IO)),
      "minimum_sum_NO_eV":minNO,"minimum_sum_IO_eV":minIO,
      "illustrative_Weinberg_operator":"mnu=kappa*v²/(2Lambda)",
      "v_EW_GeV":v_GeV,"reference_neutrino_mass_eV":reference_m_eV,
      "Lambda_over_kappa_GeV":Lam_over_kappa,
      "required_kappa_if_Lambda_equals_SM_alpha1_alpha2_crossing":kappa_at_sm,
      "required_kappa_if_Lambda_equals_simple_MSSM_one_loop_crossing":kappa_at_mssm,
      "limitations":["neutrino absolute masses and Majorana vs Dirac remain unknown",
                     "operator coefficient κ not fixed and seesaw mass need not equal GUT scale",
                     "no claim that a cosmological upper bound below inverted minimum is model independent",
                     "gauge coupling scales have one-loop threshold ambiguities"]
    }


def dark_energy():
    # Source: DES Y6 joint with DESI DR2 BAO, low-redshift joint best fit.
    w0=-.84;wa=-.53
    def w(z): return w0+wa*z/(1+z)
    zstar=-(1+w0)/(wa+1+w0)
    assert 0<zstar<1 and abs(w(zstar)+1)<1e-14
    def rho_ratio(z):
        return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z))
    rows=[{"redshift":z,"w":float(w(z)),
           "dark_energy_density_relative_today":float(rho_ratio(z))}
           for z in (0,0.1,0.4,0.5,1,2)]
    assert w(0)>-1 and w(1)<-1
    # For a minimally coupled scalar with canonical kinetic sign:
    # rho=kinetic+V, pressure=kinetic-V, rho+p=2K >=0,
    # hence w>=-1 if rho>0. Best-fit crossing requires K<0
    # at z>zstar if interpreted as exact canonical quintessence.
    return {
      "status":"PASS conditional on CPL best-fit being exact",
      "input_source":"DES Y6 + DESI DR2 BAO joint fit, published May 2026",
      "w0":w0,"wa":wa,
      "equation_of_state":"w(z)=w0+wa*z/(1+z)",
      "crosses_phantom_divide_at_z":float(zstar),
      "samples":rows,
      "canonical_minimally_coupled_positive_kinetic_single_scalar_can_exactly_realize_global_best_fit":False,
      "caveats":["data currently give a model-dependent ~2.3 sigma preference, not discovery",
                 "best-fit statistical uncertainty and parameter correlations not propagated",
                 "CPL extrapolation outside fitted redshift range may be unphysical",
                 "effective crossing can arise from multi-fields, interactions, or modified gravity",
                 "this does not prove ghost degrees of freedom are required by observations"]
    }


def quantum_gravity_filters():
    p2,Msq=sp.symbols("p2 Msq",positive=True)
    # Toy fourth-order wave propagator has opposite-residue heavy pole.
    rational=1/(p2*(1+p2/Msq))
    partial=sp.apart(rational,p2)
    assert sp.simplify(partial-(1/p2-1/(p2+Msq)))==0
    residue0=sp.limit(p2*rational,p2,0)
    residueHeavy=sp.limit((p2+Msq)*rational,p2,-Msq)
    assert residue0==1 and residueHeavy==-1
    # Low energy expansion is good as EFT; treating the heavy pole
    # as fundamental physical state violates ordinary positive norm.
    planck_length=float(np.sqrt(hbar*G/c**3))
    sun=1.98847e30
    rs=2*G*sun/c**2
    SBH_over_k=pi*rs**2/planck_length**2
    TH=hbar*c**3/(8*pi*G*sun*k)
    assert 1e76<SBH_over_k<2e77 and 5e-8<TH<7e-8
    # A local volume lattice with one qubit per Planck cube near radius
    # R is not a simultaneously accessible gravitational Hilbert space:
    # log dim = (4pi/3)*(R/lp)^3 * ln2 vs S_BH/k= pi*(R/lp)^2.
    # ratio = (4 ln2/3)*(R/lp).
    ratio_at_R1=(4*np.log(2)/3)/planck_length
    return {
      "status":"PASS",
      "fourth_order_scalar_toy":{
        "propagator":"1/[p²(1+p²/M²)]",
        "partial_fractions":str(partial),
        "massless_pole_residue":str(residue0),
        "massive_pole_residue":str(residueHeavy),
        "physical_note":"opposite-sign residue obstructs positive norm if both poles fundamental; EFT above cutoff not assumed"
      },
      "black_hole_one_solar_mass":{
        "Schwarzschild_radius_m":float(rs),
        "Hawking_temperature_K":float(TH),
        "Bekenstein_Hawking_entropy_over_k":float(SBH_over_k),
        "Planck_length_m":planck_length
      },
      "Planck_cell_volume_entropy_over_area_entropy_ratio_at_R_1m":float(ratio_at_R1),
      "cautions":["toy propagator is not a full quantum-gravity no-go theorem",
                  "covariant entropy bounds depend on gravitational state access and assumptions",
                  "cannot infer complete microphysics from black-hole thermodynamics"]
    }


def bell_quantum():
    X=np.array([[0,1],[1,0]],complex)
    Z=np.diag([1.,-1.])
    I=np.eye(2)
    B=(X+Z)/np.sqrt(2)
    Bp=(Z-X)/np.sqrt(2)
    A=Z;Ap=X
    bell=(np.kron([1,0],[1,0])+np.kron([0,1],[0,1]))/np.sqrt(2)
    CHSH=(np.kron(A,B)+np.kron(A,Bp)+np.kron(Ap,B)-np.kron(Ap,Bp))
    value=np.vdot(bell,CHSH@bell).real
    assert abs(value-2*np.sqrt(2))<1e-12
    opnorm=np.linalg.norm(CHSH,2)
    assert abs(opnorm-2*np.sqrt(2))<1e-12
    # Commutativity across the two sites and ±1 eigenvalues imply
    # C²=4I-[A,A']⊗[B,B'], whose operator norm ≤8.
    comm=lambda a,b:a@b-b@a
    assert np.allclose(CHSH@CHSH,4*np.eye(4)-np.kron(comm(A,Ap),comm(B,Bp)))
    return {"status":"PASS",
       "Bell_state":"(|00>+|11>)/sqrt2",
       "local_hidden_variable_CHSH_abs_max":2,
       "quantum_Tsirelson_abs_max":float(2*np.sqrt(2)),
       "observed_toy_state_CHSH":float(value),
       "no_signaling_PR_box_algebraic_max":4,
       "limitation":"does not explain why the Born rule and tensor-product causal structure emerge"
    }


def certify():
    records={"anomalies_and_charge_ambiguity":anomaly_ambiguity(),
             "gauge_RGE_unification":gauge_unification(),
             "neutrino_mass_and_Weinberg":neutrino_spectrum(),
             "cosmological_dark_energy":dark_energy(),
             "quantum_gravity_ghost_and_horizon":quantum_gravity_filters(),
             "quantum_Bell_Tsirelson":bell_quantum()}
    assert all(r["status"].startswith("PASS") for r in records.values())
    return {
      "title":"Theory-of-everything model-independent constraint sieve",
      "date":"2026-11-19",
      "scope":"Known physics and transparent conditional model checks; not a TOE solution",
      "all_certificates":"PASS",
      "source_uris":[
        "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-guts.pdf",
        "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-standard-model.pdf",
        "https://global-nu.org/results.html",
        "https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/"
      ],
      "frontiers":records
    }


def main():
    result=certify()
    TARGET.parent.mkdir(parents=True,exist_ok=True)
    TARGET.write_text(json.dumps(result,indent=2),encoding="utf-8")
    f=result["frontiers"]
    print(json.dumps({
       "status":result["all_certificates"],
       "anomaly_U1_family":"Y+t(B-L)",
       "SM_unification_mismatch":f["gauge_RGE_unification"]["U1_SU3_inverse_mismatch_at_crossing"],
       "neutrino_sum_NO_eV":f["neutrino_mass_and_Weinberg"]["minimum_sum_NO_eV"],
       "neutrino_sum_IO_eV":f["neutrino_mass_and_Weinberg"]["minimum_sum_IO_eV"],
       "CPL_phantom_crossing_z":f["cosmological_dark_energy"]["crosses_phantom_divide_at_z"],
       "BH_entropy_S_sun_over_k":f["quantum_gravity_ghost_and_horizon"]["black_hole_one_solar_mass"]["Bekenstein_Hawking_entropy_over_k"],
       "Tsirelson":f["quantum_Bell_Tsirelson"]["observed_toy_state_CHSH"],
       "path":str(TARGET)
    }))


if __name__=="__main__":
    main()
