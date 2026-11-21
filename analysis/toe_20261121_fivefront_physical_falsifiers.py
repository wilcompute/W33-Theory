"""Independent device/noise, 27-deck optimization, CPTP-channel, selector,
and causal-memory audits continuing the 2026-11-21 Witting bridge.
Toy parameters are labeled assumptions, never measured hardware numbers.
"""
from __future__ import annotations
import collections, itertools, json, math, sys
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_hermitian45_pauli_sic_bridge as base
import toe_20261121_27decks_fivefronts as prev
OUT=ROOT/"data/toe_20261121_device_scheduler_channel_causal_audit.json"

def geometry():
    rays,wf4=base.witting_rays()
    iso=sorted({base.norm4(v) for v in itertools.product(range(4),repeat=4)
                if any(v) and base.herm4(v,v)==0})
    supports=[frozenset(i for i,x in enumerate(wf4) if base.herm4(z,x)==0)
              for z in iso]
    keys={z:i for i,z in enumerate(iso)}
    lines=sorted({tuple(sorted({keys[base.norm4(prev.plus4(u,v,a,b))]
            for a,b in itertools.product(range(4),repeat=2) if a or b}))
            for u,v in itertools.combinations(iso,2) if base.herm4(u,v)==0})
    geo,graph,schedules=prev.first_front(rays,wf4,iso,lines,supports)
    mapping={int(k):int(v) for k,v in base.analyze()[
                        "ray_index_to_F3_projective_point_index"].items()}
    return rays,wf4,iso,supports,schedules,graph,mapping

def optical_noise(rays,supports,schedules):
    """Physical port loss, mesh-depth ledger and a separable postselection trap."""
    overlap=np.abs(rays.conj()@rays.T)**2
    # Every orthogonality K4 of the SRG(40,12,2,4) is a Witting PVM basis.
    graph=nx.Graph()
    graph.add_nodes_from(range(40))
    graph.add_edges_from((a,b) for a,b in itertools.combinations(range(40),2)
                         if overlap[a,b]<1e-10)
    tetrads=sorted(tuple(sorted(C)) for C in nx.find_cliques(graph))
    assert len(tetrads)==40 and set(map(len,tetrads))=={4}
    assert all(np.max(abs(sum(np.outer(rays[i],rays[i].conj())
                              for i in C)-np.eye(4)))<1e-11 for C in tetrads)
    # Assumed detector efficiencies (NOT calibrated from an actual experiment).
    eta4=np.array([.94,.96,.92,.95])
    eta8=np.array([.94,.96,.92,.95,.90,.93,.97,.91])
    def four_survival(v):
        return float(np.mean([sum(eta4[k]*overlap[v,i]
                      for k,i in enumerate(C)) for C in tetrads]))
    def eight_survival(v,L):
        return float(np.mean([
            sum(eta8[k]*overlap[v,i]/2 for k,i in enumerate(sorted(supports[z])))
            for z in L
        ]))
    # "Clements" rectangular universal optical mesh: 4x4 uses 6 2x2 cells;
    # 8x8 uses 28. Use illustrative paths of 4 or 8 equal-loss stages.
    bench=[]
    for per_stage_loss in (.005,.02):
        t=1-per_stage_loss
        for v in (0,7,17,39):
            orig=four_survival(v)*t**4
            new=np.array([eight_survival(v,L)*t**8 for L in schedules])
            assert all(0<x<=1 for x in [orig,*new])
            bench.append({"assumed_per_stage_loss":per_stage_loss,
                          "input_ray":v,"pvm_40setting_survival":orig,
                          "doubleSIC_5setting_survival_min":float(new.min()),
                          "doubleSIC_5setting_survival_max":float(new.max()),
                          "doubleSIC_5setting_survival_mean":float(new.mean())})
    # Explicit local filtering counterexample to postselecting a separable state.
    # Send |r0> and |r0*> (separable) into both analyzers, same random
    # chart in one 5-setting schedule. At the one chart containing ray0
    # let its detector eta(ray0)=1, all other outcomes/charts eta=1/2.
    L=schedules[0]
    z0=next(z for z in L if 0 in supports[z])
    numerator=denominator=0.
    for z in L:
        ids=sorted(supports[z])
        p=np.array([overlap[0,i]/2 for i in ids])
        assert abs(p.sum()-1)<1e-11
        eta=np.full(8,.5)
        if z==z0:eta[ids.index(0)]=1.
        q=eta*p
        numerator+=float(np.dot(q,q))/5
        denominator+=float(q.sum()**2)/5
    conditional_match=numerator/denominator
    assert abs(conditional_match-.28)<1e-12
    return {
      "status":"PASS","four_mode_PVM_settings":40,
      "eight_mode_doubleSIC_settings_per_deck":5,
      "distinct_five_setting_decks":27,
      "universal_4mode_MZI_count":6,
      "universal_8mode_MZI_count":28,
      "illustrative_balanced_path_depth_4mode":4,
      "illustrative_balanced_path_depth_8mode":8,
      "assumed_not_measured_detector_efficiencies_4":eta4.tolist(),
      "assumed_not_measured_detector_efficiencies_8":eta8.tolist(),
      "loss_sensitivity_benchmark":bench,
      "loss_postselection_trap_separable_input":"|r0> x |r0*>",
      "unfiltered_separable_match_bound":.2,
      "biased_postselected_separable_match":conditional_match,
      "biased_postselected_numerator":numerator,
      "biased_postselected_denominator":denominator,
      "assumption":"Uniform depth factor t^N and scalar photon detection response; no actual Clements decomposition, chip design, QKD security proof, or measured losses.",
      "warning":"A separable state yields 0.28 > ideal unfiltered separable bound 0.20 after outcome/setting-dependent losses: herald/detection postselection without model invalidates that witness."
    }

def scheduler(supports,schedules,graph):
    """Exact extremal 5-context coverings and 24-dimensional cost invisibility."""
    K=np.zeros((45,27),dtype=int)
    for j,L in enumerate(schedules):
        K[L,j]=1
    assert np.array_equal(K@K.T,3*np.eye(45,dtype=int)+graph)
    eigval,eigvec=np.linalg.eigh(K@K.T)
    rounded=collections.Counter(np.rint(eigval).astype(int))
    assert rounded=={0:24,6:20,15:1},rounded
    assert np.linalg.matrix_rank(K)==21
    assert set(K.sum(axis=0))=={5} and set(K.sum(axis=1))=={3}
    # Four local modes vs 8-port modes may have different costs;
    # this is about chart-dependent *scalar* costs only.
    v=eigvec[:,0]
    c=1+0.25*v/max(abs(v))
    assert c.min()>=.75 and c.max()<=1.25
    blind=K.T@c
    invis=float(max(abs(blind-5)))
    assert invis<1e-12
    rng=np.random.default_rng(20261121)
    costs=.8+.4*rng.uniform(size=45)
    scores=K.T@costs
    avg=5*costs.mean()
    assert abs(scores.mean()-avg)<1e-12
    assert scores.min()<=avg<=scores.max()
    max_cliques=[tuple(sorted(x)) for x in nx.find_cliques(nx.from_numpy_array(graph))]
    assert len(max_cliques)==27 and set(map(len,max_cliques))=={5}
    assert set(max_cliques)==set(tuple(x) for x in schedules)
    return {
      "status":"PASS","minimal_number_of_8ray_POVMs_to_cover_all_40_rays":5,
      "all_minimal_exact_disjoint_covers":27,
      "incidence_KKt_identity":"KK^T=3I_45 + A_H(3,4)",
      "cost_visible_rank":21,"cost_invisible_nullity":24,
      "KKT_spectrum":{int(k):int(v) for k,v in rounded.items()},
      "min_sample_positive_chart_cost":float(c.min()),
      "max_sample_positive_chart_cost":float(c.max()),
      "max_27_schedule_cost_deviation_for_nonuniform_invisible_cost":invis,
      "random_cost_min_schedule":int(scores.argmin()),
      "random_cost_min_total":float(scores.min()),
      "random_cost_mean_total":float(avg),
      "random_cost_max_total":float(scores.max()),
      "exact_mean_identity":"mean_27 deck cost = (1/9) sum_45 chart costs = 5 mean chart cost",
      "warning":"24D invisibility holds for additive per-chart costs, not arbitrary nonlinear switching, outcome-conditioned loss or real-device calibration."
    }

def channel(rays,mapping):
    """Choi rank/PPT and an unconditional diamond separation from isometries."""
    omega=np.exp(2j*np.pi/3)
    X=np.roll(np.eye(3),1,axis=0)
    Z=np.diag(omega**np.arange(3))
    points=sorted({base.canonical3(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    E=np.einsum("ia,ib->iab",rays,rays.conj())/10
    assert np.max(abs(E.sum(axis=0)-np.eye(4)))<1e-11
    sig=[]
    for i in range(40):
        a,c,b,d=points[mapping[i]]
        U=np.kron(np.linalg.matrix_power(Z,a)@np.linalg.matrix_power(X,b),
                  np.linalg.matrix_power(Z,c)@np.linalg.matrix_power(X,d))
        Q=(np.eye(9)+U+U.conj().T)/3
        assert np.max(abs(Q@Q-Q))<1e-11
        sig.append(Q/3)
    J=sum(np.kron(E[i].T,sig[i]) for i in range(40))
    assert np.max(abs(J-J.conj().T))<1e-11
    assert abs(np.trace(J).real-4)<1e-11
    choi=J/4
    eig=np.linalg.eigvalsh(choi)
    ppt=J.reshape(4,9,4,9).transpose(2,1,0,3).reshape(36,36)/4
    evppt=np.linalg.eigvalsh(ppt)
    assert min(eig)>-1e-11 and min(evppt)>-1e-11
    # All 40 terms are explicitly positive separable product operators,
    # which is stronger than checking PPT in 4 x 9.
    rng=np.random.default_rng(91)
    fid=[]
    for _ in range(10):
        T=rng.standard_normal((9,4))+1j*rng.standard_normal((9,4))
        V=np.linalg.qr(T)[0]
        phi=sum(np.kron(np.eye(4)[:,j],V[:,j]) for j in range(4))/2
        f=float(np.vdot(phi,choi@phi).real)
        assert 0<=f<=.25+1e-12
        fid.append(f)
    return {
      "status":"PASS","Choi_normalized_min_eigen":float(eig.min()),
      "Choi_normalized_rank":int(sum(eig>1e-12)),
      "Choi_PPT_min_eigen":float(evppt.min()),
      "explicit_separable_Choi_terms":40,
      "isometry_reference_entanglement_fidelity_10samples":fid,
      "universal_entanglement_fidelity_upper_bound_for_every_isometry":.25,
      "diamond_norm_distance_lower_bound_from_any_ideal_isometry":1.5,
      "quantum_capacity":0,
      "HS_traceless_inverse_amplification":15,
      "warning":"Diamond lower bound and capacity zero apply to THIS entanglement-breaking channel, not all possible C4->C9 coherent channels."
    }

def selector(rays,supports,schedules,graph):
    """Two-photon optical quartic collision energy and noncommuting source modes."""
    overlaps=np.abs(rays.conj()@rays.T)**2
    # Collisions for each two-copy product input |ra> x |rb>.
    F=np.array([overlaps[:,list(S)]@overlaps[:,list(S)].T for S in supports])
    assert F.shape==(45,40,40)
    # Each 5-chart schedule partitions the 40 projectors. Therefore
    # K^T F_ab = sum_{i=1..40} |<ra|ri>|^2 |<rb|ri>|^2
    #          = 2 (1+ |<ra|rb>|^2) by the complex projective 2-design.
    # The centered 45-chart collision profiles exactly span ker K^T.
    incidence=np.zeros((45,27),int)
    for j,L in enumerate(schedules):incidence[L,j]=1
    V=np.array([F[:,a,b] for a,b in itertools.combinations(range(40),2)]).T
    center=V-V.mean(axis=0,keepdims=True)
    rank_v=int(np.linalg.matrix_rank(V,tol=1e-9))
    rank_center=int(np.linalg.matrix_rank(center,tol=1e-9))
    assert (rank_v,rank_center)==(25,24)
    # EXACT integer certificate: W_{ai}=3*|<ra|ri>|^2 in {0,1,3},
    # so T_{z,ab}=sum_{i in chart z} W_ai W_bi = 9 F_z(a,b).
    W=np.rint(3*overlaps).astype(np.int64)
    assert set(W.ravel())=={0,1,3} and np.max(abs(W-3*overlaps))<1e-10
    T=np.array([W[:,list(S)]@W[:,list(S)].T for S in supports])
    assert np.max(abs(T-9*F))<1e-10
    Tpair=np.array([T[:,a,b] for a,b in itertools.combinations(range(40),2)]).T
    totals=Tpair.sum(axis=0)
    assert all(totals%9==0)
    # Five times the centered vector, with no floating-point division.
    exact_center=5*Tpair-(totals//9)[None,:]
    assert np.array_equal(incidence.T@exact_center,np.zeros((27,780),int))
    assert np.array_equal((graph+3*np.eye(45,dtype=int))@exact_center,
                          np.zeros((45,780),int))
    def rank_mod_p(raw,p):
        M=np.remainder(raw,p).copy()
        nr,nc=M.shape
        rank=0
        for j in range(nc):
            if rank>=nr:break
            nz=np.flatnonzero(M[rank:,j])
            if not nz.size:continue
            k=int(rank+nz[0])
            M[[rank,k]]=M[[k,rank]]
            M[rank]=M[rank]*pow(int(M[rank,j]),-1,p)%p
            M[rank+1:]=(M[rank+1:]-M[rank+1:,j,None]*M[rank])%p
            rank+=1
        return rank
    gf7_rank=rank_mod_p(exact_center,7)
    assert gf7_rank==24
    assert rank_mod_p(Tpair,7)==25
    # Inclusion in a 24D rational kernel + GF7 rank 24 proves
    # exact rank 24 over Q, without numerical eigenvalue inference.
    null_res=float(np.max(abs(incidence.T@center)))
    spectral_res=float(np.max(abs((graph+3*np.eye(45))@center)))
    assert null_res<1e-10 and spectral_res<1e-10
    # Each chart belongs to three decks: 3 sum_z Fz = 27 sum_i f_i,
    # so (sum_z Fz)/9 = sum_i f_i.
    design_sum_res=max(abs(float(np.sum(F[:,a,b])/9)-
                      2*(1+overlaps[a,b]))
                     for a,b in itertools.combinations(range(40),2))
    assert design_sum_res<1e-10
    nonorth_scores=set()
    orth_scores=set()
    min_gap=math.inf
    for a,b in itertools.combinations(range(40),2):
        histogram=tuple(sorted(collections.Counter(
            np.rint(9*F[:,a,b]).astype(int)).items()))
        if overlaps[a,b]>1e-10:
            nonorth_scores.add(histogram)
            vals=np.sort(F[:,a,b])
            min_gap=min(min_gap,float(vals[-1]-vals[-2]))
        else:orth_scores.add(histogram)
    assert nonorth_scores=={((4,12),(5,32),(8,1))}
    assert orth_scores=={((0,3),(3,12),(4,27),(6,3))}
    assert abs(min_gap-1/3)<1e-10
    # The matched-outcome double-SIC coincidence probability is F/4.
    # Hoeffding union bound for 45 independent settings, each sampled n:
    # Pr(any |p_hat-p| >= Delta/2) <= 90 exp(-n Delta^2/2).
    delta=1/12
    shots_per_chart=math.ceil(2*math.log(90/.01)/(delta*delta))
    assert 90*math.exp(-shots_per_chart*delta*delta/2)<=.01
    # Mean of all 45 chart collisions from uniform chart experiment
    # and unique-minimizer frequency under physically meaningful joint coincidence.
    stats={"orthogonal":collections.Counter(),"nonorthogonal":collections.Counter()}
    match={"orthogonal":0,"nonorthogonal":0}
    for a,b in itertools.combinations(range(40),2):
        s="orthogonal" if overlaps[a,b]<1e-10 else "nonorthogonal"
        col=F[:,a,b]
        arg=np.flatnonzero(abs(col-col.max())<1e-10)
        stats[s][int(len(arg))]+=1
        ideal=[z for z,S in enumerate(supports) if a in S and b in S]
        if len(arg)==1 and int(arg[0]) in ideal:match[s]+=1
    a,b=0,5
    assert abs(overlaps[a,b]-1/3)<1e-10
    A=np.outer(rays[a],rays[a].conj())
    B=np.outer(rays[b],rays[b].conj())
    comm_norm=float(np.linalg.norm(A@B-B@A,ord=2))
    assert abs(comm_norm-math.sqrt(2)/3)<1e-10
    # An apparently natural chart intensity coupling gives NO selector:
    # all chart projectors sum to 2I on the entire C4 Hilbert space.
    sum_dev=max(np.max(abs(sum(np.outer(rays[i],rays[i].conj())
                    for i in S)-2*np.eye(4))) for S in supports)
    assert sum_dev<1e-11
    energies=np.array([-(int(a in S)+int(b in S)) for S in supports],dtype=float)
    assert list(np.sort(energies))[:2]==[-2.,-1.]
    source_selector=int(np.argmin(energies))
    rng=np.random.default_rng(71)
    min_gaps=[]
    for _ in range(16):
        M=rng.normal(size=(45,45))+1j*rng.normal(size=(45,45))
        M=(M+M.conj().T)/2
        M=.4*M/np.linalg.norm(M,2)
        e=np.linalg.eigvalsh(np.diag(energies)+M)
        min_gaps.append(float(e[1]-e[0]))
    assert min(min_gaps)>.2-1e-10
    return {
      "status":"PASS",
      "nonorthogonal_two_source_example":[a,b],
      "nonorthogonal_ray_projector_commutator_norm":comm_norm,
      "total_doubleSIC_chart_intensity_is_2I_all_45":True,
      "total_chart_intensity_selector_is_impossible":True,
      "two_copy_joint_collision_max_degeneracy_histograms":{k:dict(v) for k,v in stats.items()},
      "exact_nonorthogonal_chart_score_histogram_times9":{4:12,5:32,8:1},
      "exact_orthogonal_chart_score_histogram_times9":{0:3,3:12,4:27,6:3},
      "all_780_pair_collision_vectors_span_rank":rank_v,
      "all_780_centered_pair_collision_vectors_span_rank":rank_center,
      "exact_centered_collision_rank_over_GF7":gf7_rank,
      "exact_integer_kernel_residual_zero":True,
      "exact_rank_24_Q_certificate":"rank over F7 is 24, while incidence kernel has dimension 24 over Q",
      "centered_collision_vectors_equal_deck_cost_nullspace":rank_center==24,
      "centered_collision_deck_null_residual":null_res,
      "centered_collision_minus3_eigenspace_residual":spectral_res,
      "Witting_complex_projective_2design_sum_residual":design_sum_res,
      "minimum_nonorthogonal_score_maximum_margin":min_gap,
      "matched_doubleSIC_nonorthogonal_probability_margin":delta,
      "assumed_independent_trials_for_1percent_union_bound_per_chart":shots_per_chart,
      "assumed_total_45chart_trials":45*shots_per_chart,
      "quartic_collision_unique_max_matches_incidence_chart":match,
      "externally_programmed_label_selector_selected_chart":source_selector,
      "source_selector_unperturbed_ground_gap":1,
      "all_16_perturbed_ground_gaps_above_0p2":True,
      "min_random_ground_gap_with_norm0p4_perturbation":min(min_gaps),
      "gap_bound":"Delta_gap >= g-2epsilon for Hermitian perturbation operator norm epsilon",
      "warning":"Nonorthogonal Witting ray creation/number modes do not commute; naive cross-Kerr on two 'independent ray modes' is invalid. Label-programming/copy resources are external."
    }

def causal_memory(iso,graph):
    """No invariant causal orientation; two-step collapse, qutrit memory levels."""
    assert np.array_equal(graph@graph,9*np.eye(45,dtype=int)+3*np.ones((45,45),int))
    z=0
    neighbor=np.flatnonzero(graph[z])
    assert len(neighbor)==12
    assert set(np.flatnonzero((graph@graph)[z]))==set(range(45))
    # Seven independent Hermitian generators: spatial action on 45 objects.
    I=tuple(tuple(int(i==j) for j in range(4)) for i in range(4))
    def sw(i,j):
        x=[list(row) for row in I];x[i],x[j]=x[j],x[i];return x
    def dg(i):
        x=[list(row) for row in I];x[i][i]=2;return x
    JI=[[int(i!=j) for j in range(4)] for i in range(4)]
    mi=[sw(0,1),sw(1,2),sw(2,3),dg(0),dg(1),dg(2),JI]
    ids={u:i for i,u in enumerate(iso)}
    gens=[tuple(ids[base.norm4(prev.gf4_mat_apply(M,v))] for v in iso) for M in mi]
    edge=(0,int(neighbor[0]))
    seen={edge}
    stack=[edge]
    for q in stack:
        for g in gens:
            a,b=g[q[0]],g[q[1]]
            if (a,b) not in seen:
                seen.add((a,b));stack.append((a,b))
    assert len(seen)==45*12 and (edge[1],edge[0]) in seen
    # Directed age-layer lift z,t -> w,t+1 can be G-equivariant, but is an
    # externally defined clock. Its light cone covers all 45 in only 2 ticks.
    mem=prev.memory_front()
    assert abs(mem["ideal_quantum_memory_average_fidelity"]-1)<1e-12
    assert abs(mem["classical_Zdephased_memory_average_fidelity"]-.5)<1e-12
    return {
      "status":"PASS",
      "all_ordered_incident_pairs_single_orbit":540,
      "one_element_reverses_any_given_edge":True,
      "no_nontrivial_group_invariant_orientation_of_Hermitian_collinearity_graph":True,
      "A_squared":"A^2=9I+3J",
      "one_tick_accessible_spatial_neighbors":12,
      "two_ticks_accessible_spatial_vertices":45,
      "two_tick_markov_probability_return":1/12,
      "two_tick_markov_probability_any_other_vertex":1/48,
      "causal_time_lift":"externally add t and direct edges (z,t)->(w,t+1); does not derive time from projective symmetry",
      "qutrit_two_design_probes":12,
      "qutrit_EB_memory_fidelity_upper_bound":.5,
      "qutrit_intermediate_quantum_memory_dim_le_2_fidelity_upper_bound":.75,
      "qutrit_intermediate_quantum_memory_dim_ge_3_witness":"> 0.75",
      "witness_logic":"For a d-dimensional input and Schmidt-number-k temporal Choi state, Fe<=k/d and 2-design Favg=(d Fe+1)/(d+1)<=(k+1)/(d+1).",
      "scope_warning":"Finite clique graph and a two-SWAP causal-break memory toy are NOT a Lorentzian metric, microcausal QFT, Einstein gravity, or an experimentally instrument-verified memory."
    }

def main():
    rays,wf4,iso,supports,schedules,graph,mapping=geometry()
    o=optical_noise(rays,supports,schedules);print("FRONT1 port-loss",o["biased_postselected_separable_match"],flush=True)
    s=scheduler(supports,schedules,graph);print("FRONT2 deck nullity",s["cost_invisible_nullity"],flush=True)
    c=channel(rays,mapping);print("FRONT3 EB diamond distance",c["diamond_norm_distance_lower_bound_from_any_ideal_isometry"],flush=True)
    h=selector(rays,supports,schedules,graph);print("FRONT4 quartic selection histogram",h["two_copy_joint_collision_max_degeneracy_histograms"],flush=True)
    t=causal_memory(iso,graph);print("FRONT5 orbit",t["all_ordered_incident_pairs_single_orbit"],flush=True)
    data={"status":"PASS","date":"2026-11-21",
      "front_1_optical_mesh_loss_and_postselection":o,
      "front_2_27_deck_scheduler_nullspace":s,
      "front_3_CPTP_channel_coherence_bounds":c,
      "front_4_chart_selector_obstructions_and_two_copy_candidate":h,
      "front_5_causality_and_memory_dimension_witness":t,
      "provenance":"Extends committed 2026-11-21 Witting-Hermitian scripts. External photonic literature cited in adjacent narrative; no actual experiments or hardware calibration."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS FIVE FRONTS",OUT,flush=True)

if __name__=="__main__":main()
