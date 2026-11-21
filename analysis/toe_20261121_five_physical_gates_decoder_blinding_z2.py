"""Witting five physical gates + two falsifiers, 2026-11-21.

Reuses committed Witting construction. Tests an exact detector-identifiability
obstruction and calibration, explicit Petz recovery, generic gate-teleportation,
a dynamical Z2 lattice gauge Hamiltonian, chart-label information leakage,
and one-photon model goodness-of-fit. No fabricated photonic apparatus.
"""
from __future__ import annotations
import collections
import itertools
import json
import math
import sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_single_photon_gauge_capacity_followup as native

OUT=ROOT/"data/toe_20261121_decoder_calibration_teleport_gauge_falsifiers.json"
SEED=20261121

def setup():
    rays,S,decks,A,P,O=native.previous.geometry()
    H,P24,K=native.spectral(rays,S,decks,A,O)
    return rays,S,decks,A,P,O,H,P24,K

def identifiability(rays,H,P24):
    rng=np.random.default_rng(SEED)
    x=P24@rng.normal(size=45)
    x*=.003/np.max(abs(x))
    w=np.full(45,1/45)+x
    assert w.min()>0
    t=H.T@w/8
    eta=rng.uniform(.65,.82,40)
    second=P24@rng.normal(size=45)
    second*=.002/max(abs(second))
    xp=x+second
    wp=np.full(45,1/45)+xp
    tp=H.T@wp/8
    etap=eta*t/tp
    assert wp.min()>0 and min(etap)>0 and max(etap)<1
    differences=[]
    for a in range(40):
        # Tr(rho_a P_i) are ray overlaps; a fourth input is the mixed state.
        q=abs(rays.conj()@rays[a])**2
        p=4*eta*t*q
        pp=4*etap*tp*q
        differences.append(float(max(abs(p-pp))))
        assert abs((1-p.sum())-(1-pp.sum()))<1e-12
    differences.append(float(max(abs(eta*t-etap*tp))))
    assert max(differences)<1e-13
    assert np.linalg.norm(xp-x)>1e-4
    # Known uniform chart-mixture reference: t_ref=1/40, fixes eta_i
    # from unconditioned detection probabilities. This is a separate
    # trusted calibration experiment, not free blind tomography.
    p_ref=eta/40
    eta_exact=40*p_ref
    t_exact=eta*t/eta_exact
    x_exact=P24@(2/3*H@(t_exact-np.full(40,1/40)))
    assert max(abs(x_exact-x))<1e-12
    empirical={}
    for n in (20000,200000,2000000):
        ref=rng.multinomial(n,np.r_[p_ref,1-p_ref.sum()])
        tgt=rng.multinomial(n,np.r_[eta*t,1-np.dot(eta,t)])
        ef=40*ref[:40]/n
        tr=tgt[:40]/n/np.maximum(ef,1e-9)
        xhat=P24@(2/3*H@(tr-np.full(40,1/40)))
        empirical[str(n)]={
           "calibration_launches":n,"target_launches":n,
           "max_efficiency_estimation_error":float(np.max(abs(ef-eta))),
           "hidden_bias_l2_error":float(np.linalg.norm(xhat-x))}
    # Differential Jacobian has a 24-dimensional nullspace:
    # dp_i = eta_i (H^T dx)_i/8 + t_i d_eta_i. Choose
    # d_eta_i=-eta_i (H^T dx)_i/(8 t_i).
    delta=P24@rng.normal(size=45)
    dt=H.T@delta/8
    de=-eta*dt/t
    cancellation=eta*dt+t*de
    assert max(abs(cancellation))<1e-12
    return {
      "status":"PASS",
      "unknowns":"24D chart distribution x and 40 ray-specific detector efficiencies eta",
      "observed_for_any_known_input_state":"p_i(rho)=4 eta_i t_i Tr(rho P_i), t_i=(H^T w)_i/8",
      "exact_confounding_transform":"eta'_i=eta_i t_i/t'_i for any alternative positive chart law w'",
      "maximum_probing_state_probability_difference":max(differences),
      "two_distinct_positive_chart_laws_and_detector_models_indistinguishable":True,
      "alternate_hidden_bias_distance":float(np.linalg.norm(xp-x)),
      "local_24D_joint_Jacobian_nullspace":True,
      "jacobian_cancellation_max_error":float(max(abs(cancellation))),
      "trusted_uniform_chart_reference_exactly_breaks_gauge":True,
      "trusted_uniform_reference_eta_formula":"eta_i=40 p_reference,i with no-click retained",
      "max_exact_reference_calibration_decoder_error":float(max(abs(x_exact-x))),
      "shot_simulations_with_reference_and_no_click":empirical,
      "model_caveats":"Ray efficiency constant across chart and input, mixture resampled each trial. Reference requires known chart-mixture distribution and stable efficiencies; arbitrary chart-dependent detector drift needs more controls."
    }

def petz_decode(T):
    """T has shape output d, environment e, input k."""
    do,e,k=T.shape
    rho=np.eye(k,dtype=complex)/k
    sig=np.einsum("aei,ij,bej->ab",T,rho,T.conj())
    eig,U=np.linalg.eigh(sig)
    assert eig.min()>-1e-12 and abs(eig.sum()-1)<1e-12
    positive=eig>1e-11
    sinv=(U*np.where(positive,1/np.sqrt(np.maximum(eig,1e-300)),0))@U.conj().T
    Rs=[T[:,j,:].conj().T@sinv/math.sqrt(k) for j in range(e)]
    # Complete the recovery to a TP map on ALL output states, even in
    # subspaces that the input channel can never populate.
    null=U[:,~positive]
    for j in range(null.shape[1]):
        extra=np.zeros((k,do),complex)
        extra[0,:]=null[:,j].conj()
        Rs.append(extra)
    tp=sum(R.conj().T@R for R in Rs)
    assert np.max(abs(tp-np.eye(do)))<1e-10
    eff=[R@T[:,j,:] for R in Rs for j in range(e)]
    efftp=sum(X.conj().T@X for X in eff)
    assert np.max(abs(efftp-np.eye(k)))<1e-10
    Fe=sum(abs(np.trace(X))**2 for X in eff)/(k*k)
    Fav=(k*Fe+1)/(k+1)
    assert 0<=Fe<=1+1e-10
    return {"Fe":float(Fe),"Fav":float(Fav),
            "recovery_kraus":len(Rs),
            "output_support_rank":int(positive.sum()),
            "recovery_tp_error":float(np.max(abs(tp-np.eye(do))))}

def recovery(rays):
    perm=native.previous.positive_capacity_front(rays)[
        "best_explicit_perm_45_output_modes"]
    T=native.channel_K(rays,perm)
    full=petz_decode(T)
    assert full["Fe"]>.61
    rng=np.random.default_rng(SEED)
    best=(-1,None,None)
    ff=[]
    for i in range(300):
        V,_=np.linalg.qr(rng.normal(size=(4,2))+
                       1j*rng.normal(size=(4,2)))
        val=petz_decode(T@V)
        ff.append(val["Fe"])
        if val["Fe"]>best[0]:
            best=(val["Fe"],i,V)
    _,ind,V=best
    two=petz_decode(T@V)
    assert two["Fe"]>.903
    assert abs(full["Fe"]-.611089605158904)<1e-10
    assert abs(two["Fe"]-.9034972067200644)<1e-10
    return {
      "status":"PASS","output_dim":9,"environment_dim":5,
      "full_ququart_recovery":full,
      "seeded_300_random_two_dim_subcode_search_best_index":ind,
      "best_two_dim_subcode_recovery":two,
      "best_subcode_4x2_isometry_real":V.real.tolist(),
      "best_subcode_4x2_isometry_imag":V.imag.tolist(),
      "sampled_subcode_entanglement_fidelity_avg":float(np.mean(ff)),
      "entanglement_fidelity_definition":"Fe=maximally_entangled_overlap of Petz∘N restricted to code",
      "decoder_formula":"R_j=sqrt(tau) K_j^dagger N(tau)^(-1/2), tau=I_code/code_dim",
      "TP_completion_on_unused_output_subspace":True,
      "not_claimed":"Globally optimal decoder, fault tolerance, asymptotic code threshold, physical implementation."
    }

def heralded_gate(P,supports):
    """Generic state-injection teleportation of d=16 two-ququart gates."""
    d=16
    rng=np.random.default_rng(SEED)
    I=np.eye(d,dtype=complex)
    phi=np.eye(d,dtype=complex)/math.sqrt(d)
    maxerr=0.
    probs=[]
    for support in supports:
        Q=sum(np.kron(P[i],P[i]) for i in support)
        project=.75*Q
        assert np.max(abs(project@project-project))<1e-11
        U=I+(-1-1j)*project  # t=3*pi/8, phase exp(-i*pi/2)=-i
        assert np.max(abs(U.conj().T@U-I))<1e-11
        resource=phi@U.T
        assert abs(np.vdot(resource,resource)-1)<1e-11
        for _ in range(3):
            psi=rng.normal(size=d)+1j*rng.normal(size=d)
            psi/=np.linalg.norm(psi)
            # Input register I, resource registers R,B; Bell projection
            # on I,R yields unnormalized output U|psi>/d.
            amp=np.einsum("a,ab->b",psi,resource)/math.sqrt(d)
            desired=U@psi/d
            maxerr=max(maxerr,float(np.max(abs(amp-desired))))
            probs.append(float(np.vdot(amp,amp).real))
    assert maxerr<1e-12
    assert max(abs(np.array(probs)-1/256))<1e-12
    return {
      "status":"PASS","chart_unitaries_tested":45,
      "input_dimension_two_ququarts":16,
      "ancilla_resource":"(I_16 tensor U_z)|Phi_16>, two entangled registers each with dimension16",
      "resource_ancilla_ququarts":4,
      "additional_input_ququarts":2,
      "accepted_Bell_outcomes":1,
      "ideal_single_postselected_outcome_probability":1/256,
      "outputs_tested":len(probs),
      "max_teleportation_unitary_residual":maxerr,
      "state_independent_ideal_herald_probability":True,
      "caveat":"Requires the U-rotated resource state and a generalized d=16 Bell measurement. Preparing that resource may be as hard as U; this is a generic conditional construction, NOT an optical hardware compilation or a heralding efficiency measured on a chip."
    }

def pauli_ops():
    I=np.eye(2,dtype=complex)
    X=np.array([[0,1],[1,0]],complex)
    Z=np.diag([1,-1]).astype(complex)
    return I,X,Z

def gauge_dynamics(A):
    """An actual finite Z2 link-QUBIT model with matter and exact Gauss laws."""
    I,X,Z=pauli_ops()
    ops={"I":I,"X":X,"Z":Z}
    def op(mapping):
        pieces=[ops[mapping.get(i,"I")] for i in range(8)]
        out=pieces[0]
        for a in pieces[1:]:out=np.kron(out,a)
        return out
    G=[op({v:"Z",4+v:"X",4+(v-1)%4:"X"}) for v in range(4)]
    W=op({4+i:"Z" for i in range(4)})
    t,g,m,kappa=.4,.5,.6,.25
    H=-t*sum(op({v:"X",(v+1)%4:"X",4+v:"Z"}) for v in range(4))
    H-=g*sum(op({4+i:"X"})for i in range(4))
    H-=m*sum(op({i:"Z"}) for i in range(4))
    H-=kappa*W
    assert np.max(abs(H-H.conj().T))<1e-12
    for Gi in G:
        assert np.max(abs(Gi@H-H@Gi))<1e-12
        assert np.max(abs(Gi@W-W@Gi))<1e-12
    # Basis: link X eigenvalues fix matter Z via Gauss +1.
    plus=np.array([1,1],complex)/math.sqrt(2)
    minus=np.array([1,-1],complex)/math.sqrt(2)
    computational=[np.array([1,0],complex),np.array([0,1],complex)]
    basis=[]
    for bits in itertools.product((0,1),repeat=4):
        zlink=[1-2*b for b in bits]
        zmat=[zlink[(v-1)%4]*zlink[v] for v in range(4)]
        vec=computational[0 if zmat[0]==1 else 1]
        for v in range(1,4):
            vec=np.kron(vec,computational[0 if zmat[v]==1 else 1])
        for b in bits:
            vec=np.kron(vec,plus if b==0 else minus)
        basis.append(vec)
    B=np.array(basis).T
    assert B.shape==(256,16)
    assert np.max(abs(B.conj().T@B-np.eye(16)))<1e-12
    for Gi in G:
        assert np.max(abs(Gi@B-B))<1e-12
    Hg=B.conj().T@H@B
    Wg=B.conj().T@W@B
    assert np.max(abs(Hg-Hg.conj().T))<1e-12
    assert np.max(abs(Wg@Wg-np.eye(16)))<1e-11
    rows=[]
    for kk in (0,.1,.25,.5,.8):
        Hval=Hg+(kappa-kk)*Wg
        ev,U=np.linalg.eigh(Hval)
        ground=U[:,0]
        rows.append({"plaquette_coupling":kk,
                     "ground_energy":float(ev[0]),
                     "first_excitation_gap":float(ev[1]-ev[0]),
                     "ground_Wilson_loop_mean":float(np.vdot(ground,Wg@ground).real)})
    # Genuine gauge-invariant coupling of a *global* 45-state internal
    # Witting chart degree to the physical Z2 plaquette. NOT a 3D QFT.
    delta=.01
    P24=(15*np.eye(45)-5*A+np.ones((45,45)))/30
    assert np.max(abs(P24@P24-P24))<1e-12
    # Three internal GQ spectral sectors: E=0(1), 9delta(20),15delta(24)
    # with an explicitly imposed -lambda W P24 interaction.
    lam=1.0
    Ebase=np.linalg.eigvalsh(Hg)[0]
    E20=Ebase+9*delta
    E24=np.linalg.eigvalsh(Hg-lam*Wg)[0]+15*delta
    assert E24<Ebase, (Ebase,E20,E24)
    # A distinct chart-local Wilson coupling mixes the internal spectral
    # sectors, unlike the diagonal -W P24 term above.
    from scipy import sparse
    from scipy.sparse.linalg import eigsh
    P1=np.ones((45,45))/45
    P20=np.eye(45)-P1-P24
    chart_defect=np.zeros((45,45)); chart_defect[0,0]=1
    assert np.max(abs(chart_defect@P24-P24@chart_defect))>1e-4
    chartH=12*np.eye(45)-A
    Hfree=(sparse.kron(sparse.csr_matrix(Hg),sparse.eye(45),format="csr")
           +delta*sparse.kron(sparse.eye(16),sparse.csr_matrix(chartH),format="csr"))
    Hdefect=sparse.kron(sparse.csr_matrix(Wg),sparse.csr_matrix(chart_defect),format="csr")
    mixed=[]
    for coupling in (0,.3,1.0,2.0):
        eigenvalues,vecs=eigsh(Hfree-coupling*Hdefect,k=1,which="SA",tol=1e-10)
        state=vecs[:,0].reshape(16,45)
        weights={}
        for name,projector in (("uniform",P1),("sector20",P20),("sector24",P24)):
            weights[name]=float(np.einsum("ia,ab,ib->",state.conj(),projector,state).real)
        assert abs(sum(weights.values())-1)<1e-9
        mixed.append({"chart_local_Wilson_coupling":coupling,
                      "ground_energy":float(eigenvalues[0]),
                      "internal_sector_weights":weights})
    assert mixed[0]["internal_sector_weights"]["uniform"]>.99999
    assert mixed[-1]["internal_sector_weights"]["sector24"]>.0001
    return {
      "status":"PASS",
      "chart_local_defect_Wilson_mixes_spectral_sectors":True,
      "chart_local_Wilson_coupling_scan":mixed,
      "lattice_geometry":"one square cycle of four matter vertices and four link qubits",
      "Hilbert_total_dim":256,
      "independent_Z2_Gauss_constraints":4,
      "physical_Gauss_plus1_subspace_dim":16,
      "gauge_generators":"G_v = Z_matter(v) X_link(v-1) X_link(v)",
      "gauge_invariant_hamiltonian":
          "H=-t sum X_m(v) Z_link(v) X_m(v+1) -g sum X_link -m sum Z_matter -k W_square",
      "gauge_invariant_Wilson_operator":"W_square=product_4 Z_link",
      "max_exact_Gauss_commutation_error":float(max(np.max(abs(Q@H-H@Q))for Q in G)),
      "couplings":{"hopping":t,"electric":g,"mass":m,"plaquette":kappa},
      "plaquette_coupling_scan":rows,
      "global_45chart_internal_fiber_coupling":"Delta*(12 I45-A_GQ)-lambda*W_square tensor P24",
      "global_fiber_internal_delta":delta,
      "global_fiber_Wilson_coupling_lambda":lam,
      "uncoupled_uniform_sector_ground_energy":float(Ebase),
      "uncoupled_20D_sector_ground_energy":float(E20),
      "engineered_24D_sector_ground_energy":float(E24),
      "engineered_24D_is_lowest_of_three_internal_sectors":True,
      "theory_boundary":"Gauss law exact on finite four-vertex Z2 gauge model, but chart projector coupling chosen by hand; no emergent spatial dimensions, continuous SU3 standard-model gauge group or Lorentzian gravity."
    }

def label_information(supports):
    """Exact Bayes leakage if the chart is fixed for repeated independent photons."""
    H=np.array([[int(i in s) for i in range(40)]for s in supports],int)
    assert H.shape==(45,40)
    assert np.all(H.sum(0)==9)
    prior_entropy=math.log2(45)
    data=[]
    for trials in (1,2,3,4):
        occurrences=collections.Counter()
        for support in supports:
            S=sorted(support)
            for seq in itertools.product(S,repeat=trials):
                occurrences[seq]+=1
        # With chart uniform and rays uniform among the chosen 8:
        # Pr(sequence)=#{charts supporting seq}/(45*8^n),
        # posterior chart uniform on that supporting set.
        weighted=sum(count*math.log2(count) for count in occurrences.values())
        denom=45*8**trials
        posterior=weighted/denom
        map_accuracy=len(occurrences)/denom
        if trials==1:
            assert len(occurrences)==40 and abs(posterior-math.log2(9))<1e-12
            assert abs(map_accuracy-1/9)<1e-12
        if trials==2:
            assert len(occurrences)==1600 and abs(map_accuracy-5/9)<1e-12
        data.append({"photons_on_fixed_chart":trials,
             "conditional_chart_entropy_bits":float(posterior),
             "mutual_info_chart_to_rays_bits":float(prior_entropy-posterior),
             "maximum_a_posteriori_guess_accuracy":float(map_accuracy),
             "distinct_possible_reported_sequences":len(occurrences)})
    assert data[2]["maximum_a_posteriori_guess_accuracy"]>data[1]["maximum_a_posteriori_guess_accuracy"]
    # The previous 25-bin compressed detector (24 global ray labels plus
    # a bucket for 16 other rays) trades local FI for less chart leakage.
    resolved=[31,7,21,28,22,30,3,15,4,23,26,25,8,1,32,20,19,29,14,38,16,39,11,37]
    assert len(set(resolved))==24
    compressed=np.asarray(H[:,resolved],dtype=float)/8
    compressed=np.column_stack((compressed,1-compressed.sum(axis=1)))
    def entropy(p):
        return float(-sum(float(x)*math.log2(float(x)) for x in p if x>1e-14))
    mi25=entropy(compressed.mean(axis=0))-float(np.mean([entropy(q) for q in compressed]))
    assert abs(mi25-1.4359177277412059)<1e-10
    assert 0<mi25<math.log2(5)
    return {
      "status":"PASS",
      "one_shot_25bin_compressed_chart_information_leak_bits":mi25,
      "25bin_compression_leak_reduction_bits":math.log2(5)-mi25,
      "prior_chart_entropy_bits":prior_entropy,
      "single_ray_information_leak_bits":math.log2(5),
      "single_ray_compatible_chart_count":9,
      "case_distribution":data,
      "critical_caveat":"No chart ID is explicitly logged, but a globally labeled Witting outcome still leaks chart identity. With repeated photons on the same fixed chart, chart inference rapidly improves. Resampling each chart per photon changes the leakage calculation."
    }

def check_model(supports,A):
    """The 40-global-label model has 15 independent statistical null tests."""
    H=np.array([[int(i in s) for i in range(40)]for s in supports],float)
    P24=(15*np.eye(45)-5*A+np.ones((45,45)))/30
    Q24=H.T@P24@H/12
    Q1=np.ones((40,40))/40
    R=np.eye(40)-Q1-Q24
    assert np.max(abs(R@R-R))<1e-11
    assert abs(np.trace(R)-15)<1e-11
    assert np.linalg.matrix_rank(R,tol=1e-9)==15
    rng=np.random.default_rng(SEED)
    N=20000
    p0=np.ones(40)/40
    null_test=[]
    for _ in range(400):
        freq=rng.multinomial(N,p0)/N
        chi=40*N*np.linalg.norm(R@(freq-p0))**2
        null_test.append(chi)
    mu=float(np.mean(null_test))
    assert 12<mu<18
    # Any deviation living inside Q24 passes *even at infinite shots*,
    # so goodness-of-fit cannot guarantee valid calibration.
    x=P24@rng.standard_normal(45)
    x*=.002/max(abs(x))
    alt=p0+H.T@x/8
    assert alt.min()>0 and abs(alt.sum()-1)<1e-11
    assert np.linalg.norm(R@(alt-p0))<1e-11
    return {
      "status":"PASS",
      "40_global_outcomes_normalized_simplex_dim":39,
      "hidden_chart_model_parameter_dim":24,
      "null_goodness_of_fit_constraints_dim":15,
      "residual_orthogonal_projector_exact":True,
      "pearson_like_chi_square":"chi=40*N*||R(p_observed-1_40/40)||^2",
      "uniform_model_asymptotic_reference_chi_square_degrees_of_freedom":15,
      "seeded_null_simulation_runs":400,
      "seeded_null_mean_chisquare":mu,
      "undetectable_24D_calibration_modes_remain":True,
      "caveat":"The chi-square reference is asymptotic and assumes i.i.d. uniform counts. A 24D sensor corruption can pass undetected, and nuisance-fitted alternatives need a different calibrated test distribution."
    }

def main():
    rays,S,decks,A,P,O,H,P24,K=setup()
    a=identifiability(rays,H,P24)
    print("F1 exact detector nuisance ambiguity",a["maximum_probing_state_probability_difference"],flush=True)
    b=recovery(rays)
    print("F2 Petz 4d and qubit Fe",b["full_ququart_recovery"]["Fe"],b["best_two_dim_subcode_recovery"]["Fe"],flush=True)
    c=heralded_gate(P,S)
    print("F3 postselected teleport",c["ideal_single_postselected_outcome_probability"],flush=True)
    d=gauge_dynamics(A)
    print("F4 finite Z2 gauge physical dim",d["physical_Gauss_plus1_subspace_dim"],flush=True)
    e=label_information(S)
    print("F5 chart leakage",e["case_distribution"][1]["maximum_a_posteriori_guess_accuracy"],flush=True)
    f=check_model(S,A)
    print("F6 null-model chi2",f["seeded_null_mean_chisquare"],flush=True)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    record={"date":"2026-11-21","status":"PASS",
        "front1_blind_ray_detector_efficiency_no_go_and_reference":a,
        "front2_explicit_Petz_decoder_and_subcode":b,
        "front3_exact_conditional_gate_teleportation":c,
        "front4_true_Z2_lattice_gauge_matter_Gauss_law":d,
        "front5_globally_labeled_ray_chart_leakage":e,
        "front6_one_photon_15D_model_residual_falsifier":f,
        "scope":"Mathematical finite models, random seeded simulations and exact matrix algebra; not hardware demonstrations or a TOE."}
    OUT.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("SIX FINITE FALSIFIERS PASS",OUT,flush=True)

if __name__=="__main__": main()
