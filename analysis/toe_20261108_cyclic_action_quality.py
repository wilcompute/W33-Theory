"""Explicit cyclic label orbit and declared full-field EFT quality controls.

Uses the published cyclic-fermion mechanism and standard axion-quality formula.
No global/gauge completion or quantum-gravity prediction is established.
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
MP=2.435e27
H0=1.44667e-33


def orbit24():
    parent=json.loads((ROOT/'data/toe_20261108_native_cyclic_orders.json').read_text())
    M=np.array(parent['enlarged_three_qutrit_control']['matrix'],dtype=int)
    for seed in itertools.product(range(3),repeat=6):
        v=np.array(seed);orbit=[];w=v.copy()
        for _ in range(24):
            orbit.append(w.tolist());w=M@w%3
        if len({tuple(x)for x in orbit})==24 and np.array_equal(w,v):
            def project(x):
                a=next(t for t in x if t)
                return tuple((t*(1 if a==1 else 2))%3 for t in x)
            if len({project(x)for x in orbit})==24:
                return dict(seed=list(seed),orbit=orbit,linear_order=24,projective_orbit_length=24,
                            map='Assign psi_k to the kth element of this explicit orbit of three-qutrit Pauli labels. M advances k by1. This constructs a regular cyclic label permutation, not a derivation of particle fields from Pauli operators.')
    raise AssertionError('No regular24orbit')


def quality_log10(N,r,coefficient=1.):
    """Max |V''|/H0^2 for c Phi^N/MP^(N-4)+h.c., Phi=f/sqrt2 exp(i phi/f)."""
    return (math.log10(2*N*N*abs(coefficient))+2*math.log10(MP/H0)
            +(N-2)*math.log10(r)-.5*N*math.log10(2))


def eps_for_local_beta(beta,r):
    # beta=MP/f*eps/(1+eps^2) at theta=pi/2; use small branch.
    b=beta*r
    return 2*b/(1+math.sqrt(1-4*b*b))


def quality_and_excursion():
    beta=.053;excursion=.3;required_logmass=beta*excursion
    eps_min=math.tanh(required_logmass/2)
    r_min=eps_min/(beta*(1+eps_min*eps_min))
    # This is a NECESSARY total amplitude, not constant local beta along a path.
    quality24_rmax=10**(-(math.log10(2*24*24)+2*math.log10(MP/H0)-12*math.log10(2))/22)
    rows=[]
    for r in [1.,.3,r_min,.1,.01,quality24_rmax,1e-6]:
        eps=eps_for_local_beta(beta,r)
        first=next(n for n in range(5,2000)if quality_log10(n,r)<0)
        rows.append(dict(f_over_MP=r,eps=eps,available_max_log_mass_ratio=math.log((1+eps)/(1-eps)),
                         log10_quality24_curvature_over_H0_squared=quality_log10(24,r),
                         first_operator_degree_with_unit_coefficient_envelope_below_H0_squared=first))
    return dict(local_beta_at_pi_over2=beta,supplied_target_excursion_over_MP=excursion,
                target_integrated_log_mass_change=required_logmass,
                necessary_eps_for_full_spectrum_amplitude=eps_min,
                necessary_f_over_MP_on_small_eps_branch=r_min,
                maximum_f_over_MP_for_unit_coefficient_degree24_quality=quality24_rmax,
                maximum_available_log_mass_at_quality24=math.log((1+eps_for_local_beta(beta,quality24_rmax))/(1-eps_for_local_beta(beta,quality24_rmax))),
                rows=rows,
                scope='Conditional EFT screen: coefficient1 and cutoffMP, canonical f/sqrt2 convention, scalar-only leading operator. Quantum gravity is modeled, not calculated. No universal lower bound on coefficients; UV gauge locality or other mechanisms may suppress them. The amplitude condition is necessary, not sufficient for a cosmological trajectory.')


def scalar_monomials(N=24,max_degree=28):
    # Neutral dark Higgs S and SM H can multiply these invariants without
    # removing the lowest Phi harmonic. Fermion/derivative operators separate.
    phase_breaking=[]
    for a in range(max_degree+1):
        for b in range(max_degree+1-a):
            if a!=b and (a-b)%N==0:
                phase_breaking.append(dict(Phi_power=a,Phibar_power=b,degree=a+b,charge_difference=a-b))
    return dict(max_degree=max_degree,phase_breaking=phase_breaking,
                first_degree=min(x['degree']for x in phase_breaking),
                scope='Complete monomial enumeration only for Phi and Phi*. Does not enumerate all spinor, derivative, multi-field or gravitational operators.')


def finite_flavor_extension():
    """Declared affine three-qutrit-label subgroup, induced fermion module."""
    q=np.array(orbit24()['orbit'],dtype=int)
    parent=json.loads((ROOT/'data/toe_20261108_native_cyclic_orders.json').read_text())
    M=np.array(parent['enlarged_three_qutrit_control']['matrix'],dtype=int)
    omega=np.exp(2j*np.pi/3);C=np.roll(np.eye(24),-1,axis=1)
    # Use an explicitly chosen component shift: (C psi)_k=psi_(k+1).
    C=np.array([[int(j==(i+1)%24)for j in range(24)]for i in range(24)])
    errors=[]
    for x in np.eye(6,dtype=int):
        D=np.diag(omega**((q@x)%3));Dnext=np.diag(omega**((q@(M.T@x))%3))
        errors.append(float(np.max(abs(C@D@C.T-Dnext))))
    assert max(errors)<1e-12
    signatures={tuple((q@np.array(x))%3)for x in itertools.product(range(3),repeat=6)}
    assert len(signatures)==3**6
    offdiag=[(i,j)for i in range(24)for j in range(24)if i!=j and np.all((q[j]-q[i])%3==0)]
    majorana=[(i,j)for i in range(24)for j in range(i,24)if np.all((q[i]+q[j])%3==0)]
    assert not offdiag and not majorana
    sums={}
    for i in range(24):
        for j in range(i,24):sums.setdefault(tuple((q[i]+q[j])%3),[]).append((i,j))
    witness=None
    for pairs in sums.values():
        for a,b in itertools.combinations(pairs,2):
            if len(set(a+b))==4:witness=dict(incoming=list(a),outgoing=list(b));break
        if witness:break
    return dict(group='(F3^6 additive) semidirect C24, generator action on additive x is M^T',
                order=3**6*24,representation_dimension=24,
                distinct_abelian_character_signatures=len(signatures),
                representation='D(x)_kk=exp(2pi*i*q_k dot x/3), (C psi)_k=psi_(k+1). Phi neutral under additive subgroup, transforms exp(2pi*i/24) underC. Both Dirac chiralities in the same representation.',
                generator_covariance_max_residual=max(errors),
                offdiagonal_Dirac_bilinears_allowed_by_additive_subgroup=offdiag,
                Majorana_bilinears_allowed_by_additive_subgroup=majorana,
                bilinear_conclusion='Only diagonal Dirac masses remain under additive subgroup; C forces the constant mass to be universal and the linear Phi Yukawa coefficients proportional to exp(2pi*i*k/24). Neutral Phi,S,H insertions cannot neutralize a forbidden additive charge.',
                four_fermion_charge_sum_classes=len(sums),four_fermion_rearrangement_witness=witness,
                higher_operator_boundary='A nontrivial pair-sum collision permits charge-level current-current flavor rearrangements; its cyclic orbit sum is invariant. Such extra dimension6 coefficients are not fixed by the symmetry or included in the chosen vector-only transport kernel.',
                gauge_interpretation='Can be posited as an extra finite gauge symmetry: vectorlike Dirac representation admits a gauge-invariant bare mass/regulator, so the displayed fermions do not carry a chiral gauge anomaly. No microscopic embedding, topological sector or quantum-gravity realization is computed.',
                cost='An explicit enlargement using the affine subgroup of three-qutrit symplectic labels, not the original two-qutrit W33 group or27dimensional quantum-state module. The24fermions and finite gauge symmetry are new physical inputs.',
                remaining_quality='Phi^24 is invariant under this entire extension. It repairs the bilinear selection problem but not the scalar quality obstruction.')


def field_inventory():
    return dict(spacetime='Supplied four-dimensional canonical EFT in natural units, not derived from the finite graph.',
      gauge='U1_D with coupling gD; all24 Dirac psi_k have vector charge+1; Phi is neutral; complex dark Higgs S has charge+1.',
      cyclic='omega=exp(2pi*i/24); Phi -> omega Phi; psi_k -> psi_(k+1); S,A_D unchanged.',
      action='L=|dPhi|^2+|D S|^2-lambdaPhi(|Phi|^2-f^2/2)^2-lambdaS(|S|^2-vD^2/2)^2-F_D^2/4+sum_k psiBar_k iDslash psi_k -sum_k[(M+y omega^k Phi)psiBar_kL psi_kR+h.c.] -V_break.',
      physical_masses='Phi=f/sqrt2 exp(i phi/f); m_k=M sqrt(1+eps^2+2eps cos(phi/f+2pi*k/24)); eps=y*f/(sqrt2*M). mA=gD*vD; choose mA and dark-radial mass much larger than all2*m_k and thermal energies.',
      extra_flavor_assumption='Independent vector U1_k fermion numbers forbid cyclic-invariant off-diagonal circulant masses/Yukawas. They are additional assumed global selection rules, not consequences of Z24. Pair conversions conserve every net U1_k charge and can redistribute symmetric pairs.',
      shift_control='At M=0 the displayed classical action has Phi->exp(i alpha)Phi, psi_kR->exp(-i alpha)psi_kR. The vector interaction respects this classical symmetry. Its chiral current has mixed U1_D^2 anomaly coefficient24 in LH Weyl convention; it is not asserted to be an exact quantum symmetry. Perturbative Abelian FtildeF does not by itself establish a potential, but magnetic/UV sectors require a fresh audit. M and V_break explicitly break it.',
      anomalies=dict(left_weyl_charges_per_Dirac=[1,-1],sum_q=24*(1-1),sum_q_cubed=24*(1-1),classical_shift_U1D_squared_coefficient_LH_convention=24,scope='Continuous U1_D cubic and mixed gravitational gauge anomalies cancel pairwise; this is distinct from the anomalous global chiral shift current. No proof that global cyclic/flavor symmetries can be gauged or survive quantum gravity.'),
      contact_operator='-G/2*(sum_k psiBar_k gamma_mu psi_k)^2, G=gD^2/mA^2; sign is convention dependent and rates useG^2.',
      retained_processes='psi_i antiPsi_i <-> psi_j antiPsi_j through virtual A_D, and elastic scattering. CP-symmetric number/energy moments assume n_i=nbar_i and common kinetic temperature.',
      excluded_channels='On-shell A_D,A_D and dark-radial final pairs are kinematically closed in the nonrelativistic/contact benchmark. Radiation through tiny y, off-shell multi-particle channels and portals are not computed.',
      allowed_but_unfixed=['Phi^24/MP^20+h.c.','|Phi|^2|S|^2','|Phi|^2|H_SM|^2','F_D B kinetic mixing','(S*)^2 psi_L psi_L /Lambda plus flavor/cyclic orbit sums if the extra global fermion numbers are not imposed'],
      not_a_completion='Additional scalar couplings, initial abundance, vD,f,M,y and Wilson coefficients are inputs; no complete renormalization/kinetic-equilibrium/operator/SM/gravity completion.')


def build():
    result=dict(status='EXPLICIT_REGULAR_CYCLIC_LABEL_MAP_AND_DECLARED_VECTOR_EFT_WITH_QUALITY_OBSTRUCTION',
                orbit=orbit24(),inventory=field_inventory(),finite_flavor_extension=finite_flavor_extension(),scalar_monomials=scalar_monomials(),quality=quality_and_excursion(),
                ownership='Cyclic fermion mass/cancellation mechanism2610.30253; standard scalar quality formula already in toe_20261105_pq_quality_gauge_obstruction.py and primary2606.14098. New use is this declared24partner conversion inventory and its supplied ultralight/finite-excursion compatibility screen, not discovery of the mechanisms.')
    (ROOT/'data/toe_20261108_cyclic_action_quality.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('QUALITY',result['quality'],flush=True)
    return result


if __name__=='__main__':build()
