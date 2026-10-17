"""Independent matrix/path controls for the five explicitly conditional constructions."""
import sys,json,itertools
from pathlib import Path
import numpy as np
import sympy as s
from scipy.linalg import eigh,null_space
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12000_native_unitary_clock as clock
import w33_pass11995_native_metric_gr_lift as metric
import w33_pass12001_radial_portal_decoupling as portal
import w33_pass12002_native_path_overlap as overlap
import w33_pass12003_h27_decuplet_mass27 as family
from w33_pass11991_native_four_period_cover import gamma4

def read(stem):return json.loads((ROOT/'data'/('w33_pass'+stem+'.json')).read_text())

def test_literal_native_period_paths_and_inverse():
    edges,V,paths,tree,T,words=clock.native_paths()
    assert len(tree)==26 and abs(T.det())==1
    for j,w in enumerate(words):
        for word,sign in [(w,1),([(e,-v) for e,v in reversed(w)],-1)]:
            a=0;vol=np.zeros(4,int)
            for e,v in word:
                x,y=edges[e];assert a==(x if v>0 else y)
                a=y if v>0 else x;vol+=v*V[e]
            assert a==0 and np.array_equal(vol,sign*np.array(T[:,j],int).ravel())
    assert s.Matrix([[3,0,2,1]])*T==s.Matrix([[1,0,0,0]])

def test_actual_unitary_clifford_limit_and_doubling_control():
    gamma,_=gamma4();k=np.array([.19,-.27,.31]);m=.23
    H=sum((q*g for q,g in zip(k,gamma)),m*gamma[3])
    assert np.max(abs(H@H-(k@k+m*m)*np.eye(4)))<1e-13
    errors=[]
    for a in [.02,.01,.005]:
        U=clock.update(a*k,a*m)
        assert np.linalg.norm(U.conj().T@U-np.eye(4))<1e-13
        errors.append(np.linalg.norm((np.eye(4)-U)/(1j*a)-H))
    assert errors[-1]<errors[0]/3
    nodes=sum(np.linalg.norm(clock.update(np.pi*np.array(bits))-np.eye(4))<1e-10 for bits in itertools.product([0,1],repeat=3))
    assert nodes==4
    assert np.linalg.norm((.99*U).conj().T@(.99*U)-np.eye(4))>.01

def test_ADM_jacobian_against_recomputed_native_corrector():
    d=read('11999_native_adm_weights');J=np.array(s.Matrix(d['exact_selected_edge_ADM_jacobian']),float)
    b,v,_,_=metric.inputs();T=np.array(clock.native_paths()[4],float);Ti=np.linalg.inv(T);u=np.array([3.,0,2,1])
    def q(w):
        G=metric.homogenize(w,b,v)[0];K=Ti@(G-2*np.outer(G@u,G@u)/(u@G@u))@Ti.T;g=np.linalg.inv(K)
        return np.r_[-1/K[0,0],-K[0,1:]/K[0,0],[g[i+1,j+1] for i,j in itertools.combinations_with_replacement(range(3),2)]]
    sel=read('11995_native_metric_gr_lift')['selected_edge_indices'];rng=np.random.default_rng(2);dw=rng.normal(size=10);delta=np.zeros(135);delta[sel]=dw
    step=1e-5;fd=(q(1+step*delta)-q(1-step*delta))/(2*step)
    assert np.max(abs(fd-J@dw))<1e-8

def test_ADM_canonical_form_primary_nulls_and_physical_modes():
    d=read('11999_native_adm_weights');J=s.Matrix(d['exact_selected_edge_ADM_jacobian']);W=s.Matrix(d['spatial_DeWitt_form_Q'])
    Q=s.zeros(10);Q[4:,4:]=W;B=J.T*Q*J;Z=s.Matrix(d['exact_primary_null_directions_Q'])
    assert B.rank()==6 and B*Z==s.zeros(10,4)
    p=s.Matrix(range(10));dw=s.Matrix(range(1,11));assert (p.T*J*dw)[0]==((J.T*p).T*dw)[0]
    tt=s.Matrix(d['exact_TT_kinetic_form']);assert tt.shape==(2,2) and tt[0,0]>0 and tt.det()>0
    assert 'Suppliedcontinuum' in d['explicit_action']

def test_fixed_norm_portal_projection_and_actual_threshold():
    x,H,M,Y,r=portal.inputs();v=np.r_[.2*x[:6],np.zeros(12)]
    K=np.block([[np.array([[25.]]),v[None,:]],[v[:,None],H+np.outer(v,v)/25]])
    baseline,_=portal.threshold(K,M,Y);assert abs(baseline)>1e-5
    T=null_space(r[None,:]);P=np.zeros((19,18));P[0,0]=1;P[1:,1:]=T
    assert np.linalg.norm((P.T@K@P)[0,1:])<1e-12
    vertices=np.einsum('ia,ijk->ajk',P,Y);theta,_=portal.threshold(P.T@K@P,M,vertices)
    assert abs(theta)<1e-12
    assert abs(read('12001_radial_portal_decoupling')['radial_scan'][-1]['theta'])>1e-10

def test_Barr_trace_identities_beyond_one_spectral_matrix():
    _,_,M,Y,_=portal.inputs();rng=np.random.default_rng(12)
    for _ in range(4):
        z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));F=z+z.conj().T
        theta=np.trace(np.linalg.solve(M,Y[0]@F@M.conj().T@Y[0]))
        assert abs(theta.imag)<1e-12
        G=np.einsum('i,ijk->jk',rng.normal(size=18),Y[1:])
        correction=G@F@M.conj().T@G
        assert np.max(abs(correction[:3,:]))==0 and np.max(abs(correction[:,3]))==0
        # Triangular solve avoids cancellation in a generic pivoted solver.
        from scipy.linalg import solve_triangular
        assert abs(np.trace(solve_triangular(M,correction,lower=True)))<1e-12
    z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));U,_=np.linalg.qr(z);h=rng.normal(size=3)+1j*rng.normal(size=3)
    assert abs(np.vdot(U@h,U@h)-np.vdot(h,h))<1e-12

def test_native_path_factorization_new_volume_and_links():
    rng=np.random.default_rng(29);periods=np.array([2,1,2,1]);phi=rng.uniform(-.1,.1,(4,135))
    cells,S,C,L,L0,U,R=overlap.path_fields(phi,periods)
    assert R==23 and len(cells)==4
    for a,b in zip(S,C):assert np.max(abs(a-U.conj().T@np.kron(b,np.eye(27))@U))<1e-12
    assert np.max(abs(L-U.conj().T@np.kron(np.eye(4),L0)@U))<1e-12
    assert np.linalg.eigvalsh(L0)[1]>1/729

def test_Wilson_free_identity_away_from_corners_and_optical_gap():
    gamma,g5=gamma4();rng=np.random.default_rng(3)
    for _ in range(9):
        k=rng.uniform(-np.pi,np.pi,4);r=1-np.cos(k)
        D=(sum(r)-1)*np.eye(4)+1j*sum((np.sin(q)*g for q,g in zip(k,gamma)),np.zeros((4,4),complex))
        Q=g5@D;expected=1+2*sum(a*b for a,b in itertools.combinations(r,2))
        assert np.max(abs(Q@Q-expected*np.eye(4)))<1e-12
        assert min(abs(np.linalg.eigvalsh(Q)))>=1-1e-12
    d=read('12002_native_path_overlap');assert d['uniform_native_weak_phase_radius_maxcharge6']==d['uniform_native_weak_phase_radius_charge1']/6

def test_heavy_frame_onsite_reference_and_large_gauge_covariance():
    rng=np.random.default_rng(92);n=3;C=[]
    for _ in range(4):
        z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));q,_=np.linalg.qr(z);C.append(q)
    D,G5=overlap.wilson(C);F,E,gap=overlap.heavy_frame(D,G5,4.,steps=24)
    assert gap>=3-1e-12
    gauge=np.kron(np.eye(4),np.diag(np.exp(1j*rng.uniform(-3,3,n))))
    assert np.linalg.norm(gauge@(E@E.conj().T)-(E@E.conj().T)@gauge)<1e-13
    Fg,_,_=overlap.heavy_frame(gauge.conj().T@D@gauge,G5,4.,steps=24)
    assert np.max(abs(Fg-gauge.conj().T@F@(E.conj().T@gauge@E)))<1e-11
    P,_=overlap.projector(G5@(D+4*np.eye(4*n)));assert np.linalg.norm(F@F.conj().T-P)<1e-11

def test_exact_27_mass_channel_and_continuous_stabilizer():
    d=read('12003_h27_decuplet_mass27');N=s.Matrix(d['explicit_integer_mass_N']);A=family.multiplication_matrix()
    assert A*s.Matrix([N[i,j] for i,j in family.PAIRS])==s.zeros(28,1)
    assert N.det()==1882576080 and N.rank()==10
    variations=[(T*N+N*T.T).reshape(100,1) for T in family.poly_generators()]
    assert s.Matrix.hstack(*variations).rank()==8
    perm=[family.EXP.index((e[2],e[0],e[1])) for e in family.EXP];X=s.zeros(10)
    for i,j in enumerate(perm):X[j,i]=1
    assert X*N*X.T==N
    for i,j in family.PAIRS:
        if N[i,j]:assert sum(family.EXP[a][1]+2*family.EXP[a][2] for a in (i,j))%3==0

def test_optional_SUSY_D_cancellation_and_extra_U1_anomaly():
    d=read('12003_h27_decuplet_mass27');M=s.Matrix(d['physical_mass_matrix']);vec=M.reshape(100,1)
    # Dual conjugate VEV cancels every moment map; this does not select M.
    for T in family.poly_generators():
        weights=s.diag(*[s.sqrt(v) for v in d['multinomial_normalizations']]);H=weights.inv()*T*weights
        gen=s.kronecker_product(H,s.eye(10))+s.kronecker_product(s.eye(10),H)
        first=(vec.conjugate().T*gen*vec)[0];dual=-(vec.T*gen.conjugate()*vec.conjugate())[0]
        assert s.simplify(first+dual)==0
    assert d['optional_SUSY_mass_sector_flat_complex_moduli']==54-1-8
    # Natural U3 charges are +1 on 81 matter and -3 on bar10: SU3 repair
    # alone does not cancel the central mixed gravitational anomaly.
    assert 81-3*10==51
