"""Five physical targets and five cross-connections, with explicit boundaries.

Owners: 11600/11602-11606 Hesse/alignment; 11591/11595 tensors/channel;
11289/11301 native Levi graph and pointwise derivative obstruction;
11306 parametrized graph (not gravity); 11274/11546 sequestering;
11608-11614 finite chiral filters/chambers. No classical general theorem is new.
4082 already owns conditional mobile composite hopping and4083 a pair pump;
11543 owns the distinct neutral-pair exchange gate. Here the added scalar16bar
weight proxy has a many-body pair-order/gap theorem and its even-occupation code.
"""
from pathlib import Path
from math import comb
import hashlib
import itertools
import json
import sys

import numpy as np
import sympy as s
from scipy.special import exp1
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from w33_pass11289_cycle_gram_gluing_flux import cycle_basis

RESERVATION = '40c974480'
OUT = ROOT / 'data/w33_pass11615_11619_parent_pairs_constraints.json'


def ph(path):
    p = Path(path)
    raw = (json.dumps(json.loads(p.read_text()), sort_keys=True,
                      separators=(',', ':')).encode() if p.suffix == '.json'
           else p.read_bytes().replace(b'\r\n', b'\n'))
    return hashlib.sha256(raw).hexdigest()


def yukawa(a, b, h):
    return s.Matrix([[a*h[0], b*h[2], b*h[1]],
                     [b*h[2], a*h[1], b*h[0]],
                     [b*h[1], b*h[0], a*h[2]]])


def parent():
    # Exact low-degree lift witness. All fields have canonical dimension one.
    x, y, A, B, C, M = s.symbols('x y A B C M', positive=True)
    f4 = x**4 + 2*s.sqrt(2)*x*y**3
    constraints = s.Matrix([M*A-x*x, M*B-y*y, M*C-y*B])
    lifted = A*A + 2*s.sqrt(2)*x*C
    substitution = {A:x*x/M, B:y*y/M, C:y**3/M**2}
    assert constraints.subs(substitution, simultaneous=True) == s.zeros(3, 1)
    assert s.simplify(lifted.subs(substitution)-f4/M**2) == 0
    assert constraints.jacobian([A, B, C]).det() == M**3
    # Independent residual model illustrating Schur normal stability.
    q, z = s.symbols('q z', real=True)
    V = (z-q*q)**2 + (z-1)**2
    Hess = s.hessian(V, [q,z]).subs({q:1,z:1})
    schur = s.simplify(Hess[0,0]-Hess[0,1]**2/Hess[1,1])
    assert schur == 4 and Hess.det() == 16
    # General equivariant lift: all Sym^d(R^n), d=2..D. This is deliberately
    # expensive, but names every field and preserves orthogonal symmetries.
    auxiliary_u = comb(4+8, 8)-1-4
    auxiliary_hr = comb(12+6, 6)-1-12
    assert (auxiliary_u, auxiliary_hr) == (490,18551)
    # Actual Delta54 family tensors; coefficient field u is a singlet under
    # this subgroup. G6 on u alone is NOT a symmetry of the full interaction.
    u0, u1 = s.symbols('u0 u1')
    mass = s.symbols('mass', positive=True)
    h = s.Matrix(s.symbols('h0:3'))
    a = s.conjugate(u0)/(s.sqrt(3)*mass)
    b = s.conjugate(u1)/(s.sqrt(6)*mass)
    effective = yukawa(a,b,h)
    w = -s.Rational(1,2)+s.I*s.sqrt(3)/2
    X = s.Matrix([[0,0,1],[1,0,0],[0,1,0]])
    Z = s.diag(1,w,w*w)
    R = s.Matrix([[1,0,0],[0,0,1],[0,1,0]])
    for G in [X,Z,R]:
        residual = G.T*yukawa(a,b,G*h)*G-effective
        assert all(s.simplify(t)==0 for t in residual)
    ratio = s.simplify(b/a).subs({u0:s.sqrt(s.Rational(2,3)),u1:-s.I/s.sqrt(3)})
    assert s.simplify(ratio-s.I/2)==0
    return dict(status='PASS',
        scalar_parent='Q1=x; Vchain=sum_d k_d ||M Qd-Sym(Q(d-1) tensor x)||^2; terminal residuals are linear functions of Qd with powers of M restoring dimension two. Every square has polynomial degree at most four.',
        exact_property='Every zero of the original sum of squares has one lifted zero Qd=x^d/M^(d-1), and conversely. The auxiliary Jacobian is block triangular with diagonal M I. Full-rank original residual normals imply positive lifted normals. This is zero-locus/normal matching, not equality of finite-M off-shell effective potentials.',
        H4_lift={'complex_fields':['A','B','C'], 'constraints':[str(t) for t in constraints], 'terminal':str(lifted), 'auxiliary_Jacobian_det':str(M**3)},
        Schur_witness={'full_Hessian':Hess.tolist(),'relaxed_curvature':str(schur),'unrelaxed_curvature':str(Hess[0,0])},
        manifest_real_auxiliary_counts={'Hesse_n4_D8':auxiliary_u,'neutral_flavons_n12_D6':auxiliary_hr,'total':auxiliary_u+auxiliary_hr},
        mediator='Two complex Spin10-vector family-triplets A0,A1: V=sum_j ||M Aj+conjugate(uj) H||^2. Renormalizable Yukawas use the prior diagonal tensor/sqrt3 on A0 and off-diagonal tensor/sqrt6 on A1. Tree substitution gives minus Y(conjugate(u0)/sqrt3M,conjugate(u1)/sqrt6M; an overall real sign is conventional.',
        mediator_real_components=120, b_over_a_at_11606=str(ratio),
        gauge_inventory='Gauge parent here is Spin10 with global realized X,Z,R family symmetry and coefficient CP. Neutral tensor-lift fields are gauge singlets. Add a real adjoint45 for B-L breaking, alongside the prior126 Majorana channel and gauge-invariant alignment projectors. A gauged continuous SU3 parent, common G6 action on all interactions, and selected Spin10-breaking vacuum are not constructed.',
        boundary='All target values, scales, channel coefficients and allowed counterterms are inputs. Power-counting-renormalizable tree parent is not an asymptotically complete UV theory or radiative protection. The conservative full symmetric-tensor lift is very expensive; no optimized equivariant lift is claimed.')


def cutoff_integrals(m2, cutoff=1.):
    if m2 == 0:
        return cutoff**4/2, cutoff**2
    x = m2/cutoff**2
    return (cutoff**4*((1-x)*np.exp(-x)+x*x*exp1(x))/2,
            cutoff**2*(np.exp(-x)-x*exp1(x)))


def mass_inventory(naux=19041):
    # Conditional Spin10->SM retention. Gauge direction and masses are inputs.
    return dict(real_scalars=1155+naux, gauge_vectors=45, Weyl_components=91,
                broken_vectors=33, massless_vectors=12,
                physical_real_scalars=1122+naux, auxiliary_real_scalars=naux)


def thresholds():
    inv = mass_inventory()
    signed0 = inv['real_scalars']-2*91+2*45
    physical0 = inv['physical_real_scalars']+3*33+2*12-2*91
    assert signed0 == physical0 == 20104
    # Matched spectator and Majorana singular values from actual prior maps.
    MR = 3*s.eye(3)+s.ones(3)
    assert MR.eigenvals()=={s.Integer(3):2,s.Integer(6):1}
    spectator = [(s.Integer(1),3),(s.Rational(1,30),6),(s.Rational(1,15),1)]
    sum_spec4 = s.factor(sum(n*x**4 for x,n in spectator))
    assert sum_spec4 == s.Rational(1215011,405000)
    ms, mn, mex, mone, mv, msc = s.symbols('ms mn mex mone mv msc', positive=True)
    str4 = s.factor(inv['physical_real_scalars']*msc**4+99*mv**4
                    -30*2*mex**4-2*3*mone**4
                    -2*(2*(3*mn)**4+(6*mn)**4)-2*sum_spec4*ms**4)
    cr = s.Rational(inv['physical_real_scalars'],6)+s.Rational(91,6)-s.Rational(33,2)-8
    # 33 eaten minimally coupled Goldstones must not also be retained scalars.
    assert cr == s.Rational(inv['real_scalars']+91-4*45,6)
    suppression=[]
    for m2 in [.01,1.,9.,25.]:
        I0,I1=cutoff_integrals(m2)
        assert I0>0 and I1>0
        suppression.append({'m2_over_cutoff2':m2,'I0_over_massless':2*I0,'I1_over_massless':I1})
    assert suppression[-1]['I1_over_massless']<1e-11
    return dict(status='PASS',inventory=inv,C0=signed0,CR_minimal=str(cr),
        physical_partition='1122+Naux real physical scalars;33 massive vectors;12 massless vectors;45 SM Weyls;15 exotic Dirac fermions;3 additional singlet Majoranas;3 right-handed-neutrino Majoranas;10 spectator Majoranas. Added fields over11604: two10-triplet mediators120 real, global-family28 spectator scalar56 real, real Spin10-adjoint45, and Naux. Naux=19041 only in the conservative manifest parent.',
        physical_degree_check=physical0,
        massive_vector='Feynman vector + signed complex ghost + eaten real Goldstone = K1-K0: a0=3,a2/R=-1/2 for minimal gauge-orbit scalar matching. Removing all Goldstones from physical scalar inventory avoids double counting.',
        Majorana_mass_ratios=['3 multiplicity2','6 multiplicity1'],
        spectator_mass_ratios=[{'value':str(x),'multiplicity':n} for x,n in spectator],
        spectator_sum_m4_over_ms4=str(sum_spec4),Str_m4=str(str4),
        vacuum_MS='V1=(sum_s m_s^4(log(m_s^2/mu^2)-3/2)-2sum_W m_W^4(log(m_W^2/mu^2)-3/2)+3sum_massiveV m_V^4(log(m_V^2/mu^2)-5/6))/(64pi^2), in declared MS/Landau convention. mu dV1/dmu=-Str(m^4)/(32pi^2).',
        proper_time='I0=Lambda^4[(1-x)exp(-x)+x^2 E1(x)]/2; I1=Lambda^2[exp(-x)-x E1(x)], x=m^2/Lambda^2. Signed a0/a2 multiply I0/I1. These are cutoff diagnostics, separate from renormalized MS matching.',
        suppression=suppression,
        boundary='Spectrum partition is a retention scenario, not a derived gauge vacuum. Scalar eigenvalues, vector masses, exotic/spectator couplings and counterterms remain matching inputs. Composite pair models cannot reuse elementary126 multiplicities. No physical G or cosmological constant prediction; gauge dependence of local power divergences is retained.')


def gauge_grams():
    # Standard oscillator realization, independent of the stored gamma basis.
    # 16bar singlet |11111>: B-L=-1,T3R=+1/2. Its symmetric square is126bar.
    X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]])
    Z=np.diag([1,-1]);I=np.eye(2);gam=[]
    for j in range(5):
        for sigma in [X,Y]:
            factors=[Z]*j+[sigma]+[I]*(4-j);G=factors[0]
            for F in factors[1:]:G=np.kron(G,F)
            gam.append(G)
    pairs=list(itertools.combinations(range(10),2))
    spin=[gam[i]@gam[j]/2 for i,j in pairs]
    vec=[]
    for i,j in pairs:
        T=np.zeros((10,10));T[i,j]=1;T[j,i]=-1;vec.append(T)
    adjoint=sum(vec[pairs.index((2*j,2*j+1))]*2/3 for j in range(3))
    dA=np.array([T@adjoint-adjoint@T for T in vec])
    GA=np.einsum('aij,bij->ab',dA,dA)/2
    v=np.zeros(32,complex);v[-1]=1;dv=np.array([T@v for T in spin])
    # Full symmetric-tensor inner product, not the factorized16 kinetic term.
    dS=np.array([np.outer(w,v)+np.outer(v,w) for w in dv])
    GS=np.einsum('aij,bij->ab',dS.conj(),dS).real
    rational=lambda A:s.Matrix([[s.Rational(int(round(float(x)*36)),36) for x in row] for row in A])
    A,B=rational(GA),rational(GS)
    assert np.max(abs(np.array(A,float)-GA))<1e-13
    assert np.max(abs(np.array(B,float)-GS))<1e-13
    assert A*B==B*A
    return A,B,spin,pairs


def gauge_threshold():
    A,B,spin,pairs=gauge_grams()
    assert A.rank()==30 and B.rank()==21 and (A+2*B).rank()==33
    av,bv,g=s.symbols('vA2 v1262 g',positive=True)
    mass=A*av+2*B*bv
    predicted=[(4*av/9,12),(16*av/9+2*bv,6),
               (4*av/9+2*bv,12),(2*bv,2),(10*bv,1)]
    # Joint eigenspaces built without symbolic diagonalization of a dense45.
    joint=[(s.Rational(4,9),0,12),(s.Rational(16,9),1,6),
           (s.Rational(4,9),1,12),(0,1,2),(0,5,1),(0,0,12)]
    for a,b,n in joint:
        equations=(A-a*s.eye(45)).col_join(B-b*s.eye(45))
        assert 45-equations.rank()==n
    moment=s.factor(s.trace(mass*mass))
    assert s.expand(moment-(s.Rational(640,27)*av**2+64*av*bv+180*bv**2))==0
    assert s.expand(moment-sum(n*m*m for m,n in predicted))==0
    return dict(status='PASS',
        action='Real45 kinetic1/2||D A||^2 with invariant vector-trace inner product -Tr(Ta Tb)/2=delta_ab; complex126 kinetic||D S||^2 with inherited symmetric-spinor norm. Gauge mass^2=g^2[vA^2 GA+2v126^2 GS].',
        adjoint='A=(2vA/3)(T01+T23+T45), the B-L direction; S=v126 |11111> tensor |11111> is the126bar neutral weight(-6,2,0). No scalar16bar VEV is used in this elementary gauge-threshold model.',
        Gram_adjoint=A.tolist(),Gram_126=B.tolist(),
        ranks={'adjoint':30,'126':21,'combined':33,'massless':12},
        spectrum=[{'mass_squared_over_g2':str(m),'multiplicity':n} for m,n in predicted],
        vector_sum_m4_over_g4=str(moment),
        symmetry='Adjoint45 preserves SU3c x SU2L x SU2R x U1BL; the neutral126bar triplet leaves SU3c x SU2L x U1Y, with12 massless gauge generators. Multiple family126 VEVs aligned in the same gauge direction enter through their summed squared norm v126^2.',
        budget_link='The actual full45 gauge mass matrix replaces the equal-vector-mass retention benchmark in physical threshold sums. Its vector MS running coefficient is -3g^4[640vA^4/27+64vA^2v126^2+180v126^4]/(32pi^2).',
        boundary='This is the standard45+126 breaking interface at supplied VEVs and kinetic normalization. The gauge-variant constituent is a representation coordinate, not a physical16 condensate. No scalar vacuum minimization, scalar mass spectrum, physical scale selection or full UV unification fit is claimed.')


def cycle_derivative(n):
    D=s.zeros(n)
    for i in range(n):
        D[i,(i+1)%n]=s.Rational(1,2)
        D[i,(i-1)%n]=-s.Rational(1,2)
    return D


def local_generators(n):
    D=cycle_derivative(n)
    out=[]
    for i in range(n):
        P=s.zeros(n);P[i,i]=1
        out.append((P*D+D*P)/2)
    return out


def constraints():
    # Exact finite local bracket obstruction, beyond prior pointwise theorem.
    n=5; D=cycle_derivative(n)
    N=s.diag(1,0,0,0,0);M=s.diag(0,1,0,0,0)
    B=M*D.T*N*D-N*D.T*M*D
    assert B+B.T != s.zeros(n)
    A=local_generators(n)
    flat=lambda T:s.Matrix(list(T))
    span=s.Matrix.hstack(*[flat(T) for T in A])
    assert span.rank()==5 and span.row_join(flat(B)).rank()==6
    C=A[0]*A[1]-A[1]*A[0]
    assert span.row_join(flat(C)).rank()==6
    counts=[]
    for size in [3,5,9]:
        # Edge coefficients (N_i+N_j)/4 form an invertible map on odd cycles.
        edge_map=s.zeros(size)
        for i in range(size):edge_map[i,i]=1;edge_map[i,(i+1)%size]=1
        assert abs(edge_map.det())==2
        counts.append({'sites':size,'local_generator_dimension':size,
                       'minimal_Lie_completion_dimension':size*(size-1)//2,
                       'all_pair_generators':True})
    q=s.Matrix(s.symbols('q0:5'));p=s.Matrix(s.symbols('p0:5'))
    f=(p.T*A[0]*q)[0];g=(p.T*A[1]*q)[0]
    PB=sum(s.diff(f,q[i])*s.diff(g,p[i])-s.diff(f,p[i])*s.diff(g,q[i]) for i in range(5))
    assert s.expand(PB-(p.T*C*q)[0])==0
    # Inner matrix derivations provide an exact Leibniz alternative, but
    # enlarge the algebra and do not become GR by being closed.
    X=s.Matrix([[1,2],[0,3]]);Y=s.Matrix([[0,1],[4,2]]);P=s.diag(1,-1)
    deriv=lambda Z:P*Z-Z*P
    assert deriv(X*Y)==deriv(X)*Y+X*deriv(Y)
    return dict(status='PASS',
        declared_action='S=sum_i p_i dot(q_i)-H[N]-G[v], H[N]=p^T diag(N)p/2+q^T D^T diag(N)Dq/2; G[v]=p^T{diag(v),D}q/2 on a supplied periodic cycle.',
        HH_bracket_matrix=B.tolist(),HH_symmetric_defect=(B+B.T).tolist(),
        HH_span_ranks=[5,6],GG_span_ranks=[5,6],GG_commutator=C.tolist(),
        Lie_completion=counts,
        completion_proof='On an odd cycle the map v->edge coefficients v_i+v_(i+1) is invertible (absolute determinant2). Hence local generators span each nearest edge rotation Eij-Eji. Commutators along connected paths generate every pair rotation, giving so(N). Canonical moment maps p^T A q close exactly with matrix commutators.',
        native_tower='The 3 and9 cycle sizes are native3-power refinement controls. so(3) happens to close at3 because all pairs are neighbors; at9 closure needs36 generators and distant pairs. Closure at the smallest rung alone is misleading.',
        matrix_escape='Finite matrix observables admit nonzero inner derivations [P,.] satisfying exact Leibniz. This changes the observable algebra; it does not preserve the old pointwise spatial field interpretation.',
        boundary='Neither this supplied scalar cycle action nor its all-pair so(N) moment-map completion is Einstein gravity. Completion destroys the site-local diffeomorphism ansatz; HH is not recovered as the desired GG generator. Prior11301 and11306 remain valid. Full local Hamiltonian/hypersurface algebra for a W33 gravitational action remains open.')


def pair_local():
    a=np.array([[0,1,0],[0,0,np.sqrt(2)],[0,0,0]],complex)
    parity=np.diag([1,-1,1]).astype(complex)
    one=np.diag([0,1,0]).astype(complex)
    v=np.zeros(9,complex);v[2]=1/np.sqrt(2);v[6]=-1/np.sqrt(2)
    return a,parity,one,np.outer(v,v.conj())


def embed(op, sites, n):
    # Arbitrary one/two-site operator, direct index construction for tiny tests.
    dim=3**n;out=np.zeros((dim,dim),complex)
    for col,digits in enumerate(itertools.product(range(3),repeat=n)):
        subcol=np.ravel_multi_index(tuple(digits[i] for i in sites),(3,)*len(sites))
        for subrow in range(3**len(sites)):
            coefficient=op[subrow,subcol]
            if coefficient==0:continue
            changed=list(digits)
            for i,d in zip(sites,np.unravel_index(subrow,(3,)*len(sites))):changed[i]=d
            out[np.ravel_multi_index(tuple(changed),(3,)*n),col]+=coefficient
    return out


def pair_hamiltonian(n, edges, delta=2., coupling=1.):
    a,P,Q,h=pair_local();H=np.zeros((3**n,3**n),complex)
    for i in range(n):H+=delta*embed(Q,[i],n)
    for i,j in edges:H+=coupling*embed(h,[i,j],n)
    return H


def dicke(n,k):
    psi=np.zeros(3**n,complex)
    for sites in itertools.combinations(range(n),k):
        digits=[0]*n
        for i in sites:digits[i]=2
        psi[np.ravel_multi_index(tuple(digits),(3,)*n)]=1/np.sqrt(comb(n,k))
    return psi


def pair_phase():
    incidence, cycles=cycle_basis()
    edges=[tuple(int(i) for i in np.where(incidence[:,j])[0]) for j in range(160)]
    adj=[set() for _ in range(80)]
    for i,j in edges:adj[i].add(j);adj[j].add(i)
    seen={0};todo=[0]
    for i in todo:
        for j in adj[i]-seen:seen.add(j);todo.append(j)
    assert len(seen)==80
    n=4;ring=[(i,(i+1)%n) for i in range(n)];H=pair_hamiltonian(n,ring)
    ev=np.linalg.eigvalsh(H);assert (abs(ev)<1e-10).sum()==n+1
    a,P,Q,h=pair_local();psi=dicke(n,2)
    assert np.linalg.norm(H@psi)<1e-13
    pair=embed(a@a,[0],n)
    corr=np.vdot(psi,pair.conj().T@embed(a@a,[2],n)@psi)
    atom=np.vdot(psi,embed(a,[0],n).conj().T@embed(a,[2],n)@psi)
    assert abs(corr-s.Rational(2,3))<1e-13 and abs(atom)<1e-13
    odd_indices=[i for i,d in enumerate(itertools.product(range(3),repeat=n)) if sum(d)%2]
    odd_gap=float(np.linalg.eigvalsh(H[np.ix_(odd_indices,odd_indices)]).min())
    assert abs(odd_gap-2)<1e-12
    # Number-fixed even states and symmetry-breaking product representatives
    # coexist within the exact ground multiplet, without an odd atomic VEV.
    local=np.array([1,0,1j],complex)/np.sqrt(2)
    product=local
    for _ in range(n-1):product=np.kron(product,local)
    assert np.linalg.norm(H@product)<1e-13
    assert abs(np.vdot(local,a@local))<1e-14
    pair_vev=np.vdot(local,(a@a)@local)
    assert abs(pair_vev-1j/np.sqrt(2))<1e-14
    N,k=80,40;off=s.Rational(2*k*(N-k),N*(N-1));largest=s.Rational(2*k*(N-k+1),N)
    assert (off,largest)==(s.Rational(40,79),41)
    return dict(status='PASS',native_graph={'vertices':80,'edges':160,'connected':True},
        Hamiltonian='Delta sum_i |1><1|_i + J sum_edges |v><v|_ij, v=(|0,2>-|2,0>)/sqrt2; onsite Hilbert {0,1,2}, Delta,J>0.',
        ground_theorem='On every connected graph, the exact zero-energy space is the symmetric even {0,2} tensor sector, dimension N+1. At fixed pair number k its unique state is the normalized Dicke superposition. Each odd site costs at least Delta since all edge terms are positive; one odd site with all others empty saturates Delta.',
        prior_pair_owner='4082 mobile contact-dark photon composites and4083 pair pump;11539/11543 neutral antisymmetric81-pair code. Those remain distinct carriers and do not already prove this scalar16bar-weight proxy phase.',
        number_fixed='At fixed k: <a_i>=<a_i^2>=0, <a_i^dagger a_j>=0 for i!=j, <(a_i^2)^dagger a_j^2>=2k(N-k)/(N(N-1)). The pair density matrix has largest eigenvalue 2k(N-k+1)/N, extensive at fixed nonzero density.',
        W33_half_filling={'pair_off_diagonal':str(off),'pair_largest_eigenvalue':str(largest),'atomic_largest_eigenvalue':1},
        broken_U1_representative='Product over sites of (sqrt(1-rho)|0>+exp(i theta)sqrt(rho)|2>) is an exact ground state: <a>=0, <a^2>=sqrt(2rho(1-rho))exp(i theta). Matter parity remains unbroken.',
        finite_control={'sites':n,'zero_modes':n+1,'odd_gap':odd_gap,'off_diagonal_pair':float(corr.real),'atomic_off_diagonal':float(atom.real)},
        composite_channel='Choose the scalar16bar neutral constituent weight(-3,1,0) from11595/11606. Its square has(-6,2,0); the10 symmetric channel has no such weight, so the singlet pair is in the126bar channel. This weight interface does not define the complete Spin10-covariant Hamiltonian.',
        boundary='Added constrained-boson parent on the actual graph, not a derived relativistic W33 action or full gauged Spin10 Higgs phase. Pair-superfluid mechanism and ferromagnetic/Dicke facts are established physics. Local parity conservation and enlarged pseudospin degeneracy are special to this parent; robustness to atomic hopping is not asserted. Absolute energy can be shifted freely, so zero parent energy does not solve the cosmological constant.')


def pair_holonomy():
    incidence, cycles=cycle_basis();c=cycles[:,0]
    marked=int(np.where(c!=0)[0][0]);length=int(np.count_nonzero(c))
    phase=np.zeros(160);phase[marked]=np.pi
    atomic=np.exp(1j*(c@phase));paired=np.exp(2j*(c@phase))
    assert abs(atomic+1)<1e-14 and abs(paired-1)<1e-14
    return dict(status='PASS',fundamental_cycle_length=length,marked_edge=marked,
        atomic_holonomy=-1,pair_holonomy=1,
        map='Dress pair hopping by U_ij^2 for charge-one constituents. A pi holonomy is visible to atoms while every pair link remains trivial in this witness. The positive pair parent stays frustration free; gauge-invariant pair correlations require Wilson-line dressing.',
        boundary='A kinematic residual-Z2 flux witness on native incidence, not dynamical confinement/deconfinement, a gauged Higgs phase, full Spin10 global topology or an anomaly proof. The U1 normalization here is constituent charge one.')


def pair_control():
    a,P,Q,_=pair_local();b=a@a/np.sqrt(2)
    P0=np.diag([1,0,0]);P2=np.diag([0,0,1])
    axes=[b+b.conj().T,-1j*(b-b.conj().T),P0-P2]
    indices=[0,2]
    for T in axes:
        assert np.max(abs(T@P-P@T))<1e-14
        assert np.max(abs(T@T-(P0+P2)))<1e-14
    H=np.kron(b.conj().T,b)+np.kron(b,b.conj().T)
    U=expm(-1j*np.pi*H/4);code=[0,2,6,8]
    reduced=U[np.ix_(code,code)]
    expected=np.eye(4,dtype=complex)
    expected[1:3,1:3]=np.array([[1,-1j],[-1j,1]])/np.sqrt(2)
    assert np.max(abs(reduced-expected))<1e-14
    assert np.max(abs(U[np.ix_([1,3,4,5,7],code)]))<1e-14
    assert np.linalg.matrix_rank(reduced[:,1].reshape(2,2),tol=1e-12)==2
    # Finite perturbation witness, with honest nonuniform operator bound.
    n=4;edges=[(i,(i+1)%n) for i in range(n)]
    H0=pair_hamiltonian(n,edges);V=np.zeros_like(H0)
    for i,j in edges:
        hop=embed(a.conj().T,[i],n)@embed(a,[j],n)
        V-=hop+hop.conj().T
    labels=list(itertools.product(range(3),repeat=n))
    even=[i for i,d in enumerate(labels) if sum(d)%2==0]
    odd=[i for i,d in enumerate(labels) if sum(d)%2]
    rows=[]
    for strength in [0.,.025,.05,.1]:
        Ht=H0+strength*V
        vals,vec=np.linalg.eigh(Ht[np.ix_(even,even)])
        odd_energy=np.linalg.eigvalsh(Ht[np.ix_(odd,odd)]).min()
        assert odd_energy-vals[0] >= 2-4*len(edges)*strength-1e-12
        state=np.zeros(3**n,complex);state[even]=vec[:,0]
        atom=embed(a,[0],n);other=embed(a,[2],n)
        rows.append({'atomic_hopping':strength,'odd_gap':float(odd_energy-vals[0]),
                     'pair_correlation':float(np.vdot(state,atom.conj().T@atom.conj().T@other@other@state).real),
                     'atomic_correlation':float(np.vdot(state,atom.conj().T@other@state).real),
                     'finite_norm_gap_bound':2-4*len(edges)*strength})
    return dict(status='PASS',axes='X=b+bdag,Y=-i(b-bdag),Z=P0-P2, b=a^2/sqrt2; each is an exact Pauli on {|0>,|2>} and commutes with matter parity.',
        entangler='H=J(b_i^dag b_j+b_j^dag b_i); t=pi/(4J). Exact sqrt(iSWAP)-type entangler with zero odd-sector leakage; together with supplied single-pair Pauli controls it is a conditional universal encoded gate set.',
        gate_error=float(np.max(abs(reduced-expected))),entangled_Schmidt_rank=2,
        gauge_boundary='Onsite X/Y require a charge-two phase reference or a gauge-covariant pair-condensate coupling. These actuators and a fault-tolerant error model are not derived. The2^N even code is larger than the N+1 ground multiplet; the stated gate assumes addressed controls with pair-aligning drift switched off or compensated. Pure gauge charge-conserving exchange alone does not supply all local Pauli controls.',
        perturbation_rows=rows,
        perturbation_boundary='Atomic hopping preserves total matter parity but breaks local parity. Exact ODLRO proof is for zero hopping. Four-site tests show a surviving odd gap; the norm bound Delta-4|E|t is finite-volume and not uniform in graph size, so no stable thermodynamic phase theorem follows.')


def loop_orientation():
    x=s.symbols('x0:4',real=True);u0=x[0]+s.I*x[1];u1=x[2]+s.I*x[3]
    Y=yukawa(s.conjugate(u0)/s.sqrt(3),s.conjugate(u1)/s.sqrt(6),[1,2,3])
    K=Y.H*Y;tr1=s.expand(s.trace(K));tr2=s.factor(s.expand(s.trace(K*K)))
    assert s.simplify(tr1-s.Rational(14,3)*sum(v*v for v in x))==0
    cp={x[1]:-x[1],x[3]:-x[3]}
    assert s.expand(tr2.subs(cp,simultaneous=True)-tr2)==0
    RF=s.Matrix([[1,s.sqrt(2)],[s.sqrt(2),-1]])/s.sqrt(3)
    z=RF*s.Matrix([u0,u1]);sub={x[0]:s.re(z[0]),x[1]:s.im(z[0]),x[2]:s.re(z[1]),x[3]:s.im(z[1])}
    defect=s.factor(s.expand(tr2.subs(sub,simultaneous=True)-tr2))
    assert defect!=0
    vals={x[0]:1,x[1]:0,x[2]:0,x[3]:0};control=s.simplify(defect.subs(vals));assert control!=0
    return dict(status='PASS',Tr_YdagY=str(tr1),Tr_YdagY_squared=str(tr2),
        fixed_alignment_F_defect=str(defect),defect_at_u_1_0=str(control),
        CP='Both CP-conjugate branches have identical singular spectra for real h and real parent couplings, so their one-loop vacuum thresholds are equal.',
        interpretation='At fixed unequal h=(1,2,3), the first quadratic mass trace is radial, but the quartic trace is not invariant under G6 acting on u alone. It is an allowed lower-degree angular counterterm in the realized Delta54/CP parent. The fully coupled parent must transform all backgrounds or supply further protection.',
        boundary='A polynomial divergence/selection audit, not a full radiative stationary vacuum or a claimed universal sign relation. No standalone Hesse symmetry protection is inferred for the common parent.')


def vacuum_response():
    # Prior sequestering cancels constants, not a field-dependent potential.
    f=s.Rational(1,3);C1,C2,c=s.symbols('C1 C2 c',real=True)
    mean=f*C1+(1-f)*C2
    residual=s.Matrix([C1-mean,C2-mean])
    assert f*residual[0]+(1-f)*residual[1]==0
    assert residual.subs({C1:C1+c,C2:C2+c},simultaneous=True)==residual
    a,b=s.symbols('a b',real=True)
    Y1=yukawa(a,b,[1,2,3]);Y2=yukawa(a,b,[1,1,1])
    str_difference=s.factor(s.trace((Y1.T*Y1)**2)-s.trace((Y2.T*Y2)**2))
    assert str_difference!=0
    # A genuinely field-dependent threshold mass retains force after adding
    # a constant gravitational shift counterterm.
    q=s.symbols('q',positive=True);m=s.symbols('m',positive=True)
    T=(m*m+q*q)**2*(s.log(m*m+q*q)-s.Rational(3,2))
    force=s.factor(s.diff(T,q));assert force!=0
    return dict(status='PASS',prior='11274/11284/11289 local/global four-form sequestering and11546 fixed-data shift criterion are reused, not new.',
        two_domain_residual=[str(v) for v in residual],common_shift_invariant=True,
        flavor_trace_difference=str(str_difference),threshold_force=str(force),
        quantum_running='In MS, mu dV1/dmu=-Str(m^4)/(32pi^2). A global constant shift is removed by the prior constrained gravitational source. Unequal field-dependent thresholds leave source differences and local scalar forces; running local couplings/counterterms must cancel their scale dependence separately.',
        CP_domain='CP-conjugate vacua with equal spectra have equal homogeneous loop vacuum energy. This protects degeneracy, not its absolute value. Wall gradients, tensions and non-CP-related domains remain nonconstant sources.',
        pair_parent='Adding c I to the pair Hamiltonian leaves parity, eigenvectors, atomic gap and ODLRO unchanged. Hence its engineered zero ground energy cannot determine gravitational vacuum energy.',
        boundary='No native four-form/gravity dynamics or graviton-loop completion is derived. Linear fixed-data sequestering is prior; general graviton-loop extensions exist in literature. Residual flux/counterterm, observed CC and full quantum constraint measure remain open.')


def produce():
    data={'status':'PASS','passes':list(range(11615,11620)),'reservation':RESERVATION}
    for name,fn in [('parent',parent),('thresholds',thresholds),('constraints',constraints),
                    ('pair_phase',pair_phase),('vacuum_response',vacuum_response),
                    ('additional_pair_holonomy',pair_holonomy),('additional_loop_orientation',loop_orientation),
                    ('additional_pair_control',pair_control),('additional_gauge_threshold',gauge_threshold)]:
        data[name]=fn();print(name,'PASS',flush=True)
    data['additional_parent_budget']={
        'status':'PASS','real_auxiliaries':19041,'real_scalars_total':20196,
        'C0':20104,'statement':'Constructing an explicit equivariant renormalizable scalar parent and an adjoint45 SM-breaking interface increases the quantum inventory. The large conservative lift cannot be called economical or vacuum-energy cancelling.'}
    sources=['analysis/w33_pass11600_dynamical_hesse_flavor.py',
             'data/w33_pass11602_11606_geometry_flavor_completion.json',
             'data/PART_W33_PASS11595_NEUTRINO_MAJORANA_CHANNEL.json',
             'analysis/w33_pass11289_cycle_gram_gluing_flux.py',
             'data/w33_pass11301_graph_adm_regulator.json',
             'analysis/PASS11542_11546_FIVE_DYNAMICAL_TARGETS.md',
             'data/PART_W33_PASS11608_11613_CHIRAL_UNIFICATION.json',
             'data/PART_W33_PASS11614_HESSE_COXETER_DISCRIMINANT.json']
    data['source_sha256']={p:ph(ROOT/p) for p in sources}
    data['producer_sha256']=ph(Path(__file__))
    OUT.write_text(json.dumps(data,indent=2,default=str)+'\n')
    return data


if __name__=='__main__':produce()
