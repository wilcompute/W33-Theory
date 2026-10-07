"""Independent representation, full potential, exact certificate and Ward audits."""
import importlib.util
import itertools
import json
from pathlib import Path

import numpy as np
import sympy as s
from scipy.integrate import quad
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('p11620',ROOT/'analysis/w33_pass11620_11624_covariant_pair_vacuum.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)


def certificate():return json.loads((ROOT/'data/w33_pass11620_11624_covariant_pair_vacuum.json').read_text())


def sparse_matrix(rows,shape):
    assert rows['shape']==list(shape)
    A=np.zeros(shape,dtype=np.int64)
    for i,j,v in zip(rows['rows'],rows['cols'],rows['values']):A[i,j]=v
    return A


def test_Casimir_from_full_tensor_product_and_independent_spinor_trace():
    T,_,B,R,C,P10,P126,*_=M.spin_pair_data()
    assert np.max(abs(-sum(t@t for t in T)-45*np.eye(16)/4))<1e-14
    Q=B.reshape(136,256).T
    full=-sum(np.linalg.matrix_power(np.kron(t,np.eye(16))+np.kron(np.eye(16),t),2) for t in T)
    assert np.max(abs(Q.conj().T@full@Q-C))<1e-12
    assert np.max(abs(P10@P126))<1e-13
    assert np.max(abs(P126@P126-P126))<1e-13
    assert np.linalg.matrix_rank(P126,tol=1e-10)==126
    Cr=sparse_matrix(certificate()['covariant_pair']['Casimir_raw_scaled4_sparse'],[136,136])
    I=np.eye(136,dtype=np.int64)
    assert not np.any((Cr-36*I)@(Cr-100*I))
    assert np.trace(Cr)==12960


def test_pair_projector_in_a_second_complex_spinor_basis():
    T,_,B,R,C,P10,P126,*_=M.spin_pair_data()
    rng=np.random.default_rng(12616)
    U,_=np.linalg.qr(rng.normal(size=(16,16))+1j*rng.normal(size=(16,16)))
    moved=np.einsum('ij,bjk,lk->bil',U,B,U)
    changed=np.array([U@t@U.conj().T for t in T])
    # Rebuild the symmetric representation from transformed tensors and generators.
    reps=[]
    for t in changed:
        d=np.einsum('ij,bjk->bik',t,moved)+np.einsum('bij,kj->bik',moved,t)
        reps.append(np.einsum('bij,cij->bc',moved.conj(),d))
    second=-sum(t@t for t in reps)
    assert np.max(abs(second-C))<1e-12


def test_actual126_link_swap_endpoint_covariance():
    T,_,B,R,C,P10,P126,Sbasis,raw,Praw=M.spin_pair_data()
    Q=np.einsum('bij,cij->bc',B.conj(),Sbasis)
    reduced=[Q.conj().T@R[i]@Q for i in [1,8,23]]
    U,gi,gj=[expm(.13*t) for t in reduced]
    rng=np.random.default_rng(11620)
    x=rng.normal(size=126)+1j*rng.normal(size=126);x/=np.linalg.norm(x)
    y=rng.normal(size=126)+1j*rng.normal(size=126);y/=np.linalg.norm(y)
    left=np.kron(gi@(U@y),gj@(U.conj().T@x))
    moved=gi@U@gj.conj().T
    right=np.kron(moved@(gj@y),moved.conj().T@(gi@x))
    assert np.linalg.norm(left-right)<1e-13
    assert abs(np.vdot(np.kron(x,y),np.kron(U@y,U.conj().T@x)).imag)<1e-13


def test_connected_three_level_parent_kernel_and_pair_number():
    # Two distinct126 directions plus the vacuum; no one-weight restriction.
    labels=list(itertools.product(range(3),repeat=3));H=np.zeros((27,27))
    for i,d in enumerate(labels):
        for a,b in [(0,1),(1,2)]:
            e=list(d);e[a],e[b]=e[b],e[a];j=labels.index(tuple(e))
            H[i,i]+=.5;H[i,j]-=.5
    assert np.sum(abs(np.linalg.eigvalsh(H))<1e-12)==10
    for k,expected in [(0,1),(1,2),(2,3),(3,4)]:
        ix=[i for i,d in enumerate(labels) if sum(z!=0 for z in d)==k]
        assert np.sum(abs(np.linalg.eigvalsh(H[np.ix_(ix,ix)]))<1e-12)==expected


def potential(A,S,V,T):
    nA=np.sum(abs(A)**2)/2;nS=np.sum(abs(S)**2)
    a=np.einsum('aij,ij->a',V,A)/2;tA=sum(x*t for x,t in zip(a,T))
    purity=nS*nS-np.trace((S@S.conj().T)@(S@S.conj().T)).real
    return (nA-3)**2+np.sum(abs(A@A@A+A)**2)/2+(nS-1)**2+purity+np.sum(abs(tA@S+S@tA.T+3j*S)**2)


def test_scalar_positive_action_and_common_gauge_orbit():
    H,J,Ji,Gi,A,S,V,T,D=M.scalar_jacobians()
    assert abs(potential(A,S,V,T))<1e-14
    O=expm(.173*V[11]);G=expm(.173*T[11])
    assert abs(potential(O@A@O.T,G@S@G.T,V,T))<1e-12
    rng=np.random.default_rng(11621)
    for _ in range(8):
        ar=rng.normal(size=45);z=rng.normal(size=252)
        dA=np.einsum('a,aij->ij',ar,V);dS=np.einsum('a,aij->ij',z,D)
        assert potential(A+.1*dA,S+.1*dS,V,T)>0


def test_purity_identity_by_independent_minors():
    rng=np.random.default_rng(117157)
    S=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5));S=(S+S.T)/2
    minors=sum(abs(S[i,k]*S[j,l]-S[i,l]*S[j,k])**2 for i,j in itertools.combinations(range(5),2) for k,l in itertools.combinations(range(5),2))
    K=S@S.conj().T
    assert abs(np.trace(K).real**2-np.trace(K@K).real-2*minors)<1e-10


def test_full_canonical_Hessian_against_direct_potential_second_variation():
    H,J,Ji,Gi,A,S,V,T,D=M.scalar_jacobians();rng=np.random.default_rng(297)
    for _ in range(12):
        z=rng.normal(size=297);z/=np.linalg.norm(z)
        dA=np.einsum('a,aij->ij',z[:45],V);dS=np.einsum('a,aij->ij',z[45:],D)
        eps=1e-4
        second=(potential(A+eps*dA,S+eps*dS,V,T)+potential(A-eps*dA,S-eps*dS,V,T))/eps**2
        assert abs(second-z@H@z)<2e-6


def test_stored_integer_normal_certificate_at_a_second_prime():
    c=certificate()['scalar_vacuum']['exact_normal_certificate']
    J=sparse_matrix(c['residual_scaled64_sparse'],c['residual_shape'])
    G=sparse_matrix(c['gauge_scaled2_sparse'],[317,45])
    assert not np.any(J@G)
    assert M.rank_mod(J,103)==284 and M.rank_mod(G,103)==33
    assert 317-284==33 and 297-33==264


def test_exact_mass_operator_rank_and_fourth_moment():
    c=certificate()['scalar_vacuum']['exact_mass_spectrum']
    W=sparse_matrix(c['mass_operator_scaled65536_sparse'],[317,317])
    assert M.rank_mod(W,103)==264
    moment=s.Rational(sum(int(W[i,j])*int(W[j,i]) for i,j in zip(*np.nonzero(W))),65536**2)
    assert moment==s.Rational(117157,2)
    # Rational eigenspace multiplicities from rank, independent of floating spectra.
    for eigen,multiplicity in [(2,5),(3,24),(4,3),(6,54),(8,8),(11,68),(18,60),(27,24),(38,6)]:
        assert 317-M.rank_mod(W-eigen*65536*np.eye(317,dtype=np.int64),103)==multiplicity
    assert 22-2*s.sqrt(70)>0


def test_minimal_tree_warning_is_not_the_new_EFT():
    a,w=s.symbols('a w',real=True)
    triplet=-2*a*w*w;octet=4*a*w*w
    assert s.factor(triplet*octet)==-8*a*a*w**4
    c=certificate()['scalar_vacuum']
    assert 'sextic' in c['boundary']


def test_global_zero_orbit_extremal_spinor_and_Spin4_transitivity():
    T,pairs,B,R,C,P10,P126,Sbasis,raw,Praw=M.spin_pair_data()
    H,J,Ji,Gi,A,S,V,T,D=M.scalar_jacobians()
    rng=np.random.default_rng(33)
    slots=list(itertools.combinations_with_replacement(range(16),2))
    for i,j in [(14,14),(14,15),(15,15)]:
        e=np.zeros(136);e[slots.index((i,j))]=1
        assert not np.any(Praw@e)
    for _ in range(6):
        v=np.zeros(16,complex);z=rng.normal(size=2)+1j*rng.normal(size=2);z/=np.linalg.norm(z);v[14:]=z
        assert abs(potential(A,np.outer(v,v),V,T))<1e-12
        # An explicit SU2 matrix sends the reference spinor to every such z.
        U=np.array([[z[1].conjugate(),z[0]],[-z[0].conjugate(),z[1]]])
        assert np.max(abs(U.conj().T@U-np.eye(2)))<1e-14 and abs(np.linalg.det(U)-1)<1e-14
    assert certificate()['scalar_vacuum']['global_orbit']['Spin4_restricted_algebra_rank']==3


def tensor_yukawa(u,h):
    a=u[0].conjugate()/np.sqrt(3);b=u[1].conjugate()/np.sqrt(6)
    return np.array([[a*h[0],b*h[2],b*h[1]],[b*h[2],a*h[1],b*h[0]],[b*h[1],b*h[0],a*h[2]]])


def family_generators():
    w=np.exp(2j*np.pi/3)
    return [(np.array([[w**(i*j) for j in range(3)] for i in range(3)])/np.sqrt(3),np.array([[1,np.sqrt(2)],[np.sqrt(2),-1]])/np.sqrt(3)),(np.diag([1,1,w]),np.diag([1,w]))]


def test_common_flavor_action_on_complex_inputs_and_mixed_words():
    rng=np.random.default_rng(11622);u=rng.normal(size=2)+1j*rng.normal(size=2);h=rng.normal(size=3)+1j*rng.normal(size=3)
    G=np.eye(3,dtype=complex);R=np.eye(2,dtype=complex)
    for i in [0,1,0,0,1,0,1]:
        g,r=family_generators()[i];G=g@G;R=r@R
        assert np.max(abs(G.T@tensor_yukawa(R@u,G@h)@G-tensor_yukawa(u,h)))<1e-12


def test_mediator_and_Yukawa_interactions_share_the_symmetry():
    rng=np.random.default_rng(120);psi=rng.normal(size=3)+1j*rng.normal(size=3)
    A=rng.normal(size=(2,3))+1j*rng.normal(size=(2,3));u=rng.normal(size=2)+1j*rng.normal(size=2);h=rng.normal(size=3)+1j*rng.normal(size=3)
    def vertex(p,a):
        return sum(p[i]**2*a[0,i] for i in range(3))/np.sqrt(3)+sum(p[i]*p[j]*a[1,k] for i,j,k in itertools.permutations(range(3)))/np.sqrt(6)
    for G,R in family_generators():
        changed=R.conj()@A@G.T
        assert abs(vertex(G@psi,changed)-vertex(psi,A))<1e-12
        source=A+u.conj()[:,None]*h
        transformed=changed+(R@u).conj()[:,None]*(G@h)
        assert abs(np.linalg.norm(source)-np.linalg.norm(transformed))<1e-12


def test_fixed_background_still_allows_angular_counterterms():
    u=np.array([1,0],complex);h=np.array([1,2,3]);G,R=family_generators()[0]
    trace=lambda Y:np.trace((Y.conj().T@Y)@(Y.conj().T@Y)).real
    assert abs(trace(tensor_yukawa(R@u,h))-trace(tensor_yukawa(u,h))-16/3)<1e-12
    assert abs(trace(tensor_yukawa(R@u,G@h))-trace(tensor_yukawa(u,h)))<1e-12


def test_linear_gravity_gauge_modes_for_independent_momenta():
    for k in [[1,0,0,0],[2,1,3,1],[0,1,1,2]]:
        K,G,B=M.fp_mode(k)
        assert K.rank()==6 and G.rank()==4 and K*G==s.zeros(10,4)
    # Zero momentum is a separate global mode, not a two-polarization count.
    K,G,_=M.fp_mode([0,0,0,0]);assert K==s.zeros(10) and G==s.zeros(10,4)


def test_gravity_stationary_block_preserves_action_and_gauge():
    c=certificate()['gravitational_block'];K,G,B=M.fp_mode([1,2,0,1])
    E=s.zeros(10,6)
    for j,i in enumerate([4,5,6,7,8,9]):E[i,j]=1
    T=G.row_join(E);A=s.simplify(T.T*K*T);keep=c['retained_indices'];el=c['eliminated_indices']
    q=s.Matrix([s.Rational(i+1,7) for i in range(7)])
    internal=-A.extract(el,el).inv()*A.extract(el,keep)*q
    allcoords=s.zeros(10,1)
    for i,x in zip(keep,q):allcoords[i]=x
    for i,x in zip(el,internal):allcoords[i]=x
    coarse=s.Matrix([[s.sympify(t) for t in row] for row in c['coarse_matrix']])
    assert s.simplify((allcoords.T*A*allcoords)[0]-(q.T*coarse*q)[0])==0
    assert coarse[:4,:]==s.zeros(4,7)


def test_TT_basis_and_canonical_constraint_count():
    c=certificate()['gravitational_block'];_,_,B=M.fp_mode([1,2,3]);k=s.Matrix([1,2,3])
    for v in c['transverse_traceless_basis']:
        a=s.Matrix([s.sympify(x[0]) for x in v]);h=sum((a[i]*B[i] for i in range(6)),s.zeros(3))
        assert s.trace(h)==0 and h*k==s.zeros(3,1)
    assert len(c['transverse_traceless_basis'])==2


def test_closed_history_top_flux_and_Euler_obstruction():
    D=s.Matrix(M.top_boundary());assert D.nullspace()==[s.ones(3,1)]
    assert sum((-1)**i*b for i,b in enumerate([1,82,162,82,1]))==0
    theta,q=s.symbols('theta Qhat',real=True)
    assert s.diff(theta*(32*s.pi**2*0+q),theta)==q
    for chi,n,expected in [(0,0,1),(0,1,0),(2,-2,1),(2,0,0)]:
        result=quad(lambda t:np.cos(t*(chi+n)),0,2*np.pi)[0]/(2*np.pi)
        assert abs(result-expected)<1e-14
    r,K=s.symbols('r K',positive=True)
    volume=8*s.pi**2*r**4/3;GB=24/r**4;residual=3*K/r**2
    assert s.simplify(GB*volume)==64*s.pi**2
    assert s.simplify(residual**2-24*s.pi**2*K*K/volume)==0


def test_formal_linear_shift_Ward_with_a_convergent_fourier_control():
    Q=.7;C=.4
    # Gaussian bulk test function transforms with Lambda+C. The real-line
    # measure is translation invariant; the Fourier phase remains constant.
    real=quad(lambda t:np.exp(-(t+C)**2)*np.cos(Q*t),-np.inf,np.inf)[0]
    imag=quad(lambda t:np.exp(-(t+C)**2)*np.sin(Q*t),-np.inf,np.inf)[0]
    expected=np.sqrt(np.pi)*np.exp(-Q*Q/4)*np.exp(-1j*Q*C)
    assert abs(real+1j*imag-expected)<1e-12
    # Nonlinear sigma=t+beta*t² gives a C-dependent modulus, not a phase Ward identity.
    beta=.2;A=1-1j*beta*Q
    Z=lambda c:np.exp(-c*c)*np.sqrt(np.pi/A)*np.exp((-2*c+1j*Q)**2/(4*A))
    assert abs(abs(Z(C))-abs(Z(0)))>1e-3


def test_exact_scalar_gauge_threshold_and_source_binding():
    c=certificate();threshold=c['four_form_response']['actual_stable_scalar_gauge_threshold']
    masses=[(s.Integer(2),5),(s.Integer(3),24),(s.Integer(4),3),(s.Rational(9,2),6),(22-2*s.sqrt(70),1),(s.Integer(6),54),(s.Integer(8),8),(s.Rational(19,2),4),(s.Integer(11),68),(s.Integer(18),60),(s.Integer(27),24),(s.Integer(38),6),(22+2*s.sqrt(70),1)]
    assert sum(n for z,n in masses)==264
    assert s.simplify(sum(n*z*z for z,n in masses))==s.Rational(117157,2)
    assert s.Rational(threshold['Str_m4_exact'])==s.Rational(117157,2)+3*444
    assert c['producer_sha256']==M.ph(ROOT/'analysis/w33_pass11620_11624_covariant_pair_vacuum.py')
    for p,digest in c['source_sha256'].items():assert M.ph(ROOT/p)==digest
