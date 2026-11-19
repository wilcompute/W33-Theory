"""Five-track TOE constraints: UV SIC, chiral sphere gap, causal break, graph calculus.

Mathematical checks and toy diagnostics, NOT a consistent M-theory compactification,
Einstein gravity, or experimentally reconstructed process tensor.
"""
from itertools import product,combinations
from math import comb,log,sqrt,pi
from pathlib import Path
import json
import numpy as np
from toe_20261119_w33_40_qutrit_css import checks

ROOT=Path(__file__).resolve().parents[1]

def sic_uv_naturalness():
    omega=np.exp(2j*pi/3)
    v=np.array([0,1,-1],dtype=complex)
    Q=np.column_stack([np.roll(v*np.array([1,omega**b,omega**(2*b)]),a)
                       for a in range(3) for b in range(3)])
    # Nine equal-norm triplets, three copies of each orthonormal basis vector.
    # This is a non-SIC tight frame with identical S=QQ^dagger.
    Qbad=np.column_stack([sqrt(2)*np.eye(3)[:,a]
                          for a in range(3) for b in range(3)])
    assert np.allclose(Q@Q.conj().T,6*np.eye(3))
    assert np.allclose(Qbad@Qbad.conj().T,6*np.eye(3))
    def overlaps(X):
        return [float(abs(np.vdot(X[:,i],X[:,j]))**2)
                for i,j in combinations(range(9),2)]
    pair_sic=overlaps(Q)
    pair_bad=overlaps(Qbad)
    assert np.allclose(pair_sic,[1]*36)
    assert np.allclose(sorted(pair_bad),[0]*27+[4]*9)
    assert abs(sum(pair_sic)-sum(pair_bad))<1e-12
    variance_sic=sum((4*x-4)**2 for x in pair_sic)
    variance_bad=sum((4*x-4)**2 for x in pair_bad)
    assert abs(variance_sic)<1e-10 and abs(variance_bad-1728)<1e-9
    beta=[{"dimension_N":N,"SIC_fundamental_fields_N_squared":N*N,
           "minimum_antifundamentals_if_vectorlike":N*N,
           "minimum_one_loop_SQCD_flavors":N*N,
           "maximum_one_loop_b0_3N_minus_N2":3*N-N*N}
          for N in range(2,7)]
    assert beta[1]["maximum_one_loop_b0_3N_minus_N2"]==0
    assert all(d["maximum_one_loop_b0_3N_minus_N2"]<0 for d in beta[2:])
    return {"gauged_group":"SU(N) rigid N=1, N^2 SIC states represented by independent fundamental chiral fields paired vectorlike",
            "flavor_beta_table":beta,
            "SU3_nine_flavor_one_loop_b0":0,
            "SU3_ten_flavor_one_loop_b0":-1,
            "frame_operator_both":"6*I_3",
            "individual_vector_norm_squared_both":2,
            "all_36_pair_overlap_sq_sum_SIC":sum(pair_sic),
            "all_36_pair_overlap_sq_sum_nonSIC":sum(pair_bad),
            "SIC_equiangular_variance":variance_sic,
            "nonSIC_repeated_basis_equiangular_variance":variance_bad,
            "no_go_scope":"For vectorlike fundamental-only elementary N^2 SIC, b0<=0 when N>=3; tight-frame / one moment-map constraints cannot isolate the SIC. Does not preclude different gauge representations, composites, parent gauge group, Yukawa effects, or asymptotic safety."}

def chiral_flux_gap():
    A=np.array([[0,-1],[1,-1]],dtype=np.int64)
    assert np.array_equal(np.linalg.matrix_power(A,3),np.eye(2,dtype=np.int64))
    fixed=[(a,b) for a,b in product(range(3),repeat=2)
           if np.all((A-np.eye(2,dtype=np.int64))@np.array([a,b])%3==0)]
    assert fixed==[(0,0),(1,2),(2,1)]
    R=1.0
    low_modes=[{"magnetic_torus_D2_eigenvalue":mu2,
                "total_D7_eigenvalue_lower_bound":sqrt((5/(2*R))**2+mu2)}
               for mu2 in (0.0,0.5,5.0,20.0)]
    assert all(t["total_D7_eigenvalue_lower_bound"]>=2.5 for t in low_modes)
    return {"internal_cover":"round S5(R) x T2, descended by free H27 isometries",
            "sphere_Dirac_spectrum":"+/-(l+5/2)/R, l=0,1,2,...",
            "product_operator_square":"D7^2 = D_S5^2 tensor I + I tensor D_T2,A^2 for any torus-pulled-back unitary connection",
            "torus_only_mag_flux_zero_mode_impossible":True,
            "absolute_D7_eigenvalue_lower_bound":"5/(2R) independent of the torus-only magnetic flux amplitude",
            "sample_R_equals_1_mass_gaps":low_modes,
            "scalar_curvature_of_product":"20/R^2",
            "curvature_endomorphism_necessary_operator_norm_to_defeat_weaker_Lichnerowicz_bound":"at least 5/R^2 for sphere-direction/non-product gauge curvature in standard untorsioned Dirac formula",
            "orbifold_order3_fixed_points":fixed,
            "chirality_status":"NOT PROVEN. Smooth closed odd-dimensional Dirac has no ordinary chirality index; singular ADE backgrounds/localized spectrum or sphere-coupled flux and inflow are still required.",
            "limits":"Product gap relies on round sphere metric, pulled-back torus-only gauge connection, and a compatible lift to the free quotient. Other gauge/supercovariant operators and singular metrics not excluded."}

def arbitrary_instrument_memory():
    rng=np.random.default_rng(20261119)
    raw=[rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)) for _ in range(6)]
    S=sum((M.conj().T@M for M in raw),np.zeros((3,3),complex))
    evals,V=np.linalg.eigh(S)
    assert min(evals)>0
    Sinvh=V@np.diag(1/np.sqrt(evals))@V.conj().T
    kraus=[M@Sinvh for M in raw]
    assert np.allclose(sum((M.conj().T@M for M in kraus),np.zeros((3,3),complex)),np.eye(3))
    # R-S-E order: after first swap S contains |0>, E stores half of |Phi>.
    # Each generic Kraus map K on S may change its output state arbitrarily.
    # After second SWAP the restored R-S state is exactly p_b |Phi><Phi|.
    phi=np.zeros((3,3),complex)
    np.fill_diagonal(phi,1/np.sqrt(3))
    target=phi.reshape(9)
    target=np.outer(target,target.conj())
    probs=[]
    errors=[]
    for K in kraus:
        psi=np.zeros((3,3,3),complex)
        for a in range(3):
            psi[a,:,a]=K[:,0]/sqrt(3) # R, S(current), E(original)
        restored=np.swapaxes(psi,1,2)
        rs=np.einsum("rse,tue->rstu",restored,restored.conj()).reshape(9,9)
        pr=float(np.vdot(K[:,0],K[:,0]).real)
        probs.append(pr)
        errors.append(float(np.max(abs(rs-pr*target))))
    assert abs(sum(probs)-1)<1e-12 and max(errors)<1e-12
    # Event-ready loss: no click is scored a failed Bell test, not thrown out.
    p_storage=.2
    F=1-8*p_storage/9
    eta=.5
    success_probability=eta*F
    shots=6000
    success=int(rng.binomial(shots,success_probability))
    observed=success/shots
    alpha=.001
    one_sided_lower=observed-sqrt(log(1/alpha)/(2*shots))
    assert one_sided_lower>1/3
    required_eta=1/(3*F)
    assert required_eta<eta
    return {"arbitrary_Kraus_branch_count":len(kraus),
            "Kraus_trace_preserving_sum_error":float(np.max(abs(sum(M.conj().T@M for M in kraus)-np.eye(3)))),
            "branch_probabilities":probs,
            "branch_max_RS_residual":max(errors),
            "classical_entanglement_breaking_unconditional_F_upper":1/3,
            "memory_depolarization_p":p_storage,"conditional_entangled_fidelity":F,
            "event_ready_no_click_treated_as_failure":True,
            "retrieval_and_detection_efficiency_eta":eta,
            "required_minimum_efficiency_for_conservative_violation":required_eta,
            "unconditional_Bell_projection_probability":success_probability,
            "event_ready_trials":shots,"simulated_Bell_successes":success,
            "unconditional_fidelity_observed":observed,
            "Hoeffding_99p9pct_one_sided_lower":one_sided_lower,
            "limitation":"The unconditional bound assumes a trustworthy isolated reference, a valid Bell witness, no hidden coherent bypass, correct event-ready trial accounting and a classical-memory (entanglement-breaking) comparator. Full experimental process-tensor tomography and loss characterization not performed."}

def finite_graph_calculus():
    _,A,_,_=checks()
    # Commutative finite function algebra C^40 has no nonzero derivation D:C^40->C^40.
    # Every point idempotent e_i^2=e_i yields (I-2 diag(e_i)) D(e_i)=0.
    rng=np.random.default_rng(2026111900)
    f=rng.normal(size=40)
    g=rng.normal(size=40)
    F=np.diag(f)
    G=np.diag(g)
    def c(h):return A@np.diag(h)-np.diag(h)@A
    left=c(f*g)
    right=c(f)@G+F@c(g)
    err=float(np.max(abs(left-right)))
    assert err<1e-12
    E=float(np.vdot(c(f),c(f)).real/2)
    L=12*np.eye(40)-A
    E2=float(f@L@f)
    assert abs(E-E2)<1e-9
    e=np.zeros(40);e[0]=1
    pointwise_derivative_L=L@e
    Leibniz_defect=L@(e*e)-2*e*(L@e)
    assert np.linalg.norm(Leibniz_defect)>10
    ev=np.linalg.eigvalsh(L)
    assert np.allclose(np.sort(ev),np.array([0]+[10]*24+[16]*15))
    times=[.01,.05,.1,.2,.5,1]
    ds=[]
    for t in times:
        tr=1+24*np.exp(-10*t)+15*np.exp(-16*t)
        dim=2*t*(240*np.exp(-10*t)+240*np.exp(-16*t))/tr
        ds.append({"diffusion_time":t,"heat_trace":float(tr),"effective_spectral_dimension":float(dim)})
    return {"graph":"W33, 40 points, degree12",
            "pointwise_algebra_no_go":"Every linear derivation D:C^40->C^40 satisfying D(fg)=D(f)g+fD(g) is zero, by indicator idempotents.",
            "graph_Laplacian_as_derivation_counterexample_leibniz_defect_norm":float(np.linalg.norm(Leibniz_defect)),
            "matrix_bimodule_escape":"d f=[A,diag(f)], with d(fg)=d(f)diag(g)+diag(f)d(g) exactly",
            "matrix_bimodule_Leibniz_max_error":err,
            "kinetic_action_identity":"0.5*Tr(df^dag df)=f^T (12I-A) f = sum_undirected_edges (f_i-f_j)^2",
            "kinetic_action_direct":E,"kinetic_action_laplacian":E2,
            "Laplacian_eigenvalues_multiplicities":{"0":1,"10":24,"16":15},
            "nonzero_spectral_gap":10,
            "spectral_dimension_from_heat_trace":ds,
            "physics_boundary":"Exact finite graph differential calculus is algebraic, not a derivation of hypersurface-deformation constraints, causal Lorentzian evolution, a refinement limit, or Einstein equations."}

def main():
    out={"SIC_UV":sic_uv_naturalness(),
         "sphere_chirality_gap":chiral_flux_gap(),
         "event_ready_qutrit_memory":arbitrary_instrument_memory(),
         "W33_noncommutative_differential_calculus":finite_graph_calculus()}
    dst=ROOT/"data"/"toe_20261119_four_structural_frontier_tests.json"
    dst.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    for k in out:print("PASS",k)
    print("Nf=9 b0=0, nonSIC frame same S; torus flux cannot close S5 Dirac gap.")
    print("Event-ready optical qutrit memory classical-bound violation; graph commutator restores Leibniz.")
    print(json.dumps({"event_ready":out["event_ready_qutrit_memory"]["Hoeffding_99p9pct_one_sided_lower"],
                      "kinetic_error":abs(out["W33_noncommutative_differential_calculus"]["kinetic_action_direct"]-
                                          out["W33_noncommutative_differential_calculus"]["kinetic_action_laplacian"])},indent=2))
    print(dst)
    return out

if __name__=="__main__":
    main()
