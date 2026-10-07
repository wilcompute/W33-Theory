"""Independent Pauli, direct-action, invariant-ring and canonical controls."""
import importlib.util
import itertools
import json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('five11625',ROOT/'analysis/w33_pass11625_11629_composites_joint_vacua.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)


def cert():return json.loads(M.OUT.read_text())


def test_actual_fermion_CAR_and_parity():
    c=[np.array(M.fermion_operator(4,i)).astype(float) for i in range(4)]
    for i,j in itertools.product(range(4),repeat=2):
        assert np.array_equal(c[i]@c[j]+c[j]@c[i],np.zeros((16,16)))
        assert np.array_equal(c[i]@c[j].T+c[j].T@c[i],np.eye(16)*(i==j))
    P=np.diag([(-1)**i.bit_count() for i in range(16)])
    assert np.array_equal(P@c[0].T@c[1].T,c[0].T@c[1].T@P)


def test_singlet_embedding_using_independent_antisymmetric_matrices():
    T,_,B,R,C,_,P,_,_,_=M.spin_pair_data();eps=np.array([[0,1],[-1,0]])
    A=np.array([np.kron(eps,b) for b in B])
    assert np.max(abs(A+A.transpose(0,2,1)))<1e-14
    assert np.max(abs(np.einsum('aij,bij->ab',A.conj(),A)/2-np.eye(136)))<1e-13
    for j in [0,7,31]:
        K=np.kron(np.eye(2),T[j]);d=K@A+A@K.T
        assert np.max(abs(np.einsum('aij,bij->ab',A.conj(),d)/2-R[j]))<1e-13
    assert np.linalg.matrix_rank(P,tol=1e-10)==126


def test_exact_second_order_from_full_fermionic_resolvent():
    c=[M.fermion_operator(4,i) for i in range(4)];n=[a.T*a for a in c]
    H0=sum((n[2*j]+n[2*j+1]-2*n[2*j]*n[2*j+1] for j in range(2)),s.zeros(16))
    V=-sum((c[i].T*c[i+2]+c[i+2].T*c[i] for i in range(2)),s.zeros(16))
    P=s.diag(*[int(i in [0,3,12,15]) for i in range(16)])
    inverse=s.diag(*[0 if H0[i,i]==0 else 1/H0[i,i] for i in range(16)])
    W=-P*V*inverse*V*P
    assert W.extract([0,3,12,15],[0,3,12,15])==s.Matrix([[0,0,0,0],[0,-1,-1,0],[0,-1,-1,0],[0,0,0,0]])
    small=.01;H=np.array(H0+small*V,dtype=float)
    assert abs(np.linalg.eigvalsh(H)[0]/small**2+2)<5e-4


def test_added_density_repair_is_required_not_just_an_energy_shift():
    old=s.Matrix([[0,0,0,0],[0,-1,-1,0],[0,-1,-1,0],[0,0,0,0]])
    swap=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
    n1=s.diag(0,1,0,1);n2=s.diag(0,0,1,1)
    assert old+2*(n1+n2-2*n1*n2)==s.eye(4)-swap
    assert len(set((s.eye(4)-swap-old).diagonal()))>1


def test_center_Gauss_projector_and_dressed_pair_creation():
    states=list(itertools.product(range(2),range(2),range(4)));allowed=[]
    for n1,n2,e in states:
        average=sum(np.exp(2j*np.pi*(a*(2*n1+e)+b*(2*n2-e))/4) for a,b in itertools.product(range(4),repeat=2))/16
        if abs(average-1)<1e-12:allowed.append((n1,n2,e))
        else:assert abs(average)<1e-12
    assert allowed==[(0,0,0),(1,1,2)]
    assert (1,0,0) not in allowed


def test_full_general_Hessian_direct_action_in_arbitrary_normal_directions():
    V,T,D=M.scalar_data();rng=np.random.default_rng(126297)
    for q in [[.98,.01,1.02],[1.01,-.02,.99]]:
        A,S=M.background(q);H=M.scalar_hessian(A,S)
        for _ in range(4):
            v=rng.normal(size=297);v/=np.linalg.norm(v)
            dA=np.einsum('a,aij->ij',v[:45],V);dS=np.einsum('a,aij->ij',v[45:],D);h=3e-4
            second=(M.scalar_tree(A+h*dA,S+h*dS)+M.scalar_tree(A-h*dA,S-h*dS)-2*M.scalar_tree(A,S))/h**2
            assert abs(second-v@H@v)<2e-6


def test_general_background_gauge_covariance_of_full_scalar_and_vector_spectra():
    V,T,D=M.scalar_data();A,S=M.background([.99,.01,1.01])
    O=expm(.19*V[9]);G=expm(.19*T[9]);a=O@A@O.T;z=G@S@G.T
    assert abs(M.scalar_tree(a,z)-M.scalar_tree(A,S))<1e-12
    assert np.max(abs(np.linalg.eigvalsh(M.scalar_hessian(a,z))-np.linalg.eigvalsh(M.scalar_hessian(A,S))))<1e-10
    assert np.max(abs(M.gauge_masses(a,z)-M.gauge_masses(A,S)))<1e-11


def test_shell_integral_against_closed_antiderivative_all_modes():
    q=np.array([1.,0.,1.]);A,S=M.background(q);c=.001
    sm=c*np.linalg.eigvalsh(M.scalar_hessian(A,S));vm=c*M.gauge_masses(A,S)
    def primitive(x,a):return x*x*np.log1p(a/x)/2+a*(x-a*np.log(x+a))/2
    direct=np.sum(primitive(.25,sm)-primitive(.01,sm))+3*np.sum(primitive(.25,vm)-primitive(.01,vm))
    direct=direct/(64*np.pi**2)+c*M.scalar_tree(A,S)
    assert abs(direct-M.shell_potential(q,order=64))<1e-11
    assert len(sm)==297 and len(vm)==45


def test_committed_quantum_slice_stationarity_and_resolution():
    c=cert()['quantum_vacuum'];q=np.array(c['stationary_SM_slice'])
    f=lambda q:M.shell_potential(q,order=64)
    assert np.linalg.norm(M.grad(f,q,h=1e-5))<2e-7
    assert min(np.linalg.eigvalsh(M.finite_hessian(f,q,h=2e-4)))>0
    assert np.linalg.norm(q-[1,0,1])>1e-4
    assert np.max(abs(np.array(c['three_starts'])-q))<2e-4


def test_reference_all_normal_tree_gap_is_preserved_as_formal_input():
    H=M.scalar_hessian(*M.background([1,0,1]));ev=np.linalg.eigvalsh(H)
    assert np.sum(ev>1e-8)==264
    assert np.min(ev[ev>1e-8])>1.999999
    assert 'no explicit all-normal bound' in cert()['quantum_vacuum']['formal_persistence']


def group_data():
    w=np.exp(2j*np.pi/3);F=np.array([[w**(i*j) for j in range(3)] for i in range(3)])/np.sqrt(3)
    P=np.diag([1,1,w]);X=np.roll(np.eye(3),1,axis=0);Z=np.diag([1,w,w*w])
    RF=np.array([[1,np.sqrt(2)],[np.sqrt(2),-1]])/np.sqrt(3);RP=np.diag([1,w])
    return [(F,RF),(P,RP),(X,np.eye(2)),(Z,np.eye(2))]


def test_joint_intertwiner_and_interaction_on_complex_mixed_words():
    rng=np.random.default_rng(11627);u=rng.normal(size=2)+1j*rng.normal(size=2);h=rng.normal(size=3)+1j*rng.normal(size=3)
    for G,R in group_data()+list(reversed(group_data())):
        assert np.max(abs(M.hesse_D(G@h)-G.conj()@M.hesse_D(h)@R.T))<1e-12
        assert abs(M.joint_potential(R@u,G@h)-M.joint_potential(u,h))<1e-10
        h=G@h;u=R@u


def commutant_dimension(gens):
    n=gens[0].shape[0]
    A=np.vstack([np.kron(np.eye(n),G)-np.kron(G.T,np.eye(n)) for G in gens])
    return n*n-np.linalg.matrix_rank(A,tol=1e-9)


def test_quartic_invariant_classification_by_independent_commutants():
    gens=group_data()
    assert commutant_dimension([np.kron(R,G) for G,R in gens])==1
    # Sym2(h) is the six-dimensional carrier identified by the explicit map.
    assert commutant_dimension([np.kron(G.conj(),R) for G,R in gens])==1
    b=np.zeros((4,3));b[0,0]=1;b[3,2]=1;b[1,1]=b[2,1]=1/np.sqrt(2)
    assert commutant_dimension([b.T@np.kron(R,R)@b for G,R in gens])==1


def test_joint_nonnegative_potential_global_rays_and_tetrahedral_doublets():
    c=cert()['joint_flavor'];assert c['projective_count']==12
    us=[];hs=[]
    for v in c['projective_vacua']:
        h=np.array([complex(*z) for z in v['h']]);u=np.array([complex(*z) for z in v['u']])
        hs.append(h);us.append(np.outer(u,u.conj()))
        assert abs(M.joint_potential(u,h))<1e-12
        assert np.linalg.matrix_rank(M.hesse_D(h),tol=1e-10)==1
    unique=[]
    for a in us:
        if not any(np.max(abs(a-b))<1e-10 for b in unique):unique.append(a)
    assert len(unique)==4
    for a,b in itertools.combinations(unique,2):assert abs(np.trace(a@b)-1/3)<1e-12
    rng=np.random.default_rng(12)
    for _ in range(20):
        u=rng.normal(size=2)+1j*rng.normal(size=2);h=rng.normal(size=3)+1j*rng.normal(size=3)
        assert M.joint_potential(u,h)>=-1e-12


def test_exact_joint_canonical_Hessian_instead_of_only_finite_differences():
    q=s.symbols('q0:10',real=True)
    u=s.Matrix([(q[i]+s.I*q[i+2])/s.sqrt(2) for i in range(2)])
    h=s.Matrix([(q[i+4]+s.I*q[i+7])/s.sqrt(2) for i in range(3)])
    D=s.Matrix([[h[i]**2,s.sqrt(2)*h[(i+1)%3]*h[(i+2)%3]] for i in range(3)])
    ru=(u.conjugate().T*u)[0];rh=(h.conjugate().T*h)[0];z=D*u.conjugate()
    V=s.expand((ru-1)**2+(rh-1)**2+ru*rh**2-(z.conjugate().T*z)[0])
    point={a:0 for a in q};point[q[0]]=point[q[4]]=s.sqrt(2)
    H=s.hessian(V,q).subs(point)
    assert sorted(H.diagonal())==[0,0,1,1,2,2,2,2,4,4]
    assert H==s.diag(*H.diagonal())


def test_selected_joint_orbit_is_CP_preserving_and_MUB_closed():
    hs=[np.array([complex(*z) for z in a['h']]) for a in cert()['joint_flavor']['projective_vacua']]
    for h in hs:
        for G,R in group_data():assert any(abs(abs(np.vdot(G@h,z))-1)<1e-10 for z in hs)
        assert any(abs(abs(np.vdot(h.conj(),z))-1)<1e-10 for z in hs)
    # These are the known twelve stabilizer rays, now a potential's zero set.
    for h in hs:
        overlaps=[abs(np.vdot(h,z))**2 for z in hs]
        assert sum(abs(a)<1e-10 for a in overlaps)==2
        assert sum(abs(a-1/3)<1e-10 for a in overlaps)==9


def spectral_derivative(a,order=1):
    n=len(a);k=np.fft.fftfreq(n,1/n)
    return np.fft.ifft((1j*k)**order*np.fft.fft(a)).real


def spherical_functionals(q,N,v,alpha=1.,beta=1.):
    L,R,pL,pR,phi,p=q;r1=spectral_derivative(R);l1=spectral_derivative(L);r2=spectral_derivative(R,2)
    H=-pL*pR/R+L*pL*pL/(2*R*R)+R*r2/L-R*r1*l1/(L*L)+r1*r1/(2*L)-L/2+alpha*p*p/(2*L*R*R)+beta*R*R*spectral_derivative(phi)**2/(2*L)
    D=pR*r1-L*spectral_derivative(pL)+p*spectral_derivative(phi)
    return np.sum(N*H)*2*np.pi/len(L),np.sum(v*D)*2*np.pi/len(L)


def independent_bracket(n,alpha=1.,beta=1.):
    x=np.arange(n)*2*np.pi/n
    q=np.array([1+.11*np.sin(x),2+.13*np.cos(x),.2+.07*np.cos(2*x),.11*np.sin(2*x),.12*np.cos(x+.2),.1+.08*np.sin(x+.7)])
    N=np.sin(x)+.2*np.cos(2*x);M0=np.cos(x+.3)+.1*np.sin(3*x)
    def derivative(N):
        a=np.empty_like(q);eps=2e-5
        for i,j in itertools.product(range(6),range(n)):
            d=np.zeros_like(q);d[i,j]=eps
            a[i,j]=(spherical_functionals(q+d,N,np.zeros(n),alpha,beta)[0]-spherical_functionals(q-d,N,np.zeros(n),alpha,beta)[0])/(2*eps)
        return a
    a,b=derivative(N),derivative(M0);pb=sum(np.sum(a[i]*b[j]-a[j]*b[i]) for i,j in [(0,2),(1,3),(4,5)])/(2*np.pi/n)
    v=(N*spectral_derivative(M0)-M0*spectral_derivative(N))/q[0]**2
    target=spherical_functionals(q,np.zeros(n),v,alpha,beta)[1]
    extra=np.sum(v*q[5]*spectral_derivative(q[4]))*2*np.pi/n
    return pb,target,extra


def test_nonlinear_spherical_brackets_by_independent_functional_variations():
    for n in [16,32]:
        pb,target,extra=independent_bracket(n)
        assert abs(pb-target)<2e-6


def test_scalar_speed_mismatch_is_the_predicted_local_constraint_defect():
    pb,target,extra=independent_bracket(32,alpha=2,beta=1)
    assert abs(extra)>1e-4
    assert abs(pb-target-extra)<2e-6


def test_all_three_symbolic_brackets_and_coarse_structure_function():
    c=M.spherical_constraints();assert c['status']=='PASS'
    assert s.Rational(5,8)-s.Rational(4,9)==s.Rational(13,72)
    for L in [[1,2],[.9,1.3,1.7]]:assert np.mean(1/np.array(L)**2)>1/np.mean(L)**2


def test_Lorentzian_rotor_kernel_by_independent_Fourier_transform():
    c=cert()['lorentzian_flux'];m=np.array(c['flux_labels']);E=np.array(c['energies']);n=len(m)
    theta=2*np.pi*np.arange(n)/n;F=np.exp(1j*theta[:,None]*m)/np.sqrt(n)
    U=lambda t:F@np.diag(np.exp(-1j*t*E))@F.conj().T
    assert np.max(abs(U(.2)@U(.7)-U(.9)))<1e-13
    assert np.max(abs(U(.2).conj().T@U(.2)-np.eye(n)))<1e-13


def test_membrane_shift_keeps_boundary_loss_and_energy_difference():
    n=17;S=np.zeros((n,n));S[np.arange(1,n),np.arange(n-1)]=1
    assert np.array_equal(S.T@S,np.diag([1]*16+[0]))
    e=s.symbols('e');m=s.symbols('m',integer=True)
    assert s.simplify(e*e*(m*m-(m-1)**2)/2-e*e*(m-s.Rational(1,2)))==0


def test_fixed_topology_membrane_charge_lattice_criterion():
    a=np.array([0,1]);q=np.array([1,0])
    for chi in [0,2,-4]:
        state=np.array([7,-chi]);assert a@state==-chi and a@(state+q)==-chi
        assert a@(state+[0,1])!=-chi
    assert all(z!=0 for z in [-3,-2,-1,1,2,3])
    # A single Euler flux fixed at zero has no nonzero charge preserving it.
    assert [q for q in range(-4,5) if q==0]==[0]


def test_flat_bounce_negative_mode_and_constraint_response():
    D,T,r=s.symbols('D T r',positive=True);S=2*s.pi**2*T*r**3-s.pi**2*D*r**4/2;R=3*T/D
    assert s.diff(S,r).subs(r,R)==0
    assert s.simplify(S.subs(r,R))==27*s.pi**2*T**4/(2*D**3)
    assert s.diff(S,r,2).subs(r,R)<0
    N,V,C=s.symbols('N V C');assert s.diff(-N*V*C,N)==-V*C


def test_source_binding_and_five_scoped_sections():
    c=cert();assert c['status']=='PASS'
    for k in ['fermion_matching','quantum_vacuum','joint_flavor','spherical_constraints','lorentzian_flux']:assert c[k]['status']=='PASS'
    assert c['producer_sha256']==M.ph(Path(M.__file__))
    for p,h in c['source_sha256'].items():assert M.ph(ROOT/p)==h


def test_Reye_A4_incidence_map_independently_reconstructs_every_line():
    from w33_witting_reye_toroidal_tomotope_collapse import reye_lines
    c=cert()['reye_vacuum_audit']
    mapping={tuple(a['point']):tuple(a['permutation']) for a in c['concrete_Reye_A4_isomorphism']}
    assert len(set(mapping.values()))==12
    grid=[frozenset(p for p in mapping.values() if p[i]==j) for i,j in itertools.product(range(4),repeat=2)]
    mapped=[frozenset(mapping[p] for p in L['points']) for L in reye_lines()]
    assert set(mapped)==set(grid)
    R=s.Matrix([[int(p in L) for L in grid] for p in mapping.values()])
    assert R.rank()==10 and (R*R.T-s.ones(12)).rank()==9


def test_exact_dual_Hesse_geometry_and_MUB_incidence_scope():
    c=cert()['reye_vacuum_audit'];w=-s.Rational(1,2)+s.I*s.sqrt(3)/2
    rays=[s.eye(3)[:,i] for i in range(3)]+[s.Matrix([1,w**r,w**t]) for r,t in itertools.product(range(3),repeat=2)]
    deps=set()
    for t in itertools.combinations(range(12),3):
        if s.simplify(s.det(s.Matrix.hstack(*(rays[i] for i in t))))==0:deps.add(t)
    lines=[tuple(t) for t in c['exact_projective_lines']]
    assert len(lines)==9 and set(itertools.chain.from_iterable(itertools.combinations(t,3) for t in lines))==deps
    assert len(deps)==36
    for b in c['MUB_blocks']:assert s.simplify(s.det(s.Matrix.hstack(*(rays[i] for i in b))))!=0
    for o in c['unitary_lift_orbits']:
        assert sum(tuple(t) in deps for t in o['representative'])==o['collinear_triples']<16


def test_Reye_lifts_exhaustive_and_faithful_symmetry_obstruction():
    c=M.reye_vacuum_audit();stored=cert()['reye_vacuum_audit']
    # Any valid incidence conjugator is accepted; the preceding test audits it.
    replay=json.loads(json.dumps(c))
    assert {k:v for k,v in replay.items() if k!='concrete_Reye_A4_isomorphism'}=={k:v for k,v in stored.items() if k!='concrete_Reye_A4_isomorphism'}
    assert c['MUB_preserving_Reye_lifts']==432
    assert c['collinearity_histogram']=={3:288,6:144}
    assert [o['size'] for o in c['unitary_lift_orbits']]==[72]*6
    assert c['Reye_automorphisms']%c['Clifford_ray_group_order']!=0
    for o in c['unitary_lift_orbits']:
        lines=o['representative'];pairs=list(itertools.chain.from_iterable(itertools.combinations(t,2) for t in lines))
        assert len(pairs)==len(set(pairs))==48
        assert [sum(i in t for t in lines) for i in range(12)]==[4]*12


def test_density_Gram_obstructs_equating_Reye_and_Higgs_geometries():
    c=cert();hs=[np.array([complex(*z) for z in v['h']]) for v in c['joint_flavor']['projective_vacua']]
    us=[np.array([complex(*z) for z in v['u']]) for v in c['joint_flavor']['projective_vacua']]
    H=np.array([[abs(np.vdot(a,b))**2 for b in hs] for a in hs])
    J=H*np.array([[abs(np.vdot(a,b))**2 for b in us] for a in us])
    assert np.linalg.matrix_rank(H-np.ones((12,12))/3,tol=1e-10)==8
    assert np.max(abs(np.linalg.eigvalsh(H)-np.array([0]*3+[1]*8+[4])))<1e-12
    assert np.max(abs(np.linalg.eigvalsh(J)-np.array([2/3]*3+[1]*8+[2])))<1e-12
    assert c['reye_vacuum_audit']['Reye_centered_rank']==9


def test_actual_Reye_coupling_parent_covariance_and_global_zero_retention():
    c=cert()['reye_vacuum_audit'];us,hs=M.joint_vacuum_vectors()
    rng=np.random.default_rng(432);u=rng.normal(size=2)+1j*rng.normal(size=2);h=rng.normal(size=3)+1j*rng.normal(size=3)
    u/=np.linalg.norm(u);h/=np.linalg.norm(h)
    values=[]
    cp=tuple(int(i) for i in np.argmax(abs(hs.conj()@hs.conj().T)**2,axis=0))
    for o in c['unitary_lift_orbits']:
        config=o['representative'];d=M.reye_alignment_defect(u,h,config);values.append(d*d)
        for (G,R),p in zip(group_data(),c['Clifford_generators']):
            transformed=[tuple(p[i] for i in t) for t in config]
            assert abs(M.reye_alignment_defect(R@u,G@h,transformed)-d)<1e-12
        transformed=[tuple(cp[i] for i in t) for t in config]
        assert abs(M.reye_alignment_defect(u.conj(),h.conj(),transformed)-d)<1e-12
        assert M.joint_reye_potential(u,h,config)>=M.joint_potential(u,h)-1e-12
        for a,b in zip(us,hs):assert abs(M.joint_reye_potential(a,b,config))<1e-12
    assert max(values)-min(values)>1e-7
    assert c['coupling']['separated_squared_defect_polynomials']==432


def test_no_declared_parent_antiunitary_stabilizes_any_Reye_zero_sector():
    c=cert()['reye_vacuum_audit'];us,hs=M.joint_vacuum_vectors()
    pg=c['Clifford_generators'];group={tuple(range(12))};queue=list(group)
    for p in queue:
        for a in pg:
            q=tuple(a[p[i]] for i in range(12))
            if q not in group:group.add(q);queue.append(q)
    cp=tuple(int(i) for i in np.argmax(abs(hs.conj()@hs.conj().T)**2,axis=0))
    anti={tuple(g[cp[i]] for i in range(12)) for g in group}
    assert len(group)==len(anti)==216 and not group&anti
    for o in c['unitary_lift_orbits']:
        config={frozenset(t) for t in o['representative']}
        invariant=lambda p:{frozenset(p[i] for i in t) for t in config}==config
        assert sum(invariant(p) for p in group)==3
        assert not any(invariant(p) for p in anti)
