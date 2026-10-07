"""Five scoped continuations of11620-11624; no physical TOE prediction.

Owners11620/11621: pair representation and supplied45/126 tree orbit;
11600/11622: normalized Hesse action;4082: conditional composite hopping;
11306/11323: clock completion and native lapse obstruction;11307/11324:
membranes. Classical Hubbard/Kuchar/Brown-Teitelboim mechanisms are credited.
"""
from functools import lru_cache
from pathlib import Path
import itertools
import json
import sys
import numpy as np
import sympy as s
from scipy.optimize import minimize
from numpy.polynomial.legendre import leggauss
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass11620_11624_covariant_pair_vacuum import spin_pair_data,scalar_jacobians
from w33_pass11615_11619_parent_pairs_constraints import ph
OUT=ROOT/'data/w33_pass11625_11629_composites_joint_vacua.json'
RESERVATION='90099d605'


def fermion_operator(n,mode):
    A=s.zeros(2**n)
    for state in range(2**n):
        if state>>mode&1:A[state^(1<<mode),state]=(-1)**((state&((1<<mode)-1)).bit_count())
    return A


def fermion_matching():
    T,_,B,R,_,_,_,_,_,_=spin_pair_data()
    wedge=list(itertools.combinations(range(32),2))
    E=np.zeros((496,136),complex)
    for row,(i,j) in enumerate(wedge):
        if i<16<=j:E[row]=B[:,i,j-16]
    assert np.max(abs(E.conj().T@E-np.eye(136)))<1e-14
    eps=np.array([[0,1],[-1,0]])
    F=np.einsum('uv,bij->buivj',eps,B).reshape(136,32,32)
    for a in [np.array([[0,1],[-1,0]]),1j*np.array([[0,1],[1,0]]),1j*np.diag([1,-1])]:
        K=np.kron(a,np.eye(16));assert np.max(abs(K@F+F@K.T))<1e-14
    for t,r in zip(T,R):
        K=np.kron(np.eye(2),t)
        d=K@F+F@K.T
        assert np.max(abs(np.einsum('bc,cij->bij',r.T,F)-d))<1e-13
    # Four actual fermion modes: left up/down, right up/down.
    c=[fermion_operator(4,j) for j in range(4)];n=[a.T*a for a in c]
    U,t=s.symbols('U t',positive=True)
    H0=U/2*sum((n[2*j]+n[2*j+1]-2*n[2*j]*n[2*j+1] for j in range(2)),s.zeros(16))
    V=-t*sum((c[j].T*c[j+2]+c[j+2].T*c[j] for j in range(2)),s.zeros(16))
    low=[0,3,12,15];high=[i for i in range(16) if i not in low]
    W=-V.extract(low,high)*H0.extract(high,high).inv()*V.extract(high,low)
    K=2*t*t/U
    assert W==s.Matrix([[0,0,0,0],[0,-K,-K,0],[0,-K,-K,0],[0,0,0,0]])
    repair=s.diag(0,2*K,2*K,0)
    desired=s.Matrix([[0,0,0,0],[0,K,-K,0],[0,-K,K,0],[0,0,0,0]])
    assert W+repair==desired
    # Center-only local Gauss law, explicitly weaker than full Spin10.
    states=list(itertools.product(range(2),range(2),range(4)))
    physical=[a for a in states if (2*a[0]+a[2])%4==0 and (2*a[1]-a[2])%4==0]
    assert physical==[(0,0,0),(1,1,2)]
    return dict(status='PASS',spin_singlet_embedding_shape=[496,136],singlet_rank=136,
      decomposition='Lambda2(C2 tensor C16)=Lambda2(C2) tensor Sym2(C16) + Sym2(C2) tensor Lambda2(C16), dimensions136+360=496. Thus10+126 spin-singlet fermion pairs are Pauli-allowed.',
      full_Spin10_intertwiner=True,pair_even_matter_parity=True,
      second_order_matrix=[[str(x) for x in row] for row in W.tolist()],
      conclusion='Actual attractive fermion hopping does not equal the old swap parent, even in one polarized pair direction. Pair hopping K=2t^2/U is accompanied by the wrong mixed-occupation diagonal energy.',
      repair='Add2K(nL+nR-2nL nR), i.e. a chemical term and attractive neighbor density coupling, to obtain2K(I-Swap)/2 in the polarized pair qubit. This is an added interaction; it does not generate the entire127-color parent.',
      center_Gauss_states=physical,center_dressed_map='B_Ldag B_Rdag U_link^2 maps(0,0,0) to(1,1,2), preserving both center Gauss charges. An undressed single charged pair has zero gauge-projected expectation.',
      boundary='Spin labels here are a supplied two-component singlet factor, not a derived relativistic kinetic theory. Full126 elementary/composite effective-action matching and continuous Spin10 Gauss dynamics remain open.')


@lru_cache(None)
def scalar_data():
    _,_,_,_,A,S,V,T,D=scalar_jacobians()
    return V,T,D


def scalar_tree(A,S):
    V,T,D=scalar_data();a=np.einsum('aij,ij->a',V,A)/2
    tA=np.einsum('a,aij->ij',a,T)
    nA=np.dot(a,a);nS=np.vdot(S,S).real;X=S@S.conj().T
    F=A@A@A+A;Z=tA@S+S@tA.T+3j*S
    return float((nA-3)**2+np.vdot(F,F).real/2+(nS-1)**2+nS*nS-np.trace(X@X).real+np.vdot(Z,Z).real)


def scalar_hessian(A,S):
    V,T,D=scalar_data();a=np.einsum('aij,ij->a',V,A)/2
    tA=np.einsum('a,aij->ij',a,T);nS=np.vdot(S,S).real;X=S@S.conj().T
    H=np.zeros((297,297));H[:45,:45]=8*np.outer(a,a)+4*(np.dot(a,a)-3)*np.eye(45)
    F=A@A@A+A
    dF=V@A@A+A@V@A+A@A@V+V
    H[:45,:45]+=np.einsum('aij,bij->ab',dF,dF)
    # Second derivative of A^3: all six placements of two variations and A.
    va=V@A;av=A@V
    for i in range(45):
        d2=V[i]@va+V@va[i]+V[i]@av+V@av[i]+av[i]@V+av@V[i]
        H[i,:45]+=np.einsum('ij,bij->b',F,d2)
    gS=2*np.einsum('bij,ij->b',D.conj(),S).real
    dX=D@S.conj().T+S@D.conj().transpose(0,2,1)
    H[45:,45:]=4*np.outer(gS,gS)+(4*nS-2)*np.eye(252)
    H[45:,45:]-=2*np.einsum('aij,bji->ab',dX,dX,optimize=True).real
    H[45:,45:]-=4*np.einsum('aij,ik,bkj->ab',D.conj(),X,D,optimize=True).real
    Z=tA@S+S@tA.T+3j*S
    JA=T@S+S@T.transpose(0,2,1);JS=tA@D+D@tA.T+3j*D
    J=np.concatenate([JA,JS]);H+=2*np.einsum('aij,bij->ab',J.conj(),J,optimize=True).real
    for i in range(45):
        cross=2*np.einsum('ij,bij->b',Z.conj(),T[i]@D+D@T[i].T).real
        H[i,45:]+=cross;H[45:,i]+=cross
    assert np.max(abs(H-H.T))<1e-10
    return H


def background(q):
    V,T,D=scalar_data();x,y,z=q
    A=sum((x if j<3 else y)*V[list(itertools.combinations(range(10),2)).index((2*j,2*j+1))] for j in range(5))
    S=np.zeros((16,16),complex);S[-1,-1]=z
    return A,S


def gauge_masses(A,S):
    V,T,D=scalar_data()
    ga=V@A-A@V;gs=T@S+S@T.transpose(0,2,1)
    H=np.einsum('aij,bij->ab',ga,ga)/2+2*np.einsum('aij,bij->ab',gs.conj(),gs).real
    return np.linalg.eigvalsh(H)


@lru_cache(None)
def shell_nodes(k,cutoff,order):
    z,w=leggauss(order);lo=k*k;hi=cutoff*cutoff
    return (lo+hi)/2+(hi-lo)*z/2,w*(hi-lo)/2


def shell_potential(q,c=.001,k=.1,cutoff=.5,order=48):
    A,S=background(q);sm=c*np.linalg.eigvalsh(scalar_hessian(A,S));vm=c*gauge_masses(A,S)
    x,w=shell_nodes(k,cutoff,order)
    if np.min(sm)<=-k*k:return np.inf
    val=np.sum(w*x*(np.log1p(sm[:,None]/x).sum(axis=0)+3*np.log1p(vm[:,None]/x).sum(axis=0)))/(64*np.pi**2)
    return c*scalar_tree(A,S)+float(val)


def grad(f,q,h=2e-5):
    return np.array([(f(q+h*e)-f(q-h*e))/(2*h) for e in np.eye(len(q))])


def finite_hessian(f,q,h=1e-4):
    H=np.empty((len(q),len(q)));eye=np.eye(len(q));v=f(q)
    for i,e in enumerate(eye):
        H[i,i]=(f(q+h*e)+f(q-h*e)-2*v)/h**2
        for j in range(i):
            a=eye[j];H[i,j]=H[j,i]=(f(q+h*(e+a))-f(q+h*(e-a))-f(q+h*(-e+a))+f(q-h*(e+a)))/(4*h*h)
    return H


def quantum_vacuum():
    H0=scalar_hessian(*background([1,0,1]));old=scalar_jacobians()[0]
    assert np.max(abs(H0-old))<2e-12
    f=lambda q:shell_potential(np.asarray(q),order=32)
    starts=[[1,0,1],[.98,.01,1.02],[1.02,-.02,.98]];sol=[]
    for q in starts:
        r=minimize(f,q,jac=lambda v:grad(f,v),method='BFGS',options={'gtol':2e-9,'maxiter':100})
        g=grad(f,r.x);assert np.linalg.norm(g)<1e-7
        sol.append((r.x,float(r.fun)))
    q,value=min(sol,key=lambda a:a[1]);H=finite_hessian(f,q)
    assert min(np.linalg.eigvalsh(H))>0
    assert max(np.linalg.norm(v-q) for v,e in sol)<2e-4
    refined=shell_potential(q,order=64);assert abs(refined-value)<1e-10
    return dict(status='PASS',scheme='Declared Landau-background one-loop finite Euclidean momentum shell, k=.1, UV=.5, Vtree=.001 V11621, gauge g^2=.001. No fermions. All297 scalar and45 vector eigenvalues enter; massless gauge constants drop, scalar Goldstones are not deleted.',
      definition='V_k=Vtree+(1/(64pi^2)) integral_{k^2}^{UV^2} x[Tr log(1+Hs/x)+3Tr log(1+Hv/x)] dx.',
      tree_point=[1,0,1],stationary_SM_slice=q.tolist(),three_starts=[v.tolist() for v,e in sol],value=value,
      stationarity_gradient=grad(f,q).tolist(),slice_Hessian=H.tolist(),slice_eigenvalues=np.linalg.eigvalsh(H).tolist(),quadrature32_64_difference=float(refined-value),
      full_scalar_tree_gap_at_reference=.002,formal_persistence='On a gauge-normal slice the tree Hessian is positive definite. A finite shell is smooth near the tree orbit. The implicit-function theorem therefore gives a nearby local minimum modulo gauge for sufficiently small formal loop coefficient, including all264 normals; no explicit all-normal bound at coefficient1 is asserted.',
      boundary='This is a complete one-loop shell determinant inventory, and a numerical minimum in the3-real SM-singlet slice, not a global/all264-mode quantum-stability certificate at the benchmark, physical pole masses, MS vacuum, UV completion or k->0 resummation. Finite matching/cutoff data are inputs.')


def hesse_D(h):
    h=np.asarray(h);return np.column_stack([h*h,np.sqrt(2)*np.array([h[1]*h[2],h[0]*h[2],h[0]*h[1]])])


def joint_potential(u,h,ku=1.,kh=1.,kap=1.):
    ru=np.vdot(u,u).real;rh=np.vdot(h,h).real;D=hesse_D(h)
    return float(ku*(ru-1)**2+kh*(rh-1)**2+kap*(ru*rh*rh-np.vdot(D@u.conj(),D@u.conj()).real))


@lru_cache(None)
def joint_vacuum_vectors():
    w=np.exp(2j*np.pi/3)
    hs=np.array(list(np.eye(3))+[np.array([1,w**r,w**t])/np.sqrt(3) for r,t in itertools.product(range(3),repeat=2)])
    us=np.array([np.array([1,0],complex)]*3+[np.array([1,np.sqrt(2)*w**(r+t)])/np.sqrt(3) for r,t in itertools.product(range(3),repeat=2)])
    return us,hs


def reye_alignment_defect(u,h,config):
    us,hs=joint_vacuum_vectors()
    f=abs(us.conj()@u)**2*abs(hs.conj()@h)**2
    C=sum(np.prod(f[list(t)]) for t in config)
    return float(C-(11/243)*(np.vdot(u,u).real*np.vdot(h,h).real)**3)


def joint_reye_potential(u,h,config,lam=1.):
    return joint_potential(u,h)+lam*reye_alignment_defect(u,h,config)**2


def joint_flavor():
    w=-s.Rational(1,2)+s.I*s.sqrt(3)/2
    F=s.Matrix(3,3,lambda i,j:w**(i*j)/s.sqrt(3));P=s.diag(1,1,w)
    RF=s.Matrix([[1,s.sqrt(2)],[s.sqrt(2),-1]])/s.sqrt(3);RP=s.diag(1,w)
    h=s.Matrix(s.symbols('h0:3'));D=s.Matrix([[h[i]**2,s.sqrt(2)*h[(i+1)%3]*h[(i+2)%3]] for i in range(3)])
    def symbolic_D(v):return s.Matrix([[v[i]**2,s.sqrt(2)*v[(i+1)%3]*v[(i+2)%3]] for i in range(3)])
    for G,R in [(F,RF),(P,RP)]:
        assert all(s.simplify(s.expand(a))==0 for a in symbolic_D(G*h)-G.conjugate()*D*R.T)
    rays=[np.eye(3,dtype=complex)[i] for i in range(3)]
    rays +=[np.array([1,complex(w.evalf())**r,complex(w.evalf())**t])/np.sqrt(3) for r,t in itertools.product(range(3),repeat=2)]
    vac=[]
    for h in rays:
        K=hesse_D(h).conj().T@hesse_D(h);ev,Q=np.linalg.eigh(K)
        assert abs(ev[0])<1e-13 and abs(ev[1]-1)<1e-13
        u=Q[:,-1].conj();assert abs(joint_potential(u,h))<1e-13
        vac.append(dict(h=[[float(z.real),float(z.imag)] for z in h],u=[[float(z.real),float(z.imag)] for z in u]))
    # Canonical real fields x: complex fields=(xR+i*xI)/sqrt2.
    q=np.array([np.sqrt(2),0,0,0,np.sqrt(2),0,0,0,0,0])
    def pot(q):return joint_potential((q[:2]+1j*q[2:4])/np.sqrt(2),(q[4:7]+1j*q[7:])/np.sqrt(2))
    H=finite_hessian(pot,q,h=2e-4);ev=np.linalg.eigvalsh(H)
    assert np.max(abs(ev-np.array([0,0,1,1,2,2,2,2,4,4])))<2e-6
    return dict(status='PASS',map='D(h) columns=(h0^2,h1^2,h2^2) and sqrt2(h1h2,h0h2,h0h1). D(Gh)=conjugate(G) D(h) R^T for the actual normalized11600 Hesse generators.',
      action='u->Ru, h->Gh; D(h)conjugate(u)->conjugate(G) D(h)conjugate(u).',
      potential='V=(u†u-1)^2+(h†h-1)^2+kappa[(u†u)(h†h)^2-||D(h)conjugate(u)||^2], kappa>0. The last term is nonnegative by K=D†D>=0 and TrK=(h†h)^2.',
      minimal_degree='With independent common U1 phases of u and h, every renormalizable parent invariant is a polynomial of their norms: Heisenberg X/Z act trivially on u, irreducibly on h; Sym2(h)=conjugate(h representation) tensor the same irreducible Hesse doublet. Mixed angular alignment first appears at field degree6. No claim is made without the two U1 assumptions.',
      global_zero_proof='At unit norms a zero requires rankD=1 and conjugate(u) in its top eigenspace. If h has zeros, rank1 forces a coordinate ray. If all hi are nonzero, rank1 is equivalent to h0^3=h1^3=h2^3. These are exactly3 coordinate plus9 equal-amplitude cube-root rays. Thus12 joint projective minima, with two continuous U1 phase circles each.',
      projective_vacua=vac,projective_count=12,canonical_Hessian=H.tolist(),exact_mass_squared=[0,0,1,1,2,2,2,2,4,4],
      CP_scope='All12 minima are one parent orbit; every ray has a parent generalized CP. The paired u rays are the4 tetrahedral vertices, so the11600 CP discriminant W vanishes. This degree6 selector aligns fields but does not produce generic CP breaking or observed flavor.',
      radiative_boundary='The parent with both U1 phases forbids angular dimension4 terms in this field inventory, but allows angular degree6 and higher terms. This is a symmetry classification, not all-loop stability or a derivation of target radii/couplings.')


def spherical_constraints():
    # Local jet calculus: total radial derivative, with independent smearing jets.
    keys=['L','R','pL','pR','phi','p','N','M','v','w']
    jets={k:s.symbols(k+'0:5',real=True) for k in keys}
    def dx(f):return s.expand(sum(s.diff(f,z[i])*z[i+1] for z in jets.values() for i in range(4)))
    def euler(f,k):
        z=jets[k];return s.simplify(sum((-1)**j*repeat_dx(s.diff(f,z[j]),j) for j in range(3)))
    def repeat_dx(f,n):
        for i in range(n):f=dx(f)
        return f
    L,R,pL,pR,phi,p=[jets[k][0] for k in ['L','R','pL','pR','phi','p']]
    L1,R1,pL1,ph1=[jets[k][1] for k in ['L','R','pL','phi']]
    A,B,alpha,beta,C=s.symbols('A B alpha beta C',real=True)
    kinetic=-pL*pR/R+L*pL*pL/(2*R*R)
    spatial=R*jets['R'][2]/L-R*R1*L1/L**2+R1**2/(2*L)-L/2
    hm=alpha*p*p/(2*L*R*R)+beta*R*R*ph1*ph1/(2*L)
    h=A*kinetic+B*spatial+hm+C*L*R*R
    d=pR*R1-L*pL1+p*ph1
    def pb(f,g):
        return s.simplify(sum(euler(f,q)*euler(g,p)-euler(f,p)*euler(g,q) for q,p in [('L','pL'),('R','pR'),('phi','p')]))
    N,M=jets['N'][0],jets['M'][0];v,w=jets['v'][0],jets['w'][0]
    b=pb(N*h,M*h);smear=N*jets['M'][1]-M*jets['N'][1]
    # Bracket densities differ by a total derivative; their Euler derivatives vanish.
    target=smear/L**2*(A*B*(pR*R1-L*pL1)+alpha*beta*p*ph1)
    defect=s.factor(b-target)
    residuals={k:s.factor(euler(defect,k)) for k in ['L','R','pL','pR','phi','p','N','M']}
    assert all(x==0 for x in residuals.values())
    # Universal cone condition is exact and nonconstant: alpha beta = A B.
    mismatch=s.factor(target-A*B*smear*d/L**2)
    assert s.simplify(mismatch-(alpha*beta-A*B)*p*ph1*smear/L**2)==0
    dd=pb(v*d,w*d)-(v*jets['w'][1]-w*jets['v'][1])*d
    assert all(euler(dd,k)==0 for k in ['L','R','pL','pR','phi','p','v','w'])
    hd=pb(N*h,v*d)+v*jets['N'][1]*h
    assert all(euler(hd,k)==0 for k in ['L','R','pL','pR','phi','p','N','v'])
    # A coarse mean field does not retain the nonlinear structure function.
    exact=s.Rational(1,2)*(1+s.Rational(1,4));naive=1/(s.Rational(3,2)**2)
    assert exact-naive==s.Rational(13,72)
    return dict(status='PASS',canonical_action='Integral dt dr [pL Ldot+pR Rdot+p phidot-N H-v D], supplied spherical metric ds3^2=L^2 dr^2+R^2 dOmega2, L,R>0. Compactly supported smearings or vanishing boundary variations.',
      Hamiltonian=str(h),momentum=str(d),
      exact_brackets='{H[N],H[M]}=D[A B (N Mprime-M Nprime)/L^2] iff alpha beta=A B; {D[v],D[w]}=D[v wprime-w vprime]; {H[N],D[v]}=-H[v Nprime]. All checked modulo total derivatives by Euler jets.',
      propagation_mismatch=str(mismatch),universal_cone='The scalar kinetic/gradient product must equal the gravitational product for this same nonlinear spatial metric structure function. Overall gravitational normalization remains input.',
      coarse_structure_counterexample={'fine_mean_inverse_metric':'5/8','inverse_mean_L_squared':'4/9','difference':'13/72'},
      count='Three canonical pairs and two first-class constraints leave one local scalar pair. Vacuum spherical gravity has no local graviton polarizations; angular nonspherical modes are omitted.',
      boundary='Classical Kuchar/Einstein-scalar constraint algebra is prior theory, reproduced as an executable nonlinear control. Not a W33-derived action, native finite subdivision algebra, full3D locality or a nonlinear perfect coarse action. Averages require extra subcell/correlation data.')


def lorentzian_flux():
    m=np.arange(-8,9);e=.2;volume=2.;rho=-.7
    energy=volume*(rho+e*e*m*m/2)
    U=lambda t:np.diag(np.exp(-1j*t*energy))
    assert np.max(abs(U(.7)@U(.2)-U(.9)))<1e-14
    assert np.max(abs(U(.7).conj().T@U(.7)-np.eye(17)))<1e-14
    shift=np.zeros((17,17));shift[np.arange(1,17),np.arange(16)]=1
    assert np.linalg.norm(shift@np.eye(17)[:,8])==1
    C=.13
    shifted=np.diag(np.exp(-1j*.7*(energy+volume*C)))
    assert np.max(abs(shifted-np.exp(-1j*.7*volume*C)*U(.7)))<1e-14
    # A topological Euler constraint and its membrane charge lattice.
    a=s.Matrix([[0,1]]);q=s.Matrix([1,0]);assert a*q==s.zeros(1,1)
    Delta,tau,r=s.symbols('Delta tau r',positive=True)
    bounce=2*s.pi**2*tau*r**3-s.pi**2*Delta*r**4/2
    radius=3*tau/Delta;B=s.simplify(bounce.subs(r,radius))
    assert B==27*s.pi**2*tau**4/(2*Delta**3)
    assert s.diff(bounce,r,2).subs(r,radius)==-18*s.pi**2*tau**2/Delta
    return dict(status='PASS',canonical_model='For a supplied compact spatial slice of volumeV and compact three-form holonomytheta, L=thetadot^2/(2N e^2 V)-N V rho. p=thetadot/(N e^2 V) is integerm; H=N V[rho+e^2 m^2/2]. Fixed endpoint holonomy defines the canonical boundary polarization; fixed flux uses its Legendre boundary transform.',
      kernel='K(theta_f,theta_i;T)=(1/(2pi)) sum_m exp[i m(theta_f-theta_i)-i T V(rho+e^2 m^2/2)]. The stored window[-8,8] is an exact unitary restriction of the free flux Hamiltonian, not a cyclic membrane truncation.',
      flux_labels=m.tolist(),energies=energy.tolist(),semigroup_and_unitarity=True,
      membrane='exp(i theta) raisesm by1. The finite window shift is only a partial isometry and its edge loss is retained. It cannot be made cyclic without changing the charge physics.',
      fixed_background_shift='rho->rho+C changes every fixed-background amplitude by the common phase exp(-i C V T). If lapse/metric is integrated, C changes the gravitational Hamiltonian constraint throughV C; the phase identity alone does not sequester vacuum energy.',
      Euler_charge_law='At fixed topology a dot n=-chi, a membrane chargeq stays in the sector iff a dot q=0. With one Euler-conjugate form and nonzeroa, every nonzero charge exits. With distinct forms a=(0,1), q=(1,0), the ordinary vacuum flux may jump while the Euler-conjugate flux remains fixed. Neither the new holonomytheta nor its integerm is the old rigid Euler multiplier.',
      neutral_charge_example={'a':[0,1],'q':[1,0],'constraint_pairing':0},
      flat_thin_wall={'action':str(bounce),'radius':str(radius),'exponent':str(B),'radial_second_derivative':str(s.diff(bounce,r,2).subs(r,radius)),'energy_drop':'e^2(m-1/2) for m->m-1'},
      graviton_boundary='Neither the canonical flux rotor nor the fixed-background phase removes the11624 terms a1 M^6/(2K)+a2 M^8/K^2. Full coupled gravity, boundary/corner measures and flux-transition rates with gravitational backreaction remain open.',
      boundary='Compactness, e, tension, volume, rho and topology are supplied. The flat thin-wall bounce has the usual radial negative mode; gravitational bounce and measured CC selection are not computed. Prior11307/11324 own different coupled cap/wall constructions; Brown-Teitelboim mechanism is standard.')


def reye_vacuum_audit():
    """Explicit incidence lifts; no equality from12/16 counts alone.

    BT544 owns the cyclic Reye;5580-5585 own A4 grid incidence;
    1089 owns dual Hesse;11262 owns the four qutrit MUBs.
    """
    from collections import Counter
    import networkx as nx
    from w33_witting_reye_toroidal_tomotope_collapse import reye_lines,build_reye_levi_graph
    # Exact Eisenstein arithmetic a+b*omega, omega^2+omega+1=0.
    def add(a,b):return (a[0]+b[0],a[1]+b[1])
    def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]-a[1]*b[1])
    roots=[(1,0),(0,1),(-1,-1)];zero=(0,0)
    raw=[tuple(roots[0] if i==j else zero for i in range(3)) for j in range(3)]
    raw +=[(roots[0],roots[r],roots[t]) for r,t in itertools.product(range(3),repeat=2)]
    def det(indices):
        ans=zero
        for p in itertools.permutations(range(3)):
            term=roots[0]
            for i in range(3):term=mul(term,raw[indices[i]][p[i]])
            sign=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
            ans=add(ans,(sign*term[0],sign*term[1]))
        return ans
    dependent={t for t in itertools.combinations(range(12),3) if det(t)==zero}
    geom={tuple(k for k in range(12) if k in [i,j] or det((i,j,k))==zero) for i,j in itertools.combinations(range(12),2)}
    geom=sorted(t for t in geom if len(t)>=3)
    assert len(geom)==9 and all(len(t)==4 for t in geom) and len(dependent)==36
    w=np.exp(2j*np.pi/3)
    rays=np.array(list(np.eye(3))+[np.array([1,w**r,w**t])/np.sqrt(3) for r,t in itertools.product(range(3),repeat=2)])
    blocks=[[0,1,2],[3,8,10],[4,6,11],[5,7,9]]
    for b in blocks:assert np.max(abs(rays[b].conj()@rays[b].T-np.eye(3)))<1e-12
    F=np.array([[w**(i*j) for j in range(3)] for i in range(3)])/np.sqrt(3)
    gens=[F,np.diag([1,1,w]),np.roll(np.eye(3),1,axis=0),np.diag([1,w,w*w])]
    pg=[]
    for U in gens:
        overlap=abs(rays.conj()@(U@rays.T))**2
        p=tuple(int(i) for i in np.argmax(overlap,axis=0))
        assert len(set(p))==12 and np.max(abs(overlap[list(p),range(12)]-1))<1e-12
        pg.append(p)
    exact_gens=[[[roots[(i*j)%3] for j in range(3)] for i in range(3)],
      [[roots[1 if i==2 else 0] if i==j else zero for j in range(3)] for i in range(3)],
      [[roots[0] if i==(j+1)%3 else zero for j in range(3)] for i in range(3)],
      [[roots[i] if i==j else zero for j in range(3)] for i in range(3)]]
    for U,p in zip(exact_gens,pg):
        for i,h in enumerate(raw):
            v=[]
            for row in U:
                a=zero
                for b,z in zip(row,h):a=add(a,mul(b,z))
                v.append(a)
            assert any(a!=zero for a in v)
            for j,k in itertools.combinations(range(3),2):
                assert mul(v[j],raw[p[i]][k])==mul(v[k],raw[p[i]][j])
    def closure(gs):
        group={tuple(range(12))};queue=list(group)
        for p in queue:
            for a in gs:
                q=tuple(a[p[i]] for i in range(12))
                if q not in group:group.add(q);queue.append(q)
        return sorted(group)
    group=closure(pg);cp=tuple(int(i) for i in np.argmax(abs(rays.conj()@rays.conj().T)**2,axis=0))
    extended=closure(pg+[cp]);assert len(group)==216 and len(extended)==432
    base=reye_lines();configs=set()
    for ps in itertools.product(list(itertools.permutations(range(3))),repeat=4):
        mapping={(a,b):blocks[a][ps[a][b]] for a in range(4) for b in range(3)}
        configs.add(tuple(sorted(tuple(sorted(mapping[v] for v in L['points'])) for L in base)))
    assert len(configs)==432
    def transform(c,p):return tuple(sorted(tuple(sorted(p[i] for i in t)) for t in c))
    def orbits(gs):
        left=set(configs);out=[]
        while left:
            c=min(left);orbit={transform(c,p) for p in gs};assert orbit<=configs
            counts={sum(t in dependent for t in a) for a in orbit};assert len(counts)==1
            out.append(dict(size=len(orbit),stabilizer=len(gs)//len(orbit),collinear_triples=counts.pop(),representative=c));left-=orbit
        return out
    unitary=orbits(group);anti=orbits(extended)
    assert sorted(o['size'] for o in unitary)==[72]*6
    G=build_reye_levi_graph();even=[p for p in itertools.permutations(range(4)) if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2==0]
    grid=nx.Graph()
    for i,p in enumerate(even):
        for j in range(4):grid.add_edge(('P',i),('L',j,p[j]))
    matcher=nx.algorithms.isomorphism.GraphMatcher(G,grid);assert matcher.is_isomorphic()
    iso=matcher.mapping
    aut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(grid,grid).isomorphisms_iter())
    assert aut==576 and aut%len(group)!=0
    R=np.array([[int(p[j]==k) for j,k in itertools.product(range(4),repeat=2)] for p in even])
    centered=R@R.T-np.ones((12,12));assert np.linalg.matrix_rank(centered)==9
    gram=abs(rays.conj()@rays.T)**2
    assert np.linalg.matrix_rank(gram,tol=1e-10)==9
    assert np.linalg.matrix_rank(gram-np.ones((12,12))/3,tol=1e-10)==8
    # The actual joint u/h product projectors have cross-basis overlap1/9.
    joint=np.eye(12)
    for i,j in itertools.combinations(range(12),2):
        if not any(i in b and j in b for b in blocks):joint[i,j]=joint[j,i]=1/9
    assert np.max(abs(np.linalg.eigvalsh(joint)-np.array([2/3]*3+[1]*8+[2])))<1e-12
    # An actual added coupling, rather than a count interpretation.
    # All arithmetic below is exact in Q(omega); sqrt2 is factored from u1.
    from fractions import Fraction as Fr
    norm=lambda z:z[0]*z[0]-z[0]*z[1]+z[1]*z[1]
    label_block={i:a for a,b in enumerate(blocks) for i in b}
    for config in configs:
        for j in range(12):
            f=[Fr(1) if i==j else Fr(0) if label_block[i]==label_block[j] else Fr(1,9) for i in range(12)]
            C=sum((f[t[0]]*f[t[1]]*f[t[2]] for t in config),Fr(0))
            assert C==Fr(11,243)
    rng=np.random.default_rng(11629);sample_inputs=[];samples=[]
    for _ in range(4):
        uv=[tuple(int(i) for i in z) for z in rng.integers(-2,3,size=(2,2))]
        hv=[tuple(int(i) for i in z) for z in rng.integers(-2,3,size=(3,2))]
        fu=[Fr(norm(uv[0]))]*3
        fh=[Fr(norm(z)) for z in hv]
        for r,t in itertools.product(range(3),repeat=2):
            a=add(uv[0],mul((2,0),mul(roots[-(r+t)%3],uv[1])))
            b=add(hv[0],add(mul(roots[-r%3],hv[1]),mul(roots[-t%3],hv[2])))
            fu.append(Fr(norm(a),3));fh.append(Fr(norm(b),3))
        f=[a*b for a,b in zip(fu,fh)]
        reference=Fr(11,243)*(norm(uv[0])+2*norm(uv[1]))**3*sum(norm(z) for z in hv)**3
        samples.append([sum((f[t[0]]*f[t[1]]*f[t[2]] for t in config),Fr(0))-reference for config in sorted(configs)])
        sample_inputs.append(dict(u0=list(uv[0]),u1_div_sqrt2=list(uv[1]),h=[list(z) for z in hv]))
    signatures=list(zip(*samples));squared=[tuple(z*z for z in a) for a in signatures]
    assert len(set(signatures))==len(set(squared))==432
    for o in unitary:assert o['stabilizer']==3
    for o in anti:assert o['stabilizer']==3
    distribution=Counter(sum(t in dependent for t in c) for c in configs)
    return dict(status='PASS',prior_owners=['BT544','5580-5585','BT5776-BT5783','1089','11262'],
      Higgs_ray_labels='0,1,2 are coordinate rays;3+3r+t is(1,omega^r,omega^t)/sqrt3.',MUB_blocks=blocks,
      exact_projective_lines=geom,dependent_triples=36,
      projective_geometry='The vacuum rays are the known dual Hesse12_3,9_4 configuration, not projective Reye12_4,16_3. The four orthogonal triads are independent, so cannot be Reye geometric lines in this realization.',
      concrete_Reye_A4_isomorphism=[dict(point=[a,b],permutation=list(even[iso[('P',a,b)][1]])) for a,b in itertools.product(range(4),range(3))],
      Reye_incidence_rank=int(np.linalg.matrix_rank(R)),Reye_centered_rank=9,Reye_automorphisms=aut,
      Clifford_ray_group_order=len(group),Clifford_CP_ray_group_order=len(extended),Clifford_generators=pg,
      MUB_preserving_Reye_lifts=len(configs),collinearity_histogram=dict(distribution),unitary_lift_orbits=unitary,CP_extended_lift_orbits=anti,
      symmetry_obstruction='The faithful216-element induced unitary group cannot preserve any Reye configuration on these12 rays: it would embed in Aut(Reye)=576, but216 does not divide576. Every432 tested MUB-preserving lift has unitary stabilizer3; this432 family is exhaustive only for independent within-triad relabelings of BT544, not every abstract Reye labelling.',
      Higgs_projector_Gram_spectrum={'4':1,'1':8,'0':3},Higgs_centered_rank=8,
      joint_product_projector_Gram_spectrum={'2':1,'2/3':3,'1':8},joint_projector_rank=12,
      coupling=dict(definition='f_i=|u_i†u|^2 |h_i†h|^2, C_sigma=sum_{Reye triples} product_i f_i; addlambda[C_sigma-(11/243)(u†u h†h)^3]^2 toV11627, lambda>0. Sigma is a supplied432-valued discrete incidence field. The additional field polynomial has degree24 and is nonnegative.',
        exact_zero_value='C_sigma=11/243 at each of the12 normalized joint vacua, for every432 lift; exact rational enumeration verifies5184 incidences. The full zero set is432 times12 projective choices, plus the two common phase circles.',
        exact_polynomial_separation_inputs=sample_inputs,separated_defect_polynomials=432,separated_squared_defect_polynomials=432,
        covariance='Under the parent unitary/antiunitary ray permutations, sigma andthe12 vacuum projectors are permuted together. This makes C_sigma andthe supplied potential invariant. Four exact Eisenstein evaluations distinguish every432 polynomial, including its squared defect; sigma is not an irrelevant decoupled label.',
        CP='The unitary stabilizer andCP-extended stabilizer of each sigma both have order3. Therefore none ofthe216 antiunitary elements inthis declared parent fixes sigma. Every classical zero sector breaks all generalized CP transformations inthis parent, while the total potential preserves the parent. This does not certify absence of all accidental CP transformations in other field inventories.',
        boundary='This is an engineered finite order-parameter model with an added discrete432-state field anddegree24 coupling, not a derived continuous renormalizable Spin10 theory, a unique flavor phase, a finite-volume quantum symmetry-breaking theorem or a prediction of CKM/PMNS phases.'),
      connection='Existing Reye incidence provides a concrete parent-covariant CP-breaking order parameter for the12 existing joint vacua when the supplied discrete field andexplicit coupling are added. The16-dimensional spinor and16 Reye lines still have no identified intertwiner.',

      boundary='This connects existing Hesse vacuum data with existing Reye incidence through explicit maps and enumerated choices; it does not infer masses, gravity, a Spin10 representation or a physical Reye interaction from12/16 counts.')


def produce():
    c=dict(status='PASS',passes=list(range(11625,11630)),reservation=RESERVATION)
    for name,f in [('fermion_matching',fermion_matching),('quantum_vacuum',quantum_vacuum),('joint_flavor',joint_flavor),('spherical_constraints',spherical_constraints),('lorentzian_flux',lorentzian_flux),('reye_vacuum_audit',reye_vacuum_audit)]:
        c[name]=f();print(name,'PASS',flush=True)
    paths=['analysis/w33_pass11620_11624_covariant_pair_vacuum.py','data/w33_pass11620_11624_covariant_pair_vacuum.json','analysis/w33_pass11615_11619_parent_pairs_constraints.py','analysis/w33_pass11600_dynamical_hesse_flavor.py','analysis/PASS11620_11624_COVARIANT_PAIR_VACUUM.md','analysis/w33_witting_reye_toroidal_tomotope_collapse.py','analysis/PASS5580_5585_reye_psl2_permutation_frame.md','analysis/BT5776_BT5783_reye_latin_common_core.md']
    c['source_sha256']={p:ph(ROOT/p) for p in paths};c['producer_sha256']=ph(Path(__file__))
    OUT.write_text(json.dumps(c,indent=2,default=str)+'\n');return c

if __name__=='__main__':produce()
