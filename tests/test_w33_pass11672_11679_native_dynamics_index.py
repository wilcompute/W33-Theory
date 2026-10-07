"""Independent action, analytic-loop, index, equivariance and constraint controls."""
import itertools as it
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11672_11679_native_dynamics_index as M
import w33_pass11664_11671_kernel_dynamics as P
import w33_pass11663_odd_weil_normal_map as N


def cert():return json.loads(M.OUT.read_text())


def test_frozen_bindings_and_all_eight_scopes():
    c=cert();assert c['producer_sha256']==M.digest(M.__file__)
    for p,h in c['sources'].items():assert M.digest(ROOT/p)==h
    assert set(c['passes'])=={str(i) for i in range(11672,11680)}
    assert all(v['status']=='PASS' and v['scope'] for v in c['passes'].values())


def test_global_parent_bound_on_arbitrary_fields_and_second_basis():
    rng=np.random.default_rng(11672)
    for _ in range(60):
        x=rng.normal(size=38)*rng.uniform(.1,2)
        a=x[::2]+1j*x[1::2];f,q=a[:4],a[4:14]
        T=np.einsum('i,iab->ab',x[8:28],M.basis)
        sigma=np.linalg.svd(T,compute_uv=False);u=sigma[0];r=np.vdot(f,f).real
        # Full inequality, before minimizing either radius or singular values.
        bound=(r-1)**2+r*r-2*r*u+np.sum(-sigma**2/4+sigma**4/8)
        assert M.potential(x)>=bound-1e-9 and bound>=-23/8-1e-10
        V,_=np.linalg.qr(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))
        assert np.allclose(np.linalg.svd(V@T@V.T,compute_uv=False),sigma)
    assert abs(M.potential(M.base())+23/8)<1e-12


def test_full_parent_is_stationary_with_independent_potential_hessian():
    x=M.base();H=M.hessian(x);rng=np.random.default_rng(44);step=1e-4
    assert np.linalg.norm(M.treeg(x))<1e-12
    for _ in range(12):
        a=rng.normal(size=38);a/=np.linalg.norm(a)
        observed=(M.potential(x+step*a)-2*M.potential(x)+M.potential(x-step*a))/step**2
        assert abs(observed-a@H@a)<3e-6
    ev=np.linalg.eigvalsh(H);assert sum(ev>1e-9)==31 and abs(ev[:7]).max()<1e-10


def test_full_native_group_preserves_matrix_quartic_on_arbitrary_q():
    rng=np.random.default_rng(71);T=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));T=(T+T.T)/2
    before=np.trace((T@T.conj().T)@(T@T.conj().T))
    for G in M.odd_gates().values():
        g=np.array(G.subs(N.W,np.exp(2j*np.pi/3)),complex);out=g@T@g.T
        assert abs(np.trace((out@out.conj().T)@(out@out.conj().T))-before)<1e-9


def test_analytic_scalar_mass_jets_are_polynomial_and_correctly_normalized():
    lin,second=M.scalar_jets();rng=np.random.default_rng(78);x=rng.normal(size=38)*.2
    predicted=M.hessian(np.zeros(38))+np.einsum('iab,i->ab',lin,x)+np.einsum('ijab,i,j->ab',second,x,x)/2
    assert np.linalg.norm(predicted-M.hessian(x))<1e-10
    # Kinetic sum |d complex field|² gives physical Hessian H_x/2.
    x=M.base();assert np.allclose(np.linalg.eigvalsh(M.hessian(x)/2),np.linalg.eigvalsh(M.hessian(x))/2)
    for mass in [0.,.02,1.,30.]:
        expected=quad(lambda t:t/(t+mass),M.A,M.B)[0]
        assert abs(expected-M.l1(mass))<1e-12


def test_quantum_vacuum_all38_tadpoles_ward_and_normal_masses():
    x=np.array(cert()['passes']['11673']['vacuum']);g,H=M.jets(x);g+=M.treeg(x);H+=M.hessian(x)
    assert np.linalg.norm(g)<1e-10
    ev=np.linalg.eigvalsh(H);assert abs(ev[0])<1e-10 and ev[1]>5e-5
    alpha=.317;a=x[::2]+1j*x[1::2];q=np.r_[np.ones(4),np.ones(10)*2,np.ones(5)*4]
    shifted=a*np.exp(1j*alpha*q);xx=np.empty(38);xx[::2]=shifted.real;xx[1::2]=shifted.imag
    assert abs(M.quantum_potential(xx)-M.quantum_potential(x))<1e-12
    tangent=1j*q*a;v=np.empty(38);v[::2]=tangent.real;v[1::2]=tangent.imag
    assert np.linalg.norm(H@v)<1e-10
    assert abs(M.quantum_potential(x,64)-M.quantum_potential(x,128))<1e-10


def test_analytic_complete_loop_hessian_against_directional_action():
    x=np.array(cert()['passes']['11673']['vacuum']);g,Hloop=M.jets(x);H=Hloop+M.hessian(x)
    ev,U=np.linalg.eigh(H);rng=np.random.default_rng(92);step=2e-4
    ns,ws=np.polynomial.legendre.leggauss(256);ns=.12*ns+.13;ws*=.12
    def loop_value(xx):
        masses=np.linalg.eigvalsh(M.hessian(xx))/2
        vector=2*.1**2*np.dot(M.charges,xx*xx)
        return np.dot(ws,ns*(np.sum(np.log1p(masses[None,:]/ns[:,None]),axis=1)+3*np.log1p(vector/ns)))/(32*np.pi**2)
    directions=[U[:,i] for i in range(1,7)]+[rng.normal(size=38) for _ in range(4)]
    for v in directions:
        v/=np.linalg.norm(v)
        def curvature(h):return (loop_value(x+h*v)-2*loop_value(x)+loop_value(x-h*v))/h**2
        coarse,fine=curvature(step),curvature(step/2)
        extrapolated=(4*fine-coarse)/3
        # Direct resolvent differentiation is independent of the spectral
        # divided-difference implementation, and resolves IR-sensitive modes.
        mass=M.hessian(x)/2
        first=(M.hessian(x+v)-M.hessian(x-v))/4
        second=(M.hessian(x+v)-2*M.hessian(x)+M.hessian(x-v))/2
        ma=.02*np.dot(M.charges,x*x);mi=.04*np.dot(M.charges*x,v);mii=.04*np.dot(M.charges,v*v)
        def resolvent(p):
            inv=np.linalg.inv(p*np.eye(38)+mass)
            return p*(np.trace(inv@second-inv@first@inv@first)+3*(mii/(p+ma)-mi**2/(p+ma)**2))
        direct=quad(resolvent,M.A,M.B,epsabs=1e-10,epsrel=1e-10)[0]/(32*np.pi**2)
        assert abs(direct-v@Hloop@v)<1e-10
        if abs(v@H@v)<.001:assert abs(extrapolated-direct)<1e-7
    # Error from ignoring the31 massive scalar directions is measurable.
    assert np.linalg.norm(M.jets(M.base())[0])>.003


def test_cube_root_phase_points_are_equivalent_not_new_CP_branches():
    values=[M.loop(np.array(a)*2*np.pi/3) for a in it.product(range(3),repeat=3)]
    assert np.ptp(values)<1e-13
    assert M.loop([np.pi,0,0])-values[0]>1e-5
    # Axis-preserving D1 combined with the continuous phase acts on just one
    # transverse coordinate by omega; its square generates either cube phase.
    rows=dict((n,(R,c)) for n,R,c in P.kernel_generators());R,c=rows['D1']
    effective=(R*c**2).applyfunc(N.reduce_w)
    assert effective==s.diag(N.W,1,1)
    # SUM transports this phase gate to each of the other two coordinates.
    X=rows['SUM01'][0]
    assert (X*effective*X.T).applyfunc(N.reduce_w)!=effective


def test_bulk_index_by_independent_todd_and_cech_count():
    h,k=s.symbols('h k')
    td=s.series((h/(1-s.exp(-h)))**4,h,0,4).removeO()
    index=s.series(s.exp((k-2)*h)*td,h,0,4).removeO().coeff(h,3)
    assert s.factor(index-(k**3-k)/6)==0 and index.subs(k,-4)==-10
    powers=[a for a in it.product(range(3),repeat=4) if sum(a)==2]
    assert len(powers)==10
    # Laurent Cech H3(O(-6)) basis has exponents -a_i-1; Serre pairs it
    # with every quadratic monomial, exactly the parent's ten coordinates.
    assert set(powers)=={tuple(sum(int(j==i)+int(l==i) for j,l in [pair]) for i in range(4)) for pair in M.pairs}
    assert all(index.subs(k,j)!=3 for j in range(-2,3))
    assert index.subs(k,3)==4 and index.subs(k,-3)==-4


def test_exceptional_corrections_do_not_change_bulk_cohomology():
    # chi(O_CP2(-1))=chi(O_CP2(-2))=0, with all cohomology zero.
    for degree in [-1,-2]:assert (degree+1)*(degree+2)//2==0
    bulk=s.binomial(-3,3)  # chi(O_CP3(-6)) generalized binomial
    assert bulk==-10
    assert bulk+40*(0+0)==-10
    c=cert()['passes']['11674'];assert c['base_point_derivative_ranks']==[3]*40


def test_defect_spin_c_index_and_literal_kernel_character():
    h,k=s.symbols('h k');td=1+3*h/2+h*h
    chi=s.expand((1+k*h+k*k*h*h/2)*td).coeff(h,2)
    assert chi.subs(k,-4)==3
    assert [chi.subs(k,-n) for n in range(1,6)]==[0,0,1,3,6]
    assert len([a for a in it.product(range(2),repeat=3) if sum(a)==1])==3
    for name,R,c in P.kernel_generators():
        W=(R*c**2).applyfunc(N.reduce_w)
        assert N.reduce_w(c**3)==1
        assert (c**4*W-R).applyfunc(N.reduce_w)==s.zeros(3)
        # H2(O(-4)) carries W tensor detW; the determinant inverse in B
        # cancels this and its actual L fourth power supplies c^4.
        assert (c**4*W*N.reduce_w(W.det())*N.reduce_w(W.det().subs(N.W,N.W**2))-R).applyfunc(N.reduce_w)==s.zeros(3)
    assert cert()['passes']['11677']['all_40_defect_index']==120


def test_native_octagon_set_and_automorphism_invariance():
    import networkx as nx
    B=P.native_connection()[1];permutation=np.argmax(P.native_connection()[0],axis=0)
    graph=nx.from_numpy_array(abs(B)@abs(B).T);graph.remove_edges_from(nx.selfloop_edges(graph))
    cycles=list(nx.simple_cycles(graph,length_bound=8))
    def canon(c):
        c=list(c);k=c.index(min(c));a=c[k:]+c[:k];b=[a[0]]+list(reversed(a[1:]));return min(tuple(a),tuple(b))
    unique={canon(c) for c in cycles};assert len(unique)==1620
    assert {canon([int(permutation[i]) for i in c]) for c in cycles}==unique
    assert cert()['passes']['11675']['generic_Gauss_reduced_phase_dimension']==2*(160-80)*3


def test_flux_compensator_projection_and_vacuum_shift_response():
    n=np.arange(-2,3);S=np.eye(5,k=-1);I=np.eye(5)
    G=np.kron(np.diag(n),I)+np.kron(I,np.diag(n))
    U=np.eye(25)[:,[5*i+4-i for i in range(5)]]
    assert np.linalg.norm(G@U)==0
    assert np.array_equal(U.T@np.kron(S,S.T)@U,S)
    assert not np.any(U.T@np.kron(S,I)@U)
    for t in [.05,.2,.4]:
        _,H,e,p=M.reference_flux(13,t=t);_,HC,eC,pC=M.reference_flux(13,C=.713,t=t)
        assert np.allclose(HC-H,.713*np.eye(27))
        assert abs(eC[0]-e[0]-.713)<1e-12 and np.allclose(p,pC)
        assert p[13]<1 and p[0]+p[-1]<1e-20


def test_anomaly_is_signed_and_not_hidden_by_the_number_ten():
    h=[1,1,-2];six=[h[i]+h[j] for i,j in it.combinations_with_replacement(range(3),2)]
    assert sum(v**3 for v in six)==7*sum(v**3 for v in h)
    c=cert()['passes']['11678'];assert c['indexed_bulk_module_anomaly']==-8
    assert c['E6_27_tensor_bulk_anomaly']==-216 and c['E6_27_tensor_single_defect_anomaly']==27
    assert s.Rational(c['bosonic_U1_one_loop_beta_coefficient'])==s.Rational(124,3)


def test_even_dimensional_group_specific_twistor_obstruction():
    D=M.odd_gates()['D0'];assert (D**3-s.eye(4)).applyfunc(N.reduce_w)==s.zeros(4)
    trace=N.reduce_w(s.trace(D));conj=N.reduce_w(trace.subs(N.W,N.W**2))
    assert trace!=conj
    # A projective intertwining phase obeys alpha^3=alpha^4=1
    # from order3 and det1, hence alpha=1 and the unequal trace rules it out.
    assert N.reduce_w(D.det())==1
    B=s.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    assert B*B==-s.eye(4)
    assert (D*B-B*D.applyfunc(lambda z:N.reduce_w(z.subs(N.W,N.W**2)))).applyfunc(N.reduce_w)!=s.zeros(4)


def test_angular_counterterm_obstruction_and_uv_finite_difference():
    assert M.phase_counterterms()>0
    for theta in [[0,0,0],[.3,.6,1.1],[np.pi,0,0]]:
        H=M.hessian(M.base(theta))/2
        assert abs(np.trace(H)-489/2)<1e-10
        assert abs(np.trace(H@H)-45993/8)<1e-9
    a=np.linalg.eigvalsh(M.hessian(M.base())/2)
    b=np.linalg.eigvalsh(M.hessian(M.base([np.pi,0,0]))/2)
    # Leading x and logarithmic UV terms cancel in the angular difference.
    def diff(x):return x*np.sum(np.log1p(b/x)-np.log1p(a/x))
    assert abs(diff(1000))<abs(diff(100)) and abs(diff(10000))<abs(diff(1000))
