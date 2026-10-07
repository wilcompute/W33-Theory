"""Independent operator, curvature, orbit, gauge and inventory checks."""
import importlib.util
import itertools
import json
from pathlib import Path
import sys

import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11602_11606_geometry_flavor_completion as P


def stored():return json.loads(P.OUT.read_text())


def test_source_bindings():
    r=stored()
    assert r['status']=='PASS' and r['reservation']=='235295388'
    assert r['producer_sha256']==P.canonical_hash(Path(P.__file__))
    for path,digest in r['source_sha256'].items():assert P.canonical_hash(ROOT/path)==digest


def test_flat_dispersion_has_one_wilson_species_on_even_lattice():
    L=4;g,grade=P.gammas();n=L**3
    C=np.tile(np.array(g),(n,1,1,1));U=np.tile(np.eye(4),(n,3,1,1));w=np.ones((n,3))
    D0=P.local_dirac(C,U,w,(L,)*3,1.,r=0).toarray()
    DW=P.local_dirac(C,U,w,(L,)*3,1.,r=.25).toarray()
    assert np.max(abs(DW-DW.conj().T))<1e-13
    assert sum(abs(np.linalg.eigvalsh(D0))<1e-10)==32
    assert sum(abs(np.linalg.eigvalsh(DW))<1e-10)==4
    assert abs(np.trace(DW))<1e-13


def test_general_inverse_frame_symbol_and_second_basis():
    g,_=P.gammas();E=np.array([[2.,1.,0.],[0.,1.,1.],[0.,0.,3.]])
    cov=np.array([.3,-.7,1.2]);p=np.linalg.inv(E).T@cov
    Q=sum(a*z for a,z in zip(g,p))
    expected=cov@np.linalg.inv(E.T@E)@cov
    assert np.linalg.norm(Q@Q-expected*np.eye(4))<1e-12
    from scipy.linalg import expm
    S=expm(.23*g[0]@g[2]);Qg=S@Q@S.conj().T
    assert np.linalg.norm(Qg@Qg-expected*np.eye(4))<1e-12


def test_locality_and_local_rotations_from_rebuilt_data():
    C,U,w,shape,h,_,_=P.conformal_data(3)
    from scipy.linalg import expm
    from scipy.sparse import block_diag
    g,_=P.gammas();S=np.array([expm(.3*np.cos(j)*(g[1]@g[2])) for j in range(27)])
    Cp=np.array([[S[x]@Ci@S[x].conj().T for Ci in C[x]] for x in range(27)])
    Up=np.empty_like(U)
    for pt in itertools.product(range(3),repeat=3):
        x=np.ravel_multi_index(pt,shape)
        for i in range(3):
            q=list(pt);q[i]=(q[i]+1)%3;y=np.ravel_multi_index(q,shape)
            Up[x,i]=S[x]@U[x,i]@S[y].conj().T
    D=P.local_dirac(C,U,w,shape,h);Dp=P.local_dirac(Cp,Up,w,shape,h)
    St=block_diag(S,format='csr');delta=Dp-St@D@St.conj().T
    assert np.max(abs(delta.data))<1e-12
    for x,y in zip(*D.nonzero()):
        a=np.array(np.unravel_index(x//4,shape));b=np.array(np.unravel_index(y//4,shape))
        assert sum(a!=b)<=1


def test_geometric_spin_density_identity_for_arbitrary_gradient():
    g,_=P.gammas();grad=np.array([.2,-.3,.4]);d=3
    Omega=[.5*sum((grad[j]*g[i]@g[j] for j in range(3) if j!=i),np.zeros((4,4),complex)) for i in range(3)]
    lhs=sum((-grad[i]*g[i]+Omega[i]@g[i]-g[i]@Omega[i]+d*grad[i]*g[i] for i in range(3)),np.zeros((4,4),complex))
    assert np.linalg.norm(lhs)<1e-12
    rows=stored()['local_geometry']['refinement']
    assert rows[-1]['central_error']<.01 and rows[-1]['Wilson_error']<.05


def test_nonstatic_dirac_connection_cancels_volume_derivative():
    g,_=P.gammas();g0=np.kron(np.array([[0,-1j],[1j,0]]),np.eye(2))
    N=1.3;qp=np.array([.2,-.4,.7]);Np=.15
    actual=sum((g[i]@(.5*qp[i]*g[i]@g0/N) for i in range(3)),np.zeros((4,4),complex))
    half_density=actual-.5*g0/N*(Np/N+qp.sum())
    assert np.linalg.norm(half_density+g0*Np/(2*N*N))<1e-12
    # A time-dependent transverse inverse frame gives a nonzero mixed spin term.
    mixed=-1j*g0@g[1]*.27
    assert np.linalg.norm(mixed)>0 and np.linalg.norm(mixed-mixed.conj().T)<1e-12


def test_kasner_ricci_and_riemann_from_christoffel_not_exponent_formula():
    import w33_einstein_field_equations_from_spectral_action as G
    t=s.Symbol('t',positive=True);coords=[t,*s.symbols('x y z')]
    metric=s.diag(1,t**(-s.Rational(4,7)),t**s.Rational(6,7),t**s.Rational(12,7))
    _,Ric,R,Gamma,inv=G.einstein_tensor(metric,coords)
    assert Ric==s.zeros(4) and R==0
    K=0
    for a,b,i,j in itertools.product(range(4),repeat=4):
        component=s.diff(Gamma[a][j][b],coords[i])-s.diff(Gamma[a][i][b],coords[j])
        component+=sum(Gamma[a][i][k]*Gamma[k][j][b]-Gamma[a][j][k]*Gamma[k][i][b] for k in range(4))
        K+=metric[a,a]*inv[b,b]*inv[i,i]*inv[j,j]*component**2
    assert s.simplify(K-576/(343*t**4))==0


def test_ADM_legendre_transform_and_first_class_lapse():
    N,V,K,rho=s.symbols('N V K rho',positive=True);v=s.Matrix(s.symbols('v0:3'));p=s.Matrix(s.symbols('p0:3'))
    L=-K*V*(v[0]*v[1]+v[0]*v[2]+v[1]*v[2])/N-rho*N*V
    solution=s.solve([s.diff(L,v[i])-p[i] for i in range(3)],list(v))
    H=s.factor(sum(p[i]*v[i] for i in range(3))-L).subs(solution)
    C=((p.T*p)[0]-sum(p)**2/2)/(2*K*V)+rho*V
    assert s.simplify(H-N*C)==0 and s.diff(C,N)==0
    # The single homogeneous constraint has an identically vanishing self PB;
    # this deliberately does not test/claim the full local hypersurface algebra.


def test_signed_heat_coefficients_inventory_and_nonminimal_shift():
    rows=stored()['quantum_inventory']['inventories']
    for row in rows:
        ns,nw,nv=[row[k] for k in ['real_scalars','Weyl_components','vectors']]
        assert row['signed_a0']==ns-2*nw+2*nv
        expr=s.sympify(row['signed_a2_per_R'])
        assert expr.subs({z:0 for z in expr.free_symbols})==s.Rational(ns,6)+s.Rational(nw,6)-s.Rational(2*nv,3)
    assert [r['signed_a0'] for r in rows]==[152,86,842]
    assert rows[-1]['real_scalars']==162+3*2*126+2*2+2*3*2


def test_holomorphic_fixed_spaces_below_degree12():
    x,y=s.symbols('x y')
    expected={1:0,2:0,3:0,4:1,5:0,6:0,7:0,8:1,9:0,10:0,11:0,12:2}
    for d,count in expected.items():
        basis=[x**(d-j)*y**j for j in range(0,d+1,3)]
        residual=[s.Poly(s.expand(b.subs({x:(x+y)/s.sqrt(3),y:(2*x-y)/s.sqrt(3)},simultaneous=True)-b),x,y) for b in basis]
        A=s.Matrix([[f.coeff_monomial(x**(d-j)*y**j) for f in residual] for j in range(d+1)])
        assert len(A.nullspace())==count


def phase_completed_vacua():
    axes=np.array([[np.sqrt(2/3),-np.sqrt(1/6),-np.sqrt(1/6)],[0,1/np.sqrt(2),-1/np.sqrt(2)],[1/np.sqrt(3)]*3])
    points=[]
    H4=lambda u:u[0]**4+2*np.sqrt(2)*u[0]*u[1]**3
    target=np.sqrt(9/16+9*np.sqrt(42)/196)
    for perm in itertools.permutations([1,2,3]):
        for signs in itertools.product([-1,1],repeat=3):
            if np.prod(signs)!=1:continue
            m=np.array(perm)*signs/np.sqrt(14);r=axes@m
            u0=np.sqrt((1+r[2])/2);u=np.array([u0,(r[0]+1j*r[1])/(2*u0)])
            for k in range(4):
                v=u*np.exp(1j*(-np.angle(H4(u))/4+k*np.pi/2))
                assert abs(H4(v)-target)<1e-12
                points.append(v)
    return np.array(points)


def test_phase_completion_96_vectors_two_CP_orbits_no_goldstone():
    points=phase_completed_vacua();assert len(points)==96
    F,Pg,group=P.pencil_group();C=np.diag([1.,1/np.sqrt(2)])
    matrices=[C@np.array(A.evalf(),complex)@np.linalg.inv(C) for A in group]
    orbit=np.array([A@points[0] for A in matrices])
    assert np.min(np.linalg.norm(orbit-points[0].conj(),axis=1))>.05
    assert all(np.min(np.linalg.norm(points-v,axis=1))<1e-12 for v in orbit)
    assert len({tuple(np.round(np.r_[z.real,z.imag],9)) for z in orbit})==48
    assert all(np.min(np.linalg.norm(points-z.conj(),axis=1))<1e-12 for z in points)
    c2=9/16+9*np.sqrt(42)/196
    # Independent finite difference of lambda |H4-c|² along its old U1 orbit.
    H4=lambda u:u[0]**4+2*np.sqrt(2)*u[0]*u[1]**3
    step=1e-4;c=np.sqrt(c2);u=points[0]
    V=lambda alpha:abs(H4(u*np.exp(1j*alpha))-c)**2
    assert abs((V(step)+V(-step)-2*V(0))/step**2-32*c2)<2e-6


def test_flavon_potential_symmetry_and_full_positive_Hessian():
    coords,h,r,V,vac,Hess,_,_=P.family_potential()
    assert all(s.diff(V,z).subs(vac)==0 for z in coords)
    assert Hess.is_positive_definite
    w=-s.Rational(1,2)+s.I*s.sqrt(3)/2
    generators=[s.Matrix([[0,0,1],[1,0,0],[0,1,0]]),s.diag(1,w,w**2),s.Matrix([[1,0,0],[0,0,1],[0,1,0]])]
    # Polynomial identity tested on generic symbolic complex family values.
    for G in generators:
        hp=G*h;rp=G*r;sub={}
        for i in range(3):
            sub[coords[2*i]]=s.re(hp[i]);sub[coords[2*i+1]]=s.im(hp[i])
            sub[coords[6+2*i]]=s.re(rp[i]);sub[coords[7+2*i]]=s.im(rp[i])
        assert s.expand(V.subs(sub,simultaneous=True)-V)==0


def test_alignment_projector_is_gauge_invariant_and_selects_family_line():
    rng=np.random.default_rng(91);f=rng.normal(size=3)+1j*rng.normal(size=3)
    H=rng.normal(size=(3,10))+1j*rng.normal(size=(3,10))
    U,_=np.linalg.qr(rng.normal(size=(10,10))+1j*rng.normal(size=(10,10)))
    penalty=lambda X:np.vdot(f,f).real*np.vdot(X,X).real-np.vdot(f.conj()@X,f.conj()@X).real
    assert penalty(H)>0 and abs(penalty(H@U)-penalty(H))<1e-10
    aligned=f[:,None]*(rng.normal(size=10)+1j*rng.normal(size=10))
    assert abs(penalty(aligned))<1e-10


def test_seesaw_eigenvalues_and_physical_mixing_obstruction():
    r=stored()['Majorana_alignment'];M=lambda key:s.Matrix([[s.sympify(z) for z in row] for row in r[key]])
    MD,MR,Me,mn=[M(k) for k in ['MD','MR','Me','light_Majorana']]
    assert mn==-MD*MR.inv()*MD.T
    anti=s.Matrix([0,1,-1]);assert Me*anti==-s.Rational(19,10)*anti
    assert mn*anti==-s.Rational(1,3)*anti
    lam=s.Symbol('lambda')
    assert s.factor((-mn).charpoly(lam).as_expr())==(3*lam-1)*(9*lam**2-12*lam+2)/27
    assert s.factor(Me.charpoly(lam).as_expr())==(10*lam+19)*(50*lam**2-15*lam-29)/500
    # Independent real diagonalizations: one exact isolated mass eigenstate.
    _,E=np.linalg.eigh(np.array(Me, float));_,N=np.linalg.eigh(np.array(-mn, float))
    mixing=abs(E.T@N);assert sum(mixing.ravel()<1e-12)==4
    assert abs(np.max(mixing)-1)<1e-12


def test_matter_parity_and_spectator_cost_are_not_silent():
    c=json.loads((ROOT/'data/PART_W33_PASS11595_NEUTRINO_MAJORANA_CHANNEL.json').read_text())
    assert c['required_scalar_vev_charges']['qBL']==-6
    assert (-1)**(-6)==1 and (-1)**(-3)==-1
    weights=[sum([1,1,-2][i] for i in w) for w in itertools.combinations_with_replacement(range(3),6)]
    assert len(weights)==28 and s.Rational(sum(z*z for z in weights),12)==63
    assert -s.Rational(15,2)-63/s.Integer(3)==-s.Rational(57,2)


def test_spectator_canonical_mass_preserves_family_and_has_full_rank():
    r=stored()['additional_spectator_symmetry'];lam=s.symbols('lambda',nonzero=True,real=True)
    B=s.Matrix([[s.sympify(z.replace('lambda','lam'),locals={'lam':lam}) for z in row] for row in r['canonical_sym3_mass']])
    words=list(itertools.combinations_with_replacement(range(3),3));pos={w:i for i,w in enumerate(words)}
    for perm in [[1,2,0],[0,2,1]]:
        G=s.zeros(10)
        for i,w in enumerate(words):G[pos[tuple(sorted(perm[k] for k in w))],i]=1
        assert G.T*B*G==B
    omega=-s.Rational(1,2)+s.I*s.sqrt(3)/2;Z=s.diag(*[omega**(-sum(w)) for w in words])
    assert s.simplify(Z.T*B*Z-B)==s.zeros(10)
    assert B.det()==-lam**7/(15*30**6)
    assert B.eigenvals()=={s.Integer(1):3,lam/15:1,lam/30:3,-lam/30:3}


def test_unequal_alignment_global_targets_and_full_normal_rank():
    t=s.Symbol('t');assert s.factor(t**3-14*t*t+49*t-36)==(t-1)*(t-4)*(t-9)
    # Independent Jacobian in magnitude/phase coordinates at h=(1,2,3),r=ones.
    a,b,c,d,e,f,ha,hb,hc,ra,rb,rc=s.symbols('a b c d e f ha hb hc ra rb rc',real=True)
    rad=s.Matrix([a*a+b*b+c*c-14,a*a*b*b+a*a*c*c+b*b*c*c-49,a*a*b*b*c*c-36,d*d-1,e*e-1,f*f-1])
    Jr=rad.jacobian([a,b,c,d,e,f]).subs({a:1,b:2,c:3,d:1,e:1,f:1})
    assert Jr.det()!=0
    # Linearized imaginary constraints: sum h^3, product h, cross h-dagger r;
    # r_i^3=1 already fixes each r phase.
    phase=s.Matrix([ha+8*hb+27*hc,6*(ha+hb+hc),(-ha+ra)+2*(-hb+rb)+3*(-hc+rc),3*ra,3*rb,3*rc])
    assert phase.jacobian([ha,hb,hc,ra,rb,rc]).det()!=0
    row=stored()['additional_unequal_alignment_escape']
    assert len(row['Hessian_positive_leading_minors'])==12
    assert all(int(z)>0 for z in row['Hessian_positive_leading_minors'])


def test_unequal_alignment_exact_CP_and_nonzero_three_angle_mixing():
    row=stored()['additional_unequal_alignment_escape']
    mat=lambda key:s.Matrix([[s.sympify(z) for z in rr] for rr in row[key]])
    D,R,E,m=[mat(k) for k in ['MD','MR','Me','light_Majorana']]
    assert m==-D*R.inv()*D.T
    He=E.H*E;Hn=m.H*m;K=He*Hn-Hn*He
    assert s.im(s.trace(K**3))==-s.Rational(94163140688,5625)
    lam=s.Symbol('lam');assert s.discriminant(He.charpoly(lam).as_expr(),lam)!=0
    assert s.discriminant(Hn.charpoly(lam).as_expr(),lam)!=0
    _,U=np.linalg.eigh(np.array(He,complex));_,V=np.linalg.eigh(np.array(Hn,complex));mix=abs(U.conj().T@V)**2
    assert np.min(mix)>.03
    assert np.max(abs(mix-np.array(row['mixing_modulus_squared'])))<1e-12
    assert abs(row['sin_squared_angles']['theta13']-.03347437761864)<1e-12
    # CP originates in a possible Hesse vacuum ratio; its selectors are supplied.
    u0=s.sqrt(s.Rational(2,3));u1=-s.I/s.sqrt(3)
    assert s.simplify(s.conjugate(u1)/(s.sqrt(2)*u0))==s.I/2
    assert s.expand(u0**4+2*s.sqrt(2)*u0*u1**3)==4*(1+s.I)/9


def test_parallel_filter_phase_completion_and_antilinear_basis_transport():
    source=json.loads((ROOT/'data/w33_pass10961_albert_clifford9_gammas.json').read_text())
    gam=[]
    for raw in source['gamma9']:
        A=np.array(raw,float);gam.append(np.block([[np.zeros((16,16)),A],[A,np.zeros((16,16))]]))
    gam.append(np.diag([1.]*16+[-1.]*16));Chi=1j*np.linalg.multi_dot(gam);R=1j*gam[-1]
    assert np.linalg.norm(Chi.conj()+Chi)==0
    assert np.linalg.norm(R@Chi@R.conj().T+Chi)==0
    assert np.linalg.norm(R@Chi.conj()@R.conj().T-Chi)==0
    # Check a complex basis, transporting the anti-linear parts correctly.
    rng=np.random.default_rng(11607);S,_=np.linalg.qr(rng.normal(size=(32,32))+1j*rng.normal(size=(32,32)))
    Ch=S@Chi@S.conj().T;Kpart=S@S.T;RKpart=S@R@S.T
    assert np.linalg.norm(Kpart@Ch.conj()@Kpart.conj().T+Ch)<1e-12
    assert np.linalg.norm(RKpart@Ch.conj()@RKpart.conj().T-Ch)<1e-12
    axes=np.array([[np.sqrt(2/3),-np.sqrt(1/6),-np.sqrt(1/6)],[0,1/np.sqrt(2),-1/np.sqrt(2)],[1/np.sqrt(3)]*3])
    c=15/343
    for u in phase_completed_vacua():
        r=np.array([2*np.real(u[0].conj()*u[1]),2*np.imag(u[0].conj()*u[1]),abs(u[0])**2-abs(u[1])**2]);x,y,z=axes.T@r
        W=(x*x-y*y)*(y*y-z*z)*(z*z-x*x)
        assert abs(abs(W)-c)<1e-14
        A=c*np.eye(32)+W*Chi;ev=np.linalg.eigvalsh(A@A)
        assert sum(abs(ev)<1e-12)==16 and np.max(abs(ev[16:]-4*c*c))<1e-13
