"""Five explicit continuations of the native W33 period/code program.

Standard magic, Weil quantization, E6 cubics and periodic homogenization are
used with named maps. No fundamental action or physical constants derived.
"""
from pathlib import Path
from itertools import product, combinations
from collections import Counter
from functools import lru_cache
import json, hashlib, sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import numpy as np
import sympy as s
try:
    import w33_pass12188_native_period_symplectic_repair as native
    import w33_20261022_five_toe_frontiers as code
except ModuleNotFoundError:
    from analysis import w33_pass12188_native_period_symplectic_repair as native
    from analysis import w33_20261022_five_toe_frontiers as code
ROOT=Path(__file__).resolve().parents[1]
OMEGA=(-1+s.sqrt(3)*s.I)/2


def matrix_list(M):
    return [[int(x) for x in row]for row in M.tolist()]


def phase_sum(counts):
    """Exact cyclotomic polynomial modulo Phi_9, divided by 59049."""
    z=s.Symbol('z')
    return s.rem(sum(int(n)*z**i for i,n in enumerate(counts)),z**6+z**3+1,z)/59049


@lru_cache(None)
def heralded_magic():
    _,B,C=code.point_geometry()
    u=np.zeros(40,dtype=int);u[:4]=1
    assert np.all(B@u%3==0) and code.rank(np.vstack((C,u)),3)==11
    coeff=np.array(list(product(range(3),repeat=10)),dtype=int)
    words=coeff@C%3
    counts=[];k=[];noise=[]
    z=np.exp(2j*np.pi/9)
    for t in range(3):
        w=(words+t*u)%3;phase=w.sum(1)%9
        hist=np.bincount(phase,minlength=9);counts.append(hist.tolist())
        k.append(sum(hist[i]*z**i for i in range(9))/len(words))
    assert counts==[[59049,0,0,0,0,0,0,0,0],
                    [0,26244,0,0,19683,0,0,13122,0],
                    [0,0,26244,0,0,13122,0,0,19683]]
    zsym=s.Symbol('z')
    exact=[phase_sum(h)for h in counts]
    def norm9(f):
        conjugate=sum(f.expand().coeff(zsym,i)*zsym**((-i)%9)for i in range(6))
        return s.rem(s.expand(f*conjugate),zsym**6+zsym**3+1,zsym)
    assert [norm9(f)for f in exact]==[s.Integer(1),s.Rational(1,27),s.Rational(1,27)]
    k=np.array(k);norm=float(np.vdot(k,k).real)
    assert np.allclose(abs(k)**2,[1,1/27,1/27],atol=1e-14)
    assert abs(norm/3-29/81)<1e-14
    psi=k/np.sqrt(norm)
    wigner=[]
    for q,p in product(range(3),repeat=2):
        value=sum(z**(3*p*y)*psi[(q+2*y)%3]*psi[(q-2*y)%3].conjugate() for y in range(3))/3
        assert abs(value.imag)<1e-14
        wigner.append(float(value.real))
    assert min(wigner)<-.02 and abs(sum(wigner)-1)<1e-13
    # A single physical Z is applied AFTER the resource gate, BEFORE selection.
    # Distance alone does not justify a higher-order accepted-error claim.
    for site in range(40):
        hist=[];amp=[]
        for t in range(3):
            w=(words+t*u)%3
            h=np.bincount((w.sum(1)+3*w[:,site])%9,minlength=9)
            hist.append(h.tolist());amp.append(sum(h[i]*z**i for i in range(9))/len(words))
        noise.append({'site':site,'phase_counts':hist,
                      'success':float(np.vdot(amp,amp).real/3),
                      'fidelity_to_ideal':float(abs(np.vdot(psi,amp))**2/np.vdot(amp,amp).real) if np.vdot(amp,amp).real>1e-20 else None})
    assert any(r['success']>1e-10 and r['fidelity_to_ideal']<.99 for r in noise)
    return {'pass':12189,'status':'EXACT_FULL_RANK_HERALDED_MAGIC_WITH_SUPPLIED_NONCLIFFORD',
        'input':'(|C>+|u+C>+|2u+C>)/sqrt(3), an encoded stabilizer state',
        'u_support':[0,1,2,3],'codewords_per_coset':len(words),
        'physical_resource':'diag(1,zeta9,zeta9^2) on all 40 physical qutrits',
        'accepted_instrument':'project onto the CSS codespace, trivial syndrome only',
        'phase_counts_mod9':counts,'exact_kraus_entries':[str(phase_sum(h))for h in counts],
        'kraus_rank_on_declared_logical_qutrit':3,
        'squared_amplitudes_before_normalization':['1','1/27','1/27'],
        'ideal_success_probability':'29/81','normalized_probabilities':['27/29','1/29','1/29'],
        'pure_magic_proof':'A pure one-qutrit stabilizer has support 1, or support 3 with equal magnitudes. These three nonzero magnitudes are unequal.',
        'wigner_q_then_p':wigner,'single_Z_after_gate_controls':noise,
        'scope':'Resource conversion, not Clifford-only magic creation, a deterministic logical unitary, distillation, or a fault-tolerance threshold. Native physical gate and syndrome extraction remain supplied.',
        'prior':['2026-10-22_five_toe_frontiers.md','2026-10-22_allfive_deeper_frontiers.md','2026-10-22_five_frontiers_round4.md','2026-10-22_five_frontiers_round6.md',
                 'https://arxiv.org/abs/quant-ph/0602001','https://arxiv.org/abs/2109.13481']}


@lru_cache(None)
def discriminant_weil():
    _,R=native.native();F=native.alternating([-3,-1,-2,2,1,0]);Fi=F.inv()
    u=s.Matrix([1,0,0,0]);v=s.Matrix([0,0,2,0]);classes=[(a,b,a*u+b*v)for a,b in product(range(3),repeat=2)]
    actions={};records=[]
    for g,M in R.items():
        columns=[]
        for x in (u,v):
            y=M.inv().T*x
            columns.append(s.Matrix(next((a,b)for a,b,z in classes if all(t.q==1 for t in Fi*(y-z)))))
        A=s.Matrix.hstack(*columns);actions[g]=A
        assert A==s.Matrix([[1,0],[2*(g[0]+g[1])%3,1]])
        records.append({'h':list(g),'matrix2_mod3':matrix_list(A),'Weil_diagonal_exponents':[0,2*(g[0]+g[1])%3,2*(g[0]+g[1])%3]})
    H=list(R)
    for g,h in product(H,repeat=2):
        assert (actions[g]*actions[h]-actions[native.mul(g,h)]).applyfunc(lambda z:z%3)==s.zeros(2)
    # Exact exponent arithmetic for U_g D(a,b) U_g^-1 = D(A_g(a,b)).
    # D(a,b)|t> = omega^(ab-bt)|t+a>.
    for g in H:
        k=2*(g[0]+g[1])%3
        for a,b,t in product(range(3),repeat=3):
            A,B=map(int,actions[g]*s.Matrix([a,b]));A%=3;B%=3
            lhs=k*((t+a)**2-t*t)+a*b-b*t
            assert (lhs-(A*B-B*t))%3==0
    return {'pass':12190,'status':'EXACT_NATIVE_DISCRIMINANT_ACTION_AND_LINEAR_WEIL_LIFT',
        'discriminant_generators':[[1,0,0,0],[0,0,2,0]],'pairing':'u^T F^-1 v = 1/3 mod Z',
        'correct_action':'[x] -> [R_g^-T x] on coker(F), not R_g x',
        'image_order':len({tuple(A)for A in actions.values()}),
        'kernel':[list(g)for g,A in actions.items()if A==s.eye(2)],
        'actions':records,'symmetrized_Weyl':'D(a,b)=omega^(ab) X^a Z^(-b)',
        'intertwiner':'U_g|t>=omega^(2*(g.a+g.b)*t^2)|t>',
        'covariance_cases':27*9*3,'group_products_checked':729,
        'central_distinction':'The native address center is trivial in this Weil lift. It remains nontrivial in the separate Schrödinger W(a,b,c) representation; the representations are not identified.',
        'normalization':'The discriminant pairing fixes a dimensionless third-root commutator after choosing a central character. No map to physical area/action units is supplied, so hbar is not determined.',
        'prior':['PASS12188_NATIVE_PERIOD_SYMPLECTIC_REPAIR.md','https://arxiv.org/abs/0705.4556']}


def native_normalizers():
    _,R,S,T=native.repaired()
    P=s.Matrix([[-1,0,-1,1],[-1,1,-1,0],[0,0,1,-2],[0,0,1,1]])
    J=s.Matrix([[0,-1],[1,-1]]);C=s.Matrix([[1,-1],[0,-1]])
    D12=[sig*J**k*C**e for sig,k,e in product((1,-1),range(3),range(2))]
    flip=s.zeros(4);flip[:2,2:]=s.eye(2);flip[2:,:2]=s.eye(2)
    assert P.det()==-3 and (S.inv()*P).det()==-1
    assert {tuple(P.inv()*M*P)for M in R.values()}=={tuple(s.diag(J**a,J**b))for a,b in product(range(3),repeat=2)}
    out=[]
    for Q in (s.eye(4),S):
        mats=[]
        for U,V,e in product(D12,D12,range(2)):
            M=Q.inv()*P*s.diag(U,V)*flip**e*P.inv()*Q
            if all(x.q==1 for x in M):mats.append(M)
        group=R if Q==s.eye(4)else T
        group_keys={tuple(M)for M in group.values()}
        assert all(tuple(M*A*M.inv())in group_keys for M in mats for A in set_matrices(group.values()))
        assert len({tuple(M)for M in mats})==len(mats)
        out.append(mats)
    assert [len(x)for x in out]==[144,288]
    return P,S,out


def set_matrices(mats):
    return [s.Matrix(4,4,list(k))for k in {tuple(M)for M in mats}]


def projective_key(F,p):
    values=[int(x)%p for x in F];unit=next(x for x in values if x)
    return tuple(x*pow(unit,-1,p)%p for x in values)


@lru_cache(None)
def normalizer_actions():
    P,S,groups=native_normalizers()
    d=json.loads((ROOT/'data/w33_pass12186_context_cover_holonomy.json').read_text())
    planes=[tuple(K)for K in d['binary_quadric']['maximal_singular_planes']]
    vec=np.array(list(product(range(2),repeat=4)),dtype=int);vidx={tuple(v):i for i,v in enumerate(vec)}
    forms=[native.alternating([1,1,c,1,1+c,b])for b in (0,2)for c in range(3)]
    fidx={projective_key(F,3):i for i,F in enumerate(forms)};records=[]
    for number,mats in enumerate(groups):
        repaired=[S.inv()*M*S for M in mats]if number==0 else mats
        binary=[];ternary=[]
        for M,N in zip(mats,repaired):
            mat=np.array(M,dtype=int)%2
            perm=[]
            for K in planes:
                key=tuple(sorted(vidx[tuple(mat@vec[i]%2)]for i in K));perm.append(planes.index(key))
            binary.append(perm)
            ternary.append([fidx[projective_key(N.T*F*N,3)]for F in forms])
        bo=[sorted({p[i]for p in binary})for i in range(6)]
        to=[sorted({p[i]for p in ternary})for i in range(6)]
        assert all(len(x)==6 for x in bo)
        assert sorted({tuple(x)for x in to})==[(0,3),(1,2,4,5)]
        records.append({'lattice':'original Z4'if number==0 else'repaired Lminus',
                        'order':len(mats),'binary_matrix_image_order':len({tuple(int(x)%2 for x in M)for M in mats}),
                        'binary_kernel_orbits':[list(x)for x in sorted({tuple(x)for x in bo})],
                        'ternary_polarity_orbits':[list(x)for x in sorted({tuple(x)for x in to})],
                        'matrices':[matrix_list(M)for M in mats],
                        'binary_permutations':binary,'ternary_permutations':ternary})
    return {'pass':12193,'status':'EXACT_FULL_INTEGRAL_NORMALIZERS_AND_BOTH_ACTIONS',
        'Eisenstein_plane_basis':matrix_list(P),'original_index':3,'repaired_basis_determinant':-1,
        'groups':records,'complete_proof':'The rational C3xC3 module has exactly two irreducible character planes. Every normalizer permutes them. Each primitive plane is a free rank-one Eisenstein lattice: its integral normalizer is D12. The repaired basis S^-1 P is unimodular, hence the full group is D12 wreath C2, order288. Filtering these288 rational candidates for original-Z4 integrality gives144; every original normalizer must already be among them.',
        'no_equivariant_bijection':'The six binary kernels are transitive under either normalizer, while the six ternary polarities split2+4. Thus no bijection intertwines these declared actions.',
        'integral_liftable_polarity_indices':[0,3],
        'prior':['PASS12186_CONTEXT_LOCKING_NATIVE_COVER.md','PASS12188_NATIVE_PERIOD_SYMPLECTIC_REPAIR.md']}


@lru_cache(None)
def yukawa_slice():
    _,R=native.native();w=OMEGA
    la=s.Matrix([[0,0,-s.conjugate(w),1]])
    lb=s.Matrix([[-1-2*w,2+w,-w,1]])
    for g,M in R.items():
        assert all(s.simplify(z)==0 for z in la*M-w**(-g[1]%3)*la)
        assert all(s.simplify(z)==0 for z in lb*M-w**(-g[0]%3)*lb)
    # The real-linear map x -> (Re alpha,Im alpha,Re beta,Im beta) is invertible.
    realmap=s.Matrix.vstack(la.applyfunc(s.re),la.applyfunc(s.im),lb.applyfunc(s.re),lb.applyfunc(s.im))
    determinant=s.simplify(realmap.det());assert determinant!=0
    a,b,c,d=s.symbols('a b c d',real=True)
    alpha=a+s.I*b;beta=c+s.I*d
    X=s.Matrix([[0,0,1],[1,0,0],[0,1,0]]);Z=s.diag(1,w,s.conjugate(w))
    Y=alpha*X+s.conjugate(alpha)*X.T+beta*Z+s.conjugate(beta)*Z.conjugate()
    Y=Y.applyfunc(s.expand_complex)
    assert s.simplify(s.trace(Y))==0 and Y==Y.conjugate().T
    tr2=s.simplify(s.trace(Y*Y));det=s.factor(s.expand_complex(Y.det()))
    adj=Y.adjugate();norm=s.simplify(s.trace(adj.conjugate().T*adj))
    assert s.simplify(tr2-6*(a*a+b*b+c*c+d*d))==0
    assert s.expand(det-2*(a**3-3*a*b*b+c**3-3*c*d*d))==0
    assert s.simplify(norm-tr2**2/4)==0
    # An actual integral normalizer exchanges the two liftable polarities.
    K=s.Matrix([[1,0,1,1],[0,1,1,1],[0,0,0,-1],[0,0,-1,0]])
    F0=native.alternating([-3,-1,-2,2,1,0])
    F1=native.alternating([-3,-1,-2,2,1,-2])
    _,_,S,_=native.repaired();Krepair=S.inv()*K*S
    assert K*K==s.eye(4) and K.det()==-1 and K.T*F0*K==F1
    assert all(s.simplify(z)==0 for z in la*K-w**2*la.conjugate())
    assert all(s.simplify(z)==0 for z in lb*K-lb)
    assert all(K*R[g]*K==R[(g[0],(-g[1])%3,(-g[2]+2*g[0])%3)]for g in R)
    # Standard E6 norm N(A,B,C)=det A+det B+det C-Tr ABC.
    # At (Y,0,0), F_A=adj(Y)^T and the other18 F terms vanish.
    r2=a*a+b*b+c*c+d*d
    assert s.expand(norm-9*r2*r2)==0
    dquartic=s.simplify(s.trace(Y**4)-tr2**2/3)
    assert s.simplify(dquartic-tr2**2/6)==0
    return {'pass':12191,'status':'EXPLICIT_NATIVE_INTERTWINER_AND_E6_SLICE_VACUUM_TEST',
        'alpha_row':[str(s.expand_complex(z))for z in la],
        'beta_row':[str(s.expand_complex(z))for z in lb],
        'real_map_determinant':str(determinant),
        'polarity_exchange':{'original_matrix':matrix_list(K),'repaired_matrix':matrix_list(Krepair),
            'determinant':-1,'square':'I','form_identity':'K^T F(1,0) K=F(1,-2)',
            'coefficient_map':'alpha -> omega^2 conjugate(alpha); beta -> beta',
            'antiunitary':'Theta=Z^2 complex_conjugation; Theta^2=I',
            'texture_identity':'Y(Kx)=Z^2 conjugate(Y(x)) Z^(-2)',
            'address_automorphism':'(a,b,c)->(a,-b,-c+2a) mod3',
            'consequence':'The two integral polarities give antiunitarily isospectral textures with identical real cubic, F/D potential and isotropic/real-cubic soft potential. They cannot select different mass hierarchies in this model.',
            'scope':'Explicit finite antiunitary intertwiner, not an independently justified physical time-reversal operation or derived chirality choice.'},
        'address_operator':'W(a,b,c)=omega^c X^a Z^(-b)',
        'map':'x -> (Y(x),0,0), Y=alpha X+alpha* Xdag+beta Z+beta* Zdag',
        'E6_action':'(P,Q,R)=(W_g,W_g,I): (A,B,C)->(P A Q^-1,Q B R^-1,R C P^-1)',
        'native_covariance':'alpha(R_g x)=omega^(-g.b) alpha(x); beta(R_g x)=omega^(-g.a) beta(x), so Y(R_g x)=W_g Y(x) W_gdag',
        'invariant_cubic':'N=det A+det B+det C-Tr(ABC)',
        'trY2':str(tr2),'detY':str(det),'Fterm_norm_squared':str(norm),
        'actual_E6_BC_mass_map':'At A=Y, the mixed cubic Hessian couples B_(j,k) to C_(k,i) by -Y_(i,j). Ordering pairs by k gives M_BC=-I3 tensor Y^T: every singular value of Y occurs three times. Identifying Y itself with three physical family Yukawas requires an additional matter embedding.',
        'Dterm_trace_invariant':str(dquartic),
        'Dterm_normalization':'With Tr(tA tB)=deltaAB/2 and canonical kinetic terms, V_D=(gL^2+gR^2)*(Tr(Y^4)-(Tr(Y^2))^2/3)/4=(gL^2+gR^2)*(Tr(Y^2))^2/24, also radial on this slice.',
        'soft_cubic_selection':'At fixed r2, |det Y|<=2*r2^(3/2). Equality requires exactly one of alpha,beta nonzero, with its cube real. A nonzero real soft detY term therefore selects singular values proportional to (2,1,1), not a three-way hierarchy, if a stable nonzero radial minimum exists.',
        'radial_vacuum':'V_F=9*(|alpha|^2+|beta|^2)^2. Adding a common tachyonic soft mass -m2*r2 yields r2=m2/18 but leaves the entire angular S3 flat.',
        'Fflat_proof':'adj(Y)=0 implies rank(Y)<=1. A Hermitian traceless rank<=1 matrix is zero. The only F-flat point on THIS four-real-dimensional slice is x=0.',
        'scope':'Named equivariant map into the standard complex E6 trinification cubic. This does not identify the preferred E8 root embedding, the fitted theta Yukawa textures, or choose a three-family vacuum. Two complex intertwiner scalars remain free. The six polarities alone do not fix these Yukawa coefficients.',
        'prior':['PASS12188_NATIVE_PERIOD_SYMPLECTIC_REPAIR.md','papers/forty_points/sec05_e8.tex','w33_pass12034_12038_joint_mechanisms.py','https://mahalex.net/about-me/publications/minie6.pdf']}


def graph_inputs():
    d=json.loads((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_text())
    H=list(product(range(3),repeat=3));idx={g:i for i,g in enumerate(H)}
    dirs=((0,0,1),(0,1,1),(1,0,1),(1,1,0),(1,2,2))
    edges=sorted({tuple(sorted((idx[g],idx[native.mul(g,t)])))for g in H for z in dirs for t in(z,native.mul(z,z))})
    B=np.zeros((135,27));aa,bb=np.array(edges).T
    B[np.arange(135),aa]=-1;B[np.arange(135),bb]=1
    V=np.array(d['primitive_integer_edge_voltages'],dtype=float)
    G=np.array(s.Matrix(d['exact_acoustic_metric']),dtype=float)
    assert len(edges)==135 and np.linalg.matrix_rank(B)==26
    return d,B,V,G,aa,bb


def conductivity(w,b,V):
    h=V-b@np.linalg.solve(b.T@(w[:,None]*b),b.T@(w[:,None]*V))
    return h.T@(w[:,None]*h)/27,h


@lru_cache(None)
def continuum_bridge():
    d,B,V,G,aa,bb=graph_inputs();b=B[:,1:];rho=np.sqrt(np.linalg.det(G))
    baseline,h=conductivity(np.ones(135),b,V)
    assert np.max(abs(baseline-G))<1e-13
    rows=[];modes=np.array([x for x in product(range(-2,3),repeat=4)if any(x)],float)
    reference=np.einsum('ni,ij,nj->n',modes,G/rho,modes)
    for N in (8,16,32,64):
        k=2*np.pi/N*modes;phase=np.exp(1j*k@V.T)
        L=np.tile(np.diag(np.bincount(np.r_[aa,bb],minlength=27)),(len(k),1,1)).astype(complex)
        L[:,aa,bb]-=phase;L[:,bb,aa]-=phase.conjugate()
        eigen=np.linalg.eigvalsh(L)[:,0]/(rho*(2*np.pi/N)**2)
        error=float(np.max(abs(eigen-reference)/reference))
        rows.append({'N':N,'total_graph_vertices':27*N**4,'tested_nonzero_modes':len(modes),
                     'distinct_tested_acoustic_values':len(np.unique(np.round(eigen,8))),
                     'max_relative_dispersion_error':error})
    assert all(rows[i+1]['max_relative_dispersion_error']<rows[i]['max_relative_dispersion_error']/3.5 for i in range(3))
    # Two independent nonlinear weight fields; internal cell-gauge invariance
    # and the exact negative conductivity Hessian are tested away from w=1.
    rng=np.random.default_rng(12192);directions=rng.normal(size=(2,135))*.05
    gauge=rng.normal(size=(26,4));nonlinear=[]
    for theta,phi in ((.2,-.3),(-.4,.1),(.35,.4)):
        w=np.exp(theta*directions[0]+phi*directions[1]);K,h=conductivity(w,b,V)
        density=np.sqrt(np.linalg.det(K));metric=density*np.linalg.inv(K)
        assert abs(np.linalg.det(metric)-density**2)<1e-10
        Kg,_=conductivity(w,b,V+b@gauge);gauge_error=float(np.max(abs(Kg-K)));assert gauge_error<1e-12
        z=directions[0];Z=b.T@(z[:,None]*h)
        hessian=-2*Z.T@np.linalg.solve(b.T@(w[:,None]*b),Z)/27
        assert max(np.linalg.eigvalsh(hessian))<1e-12
        step=1e-3
        fd=(conductivity(w+step*z,b,V)[0]-2*K+conductivity(w-step*z,b,V)[0])/step**2
        hess_error=float(np.max(abs(fd-hessian)));assert hess_error<1e-8
        nonlinear.append({'theta':theta,'phi':phi,'minimum_weight':float(min(w)),
                          'capacity_density':float(density),'conductivity':K.tolist(),'metric':metric.tolist(),
                          'internal_gauge_error':gauge_error,'Hessian_fd_error':hess_error})
    return {'pass':12192,'status':'NATIVE_PERIODIC_SPECTRAL_TOWER_AND_NONLINEAR_DENSITY_IDENTITY',
        'native_graph':'11991, 27 vertices and135 edges per Z4 cell; not the diameter-two W(3,q) tower',
        'Bloch_controls':rows,'nonlinear_controls':nonlinear,
        'flat_limit_theorem':'Primitivity of the actual cycle-voltage lattice gives a Bloch zero only at k=0. The base graph has one zero and a positive optical gap. Analytic perturbation gives lambda0(k)=k^T G k+O(|k|^4). Compactness gaps all momenta away from0. Therefore at a=2pi/N every fixed-energy spectral window of L/(rho*a^2) converges, with multiplicities away from boundary levels, to the flat4torus Laplacian with symbol G/rho. Its limiting counting function grows as (pi^2*rho/2)*E^2. This is a standard periodic-graph argument specialized to the certified native data, not new homogenization theory.',
        'Weyl_coefficient':float(np.pi**2*rho/2),
        'nonlinear_density':'K(w)=h^T W h/27; rho(w)=sqrt(det K); g(w)=rho K^-1. Then sqrt(det g)=rho and rho*g^-1=K exactly in dimension4. Capacities rho and edge conductivities K are both needed for the Laplace-Beltrami target.',
        'cell_gauge_identity':'V -> V+b chi leaves K(w) invariant for every positive w. This is internal cell-coordinate gauge, not spacetime diffeomorphism invariance.',
        'exact_Hessian':'d2K[w](z,z)=-2/27 (b^T diag(z)h)^T (b^T W b)^-1 (b^T diag(z)h), negative semidefinite.',
        'scope':'A native Euclidean four-dimensional kinematic spectral limit and exact nonlinear constitutive identities. No Lorentzian propagation, derived dynamics of weights, nonlinear Einstein equations, gravitational Ward identities or Newton/Lambda normalization is claimed. Earlier11991/11995/12023/12029 own the cover, metric chart and curved recovery/heat methods.',
        'prior':['w33_pass11991_native_four_period_cover.py','w33_pass11995_native_metric_gr_lift.py','prior12023 curved recovery, as cited in w33_pass12029_native_heat_curvature.py','w33_pass12029_native_heat_curvature.py','2026-10-22_five_frontiers_round6.md',
                 'https://epubs.siam.org/doi/10.1137/20M1368513']}


def build():
    inputs=['data/w33_pass11991_native_four_period_cover.json','data/w33_pass12186_context_cover_holonomy.json']
    return {'schema':'w33.passes12189-12193.five_bridges.v1',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'input_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in inputs},
        'magic':heralded_magic(),'discriminant':discriminant_weil(),
        'yukawa':yukawa_slice(),'continuum':continuum_bridge(),'normalizer':normalizer_actions()}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'data/w33_pass12189_12193_five_bridges.json');args=parser.parse_args()
    result=build();args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS five bridges',flush=True)
