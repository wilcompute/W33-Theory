#!/usr/bin/env python3
"""Native null-frame five-front constructive witness (2026-11-08).

Scope: exact finite mathematics, conditional native cubic constraint, ideal
single-photon optical controls, and source-only cosmology validity guards.
No claim of physical TOE, unbroken finite Lorentz symmetry, measured photons,
strong CP protection, or new survey likelihoods.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parents[1]
DIRECTIONS = ((1, 0, 0), (1, 1, 1), (0, 0, 1))

def read_json(path, root=ROOT):
    return json.loads((root / path).read_text(encoding="utf-8"))

def detq(v, p):
    return (v[0]*v[2] - v[1]*v[1]) % p

def normalize_projective(v,p):
    for c in v:
        if c % p:
            inv=pow(int(c)%p,-1,p)
            return tuple((int(x)*inv)%p for x in v)
    raise ValueError("zero vector not projective")

def projective_stabilizer_bruteforce(p):
    selected={normalize_projective(x,p) for x in DIRECTIONS}
    gl=0;good=0
    for r,s,t,u in itertools.product(range(p),repeat=4):
        if (r*u-s*t)%p == 0:continue
        gl+=1
        target=set()
        for a,b,c in DIRECTIONS:
            v=((r*r*a+2*r*s*b+s*s*c)%p,
               (r*t*a+(r*u+s*t)*b+s*u*c)%p,
               (t*t*a+2*t*u*b+u*u*c)%p)
            target.add(normalize_projective(v,p))
        if target==selected:good+=1
    assert gl==p*(p-1)*(p*p-1)
    assert good==6*(p-1), (p,gl,good)
    return dict(p=p,GL2_order=gl,setwise_frame_stabilizer_order=good,
                GL2_orbit_size=gl//good,binomial_frame_choices=math.comb(p+1,3))

def null_coordinate_basis(p):
    assert p%2 and p>=3
    for d in DIRECTIONS:assert detq(d,p)==0
    coords=list(itertools.product(range(p),repeat=3))
    physical=[((a+b)%p,b,(b+c)%p) for a,b,c in coords]
    assert len(set(physical))==p**3
    return coords,np.asarray(physical,dtype=int)

def dft_and_log(p):
    x=np.arange(p)
    z=np.exp(2j*np.pi/p)
    F=z**(x[:,None]*x[None,:])/math.sqrt(p)
    I=np.eye(p,dtype=complex)
    assert np.max(np.abs(F.conj().T@F-I))<1e-12
    assert np.max(np.abs(np.linalg.matrix_power(F,4)-I))<1e-12
    h=np.zeros((p,p),complex)
    phases=((1,0),(1j,-math.pi/2),(-1,math.pi),(-1j,math.pi/2))
    for eig,theta in phases:
        projector=sum((I if power==0 else
             np.linalg.matrix_power(F,power)/(eig**power))
             for power in range(4))/4
        h+=theta*projector
    assert np.max(np.abs(h-h.conj().T))<2e-12
    assert np.max(np.abs(expm(-1j*h)-F))<2e-12
    return F,h

def exact_null_frame_clock():
    cases=[]
    for p in (3,5,7):
        _,points=null_coordinate_basis(p)
        F,h=dft_and_log(p)
        I=np.eye(p)
        H=np.kron(np.kron(h,I),I)+np.kron(np.kron(I,h),I)+np.kron(np.kron(I,I),h)
        U=np.kron(np.kron(F,F),F)
        assert np.max(np.abs(H-H.conj().T))<1e-11
        uniform=float(np.max(np.abs(np.abs(U)**2-1/(p**3))))
        assert uniform<2e-12
        dv=(points[:,None,:]-points[None,:,:])%p
        nonnull=((dv[:,:,0]*dv[:,:,2]-dv[:,:,1]**2)%p)!=0
        forbidden=float(np.max(np.abs(H[nonnull])))
        assert forbidden<1e-11,forbidden
        edge_count=int(np.count_nonzero(np.triu(np.abs(H)>1e-10,1)))
        expected=3*(p**3)*(p-1)//2
        assert edge_count==expected,(p,edge_count,expected)
        if p==3:
            sys.path.insert(0,str(ROOT/"analysis"))
            import w33_20261108_s4_harmonic_qdual as native
            n_edges,_,n_ei,_,_=native.complex27()
            assert len(n_edges)==108
            active=np.argwhere(np.triu(np.abs(H)>1e-10,1))
            native_nodes=[native.IX[tuple(v)] for v in points.tolist()]
            mapped={tuple(sorted((native_nodes[int(a)],native_nodes[int(b)]))) for a,b in active}
            assert len(mapped)==81 and mapped.issubset(n_ei.keys())
        shift=np.roll(I,1,axis=0)
        translation_break=float(np.linalg.norm(h@shift-shift@h))
        assert translation_break>0.1
        # Three commuting line-supported Hamiltonians are ONE constant
        # Hamiltonian, not only a circuit of noncommuting switched gates.
        cases.append(dict(p=p,modes=p**3,
            selected_rank_one_directions=[list(x) for x in DIRECTIONS],
            exact_flat_probability=1/(p**3),
            max_flat_probability_error=uniform,
            maximal_forbidden_nonnull_hopping_magnitude=forbidden,
            actual_undirected_null_hopping_edges=edge_count,
            native_27_graph_edge_count=(108 if p==3 else None),
            selected_hops_are_subset_of_native_27_graph=(p==3),
            translation_shift_commutator_Frobenius=translation_break,
            operator_norm_upper_bound_3pi=3*math.pi,
            architecture="H=h_F tensor I tensor I + I tensor h_F tensor I + I tensor I tensor h_F, with exp(-i h_F)=DFT_p and zero couplings outside three null directions"))
    groups=[projective_stabilizer_bruteforce(p) for p in (3,5,7)]
    return dict(status="EXACT_STRICTLY_NULL_SUPPORTED_STATIC_HAMILTONIAN_FLAT_MIXING",
        tested_cases=cases,
        frame_symmetry_orbit_checks=groups,
        all_odd_prime_theorem="Choose 3 independent isotropic vectors as a basis. The one-site Fourier F_p has F_p^4=I and Hermitian polynomial logarithm h_p. Its tensor sum H is Hermitian, strictly supported on one of those 3 null line families off diagonal, and exp(-iH)=F_p^tensor3, a complex Hadamard matrix. No translation invariance or SL2 covariance is claimed.",
        first_pulse_count_is_one=True,
        commuting_directional_generators=3,
        earlier_affine_no_go_not_contradicted=True,
        stronger_novelty_boundary="Fourier tensor products and Hermitian matrix logarithms are standard. The W33-specific point is that three isotropic basis directions realize the full transform with strict null-edge support, provided homogeneous finite-Lorentz covariance is relinquished.",
        physical_caveat="An inhomogeneous finite-dimensional exact mixer is not a relativistic clock, calibrated Hamiltonian, quantum gravity, or universal one-photon computer.")

def framed_spatial_maxwell():
    result=[]
    for p in (3,5,7,11,17,31):
        p=int(p)
        ratio=math.sin(math.pi/p)/(math.pi/p)
        dispersion_ratio=ratio**2
        # Fixed 3D spatial unit torus, time is an ADDED independent
        # continuous evolution parameter, not a theorem about det(S).
        a=np.array([np.exp(2j*np.pi/p)-1,0,0])
        K=np.vdot(a,a).real*np.eye(3)-np.outer(a,a.conj())
        spectrum=np.linalg.eigvalsh(K)
        assert abs(spectrum[0])<1e-12
        assert np.max(np.abs(spectrum[1:]-4*math.sin(math.pi/p)**2))<1e-12
        result.append(dict(p=p,spatial_sites=p**3,spatial_edge_channels=3,
            transverse_modes_per_nonzero_momentum=2,
            uniform_Wilson_holonomy_modes=3,
            transverse_nonzero_momentum_degrees=2*(p**3-1),
            total_gauge_inequivalent_real_edge_modes=2*(p**3-1)+3,
            single_axis_lattice_to_continuum_omega_squared_ratio=dispersion_ratio,
            relative_dispersion_error=abs(1-dispersion_ratio)))
    assert result[-1]["relative_dispersion_error"]<.004
    assert all(result[i+1]["relative_dispersion_error"]<result[i]["relative_dispersion_error"] for i in range(len(result)-1))
    return dict(status="EXPLICIT_3_SPATIAL_AXES_DISCRETE_MAXWELL_NOT_NATIVE_LORENTZ_EMERGENCE",
       cases=result,
       fixed_physical_setup="Unit-length spatial 3-torus T3, lattice spacing 1/p, added continuous time, positive Maxwell action with ordinary temporal electric kinetic term and square-plaquette magnetic curvature.",
       exact_Bloch_operator="K(k)=||a(k)||^2 I3-a(k) a(k)^dagger, a_i(k)=exp(2pi i k_i/p)-1; eigenvalues (0,||a||²,||a||²) for k !=0.",
       continuum_dispersion="omega_p(k)^2 = 4p^2 sum_i sin²(pi k_i/p) -> 4pi² |k|² at fixed integer spatial momentum.",
       choice_of_frame_cost="Select 3 projective null directions out of p+1, generating binomial(p+1,3) symmetry-related frames. GL2(p) setwise frame stabilizer has 6(p-1) elements.",
       material_limitation="This recovers standard lattice U(1) by explicitly installing external time, a Euclidean positive spatial metric and an anisotropic frame. It DOES NOT derive 3+1 Lorentz invariance from the original determinant's 2+1 analogy, dynamical frame selection, a measured coupling, or physical charged matter.")

def cubic_anchored_e6(root=ROOT):
    sys.path.insert(0,str(root/"analysis"))
    import w33_pass11261_g26_cartan_coordinate_map as mod
    parent=mod._load(root/"analysis/w33_pass11218_e8_cubic_cartan_kernel.py","w33_local_frame_e6_cubic_anchor")
    records=parent.load_parent().build_records()
    assert len(records)==1620
    rng=np.random.default_rng(26081109)
    phi=rng.normal(size=81)+1j*rng.normal(size=81)
    M=np.zeros((81,81),complex)
    for u,x,o,c in records:M[o,x]+=c*phi[u]
    assert np.linalg.matrix_rank(M,tol=1e-8)==78
    Xi=np.linalg.qr(rng.normal(size=(81,3))+1j*rng.normal(size=(81,3)))[0]
    assert np.max(np.abs(Xi.conj().T@Xi-np.eye(3)))<1e-12
    def cubic(A):
        return sum(c*A[u,0]*A[x,1]*A[o,2] for u,x,o,c in records)
    val=cubic(Xi)
    assert abs(val)>1e-5
    w=rng.normal(size=81)+1j*rng.normal(size=81)
    w-=Xi@(Xi.conj().T@w);w/=np.linalg.norm(w)
    tangent=Xi.copy(); tangent[:,0]=w
    # Cubic derivative along the tangent rotation Xi0 -> cos(t)Xi0+sin(t)w.
    dval=cubic(tangent)
    det_jacobian=float(abs((val.conjugate()*dval).real))
    assert det_jacobian>1e-7,(abs(val),abs(dval),det_jacobian)
    phase=.37
    Xi_rel=Xi.copy()
    Xi_rel[:,0]*=np.exp(1j*phase)
    Xi_rel[:,1]*=np.exp(-1j*phase)
    assert abs(cubic(Xi_rel)-val)<1e-11
    assert np.max(np.abs(Xi_rel.conj().T@Xi_rel-np.eye(3)))<1e-12
    T=np.diag([.4,.6,.8])
    def complete(A):
        U=A.conj()
        return M+U@T@U.T
    assert np.linalg.matrix_rank(complete(Xi),tol=1e-8)==81
    Xi_rot=Xi.copy();Xi_rot[:,0]*=np.exp(1j*phase)
    z0,mag0=np.linalg.slogdet(complete(Xi))
    z1,mag1=np.linalg.slogdet(complete(Xi_rot))
    phase_error=float(abs(z1/z0-np.exp(-2j*phase)))
    assert phase_error<1e-8 and abs(mag1-mag0)<1e-8
    return dict(status="NATIVE_CUBIC_ANCHOR_ONLY_REMOVES_AT_MOST_TWO_SCALAR_MODULI",
        source_cubic_signed_records=len(records),
        original_81_state_alternating_mass_rank=78,
        completed_mass_rank=81,
        quartic_Stiefel_real_minimum_dimension=477,
        complex_native_cubic_contraction_magnitude=abs(val),
        two_real_component_cubic_Jacobian_nondegeneracy_witness=det_jacobian,
        quartic_plus_complex_cubic_regular_level_set_dimension=475,
        maximal_E6_gauge_orbit_dimension=78,
        conditional_remaining_gauge_inequivalent_moduli_lower_bound=397,
        continuous_relative_spurion_phase_preserves_Gram_and_cubic=True,
        phase_unpinned_in_quartic_only_mass_determinant_error=phase_error,
        conditional_invariant="Adding kappa*abs(C(Xi)-C0)^2 is a *candidate* tensor-anchored scalar interaction only if invariance of this exact 81-index contraction under the desired actual E6 gauge action is independently certified.",
        evidence_boundary="Computes exact mass contraction and generic Jacobian witness, not full E6 generators, gauge invariant vacuum, anomaly cancellation, SM masses, RG stability, or theta-bar; 397 bound is conditional on accepted extra cubic interaction.")

def photonic_controls():
    p=3;rows=p**3
    three_basis_spatial_modes=rows
    max_two_mode_couplers=3*(p**3)*(p-1)//2
    # Ideal three sequential Fourier layers can be synthesized with at
    # most p(p-1)/2 arbitrary two-mode mixing operations per p-mode block.
    assert max_two_mode_couplers==81
    transmission=np.array([.98,1.,1.])
    survival=float(transmission.mean())
    conditional=transmission/transmission.sum()
    total_variation=float(np.sum(abs(conditional-1/3))/2)
    common=np.array([.98,.98,.98])
    common_tv=float(np.sum(abs(common/common.sum()-1/3))/2)
    delta=math.pi/3
    echo_probability=abs((2+np.exp(1j*delta))/3)**2
    assert abs(echo_probability-7/9)<1e-12
    assert 0<total_variation<.01 and common_tv<1e-15
    return dict(status="IDEAL_OPTICAL_HARDWARE_COUNTS_AND_PHASE_SENSITIVE_ECHO",
       physical_modes=three_basis_spatial_modes,selected_null_directions=3,
       p_mode_DFT_blocks_total=3*(p**2),
       max_two_mode_couplers_in_naive_DFT_triangular_synthesis=max_two_mode_couplers,
       phase_error_echo_radians=delta,
       single_address_phase_echo_return_probability=float(echo_probability),
       differential_rail_intensity_transmission=list(map(float,transmission)),
       differential_transmission_average_survival=survival,
       differential_transmission_conditional_total_variation=total_variation,
       common_mode_transmission_conditional_total_variation=common_tv,
       source_and_detector_efficiency_not_assumed=True,
       physical_scope="Optical unitary and toy rail-loss/phase controls only; routing, propagation delays, correlated drifts, error correction, total chip losses, heralding, and real process tomography unmeasured. Cubic mode count 3^n remains exponential for n logical qutrit factors.")

def cosmology_and_clock_firewall(root=ROOT):
    old=read_json("analysis/toe_uv/halofit_check_orig.json",root)["rows"]
    hf=read_json("analysis/toe_uv/halofit_check_hf.json",root)["rows"]
    hm=read_json("analysis/toe_uv/hmcode_check.json",root)["hm"]
    patched=[]
    for z,k in itertools.product(("0.01","1.0"),("0.1","1.0","3.0")):
        base=hf["lcdm_lambda"][z][k]
        err=abs(hf["lcdm_scf"][z][k]/base-1)
        assert err<3e-6
        patched.append(dict(z=z,k=k,original_scf_Lambda_ratio=old["lcdm_scf"][z][k]/base,
                            patched_scf_Lambda_ratio=hf["lcdm_scf"][z][k]/base))
    grids=[]
    for z,k in itertools.product(("0.01","1.0"),("0.1","1.0","3.0")):
        hr=hf["fading_fit"][z][k]/hf["cpl_fit"][z][k]-1
        mr=hm["fading_fit"][z][k]/hm["cpl_fit"][z][k]-1
        grids.append(dict(z=z,k=k,Halofit_fading_over_CPL_minus_one=hr,
                          HMcode_fading_over_CPL_minus_one=mr,
                          two_prescription_difference=mr-hr))
    src=read_json("data/w33_pass12633_flavour_clock.json",root)
    min_sens=min(src["sensitivity_h3"]["omega"].values())
    bound=src["kappa_mu_max"]/min_sens
    assert src["min_violation_factor"]>1e6 and bound<6e-7
    score={}
    for survey,pre,post in (
        ("DES_Y3","analysis/toe_uv/sign_des_orig.json","analysis/toe_uv/sign_des.json"),
        ("KiDS_Legacy","analysis/toe_uv/sign_des_kids_orig.json","analysis/toe_uv/sign_des_kids.json")):
        a=read_json(pre,root);b=read_json(post,root)
        prev=a["CPL"]["des"]-a["free_neg"]["des"]
        nxt=b["CPL"]["des"]-b["free_neg"]["des"]
        assert prev>2.5 and -1<nxt<0
        score[survey]=dict(original_CPL_minus_fading_chi2=prev,
                           corrected_fixed_background_delta_chi2=nxt)
    return dict(status="HALOFIT_AND_HMCODE_PATCHED_FINITE_GRID_REPLAY_PLUS_FLAVOUR_CLOCK_GUARD",
       Lambda_control_cells=patched,patched_two_prescription_fading_CPL_ratio_cells=grids,
       fixed_background_shear_model_comparison=score,
       independent_corrected_heldout_DES_KiDS_likelihood_executed=False,
       S7_S8_prepatch_shear_results_withdrawn=True,
       min_A4_flavour_mass_ratio_sensitivity_per_Mp=min_sens,
       maximum_visible_rolling_flavour_admixture_under_proxy=bound,
       sequestering_ratio_visible_over_dark_upper_bound=src["kappa_mu_max"]/.05,
       provenance="Uses already committed PASS12632 corrected CLASS/Halofit/HMcode numbers and PASS12633 sensitivity proxy; no new CLASS run, no independent raw shear chains, no coupled-dark-matter nonlinear calibration. The flavour admixture bound assumes linear inherited proxy sensitivity and no cancellations.")

def produce(root=ROOT):
    return dict(schema="w33.20261108.frame_selection_null_clock_five_fronts.v1",
        clock=exact_null_frame_clock(),
        Maxwell=framed_spatial_maxwell(),
        E6=cubic_anchored_e6(root),
        photonic=photonic_controls(),
        cosmology=cosmology_and_clock_firewall(root),
        sixth_connection="One symmetry-breaking choice of three independent null directions gives both a p^3-mode exact static flat-mixing Hamiltonian and an explicitly time-augmented cubic spatial Maxwell model with two transverse k!=0 branches. This is a *counterexample to an overbroad no-go*, not emergence of physics from finite Lorentz symmetry.",
        conclusion_boundary="Exact finite linear algebra and toy controls only. No quantum gravitation, calibrated energy scale, native 3+1 derivation, anomaly-free E6 vacuum, experimentally demonstrated one-photon processor, or new DES/KiDS likelihood.")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="data/w33_20261108_null_frame_selection_five_fronts.json")
    args=parser.parse_args()
    result=produce()
    path=ROOT/args.out
    path.parent.mkdir(exist_ok=True,parents=True)
    path.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps(dict(output=str(path),
         clock_errors=[(x["p"],x["max_flat_probability_error"],x["maximal_forbidden_nonnull_hopping_magnitude"]) for x in result["clock"]["tested_cases"]],
         maxwell_p31_continuum_error=result["Maxwell"]["cases"][-1]["relative_dispersion_error"],
         e6_residual_moduli_lower_bound=result["E6"]["conditional_remaining_gauge_inequivalent_moduli_lower_bound"],
         photon_echo=result["photonic"]["single_address_phase_echo_return_probability"],
         cosmology_heldout_performed=result["cosmology"]["independent_corrected_heldout_DES_KiDS_likelihood_executed"])))
if __name__=="__main__":main()
