"""Independent checks of running, symmetry, optical thresholds and internal index."""
import importlib.util
from pathlib import Path
import sys
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12011_12015_scale_flavour_internal_index as p

def test_analytic_gauge_running_and_flavour_covariance():
    t=7.;g0=p.unpack(p.running().sol(0))[0];gt=p.unpack(p.running().sol(t))[0]
    expect=1/np.sqrt(1/g0**2-2*np.array([41/6,-19/6,-7])*t/(16*np.pi**2))
    assert np.max(abs(gt-expect))<1e-8
    rng=np.random.default_rng(100);W=np.linalg.qr(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))[0]
    g,m=p.unpack(p.running().sol(0));b0=p.unpack(p.beta(0,p.pack(g,m)))[1];rot=[W@z for z in m];br=p.unpack(p.beta(0,p.pack(g,rot)))[1]
    assert max(np.linalg.norm(a-W@b) for a,b in zip(br,b0))<1e-12

def test_running_ratio_beta_and_full_joint_inverse_match():
    g,m=p.unpack(p.running().sol(0));u,d,e=m
    hu=u@u.conj().T;hd=d@d.conj().T;he=e@e.conj().T
    vd=np.linalg.svd(d)[0][:,0];bd=np.linalg.svd(d,compute_uv=False)[0];te=np.linalg.svd(e,compute_uv=False)[0]
    analytic=(1.5*(bd*bd-te*te-np.vdot(vd,hu@vd).real)+10/3*g[0]**2-8*g[2]**2)/(16*np.pi**2)
    dt=1e-4;r0=p.shape_observables(m)[0];r1=p.shape_observables(p.unpack(p.running().sol(dt))[1])[0]
    rh=p.shape_observables(p.unpack(p.running().sol(dt/2))[1])[0]
    richardson=(4*np.log(rh/r0)-np.log(r1/r0))/dt
    assert abs(richardson-analytic)<2e-7
    out=p.rg_matching();assert max(abs(np.array(out['residual'])))<1e-7
    assert out['back_to_MZ_max_relative_error']<1e-7
    assert 1e6<out['matching_scale_GeV']<1e7
    assert out['local_Jacobian_singular_values'][-1]>.001

def test_independent_theta_cutoff_on_new_running_branch():
    x=p.RG_FIT;yy,eu=np.exp(x[:2]);v=x[2:10];tau=1+1j*yy
    Ou=np.array([[tau,1j*eu],[1j*eu,tau]]);Od=np.array([[tau,1j*v[1]],[1j*v[1],1j*np.exp(v[0])]])
    def direct(O,z):
        a,b=np.meshgrid(np.arange(-12,13),np.arange(-12,13),indexing='ij');out=np.zeros((3,3),complex)
        for i in range(3):
            for j in range(3):
                r=a+i/3;s=b+j/3;out[i,j]=np.exp(3j*np.pi*(O[0,0]*r*r+2*O[0,1]*r*s+O[1,1]*s*s)+6j*np.pi*s*z).sum()
        return out
    assert np.max(abs(direct(Ou,0)-p.theta(Ou)))<1e-13
    assert np.max(abs(direct(Od,1j*v[2])-p.theta(Od,(0,1j*v[2]))))<1e-13

def test_stabilizer_second_basis_and_degenerate_negative_control():
    mats=p.theta_matrices(p.RG_FIT)[:3];a=p.stabilizer(mats)
    W=expm(1j*np.array([[.2,.3j,.4],[-.3j,-.2,.1j],[.4,-.1j,0]]))
    b=p.stabilizer([W@m for m in mats])
    assert a['U3_commutant_real_dimension']==b['U3_commutant_real_dimension']==1
    assert np.allclose(a['up_Gram_eigenvalues'],b['up_Gram_eigenvalues'],atol=1e-12)
    assert abs(a['normalized_CP_odd_cubic']-b['normalized_CP_odd_cubic'])<1e-16
    # Identical diagonal Grams have a three-dimensional U3 commutant.
    H=np.diag([1,2,4]);cols=[]
    for A in p.hermitian_basis(3):
        C=A@H-H@A;cols.append(np.r_[C.real.ravel(),C.imag.ravel()])
    assert np.linalg.matrix_rank(np.array(cols).T)==6

def test_nonuniversal_spectral_alignment_random_mass_and_basis():
    rng=np.random.default_rng(13);M=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));Sq=p.spectral_soft(M)
    result=p.colored_phase(M,Sq);assert abs(result['sum'])<1e-11
    U=np.linalg.qr(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))[0];V=np.linalg.qr(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))[0]
    T=np.zeros((8,8),complex);T[:4,:4]=U;T[4:,4:]=V
    assert np.linalg.norm(p.spectral_soft(U@M@V.conj().T)-T@Sq@T.conj().T)<1e-10
    assert abs(p.colored_phase(U@M@V.conj().T,T@Sq@T.conj().T)['sum'])<1e-11

def test_misalignment_conjugation_and_strong_phase_control():
    a=p.spurion_alignment();assert abs(a['misaligned_control']['sum'])>1e-10
    rng=np.random.default_rng(131);M=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));S=p.spectral_soft(M);E=.01*np.arange(16).reshape(4,4)*M;S[:4,4:]+=E;S[4:,:4]+=E.conj().T
    a=p.colored_phase(M,S);b=p.colored_phase(M.conj(),S.conj())
    assert abs(a['sum']+b['sum'])<1e-11

def test_proper_time_quadrature_and_native_species_decoupling():
    ev=p.tree_eigenvalues();assert len(ev)==27 and ev[1]>.1
    for kappa in [.1,1.]:
        x=kappa*ev
        numerical2=quad(lambda t:sum(np.exp(-x*t))/t**2,1,np.inf,epsabs=1e-9)[0]
        numerical3=quad(lambda t:sum(np.exp(-x*t))/t**3,1,np.inf,epsabs=1e-9)[0]
        assert abs(numerical2-sum(p.expn(2,x)))<1e-8
        assert abs(numerical3-sum(p.expn(3,x)))<1e-8
    rows=p.induced_scale()['rows'];assert rows[0]['curvature_effective_species']==27
    assert rows[-1]['curvature_effective_species']==1
    assert rows[-1]['absolute_vacuum_over_reduced_Planck_fourth']>1000
    # With conformal scalar coupling, the induced scalar R coefficient vanishes.
    assert (1-6*(1/6))*sum(p.expn(2,ev))==0

def test_internal_index_zero_mode_chirality_and_GW():
    cells,idx,U,S,g5,D,ev,Do,z,K=p.internal_flux()
    assert K.shape==(72,3) and min(abs(ev))>.7
    assert np.linalg.norm(g5@Do+Do@g5-Do@g5@Do)<1e-11
    assert np.linalg.norm(Do@K)<1e-11
    assert np.allclose(np.linalg.eigvalsh(K.conj().T@g5@K),[-1]*3,atol=1e-11)
    reverse=p.internal_flux(charge=-3);assert int(-sum(np.sign(reverse[6]))/2)==3
    trivial=p.internal_flux(charge=0);assert int(-sum(np.sign(trivial[6]))/2)==0

def test_internal_magnetic_action_irreducible_and_gauge_covariant():
    cells,idx,U,S,g5,D,ev,Do,z,K=p.internal_flux();X=p.magnetic_translation(cells,idx,U,(2,0));Y=p.magnetic_translation(cells,idx,U,(0,2))
    x=K.conj().T@np.kron(np.eye(2),X)@K;y=K.conj().T@np.kron(np.eye(2),Y)@K
    assert np.linalg.norm(x@y-np.exp(-2j*np.pi/3)*y@x)<1e-11
    cols=[]
    for A in p.hermitian_basis(3):
        C=np.r_[(A@x-x@A).ravel(),(A@y-y@A).ravel()];cols.append(np.r_[C.real,C.imag])
    assert np.linalg.matrix_rank(np.array(cols).T,tol=1e-9)==8
    rng=np.random.default_rng(15);phase=np.diag(np.exp(1j*rng.normal(size=36)));G=np.kron(np.eye(2),phase);Dg=G.conj().T@D@G;Kg=G.conj().T@K
    assert np.linalg.norm(Dg@(G.conj().T@np.kron(np.eye(2),X)@G)-(G.conj().T@np.kron(np.eye(2),X)@G)@Dg)<1e-11
    assert np.linalg.norm(Kg.conj().T@(G.conj().T@np.kron(np.eye(2),X)@G)@Kg-x)<1e-11

def test_sm_embedding_center_wedge_and_representation_bound():
    out=p.measure_restriction();assert sorted(out['ten_integer_6Y_charges'])==[-4]*3+[1]*6+[6]
    rng=np.random.default_rng(155)
    for _ in range(5):
        A=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5));A=(A+A.conj().T)/2;A-=np.trace(A)*np.eye(5)/5;V=expm(1j*A)
        assert np.linalg.norm(p.wedge2(V).conj().T@p.wedge2(V)-np.eye(10))<1e-11
        assert np.linalg.norm(p.wedge2(V)-np.eye(10),2)<=2*np.linalg.norm(V-np.eye(5),2)+1e-11
        c=p.sm_embedding(np.exp(2j*np.pi/3)*np.eye(3),-np.eye(2),np.exp(1j*np.pi/3));assert np.linalg.norm(np.linalg.matrix_power(c,6)-np.eye(5))<1e-11

def test_certificate_scopes_and_frozen_witness():
    import json
    data=json.loads((ROOT/'data/w33_pass12011_12015_scale_flavour_internal_index.json').read_text())
    assert data['status']=='PASS' and data['pass12015']['zero_modes']==3
    assert 'NOT a prediction' in data['pass12011']['boundary']
    assert 'EXTERNAL' in data['pass12015']['family_reading']
    assert 'NOT automatically an ultraviolet' in data['pass12013']['group_action']
