"""Independent controls of objects, relaxed fields, physical loops and boundaries."""
import json
from pathlib import Path
import sys

import numpy as np
import sympy as s
from scipy.integrate import quad

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11664_11671_kernel_dynamics as M
import w33_pass11663_odd_weil_normal_map as N


def certificate():
    return json.loads(M.OUT.read_text())


def test_frozen_source_bindings_and_all_eight_boundaries():
    d=certificate();assert d['status']=='PASS'
    assert d['producer_sha256']==M.digest(M.__file__)
    for p,h in d['sources'].items():assert M.digest(ROOT/p)==h
    assert set(d['passes'])=={str(i) for i in range(11664,11672)}
    for n,p in d['passes'].items():
        assert p['status']=='PASS'
        assert p.get('scope',p.get('bilinear_boundary'))


def test_exact_g25_is_the_prior_group_and_h27_is_irreducible():
    group=M.exact_kernel_group();assert len(group)==648
    rs=dict((n,R) for n,R,_ in M.kernel_generators())
    X,Z=rs['SUM01'],rs['CZ']
    assert (Z*X-N.W*X*Z).applyfunc(N.reduce_w)==s.zeros(3)
    assert (Z*X-X*Z).applyfunc(N.reduce_w)!=s.zeros(3)
    # Actual invariant bilinear equations, independent of the central shortcut.
    b=s.symbols('b0:9');B=s.Matrix(3,3,b)
    center=rs['D0']
    assert s.linsolve(list((center.T*B*center-B).applyfunc(N.reduce_w)),b)==s.FiniteSet((0,)*9)


def test_same_kernel_and_transverse_triplet_in_a_second_basis():
    rng=np.random.default_rng(641)
    U,_=np.linalg.qr(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))
    embed=np.eye(5)[:,2:];odd=np.eye(4)[:,1:]
    E,O=N.parity_bases();en=np.array(E,complex)@np.diag([1,*([1/np.sqrt(2)]*4)])
    on=np.array(O,complex)/np.sqrt(2)
    for name,gate in N.canonical_generators().items():
        if name=='F0':continue
        g=np.array(gate.subs(N.W,np.exp(2j*np.pi/3)),complex)
        a=U.conj().T@embed.T@(en.conj().T@g@en)@embed@U
        b=U.conj().T@odd.T@(on.conj().T@g@on)@odd@U
        assert np.allclose(a,b)
    mass=N.canonical_mass([1,0,0,0]);assert np.linalg.norm(mass@embed@U)==0


def test_parent_maps_are_full_polarization_not_a_radial_approximation():
    f,q,z,Q,P=M.parent_maps()
    _,_,K=N.cubic_normal_map();F=N.pfaffian_vector(K)
    pairs=list(__import__('itertools').combinations_with_replacement(range(4),2))
    basis=[]
    for i,j in pairs:
        a=s.zeros(4);a[i,j]=a[j,i]=1/s.sqrt(2) if i!=j else 1;basis.append(a)
    # Independent contraction of every symmetric four-index tensor component.
    for k in range(5):
        projected=0
        for idx in __import__('itertools').product(range(4),repeat=4):
            t=s.diff(F[k],*[f[i] for i in idx])/24
            if not t:continue
            i,j,l,m=idx
            projected+=t*sum(q[a]*basis[a][i,j] for a in range(10))*sum(q[a]*basis[a][l,m] for a in range(10))
        assert s.expand(s.sqrt(N.G[k,k])*projected-P[k])==0
    corrupted=P.copy();corrupted[0]+=q[1]*q[8]
    assert any(s.expand(v) for v in corrupted.subs(dict(zip(q,Q)),simultaneous=True)-s.diag(1,*([s.sqrt(2)]*4))*F)


def test_all_forty_parent_hessians_and_relaxed_schur_curvature():
    f,q,z,Q,P=M.parent_maps();H,low=M.parent_hessian()
    vals=np.linalg.eigvalsh(np.array(H,float))
    assert abs(vals[0])<1e-12 and min(vals[1:])>.1
    assert low==s.diag(8,0,*([s.Rational(8,3)]*6))
    # Complex holomorphic residual derivatives checked across all40 actual rays.
    dq=s.lambdify([list(f)],Q.jacobian(f),'numpy');dp=s.lambdify([list(q)],P.jacobian(q),'numpy');qfun=s.lambdify([list(f)],Q,'numpy')
    _,rays=N.witting_pauli_dictionary(N.exact_base_rays())
    def real(a):
        r=np.empty((2*a.shape[0],2*a.shape[1]));r[0::2,0::2]=r[1::2,1::2]=a.real
        r[0::2,1::2]=-a.imag;r[1::2,0::2]=a.imag;return r
    for ray in rays:
        aa=np.hstack([-dq(ray),np.eye(10),np.zeros((10,5))])
        bb=np.hstack([np.zeros((5,4)),-dp(qfun(ray).ravel()),np.eye(5)])
        cc=np.hstack([np.zeros((5,14)),np.eye(5)])
        jac=real(np.vstack([aa,bb,cc]));rad=np.zeros(38);rad[:8]=2*np.array([[v.real,v.imag] for v in ray]).ravel()
        hh=2*(jac.T@jac+np.outer(rad,rad))
        assert np.allclose(np.linalg.eigvalsh(hh),vals,atol=1e-10)
        eff=hh[:8,:8]-hh[:8,8:]@np.linalg.solve(hh[8:,8:],hh[8:,:8])
        assert np.allclose(np.linalg.eigvalsh(eff),[0,*([8/3]*6),8])


def test_parent_covariance_on_independent_auxiliary_fields():
    f,q,z,Q,P=M.parent_maps();pairs=list(__import__('itertools').combinations_with_replacement(range(4),2))
    pf=s.lambdify([list(q)],P,'numpy');E,O=N.parity_bases()
    en=np.array(E,complex)@np.diag([1,*([1/np.sqrt(2)]*4)]);on=np.array(O,complex)/np.sqrt(2)
    rng=np.random.default_rng(652);q0=rng.normal(size=10)+1j*rng.normal(size=10)
    tensor=np.zeros((4,4),complex)
    for value,(i,j) in zip(q0,pairs):tensor[i,j]=tensor[j,i]=value/(np.sqrt(2) if i!=j else 1)
    assert np.linalg.matrix_rank(tensor)==4  # deliberately outside Veronese.
    for gate in N.canonical_generators().values():
        g=np.array(gate.subs(N.W,np.exp(2j*np.pi/3)),complex)
        go=on.conj().T@g@on;ge=en.conj().T@g@en
        t=go@tensor@go.T
        qq=np.array([t[i,j]*(np.sqrt(2) if i!=j else 1) for i,j in pairs])
        assert np.allclose(np.linalg.norm(qq),np.linalg.norm(q0))
        assert np.allclose(pf(qq).ravel(),ge@pf(q0).ravel())


def test_bare_skew_yukawas_cannot_produce_three_mass_splittings_or_cp():
    rng=np.random.default_rng(665)
    def skew(v):
        a,b,c=v;return np.array([[0,-c,b],[c,0,-a],[-b,a,0]])
    for _ in range(20):
        v,w=rng.normal(size=(2,3))+1j*rng.normal(size=(2,3))
        a,b=skew(v),skew(w);H=a.conj().T@a;G=b.conj().T@b
        assert np.allclose(np.linalg.eigvalsh(H),[0,np.vdot(v,v).real,np.vdot(v,v).real])
        c=H@G-G@H;assert abs(np.trace(c@c@c))<1e-10


def test_actual_e6_yukawa_lift_and_cp_basis_covariance():
    data=certificate()['passes']['11666'];e=s.Symbol('epsilon',real=True)
    a=np.array(s.Matrix(data['Y1']),complex);b=np.array(s.Matrix(data['Y2']),complex)
    rng=np.random.default_rng(666);U,_=np.linalg.qr(rng.normal(size=(5,5))+1j*rng.normal(size=(5,5)))
    eta=.1;eps=.01;embed=np.eye(5)[:,2:];base=N.canonical_mass([1,0,0,0])
    x=base+eta*embed@a@embed.T;y=base+eta*embed@(a+eps*b)@embed.T
    def inv(x,y):
        A=x.conj().T@x;B=y.conj().T@y;C=A@B-B@A;return np.trace(C@C@C).imag
    want=eta**12*float(s.sympify(data['exact_light_CP'],locals={'epsilon':e}).subs(e,eps))
    assert abs(want)>1e-15
    assert np.isclose(inv(x,y),want,rtol=1e-9,atol=1e-20)
    assert np.isclose(inv(U.T@x@U,U.T@y@U),want,rtol=1e-7,atol=1e-20)
    assert np.linalg.matrix_rank(x)==5 and np.linalg.matrix_rank(y)==5
    assert abs(inv(x,x))<1e-20


def test_yukawa_completion_and_vacuum_stability_in_the_same_action():
    data=certificate()['passes']['11666'];p=data['joint_vacuum']
    a=np.array(s.Matrix(data['Y1']),complex);b=np.array(s.Matrix(data['Y2']),complex);U=np.eye(5)[:,2:]
    Ys=[p['eta']*U@a@U.T,p['eta']*U@(a+p['epsilon']*b)@U.T]
    x=np.zeros(8);x[0]=np.sqrt(p['squared_radius']);delta=1e-4
    V=lambda z:M.joint_flavor_potential(z,Ys);v=V(x);H=np.zeros((8,8))
    for i in range(8):
        ei=np.eye(8)[i]*delta;H[i,i]=(V(x+ei)+V(x-ei)-2*v)/delta**2
        for j in range(i):
            ej=np.eye(8)[j]*delta
            H[i,j]=H[j,i]=(V(x+ei+ej)-V(x+ei-ej)-V(x-ei+ej)+V(x-ei-ej))/(4*delta**2)
    assert np.allclose(np.linalg.eigvalsh(H),p['Hessian'],atol=1e-7)
    assert min(p['Hessian'][1:])>2e-4 and abs(p['Hessian'][0])<1e-11
    assert p['gradient_norm']<1e-11 and p['quadrature_operator_norm_error']<1e-10
    assert min(p['light_up'])>0 and min(p['light_down'])>0


def test_native_graph_and_connection_preserve_constraints():
    P,B,L,Us,hop,H,cs,physical,tree=M.native_connection()
    assert np.array_equal(P@B@B.T@P.T,B@B.T)
    assert len(tree)==79 and np.linalg.matrix_rank(L)==79
    W=np.zeros((240,240))
    for j,u in enumerate(Us):W[80*j:80*(j+1),80*j:80*(j+1)]=u
    for c in cs:
        assert np.array_equal(c@physical,np.zeros((6,6)))
        assert np.array_equal(physical@c,np.zeros((6,6)))
    # A generic transported constraint intertwines hopping; wrong ungated
    # branch links fail, which distinguishes the statement from commuting
    # site-independent fiber projectors alone.
    A=np.diag(np.arange(80));C=W@np.kron(np.eye(3),A)@W.T
    assert np.linalg.norm(C@hop-hop@C)<1e-12
    wrong=np.kron(np.ones((3,3))-np.eye(3),np.eye(80))
    assert np.linalg.norm(C@wrong-wrong@C)>1


def test_flux_shift_covariance_and_boundary_of_fixed_sector_ward():
    n,U,S=M.flux_operators(C=.71,q=.3,alpha=.8,size=7)
    phase=np.exp(1j*.71*.3/.8)
    assert np.allclose(U.conj().T@S@U,phase*S)
    assert not np.allclose(U.conj().T@S@U,S)
    assert not np.allclose(S.conj().T@S,np.eye(7))  # no artificial periodic flux.
    psi=np.ones(7)/np.sqrt(7)
    rotated=U@S@U.conj().T
    assert np.allclose(np.vdot(U@psi,rotated@(U@psi)),np.vdot(psi,S@psi))
    assert np.allclose(abs(U@psi)**2,abs(psi)**2)


def test_radius_free_loop_against_independent_dirac_inventory():
    rng=np.random.default_rng(669)
    for _ in range(8):
        f=rng.normal(size=4)+1j*rng.normal(size=4);f*=rng.uniform(.2,2)/np.linalg.norm(f)
        r=np.vdot(f,f).real;t=N.order_parameter(f)/r**4
        masses=np.linalg.svd(N.canonical_mass(f),compute_uv=False)**2
        independent=-2*sum(quad(lambda x:x*np.log1p(.2**2*mu/x),.01,.25,epsabs=1e-14)[0] for mu in masses)/(16*np.pi**2)
        assert abs(independent-M.full_loop(r,t))<1e-13


def test_exact_sufficient_global_radial_conditions_and_eight_real_hessian():
    p=certificate()['passes']['11669']['benchmark'];r=p['squared_radius'];lam=p['lambda_'];kap=p['kappa']
    assert abs(M.radial_derivatives(r)[0])<1e-12 and r>1
    assert kap>p['global_kappa_bound']>p['local_kappa_threshold']
    # Independent finite differences of the full 8-coordinate mass determinant.
    def V(x):
        f=x[0::2]+1j*x[1::2];rr=np.vdot(f,f).real
        return lam*(rr-1)**2+kap*N.order_parameter(f)+M.full_loop(rr,N.order_parameter(f)/rr**4)
    x=np.zeros(8);x[0]=np.sqrt(r);delta=2e-4;h=np.zeros((8,8));v=V(x)
    for i in range(8):
        ei=np.eye(8)[i]*delta;h[i,i]=(V(x+ei)+V(x-ei)-2*v)/delta**2
        for j in range(i):
            ej=np.eye(8)[j]*delta;h[i,j]=h[j,i]=(V(x+ei+ej)-V(x+ei-ej)-V(x-ei+ej)+V(x-ei-ej))/(4*delta**2)
    assert np.allclose(np.linalg.eigvalsh(h),sorted(p['all_real_hessian']),atol=8e-7)
    for rr in [.01,.5,1.,2.,10.]:
        orientation=np.linspace(0,1,21)
        energy=[kap*rr**4*t+M.full_loop(rr,t) for t in orientation]
        assert np.all(np.diff(energy)>0)


def test_full_radial_second_bound_and_orientation_log_divergence():
    # This checks the inequality used in the global proof and its inventory.
    for r in np.logspace(-4,4,31):
        _,second=M.radial_derivatives(r)
        assert abs(second-2)<=.2**2*(.25-.01)/(4*np.pi**2)+1e-12
    # UV derivative per logarithmic shell tends to the required S counterterm.
    lo,hi=1e5,1e6;y=.2
    derivative=-y**4*quad(lambda x:x/(x*x+y*y*x/2),lo,hi)[0]/(64*np.pi**2)
    expected=-y**4*np.log(hi/lo)/(64*np.pi**2)
    assert np.isclose(derivative,expected,rtol=1e-6)


def test_nonflat_wilson_phase_survives_frame_changes():
    W,H=M.wilson_hamiltonian();rng=np.random.default_rng(670)
    frames=[]
    for _ in range(3):
        a,_=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)));frames.append(a)
    D=np.zeros((6,6),complex)
    for j,u in enumerate(frames):D[2*j:2*j+2,2*j:2*j+2]=u
    H2=D@H@D.conj().T
    assert np.allclose(np.linalg.eigvalsh(H2),np.linalg.eigvalsh(H))
    assert np.linalg.eigvalsh(H)[0]>.4
    _,flat=M.wilson_hamiltonian(0)
    assert abs(np.linalg.eigvalsh(flat)[0])<1e-12
    assert abs(np.trace(W)-2)>1


def test_zero_mode_bundle_has_no_base_points_and_degree_four():
    A,B,pol=M.band_line();assert max(p.degree() for p in pol)==4
    assert s.Poly(s.gcd_list([p.as_expr() for p in pol]),pol[0].gens[0]).degree()==0
    rng=np.random.default_rng(671)
    for _ in range(15):
        z=rng.normal()+1j*rng.normal();f=np.array(A,complex).ravel()+z*np.array(B,complex).ravel()
        mm=N.canonical_mass(f);v=np.diag(np.sqrt(np.diag(np.array(N.G,float))))@N.quartic(f)
        assert np.linalg.norm(mm@v)<1e-8*np.linalg.norm(v)
        assert np.linalg.matrix_rank(mm,tol=1e-9)==4
    coarse,overlap=M.berry_charge(64,128);fine=certificate()['passes']['11671']['numerical_Berry_charge']
    assert abs(coarse+4)<1e-8 and abs(fine+4)<1e-8 and overlap>.1
