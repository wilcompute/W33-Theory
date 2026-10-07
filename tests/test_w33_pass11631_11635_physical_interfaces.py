"""Independent pulse, CP, exact-map, full-normal and ensemble controls."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import sympy as s
import pytest
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11631_11635_physical_interfaces as m

@pytest.fixture(scope='module')
def cert():return json.loads(m.OUT.read_text())

def unpack(rows):return np.array([[complex(*z) for z in row] for row in rows])
def symbolic(rows):return np.array([[complex(s.sympify(z)) for z in row] for row in rows])

def test_producer_binding_and_five_interfaces(cert):
    assert cert['passes']==list(range(11631,11636))
    assert cert['producer_sha256']==hashlib.sha256(Path(m.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    for k in ['microscopic_instrument','physical_flavor','phase_quotient','full_quantum_normals','native_tree_gravity']:assert cert[k]['status']=='PASS'
    assert m.full_quantum_normals()['certificate_sha256']==cert['full_quantum_normals']['certificate_sha256']

def test_pulses_entangled_channel_and_noise(cert):
    d=cert['microscopic_instrument'];Y=np.array([[0,-1j],[1j,0]]);I=np.eye(2)
    theta=d['filter_angle'];H=theta/2*(np.kron(Y,np.eye(4))-np.kron(np.kron(Y,Y),I))
    W=np.kron(I,expm(-1j*unpack(d['polar_Hamiltonian'])))@expm(-1j*H)
    assert np.allclose(W,unpack(d['unitary']),atol=2e-13)
    assert np.allclose(W.conj().T@W,np.eye(8))
    rng=np.random.default_rng(11631);v=rng.normal(size=8)+1j*rng.normal(size=8);v/=np.linalg.norm(v)
    outs=[np.kron(W[:4,:4],I)@v,np.kron(W[4:,:4],I)@v]
    assert abs(sum(np.vdot(x,x).real for x in outs)-1)<1e-12
    assert all(t['Hadamard_distillable'] for t in d['explicit_noise_trials'])
    assert d['sufficient_coherent_unitary_error']**2==pytest.approx(d['total_success']/200)
    # A missing polar pulse is physically observable on the magic preparation.
    assert np.linalg.norm(W[:4,:4]-expm(-1j*H)[:4,:4])>.1

def test_exact_physical_CP_polynomial_and_spectrum(cert):
    d=cert['physical_flavor'];e=s.symbols('epsilon',real=True)
    Yu=s.diag(1,2,4);Yd=s.Matrix([[2,1,s.I*e],[1,3,1],[s.I*e,1,4]])
    Hu=Yu.H*Yu;Hd=Yd.H*Yd;C=Hu*Hd-Hd*Hu
    invariant=s.factor(s.trace(C**3)/s.I)
    assert invariant==6480*e*(e*e+34)
    assert s.sympify(d['exact_CP_invariant_Tr_commutator_cube_over_i'],locals={'epsilon':e})==invariant
    assert invariant.subs(e,-1)==-invariant.subs(e,1) and invariant.subs(e,0)==0
    V=unpack(d['epsilon1_CKM']);eu=d['epsilon1_squared_masses']['up'];ed=d['epsilon1_squared_masses']['down']
    J=(V[0,0]*V[1,1]*V[0,1].conjugate()*V[1,0].conjugate()).imag
    assert J==pytest.approx(d['epsilon1_Jarlskog']) and abs(J)>.03
    # The convention-independent absolute Jarlskog determinant relation.
    gaps=lambda a:np.prod([a[j]-a[i] for i in range(3) for j in range(i+1,3)])
    assert abs(float(invariant.subs(e,1)))==pytest.approx(abs(6*J*gaps(eu)*gaps(ed)))
    rephase=np.diag(np.exp(1j*np.array([.2,.7,-.1])))@V@np.diag(np.exp(1j*np.array([-.3,.6,.9])))
    assert (rephase[0,0]*rephase[1,1]*rephase[0,1].conjugate()*rephase[1,0].conjugate()).imag==pytest.approx(J)

def test_joint_sector_little_groups_and_covariance(cert):
    d=cert['physical_flavor'];_,group,gens,pg,cp,tr,configs=m.clifford_geometry()
    from collections import Counter
    counts=Counter(len([p for p in group if p[h]==h and tr(c,p)==c]) for c in configs for h in range(12))
    assert counts=={1:4752,3:432} and {str(k):v for k,v in counts.items()}==d['joint_sector_stabilizer_census']
    table={}
    seed=np.array([[2,1,1j],[1,3,1],[1j,1,4]])
    u=np.diag([1,4,16]);v=seed.conj().T@seed
    for item in d['orbit_representatives']:
        c=tuple(map(tuple,item['config']));h=item['h'];G=unpack(item['representative']);table[c,h]=(G@u@G.conj().T,G@v@G.conj().T)
    assert len(table)==216
    for (c,h),(a,b) in list(table.items()):
        assert (tr(c,cp),cp[h]) not in table
        for p,G in zip(pg,gens):
            aa,bb=table[tr(c,p),p[h]]
            assert np.allclose(aa,G@a@G.conj().T) and np.allclose(bb,G@b@G.conj().T)

def test_Weyl_word_complex_structure_and_exact_intertwiner(cert):
    d=cert['phase_quotient'];R,C,omega,refs=m.coxeter_data();W=s.eye(8)
    for j in d['compatible_Weyl_word']:W=refs[j]*W
    good=W*omega*W.T;stored=s.Matrix(d['repaired_omega'])
    assert good==stored and good*good+good+s.eye(8)==s.zeros(8)
    E=s.eye(8)[:,4:];N=E.T*(2*good+s.eye(8))*E
    assert N*N==-s.eye(4) and N==s.Matrix(d['compatible_restricted_N'])
    P=s.Matrix(d['complex_projection']);J=(2*good+s.eye(8))/s.sqrt(3)
    assert all(s.simplify(s.expand(z))==0 for z in P*J-s.I*P)
    old=E.T*(2*omega+s.eye(8))*E
    assert old.rank()==2 and d['original_complex_distinct_D4_rays']==10
    assert len(d['selected_D4_Witting_rays'])==12

def map_agrees(mapping,P,R):
    from w33_pass11630_reye_witting_instrument import numeric_vectors
    V=numeric_vectors();out=P@R.T;out/=np.linalg.norm(out,axis=0)
    return np.all(abs(np.sum(V[:,mapping].conj()*out,axis=0))**2>1-1e-12)

def test_all240_dictionary_and_corrupt_fiber_control(cert):
    d=cert['phase_quotient'];R,C,omega,refs=m.coxeter_data();P=symbolic(d['complex_projection']);mapping=d['all240_root_to_Witting_ray']
    assert map_agrees(mapping,P,R)
    from collections import Counter
    assert Counter(mapping)=={i:6 for i in range(40)}
    bad=mapping.copy();bad[0]=(bad[0]+1)%40;assert not map_agrees(bad,P,R)
    selected={mapping[i] for i,r in enumerate(R) if not any(r[:4])}
    assert selected==set(d['selected_D4_Witting_rays'])

def test_full_normal_frame_Ward_identity_and_positive_gap(cert):
    d=json.loads((ROOT/'data/w33_pass11634_full_quantum_normals.json').read_text())
    H=np.array(d['full_Hessian']);G=np.array(d['gauge_frame']);N=np.array(d['normal_frame'])
    assert H.shape==(297,297) and G.shape==(297,45) and N.shape==(297,264)
    import w33_pass11625_11629_composites_joint_vacua as old
    V,T,D=old.scalar_data();q=np.array(d['canonical_background'])
    A=np.einsum('a,aij->ij',q[:45],V);S=np.einsum('a,aij->ij',q[45:],D)
    ga=V@A-A@V;gs=T@S+S@T.transpose(0,2,1)
    independently_built=np.vstack([np.einsum('aij,bij->ab',V,ga)/2,2*np.einsum('aij,bij->ab',D.conj(),gs).real])
    assert np.max(abs(G-independently_built))<1e-12
    assert np.max(abs(H-H.T))<1e-10 and np.linalg.norm(H@G)<1e-8
    assert np.linalg.matrix_rank(G,tol=1e-9)==33 and np.linalg.norm(G.T@N)<1e-12
    assert np.max(abs(N.T@N-np.eye(264)))<1e-12
    eig=np.linalg.eigvalsh(N.T@H@N);assert eig[0]>.0016
    assert np.allclose(eig,d['normal_eigenvalues'],atol=1e-12)
    assert d['full_gradient_norm']<1e-8 and d['minimum_scalar_denominator']>0
    assert d['quadrature_control']['reference_order']==32 and d['quadrature_control']['Hessian_operator_norm_difference']<1e-9
    for c in d['directional_controls']:
        v=np.array(c['direction']);actual=v@H@v
        assert actual==pytest.approx(c['AD_curvature'],abs=1e-12)
        assert abs(actual-c['finite_difference_curvatures'][-1])<3e-7
    # Corruption parallel to a physical normal must be observable.
    broken=H-.01*np.outer(N[:,0],N[:,0]);assert np.linalg.norm(N.T@(broken-H)@N)>.009

def test_repeated_eigenvalue_Frechet_rule():
    import w33_pass11634_full_quantum_normals as q
    import jax,jax.numpy as j
    _,_,_,_,_,_,first=q.make_action(32)
    H=j.eye(3)*.2;E=j.asarray([[1.,.1,.2],[.1,-.3,.4],[.2,.4,.5]])
    _,ad=jax.jvp(first,(H,),(E,));step=1e-5
    fd=(np.array(first(H+step*E))-np.array(first(H-step*E)))/(2*step)
    assert np.max(abs(fd-np.array(ad)))<1e-11

def test_native_tree_projector_covariance_and_weighted_partition(cert):
    d=cert['native_tree_gravity'];K=np.array(d['exact_cut_projector_numerator'],dtype=np.int64)
    B=np.zeros((80,160),dtype=np.int64)
    for j,(a,b) in enumerate(d['edges']):B[a,j]=-1;B[b,j]=1
    assert np.array_equal(K@K,160*K) and np.array_equal(B@K,160*B)
    tree=B[:,d['representative_tree_edges']];assert np.linalg.matrix_rank(tree)==79
    assert d['conditional_branch_spin2_polarizations']==2+79*5
    incident=np.where(B[0])[0];Cov=-K*K;np.fill_diagonal(Cov,79*81)
    assert not np.any(Cov.sum(axis=1))
    assert s.Rational(int(Cov[np.ix_(incident,incident)].sum()),160**2)==s.Rational(1053,1600)
    assert d['exact_adjacent_edge_covariance']=='-729/25600'
    assert Cov[incident[0],incident[1]]!=0  # a nonzero quartic cumulant
    for t in d['weighted_cofactor_controls']:assert t['cofactor_ratio']==pytest.approx(t['exact_polynomial_value'],abs=3e-13)

def test_flux_detailed_balance_and_vacuum_shift_obstruction(cert):
    d=cert['native_tree_gravity'];f=d['flux_control'];Q=np.array(f['generator']);pi=np.array(f['stationary_distribution'])
    assert max(abs(pi@Q))<2e-15 and max(abs(Q.sum(axis=1)))<2e-15
    for i in range(16):assert pi[i]*Q[i,i+1]==pytest.approx(pi[i+1]*Q[i+1,i])
    assert f['smallest_positive_energy']=='1/50' and f['next_downhill_energy']=='-1/5'
    assert Q[14,13]>0 and pi[8]>pi[14]  # no absorbing smallest-positive vacuum
    assert np.exp(-.3*(2.-5.))!=pytest.approx(1.)
    assert 'not' in d['boundary'] and 'not sequester' in d['vacuum_boundary']
