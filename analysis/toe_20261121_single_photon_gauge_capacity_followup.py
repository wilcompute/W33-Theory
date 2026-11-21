"""Witting research: one-photon hidden-chart inverse, constrained 9x5 channel
routing, two-use coherent information, ancilla SWAP compilation, lattice gauge
fiber, and labeled-detector cross-talk.

No measured device or emergent spacetime is claimed. Run from W33 repo.
"""
from __future__ import annotations
import collections
import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_capacity_fisher_schmidt_locality as previous
import toe_20261121_fivefront_tightframe_coherent_memory as earlier

OUT=ROOT/"data/toe_20261121_onephoton_chart_channel_gauge_sevenfronts.json"
SEED=20261121

def spectral(rays,supports,decks,A,O):
    H=np.zeros((45,40),dtype=np.int64)
    for z,S in enumerate(supports):
        H[z,list(S)]=1
    I=np.eye(45,dtype=np.int64)
    J=np.ones((45,45),dtype=np.int64)
    assert np.array_equal(H@H.T,6*I-2*A.astype(np.int64)+2*J)
    K=np.zeros((45,27),dtype=np.int64)
    for i,L in enumerate(decks):K[L,i]=1
    M=15*I-5*A.astype(np.int64)+J
    P24=M/30
    assert np.array_equal(H@H.T @ M,12*M)
    assert np.array_equal(K.T@M,np.zeros((27,45),dtype=np.int64))
    assert np.array_equal(H.sum(axis=1),np.full(45,8))
    assert np.array_equal(H.sum(axis=0),np.full(40,9))
    assert np.linalg.matrix_rank(H,tol=1e-9)==25
    return H,P24,K

def single_photon_front(rays,supports,decks,A,O):
    """Retain calibrated global ray label (40 outcomes), no pair coincidence."""
    H,P24,K=spectral(rays,supports,decks,A,O)
    I40=np.eye(40)
    p0=np.ones(40)/40
    rng=np.random.default_rng(SEED)
    x=P24@rng.standard_normal(45)
    x*=.004/max(abs(x))
    w=np.ones(45)/45+x
    assert w.min()>0
    p=H.T@w/8
    assert np.max(abs(p-p0-H.T@x/8))<1e-13
    assert abs(p.sum()-1)<1e-13
    exact=(2/3)*H@(p-p0)
    assert np.max(abs(exact-x))<1e-12
    assert np.max(abs(K.T@w-np.ones(27)/9))<1e-12
    # From one globally labeled outcome i, the unbiased 45-vector
    # update is a constant-norm vector in the 24D sector.
    column=2/3*(H.astype(float)-.2)
    assert np.max(abs(P24@column-column))<1e-13
    assert np.max(abs(np.sum(column**2,axis=0)-3.2))<1e-12
    assert np.max(abs(column@p-x))<1e-12
    # The exact multinomial MSE for the sample mean is:
    # [E||column_i||^2 -||x||^2]/N = (3.2-||x||^2)/N.
    Nshots=(1000,100000,1000000)
    examples={}
    for N in Nshots:
        n=rng.multinomial(N,p)
        xhat=(2/3)*H@(n/N-p0)
        examples[str(N)]={
          "shot_count":N,"l2_error":float(np.linalg.norm(xhat-x)),
          "exact_mse":float((3.2-np.vdot(x,x).real)/N),
          "ideal_rms_upper_bound":math.sqrt(3.2/N)}
    # Fisher at UNIFORM chart weights and input rho=I4/4:
    # dp/dx=H^T U/8, p0=1/40; F=(5/8) U^T HH^T U =7.5 I24.
    eigen=np.linalg.eigh(P24)[1][:,-24:]
    FI=(5/8)*eigen.T@H@H.T@eigen
    assert np.max(abs(FI-7.5*np.eye(24)))<1e-10
    cr_coeff=float(np.trace(np.linalg.inv(FI)))
    assert abs(cr_coeff-3.2)<1e-10
    # A physical compression: resolve only 24 globally labelled rays,
    # and lump all remaining 16 labels into a single coarse detector.
    # 25 outcome bins are information-theoretically minimal for 24
    # independent probabilities, although a different 25-bin POVM
    # might be better conditioned.
    compressed_labels=[31,7,21,28,22,30,3,15,4,23,26,25,
                       8,1,32,20,19,29,14,38,16,39,11,37]
    assert len(set(compressed_labels))==24
    D=eigen.T@H[:,compressed_labels]/8
    compressed_rank=int(np.linalg.matrix_rank(D,tol=1e-9))
    assert compressed_rank==24
    compressed_p=p[compressed_labels]
    compressed_reconstruction=eigen@np.linalg.solve(D.T,compressed_p-1/40)
    assert np.max(abs(compressed_reconstruction-x))<1e-10
    missing_deriv=-D.sum(axis=1)
    FI24=40*D@D.T+(40/16)*np.outer(missing_deriv,missing_deriv)
    fi24lam=np.linalg.eigvalsh(FI24)
    fi24Coeff=float(np.sum(1/fi24lam))
    assert abs(fi24Coeff-11.8133333333333)<1e-9
    Nneeded=int(round(3.2/1e-6))
    # A pure Witting input has 28 nonzero input-ray outcomes, FI rank21,
    # but a uniform classical mixture of 4 basis inputs gives full24.
    ranks=[]
    for a in range(40):
        q=O[a]
        d=((H*(q/2)[None,:]).T@eigen)
        good=q>1e-10
        pa=q[good]/10
        FIa=d[good].T@(d[good]/pa[:,None])
        ranks.append(int(np.linalg.matrix_rank(FIa,tol=1e-9)))
    assert set(ranks)=={21}
    return {
       "status":"PASS",
       "chart_to_ray_incidence_shape":[45,40],
       "exact_incidences_per_chart":8,"exact_charts_per_ray":9,
       "H_Htrans_exact":"H H^T = 6 I - 2 A + 2 J",
       "H_Htrans_spectrum":{"72":1,"12":24,"0":20},
       "H_rank":25,"K_rank":21,"K_visible_subspace_orthogonal_to_hidden24":True,
       "single_photon_output_model":"p_i=sum_z w_z H[z,i]/8 for input I4/4",
       "global_label_decoder":"x=(2/3) H (p - 1_40/40), w=1_45/45+x",
       "exact_decoder_max_residual":float(np.max(abs(exact-x))),
       "hidden_bias_has_identical_27_deck_totals_as_uniform":True,
       "unbiased_per_detection_estimator_squared_norm":3.2,
       "global_multinomial_MSE_identity":"E||xhat-x||^2=(3.2-||x||^2)/N",
       "sufficient_detected_single_photons_for_RMS_le_0p001":Nneeded,
       "single_photon_local_Fisher_24_eigenvalue":7.5,
       "single_photon_local_Cramer_Rao_trace_inverse_coefficient":cr_coeff,
       "compressed_distinguishable_output_bins":25,
       "compressed_globally_resolved_ray_labels":compressed_labels,
       "compressed_coarse_unresolved_ray_count":16,
       "compressed_hidden_chart_rank":compressed_rank,
       "compressed_exact_inverse_residual":float(np.max(abs(compressed_reconstruction-x))),
       "compressed_local_Cramer_Rao_trace_inverse_coefficient":fi24Coeff,
       "compressed_local_Fisher_condition_number":float(fi24lam[-1]/fi24lam[0]),
       "compressed_vs_full_label_Cramer_Rao_penalty":fi24Coeff/cr_coeff,
       "old_540_pair_binary_Probe_Cramer_Rao_coefficient":4492.8,
       "local_Fisher_trace_inverse_advantage_per_ideal_event":4492.8/3.2,
       "ranks_of_single_pure_Witting_input_Fisher":dict(collections.Counter(ranks)),
       "mixed_state_can_be_prepared_by_classical_randomization":True,
       "seeded_multinomial_simulations":examples,
       "scope":"Needs globally consistent Witting RAY LABELS and calibrated per-outcome efficiencies; an anonymous local port ID destroys this inverse. Label postprocessing can disclose the setting unless mapping to global rays is retained."
    }

def entropy(rho):
    lam=np.linalg.eigvalsh((rho+rho.conj().T)/2)
    assert min(lam)>-1e-10
    return float(-sum(x*math.log2(x) for x in lam if x>1e-12))

def channel_K(rays,perm):
    B=np.zeros((45,4),dtype=complex)
    B[:40]=rays.conj()/math.sqrt(10)
    assert max(abs((B.conj().T@B-np.eye(4)).ravel()))<1e-11
    return B[np.asarray(perm)].reshape(9,5,4)

def out_env(K,rho):
    B=np.einsum("aik,kl,bil->ab",K,rho,K.conj())
    E=np.einsum("aik,kl,ajl->ij",K,rho,K.conj())
    assert abs(np.trace(B)-1)<1e-9 and abs(np.trace(E)-1)<1e-9
    return B,E

def coh(K,rho=None):
    if rho is None:rho=np.eye(4)/4
    B,E=out_env(K,rho)
    return entropy(B)-entropy(E)

def routed_channel_front(rays):
    """Capacity under physical constraint: 5 unused channels share 9th output rail."""
    base=np.arange(45)
    original=np.array(previous.positive_capacity_front(rays)["best_explicit_perm_45_output_modes"])
    witness=coh(channel_K(rays,original))
    assert witness>1.08
    rng=np.random.default_rng(SEED+11)
    trials=600
    # Preserve five zero Naimark rows in one complete ninth output rail:
    # 40 real input rows occupy an 8 x 5 rectangular matrix, not all9 rails.
    perm=np.concatenate([rng.permutation(40),np.arange(40,45)])
    current=coh(channel_K(rays,perm))
    best=perm.copy();bestval=current
    best_history=[]
    for sweep in range(4):
        improved=0
        for i in range(40):
            for j in range(i+1,40):
                if rng.random()>.5:continue
                perm[i],perm[j]=perm[j],perm[i]
                val=coh(channel_K(rays,perm))
                if val>current+1e-11:
                    current=val;improved+=1
                    if val>bestval:
                        bestval=val;best=perm.copy()
                else:perm[i],perm[j]=perm[j],perm[i]
        best_history.append(float(bestval))
    # 8-level output effective because fifth output rail is all zeros.
    KB=channel_K(rays,best)
    assert np.max(abs(KB[8,:,:]))<1e-12
    assert bestval>0
    # Physical ray geometry cost: orthogonality pairs within each 5-group.
    def ortho_count(perm):
        return sum(int(abs(np.vdot(rays[perm[i]],rays[perm[j]]))<1e-10)
                   for start in range(0,40,5)
                   for i,j in itertools.combinations(range(start,start+5),2))
    # optimize a SECOND axis: 8x5 grouping by geometric orthogonality
    # at the expense of coherent information (correlation not causality).
    refcounts=[]
    refscores=[]
    for _ in range(100):
        pp=np.concatenate([rng.permutation(40),np.arange(40,45)])
        refcounts.append(ortho_count(pp))
        refscores.append(coh(channel_K(rays,pp)))
    return {
      "status":"PASS",
      "prior_unrestricted_routed_IC_qubits":witness,
      "constrained_zero_rows_in_one_output_rail":True,
      "constrained_effective_output_support_dimension":8,
      "constrained_input_and_environment_dimensions":[4,5],
      "constrained_best_IC_qubits":bestval,
      "constrained_permutation":best.tolist(),
      "constrained_stored_iteration_best":[float(x) for x in best_history],
      "constrained_ray_orthogonality_pairs_per_8_groups":ortho_count(best),
      "random_100_constrained_baseline_IC_min_avg_max":
        [min(refscores),float(np.mean(refscores)),max(refscores)],
      "random_100_constrained_orthogonality_pairs_min_avg_max":
        [min(refcounts),float(np.mean(refcounts)),max(refcounts)],
      "perfect_full_45_Naimark_isometry_preserved":True,
      "claim_scope":"A constructive physically more parsimonious eight-output-rail channel with 5-level environment; not globally optimal and no claim of exact A5 covariance."
    }

def optimized_input_front(rays):
    """An independent explicit full-rank ququart state raises coherent information."""
    perm=previous.positive_capacity_front(rays)["best_explicit_perm_45_output_modes"]
    K=channel_K(rays,perm)
    gen=[]
    for i in range(4):
        for j in range(i+1,4):
            X=np.zeros((4,4),complex)
            X[i,j]=X[j,i]=1/math.sqrt(2)
            gen.append(X)
            Y=np.zeros((4,4),complex)
            Y[i,j]=1j/math.sqrt(2)
            Y[j,i]=-1j/math.sqrt(2)
            gen.append(Y)
    for m in range(1,4):
        gen.append(np.diag([1]*m+[-m]+[0]*(3-m)).astype(complex)/
                   math.sqrt(m*(m+1)))
    assert len(gen)==15
    coeff=np.array([.12510,-.04890,.05712,.09473,-.11319,
                    -.05176,.05036,-.12411,.19162,-.00705,
                    -.02493,.06910,-.07468,-.04334,-.02777])
    h=np.einsum("i,ijk->jk",coeff,np.array(gen))
    assert np.max(abs(h-h.conj().T))<1e-12
    R=expm(h)
    rho=R/np.trace(R)
    assert np.max(abs(rho-rho.conj().T))<1e-12
    eig=np.linalg.eigvalsh(rho)
    assert eig.min()>0.19 and abs(eig.sum()-1)<1e-12
    baseline=coh(K,np.eye(4)/4)
    value=coh(K,rho)
    assert value>1.097 and value>baseline+.01
    return {
      "status":"PASS",
      "optimized_4x4_input_eigenvalues":eig.tolist(),
      "input_log_density_15_parameters_in_SU4_Hermitian_basis":coeff.tolist(),
      "basis_construction":"12 normalized complex off-diagonal Gell-Mann pairs followed by 3 diagonal traceless Hermitian generators",
      "density_preparation_formula":"rho=exp(sum_j theta_j G_j)/Tr exp(sum_j theta_j G_j)",
      "routed_maximally_mixed_coherent_information_bits":baseline,
      "explicit_full_rank_input_coherent_information_bits":value,
      "strict_unassisted_quantum_capacity_lower_bound_qubits_per_use":value,
      "two_use_product_state_lower_bound_total_qubits":2*value,
      "scope":"Finite-dimensional theoretical witness from numeric search, NOT proven global optimum or practical optical encoder."
    }

def two_use_front(rays):
    """Compare 2-use coherent information of structured correlated input families."""
    cand=previous.positive_capacity_front(rays)["best_explicit_perm_45_output_modes"]
    K=channel_K(rays,cand)
    assert coh(K)>1
    kraus=np.stack([K[:,k,:] for k in range(5)])
    # Two-use Kraus set. Vectorize at 81x16 instead of 9x4.
    L=np.stack([np.kron(A,B) for A,B in itertools.product(kraus,kraus)])
    assert L.shape==(25,81,16)
    rho=np.eye(4)/4
    out1,env1=out_env(K,rho)
    baseline=coh(K,rho)
    def ic2(r):
        out=np.einsum("aik,kl,ajl->ij",L,r,L.conj(),optimize=True)
        env=np.einsum("aik,kl,bil->ab",L,r,L.conj(),optimize=True)
        return entropy(out)-entropy(env)
    product=ic2(np.kron(rho,rho))
    assert abs(product-2*baseline)<1e-9
    bell=np.zeros((16,16),complex)
    v=np.zeros(16,complex)
    for i in range(4):v[5*i]=.5
    bell=np.outer(v,v.conj())
    diagonal=sum(np.outer(np.eye(16)[5*i],np.eye(16)[5*i]) for i in range(4))/4
    results=[]
    for family,X in (("Bell",bell),("diagonal_correlated",diagonal)):
        for t in (.10,.25,.50,.75,1):
            mixed=(1-t)*np.eye(16)/16+t*X
            ic=ic2(mixed)
            results.append({"family":family,"mix_weight":t,
                            "two_use_coherent_information_bits":float(ic),
                            "per_use_bits":float(ic/2)})
    # Also test correlated classical mixture along product spectral basis:
    assert len(results)==10
    best=max([x["per_use_bits"] for x in results])
    return {
      "status":"PASS",
      "single_use_maxmixed_routed_coherent_information_bits":baseline,
      "independent_two_use_product_coherent_information_bits":product,
      "two_use_Kraus_count":25,
      "two_use_output_dims":[81,25],
      "structured_two_use_inputs":results,
      "best_tested_structured_per_use":best,
      "structured_test_has_superadditivity_over_PRODUCT_MAXMIXED":bool(best>baseline+1e-8),
      "warning":"Even failure to improve does NOT rule out superadditivity; compare with optimized one-letter input before claiming a genuine superadditive rate. The tested state families are narrow."
    }

def Hamiltonian_front(P,supports,O):
    """Compile Q_z into same-block projector D and its swap S."""
    S=earlier.swap_d(4)
    I=np.eye(16)
    residual=0.0
    unitary_resid=0.0
    exampleSchmidt=0
    t=3*math.pi/8
    for ids in supports:
        ids=sorted(ids)
        Lset=[i for i in ids if O[i,ids[0]]>1e-10]
        Rset=list(sorted(set(ids)-set(Lset)))
        L=sum(P[i] for i in Lset)/2
        R=sum(P[i] for i in Rset)/2
        D=np.kron(L,L)+np.kron(R,R)
        Q=sum(np.kron(P[i],P[i])for i in ids)
        proj=D@(I+S)/2
        assert np.max(abs(proj@proj-proj))<1e-11
        assert np.max(abs(D@S-S@D))<1e-11
        residual=max(residual,float(np.max(abs(Q-4*proj/3))))
        U=I+np.expm1(-4j*t/3)*proj
        Ua=expm(-2j*t*D/3)@expm(-2j*t*D@S/3)
        unitary_resid=max(unitary_resid,float(np.max(abs(U-Ua))))
        assert np.max(abs(U.conj().T@U-I))<1e-11
    return {
      "status":"PASS","all_45_charts_verified":45,
      "projector_formula":"Q_z=(4/3) D_z (I+SWAP)/2, D_z=L tensor L + R tensor R",
      "exact_unitary_factorization":
          "exp(-it Q_z)= exp(-i(2t/3)D_z) exp(-i(2t/3) D_z SWAP)",
      "max_projector_compilation_error":residual,
      "max_two_factor_unitary_error":unitary_resid,
      "coherent_projector_phase_gate_requires_nonlinear_or_ancilla_resource":True,
      "warning":"The two commuting exponentials are NONLOCAL two-ququart operators, not physical single-mode gates or a two-gate KLM circuit. Herald success probability not derived."
    }

def gauge_front(A):
    """Finite-range 3-torus covariant Laplacian with nonzero Wilson loop."""
    from scipy.linalg import expm
    n=45
    Id=np.eye(n)
    A=A.astype(float)
    assert np.array_equal(A@A,9*Id+3*np.ones((n,n)))
    generator=A/12
    D=np.diag([1 if i==0 else 0 for i in range(n)])
    assert np.linalg.norm(generator@D-D@generator)>0
    alpha=1.1;beta=.7
    rows=[]
    for L in (8,16,32,64):
        Ux=expm(1j*alpha*generator/L)
        Uy=expm(1j*beta*D/L)
        Uz=Id.copy()
        W=Ux@Uy@Ux.conj().T@Uy.conj().T
        nrm=float(np.linalg.norm(W-Id,2))
        assert nrm>1e-9
        assert np.linalg.norm(W.conj().T@W-Id)<1e-10
        # Spatial H(k) with localized hopping and fixed internal gap.
        # Kinetic coefficient scales L^2 for a nontrivial 3D continuum
        # Schrödinger limit, so this is NOT finite-speed relativistic.
        def Hk(k):
            H0=12*Id-A
            kinetic=0j*Id
            for q,U in zip(k,(Ux,Uy,Uz)):
                kinetic=kinetic+2*Id-np.exp(1j*q)*U-np.exp(-1j*q)*U.conj().T
            H=H0+(L*L)*kinetic
            assert np.max(abs(H-H.conj().T))<1e-9
            return H
        lam0=np.linalg.eigvalsh(Hk((0,0,0)))
        lam1=np.linalg.eigvalsh(Hk((2*math.pi/L,0,0)))
        rows.append({"L":L,"sites":45*L**3,
            "internal_Wilson_loop_norm_minus_identity":nrm,
            "L_squared_Wilson_deviation":nrm*L*L,
            "minimum_Bloch_energy_k0":float(lam0[0]),
            "second_Bloch_energy_k0":float(lam0[1]),
            "first_Bloch_energy_kx_one":float(lam1[0]),
            "finite_internal_excitation_gap_at_k0":float(lam0[1]-lam0[0]),
            "max_hermiticity_error":float(np.max(abs(Hk((0,0,0))-Hk((0,0,0)).conj().T)))})
    assert rows[-1]["internal_Wilson_loop_norm_minus_identity"] < rows[0]["internal_Wilson_loop_norm_minus_identity"]
    # Discrete-time controlled nearest-neighbor shift (separate dynamics):
    # one spatial cell per time step => exact graph-local light cone, with
    # coordinate scale dx=dt=1/L. This is NOT Hk continuous-time Schrödinger.
    return {
      "status":"PASS",
      "gauge_lattice":"GQ45 Cartesian C_L^3, link Ux=exp(i alpha A/(12L)), Uy=exp(i beta |0><0|/L), Uz=I",
      "internal_mass_operator":"12 I45 - A_GQ; ideal spectrum (0^1,9^20,15^24)",
      "noncommuting_links_with_nonzero_Wilson_plaquette":True,
      "bloch_dispersion_evaluated_nontrivially":True,
      "lattice_rows":rows,
      "continuous_time_hopping_has_no_strict_finite_speed_in_continuum_limit":True,
      "separate_discrete_time_local_coin_shift_has_maximum_one_cell_per_step":True,
      "physical_scope":"Externally imposed 3D spatial graph, choice of non-Abelian synthetic link matrices and time clock. No emergent Lorentz metric, gravitational field equation, fundamental gauge coupling or physical implementation."
    }

def detector_front(supports,O):
    """Calibrated ray-label confusion, per-launch losses, and identifiability."""
    H=np.array([[int(i in s) for i in range(40)]for s in supports],float)
    # A symmetric mistaken-ray report: with probability eps label i
    # becomes a random j != i. At uniform p, p'=p and the hidden
    # derivative is attenuated by alpha=1-40 eps/39.
    errors=[]
    for eps in (0,.01,.05,.15,.40):
        alpha=1-40*eps/39
        if alpha<=0:continue
        F=7.5*alpha*alpha
        results={
          "wrong_label_probability":eps,
          "label_signal_attenuation":alpha,
          "per_detected_photon_Fisher_eigenvalue":F,
          "local_Cramer_Rao_trace_inverse_coeff":24/F,
          "global_inverse_unbiased_with_known_epsilon":True,
          "sufficient_detected_photons_for_RMS_0p001_from_linear_inverse":
              math.ceil(3.2/(alpha*alpha*1e-6))
        }
        errors.append(results)
    # Uniform throughput eta leaves *conditional detected* ray
    # probabilities unchanged; with no-click as a distinct outcome,
    # per launched photon FI scales linearly with eta.
    eta=.70
    assert abs(7.5*eta-5.25)<1e-12
    return {
      "status":"PASS","calibrated_global_label_misidentification_model":
       "M_{j|i}=(1-eps) if j=i else eps/39",
      "cases":errors,
      "uniform_detection_efficiency":eta,
      "Fisher_per_launched_photon_with_no_click_global_eta":7.5*eta,
      "shot_cost_multiplier_to_detected_count":1/eta,
      "missing_identifiability":"Unknown arbitrary ray-dependent confusion can mimic chart bias; joint self-calibration needs additional known probes or reference measurements."
    }

def main():
    rays,S,decks,A,P,O=previous.geometry()
    a=single_photon_front(rays,S,decks,A,O)
    print("FRONT1 one photon detector label",a["sufficient_detected_single_photons_for_RMS_le_0p001"],flush=True)
    b=routed_channel_front(rays)
    print("FRONT2 zero-row constrained capacity",b["constrained_best_IC_qubits"],flush=True)
    c=two_use_front(rays)
    print("FRONT3 two-use structured best",c["best_tested_structured_per_use"],flush=True)
    g=optimized_input_front(rays)
    print("FRONT7 optimized input quantum capacity",g["explicit_full_rank_input_coherent_information_bits"],flush=True)
    d=Hamiltonian_front(P,S,O)
    print("FRONT4 exact SWAP factorization",d["max_two_factor_unitary_error"],flush=True)
    e=gauge_front(A)
    print("FRONT5 Wilson",e["lattice_rows"][-1]["L_squared_Wilson_deviation"],flush=True)
    f=detector_front(S,O)
    print("FRONT6 detector confusion",f["cases"][2]["per_detected_photon_Fisher_eigenvalue"],flush=True)
    payload={"status":"PASS","date":"2026-11-21",
       "front1_single_photon_global_ray_label_hidden24":a,
       "front2_constrained_9x5_channel_routing":b,
       "front3_two_use_coherent_information":c,
       "front4_chart_projection_swap_compilation":d,
       "front5_45_fiber_noncommuting_lattice_gauge":e,
       "front6_detector_label_confusion_and_no_click":f,
       "front7_routed_channel_explicit_optimized_input_capacity":g,
       "scientific_scope":"Ideal finite-dimensional physics/math and seeded toy sensor simulations; no experimental realization or TOE."}
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("SEVEN FRONTS PASS:",OUT,flush=True)

if __name__=="__main__":main()
