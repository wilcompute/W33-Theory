"""Five independently falsifiable continuations of the 45 Hermitian Witting charts.

All claims finite/ideal quantum only. Not a physical TOE, secure QKD or
experiment. Deterministic certificate: data/toe_20261121_fivefront_27decks.json
"""
from __future__ import annotations
import collections, itertools, json, math, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_hermitian45_pauli_sic_bridge as old

OUT=ROOT/"data/toe_20261121_fivefront_27decks.json"
P4=(1,2,3)

def gf4_mul(a,b):
    return old.mul4(a,b)

def gf4_point(v):
    return old.norm4(v)

def herm(u,v):
    return old.herm4(u,v)

def plus4(u,v,a,b):
    return tuple(gf4_mul(a,x)^gf4_mul(b,y) for x,y in zip(u,v))

def gf4_mat_apply(M,v):
    return tuple(__import__("functools").reduce(
        int.__xor__, (gf4_mul(a,b) for a,b in zip(row,v)),0) for row in M)

def perm_comp(a,b):
    return tuple(a[b[i]] for i in range(len(a)))

def generate_group(gens,cap=60000):
    identity=tuple(range(len(gens[0])))
    seen={identity}
    stack=[identity]
    for p in stack:
        for g in gens:
            new=perm_comp(g,p)
            if new not in seen:
                seen.add(new)
                stack.append(new)
                if len(seen)>cap:
                    raise ValueError("unexpected group order exceeding cap")
    return seen

def first_front(rays,wf4,iso,iso_lines,supports):
    """Full Hermitian GQ line and the 27 five-setting measurement schedules."""
    sigma={x:i for i,x in enumerate(iso)}
    candidate={frozenset(gf4_point(plus4(u,v,a,b))
                        for a,b in itertools.product(range(4),repeat=2) if a or b)
               for u,v in itertools.combinations(iso,2) if herm(u,v)==0}
    assert len(candidate)==27 and all(len(L)==5 for L in candidate)
    iso_line_ids=sorted(tuple(sorted(sigma[x] for x in L)) for L in candidate)
    assert all(sum(int(z in L) for L in iso_line_ids)==3 for z in range(45))
    assert iso_lines==iso_line_ids
    chart_edges=np.zeros((45,45),dtype=int)
    for i,j in itertools.combinations(range(45),2):
        disjoint=int(not(supports[i]&supports[j]))
        chart_edges[i,j]=chart_edges[j,i]=disjoint
        assert disjoint==int(herm(iso[i],iso[j])==0)
    assert set(chart_edges.sum(axis=0))=={12}
    adjacent_common=set()
    nonadjacent_common=set()
    for i,j in itertools.combinations(range(45),2):
        n=int(chart_edges[i]@chart_edges[j])
        (adjacent_common if chart_edges[i,j] else nonadjacent_common).add(n)
    assert adjacent_common=={3} and nonadjacent_common=={3}
    schedules=[]
    for L in iso_lines:
        assert len(set().union(*(supports[z] for z in L)))==40
        assert all(not(supports[i]&supports[j]) for i,j in itertools.combinations(L,2))
        schedules.append(list(L))
    assert len(schedules)==27

    # The 27 geometric lines are the 27 Schlaefli/cubic-line labels.
    line_graph=np.zeros((27,27),dtype=int)
    for a,b in itertools.combinations(range(27),2):
        line_graph[a,b]=line_graph[b,a]=int(set(schedules[a]).isdisjoint(schedules[b]))
    assert set(line_graph.sum(axis=0))=={16}
    lam,mu=set(),set()
    for i,j in itertools.combinations(range(27),2):
        n=int(line_graph[i]@line_graph[j])
        (lam if line_graph[i,j] else mu).add(n)
    assert lam=={10} and mu=={8}

    L=12*np.eye(45,dtype=int)-chart_edges
    spectrum=collections.Counter(np.rint(np.linalg.eigvalsh(L)).astype(int))
    assert spectrum=={0:1,9:20,15:24}
    return {
        "status":"PASS",
        "H34_points":45,"H34_lines":27,
        "isotropic_points_per_line":5,"isotropic_lines_per_point":3,
        "H34_collinearity_SRG": [45,12,3,3],
        "chart_disjointness_equals_Hermitian_isotropic_collinearity":True,
        "all_27_five_chart_schedules_partition_40_Witting_rays":True,
        "Schlaefli_skew_lines_SRG": [27,16,10,8],
        "unique_27_five_chart_schedules":[list(L) for L in schedules],
        "chart_laplacian_spectrum":{int(k):int(v) for k,v in spectrum.items()},
        "spacetime_caveat":"Undirected unweighted graph Laplacian is positive semidefinite; no Lorentzian dynamics or continuum derived."
    },chart_edges,schedules

def group_front(wf4,iso,supports,chart_edges,schedules,mapping):
    """Explicit projective GU4(2)=PSp4(3) exceptional isomorphism on 40+45+27."""
    eye=tuple(tuple(int(i==j) for j in range(4)) for i in range(4))
    def sw(i,j):
        a=[list(row) for row in eye]
        a[i],a[j]=a[j],a[i]
        return tuple(tuple(row) for row in a)
    def dg(i):
        a=[list(row) for row in eye]
        a[i][i]=2
        return tuple(tuple(row) for row in a)
    JI=tuple(tuple(int(i!=j) for j in range(4)) for i in range(4))
    M=[sw(0,1),sw(1,2),sw(2,3),dg(0),dg(1),dg(2),JI]
    for m in M:
        for i in range(4):
            for j in range(4):
                ei=eye[i]
                ej=eye[j]
                assert herm(gf4_mat_apply(m,ei),gf4_mat_apply(m,ej))==int(i==j)
    index4={x:i for i,x in enumerate(wf4)}
    index45={x:i for i,x in enumerate(iso)}
    pg=[]
    hg=[]
    for m in M:
        pg.append(tuple(index4[gf4_point(gf4_mat_apply(m,x))] for x in wf4))
        hg.append(tuple(index45[gf4_point(gf4_mat_apply(m,x))] for x in iso))
    # Verify each map on the complete 45 x 40 polar support, 27 incidence.
    sch_indices={tuple(x):i for i,x in enumerate(schedules)}
    line_gens=[]
    for p,q in zip(pg,hg):
        assert all({p[x] for x in supports[z]}==supports[q[z]]
                   for z in range(45))
        assert all(chart_edges[z,w]==chart_edges[q[z],q[w]]
                   for z in range(45) for w in range(45))
        rg=tuple(sch_indices[tuple(sorted(q[z] for z in line))]
                 for line in schedules)
        assert len(set(rg))==27
        line_gens.append(rg)
    gp=generate_group(pg)
    assert len(gp)==25920, ("wrong projective Hermitian group",len(gp))
    hgset=generate_group(hg)
    assert len(hgset)==25920
    line_set=generate_group(line_gens)
    assert len(line_set)==25920
    # Recover native full Sp(4,3) from five transvections as in TOE92.
    X=sorted({old.canonical3(q) for q in itertools.product(range(3),repeat=4) if any(q)})
    ix={x:i for i,x in enumerate(X)}
    reverse={j:i for i,j in mapping.items()}
    def sv(v):
        perm=[]
        for i in range(40):
            x=X[mapping[i]]
            t=old.symp3(x,v)
            y=old.canonical3(tuple((x[k]+t*v[k])%3 for k in range(4)))
            perm.append(reverse[ix[y]])
        return tuple(perm)
    trans=[sv(tuple(int(i==j) for i in range(4))) for j in range(4)]
    trans.append(sv((1,1,0,0)))
    assert all(g in gp for g in trans), "unitary and symplectic actions differ"
    # Native five symplectic transvections generate exactly the same group.
    st=generate_group(trans)
    assert st==gp
    return {
      "status":"PASS",
      "projective_GF4_Hermitian_group_order":len(gp),
      "PSp4_F3_full_group_order":len(st),
      "entire_25920_element_40point_actions_identical":True,
      "entire_45chart_group_order":len(hgset),
      "entire_27deck_group_order":len(line_set),
      "seven_Hermitian_generators_preserve_all_polar_supports":True,
      "five_F3_symplectic_transvections_generate_same_40point_group":True,
      "isomorphism":"PGU(4,2) isomorphic PSp(4,3) at projective permutation-group level",
      "physical_warning":"GF4 group actions identify projective incidence symmetry, not a C4-to-C9 unitary intertwiner."
    }

def optical_front(rays,wf4,iso,supports,schedules):
    """Eight-mode Naimark dilation for 45 double-SIC POVMs, and 27 five-setting readouts."""
    P=np.einsum("ia,ib->iab",rays,rays.conj())
    phi=np.zeros(16,complex)
    for i in range(4):
        phi[5*i]=0.5
    Phi=np.outer(phi,phi.conj())
    Ctarget=(np.eye(16)+4*Phi)/10
    max_pvm=0.0
    max_nai=0.0
    max_C=0.0
    for z in range(45):
        ids=sorted(supports[z])
        # Naimark isometry: 8 output amplitudes from 4 input modes.
        V=rays[ids].conj()/np.sqrt(2)
        err=float(np.max(abs(V.conj().T@V-np.eye(4))))
        max_pvm=max(max_pvm,err)
        Q,_=np.linalg.qr(V,mode="complete")
        U=np.column_stack((V,Q[:,4:]))
        max_nai=max(max_nai,float(np.max(abs(U.conj().T@U-np.eye(8)))))
        assert max_nai<1e-10
        # A single trial: append 4 vacuum amplitudes and unitary U;
        # 8 computational output probabilities equal Tr(rho P_i/2).
        psi=rays[17]
        probs=abs(U@np.r_[psi,np.zeros(4)])**2
        assert np.max(abs(probs-np.array([np.vdot(psi,P[i]@psi).real/2
                   for i in ids])))<1e-12
    assert max_pvm<1e-11
    for sched in schedules:
        for i in range(40):
            assert sum(i in supports[z] for z in sched)==1
        # Matched-outcome operator for E_i=P_i/2 at each arm.
        C=np.zeros((16,16),complex)
        for z in sched:
            for i in supports[z]:
                C+=np.kron(P[i],P[i].conj())/20
        max_C=max(max_C,float(np.max(abs(C-Ctarget))))
    assert max_C<1e-11
    eig=collections.Counter(np.rint(np.linalg.eigvalsh(Ctarget)*10).astype(int))
    assert eig=={1:15,5:1}
    return {
      "status":"PASS",
      "genuine_Naimark_8x8_extensions":45,
      "minimum_ancilla_outcome_space":8,
      "inputs_per_dilated_measurement":4,
      "max_coisometry_error":max_pvm,
      "max_nai_unity_error":max_nai,
      "all_27_schedules_equal_the_Witting_40outcome_POVM":True,
      "per_ray_POVM_effect":"P_i/10",
      "chart_bipartite_matched_operator":"(I_16+4 Phi4)/10",
      "max_27_schedule_matched_operator_residual":max_C,
      "entanglement_separable_threshold_trusted":0.2,
      "ideal_maximally_entangled_match_probability":0.5,
      "context_count_original_PVMs":40,"context_count_new_8outcome_POVMs":5,
      "hardware_warning":"8 outcomes need Naimark optical enlargement and calibrated losses; context compression does not imply resource or key-rate advantage."
    }

def channel_front(rays,mapping):
    """CPTP measurement/prepare bridge plus Weyl-covariant rank-four no-go."""
    omega=np.exp(2j*np.pi/3)
    Z=np.diag([omega**k for k in range(3)])
    X=np.roll(np.eye(3),1,axis=0)
    ops=[np.kron(np.linalg.matrix_power(Z,a)@np.linalg.matrix_power(X,b),
                 np.linalg.matrix_power(Z,c)@np.linalg.matrix_power(X,d))
         for a,b,c,d in itertools.product(range(3),repeat=4)]
    assert len(ops)==81
    rng=np.random.default_rng(20261121)
    examples=[]
    for seed in range(3):
        T=rng.normal(size=(9,4))+1j*rng.normal(size=(9,4))
        V,_=np.linalg.qr(T)
        P=V@V.conj().T
        twirl=sum(U@P@U.conj().T for U in ops)/81
        err=float(np.max(abs(twirl-(4/9)*np.eye(9))))
        assert err<1e-12
        leak=[1-np.trace(P@U@P@U.conj().T).real/4 for U in ops]
        assert abs(np.mean(leak)-5/9)<1e-12
        assert abs(np.mean(leak[1:])-9/16)<1e-12
        assert min(leak)>-1e-12
        examples.append({"seed":seed,"max_Pauli_twirl_error":err,
                         "nontrivial_Weyl_average_leakage":float(np.mean(leak[1:])),
                         "max_single_Weyl_leakage":float(max(leak))})
    # Confirm the projective-pair average explicitly for the third random code.
    point3=sorted({old.canonical3(v) for v in itertools.product(range(3),repeat=4)
                   if any(v)})
    named_W=[]
    for u in point3:
        a,b,c,d=u[0],u[2],u[1],u[3]
        U=np.kron(np.linalg.matrix_power(Z,a)@np.linalg.matrix_power(X,b),
                  np.linalg.matrix_power(Z,c)@np.linalg.matrix_power(X,d))
        assert np.max(abs(np.linalg.matrix_power(U,3)-np.eye(9)))<1e-11
        named_W.append(U)
    leak40=[1-np.trace(P@U@P@U.conj().T).real/4 for U in named_W]
    assert abs(np.mean(leak40)-9/16)<1e-12

    # A GENUINE physical bridge (but only an entanglement-breaking one):
    # ququart IC Witting effects P_i/10 -> two-qutrit rank-3 Pauli
    # eigenspace density matrices sigma_i=Pi_i/3.
    projectors=np.einsum("ia,ib->iab",rays,rays.conj())
    effects=projectors/10
    assert np.max(abs(np.sum(effects,axis=0)-np.eye(4)))<1e-12
    sigmas=[]
    for i in range(40):
        U=named_W[mapping[i]]
        Pi=(np.eye(9)+U+U.conj().T)/3
        assert np.max(abs(Pi@Pi-Pi))<1e-11
        assert abs(np.trace(Pi).real-3)<1e-11
        sigmas.append(Pi/3)
    sigmas=np.array(sigmas)
    sg=np.real(np.einsum("iab,jba->ij",sigmas,sigmas))
    expect=np.ones((40,40))/9+np.eye(40)*2/9
    assert np.max(abs(sg-expect))<1e-11
    # Choi J = sum_i E_i^T tensor sigma_i is manifestly separable,
    # positive semidefinite, and trace-preserving.
    choi=sum(np.kron(effects[i].T,sigmas[i]) for i in range(40))
    choi_error=max(0.,-float(np.linalg.eigvalsh(choi).min()))
    TP=np.trace(choi.reshape(4,9,4,9),axis1=1,axis2=3)
    trace_error=float(np.max(abs(TP-np.eye(4))))
    assert choi_error<1e-12 and trace_error<1e-12
    # The channel remains injective as a REAL density-operator linear
    # map: exactly HS-isotropic on all 15 ququart traceless generators.
    unit=[]
    for k in range(1,4):
        H=np.zeros((4,4),complex)
        for j in range(k):H[j,j]=1
        H[k,k]=-k
        unit.append(H/math.sqrt(k*(k+1)))
    for i,j in itertools.combinations(range(4),2):
        H=np.zeros((4,4),complex)
        H[i,j]=H[j,i]=1/math.sqrt(2)
        unit.append(H)
        H=np.zeros((4,4),complex)
        H[i,j]=-1j/math.sqrt(2)
        H[j,i]=1j/math.sqrt(2)
        unit.append(H)
    assert len(unit)==15
    def E(channel_input):
        probs=np.array([np.trace(eff@channel_input) for eff in effects])
        return np.einsum("i,ijk->jk",probs,sigmas)
    outputs=np.array([E(H) for H in unit])
    opgram=np.real(np.einsum("iab,jba->ij",outputs,outputs))
    isotropic_error=float(np.max(abs(opgram-np.eye(15)/225)))
    assert isotropic_error<1e-11
    assert np.linalg.matrix_rank(opgram,tol=1e-10)==15
    return {
      "status":"PASS",
      "Weyl_operators":81,"nontrivial_Weyl_operators":80,
      "sample_isometries":3,
      "physical_entanglement_breaking_CPTP_bridge_built":True,
      "bridge_measurement":"40 Witting informationally complete effects P_i/10",
      "bridge_preparation":"40 rank-three two-qutrit Pauli +1 eigenspace states Pi_i/3",
      "Choi_positive_semidefinite_error":choi_error,
      "Choi_trace_preserving_error":trace_error,
      "output_Pauli_state_Gram":"offdiag 1/9, diagonal 1/3",
      "injective_on_full_15dim_traceless_ququart_sector":True,
      "HS_isotropic_tracezero_contraction_factor":1/15,
      "max_15dim_HS_isotropy_Gram_error":isotropic_error,
      "entanglement_breaking_warning":"The channel is CPTP, informationally injective but measure-and-prepare: no entanglement survives and no CPTP exact inverse exists.",
      "universal_Weyl_twirl":"(1/81)sum_W W P W^dagger = rank(P)/9 * I_9",
      "rank_four_all_81_average_leakage":5/9,
      "rank_four_nonidentity_average_leakage":9/16,
      "rank_four_40projective_class_average_leakage":9/16,
      "exact_no_go":"No rank-4 invariant code subspace under full two-qutrit Weyl group; projective incidence equivalence is not a Weyl-covariant C4->C9 isometry.",
      "independent_numeric_certificates":examples
    }

def selector_front(rays,supports,iso,chart_edges):
    """Minimal source multiplicity and entropic 9-vs-36 vacuum-selection obstruction."""
    members=[frozenset(x for x in range(45) if p in supports[x]) for p in range(40)]
    assert set(map(len,members))=={9}
    orth,non=collections.Counter(),collections.Counter()
    omega=np.exp(2j*np.pi/3)
    max_ent_err=0.0
    for a,b in itertools.combinations(range(40),2):
        k=len(members[a]&members[b])
        is_orth=abs(np.vdot(rays[a],rays[b]))<1e-9
        (orth if is_orth else non)[k]+=1
    assert orth=={3:240} and non=={1:540}
    entropy=collections.Counter()
    for z,S in enumerate(supports):
        prob=np.array([abs(np.vdot(rays[i],rays[0]))**2/2 for i in sorted(S)])
        assert abs(sum(prob)-1)<1e-12
        H=-sum(x*math.log2(x) for x in prob if x>1e-12)
        lab="contains_source" if 0 in S else "does_not_contain_source"
        target=(0.5+0.5*math.log2(6)) if lab=="contains_source" else math.log2(6)
        max_ent_err=max(max_ent_err,abs(H-target))
        entropy[lab]+=1
    assert entropy=={"contains_source":9,"does_not_contain_source":36}
    assert max_ent_err<1e-11, max_ent_err
    # The externally chosen pair of nonorthogonal projective input sources
    # uniquely selects one chart via the simple source-dependent potential.
    a,b=next((a,b) for a,b in itertools.combinations(range(40),2)
             if abs(np.vdot(rays[a],rays[b]))>1e-9)
    minimizers=members[a]&members[b]
    assert len(minimizers)==1
    return {
       "status":"PASS",
       "single_Witting_source_compatible_charts":9,
       "single_source_other_charts":36,
       "chart_entropy_contains_source_bits":0.5+0.5*math.log2(6),
       "chart_entropy_other_bits":math.log2(6),
       "max_chart_entropy_residual":max_ent_err,
       "orthogonal_source_pairs_3common_charts":240,
       "nonorthogonal_source_pairs_1common_chart":540,
       "minimal_explicit_2ray_selector":[a,b],
       "minimizer_chart":next(iter(minimizers)),
       "honest_interpretation":"This source-dependent two-ray potential externally breaks symmetry; no unforced PSp4(3)-invariant Hamiltonian can uniquely select a transitive 45-chart orbit."
    }

def memory_front():
    """Genuine multitime quantum-memory benchmark beyond static Choi labels."""
    omega=np.exp(2j*np.pi/3)
    Z=np.diag([omega**i for i in range(3)])
    X=np.roll(np.eye(3),1,axis=0)
    bases=[]
    for U in (Z,X,X@Z,X@Z@Z):
        _,vectors=np.linalg.eig(U)
        assert np.max(abs(vectors.conj().T@vectors-np.eye(3)))<1e-10
        bases.append([vectors[:,j] for j in range(3)])
    states=[v for basis in bases for v in basis]
    for i,j in itertools.combinations(range(4),2):
        for u in bases[i]:
            for v in bases[j]:
                assert abs(abs(np.vdot(u,v))**2-1/3)<1e-12
    P=[np.outer(v,v.conj()) for v in states]
    swap=np.zeros((9,9),complex)
    for a,b in itertools.product(range(3),repeat=2):
        swap[3*b+a,3*a+b]=1
    design=sum(np.kron(proj,proj) for proj in P)/12
    assert np.max(abs(design-(np.eye(9)+swap)/12))<1e-12
    zero=np.diag([1.,0.,0.])
    # Causal break at middle slot: discard/reprepare S, leave memory E.
    def partial_S(rho):
        return np.einsum("abac->bc",rho.reshape(3,3,3,3))
    def partial_E(rho):
        return np.einsum("abcb->ac",rho.reshape(3,3,3,3))
    quantum=[]; classical=[]; markov=[]
    for state in P:
        initial=np.kron(state,zero)
        after=swap@initial@swap
        env=partial_S(after)
        broken=np.kron(zero,env)
        final=swap@broken@swap
        output=partial_E(final)
        assert np.max(abs(output-state))<1e-12
        quantum.append(float(np.trace(output@state).real))
        classical.append(float(np.trace(np.diag(np.diag(state))@state).real))
        markov.append(float(np.trace(zero@state).real))
    assert abs(np.mean(quantum)-1)<1e-12
    assert abs(np.mean(classical)-0.5)<1e-12
    assert abs(np.mean(markov)-1/3)<1e-12
    return {
      "status":"PASS",
      "qutrit_MUB_probe_bases":4,
      "qutrit_projective_2design_probe_states":12,
      "two_SWAPS_store_and_restore_after_system_causal_break":True,
      "ideal_quantum_memory_average_fidelity":float(np.mean(quantum)),
      "measure_prepare_best_2design_average_fidelity":0.5,
      "classical_Zdephased_memory_average_fidelity":float(np.mean(classical)),
      "reset_no_memory_average_fidelity":float(np.mean(markov)),
      "quantum_memory_witness":"12-state average survival >1/2 rules out entanglement-breaking temporal input->output transmission, if calibrated preparations and fidelity measurements are trusted.",
      "caveat":"Synthetic SWAP-causal-break model only; not a real single-photon self-entanglement or gravity experiment. A causal break must be instrumentally verified."
    }

def site_front():
    """Retrieve full live static mirror site map, not the unavailable legacy host."""
    import requests
    from html.parser import HTMLParser
    from urllib.parse import urljoin,urlparse
    url="https://m759.github.io/map.html"
    page=requests.get(url,timeout=20)
    assert page.status_code==200 and b"Site Map" in page.content
    class Links(HTMLParser):
        def __init__(self):
            super().__init__();self.hrefs=[]
        def handle_starttag(self,tag,attrs):
            if tag=="a":
                self.hrefs.extend(v for k,v in attrs if k=="href" and v)
    parser=Links();parser.feed(page.text)
    urls=[]
    for href in parser.hrefs:
        href=href.strip()
        if href.startswith("#") or href.startswith("mailto:"):continue
        full=urljoin(url,href)
        if full not in urls:urls.append(full)
    assert len(urls)>100,len(urls)
    archive={
      "status":"PASS",
      "original":"https://finitegeometry.org/sc/map.html",
      "original_status":"timed out from ChatGPT web and Windows requests (prior pass)",
      "working_mirror":url,
      "total_distinct_link_targets":len(urls),
      "internal_links":[u for u in urls if urlparse(u).netloc=="m759.github.io"],
      "thirdparty_links":[u for u in urls if urlparse(u).netloc!="m759.github.io"],
      "Zenodo_zip_archive":"https://zenodo.org/records/1038121",
      "canonical_GitHub_source":"https://github.com/finite-geometry/galois",
      "note":"A complete link index, not a claim of having read every external paper or confirmed all links."
    }
    return archive

def main():
    rays,wf4=old.witting_rays()
    iso=sorted({old.norm4(q) for q in itertools.product(range(4),repeat=4)
                if any(q) and old.herm4(q,q)==0})
    supports=[frozenset(i for i,u in enumerate(wf4) if herm(z,u)==0) for z in iso]
    assert len(iso)==45 and all(len(s)==8 for s in supports)
    mapping={int(k):int(v) for k,v in old.analyze()[
                      "ray_index_to_F3_projective_point_index"].items()}
    # Lines computed from first principles, twice for consistency.
    ids={x:i for i,x in enumerate(iso)}
    lines=sorted({tuple(sorted(ids[gf4_point(plus4(x,y,a,b))]
                     for a,b in itertools.product(range(4),repeat=2) if a or b))
                  for x,y in itertools.combinations(iso,2) if herm(x,y)==0})
    # remove projective scalar duplicated entries
    lines=sorted({tuple(sorted(set(line))) for line in lines})
    f1,graph,schedules=first_front(rays,wf4,iso,lines,supports)
    print("FRONT1",len(schedules),"Schlaefli packets",flush=True)
    f2=group_front(wf4,iso,supports,graph,schedules,mapping)
    print("FRONT2",f2["projective_GF4_Hermitian_group_order"],flush=True)
    f3=optical_front(rays,wf4,iso,supports,schedules)
    print("FRONT3",f3["max_nai_unity_error"],flush=True)
    f4=channel_front(rays,mapping)
    print("FRONT4",f4["rank_four_nonidentity_average_leakage"],flush=True)
    f5=selector_front(rays,supports,iso,graph)
    print("FRONT5",f5["minimal_explicit_2ray_selector"],flush=True)
    f6=memory_front()
    print("FRONT6",f6["ideal_quantum_memory_average_fidelity"],flush=True)
    f7=site_front()
    print("SITEMAP",f7["total_distinct_link_targets"],flush=True)
    obj={"status":"PASS",
         "f1_Hermitian27Schlaefli_five_chart_partition":f1,
         "f2_full_projective_exceptional_group_equivariance":f2,
         "f3_Naimark_27_five_setting_POVMs":f3,
         "f4_quantitative_Weyl_covariant_channel_obstruction":f4,
         "f5_two_source_chart_selector":f5,
         "f6_multitime_quantum_memory_witness":f6,
         "f7_restored_finitegeometry_site_index":f7,
         "original_study_prior_art":"GQ(4,2), W(3,3), 45 frames, E8 reduction, full 25920 symmetry, ququart 2-design known; new synthesis/certificates here must not be confused with new physical laws."}
    OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS ALL SEVEN FRONTS",OUT,flush=True)
    return obj

if __name__=="__main__":main()
