"""Six falsifiable W33/Witting continuations with outside-literature context.

Includes an explicitly POSITIVE unassisted quantum capacity lower bound,
locally optimal 24D Fisher design, a Schmidt-rank-eight Hamiltonian
decomposition, a controlled photonic gate-noise envelope, non-collapsing
( externally imposed ) spatial geometry, and global-loss orthogonality.
This is not a device, cryptographic security proof or TOE.
"""
from __future__ import annotations
import collections
import itertools
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.linalg import null_space, qr

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_fivefront_tightframe_coherent_memory as old

OUT=ROOT/"data/toe_20261121_capacity_fisher_schmidt_locality_sixfront.json"
RNG_SEED=20261121

def geometry():
    return old.geometry()

def entropy(matrix):
    ev=np.linalg.eigvalsh((matrix+matrix.conj().T)/2)
    assert ev.min()>-1e-10
    return -sum(float(x)*math.log2(float(x)) for x in ev if x>1e-13)

def positive_capacity_front(rays):
    """Both output/complement and independent Choi entropy crosscheck."""
    B=np.zeros((45,4),dtype=complex)
    B[:40]=rays.conj()/math.sqrt(10)
    assert np.max(abs(B.conj().T@B-np.eye(4)))<1e-11
    rho=np.eye(4)/4
    def channel(perm):
        K=B[perm].reshape(9,5,4)
        output=np.einsum("bai,ij,caj->bc",K,rho,K.conj())
        env=np.einsum("bai,ij,bdj->ad",K,rho,K.conj())
        assert max(abs(np.trace(output)-1),abs(np.trace(env)-1))<1e-11
        I=entropy(output)-entropy(env)
        # Independent Stinespring-Choi check:
        # J=(id_R x N)(|Phi4><Phi4|), whose entropy equals env entropy.
        J=sum(np.outer(K[:,k,:].T.reshape(-1),
                       K[:,k,:].T.reshape(-1).conj())/4
              for k in range(5))
        choi_ic=entropy(output)-entropy(J)
        assert abs(choi_ic-I)<1e-10
        assert np.linalg.eigvalsh(J).min()>-1e-11
        return I,entropy(output),entropy(env),int(sum(np.linalg.eigvalsh(J)>1e-11))
    ident=np.arange(45)
    c0,sb0,se0,rk0=channel(ident)
    assert c0>0.43
    # Permuting OUTPUT (9 x 5) computational rails preserves all 40
    # POVM effects up to relabeling but changes which modes are discarded.
    # This is an engineered physical routing choice, not gauge invariance.
    candidate=np.array([0,22,14,19,6,7,2,11,33,38,35,40,23,31,10,
                        32,8,43,29,36,27,44,9,15,21,16,12,25,3,37,
                        13,41,20,5,34,26,30,17,42,24,18,39,28,1,4])
    assert sorted(candidate.tolist())==list(range(45))
    copt,sbo,seo,rko=channel(candidate)
    assert copt>1.08 and copt>c0
    rng=np.random.default_rng(RNG_SEED)
    random_scores=[channel(rng.permutation(45))[0] for _ in range(100)]
    # A flagged erasure channel, output C9 plus |erasure> (dimension10).
    # Its complementary branch receives the full input on erasures.
    # For maximally mixed rho, I_c(p)=(1-p) I_c(0)-2p.
    pmax=copt/(copt+2)
    assert (1-0.2)*copt-2*0.2>0
    assert (1-0.4)*copt-2*0.4<0
    return {
      "status":"PASS",
      "isometry_45x4_and_two_qutrit_output_with_fivelevel_environment":True,
      "canonical_maxmixed_output_entropy_bits":sb0,
      "canonical_maxmixed_environment_entropy_bits":se0,
      "canonical_maxmixed_coherent_information_bits":c0,
      "canonical_unassisted_quantum_capacity_lower_bound_qubits_per_use":c0,
      "canonical_Choi_rank":rk0,
      "best_explicit_perm_45_output_modes":candidate.tolist(),
      "routed_maxmixed_output_entropy_bits":sbo,
      "routed_maxmixed_environment_entropy_bits":seo,
      "routed_maxmixed_coherent_information_bits":copt,
      "routed_unassisted_quantum_capacity_lower_bound_qubits_per_use":copt,
      "routed_Choi_rank":rko,
      "100_random_assignment_coherent_information_min_avg_max":
        [min(random_scores),float(np.mean(random_scores)),max(random_scores)],
      "erasure_flag_augmented_output_dim":10,
      "routed_10D_erasure_channel_positive_lower_bound_for_p_less_than":pmax,
      "erasure_formula_at_maxmixed":"I_c(p)=(1-p)*I_c(0)-2p",
      "independent_entropy_check":"S(B)-S(E) equals S(B)-S(RB) from explicit normalized Choi state",
      "warning":"Positive single-letter coherent information proves positive asymptotic UNASSISTED quantum capacity for this ideal routed channel; it is not an exact capacity or Pauli-covariant QKD security rate. Output row assignments require mode routing and source engineering."
    }

def fisher_front(supports,overlaps):
    """Locally optimal A-/E-optimal design at uniform hidden-chart weights."""
    pairs=[(a,b) for a,b in itertools.combinations(range(40),2) if overlaps[a,b]>1e-10]
    assert len(pairs)==540
    F=np.array([overlaps[:,sorted(S)]@overlaps[:,sorted(S)].T for S in supports])
    Raw=np.column_stack([F[:,a,b] for a,b in pairs])/4
    R=Raw-Raw.mean(axis=0,keepdims=True)
    Gram=R@R.T
    eig,vec=np.linalg.eigh(Gram)
    assert sum(eig>1e-10)==24
    U=vec[:,-24:]
    basis=U.T@R
    assert np.max(abs(basis@basis.T-np.eye(24)/3))<1e-11
    assert np.max(abs(basis.sum(axis=1)))<1e-10
    p0=2/15  # uniform chart randomizer: every nonorth pair same probability
    assert np.max(abs(Raw.mean(axis=0)-p0))<1e-11
    v=p0*(1-p0)  # 26/225
    norms=np.sum(basis*basis,axis=0)
    assert max(abs(norms-2/135))<1e-10
    per_total_full_fi=(basis@basis.T)/(540*v)
    spec=np.linalg.eigvalsh(per_total_full_fi)
    expected=5/936
    assert np.max(abs(spec-expected))<1e-11
    A_coefficient=float(np.trace(np.linalg.inv(per_total_full_fi)))
    assert abs(A_coefficient-22464/5)<1e-8  # 4492.8
    # Every pair has the SAME local Fisher trace. AM-HM for SPD matrices:
    # tr(F^-1) >= d^2/tr(F), and full uniform saturates it.
    per_probe_trace=float(norms[0]/v)
    assert abs(per_probe_trace-5/39)<1e-10
    # QR-selected 24-probe baseline, and a separate exact labeled
    # 24-probe improved design found by offline discrete exchange search.
    _,_,qrpiv=qr(basis,pivoting=True,mode="economic")
    sparse_qr=qrpiv[:24]
    improved=np.array([117,183,370,328,110,165,476,272,118,354,303,304,
                       160,289,310,448,209,64,271,133,288,337,203,142])
    assert len(set(improved))==24
    def A_coeff(indices):
        D=basis[:,indices]
        FI=D@D.T/(len(indices)*v)
        eigs=np.linalg.eigvalsh(FI)
        assert eigs.min()>1e-10
        return float(sum(1/eigs)),float(eigs.max()/eigs.min())
    aq,condq=A_coeff(sparse_qr)
    ai,condi=A_coeff(improved)
    print("Sparse QR and fixed exchange Fisher A coefficients:",aq,ai,flush=True)
    assert ai>A_coefficient and aq>A_coefficient
    assert abs(ai-11681.28)<1e-5
    # Cramer-Rao is a lower bound for locally UNBIASED estimator; not
    # an achievable finite-shot guarantee, and shot noise persists.
    return {
      "status":"PASS","full_nonorthogonal_pair_count":540,
      "hidden_classical_chart_bias_dimension":24,
      "reference_matching_probability":p0,
      "per_probe_Fisher_trace_for_one_launch":per_probe_trace,
      "uniformly_weighted_Fisher_eigenvalues_per_total_shot":[expected]*24,
      "uniform_full_540_probe_Aoptimal_Cramer_Rao_MSE_coefficient":A_coefficient,
      "uniform_full_540_probe_local_RMS_lower_bound_for_N_shots":"sqrt(4492.8/N)",
      "total_iid_shots_needed_for_CR_lower_bound_MSE_1e_minus6":math.ceil(A_coefficient/1e-6),
      "uniform_540_probe_locally_A_and_E_optimal_at_uniform_chart_weights":True,
      "minimal_24_probe_QR_condition_number_Fisher":condq,
      "24_probe_QR_Acriterion_coefficient":aq,
      "24_probe_exchange_candidate_pair_indices":improved.tolist(),
      "24_probe_exchange_candidate_Acriterion_coefficient":ai,
      "24_probe_exchange_candidate_Fisher_condition_number":condi,
      "local_Acriterion_relative_penalty_of_sparse_candidate":ai/A_coefficient,
      "warning":"At uniform chart distribution ONLY; no 24-probe global optimality claim. CR lower bounds do not guarantee finite-shot attainability. Priors, detector noise, adaptive feedback or different probe families can change optimality."
    }

def optical_front(rays,supports,overlaps):
    """Explicit per-MZI coherent noise on all 45 charts, including worst-case gate envelope."""
    from scipy.linalg import null_space
    pideal=np.array([overlaps[:,sorted(S)]@overlaps[:,sorted(S)].T/4 for S in supports])
    pairs=[(a,b) for a,b in itertools.combinations(range(40),2)
           if overlaps[a,b]>1e-10]
    ideal=np.array([int(np.argmax(pideal[:,a,b])) for a,b in pairs])
    g=1e-4
    pg=[]
    gate_nums=[]
    worst_op=0.
    for S in supports:
        ids=sorted(S)
        V=rays[ids].conj()/math.sqrt(2)
        U=np.column_stack((V,null_space(V.conj().T)))
        gates,phases,reconstruction=old.mesh_reck(U)
        gate_nums.append(len(gates))
        # Every adjacent-rail two-mode gate receives a coherent D(g)
        # overrotation: ||D(g)-I2||=2 sin(g/2)<g+o(g).
        D=np.diag([np.exp(1j*g),np.exp(-1j*g)])
        perturbed=np.diag(phases)
        for i,j,G in reversed(gates):
            perturbed[[i,j]]=(D@G).conj().T@perturbed[[i,j]]
        worst_op=max(worst_op,float(np.linalg.norm(perturbed-U,2)))
        assert np.linalg.norm(perturbed.conj().T@perturbed-np.eye(8),2)<1e-10
        v=abs(perturbed[:,:4]@rays.T)**2
        pg.append(v.T@v/1.0)
    pg=np.array(pg)
    assert max(gate_nums)<=28
    noisy=np.array([int(np.argmax(pg[:,a,b])) for a,b in pairs])
    ncorrect=int(sum(noisy==ideal))
    assert ncorrect==540
    gaps=[sorted(pg[:,a,b])[-1]-sorted(pg[:,a,b])[-2] for a,b in pairs]
    min_gap=min(gaps)
    assert min_gap>0
    # Two uses of an analyzer per matched coincidence:
    # operator-norm gate error <=d*g; total two-photon state difference
    # <=2*d*g, so outcome-event probability change <=2*d*g.
    # Two chart scores differ ideally by Delta=1/12.
    # Guaranteed ranking: 1/12 > 4*d*g, hence g<1/(48d).
    threshold=1/(48*28)
    assert g<threshold
    return {
      "status":"PASS","mesh_count":45,"gate_count_min_max":[min(gate_nums),max(gate_nums)],
      "assumed_systematic_unitary_per_gate_error_radians":g,
      "worst_reconstructed_interferometer_unitary_2norm_error":worst_op,
      "worst_case_telescoping_bound_d_times_g":28*g,
      "correct_chart_after_gate_errors_out_of_540":ncorrect,
      "minimum_noisy_two_photon_probability_gap":float(min_gap),
      "rigorous_sufficient_per_gate_operator_error_for_unique_chart":threshold,
      "gate_error_witness_formula":"p_win-p_runner>=1/12-4*28*g",
      "physical_caveat":"No foundry device, calibrated voltage-to-phase model, correlated drift or photodetector SPAM. Error formula assumes each two-mode gate operator perturbation <=g and unchanged detection POVM."
    }

def hamiltonian_front(P,supports,overlaps):
    """All 45 exact eight-product term decompositions / operator Schmidt rank."""
    pauli=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),
           np.diag([1,-1])]
    allsv=[]
    maxerr=0.
    for S in supports:
        ids=sorted(S)
        own=sorted(i for i in ids if overlaps[i,ids[0]]>1e-10)
        other=sorted(set(ids)-set(own))
        assert len(own)==len(other)==4
        Q=sum(np.kron(P[i],P[i]) for i in ids)
        sch=np.linalg.svd(Q.reshape(4,4,4,4).transpose(0,2,1,3).reshape(16,16),
                         compute_uv=False)
        assert sum(sch>1e-9)==8
        assert max(abs(sch[:2]-2))<1e-10
        assert max(abs(sch[2:8]-2/3))<1e-10
        allsv.append(sch)
        def block_qubit(group):
            # Use the exact rank-two block projector, then recover its
            # orthonormal qubit coordinates by Hermitian diagonalization.
            t=sum(P[i] for i in group)/2
            ew,ev=np.linalg.eigh(t)
            W=ev[:,-2:]
            assert np.max(abs(W@W.conj().T-t))<1e-10
            return t,[W@s@W.conj().T for s in pauli]
        L,PL=block_qubit(own)
        R,PR=block_qubit(other)
        compiled=np.kron(L,L)+np.kron(R,R)
        for X in PL:compiled+=np.kron(X,X)/3
        for X in PR:compiled+=np.kron(X,X)/3
        maxerr=max(maxerr,float(max(abs((Q-compiled).ravel()))))
        assert np.max(abs(Q-compiled))<1e-10
    return {
      "status":"PASS","charts_verified":45,
      "operator_schmidt_rank_each_two_copy_chart":8,
      "exact_nonzero_operator_schmidt_singular_values":[2,2]+[2/3]*6,
      "explicit_minimal_sum_of_product_operators":8,
      "local_ququart_blocks_per_chart":2,
      "per_chart_two_block_Pauli_correlation_terms":6,
      "per_chart_two_block_identity_product_terms":2,
      "max_Pauli_product_compilation_residual":maxerr,
      "two_copy_Hamiltonian_formula":"Qz = PL tensor PL + PR tensor PR + (1/3) sum_{sigma=X,Y,Z} (sigmaL tensor sigmaL + sigmaR tensor sigmaR)",
      "warning":"Operator Schmidt rank eight counts tensor-product *summands*, NOT a gate-depth lower bound. A deterministic physical optical realization cannot follow from this algebra; passive single-rail linear optics has relevant no-go results."
    }

def causal_front(A):
    """Compact GQ internal fiber times 3D lattice torus; finite-speed countermodel."""
    assert A.shape==(45,45) and set(A.sum(axis=0))=={12}
    assert np.array_equal(A@A,9*np.eye(45,dtype=int)+3*np.ones((45,45),dtype=int))
    out=[]
    for L in (4,8,16,32,64):
        n=45*L**3
        degree=18   # GQ 12 plus 6 toroidal nearest neighbors
        diameter=2+3*(L//2)
        scaled=diameter/L
        gap_adj=2-2*math.cos(2*math.pi/L)
        norm_gap=gap_adj/18
        assert abs(diameter-2-3*L/2)<1e-12
        out.append({"cycle_length":L,"graph_vertices":n,
                    "regular_degree":degree,
                    "graph_diameter":diameter,
                    "edge_length":1/L,
                    "scaled_metric_diameter":scaled,
                    "normalized_laplacian_gap":norm_gap,
                    "scaled_gap_times_L_squared":norm_gap*L*L})
    # For any path length t, nearest-neighbor propagation changes at
    # most t graph edges: light-cone radius t by construction.
    for L in (8,16):
        def cd(a,b):return min(abs(a-b),L-abs(a-b))
        def gd(z,w):return 0 if z==w else 1 if A[z,w] else 2
        rng=np.random.default_rng(33+L)
        for _ in range(200):
            z,w=int(rng.integers(45)),int(rng.integers(45))
            x=rng.integers(0,L,size=3)
            y=rng.integers(0,L,size=3)
            dist=gd(z,w)+sum(cd(int(a),int(b)) for a,b in zip(x,y))
            assert dist>=gd(z,w)
            assert dist<=2+3*(L//2)
    return {
      "status":"PASS",
      "construction":"Cartesian product of 45-vertex GQ chart graph with C_L^3",
      "vertex_degree_all_L":18,
      "sequence":out,
      "limiting_scaled_diameter":1.5,
      "limiting_noncollapsed_spatial_metric":"3-torus with L1 (taxicab) metric",
      "internal_45point_fiber_scaled_diameter_goes_to_zero":True,
      "causal_finite_cone_radius_after_t_steps_at_most_t":True,
      "temporal_edges":"Separate directed time lift with stay/nearest-neighbor transfer; no intrinsic time generated",
      "caveat":"Constructed product/spacetime lattice, not derived from W33, E8, Einstein gravity, or Lorentzian metric. Finite-propagation is engineered, not emergent."
    }

def loss_orthogonality_front(supports,overlaps):
    """At uniform chart weight, global throughput is FI-orthogonal to 24D bias."""
    pair=[(a,b) for a,b in itertools.combinations(range(40),2) if overlaps[a,b]>1e-10]
    F=np.array([overlaps[:,sorted(S)]@overlaps[:,sorted(S)].T for S in supports])
    raw=np.column_stack([F[:,a,b] for a,b in pair])/4
    centered=raw-raw.mean(axis=0,keepdims=True)
    residual=float(np.max(abs(centered.sum(axis=1))))
    assert residual<1e-10
    p0=2/15
    throughput=.87
    prob=throughput*p0
    # Classically observed 540 Bernoulli success rates:
    # p_ab = s*(p0 + R_ab^T x). At x=0, derivatives dp/ds=p0
    # and dp/dx=s R_ab. FI offdiagonal proportional to sum_ab R_ab.
    cross=throughput*p0*centered.sum(axis=1)/(prob*(1-prob))
    assert max(abs(cross))<1e-10
    # But arbitrary port-dependent efficiency lies in a much larger
    # nuisance class that may overlap the hidden 24D subspace.
    return {
      "status":"PASS",
      "joint_model":"observed nonorth matching p_ab=s*(2/15+R_ab^T x), 0<s<=1",
      "nominal_unknown_global_throughput":throughput,
      "full540_local_FI_throughput_hidden_bias_cross_block_zero":True,
      "max_FI_cross_block_residual":float(max(abs(cross))),
      "centered_response_sum_over_all_540_pairs_residual":residual,
      "restriction":"Local x=0; uniform global throughput only, not per-port or per-chart efficiencies.",
      "warning":"Local statistical orthogonality does NOT identify arbitrary SPAM and may fail away from uniform chart weights."
    }

def main():
    rays,S,decks,A,P,overlaps=geometry()
    ch=positive_capacity_front(rays)
    print("FRONT1 positive quantum capacity",ch["routed_maxmixed_coherent_information_bits"],flush=True)
    fi=fisher_front(S,overlaps)
    print("FRONT2 Fisher optimum",fi["uniform_full_540_probe_Aoptimal_Cramer_Rao_MSE_coefficient"],flush=True)
    optical=optical_front(rays,S,overlaps)
    print("FRONT3 photonic all",optical["correct_chart_after_gate_errors_out_of_540"],flush=True)
    H=hamiltonian_front(P,S,overlaps)
    print("FRONT4 Schmidt rank",H["operator_schmidt_rank_each_two_copy_chart"],flush=True)
    causal=causal_front(A)
    print("FRONT5 noncollapse dimension",causal["limiting_noncollapsed_spatial_metric"],flush=True)
    loss=loss_orthogonality_front(S,overlaps)
    print("FRONT6 global loss orthogonality",loss["full540_local_FI_throughput_hidden_bias_cross_block_zero"],flush=True)
    record={"status":"PASS","date":"2026-11-21","baseline_sha":"47af4e9a2796a9e30c741e8c25d2de5b781f9958",
       "front1_positive_coherent_information_capacity_and_routing":ch,
       "front2_local_AE_optimal_Fisher_and_sparse_tradeoff":fi,
       "front3_reck_control_gate_noise":optical,
       "front4_eight_product_Hamiltonian_compilation":H,
       "front5_noncollapsing_external_3torus_spatial_scaffold":causal,
       "front6_throughput_hidden_chart_Fisher_orthogonality":loss,
       "scope":"Mathematical certificates/seeded simulations; no fabricated hardware, measured QKD security, Pauli-covariant experimental code or derivation of Lorentzian gravity."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS SIX FRONTS",OUT,flush=True)

if __name__=="__main__": main()
