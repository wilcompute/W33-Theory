#!/usr/bin/env python3
"""Nov 1 W33 five-front / three independent physics probes.

Finite stipulated geometries and quantum channels; not TOE or experiments.
Builds on exact Oct-31 W33 server campaign, no local-desktop dependency.
"""
from __future__ import annotations
import json, math, sys, hashlib, itertools
from pathlib import Path
from collections import Counter
import numpy as np
import networkx as nx
from scipy.linalg import null_space,expm
from scipy.sparse.linalg import LinearOperator,eigsh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261031_eight_front_server_campaign as old
import w33_20261031_server_five_fronts as core
OUT=ROOT/'data'/'w33_20261101_five_plus_three.json'


def sparse_optical():
    D,lines,flags=old.incidence()
    graph=nx.Graph()
    graph.add_nodes_from(range(80))
    for i,(p,line) in enumerate(flags):graph.add_edge(p,40+line,edge_index=i)
    assert nx.is_connected(graph)
    assert min(len(c)for c in nx.minimum_cycle_basis(graph))==8
    assert all(len(c)>=8 for c in nx.minimum_cycle_basis(graph))
    tree=nx.bfs_tree(graph,source=0)
    assert tree.number_of_edges()==79
    spanning=set(graph[a][b]['edge_index']for a,b in tree.edges())
    chords=[i for i in range(160) if i not in spanning]
    assert len(chords)==81
    T=nx.Graph();T.add_nodes_from(range(80));T.add_edges_from(tree.edges())
    Z=np.zeros((160,81),dtype=np.int64)
    for j,edge in enumerate(chords):
        p,l=flags[edge];end=40+l
        Z[edge,j]=1
        path=nx.shortest_path(T,p,end)
        for a,b in zip(path,path[1:]):
            k=graph[a][b]['edge_index']
            Z[k,j]=(-1 if a<40 else 1)
    assert np.array_equal(D@Z,np.zeros((80,81),dtype=int))
    assert np.array_equal(Z[chords,:],np.eye(81,dtype=int))
    lengths=np.count_nonzero(Z,axis=0)
    assert np.all(lengths==8)
    Q=np.linalg.qr(Z.astype(float),mode='reduced')[0]
    assert np.linalg.norm(Q.T@Q-np.eye(81))<1e-10
    assert np.linalg.norm(D@Q)<1e-10
    A=Q.copy();gates=[]
    for col in range(81):
        for row in range(159,col,-1):
            a,b=A[row-1,col],A[row,col]
            if abs(b)<1e-11:continue
            r=math.hypot(a,b);c,s=a/r,b/r
            x=A[row-1,col:].copy();y=A[row,col:].copy()
            A[row-1,col:]=c*x+s*y
            A[row,col:]=-s*x+c*y
            gates.append((row-1,row,c,s))
    diag=np.diag(A[:81,:81]);assert np.linalg.norm(A[81:])<1e-8
    assert np.linalg.norm(A[:81,:81]-np.diag(diag))<1e-8
    R=np.zeros((160,81));R[:81]=np.diag(np.sign(diag))
    for i,j,c,s in reversed(gates):
        x=R[i].copy();y=R[j].copy()
        R[i]=c*x-s*y;R[j]=s*x+c*y
    error=float(np.linalg.norm(R-Q))
    assert error<1e-9
    assert len(gates)==5346
    blob=np.array(gates,dtype=np.float64)
    return dict(status='PASS_81_GIRTH8_BASIS_AND_5346_ADJACENT_ROTATION_ENCODER',
       logical_modes=81,rails=160,girth=8,number_independent_girth_cycles=81,
       fundamental_cycle_supports=int(np.count_nonzero(Z)),
       gate_count=5346,prior_gate_count=8416,improvement_fraction=1-5346/8416,
       reconstruction_error=error,gate_list_SHA256=hashlib.sha256(blob.tobytes()).hexdigest(),
       first_five_gates=[list(map(float,g))for g in gates[:5]],
       boundary='Deterministic real nearest-neighbor rotation count; physical chip depth, crosstalk, calibrations and encoder loss unmeasured.')


def single_photon_loss_nogo():
    D,C=old.projector_exact();P=C.astype(float)/320
    assert np.linalg.norm(P@P-P)<1e-12
    j=0;v=P[:,j];amplitude=math.sqrt(P[j,j])
    psi_max=v/amplitude
    rng=np.random.default_rng(1011)
    u=P@rng.normal(size=160)
    u-=np.vdot(psi_max,u)*psi_max;u/=np.linalg.norm(u)
    assert abs(u[j])<1e-12
    assert abs(np.vdot(psi_max,u))<1e-12
    max_prob=abs(psi_max[j])**2;min_prob=abs(u[j])**2
    assert abs(max_prob-81/160)<1e-12 and min_prob<1e-20
    # E_j=|vac><j|; P E_j†E_j P is rank1 with nonzero eigenvalue Pjj.
    K=P@np.diag([1]+[0]*159)@P
    assert abs(np.trace(K)-81/160)<1e-12
    assert np.linalg.norm(K@u)<1e-12
    assert abs(psi_max@K@psi_max-81/160)<1e-12
    return dict(status='PASS_NO_SINGLE_RAIL_LOSS_KNILL_LAFLAMME_FOR_ONE_PHOTON_81CODE',
        rail=0,loss_probability_max=max_prob,loss_probability_min=min_prob,
        restricted_loss_observable_rank=1,
        theorem='P|j><j|P cannot equal cP for rank(P)=81 since Pjj=81/160>0; detecting which rail is lost leaks logical information. Vacuum erasure of the only photon is not correctable within single-photon 160-rail encoding.',
        nuance='This does not forbid multi-photon quantum error correcting codes or erasure flags with an extra intact encoded carrier.')

def strange_verification_tomography():
    """Four qutrit stabilizer MUB measurements certify Strange identity independently."""
    w=np.exp(2j*np.pi/3)
    X=np.roll(np.eye(3),1,axis=0)
    Z=np.diag([1,w,w*w]);bases=[np.eye(3,dtype=complex)]
    for k in range(3):
        U=X@np.linalg.matrix_power(Z,k)
        val,V=np.linalg.eig(U)
        V=V/np.linalg.norm(V,axis=0,keepdims=True)
        assert np.linalg.norm(V.conj().T@V-np.eye(3))<1e-12
        bases.append(V)
    for a,b in itertools.combinations(range(4),2):
        assert np.max(abs(abs(bases[a].conj().T@bases[b])**2-1/3))<1e-12
    S=np.array([0,1,-1],complex)/math.sqrt(2)
    E=np.array([0,1,1],complex)/math.sqrt(2)
    # Stipulated heralded output with opposite-parity false positives + vacuum-rail leakage.
    rho=(.93*np.outer(S,S.conj())+.05*np.outer(E,E.conj())
          +.02*np.diag([1,0,0]))
    assert abs(np.trace(rho)-1)<1e-12
    F=float(np.vdot(S,rho@S).real)
    # Complete MUB linear frame: sum_b,k p(b,k)|b,k><b,k| = rho+I.
    q=[];prob=[]
    for V in bases:
        q.append(np.abs(V.conj().T@S)**2)
        prob.append(np.real(np.diag(V.conj().T@rho@V)))
    assert abs(sum(float(np.dot(p,v))for p,v in zip(prob,q))-1-F)<1e-12
    rng=np.random.default_rng(11126)
    M=6000;mislabel=.03
    confusion=(1-mislabel)*np.eye(3)+mislabel*(np.ones((3,3))-np.eye(3))/2
    inv=np.linalg.inv(confusion)
    observed=[];corrected=[];trace_f=[]
    for p,v in zip(prob,q):
        samples=rng.multinomial(M,confusion@p)/M
        observed.append(float(np.dot(v,samples)))
        corrected.append(float(np.dot(v,inv@samples)))
        trace_f.append(v.tolist())
    estimate=sum(corrected)-1
    biased=sum(observed)-1
    # Union/Hoeffding range bound with each measured outcome assigned corrected score.
    ranges=[np.ptp(inv.T@v)for v in q]
    delta=math.sqrt(math.log(2/.01)*sum(r*r for r in ranges)/(2*M))
    assert abs(estimate-F)<delta
    # Analytic single-shot no-QND certification: repeat over an ensemble of prepared samples.
    return dict(status='PASS_FOUR_STABILIZER_MUB_STRANGE_TOMOGRAPHY_WITH_CALIBRATED_READOUT',
        number_stabilizer_basis_settings=4,shots_per_setting=M,total_shots=4*M,
        readout_symmetric_mislabel_probability=mislabel,true_Strange_fidelity=F,
        raw_uncalibrated_fidelity=biased,readout_corrected_fidelity=estimate,
        conservative_99pct_Hoeffding_halfwidth=delta,
        MUB_trace_reconstruction_error=abs(sum(float(np.dot(p,v))for p,v in zip(prob,q))-1-F),
        boundary='Ensemble destructive tomography in four stabilizer bases; not QND verification of an individual surviving photon. Detector confusion must be independently calibrated; error bars reflect sampling, not model uncertainty.')


def quantum_120_chain():
    A=core.ADJ;n=120;J,K=1.,2.
    epsilon=2*J-4*K/3
    labels=np.arange(n);dirs=labels//3
    pair=np.where(labels[:,None]==labels[None,:],0.,
        np.where(dirs[:,None]==dirs[None,:],3*J,
            np.where(A[dirs[:,None],dirs[None,:]]==1,2*J,epsilon)))
    assert np.allclose(pair,pair.T)
    rows=[];h=.5
    for N in (2,3):
        shape=(n,)*N;d=n**N
        diag=np.zeros(shape)
        for k in range(N-1):
            left=np.arange(n).reshape((1,)*k+(n,)+(1,)*(N-k-1))
            right=np.arange(n).reshape((1,)*(k+1)+(n,)+(1,)*(N-k-2))
            diag+=pair[left,right]
        def mv(v):
            X=v.reshape(shape)
            Y=diag*X
            for axis in range(N):Y=Y-h/n*np.sum(X,axis=axis,keepdims=True)
            return Y.ravel()
        H=LinearOperator((d,d),matvec=mv,dtype=float)
        vals=np.sort(eigsh(H,k=2,which='SA',tol=1e-7,maxiter=700,return_eigenvectors=False))
        assert vals[1]>vals[0]
        rows.append({'open_chain_length':N,'local_dimension':n,'Hilbert_dimension':d,
                     'transverse_h':h,'ground_energy':float(vals[0]),'excitation_gap':float(vals[1]-vals[0]),
                     'ground_energy_per_site':float(vals[0]/N)})
    assert abs(rows[0]['excitation_gap']-.35541122)<1e-5
    assert abs(rows[1]['excitation_gap']-.28203549)<1e-5
    return dict(status='PASS_FULL_120_CLOCK_THREE_SITE_1728000_DIMENSION_QUANTUM_LANCZOS',
        rows=rows,operator='Open N-site sum nearest-neighbor native 120-label pair energy and -0.5 per-site rank-one uniform mixing',
        scope='N=2 and N=3 finite quantum chains, not an MPS thermodynamic limit; real microscopic Hamiltonian externally stipulated.')


def clock_zero_temperature_entropy():
    # Dominant noncommuting tick adjacency N: 120 x 120, eigenvalues 81, -9, +9, 0.
    A=core.ADJ
    Nc=np.kron(np.ones((40,40),dtype=np.int64)-np.eye(40,dtype=np.int64)-A,np.ones((3,3),dtype=np.int64))
    assert np.all(Nc.sum(axis=1)==81)
    eig=np.linalg.eigvalsh(Nc)
    theory=np.sort(np.array([81.]+[-9.]*24+[9.]*15+[0.]*80))
    assert np.max(abs(eig-theory))<1e-11
    rows=[]
    for N in (2,3,4,5,6):
        count=int(81**N+24*(-9)**N+15*9**N)
        assert count>0
        if N<=3:
            mat=np.linalg.matrix_power(Nc,N)
            assert int(np.trace(mat))==count
        rows.append(dict(ring_sites=N,exact_ground_configurations=count,per_site_entropy=math.log(count)/N))
    return dict(status='PASS_120_TICK_ZERO_TEMPERATURE_CLOSED_RING_COLORING_TRACE',
        noncommuting_graph_spectrum={'81':1,'-9':24,'9':15,'0':80},
        number_ground_configurations_formula='81^N +24*(-9)^N +15*9^N for N>=2',
        residual_entropy_density='ln(81)',zero_temperature_correlation_length='1/ln(9)',
        rings=rows,scope='Classical zero-temperature 1D nearest-neighbor model, not a dynamic mechanism for emergent time or gravity.')

def correlated_erasure_edge():
    """Exact known-erasure success under local two-neighbor burst faults."""
    rows=[]
    for p_tick in (.001,.005,.01):
        q=1-(1-p_tick)**26
        independent=(1-q)**3+3*q*(1-q)**2
        threshold=(independent-(1-q))/(independent-2*(1-q)/3)
        assert 0<threshold<1
        for burst in (0.,.01,.05,.1,.2,.3):
            # Burst destroys either pair (rail0,rail1) or (rail1,rail2);
            # otherwise independent per-carrier erasures q.  Bare carrier
            # uniformly picked among three positions, affected with prob 2/3.
            coded=(1-burst)*independent
            bare=(1-2*burst/3)*(1-q)
            rows.append(dict(per_tick_erasure=p_tick,per_active_rail_erasure=q,
                adjacent_pair_burst=burst,erasure_code_success=coded,
                bare_uniform_rail_success=bare,encoded_gain=coded-bare))
        # threshold advantage when bursts strike two of three rails
        assert abs((1-threshold)*independent - (1-2*threshold/3)*(1-q))<1e-12
    return dict(status='PASS_FLOQUET_THREE_QUTRIT_BURST_ERASURE_FAILURE_THRESHOLD',
        number_edge_carriers=3,native_ticks_per_carrier=26,
        burst_model='With probability b, a uniformly chosen nearest-neighbor pair is erased, otherwise three independent per-carrier erasures q=1-(1-p_tick)^26; bare rail sampled uniformly among three.',
        advantage_loss_thresholds=[{'p_tick':p,'critical_burst_probability':
          (1-(1-p)**26 and ((1-3*(1-(1-p)**26)**2+2*(1-(1-p)**26)**3)-(1-p)**26)/
          ((1-3*(1-(1-p)**26)**2+2*(1-(1-p)**26)**3)-2*(1-p)**26/3))} for p in (.001,.005,.01)],
        rows=rows,
        scope='Independent + adjacent-pair flagged-erasure toy; no encoding/decoding noise, coherence, or network-level error threshold.')


def nonabelian_lorentz_curvature():
    """SO+(1,3) noncompact Wilson plaquette gauge covariance, and stability no-go."""
    eta=np.diag([-1.,1.,1.,1.]);K=[];J=[]
    for i in (1,2,3):
        a=np.zeros((4,4));a[0,i]=a[i,0]=1.;K.append(a)
    for i,j in ((1,2),(1,3),(2,3)):
        a=np.zeros((4,4));a[i,j]=1.;a[j,i]=-1.;J.append(a)
    gen=K+J
    assert all(np.linalg.norm(a.T@eta+eta@a)<1e-14 for a in gen)
    # All [so(1,3),so(1,3)] bracket Lie algebra closure.
    v=np.stack([g.flatten()for g in gen],axis=1)
    max_closure=0
    for A,B in itertools.combinations(gen,2):
        C=A@B-B@A;coeff=np.linalg.lstsq(v,C.flatten(),rcond=None)[0]
        max_closure=max(max_closure,float(np.linalg.norm(v@coeff-C.flatten())))
    assert max_closure<1e-13
    rng=np.random.default_rng(20261101);L=2
    coords=list(itertools.product(range(L),repeat=3))
    def nxt(x,mu):return tuple((x[i]+int(i==mu))%L for i in range(3))
    U={}
    for x in coords:
        for mu in range(3):
            co=rng.normal(scale=.12,size=6)
            U[x,mu]=expm(sum(float(c)*g for c,g in zip(co,gen)))
    G={x:expm(sum(float(c)*g for c,g in zip(rng.normal(scale=.21,size=6),gen))) for x in coords}
    assert max(np.linalg.norm(g.T@eta@g-eta) for g in G.values())<1e-12
    Up={(x,mu):G[nxt(x,mu)]@U[x,mu]@np.linalg.inv(G[x])for x in coords for mu in range(3)}
    def W(links,x,a,b):
        # Loop x -> x+a -> x+a+b -> x+b -> x
        return np.linalg.inv(links[x,b])@np.linalg.inv(links[nxt(x,b),a])@links[nxt(x,a),b]@links[x,a]
    max_trace=0;max_cov=0
    wilson=0.;other=0.
    for x in coords:
        for a,b in itertools.combinations(range(3),2):
            oldW=W(U,x,a,b);newW=W(Up,x,a,b)
            max_trace=max(max_trace,abs(np.trace(oldW)-np.trace(newW)))
            max_cov=max(max_cov,float(np.linalg.norm(newW-G[x]@oldW@np.linalg.inv(G[x]))))
            wilson+=np.trace(2*np.eye(4)-oldW-np.linalg.inv(oldW)).real
            other+=np.trace(2*np.eye(4)-newW-np.linalg.inv(newW)).real
    assert max_cov<1e-10 and max_trace<1e-10 and abs(wilson-other)<1e-10
    xfield={x:rng.normal(size=4) for x in coords}
    def matter(links,frames):
        return sum(float((frames[nxt(x,mu)]-links[x,mu]@frames[x])@eta@
                  (frames[nxt(x,mu)]-links[x,mu]@frames[x]))
                   for x in coords for mu in range(3))
    frame_other={x:G[x]@xfield[x]for x in coords}
    mf=abs(matter(U,xfield)-matter(Up,frame_other))
    assert mf<1e-10
    boost=[]
    for theta in (0.,1.,2.,4.,8.):
        Wb=expm(theta*K[0])
        val=float(np.trace(2*np.eye(4)-Wb-expm(-theta*K[0])).real)
        expected=4-4*math.cosh(theta)
        assert abs(val-expected)<1e-8*max(1,abs(expected))
        boost.append(dict(rapidity=theta,noncompact_Wilson_weight=val))
    return dict(status='PASS_SO13_NONABELIAN_PLAQUETTE_WARD_AND_NONCOMPACT_INSTABILITY',
        spatial_lattice=[2,2,2],lie_bracket_closure_error=max_closure,
        gauge_plaquette_covariance_max_error=max_cov,gauge_trace_max_error=max_trace,
        gauge_matter_action_error=mf,
        Wilson_energy_boost_sequence=boost,
        no_go='Natural trace Wilson term 8-Tr(U_p)-Tr(U_p^-1) =4-4cosh(rapidity) for a boost, unbounded below. Gauge covariance is not a positive Hamiltonian or Einstein constraint closure.',
        scope='Externally postulated 3D lattice Lorentz gauge action and matter vector. No invertible tetrad, second-class constraints, spin-two propagation or ADM closure.')


def block_correlated_phase_noise():
    """Exact input-independent code survival for per-line common-mode phase noise."""
    D,C=old.projector_exact();P=C.astype(float)/320
    _,lines,flags=old.incidence()
    assert all(flags[4*l+i][1]==l for l in range(40)for i in range(4))
    blocks=[]
    for l in range(40):
        idx=list(range(4*l,4*l+4))
        B=P[np.ix_(idx,idx)]
        exact=(108*np.eye(4)-27*np.ones((4,4)))/160
        assert np.linalg.norm(B-exact)<1e-14
        blocks.append(B)
    # For zero-sum code amplitudes on each line: B v=(27/40) v.
    K=27/40
    Q=null_space(D.astype(float))
    rng=np.random.default_rng(4816)
    a=rng.normal(size=81)+1j*rng.normal(size=81);a/=np.linalg.norm(a)
    psi=Q@a
    for l in range(40):assert abs(sum(psi[4*l:4*l+4]))<1e-12
    local=0
    for l,B in enumerate(blocks):
        v=psi[4*l:4*l+4]
        local+=float(np.vdot(v,B@v).real)
    assert abs(local-K)<1e-12
    rows=[]
    for sigma in (0.,.35,.7,1.5):
        expected=math.exp(-sigma*sigma)+(1-math.exp(-sigma*sigma))*K
        iid=math.exp(-sigma*sigma)+(1-math.exp(-sigma*sigma))*81/160
        phases=rng.normal(scale=sigma,size=(450,40))
        arr=np.exp(1j*np.repeat(phases,4,axis=1))*psi[None,:]
        # Projection norm via orthonormal code basis avoids dense 160x160 matrix.
        observed=float(np.mean(np.sum(abs(arr@Q)**2,axis=1)))
        assert abs(observed-expected)<.025
        rows.append(dict(sigma=sigma,exact_line_correlated_survival=expected,
                         MonteCarlo_survival=observed,independent_rail_survival=iid))
    return dict(status='PASS_W33_LINE_COMMON_MODE_PHASE_NOISE_UNIVERSAL_27OVER40',
        rail_block_size=4,number_line_blocks=40,
        projected_each_line_diagonal='81/160',projected_each_line_offdiagonal='-27/160',
        block_code_eigenvalue='27/40',phase_noise_survival_formula=
          'exp(-sigma^2)+(1-exp(-sigma^2))*27/40 for any normalized 81D code state',
        original_independent_rail_formula=
          'exp(-sigma^2)+(1-exp(-sigma^2))*81/160',rows=rows,
        scope='Exactly line-correlated Gaussian phase drift, not arbitrary correlated stochastic noise, quantum error correction or physical passive implementation.')

def build():
    tasks={
        '01_optical_81_shortest_cycles_sparse_compiler':sparse_optical,
        '02_QND_strange_fidelity_stabilizer_tomography':strange_verification_tomography,
        '03_full_120_tick_three_site_quantum_chain':quantum_120_chain,
        '04_Floquet_correlated_burst_erasure':correlated_erasure_edge,
        '05_Lorentz_nonAbelian_curvature_gauge_and_stability':nonabelian_lorentz_curvature,
        '06_outside_single_photon_rail_loss_KL_nogo':single_photon_loss_nogo,
        '07_outside_full120_zero_temperature_entropy':clock_zero_temperature_entropy,
        '08_outside_line_correlated_phase_noise':block_correlated_phase_noise
    }
    result={}
    for k,func in tasks.items():
        v=func();result[k]=v;print(k,v['status'],flush=True)
    return dict(schema='w33.20261101.five_plus_three.v1',
        based_on='3e77fafcfa77cf228dd74438d18b448de8be4509',results=result,
        scope='Finite mathematical models and error budgets; no physical TOE or unobserved particle-physics claims.')

if __name__=='__main__':
    data=build();OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print('WROTE',OUT,flush=True)
