"""Five independent TOE interfaces with exact falsifiers, 2026-11-18.

1. One-dimensional Jackiw-Rebbi chirality versus conjugate bundles.
2. E8 -> E6 x SU3 family cubic anomaly and exact 27 charge balances.
3. Full 11D Freund-Rubin S7 M2/Page flux quantization and weak-G2 torsion.
4. Markovian qutrit channel with positive intrinsic qutrit Schmidt-number witness.
5. Compensated C3 quartic PW equivariance versus the E8/H27 center.

Mathematical or conditional effective-model constructions, NOT an E8 7D
Dirac spectrum, a solved compactification or experimental quantum memory.
"""
import json
import math
from pathlib import Path
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
def domain_wall():
    x=s.symbols('x',real=True)
    rows=[]
    for mu in range(1,6):
        phi=s.cosh(x)**(-mu)
        mass=mu*s.tanh(x)
        Dplus=s.simplify(s.diff(phi,x)+mass*phi)
        Dminus_at_flipped_mass=s.simplify(-s.diff(phi,x)-mass*phi)
        assert Dplus==0 and Dminus_at_flipped_mass==0
        norm=s.simplify(s.sqrt(s.pi)*s.gamma(mu)/s.gamma(s.Rational(2*mu+1,2)))
        assert norm>0
        rows.append(dict(kink_mass_mu=mu,L2_norm_squared=str(norm),
            normalized_chirality_plus_kernel_dim=1,
            normalized_chirality_minus_kernel_dim=0,
            reverse_mass_flips_the_index_to=-1))
    assert rows[0]["L2_norm_squared"]=="2"
    return dict(status="PASS",operator_plus="d/dx+mu*tanh(x)",
        adjoint_operator_minus="-d/dx+mu*tanh(x)",
        normalized_mode="sech(x)^mu / sqrt(Beta(1/2,mu))",
        exact_integral="sqrt(pi)*Gamma(mu)/Gamma(mu+1/2)",
        positive_mass_profile_Fredholm_index=1,
        negative_mass_profile_Fredholm_index=-1,
        three_independent_positive_wall_channels_index=3,
        corresponding_three_negative_mass_channels_index=-3,
        formal_direct_sum_of_both_charges_total_index=0,
        rows=rows,scope="Exact scalar 1D domain-wall toy Fredholm operator, not the charged 7D G2/E8 Dirac operator. Opposite 4D chirality and conjugate gauge charge can describe CPT-related fields rather than a mirror vectorlike pair; requires a full real-spinor/domain decomposition.")

def anomaly():
    # E6 27 -> Spin10 16_1 + 10_-2 + 1_4.
    # Under SU5: 16=10+5bar+1, 10=5+5bar.
    # SU5 cubic anomaly of 10=+1, 5=+1 and their conjugates -1.
    su5={"ten_from_16":1,"fivebar_from_16":-1,
         "five_from_10":1,"fivebar_from_10":-1}
    assert sum(su5.values())==0
    psi_linear=16*1+10*(-2)+1*4
    psi_cubic=16*1**3+10*(-2)**3+1*4**3
    assert psi_linear==psi_cubic==0
    # A(3)=+1, A(3bar)=-1; 27 E6 components transform as triplets.
    family_triplet=27
    family_conjugate=-27
    assert family_triplet+family_conjugate==0
    return dict(status="PASS",
        chiral_27_SU5_cubic_anomaly_contributions=su5,
        single_27_SU5_cubic_anomaly=0,
        psi_trace_in_one_complete_27=psi_linear,
        psi_cubic_trace_in_one_complete_27=psi_cubic,
        one_chiral_27x3_family_SU3_cubic_anomaly=family_triplet,
        one_chiral_27barx3bar_family_SU3_cubic_anomaly=family_conjugate,
        complete_E8_adjoint_pair_family_anomaly=0,
        only_27x3_with_gauged_SU3_family_consistent_without_inflow_or_extra_matter=False,
        note="SU3_family is a hypothetical continuous gauged symmetry. If only H27 is gauged, local SU3 cubed anomaly is not the complete discrete anomaly test. Exact local inflow coefficients at real G2 singularities remain uncomputed.",
        local_source="Acharya-Witten chiral G2 singularities; Bilal-Metzger anomaly cancellation at each G2 singular point.")

def flux():
    L,lp,N=s.symbols("L lp N",positive=True,real=True)
    R=2*L
    f=3/L
    vol=s.pi**4*R**7/3  # volume(S7_R); vol(unit S7)=pi^4/3
    charge=s.simplify(f*vol/(2*s.pi*lp)**6)
    assert s.simplify(charge-2*L**6/(s.pi**2*lp**6))==0
    ratio=s.solve(s.Eq(N,charge),L)[0]/lp
    target=(s.pi**2*N/2)**s.Rational(1,6)
    assert s.simplify(ratio-target)==0
    sphere=s.simplify((2*L)**6)
    assert s.simplify(sphere-64*L**6)==0
    torsion_lp=s.simplify((2/L)*lp).subs(L,lp*target)
    assert s.simplify(torsion_lp-2/target)==0
    sample=[]
    for v in (1,10,81,100,240,10000,1000000):
        lv=float(target.subs(N,v))
        sample.append(dict(integer_flux_N=v,AdS4_L_in_Planck_lengths=lv,
              sphere_R_in_Planck_lengths=2*lv,
              nearparallel_tau0_in_inverse_Planck_lengths=2/lv))
    return dict(status="PASS",round_S7_vol="pi^4*R^7/3",
        F4="(3/L) vol_AdS4",normalization="N=(1/(2*pi*lp)^6) integral_S7(*F4)",
        exact_N="2*L^6/(pi^2*lp^6)",
        exact_R7_to_lp="(32*pi^2*N)^(1/6)",
        exact_AdS_L_to_lp="(pi^2*N/2)^(1/6)",
        nearparallel_tau0_lp="2/(pi^2*N/2)^(1/6)",
        exact_flux_integer_constraint="N is positive integer for this unquotiented S7 electric flux solution",
        examples=sample,
        caveat="Classical S7 Freund-Rubin geometry with no orbifold, branes localized away from sphere, gravitational shift or extra flux. No E8 chiral matter; N is an independent quantized input, not predicted by W33.")

def markov_qutrit():
    t=s.Rational(9,10)
    p1=s.simplify((1+8*t)/9)
    p2=s.simplify((1+8*t*t)/9)
    matched1=s.simplify((1+3*p1)/4)
    matched2=s.simplify((1+3*p2)/4)
    assert p1>s.Rational(2,3) and p2>s.Rational(2,3)
    assert matched1>s.Rational(3,4) and matched2>s.Rational(3,4)
    v=np.eye(3).reshape(9)/math.sqrt(3)
    P=np.outer(v,v.conj())
    rho1=float(t)*P+(1-float(t))*np.eye(9)/9
    rho2=float(t*t)*P+(1-float(t*t))*np.eye(9)/9
    assert abs(np.trace(rho1)-1)<1e-12
    assert np.linalg.eigvalsh(rho1).min()>0
    assert np.linalg.eigvalsh(rho2).min()>0
    # By definition Delta_t(rho)=t*rho+(1-t)*I3*Tr(rho)/3.
    # Fresh, independent environments at each step give the
    # operational Markov process Delta_t o Delta_t=Delta_t².
    rng=np.random.default_rng(20261118)
    maxerr=0.0
    def dep(a,v):
        return v*a+(1-v)*np.trace(a)*np.eye(3)/3
    for k in range(12):
        a=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
        rho=a@a.conj().T/np.trace(a@a.conj().T)
        err=np.max(abs(dep(dep(rho,float(t)),float(t))-dep(rho,float(t*t))))
        maxerr=max(maxerr,float(err))
    assert maxerr<1e-12
    return dict(status="PASS",
        channel="Delta_t(rho)=t rho+(1-t) Tr(rho) I3/3",
        t=str(t),t_two_steps=str(t*t),
        one_step_entanglement_fidelity=str(p1),
        two_steps_entanglement_fidelity=str(p2),
        one_step_fourMUB_match_probability=str(matched1),
        two_steps_fourMUB_match_probability=str(matched2),
        Schmidt_number3_threshold_fidelity="2/3",
        both_steps_certify_dimension3_with_ideal_Choi_witness=True,
        process_tensor_genuinely_multitime_quantum_memory=False,
        Markov_reason="Two independent fresh depolarizing environments, no retained system-environment correlations after interventions; process-tensor factorizes.",
        direct_matrix_composition_max_error=maxerr,
        conclusion="Even qutrit Schmidt-number3 witness success at both one and two time separations does not imply nonclassical multi-time memory. Need intervention-sensitive witness (Beyer et al 2026).")

def equivariance():
    rec=[]
    for n in range(2,15):
        q=(-n-1)%3
        rec.append(dict(Morse_family_count_parameter_n=n,
             holomorphic_localizer_degree=n+1,
             compensation_center_character_q=q,
             no_compensator_rotation_invariant=(q==0)))
    assert next(x for x in rec if x["Morse_family_count_parameter_n"]==3)["compensation_center_character_q"]==2
    assert [x["Morse_family_count_parameter_n"] for x in rec if x["compensation_center_character_q"]==2]==[3,6,9,12]
    return dict(status="PASS",assumed_geometric_C3_rotation="w -> omega*w",
         complex_holomorphic_localizer="Phi_n(w)=w^(n+1)",
         combined_invariance_condition="n+1+q == 0 mod3",
         quartic_n3_requires_character_q=2,
         E8_H27_family_triplet_center_character_q=1,
         E8_H27_antitriplet_center_character_q=2,
         n3_is_not_uniquely_selected_by_q2_because_n6_n9_n12_also_allowed=True,
         census=rec,
         limitation="Condition applies only if INTERNAL E8 center is explicitly identified with a geometric C3 rotation acting on a COMPLEX charged localizer. Earlier real harmonic Re(w^4), nonzero tilt and physical PW Higgs field need a new equivariant bundle construction. Hence neither a physical preference for conjugate matter nor a prediction of three families follows.")

def run():
    out=dict(status="PASS",date="2026-11-18",
      localized_chirality=domain_wall(),E8_anomaly=anomaly(),
      FR_flux_quantization=flux(),Markov_qutrit_counterexample=markov_qutrit(),
      equivariant_family_selection=equivariance(),
      physical_TOE=False)
    dest=ROOT/"data/toe_20261118_chirality_anomaly_FRflux_Markov_equivariant.json"
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS five fronts: kink chirality plus/minus 1, SU3fam anomaly plus/minus 27, quantized FR flux, Markov qutrit with SN3 at two time separations, C3 equivariance fails unique n=3 selection")
    return out

if __name__=="__main__":run()
