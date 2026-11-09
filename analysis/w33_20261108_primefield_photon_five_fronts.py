#!/usr/bin/env python3
"""Independent 2026-11-08 next-5 W33 experiments: prime-field Maxwell,
E6 moduli and phase orbit, exact chirp versus null locality, single-photon
controlled-SUM rail routing, and fail-closed corrected cosmology.
All results are mathematical/certificate audits; no experimental TOE claim.
"""
from __future__ import annotations
import argparse
from collections import Counter
import itertools
import json
import math
import sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

def readj(path,root=ROOT):
    return json.loads((root/path).read_text(encoding="utf-8"))

def dirs(p):
    return [(1,x,(x*x)%p) for x in range(p)]+[(0,0,1)]

def dotp(k,d,p):
    return sum(x*y for x,y in zip(k,d))%p

def prime_bloch_maxwell():
    """Exact Fourier blocks for the natural complete projective-null set."""
    results=[]
    for p in (3,5,7,11,17,31):
        ds=dirs(p)
        assert len(ds)==p+1
        def B(k):
            return sum(2-2*math.cos(2*math.pi*dotp(k,d,p)/p) for d in ds)
        soft=B((1,0,0))
        lateral=B((0,1,0))
        quadratic=B((0,0,1))
        exact_soft=2*p*(1-math.cos(2*math.pi/p))
        assert abs(soft-exact_soft)<1e-10
        assert abs(lateral-2*p)<1e-10
        assert quadratic>=2*(p-math.sqrt(p))-1e-9
        assert quadratic<=2*(p+2+math.sqrt(p))+1e-9
        if p>=17:
            assert lateral/soft>10
        # Square-plaquette Fourier block is ||a||^2 I - a a*,
        # a_i=exp(2*pi*i*k.d_i/p)-1. Its nonzero eigenvalue repeats p
        # times for every k !=0, with precisely one gradient null vector.
        k=(1,1,1)
        a=np.array([np.exp(2j*np.pi*dotp(k,v,p)/p)-1 for v in ds])
        b=float(np.vdot(a,a).real)
        K=b*np.eye(p+1)-np.outer(a,a.conj())
        assert np.max(abs(K-K.conj().T))<1e-12
        ev=np.linalg.eigvalsh(K)
        assert abs(ev[0])<1e-9
        assert np.max(abs(ev[1:]-b))<1e-8
        results.append(dict(p=p,vertices=p**3,edge_directions=p+1,
            nonzero_momentum_transverse_branch_count=p,
            physical_nonzero_k_modes=p*(p**3-1),
            square_only_global_harmonics=p+1,
            local_square_Bloch_soft_axis=soft,
            local_square_Bloch_lateral_axis=lateral,
            local_square_Bloch_quadratic_axis=quadratic,
            lateral_over_soft=lateral/soft,
            exact_lateral=2*p,exact_soft=exact_soft,
            quadratic_Gauss_lower_bound=2*(p-math.sqrt(p))))
    # q3 native 27-site case: adding one length-three cycle per
    # projective null line, normalized over its 3 sites, adds eigenvalue 3
    # for precisely the zero-gradient edge directions at each momentum.
    p=3;ds=dirs(3);physical=Counter();gradients=0
    for k in itertools.product(range(p),repeat=3):
        zero=sum(dotp(k,v,p)==0 for v in ds)
        L=round(sum(2-2*math.cos(2*math.pi*dotp(k,v,p)/p) for v in ds))
        if k==(0,0,0):
            physical[3]+=4
        else:
            gradients+=1
            physical[L]+=(3-zero)
            physical[L+3]+=zero
    physical={str(k):v for k,v in sorted(physical.items()) if v}
    assert gradients==26
    assert physical=={"3":4,"6":12,"9":40,"12":26},physical
    old=readj("data/w33_20261108_five_physical_falsifiers.json")["maxwell"]
    assert {str(k):v for k,v in old["magnetic_spectrum"].items() if str(k)!="0"}==physical
    return dict(status="EXACT_PRIME_BLOCH_STRUCTURAL_DISPERSION_BOUND",
       natural_full_null_direction_family=results,
       q3_triangle_plus_square_spectral_multiplicities=physical,
       q3_gradient_modes=gradients,q3_square_only_boundary_rank=78,
       q3_square_only_harmonic_modes=4,
       Fourier_proof="K_square(k)=||a(k)||^2 I-a(k)a(k)^*, a_i=e^(2pi i k.dot(d_i)/p)-1, rank=p at all k !=0; four uniform modes remain at p3. q3 triangular p-gons add eigenvalue p only when k.dot(d_i)=0.",
       rigorous_asymptotic="Soft k=(1,0,0): lambda=2p(1-cos(2pi/p))~4pi^2/p; lateral k=(0,1,0): lambda=2p; quadratic k=(0,0,1): lambda>=2(p-sqrt(p)). No common scalar stiffness rescales all three to isotropic 3D massless Maxwell; p extra transverse branches remain at nonzero k.",
       limits="This is the unprojected complete-null-direction square model and fixed-coordinate p->infinity identification; additional gauge constraints, Wilson/matter sectors, anisotropic stiffness, subquotients or nontrivial embeddings might alter the conclusion.")

def e6_moduli_and_cp_orbit(root=ROOT):
    """Native matrix, exact dimension bound and phase-transform law."""
    sys.path.insert(0,str(root/"analysis"))
    import w33_pass11261_g26_cartan_coordinate_map as util
    src=util._load(root/"analysis/w33_pass11218_e8_cubic_cartan_kernel.py","e6_phase_orbit_20261108")
    rec=src.load_parent().build_records()
    assert len(rec)==1620
    rng=np.random.default_rng(202611082)
    phi=rng.normal(size=81)+1j*rng.normal(size=81)
    M=np.zeros((81,81),complex)
    for u,x,o,c in rec:M[o,x]+=c*phi[u]
    assert np.linalg.matrix_rank(M,tol=1e-8)==78
    assert np.max(abs(M+M.T))<1e-11
    Xi=np.linalg.qr(rng.normal(size=(81,3))+1j*rng.normal(size=(81,3)))[0]
    assert np.max(abs(Xi.conj().T@Xi-np.eye(3)))<1e-12
    coeff=np.diag([.4,.6,.8])
    def mass(xi):
        u=xi.conj()
        return M+u@coeff@u.T
    def det(xi):
        return np.linalg.slogdet(mass(xi))
    sign,log=det(Xi)
    assert np.linalg.matrix_rank(mass(Xi),tol=1e-8)==81
    theta=math.pi/7
    Xi2=Xi.copy();Xi2[:,0]*=np.exp(1j*theta)
    sign2,log2=det(Xi2)
    assert np.max(abs(Xi.conj().T@Xi-Xi2.conj().T@Xi2))<1e-12
    pred=np.exp(-2j*theta)
    err=abs(sign2/sign-pred)
    assert err<1e-8 and abs(log2-log)<1e-8,(err,log2-log)
    dim=2*81*3-3*3
    gauge_dim=78
    return dict(status="E6_POTENTIAL_HAS_GAUGE_INEQUIVALENT_FLAT_MODULI_AND_UNPINNED_CP_PHASE",
      native_signed_records=len(rec),native_rank_before=78,native_rank_after=81,
      minimum_manifold="V_3(C^81)",real_dimensions=dim,
      upper_bound_E6_gauge_orbit_dimension=gauge_dim,
      lower_bound_unlifted_flat_moduli_after_E6_quotient=dim-gauge_dim,
      conditional_lower_bound_if_extra_U3_flavor_is_gauged=dim-gauge_dim-9,
      potential="Tr((Xi^dagger Xi-v^2 I3)^2) with lambda>0",
      potential_invariant_phase_rotation_of_first_spurion=theta,
      determinant_ratio_phase_error=err,
      determinant_log_magnitude_invariance_error=abs(log2-log),
      determinant_ratio_law="Under Xi[:,0]->exp(i theta)Xi[:,0], det(M+U T U^T) -> exp(-2i theta) times det, at corank=3 with U=conj(Xi) and positive coefficient T.",
      caveat="Flat-moduli bound pertains to this isolated quartic potential, not a complete gauged E6 Lagrangian. A VEV rephasing might be an anomalous field redefinition; it is NOT by itself physical theta-bar, and no anomaly or radiative CP cancellation is claimed.")

def chirp_locality_projection():
    """Perfect Gaussian mixing, but its particular principal H is not null-local."""
    cases=[]
    for p in (3,5,7):
        a,b,c=np.indices((p,p,p))
        Q=(a*c-b*b)%p
        psi=np.exp(-2j*np.pi*Q/p)
        u=np.fft.ifftn(psi)
        target=1/p**3
        max_err=float(np.max(abs(abs(u)**2-target)))
        assert max_err<1e-12
        centered=(Q+(p//2))%p-(p//2)
        H=np.fft.ifftn(2*math.pi*centered/p)
        assert np.max(abs(H.imag))<1e-10
        null=((a*c-b*b)%p==0)
        null[0,0,0]=False
        nonnull=~null;nonnull[0,0,0]=False
        energy_total=float(np.sum(abs(H[nonnull| null])**2))
        off=float(np.sum(abs(H[nonnull])**2))
        fraction=off/energy_total
        assert fraction>.20 and fraction<1
        cases.append(dict(p=p,flat_probability=target,max_flat_error=max_err,
          principal_log_off_null_energy_fraction=fraction,
          off_null_hopping_count=int(np.count_nonzero(abs(H[nonnull])>1e-10)),
          off_null_possible_count=int(nonnull.sum()),
          minimum_relative_offdiagonal_Frobenius_distance_for_fixed_principal_H=math.sqrt(fraction)))
    return dict(status="EXACT_FLAT_CHIRP_WITH_PRINCIPAL_BRANCH_LOCALITY_PENALTY",
      data=cases,condition="Fixed principal continuous-time Hermitian logarithm H(k)=(2pi/p)*centered(det(k)) and translation-invariant convolutions.",
      theorem="Fourier projection onto supported null displacements minimizes Frobenius distance for this fixed H, so energy fraction on excluded links is the exact squared relative projection error.",
      scope="Other 2pi spectral branch lifts, other flat unitaries and time-dependent/null-supported products are NOT excluded. An exact finite Gaussian Hadamard is already known in the repo; the new datum is the energetic projection penalty.")

def single_photon_csum():
    """Logical two-qutrit controlled SUM on one photon = permutation of rails."""
    N=27
    P=np.zeros((N,N),int)
    perm=[]
    for a,b,c in itertools.product(range(3),repeat=3):
        col=9*a+3*b+c
        row=9*a+3*((b+a)%3)+c
        P[row,col]=1
        perm.append(row)
    assert np.array_equal(P.T@P,np.eye(N,dtype=int))
    cycles=[];seen=set()
    for i in range(N):
        if i in seen:continue
        cyc=[];j=i
        while j not in seen:
            seen.add(j);cyc.append(j);j=perm[j]
        cycles.append(cyc)
    count=Counter(map(len,cycles))
    assert count=={1:9,3:6},count
    swaps=sum(len(c)-1 for c in cycles)
    assert swaps==12
    psi=np.zeros(N,complex)
    for a in range(3):psi[9*a]=1/math.sqrt(3)
    out=P@psi
    reduced=np.zeros((3,3),complex)
    for a in range(3):
        for a2 in range(3):
            reduced[a,a2]=np.vdot(out[9*a2:9*a2+9],out[9*a:9*a+9])
    assert np.allclose(reduced,np.eye(3)/3)
    zeta9=np.exp(2j*math.pi/9)
    t=np.array([1,zeta9,zeta9**-1])
    diagonal=np.array([t[a] for a in range(3) for _ in range(9)])
    assert sum(abs(diagonal-1)>1e-10)==18
    p_in=np.zeros(27,complex)
    p_in[0]=p_in[9]=1/math.sqrt(2)
    p_magic=diagonal*p_in
    assert np.array_equal(abs(p_magic)**2,abs(p_in)**2)
    omega=np.exp(2j*math.pi/3)
    F=np.array([[omega**(i*j)/math.sqrt(3) for j in range(3)] for i in range(3)])
    F27=np.kron(np.kron(F,np.eye(3)),np.eye(3))
    q_before=np.array([abs((F27@p_in)[9*a])**2 for a in range(3)])
    q_after=np.array([abs((F27@p_magic)[9*a])**2 for a in range(3)])
    assert np.max(abs(q_before-q_after))>.05
    return dict(status="IDEAL_ONE_PHOTON_27_RAIL_CSUM_WITH_EXPLICIT_RESOURCE_BOUND",
      mode_count=27,logical_encoding="|a,b,c> represented by one photon in rail 9a+3b+c",
      mapping="(a,b,c)->(a,b+a mod3,c)",permutation_cycle_lengths={str(k):v for k,v in count.items()},
      minimum_arbitrary_rail_swap_count=swaps,
      path_csum_deterministic_conditional_on_lossless_routing=True,
      intra_particle_qutrit_nonseparability_Schmidt_rank=3,
      ninth_root_phase_required_nontrivial_rails=18,
      intensity_blindness_to_direct_ninth_root_phase=True,
      Fourier_control_basis_readout_distribution_before=list(map(float,q_before)),
      Fourier_control_basis_readout_distribution_after=list(map(float,q_after)),
      max_phase_sensitive_readout_difference=float(max(abs(q_after-q_before))),
      rail_requirement_by_logical_qutrit_count={str(n):3**n for n in (1,2,3,4,5,8,10)},
      physical_distinction="Controlled-SUM of tensor factors inside ONE photon is a passive unitary rail permutation; independent photons' entangling gates are NOT implemented by this argument. Destructive photodetection of an ancilla mode also destroys the same photon; direct T9 rail phases avoid the ideal magic-state measurement.",
      scalability_limit="n logical qutrit factors encoded in orthogonal single-photon modes require >=3^n distinguishable mode states. Passive routing does not evade this Hilbert-space counting bound.")

def corrected_cosmology(root=ROOT):
    prior=readj("analysis/toe_uv/halofit_check_orig.json",root)["rows"]
    fixed=readj("analysis/toe_uv/halofit_check_hf.json",root)["rows"]
    fluid=readj("analysis/toe_uv/hf_matched_fluid.json",root)
    checks=[]
    for z,k in itertools.product(("0.01","1.0"),("0.1","1.0","3.0")):
        ref=fixed["lcdm_lambda"][z][k]
        pre=prior["lcdm_scf"][z][k]
        post=fixed["lcdm_scf"][z][k]
        err=abs(post/ref-1)
        assert err<3e-6
        checks.append(dict(z=z,k=k,original_scf_to_Lambda=pre/ref,patched_scf_to_Lambda=post/ref))
    assert fluid["exp_neg"]["max_frac_dev_vs_fluid"]["patched"]<.001
    for label in ("free_neg","free_pos"):
        assert .03<fluid[label]["max_frac_dev_vs_fluid"]["patched"]<.05
    pair={}
    for tag,a,b in (
      ("DES_Y3","analysis/toe_uv/sign_des_orig.json","analysis/toe_uv/sign_des.json"),
      ("KiDS_Legacy","analysis/toe_uv/sign_des_kids_orig.json","analysis/toe_uv/sign_des_kids.json")):
        old=readj(a,root);new=readj(b,root)
        for model in ("CPL","free_neg"):
            assert abs(old[model]["S8"]-new[model]["S8"])<1e-12
        x=old["CPL"]["des"]-old["free_neg"]["des"]
        y=new["CPL"]["des"]-new["free_neg"]["des"]
        assert x>2.5 and -1<y<0
        pair[tag]=dict(original_CPL_minus_fading=x,patched_CPL_minus_fading=y,
                       shift_due_to_recomputed_model_comparison=y-x,
                       patched_min_chi2_pairwise_absolute_difference=abs(y))
    # Parallel Pass12632 addendum 2: HMcode patched scalar-field control.
    # Compare *nonlinear boost* ratios, not empirical shear likelihoods.
    hm=readj("analysis/toe_uv/hmcode_check.json",root)
    hz="0.01";hk="1.0"
    hm_ratio=hm["hm"]["fading_fit"][hz][hk]/hm["hm"]["cpl_fit"][hz][hk]-1
    hf_ratio=fixed["fading_fit"][hz][hk]/fixed["cpl_fit"][hz][hk]-1
    hm_lcdm_error=abs(hm["hm"]["lcdm_scf"][hz][hk]/hm["hm"]["lcdm_lambda"][hz][hk]-1)
    assert 0<hm_ratio<.03 and 0<hf_ratio<.03
    assert abs(hm_ratio-hf_ratio)<.02
    assert hm_lcdm_error<.004
    return dict(status="HALOFIT_HMCODE_TWO_PRESCRIPTION_CHECK_AND_WITHDRAWN_HELDOUT_INFERENCE",
        two_nonlinear_prescriptions_at_z001_k1=dict(
            HMcode_fading_over_CPL_minus_one=hm_ratio,
            Halofit_fading_over_CPL_minus_one=hf_ratio,
            HMcode_scalar_LCDM_control_relative_error=hm_lcdm_error,
            physical_scope="Two patched CLASS prescriptions; neither is calibrated as a general interacting-dark-matter simulation or a fresh shear likelihood."),
        lambda_control_cells=checks,matched_fluid_max_deviation={
           t:{k:float(v) for k,v in fluid[t]["max_frac_dev_vs_fluid"].items()}
           for t in ("free_neg","free_pos","exp_neg")},
        fixed_background_pairwise_chi2=pair,heldout_likelihood_recomputed=False,
        S7_S8_original_shear_claims_withdrawn=True,
        comparison_scope="Replays already committed patched reference spectra and fixed-background nuisance-refitted chi2; no raw KiDS/DES likelihood or cross-survey covariance was executed. 4% coupled-model residual vs fluid is NOT a validation of uncalibrated coupled-dark-matter Halofit physics.",
        source="analysis/PASS12632_HALOFIT_SCF_BUG.md")

def produce(root=ROOT):
    return dict(schema="w33.20261108.primefield_photon_five_fronts.v1",
      prime_Maxwell=prime_bloch_maxwell(),
      E6=e6_moduli_and_cp_orbit(root),
      quantum_clock=chirp_locality_projection(),
      photonic=single_photon_csum(),
      cosmology=corrected_cosmology(root),
      sixth_connection="Projective null direction count p+1 yields p transverse edge modes at nonzero k, not two; single-photon SUM does not require photon-photon interactions but incurs 3^n modes.",
      evidence_boundary="Exact finite algebra, native tensor replay, ideal single-photon permutation, and sourced corrected Halofit control only. No predictive TOE, two-polarization continuum, physical E6 SM vacuum, scalable single photon quantum computer, or new cosmological evidence.")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="data/w33_20261108_primefield_photon_five_fronts.json")
    args=ap.parse_args()
    d=produce()
    p=ROOT/args.out;p.parent.mkdir(exist_ok=True,parents=True)
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"out":str(p),"p31_lateral_over_soft":d["prime_Maxwell"]["natural_full_null_direction_family"][-1]["lateral_over_soft"],
        "E6_gauge_inequivalent_moduli_lower_bound":d["E6"]["lower_bound_unlifted_flat_moduli_after_E6_quotient"],
        "q5_principal_nonnull_fraction":d["quantum_clock"]["data"][1]["principal_log_off_null_energy_fraction"],
        "single_photon_SUM_swaps":d["photonic"]["minimum_arbitrary_rail_swap_count"],
        "cosmology_revalidated_heldout":d["cosmology"]["heldout_likelihood_recomputed"]},indent=2))
if __name__=="__main__":main()
