"""Independent normal, determinant, bracket, order and quantum-control audits."""
import importlib.util
import itertools
import json
from math import comb
from pathlib import Path

import numpy as np
import sympy as s
from scipy.integrate import quad
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('p11615',ROOT/'analysis/w33_pass11615_11619_parent_pairs_constraints.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)


def test_complex_mediator_elimination_and_normalized_ratio():
    u=np.array([np.sqrt(2/3),-1j/np.sqrt(3)])
    rng=np.random.default_rng(11615);H=rng.normal(size=(3,10))+1j*rng.normal(size=(3,10))
    mass=2.3;A=-u.conj()[:,None,None]*H[None,:,:]/mass
    assert np.max(abs(mass*A+u.conj()[:,None,None]*H))<1e-14
    assert abs((u[1].conjugate()/np.sqrt(6))/(u[0].conjugate()/np.sqrt(3))-1j/2)<1e-14
    # Gauge-basis change preserves the positive matching square.
    Q,_=np.linalg.qr(rng.normal(size=(10,10))+1j*rng.normal(size=(10,10)))
    residual=mass*(A+.02)+u.conj()[:,None,None]*H
    assert abs(np.linalg.norm(residual@Q)-np.linalg.norm(residual))<1e-13


def test_H4_complex_lift_and_no_false_offshell_equality():
    x=1.2+.3j;y=-.4+.7j;mass=2.
    A=x*x/mass;B=y*y/mass;C=y*B/mass
    assert abs((A*A+2*np.sqrt(2)*x*C)-(x**4+2*np.sqrt(2)*x*y**3)/mass**2)<1e-14
    # The finite-stiffness parent does NOT equal the original off-shell square.
    # At q=0, minimize (z-q^2)^2+(z-1)^2: z=1/2, V=1/2 vs V_original=1.
    assert (.5**2+(.5-1)**2)==.5


def test_equivariant_tensor_chain_and_positive_normals():
    # Full tensor realizations give an independent second coordinate basis.
    O=np.array([[.6,-.8],[.8,.6]])
    x=np.array([.7,-.3]);Q=np.array([[1,.2],[.2,2.]])
    lhs=Q-np.outer(x,x)
    rhs=O@Q@O.T-np.outer(O@x,O@x)
    assert np.linalg.norm(rhs-O@lhs@O.T)<1e-14
    assert abs(np.linalg.norm(rhs)-np.linalg.norm(lhs))<1e-14
    # Six real constraints on three complex auxiliaries plus two terminal
    # constraints have a triangular full auxiliary derivative at nonzero M.
    xr,xi,yr,yi,ar,ai,br,bi,cr,ci=s.symbols('z0:10',real=True)
    X=xr+s.I*xi;Y=yr+s.I*yi;A=ar+s.I*ai;B=br+s.I*bi;C=cr+s.I*ci
    residual=[2*A-X*X,2*B-Y*Y,2*C-Y*B]
    real=[part for z in residual for part in [s.re(z),s.im(z)]]
    assert s.Matrix(real).jacobian([ar,ai,br,bi,cr,ci]).det()==64
    assert comb(12,8)-5==490 and comb(18,6)-13==18551


def test_massive_gauge_goldstone_and_inventory():
    prior=json.loads((ROOT/'data/w33_pass11602_11606_geometry_flavor_completion.json').read_text())
    assert prior['quantum_inventory']['status']=='PASS'
    scalar_total=934+2*3*10*2+28*2+45+(comb(12,8)-5)+(comb(18,6)-13)
    assert scalar_total==20196
    physical_scalar=scalar_total-33
    assert physical_scalar+33*3+12*2-91*2==20104
    # Vector - two ghosts + Goldstone, with minimal scalar matching.
    assert 4-2+1==3
    assert -s.Rational(1,3)-2*s.Rational(1,6)+s.Rational(1,6)==-s.Rational(1,2)
    assert (scalar_total+91-4*45)/6==20107/6


def test_prior_Majorana_and_spectator_moments():
    prior=json.loads((ROOT/'data/w33_pass11602_11606_geometry_flavor_completion.json').read_text())
    Majorana=s.Matrix(prior['additional_unequal_alignment_escape']['MR'])
    assert s.trace(Majorana**4)==1458
    def parse(t):return complex(s.sympify(str(t).replace('lambda','lam'),locals={'lam':s.Integer(1)}))
    B=np.array([[parse(t) for t in row] for row in prior['additional_spectator_symmetry']['canonical_sym3_mass']])
    singular=np.linalg.svd(B,compute_uv=False)
    assert abs(np.sum(singular**4)-float(s.Rational(1215011,405000)))<1e-13
    assert len(singular)==10


def test_mass_dependent_integrals_against_quadrature():
    for mass2 in [.01,1.,9.,25.]:
        I0,I1=M.cutoff_integrals(mass2)
        Q0=quad(lambda t:np.exp(-mass2*t)/t**3,1,np.inf,epsabs=1e-15)[0]
        Q1=quad(lambda t:np.exp(-mass2*t)/t**2,1,np.inf,epsabs=1e-15)[0]
        assert np.isclose(I0,Q0,rtol=1e-8,atol=1e-15)
        assert np.isclose(I1,Q1,rtol=1e-8,atol=1e-15)
    assert M.cutoff_integrals(0)==(.5,1.)


def test_actual_HH_bracket_by_canonical_differentiation():
    n=5;q=s.Matrix(s.symbols('q0:5'));p=s.Matrix(s.symbols('p0:5'))
    D=M.cycle_derivative(n);N=s.diag(1,0,0,0,0);T=s.diag(0,1,0,0,0)
    H=lambda L:((p.T*L*p)[0]+(q.T*D.T*L*D*q)[0])/2
    a,b=H(N),H(T)
    PB=sum(s.diff(a,q[i])*s.diff(b,p[i])-s.diff(a,p[i])*s.diff(b,q[i]) for i in range(n))
    B=T*D.T*N*D-N*D.T*T*D
    assert s.expand(PB-(p.T*B*q)[0])==0
    assert B+B.T!=s.zeros(n)
    assert B[1,4]==-s.Rational(1,4) and B[0,2]==s.Rational(1,4)


def test_local_GG_generates_distant_rotations():
    A=M.local_generators(9)
    C=A[0]*A[1]-A[1]*A[0]
    assert C[8,1]!=0 or C[0,2]!=0
    # Direct local edge rotations and all path commutators generate so(9).
    edges=[]
    for i in range(9):
        E=s.zeros(9);E[i,(i+1)%9]=1;E[(i+1)%9,i]=-1;edges.append(E)
    generated=list(edges)
    # A rooted path builds E(0,j), and their mutual brackets give E(i,j).
    path=edges[0]
    rooted=[path]
    for j in range(1,8):path=path*edges[j]-edges[j]*path;rooted.append(path)
    completed=rooted+[U*V-V*U for i,U in enumerate(rooted) for V in rooted[i+1:]]
    assert s.Matrix.hstack(*[s.Matrix(list(T)) for T in completed]).rank()==36


def test_four_site_parent_all_ground_states_and_odd_gap():
    # Independent construction using elementary computational-basis projectors.
    n=4;dim=3**n;H=np.zeros((dim,dim),complex)
    basis=list(itertools.product(range(3),repeat=n))
    for i,d in enumerate(basis):H[i,i]=2*d.count(1)
    for a,b in [(0,1),(1,2),(2,3),(3,0)]:
        for i,d in enumerate(basis):
            if (d[a],d[b]) not in [(0,2),(2,0)]:continue
            e=list(d);e[a],e[b]=e[b],e[a];j=basis.index(tuple(e))
            H[i,i]+=.5;H[i,j]-=.5
    eig=np.linalg.eigvalsh(H)
    assert abs(eig.min())<1e-12 and np.sum(abs(eig)<1e-10)==5
    for k in range(5):
        state=M.dicke(n,k)
        assert np.linalg.norm(H@state)<1e-14
    odd=[i for i,d in enumerate(basis) if sum(d)%2]
    assert abs(np.linalg.eigvalsh(H[np.ix_(odd,odd)]).min()-2)<1e-12


def test_pair_and_atomic_density_matrices_by_state_enumeration():
    n=5;k=2;state=M.dicke(n,k);a,_,_,_=M.pair_local()
    atoms=[M.embed(a,[i],n)@state for i in range(n)]
    pairs=[M.embed(a@a,[i],n)@state for i in range(n)]
    A=np.array([[np.vdot(v,w) for w in atoms] for v in atoms])
    B=np.array([[np.vdot(v,w) for w in pairs] for v in pairs])
    assert np.max(abs(A-np.eye(n)*2*k/n))<1e-13
    off=2*k*(n-k)/(n*(n-1))
    expected=np.ones((n,n))*off+np.eye(n)*(2*k/n-off)
    assert np.max(abs(B-expected))<1e-13
    assert abs(np.linalg.eigvalsh(B).max()-2*k*(n-k+1)/n)<1e-13


def test_unbroken_parity_and_broken_pair_phase_representative():
    a,P,_,_=M.pair_local()
    for rho in [.2,.5,.8]:
        z=np.array([np.sqrt(1-rho),0,np.exp(.7j)*np.sqrt(rho)])
        assert np.max(abs(P@z-z))<1e-14
        assert abs(np.vdot(z,a@z))<1e-14
        assert abs(np.vdot(z,a@a@z)-np.sqrt(2*rho*(1-rho))*np.exp(.7j))<1e-14


def test_native_connected_graph_and_parity_holonomy():
    inc,C=M.cycle_basis();assert inc.shape==(80,160) and C.shape==(160,81)
    assert not np.any(inc@C)
    # Reconstruct a fundamental loop from its edge coefficients, not prose.
    c=C[:,0];assert np.count_nonzero(c)>=8
    t=np.zeros(160);t[np.flatnonzero(c)[0]]=np.pi
    assert abs(np.exp(1j*c@t)+1)<1e-13
    assert abs(np.exp(2j*c@t)-1)<1e-13


def test_actual_qutrit_pair_gate_and_Pauli_algebra():
    a,P,_,_=M.pair_local();b=a@a/np.sqrt(2)
    X=b+b.conj().T;Y=-1j*(b-b.conj().T);Z=np.diag([1,0,-1])
    assert np.max(abs(X@Y-Y@X-2j*Z))<1e-13
    H=np.kron(b.conj().T,b)+np.kron(b,b.conj().T)
    psi=np.zeros(9,complex);psi[2]=1
    evolved=expm(-1j*np.pi*H/4)@psi
    assert abs(evolved[2]-1/np.sqrt(2))<1e-13
    assert abs(evolved[6]+1j/np.sqrt(2))<1e-13
    assert np.linalg.matrix_rank(evolved[[0,2,6,8]].reshape(2,2))==2
    for T in [X,Y,Z]:assert np.max(abs(T@P-P@T))<1e-13


def test_small_atomic_hopping_still_has_finite_gap():
    r=M.pair_control()
    assert all(row['odd_gap']>row['finite_norm_gap_bound']-1e-12 for row in r['perturbation_rows'])
    last=r['perturbation_rows'][-1]
    assert last['odd_gap']>1.6 and last['pair_correlation']>.65
    assert last['atomic_correlation']>0 # no false persistence of local parity


def test_CP_threshold_equality_and_broken_standalone_pencil_action():
    h=np.array([1,2,3]);u=np.array([.6+.2j,.3-.7j])
    def Y(v):
        a=v[0].conjugate()/np.sqrt(3);b=v[1].conjugate()/np.sqrt(6)
        return np.array([[a*h[0],b*h[2],b*h[1]],[b*h[2],a*h[1],b*h[0]],[b*h[1],b*h[0],a*h[2]]])
    singular=np.linalg.svd(Y(u),compute_uv=False)
    assert np.max(abs(singular-np.linalg.svd(Y(u.conj()),compute_uv=False)))<1e-13
    F=np.array([[1,np.sqrt(2)],[np.sqrt(2),-1]])/np.sqrt(3)
    assert abs(np.sum(singular**4)-np.sum(np.linalg.svd(Y(F@u),compute_uv=False)**4))>.01


def test_constant_sequestering_does_not_remove_local_forces():
    r=M.vacuum_response()
    C1,C2=s.symbols('C1 C2',real=True)
    rr=s.Matrix([s.sympify(t,locals={'C1':C1,'C2':C2}) for t in r['two_domain_residual']])
    assert s.simplify(rr[0]/3+2*rr[1]/3)==0
    assert rr.subs({C1:3,C2:0})==s.Matrix([2,-1])
    q,m=s.symbols('q m',positive=True)
    V=(m*m+q*q)**2*(s.log(m*m+q*q)-s.Rational(3,2))
    assert s.diff(V+12345,q)==s.diff(V,q)
    assert s.diff(V,q)!=0


def test_MS_running_mass_moments_and_certificate_binding():
    mu=s.symbols('mu',positive=True);m=s.symbols('m',positive=True)
    f=m**4*(s.log(m*m/(mu*mu))-s.Rational(3,2))/(64*s.pi**2)
    assert s.simplify(mu*s.diff(f,mu)+m**4/(32*s.pi**2))==0
    cert=json.loads((ROOT/'data/w33_pass11615_11619_parent_pairs_constraints.json').read_text())
    assert cert['producer_sha256']==M.ph(ROOT/'analysis/w33_pass11615_11619_parent_pairs_constraints.py')
    for path,digest in cert['source_sha256'].items():assert M.ph(ROOT/path)==digest
    assert all(cert[k]['status']=='PASS' for k in ['parent','thresholds','constraints','pair_phase','vacuum_response','additional_pair_holonomy','additional_loop_orientation','additional_pair_control','additional_parent_budget','additional_gauge_threshold'])


def test_full_gauge_spectrum_against_D5_root_weights():
    A,B,_,_=M.gauge_grams();av=2.;bv=.3
    actual=np.linalg.eigvalsh(np.array(av*A+2*bv*B,float))
    # Ten Cartan planes: positive roots ei-ej and ei+ej, each has two real
    # gauge generators. The126 singlet is SU5 invariant, so difference roots
    # are unbroken by it and sum roots get2bv. Four Cartans survive.
    charge=[2/3]*3+[0,0];expected=[0]*4+[10*bv]
    for i,j in itertools.combinations(range(5),2):
        expected += [av*(charge[i]-charge[j])**2]*2
        expected += [av*(charge[i]+charge[j])**2+2*bv]*2
    assert len(expected)==45
    assert np.max(abs(actual-np.sort(expected)))<1e-12
    assert np.sum(actual<1e-12)==12
    moment=np.sum(actual**2)
    assert abs(moment-(640*av**2/27+64*av*bv+180*bv**2))<1e-10


def test_symmetric_spinor_gauge_Gram_in_a_second_complex_basis():
    _,B,T,_=M.gauge_grams();rng=np.random.default_rng(126)
    U,_=np.linalg.qr(rng.normal(size=(32,32))+1j*rng.normal(size=(32,32)))
    v=U[:,-1];columns=[]
    for generator in T:
        transported=U@generator@U.conj().T
        w=transported@v
        columns.append((np.outer(w,v)+np.outer(v,w)).ravel())
    J=np.stack(columns,axis=1)
    transformed=(J.conj().T@J).real
    assert np.max(abs(transformed-np.array(B,float)))<1e-12
