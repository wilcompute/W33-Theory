"""Eight scoped physical interfaces, built on the actual11663 normal map.

1068/1077 own the G25 parabolic;11271/11636 own the E6 family cubic.
11615 owns auxiliary-chain completions;11639 owns the tree-overlap obstruction.
11546/11624 own affine fixed-flux Ward identities. No complete TOE is claimed.
"""
from __future__ import annotations

from collections import deque
from functools import lru_cache
import hashlib
import itertools as it
import json
from pathlib import Path
import sys

import numpy as np
import sympy as s
from scipy.integrate import quad
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'analysis'))
import w33_pass11663_odd_weil_normal_map as N
import w33_pass1068_chevie_g25_g32_matrices as EIS
from w33_pass11278_symplectic_ring_geometry import points, J
from w33_pass11279_history_flux_obstruction import complex_data
from w33_pass11636_11640_operator_selector_transitions import incidence_yukawas, family_rays

OUT = ROOT/'data/w33_pass11664_11671_kernel_dynamics.json'


def digest(path):
    p=Path(path);raw=p.read_bytes()
    if p.suffix!='.npz':raw=raw.replace(b'\r\n',b'\n')
    return hashlib.sha256(raw).hexdigest()


@lru_cache(None)
def kernel_generators():
    E, O = N.parity_bases()
    E = E*s.diag(1, *([1/s.sqrt(2)]*4)); O = O/s.sqrt(2)
    gates = N.canonical_generators()
    SUM = s.zeros(9)
    for j, (a, b) in enumerate(N.PTS):
        SUM[N.PTS.index((a, (b+a) % 3)), j] = 1
    gates = {k: gates[k] for k in ['D0', 'D1', 'F1', 'CZ']} | {'SUM01': SUM}
    rows = []
    for name, gate in gates.items():
        ge = (E.T*gate*E).applyfunc(N.reduce_w)
        go = (O.T*gate*O).applyfunc(N.reduce_w)
        assert go[1:, 0] == s.zeros(3, 1)
        assert ge[:2, 2:] == s.zeros(2, 3) and ge[2:, :2] == s.zeros(3, 2)
        R = ge[2:, 2:]
        assert go[1:, 1:] == R
        rows.append((name, R, go[0, 0]))
    return rows


def eis_matrix(A):
    return tuple(EIS.Eis(s.Poly(N.reduce_w(z), N.W).nth(0),
                         s.Poly(N.reduce_w(z), N.W).nth(1)) for z in A)


def emul(A, B):
    return tuple(sum((A[3*i+k]*B[3*k+j] for k in range(3)), EIS.ZERO)
                 for i in range(3) for j in range(3))


@lru_cache(None)
def exact_kernel_group():
    gens = [eis_matrix(R) for _, R, _ in kernel_generators()]
    I = tuple(EIS.ONE if i == j else EIS.ZERO for i in range(3) for j in range(3))
    seen = {I}; queue = deque([I])
    while queue:
        A = queue.popleft()
        for g in gens:
            B = emul(A, g)
            if B not in seen:
                seen.add(B); queue.append(B)
        assert len(seen) <= 648
    assert len(seen) == 648
    # Literal equality with the earlier CHEVIE G25, not a fitted conjugator.
    for v in [(0, 0, -1), (1, 1, 1), (0, 1, 0)]:
        r = EIS.reflection(v)
        assert tuple(z for row in r for z in row) in seen
    return seen


def kernel_sector():
    group = exact_kernel_group()
    rs = dict((name, R) for name, R, _ in kernel_generators())
    X, Z = rs['SUM01'], rs['CZ']
    assert (Z*X-N.W*X*Z).applyfunc(N.reduce_w) == s.zeros(3)
    # Schur commutant: the actual native X and Z, no arbitrary triplet basis.
    B = s.Matrix(3, 3, s.symbols('b0:9'))
    eq = [N.reduce_w(z) for z in (B*X-X*B)] + [N.reduce_w(z) for z in (B*Z-Z*B)]
    assert len(s.linsolve(eq, list(B)).free_symbols) == 1
    return dict(status='PASS', exact_group_order=len(group),
                literal_prior_G25_generators_present=True,
                transverse_odd_equals_even_mass_kernel=True,
                generators=[dict(name=n, R=[[str(z) for z in row] for row in R.tolist()],
                                 odd_axis_character=str(c), determinant=str(N.reduce_w(R.det())))
                            for n, R, c in kernel_generators()],
                H27_relation='ZX=omega XZ; center=omega I3',
                bilinear_boundary='Identical triplets have no invariant bare bilinear: the H27 center acts by omega^2. A conjugate Dirac pair admits only a scalar mass under unbroken H27. Chiral field content and broken-family Yukawas are extra data.',
                prior_owners=['analysis/w33_pass1068_chevie_g25_g32_matrices.py',
                              'analysis/w33_pass1077_g32_g25_invariant_restriction.py',
                              'analysis/2026-09-21_physical_external_a2_h27.md'])


@lru_cache(None)
def parent_maps():
    f = s.Matrix(N.FVAR)
    pairs = list(it.combinations_with_replacement(range(4), 2))
    q = s.Matrix(s.symbols('q0:10')); z = s.Matrix(s.symbols('z0:5'))
    Q = s.Matrix([f[i]*f[j]*(s.sqrt(2) if i != j else 1) for i, j in pairs])
    P = s.Matrix([-2*q[1]*q[8]-2*q[2]*q[6]-2*q[3]*q[5],
                  2*q[1]*q[4]+2*q[2]*q[7]+2*q[3]*q[9],
                  -2*q[0]*q[1]-2*q[5]*q[7]+2*q[6]*q[9],
                  -2*q[0]*q[2]+2*q[4]*q[5]-2*q[8]*q[9],
                  -2*q[0]*q[3]-2*q[4]*q[6]+2*q[7]*q[8]])
    _, _, K = N.cubic_normal_map(); F = N.pfaffian_vector(K)
    assert (P.subs(dict(zip(q, Q)), simultaneous=True)-s.diag(1,*([s.sqrt(2)]*4))*F).applyfunc(s.expand) == s.zeros(5, 1)
    return f, q, z, Q, P


def realify(A):
    """Holomorphic differential in interleaved real/imaginary coordinates."""
    B = s.zeros(2*A.rows, 2*A.cols)
    for i in range(A.rows):
        for j in range(A.cols):
            r, t = s.re(A[i,j]), s.im(A[i,j])
            B[2*i,2*j] = B[2*i+1,2*j+1] = r
            B[2*i,2*j+1] = -t; B[2*i+1,2*j] = t
    return B


@lru_cache(None)
def parent_hessian():
    f, q, z, Q, P = parent_maps()
    fs = {f[0]: 1, **dict.fromkeys(f[1:], 0)}
    qs = dict(zip(q, Q.subs(fs)))
    DQ, DP = Q.jacobian(f).subs(fs), P.jacobian(q).subs(qs)
    A = (-DQ).row_join(s.eye(10)).row_join(s.zeros(10,5))
    B = s.zeros(5,4).row_join(-DP).row_join(s.eye(5))
    C = s.zeros(5,14).row_join(s.eye(5))
    jr = realify(A.col_join(B).col_join(C))
    radial = s.zeros(1,38); radial[0,0] = 2
    jr = jr.col_join(radial); H = 2*jr.T*jr
    effective = H[:8,:8]-H[:8,8:]*H[8:,8:].inv()*H[8:,:8]
    assert effective == s.diag(8,0,*([s.Rational(8,3)]*6))
    # The auxiliary differential has an invertible block-triangular square
    # submatrix. Its Gram is positive definite; Schur congruence and the
    # seven positive entries above give full rank30+7 without costly general
    # symbolic principal-minor detection.
    assert A[:,4:14] == s.eye(10) and A[:,14:] == s.zeros(10,5)
    assert B[:,14:] == s.eye(5)
    return H, effective


def parent_sector():
    _, q, _, Q, P = parent_maps(); H, low = parent_hessian()
    E, O = N.parity_bases()
    E = E*s.diag(1,*([1/s.sqrt(2)]*4)); O = O/s.sqrt(2)
    # Polarization must intertwine on all of Sym^2(4), not just on its
    # Veronese locus Q(f). This tests the actual auxiliary-field action.
    covariance = []
    for name,gate in N.canonical_generators().items():
        go = (O.T*gate*O).applyfunc(N.reduce_w)
        ge = (E.T*gate*E).applyfunc(N.reduce_w)
        transformed = Q.subs(dict(zip(N.FVAR,go*s.Matrix(N.FVAR))),simultaneous=True)
        pairs = list(it.combinations_with_replacement(range(4),2))
        R = s.Matrix(10,10,lambda i,j:N.reduce_w(s.expand(transformed[i]).coeff(
            N.FVAR[pairs[j][0]]*N.FVAR[pairs[j][1]])/(s.sqrt(2) if pairs[j][0]!=pairs[j][1] else 1)))
        difference = P.subs(dict(zip(q,R*q)),simultaneous=True)-ge*P
        assert all(N.reduce_w(v)==0 for v in difference)
        covariance.append(name)
    return dict(status='PASS', real_fields=38, full_hessian_rank=37,
                full_auxiliary_covariance=covariance,
                relaxed_light_hessian=[str(low[i,i]) for i in range(8)],
                Q=[str(v) for v in Q], P=[str(v) for v in P],
                action='lambda(||f||^2-1)^2+||M q-Q(f)||^2+||M z-P(q)||^2+m_z^2||z||^2',
                frozen_q_matching='kappa=m_z^2/((M^2+m_z^2) M^4)',
                UV_orientation_log='-y^4 S log(B/A)/(64 pi^2)',
                scope='A supplied positive renormalizable parent, with f4+q10+z5 complex fields; common mass M and input couplings. The source tensors use the native normal map. It is not an E6 UV derivation or a prediction of renormalized kappa. Scalar/gauge loops remain open.',
                prior_owners=['analysis/PASS11615_11619_PARENT_PAIRS_CONSTRAINTS.md'])


def flavor_sector():
    prior = json.loads((ROOT/'data/w33_pass11631_11635_physical_interfaces.json').read_text())['physical_flavor']
    config, hi = prior['selected_config'], prior['selected_h']
    y1, y2 = incidence_yukawas(config, family_rays(True)[hi], True)
    e = s.Symbol('epsilon', real=True); yd = y1+e*y2
    hu, hd = (y1.H*y1).applyfunc(s.expand), (yd.H*yd).applyfunc(s.expand)
    comm = (hu*hd-hd*hu).applyfunc(s.expand)
    cp = s.factor(s.expand(s.trace(comm**3)/s.I))
    assert cp != 0
    U = s.eye(5)[:,2:]; axis_mass = s.zeros(5)
    axis_mass[0,1] = 1/s.sqrt(2); axis_mass[1,0] = -1/s.sqrt(2)
    # The added symmetric family operators are explicit; no identification of
    # antisymmetric Dirac masses with identical-Weyl Majorana masses.
    eta = s.Symbol('eta', real=True)
    full1 = axis_mass+eta*U*y1*U.T; full2 = axis_mass+eta*U*yd*U.T
    HH1, HH2 = (full1.H*full1).applyfunc(s.expand), (full2.H*full2).applyfunc(s.expand)
    cc = (HH1*HH2-HH2*HH1).applyfunc(s.expand)
    assert s.simplify(s.trace(cc**3)/s.I-eta**12*cp) == 0
    eps = s.Rational(1,100)
    assert yd.subs(e,eps).det() != 0 and y1.det() != 0
    archive = ROOT/'data/w33_pass11636_e6_cubic_inputs.npz'; data = np.load(archive)
    d, bs = data['d'], data['B']; assert d.shape == (27,27,27)
    for b in bs:
        assert not np.any(np.einsum('ai,ajk->ijk',b,d)+np.einsum('aj,iak->ijk',b,d)+np.einsum('ak,ija->ijk',b,d))
    return dict(status='PASS', embedding=U.tolist(), selected_config=config, selected_h=hi,
                Y1=[[str(v) for v in row] for row in y1.tolist()],
                Y2=[[str(v) for v in row] for row in y2.tolist()],
                exact_light_CP=str(cp), full5_CP_scaling='eta^12 times the prior exact light invariant',
                antisymmetric_triplet_CP='Tr([Hu,Hd]^3)=0 for all two bare3x3 skew Yukawas: each H is a scalar minus a rank-one projector; the commutator has rank<=2 and trace0.',
                E6_archive=str(archive.relative_to(ROOT)), E6_archive_sha256=digest(archive),
                joint_vacuum=joint_flavor_vacuum(np.array(y1,complex),np.array(y2,complex)),
                scope='A concrete conditional lift of prior11271/11636 symmetric E6-family operators into the actual Witting kernel at the reference ray. Symmetric additions explicitly change the antisymmetric-only Dirac model. Coefficients, selected Higgs sector and chirality are inputs; measured flavor and a global E6 field embedding are not derived.',
                prior_owners=['analysis/w33_pass11271_chiral_symmetric_yukawa_completion.py',
                              'analysis/PASS11636_11640_OPERATORS_SELECTORS_AND_TRANSITIONS.md'])


@lru_cache(None)
def native_connection():
    pts = points(3); _,_,lines,_ = complex_data()
    def canon(v):
        v = np.asarray(v,dtype=int)%3
        k = np.flatnonzero(v)[0]
        return tuple((v*pow(int(v[k]),-1,3))%3)
    index = {tuple(v):i for i,v in enumerate(pts)}
    v = np.array([1,0,0,0]); T = (np.eye(4,dtype=int)+np.outer(v,v@J))%3
    perm = [index[canon(T@a)] for a in pts]
    lookup = {tuple(sorted(line)):i for i,line in enumerate(lines)}
    perm += [40+lookup[tuple(sorted(perm[a] for a in line))] for line in lines]
    P = np.eye(80,dtype=int)[:,perm]
    # Column j is e_perm[j]: P acts by the displayed native vertex permutation.
    assert np.array_equal(P@P@P,np.eye(80,dtype=int))
    edges = [(p,40+i) for i,line in enumerate(lines) for p in line]
    inc = np.zeros((80,160),int)
    for k,(a,b) in enumerate(edges):inc[a,k]=-1;inc[b,k]=1
    graph = inc@inc.T; assert np.array_equal(P@graph@P.T,graph)
    adj = [[] for _ in range(80)]
    for k,(a,b) in enumerate(edges):adj[a].append((b,k));adj[b].append((a,k))
    visited = {0}; queue=[0]; tree=[]
    for a in queue:
        for b,k in adj[a]:
            if b not in visited:visited.add(b);queue.append(b);tree.append(k)
    L = inc[:,tree]@inc[:,tree].T
    Us = [np.eye(80,dtype=int),P,P@P]
    ls = [U@L@U.T for U in Us]
    assert all(np.count_nonzero(ls[i]-ls[j]) for i in range(3) for j in range(i))
    # Six declared fiber coordinates, four commuting gauge constraints and two
    # physical polarizations. This is an actual finite constraint witness, not
    # the nonlinear Dirac algebra of gravity.
    gauge = [np.diag([int(i==j) for i in range(6)]) for j in range(4)]
    physical = np.diag([0,0,0,0,1,1])
    W = np.zeros((240,240),int)
    for j,U in enumerate(Us):W[80*j:80*(j+1),80*j:80*(j+1)]=U
    C3 = np.array([[2,-1,-1],[-1,2,-1],[-1,-1,2]])
    hopping = W@np.kron(C3,np.eye(80,dtype=int))@W.T
    H = W@np.kron(np.eye(3,dtype=int),L)@W.T+hopping
    assert np.array_equal(W.T@H@W,np.kron(np.eye(3,dtype=int),L)+np.kron(C3,np.eye(80,dtype=int)))
    return P, inc, L, Us, hopping, H, gauge, physical, tree


def connection_sector():
    P,B,L,Us,hop,H,gauge,phys,tree = native_connection()
    assert all(np.array_equal(c@phys, np.zeros((6,6))) for c in gauge)
    # Link intertwining preserves any transported constraint. Preservation by
    # the FULL Hamiltonian additionally requires [Href,Ca]=0 in the reference
    # theory. The supplied fiber-projector witness satisfies this requirement.
    D = np.diag(np.arange(80))
    Cs = [U@D@U.T for U in Us]
    for j in range(3):
        k=(j+1)%3; link=Us[k]@Us[j].T
        assert np.array_equal(Cs[k]@link,link@Cs[j])
    return dict(status='PASS', native_vertices=80, native_edges=160,
                transvection_site_permutation=np.argmax(P,axis=0).tolist(), tree=tree,
                register_branches=3, transported_constraints=4, physical_fiber=2,
                flat_connection_equivalence='diag(Uj)^dag H diag(Uj)=I3 tensor Ltree+Lcycle3 tensor I80',
                scope='An explicit quantum connection on three automorphic native trees, with exact link intertwiners and four supplied commuting projector constraints. It preserves a transported constraint algebra when the reference Hamiltonian already preserves it; a full HR constraint set has not been supplied. Flat links describe frame copies; this does not generate nonlinear Einstein gravity or independent topology dynamics.',
                prior_owners=['analysis/PASS11636_11640_OPERATORS_SELECTORS_AND_TRANSITIONS.md',
                              'analysis/w33_pass11289_cycle_gram_gluing_flux.py'])


def flux_operators(C=.3,q=1.,alpha=1.,size=5):
    n=np.arange(1,size+1); U=np.diag(np.exp(-1j*C*q*n/alpha))
    shift=np.eye(size,k=-1,dtype=complex)
    return n,U,shift


def flux_sector():
    n,U,shift=flux_operators(); phase=np.exp(1j*.3)
    assert np.allclose(U.conj().T@shift@U,phase*shift)
    psi=np.ones(5)/np.sqrt(5)
    before=np.vdot(psi,shift@psi); after=np.vdot(U@psi,shift@(U@psi))
    assert abs(after-phase*before)<1e-12 and abs(after-before)>.1
    assert np.allclose(abs(U@psi)**2,abs(psi)**2)
    return dict(status='PASS', fluxes=n.tolist(),
                common_shift_phase='U_C|n>=exp(-i C n q/alpha)|n>',
                membrane_covariance='U_C^dag S U_C=exp(i C q/alpha) S',
                unchanged_flux_probabilities=True, fixed_membrane_reference_changes_coherence=True,
                scope='The fixed-sector affine Ward result gives only a phase in each sector. Across a declared coherent flux superposition, a fixed membrane-reference operator rotates; transforming that reference restores covariance. This is not a violation of local sequestering. Superselection, membrane dynamics, allowed gauge-invariant states and a flux measure remain inputs; no cosmological constant is selected.',
                prior_owners=['analysis/PASS11620_11624_COVARIANT_PAIR_VACUUM.md',
                              'analysis/PASS11625_11629_COMPOSITES_JOINT_VACUA.md'],
                primary_sources=['https://arxiv.org/abs/1505.01492','https://arxiv.org/abs/1812.11625'])


def full_loop(squared_radius, orientation, y=.2, A=.01, B=.25):
    r=squared_radius
    return -quad(lambda x:x*np.log1p(y*y*r*r/(2*x)+y**4*r**4*orientation/(16*x*x)),A,B,
                 epsabs=1e-14,epsrel=1e-12)[0]/(4*np.pi*np.pi)


def radial_derivatives(r,y=.2,A=.01,B=.25,lam=1.):
    c=y*y*r*r/2; integral=B-A-c*np.log((B+c)/(A+c))
    first=2*lam*(r-1)-y*y*r*integral/(4*np.pi*np.pi)
    second=2*lam-y*y*quad(lambda x:x*(x-c)/(x+c)**2,A,B,epsabs=1e-14)[0]/(4*np.pi*np.pi)
    return first,second


def radial_sector():
    y,A,B,lam,kappa=.2,.01,.25,1.,1e-5
    bound=y**4*np.log(B/A)/(64*np.pi*np.pi)
    assert kappa>bound and 2*lam>y*y*(B-A)/(4*np.pi*np.pi)
    r=brentq(lambda r:radial_derivatives(r,y,A,B,lam)[0],1.,2.,xtol=1e-14)
    _,ss=radial_derivatives(r,y,A,B,lam)
    threshold=y**4*np.log((B+y*y*r*r/2)/(A+y*y*r*r/2))/(64*np.pi*np.pi)
    h=[0.,4*r*ss,*([16*r**3*(kappa-threshold)]*6)]
    assert min(h[1:])>0
    return dict(status='PASS', benchmark=dict(y=y,shell=[A,B],lambda_=lam,kappa=kappa,
                 squared_radius=r,all_real_hessian=h,global_kappa_bound=bound,local_kappa_threshold=threshold),
                exact_global_conditions='kappa>y^4 log(B/A)/(64 pi^2) and 2lambda>y^2(B-A)/(4 pi^2)',
                theorem='Under these sufficient conditions the full radius-free finite-shell one-Dirac-loop potential has exactly the40 Witting projective vacuum rays, one unique positive radius and seven positive real normal curvatures. The common phase remains flat.',
                radial_second_bound='|Vfermion,ss|<=y^2(B-A)/(4 pi^2)',
                scope='Global proof for the supplied scalar+five-species Dirac finite-shell action. No fixed-radius assumption remains. Scalar/gauge loops, renormalized coefficients, physical units and continuum UV matching remain open.',
                prior_owners=['analysis/PASS11663_ODD_WEIL_NORMAL_MAP.md'])


def joint_flavor_potential(x,Ys,y=.2,kappa=2.5e-5):
    f=np.asarray(x)[::2]+1j*np.asarray(x)[1::2];r=np.vdot(f,f).real
    masses=np.concatenate([np.linalg.svd(N.canonical_mass(f)+Y,compute_uv=False)**2 for Y in Ys])
    loop=-quad(lambda z:z*np.sum(np.log1p(y*y*masses/z)),.01,.25,epsabs=1e-14)[0]/(8*np.pi*np.pi)
    return (r-1)**2+kappa*N.order_parameter(f)+loop


def joint_flavor_hessian(x,Ys,order=64,y=.2,kappa=2.5e-5):
    """Analytic log-determinant derivatives; polarization is exact for M quadratic."""
    f=x[::2]+1j*x[1::2];r=np.vdot(f,f).real;D=N.canonical_mass(f)
    e=np.array([np.eye(4)[i//2]*(1j if i%2 else 1) for i in range(8)])
    first=np.array([(N.canonical_mass(f+v)-N.canonical_mass(f-v))/2 for v in e])
    second=np.array([[N.canonical_mass(f+a+b)-N.canonical_mass(f+a)-N.canonical_mass(f+b)+D for b in e] for a in e])
    nodes,weights=np.polynomial.legendre.leggauss(order);nodes=.12*nodes+.13;weights*=.12
    H=np.diag([8*r+4*(r-1),4*(r-1),*([4*(r-1)+16*kappa*r**3]*6)])
    grad=4*(r-1)*np.asarray(x)
    for Y in Ys:
        mass=D+Y;h=mass.conj().T@mass
        hi=np.array([a.conj().T@mass+mass.conj().T@a for a in first])
        hij=np.array([[second[i,j].conj().T@mass+mass.conj().T@second[i,j]+first[i].conj().T@first[j]+first[j].conj().T@first[i] for j in range(8)] for i in range(8)])
        for z,weight in zip(nodes,weights):
            inverse=np.linalg.inv(np.eye(5)+y*y*h/z);t=inverse@hi
            grad-=weight*y*y*np.einsum('ab,iba->i',inverse,hi).real/(8*np.pi*np.pi)
            H-=weight*(y*y*np.einsum('ab,ijba->ij',inverse,hij).real-y**4/z*np.einsum('iab,jba->ij',t,t).real)/(8*np.pi*np.pi)
    return grad,(H+H.T)/2


def joint_flavor_vacuum(Y1,Y2):
    eta=1e-5;epsilon=.01;U=np.eye(5)[:,2:]
    Ys=[eta*U@Y1@U.T,eta*U@(Y1+epsilon*Y2)@U.T]
    # At the reference ray the constant light block and heavy block separate.
    # Hence its radial derivative is precisely the two-Dirac heavy inventory.
    r=brentq(lambda r:2*radial_derivatives(r)[0]-2*(r-1),1.,2.,xtol=1e-14)
    x=np.zeros(8);x[0]=np.sqrt(r)
    g,H=joint_flavor_hessian(x,Ys,64);gg,HH=joint_flavor_hessian(x,Ys,128)
    err=float(np.linalg.norm(H-HH,ord=2));eigen=np.linalg.eigvalsh(HH)
    assert np.linalg.norm(gg)<1e-11 and err<1e-10
    assert abs(eigen[0])<1e-11 and min(eigen[1:])>2e-4
    return dict(status='PASS',eta=eta,epsilon=epsilon,y=.2,kappa=2.5e-5,
                squared_radius=r,gradient_norm=float(np.linalg.norm(gg)),
                Hessian=eigen.tolist(),quadrature_operator_norm_error=err,
                light_up=np.linalg.svd(eta*Y1,compute_uv=False).tolist(),
                light_down=np.linalg.svd(eta*(Y1+epsilon*Y2),compute_uv=False).tolist(),
                scope='One supplied scalar action with BOTH five-state Dirac operators and fixed symmetric family spurions. The reference-ray saddle has nonzero exact CP, full-rank light masses and seven positive local normal curvatures. Other40-ray degeneracy and the bare global theorem are not inherited. Flavon dynamics, scalar/gauge loops and physical parameter matching remain open.')


def wilson_hamiltonian(theta=2*np.pi/3):
    W=np.diag(np.exp(1j*np.array([theta,-theta])))
    H=2*np.eye(6,dtype=complex)
    for a,b in [(0,1),(1,2)]:H[2*a:2*a+2,2*b:2*b+2]=-np.eye(2);H[2*b:2*b+2,2*a:2*a+2]=-np.eye(2)
    H[4:6,0:2]=-W;H[0:2,4:6]=-W.conj().T
    return W,H


def holonomy_sector():
    W,H=wilson_hamiltonian()
    expected=sorted(2*(1-np.cos((2*np.pi*k+sg*2*np.pi/3)/3)) for k in range(3) for sg in [-1,1])
    assert np.allclose(np.linalg.eigvalsh(H),expected)
    assert expected[0]>0
    return dict(status='PASS', physical_register_spectrum=expected,
                exact_gap='2(1-cos(2pi/9)) times the supplied hopping coefficient',
                Wilson_eigenphases=['2pi/3','-2pi/3'],
                scope='A nonflat connection on the two declared free physical polarizations, extended by identity on the four gauge directions. It commutes with their projector constraints and the polarization-independent tree Hamiltonian. This added holonomy cannot be removed by branch frames; it is not an Einstein interaction, a native prediction of its phase or a physical graviton mass.',
                prior_owners=['analysis/PASS11636_11640_OPERATORS_SELECTORS_AND_TRANSITIONS.md'])


def band_line():
    A=s.Matrix([1,2,3,4]); B=s.Matrix([4,-3,2,-1]); z=s.Symbol('z')
    _,_,K=N.cubic_normal_map(); F=N.pfaffian_vector(K)
    pol=[s.Poly(s.expand(v.subs(dict(zip(N.FVAR,A+z*B)),simultaneous=True)),z) for v in F]
    common=pol[0]
    for p in pol[1:]:common=s.gcd(common,p)
    assert common.degree()==0
    at_infinity=F.subs(dict(zip(N.FVAR,B)),simultaneous=True)
    assert any(at_infinity)
    return A,B,pol


def berry_charge(n_theta=64,n_phi=128):
    A=np.array([1,2,3,4]);B=np.array([4,-3,2,-1])
    weights=np.array([1,*([np.sqrt(2)]*4)])
    vectors=[]
    for theta in np.linspace(0,np.pi,n_theta+1):
        row=[]
        for phi in np.linspace(0,2*np.pi,n_phi,endpoint=False):
            f=np.cos(theta/2)*A+np.sin(theta/2)*np.exp(1j*phi)*B
            v=weights*N.quartic(f);row.append(v/np.linalg.norm(v))
        vectors.append(row)
    vectors=np.array(vectors);total=0.;minimum=1.
    def tri(a,b,c):
        nonlocal minimum
        ab,bc,ca=np.vdot(a,b),np.vdot(b,c),np.vdot(c,a)
        minimum=min(minimum,abs(ab),abs(bc),abs(ca))
        return np.angle(ab*bc*ca)
    for i in range(n_theta):
        for j in range(n_phi):
            k=(j+1)%n_phi
            a,b,c,d=vectors[i,j],vectors[i+1,j],vectors[i+1,k],vectors[i,k]
            total+=tri(a,b,c)+tri(a,c,d)
    # A=i<u|du>; this is the Chern class of the eigenspace (tautological
    # line), the negative of the holomorphic map's positive degree.
    return -total/(2*np.pi),minimum


def bundle_sector():
    A,B,pol=band_line(); charge,overlap=berry_charge(128,256)
    assert abs(charge+4)<1e-8 and overlap>.1
    return dict(status='PASS', projective_line_A=list(A),projective_line_B=list(B),
                restricted_Pfaffians=[str(p.as_expr()) for p in pol],common_polynomial_gcd=1,
                no_base_at_infinity=True,pullback_zero_line='O(-4)', exact_first_Chern_class=-4,
                numerical_Berry_charge=charge,minimum_mesh_overlap=overlap,
                exceptional_direction='At f=(1,b,c,d), the kernel Pfaffian has linear part (0,0,-2b,-2c,-2d). The direction [b:c:d] selects one line in the three-dimensional base-ray kernel.',
                scope='The classical Maschke quartic gives the map and exceptional planes. Here its actual normalized mass zero-mode line is audited as a gapped kernel bundle along a named base-free parameter sphere. This parameter-space Chern class is not electric charge, a particle-family count or a spacetime topological phase.',
                primary_sources=['https://arxiv.org/html/2207.04393v1#S3.SS1'])


def main():
    funcs=[kernel_sector,parent_sector,flavor_sector,connection_sector,flux_sector,radial_sector,holonomy_sector,bundle_sector]
    out=dict(status='PASS',reservation='830b1835c',reservation_integration='85ff2435e',
             producer_sha256=digest(__file__),sources={str(p):digest(ROOT/p) for p in [
                'analysis/w33_pass11663_odd_weil_normal_map.py',
                'analysis/w33_pass1068_chevie_g25_g32_matrices.py',
                'analysis/w33_pass11278_symplectic_ring_geometry.py',
                'analysis/w33_pass11279_history_flux_obstruction.py',
                'analysis/w33_pass11636_11640_operator_selector_transitions.py',
                'data/w33_pass11636_e6_cubic_inputs.npz',
                'data/w33_pass11631_11635_physical_interfaces.json']},passes={})
    for number,func in enumerate(funcs,11664):
        out['passes'][str(number)]=func();print(number,'PASS',flush=True)
    OUT.write_text(json.dumps(out,indent=2,default=lambda v:int(v))+'\n')
    return out


if __name__=='__main__':
    main()
