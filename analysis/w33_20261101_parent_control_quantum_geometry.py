"""Parent controls, rigorous error bounds, and two quantum-geometry audits.

Generic interferometer synthesis, spectral perturbation theory, Markov traces
and real spectral data are established methods, applied to explicit native maps.
"""
import pathlib,sys,json,itertools,math
import numpy as np
from scipy.linalg import expm
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261031_tick_loop_rigidity import PI
from w33_pass12055_microscopic_tick_model import X,Z,w

def native_gates():
    I=np.eye(3);F=np.array([[w**(i*j) for j in range(3)] for i in range(3)])/np.sqrt(3);S=np.diag([1,1,w])
    SUM=np.zeros((9,9))
    for i,j in itertools.product(range(3),repeat=2):SUM[3*i+(i+j)%3,3*i+j]=1
    return dict(X1=np.kron(X,I),Z1=np.kron(Z,I),X2=np.kron(I,X),Z2=np.kron(I,Z),
                F1=np.kron(F,I),F2=np.kron(I,F),S1=np.kron(S,I),S2=np.kron(I,S),SUM=SUM)

def parent_data():
    tetra=json.loads((ROOT/'data/w33_20261031_chiral_tetrahedron_strange_bridge.json').read_text())
    loop=json.loads((ROOT/'data/w33_20261031_tick_loop_rigidity.json').read_text())
    labels=tetra['canonical_native_ticks'];Q=np.eye(9)-sum(PI[a] for a in labels)/2
    return tetra,loop,labels,Q

def control(tetra,loop,labels,Q):
    gs=native_gates();perms=loop['Clifford_generator_permutations'];root=tuple(sorted(labels))
    words={root:[]};matrices={root:np.eye(9)};queue=[root]
    for t in queue:
        for name,p in perms.items():
            u=tuple(sorted(p[i] for i in t))
            if u not in words:words[u]=words[t]+[name];matrices[u]=gs[name]@matrices[t];queue.append(u)
    assert len(words)==810
    errors=[]
    for t in queue:
        U=matrices[t];Qt=np.eye(9)-sum(PI[i] for i in t)/2
        errors.append(float(np.max(abs(Qt-U@Q@U.conj().T))))
    assert max(errors)<1e-11
    frame=json.loads((ROOT/'data/w33_20261101_frame_tomography_octahedron.json').read_text())['tomography']['frame_outcome_indices'][0]
    ts=tetra['oriented_tetrahedra']
    Hs=np.array([sum(PI[a] for a in ts[i])/2 for i in frame])
    gram=np.einsum('aij,bji->ab',Hs,Hs).real
    assert np.max(abs(np.linalg.eigvalsh(gram)-np.array([0]*9+[2.25]*80+[360])))<1e-9
    V=np.array([[1,0,0],[0,1/np.sqrt(2),1/np.sqrt(2)],[0,1/np.sqrt(2),-1/np.sqrt(2)]],complex)
    S=np.array([[0,0,0],[0,.5,-.5],[0,-.5,.5]],complex)
    samples=[]
    for t in (0.,math.pi/6,math.pi/2,math.pi,1.234,2*math.pi):
        U=np.exp(-1j*t)*V@np.diag([1,1,np.exp(1j*t)])@V.conj().T
        exact=expm(-1j*t*(np.eye(3)-S));assert np.max(abs(U-exact))<1e-12
        moved=U@Z@U.conj().T
        assert abs(abs(moved[1,2])-math.sqrt(3)*abs(math.sin(t))/2)<1e-12
        samples.append(dict(time=t,compiled_error=float(np.max(abs(U-exact))),Z_image_offdiagonal=float(abs(moved[1,2]))))
    thermal=[]
    parity=np.eye(3)[:,[0,2,1]]
    phase=[D@parity@D.conj().T for D in [np.linalg.matrix_power(X,q)@np.linalg.matrix_power(Z,p) for q,p in itertools.product(range(3),repeat=2)]]
    for beta in (0.,.3,math.log(2),1.,2.,5.,10.):
        r=math.exp(-beta);rho=(S+r*(np.eye(3)-S))/(1+2*r);F=1/(1+2*r)
        W=np.array([np.trace(A@rho).real/3 for A in phase]);mana=math.log(abs(W).sum())
        assert abs(mana-max(0.,math.log((1+4*F)/3)))<1e-12
        thermal.append(dict(beta=beta,ground_fidelity=F,Wigner_minimum=float(W.min()),mana=mana))
    return dict(status='PASS_ALL810_PARENT_CONTROLS',
        Clifford_words=[dict(ticks=t,word=words[t]) for t in sorted(words)],
        maximum_Clifford_word_length=max(map(len,words.values())),maximum_parent_transport_error=max(errors),
        exact_control_span_dimension=81,
        controllability='One continuous parent evolution plus native Clifford conjugations generates u(9): the90 parent Hamiltonians from any tomography frame have Gram eigenvalues360 once,9/4 eighty times,0 nine times, hence span all Herm9. Inverses use period2pi. This is supplied analog non-Clifford control, not braid-only universality or a gate-count/noise-efficiency theorem.',
        canonical_control='exp(-itH)=exp(-it)[I3 tensor V diag(1,1,exp(it)) Vdagger], H=I-Q, V balanced mixer of the active qutrit modes1,2.',
        native_control_cost='For each810 parent: its exported Clifford word, two balanced active-mode mixers and one relative phase, then inverse Clifford word. A coherent controlled operation must also retain the global exp(-it) phase reference.',
        Clifford_time_classification='Exactly t in pi Z, up to global phase. A Pauli image UZUdagger fixes the first basis rail, so if monomial it must be diagonal. Its (1,2) magnitude is sqrt3 |sin t|/2. At t in pi Z the operation is identity or parity, both Clifford.',
        time_samples=samples,thermal_controls=thermal,
        exact_thermal_magic_threshold='For supplied Gibbs cooling, F=1/(1+2exp(-beta)); Wigner negativity iff beta>log2. Mana=max(0,log((1+4F)/3)). Spectator is maximally mixed.',
        boundary='Ideal control compilation and a supplied bath/Hamiltonian, not device calibration or free stabilizer magic. Energy scale and temperature remain inputs. Known parity heralding and magic factories are credited in the companion report.')

def robustness(labels,Q):
    rng=np.random.default_rng(114810);samples=[];H=np.eye(9)-Q
    for angle in (.001,.01,.05,.1):
        moved=[]
        for a in labels:
            A=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9));A=(A+A.conj().T)/2;A/=np.linalg.norm(A,2)
            U=expm(1j*angle*A);moved.append(U@PI[a]@U.conj().T)
        eps=max(float(np.linalg.norm(P-PI[a],2)) for a,P in zip(labels,moved));eta=2*eps
        Hp=sum(moved)/2;e,V=np.linalg.eigh(Hp);P=V[:,:3]@V[:,:3].conj().T
        gap=float(e[3]-e[2]);distance=float(np.linalg.norm(P-Q,2))
        assert gap>=1-4*eps-1e-12 and distance<=eta/(1-eta)+1e-12
        original=np.trace(PI[labels[0]]@PI[labels[1]]@PI[labels[2]])
        new=np.trace(moved[0]@moved[1]@moved[2]);assert abs(new-original)<=9*eps+1e-12
        samples.append(dict(angle=angle,projector_error=eps,observed_cluster_gap=gap,
            certified_gap_lower=1-4*eps,cluster_projector_distance=distance,
            certified_projector_upper=eta/(1-eta),loop_trace_error=float(abs(new-original)),loop_error_upper=9*eps))
    energies=json.loads((ROOT/'data/w33_20261101_frame_tomography_octahedron.json').read_text())['energies']
    Delta=energies['tetrahedron_exact_gap'];C=36+144*math.sqrt(2)+36*math.sqrt(3)
    return dict(status='PASS_RIGOROUS_PARENT_AND_LOOP_ERROR_BOUNDS',
       projector_hypothesis='Four rank3 orthoprojectors with ||Ptilde_i-P_i||op <=epsilon; epsilon<1/4. Pair-energy bounds assume J,K>=0.',
       exact_bounds=['||Htilde-H||op<=2epsilon. The three-low/six-high cluster gap is at least1-4epsilon.',
         '||Qtilde-Q||op <=2epsilon/(1-2epsilon). Qtilde is the low cluster, not a promised exact common kernel.',
         '|Tr(Atilde Btilde Ctilde)-Tr(ABC)| <=9epsilon for rank3 orthoprojectors.',
         '|delta E_pair| <=(6J+12sqrt2 K)epsilon for the native alignment/current energy.',
         '|delta E_tetra| <=(36J+72sqrt2 K+36|lambda|)epsilon.'],
       tetrahedron_gap_at_J1_K2_lambda_sqrt3=Delta,
       sufficient_epsilon_to_keep_classical_minimizers_inside_original_ground_set=Delta/(2*C),
       samples=samples,
       proof='Weyl bounds separate the clusters. Projecting the perturbed low eigenvector equation onto Qperp bounds sinTheta by eta/(1-eta), eta=2epsilon. Cyclic trace telescoping uses product trace norm <=3. Commutator Frobenius variation <=4sqrt3 epsilon, and projector commutator norm <=sqrt(3/2). Finite classical gap and uniform energy error prevent former excited configurations from winning when2Cepsilon<Delta.',
       boundary='Degeneracy may split. These are finite supplied-model bounds, not a thermodynamic phase or laboratory tolerance without calibrated error assumptions.')

def markov():
    I=np.eye(9);P=[PI[3*p] for p in [0,4,2,13,1]]
    f2=I-P[0];f3=f2-1.5*f2@P[1]@f2;f4=f3-2*f3@P[2]@f3
    lhs=np.trace(f4@P[4]).real/9;rhs=np.trace(f4).real/27
    assert abs(lhs-1/9)<1e-12 and abs(rhs-1/27)<1e-12
    # Fresh third qutrit: the last Pauli is Z_first tensor I_second tensor Z_third.
    W=np.kron(np.kron(Z,np.eye(3)),Z);fresh=(np.eye(27)+W+W@W)/3
    extended=[np.kron(p,np.eye(3)) for p in P[:4]]+[fresh]
    residuals=[]
    for i,A in enumerate(extended):
        assert np.max(abs(A@A-A))<1e-12
        for j,B in enumerate(extended):
            if abs(i-j)==1:residuals.append(float(np.max(abs(A@B@A-A/3))))
            elif i!=j:residuals.append(float(np.max(abs(A@B-B@A))))
    assert max(residuals)<1e-12
    partial=np.trace(fresh.reshape(9,3,9,3),axis1=1,axis2=3)
    assert np.max(abs(partial-np.eye(9)))<1e-12
    paths=np.array([1,0,0,0,0],dtype=object);levels=[]
    for n in range(1,13):
        nxt=np.zeros(5,dtype=object)
        for j in range(5):
            for k in (j-1,j+1):
                if 0<=k<5:nxt[k]+=paths[j]
        paths=nxt;D=3**(n//2)
        mult={str(j):(1 if n%2 else [1,0,2,0,1][j]) for j in range(5) if paths[j]}
        assert sum(int(paths[j])*mult[str(j)] for j in range(5) if paths[j])==D
        levels.append(dict(strands=n,path_dimensions=[int(x) for x in paths],Markov_multiplicities=mult,minimum_ordinary_trace_dimension=D))
    return dict(status='PASS_NATIVE_MARKOV_TRACE_COUNTEREXAMPLE_AND_REPAIR',
       native_normalized_trace_f4_Plast=lhs,Markov_required_value=rhs,
       exact_counterexample='tau9(f4 P_last)=1/9, whereas the Markov property requires tau9(f4)/3=1/27. The nine-dimensional representation is a valid braid/TL representation but is not the full six-strand Markov-trace carrier.',
       repaired_dimension=27,maximum_TL_relation_error=max(residuals),fresh_partial_trace_error=float(np.max(abs(partial-np.eye(9)))),
       exact_repair='Keep the first four native projectors tensored with I3, replace the final Z_first projector by the eig0 projector of Z_first tensor I_second tensor Z_third. Its partial trace on the fresh register is I9, proving the Markov extension for every x in Mat9, hence for the prefix TL algebra.',
       fusion_path_ledger=levels,
       capacity_scope='At SU(2)_4, the full positive Markov trace on the semisimple Jones quotient is represented by normalized ordinary matrix trace only in dimensions divisible by3^floor(n/2); the minimum is attained with the recorded quantum-dimension multiplicities. This does not bound arbitrary fixed-charge braid representations or the cost of a local R-matrix realization.',
       prior='SU(2)_4 fusion and localization are classical (Rowell-Wang). Native TL generators and f4 are previous repository results. Here the explicit trace failure and fresh-register repair are checked on those actual matrices.')

def spectral(Q):
    H=np.eye(9)-Q;D=np.kron(np.eye(9),H)-np.kron(H.T,np.eye(9))
    eig=np.linalg.eigvalsh(D);expected=np.array([-1]*18+[0]*45+[1]*18)
    assert np.max(abs(eig-expected))<1e-11
    J=np.zeros((81,81))
    for i,j in itertools.product(range(9),repeat=2):J[j+9*i,i+9*j]=1
    assert np.max(abs(J@D.conj()@J+D))<1e-12
    rng=np.random.default_rng(814536);checks=[]
    for _ in range(4):
        a=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9));b=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
        L=np.kron(np.eye(9),a);R=np.kron(b.T,np.eye(9));comm=D@L-L@D
        err=max(float(np.max(abs(L@R-R@L))),float(np.max(abs(comm@R-R@comm))))
        assert err<1e-11;checks.append(err)
    return dict(status='PASS_REAL_FIRST_ORDER_MATRIX_MODULE_AND_SPECTRAL_BLINDNESS',
       fundamental_obstruction='On C9 the faithful Mat9 left action has scalar commutant. No antiunitary J can make J Mat9 J^-1 commute with all Mat9; the order-zero reality condition fails on that carrier.',
       explicit_module='On Mat9 with Hilbert-Schmidt product: L_a(M)=aM, R_b(M)=Mb, J(M)=Mdagger, D(M)=[H,M], H=I-Q.',
       minimum_faithful_order_zero_bimodule_dimension=81,
       bimodule_dimension_reason='Commuting faithful left/right Mat9 actions give a nonzero representation of Mat9 tensor Mat9^op =Mat81. Thus its dimension is a multiple of81; the Hilbert-Schmidt module attains the minimum. This operator module is not automatically the different Steinberg81 homology representation.',
       exact_identities=['J^2=1; JD=-DJ; [L_a,R_b]=0; [[D,L_a],R_b]=0.','D spectrum: -1 multiplicity18,0 multiplicity45,+1 multiplicity18.'],
       maximum_matrix_identity_error=max(checks),
       spectral_action='Tr f(D^2/Lambda^2)=45f(0)+36f(1/Lambda^2), identical for all810 unitarily conjugate parents and both tetrahedral orientations.',
       even_grading_obstruction='Any grading commuting with all L_a is a right multiplication. Anticommuting it with L_H-R_H would force L_H to be a right multiplication, hence H scalar. The chosen nonconstant parent therefore admits no such even grading.',
       boundary='Explicit finite real first-order operator data, not a completed orientable/Poincare-dual spectral triple of the Standard Model, not even KO6 matter geometry, not Lorentzian gravity. The spectral action alone cannot select among these810 conjugate parents.',
       prior='Connes-Chamseddine spectral action/real-geometry framework is established. Previous repository work already distinguishes fundamental and full matrix modules; here the chosen parent gives an explicit commutant obstruction, first-order construction and selection no-go.')

def build():
    tetra,loop,labels,Q=parent_data();out={}
    out['control']=control(tetra,loop,labels,Q);print(out['control']['status'],flush=True)
    out['robustness']=robustness(labels,Q);print(out['robustness']['status'],flush=True)
    out['markov']=markov();print(out['markov']['status'],flush=True)
    out['spectral']=spectral(Q);print(out['spectral']['status'],flush=True)
    return dict(status='PASS_PARENT_CONTROL_AND_QUANTUM_GEOMETRY',**out)

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261101_parent_control_quantum_geometry.json').write_text(json.dumps(d,indent=2)+'\n')
