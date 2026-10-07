"""Five explicit continuations: covariant pairs, scalar orbit, shared flavor,
linear gravitational blocking and top-form quantum response.

Owners11615-11619: weight proxy/threshold interface;11600: Hesse intertwiner;
11595: Sym^2(16)=10+126;11284: closed history;11306: relational clocks;
11316 already owns the native-edge two-helicity/free-spin-two construction;
11425/11430: curved Regge normal blocking, not a perfect nonlinear action.
All potentials, geometry, flux sectors and scales below are declared inputs.
"""
from functools import lru_cache
from pathlib import Path
from math import comb
import hashlib
import itertools
import json
import sys

import numpy as np
import sympy as s
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass11615_11619_parent_pairs_constraints import gauge_grams, yukawa, ph
from w33_pass11284_closed_history_flux import top_boundary

OUT=ROOT/'data/w33_pass11620_11624_covariant_pair_vacuum.json'
RESERVATION='7a3b8dabf'


def sparse_pack(A):
    rows,cols=np.nonzero(A)
    return dict(shape=list(A.shape),rows=rows.tolist(),cols=cols.tolist(),
                values=[int(A[i,j]) for i,j in zip(rows,cols)])


@lru_cache(None)
def spin_pair_data():
    _,_,full,pairs=gauge_grams()
    odd=[i for i in range(32) if i.bit_count()%2]
    T=np.array([a[np.ix_(odd,odd)] for a in full])
    slots=list(itertools.combinations_with_replacement(range(16),2))
    B=np.zeros((136,16,16),complex)
    for z,(i,j) in enumerate(slots):B[z,i,j]=B[z,j,i]=1 if i==j else 1/np.sqrt(2)
    # Shape generator,basis,row,col. Casimir -sum Tpair^2 is positive.
    d=np.array([np.einsum('ij,bjk->bik',t,B)+np.einsum('bij,kj->bik',B,t) for t in T])
    R=np.einsum('bij,acij->abc',B.conj(),d)
    C=-np.einsum('aij,ajk->ik',R,R)
    assert np.max(abs(C-C.conj().T))<1e-13
    assert np.max(abs((C-9*np.eye(136))@(C-25*np.eye(136))))<1e-11
    P10=(25*np.eye(136)-C)/16;P126=(C-9*np.eye(136))/16
    assert abs(np.trace(P10)-10)<1e-12 and abs(np.trace(P126)-126)<1e-12
    assert max(np.max(abs(t@P126-P126@t)) for t in R)<1e-13
    vals,Q=np.linalg.eigh(P126);U=Q[:,vals>.5]
    assert U.shape==(136,126)
    Sbasis=np.einsum('bj,bkl->jkl',U,B)
    # Unnormalized symmetric coordinates remove all sqrt2 factors for exact
    # rational rank certificates, while physical Hessians use orthonormal B.
    norms=np.array([1 if i==j else np.sqrt(2) for i,j in slots])
    raw=np.zeros_like(B)
    for z,(i,j) in enumerate(slots):raw[z,i,j]=raw[z,j,i]=1
    # This path uses only integer and half-integer Gaussian entries. IEEE
    # operations here are exact dyadic arithmetic, with no sqrt2 involved.
    Craw=22.5*raw-2*sum(np.einsum('ij,bjk,lk->bil',t,raw,t) for t in T)
    Cr=np.array([[z[i,j] for i,j in slots] for z in Craw]).T
    assert not np.any(Cr.imag)
    C4=np.rint(4*Cr.real).astype(np.int64)
    assert np.array_equal(C4/4,Cr)
    I=np.eye(136,dtype=np.int64)
    assert not np.any((C4-36*I)@(C4-100*I))
    assert np.trace(C4)==12960
    for t in T:
        dr=np.einsum('ij,bjk->bik',t,raw)+np.einsum('bij,kj->bik',raw,t)
        rr=np.array([[z[i,j] for i,j in slots] for z in dr]).T
        assert not np.any(C4@rr-rr@C4)
    assert np.max(abs(C*norms[None,:]/norms[:,None]-Cr))<1e-12
    P10raw=(100*np.eye(136,dtype=np.int64)-C4)/64
    return T,pairs,B,R,C,P10,P126,Sbasis,raw,P10raw


def rank_mod(A,p=101):
    a=np.asarray(A,dtype=np.int64).copy()%p;r=0
    for col in range(a.shape[1]):
        hits=np.flatnonzero(a[r:,col])
        if not len(hits):continue
        j=r+hits[0];a[[r,j]]=a[[j,r]]
        a[r]=a[r]*pow(int(a[r,col]),-1,p)%p
        rows=np.flatnonzero(a[:,col]);rows=rows[rows!=r]
        a[rows]=(a[rows]-a[rows,col,None]*a[r])%p
        r+=1
        if r==min(a.shape):break
    return r


def covariant_pair():
    T,pairs,B,R,C,P10,P126,Sbasis,raw,Praw=spin_pair_data()
    coeff=np.einsum('bij,ij->b',B.conj(),np.diag([0]*15+[1]))
    assert np.linalg.norm(P10@coeff)<1e-14
    angle=.137;G=expm(angle*T[8])
    S=np.einsum('b,bij->ij',coeff,B);SG=G@S@G.T
    transformed=np.einsum('bij,ij->b',B.conj(),SG)
    assert np.linalg.norm(P10@transformed)<1e-13
    # Scalar kernel proof uses a connected graph and permutations; two-site
    # controls use two independent actual126 directions instead of a weight.
    low=3;swap=np.zeros((low*low,low*low))
    for i in range(low):
        for j in range(low):swap[i*low+j,j*low+i]=1
    h=(np.eye(low*low)-swap)/2
    assert np.linalg.matrix_rank(h)==3
    assert np.linalg.norm(h@h-h)<1e-14
    gauge=expm(.19*R[8]);assert np.linalg.norm(gauge@P126-P126@gauge)<1e-12
    C4=np.rint(100*np.eye(136)-64*Praw).astype(np.int64)
    return dict(status='PASS',Casimir_eigenvalues={'9':10,'25':126},
        Casimir_raw_scaled4_sparse=sparse_pack(C4),
        projector='C=-sum_a(Ta tensor1+1tensor Ta)^2; P10=(25I-C)/16; P126=(C-9I)/16 on Sym^2(16bar). All45 intertwining commutators vanish.',
        onsite='Hsite=0plus16barplusSym^2(16bar), complex dimension153. Honsite=Delta P16+kappa P10, Delta,kappa>0; low space=0plus126bar, dimension127.',
        edge='Hedge=J(P_low tensor P_low)(I-Swap)/2, J>0. It acts as zero whenever either site is outside low space. Gauge covariance: use Swap_U=(R_low(U)tensor R_low(U)^dagger)Swap on an oriented link; U->g_i U g_j^-1 gives endpoint covariance.',
        ground_theorem='For a connected graph with flat trivializable supplied links, positivity and edge swaps give Sym^N(C^127). At fixed k pairs the ground space is Sym^k(C^126), dimension binomial(k+125,125). This explicitly removes the hidden one-weight restriction; the vacuum orientation is not unique.',
        W33_ground_dimensions={'all':str(comb(206,126)),'half_filling':str(comb(165,125))},
        polarized_sector='For any normalized126 direction w, the fixed-k state has <B_i^dag(w)B_j(w)>=k(N-k)/(N(N-1)) and largest eigenvalue k(N-k+1)/N. B^dag(w)|0>=|w>. The earlier a^2 normalization multiplies these by2. At N80,k40:20/79 and41/2.',
        gap='Every globally odd state has at least one16bar occupation and energy>=Delta. One16bar site and vacuum elsewhere saturates Delta. Ten-channel occupation costs at least kappa.',
        boundary='Full Spin10-covariant added occupation Hamiltonian, not Lorentzian continuum, derived gauge-link dynamics, selected126 orientation, non-flat frustration theorem or a gauged Higgs phase. Atomic one-point order vanishes in its even ground sector; gauge-charged one-point values are not physical observables.')


def scalar_jacobians():
    T,pairs,B,R,C,P10,P126,Sbasis,raw,Praw=spin_pair_data()
    V=np.zeros((45,10,10))
    for k,(i,j) in enumerate(pairs):V[k,i,j]=1;V[k,j,i]=-1
    A=sum(V[pairs.index((2*j,2*j+1))] for j in range(3))
    tA=sum(T[pairs.index((2*j,2*j+1))] for j in range(3))
    S=np.diag([0]*15+[1]).astype(complex)
    assert np.max(abs(tA@S+S@tA.T+3j*S))<1e-14
    dA=np.array([v@A@A+A@v@A+A@A@v+v for v in V])
    J3=dA.reshape(45,-1).T/np.sqrt(2)
    gA=np.einsum('aij,ij->a',V,A)
    D=np.concatenate([Sbasis,1j*Sbasis])/np.sqrt(2)
    gS=2*np.einsum('aij,ij->a',D.conj(),S).real
    Jpur=D[:,:15,:15].reshape(252,-1).T
    JA=np.array([t@S+S@t.T for t in T]).reshape(45,-1).T
    JS=np.array([tA@d+d@tA.T+3j*d for d in D]).reshape(252,-1).T
    Jalign=np.concatenate([JA,JS],axis=1)
    H=np.zeros((297,297))
    H[:45,:45]=2*np.outer(gA,gA)+2*(J3.conj().T@J3).real
    H[45:,45:]=2*np.outer(gS,gS)+4*(Jpur.conj().T@Jpur).real
    H+=2*(Jalign.conj().T@Jalign).real
    # Exact rational residual Jacobian in ambient45+136complex coordinates.
    Dr=np.concatenate([raw,1j*raw])
    jr=np.array([tA@d+d@tA.T+3j*d for d in Dr]).reshape(272,-1).T
    ja=np.array([t@S+S@t.T for t in T]).reshape(45,-1).T
    complex_align=np.concatenate([ja,jr],axis=1)
    def realrows(Z):return np.concatenate([Z.real,Z.imag],axis=0)
    zeroA=np.zeros((15*15,45))
    pure=np.concatenate([zeroA,Dr[:,:15,:15].reshape(272,-1).T],axis=1)
    p10=np.zeros((272,317));p10[:136,45:181]=Praw;p10[136:,181:]=Praw
    adj=np.zeros((100,317));adj[:,:45]=dA.reshape(45,-1).T
    normA=np.zeros((1,317));normA[0,:45]=gA
    normS=np.zeros((1,317));normS[0,45:181]=2*np.einsum('aij,ij->a',raw.conj(),S).real
    J=np.vstack([realrows(complex_align),realrows(pure),p10,adj,normA,normS])
    scaled=np.rint(J*64).astype(np.int64)
    assert np.max(abs(scaled/64-J))<1e-13
    # Explicit gauge tangent upper bound matches the modular rank lower bound.
    ga=np.array([v@A-A@v for v in V])
    avec=np.einsum('aij,bij->ab',V,ga)/2
    gs=np.array([t@S+S@t.T for t in T])
    scoeff=np.array([[z[i,j] for i,j in itertools.combinations_with_replacement(range(16),2)] for z in gs])
    Graw=np.vstack([avec,scoeff.real.T,scoeff.imag.T])
    assert np.max(abs(J@Graw))<1e-12
    Gi=np.rint(2*Graw).astype(np.int64)
    assert np.array_equal(Gi/2,Graw)
    assert not np.any(scaled@Gi)
    return H,J,scaled,Gi,A,S,V,T,D


def scalar_vacuum():
    H,J,Ji,Gi,A,S,V,T,D=scalar_jacobians()
    assert rank_mod(Ji)==284 and rank_mod(Gi)==33
    # Ambient317 minus20 linear10 directions ->297; exactly33 gauge zeros.
    ev=np.linalg.eigvalsh(H)
    positive=ev[ev>1e-8]
    assert len(positive)==264 and np.min(ev)>-1e-11
    # Numerical canonical masses are checked by a separate exact rational
    # characteristic factorization; rank/positivity has its own certificate.
    groups=[]
    for mass in positive:
        if not groups or abs(groups[-1]['mass_squared']-mass)>1e-7:groups.append({'mass_squared':float(mass),'multiplicity':1})
        else:groups[-1]['multiplicity']+=1
    moment=float(np.sum(positive**2))
    exact=exact_scalar_spectrum(J)
    assert exact['sum_m4']=='117157/2'
    assert abs(moment-117157/2)<1e-8
    orbit=global_scalar_orbit()
    return dict(status='PASS',
        potential='V=lambdaA(||A||^2-3a^2)^2+(kappa/M^2)||A^3+a^2 A||^2+lambdaS(||S||^2-b)^2+eta[(TrSSdag)^2-Tr(SSdagSSdag)]+zeta||T_A S+S T_A^T+3i a S||^2. A real45, S in126bar, ||A||^2=-TrA^2/2; all coefficients and a,b,M positive.',
        positivity='Purity term equals2 sum|all2x2 minors of S|^2. Every summand is nonnegative. A=a(J01+J23+J45), S=sqrt(b)|11111><11111|_symmetric saturates all terms. This is a global zero minimum of the declared cutoff action.',
        units='a=b=M=lambdaA=kappa=lambdaS=eta=zeta=1 for the complete297-coordinate physical Hessian. Real adjoint kinetic1/2||dA||^2; complex126 kinetic||dS||^2, so real components of S are divided bysqrt2.',
        exact_normal_certificate={'ambient_columns':317,'ten_channel_constraints_real_rank':20,'residual_rank_mod101':284,'gauge_tangent_rank_mod101':33,'physical_field_dimension':297,'exact_gauge_zero_dimension':33,'exact_positive_normal_dimension':264,'residual_shape':list(Ji.shape),'residual_scaled64_sparse':sparse_pack(Ji),'gauge_scaled2_sparse':sparse_pack(Gi)},
        proof='The scaled integer residual Jacobian has rank284 mod101, hence rational rank>=284. Its explicit33 independent gauge tangents lie in the kernel, hence rank<=284. A positive sum of residual squares therefore has exactly33 zeros and264 positive126/45 normal directions. An independent rational kinetic-normalized operator is split into215 coordinate blocks of size at most5; exact characteristic polynomials give the full physical mass spectrum.',
        exact_mass_spectrum=exact,
        global_orbit=orbit,
        mass_groups_numeric=groups,scalar_sum_m4_numeric=moment,
        vector_sum_m4_at_same_VEV=444,
        standard_minimal_warning='For the distinct standard renormalizable45+126 potential, the tree triplet/octet at omegaR=0 are proportional to-2a2 omegaBL^2 and4a2 omegaBL^2. They cannot both be strictly positive. Known loop stabilization exists. The positive sextic-adjoint EFT above does not supersede that model or prove its radiative vacuum.',
        boundary='A unique zero orbit of an engineered gauge-invariant SM cutoff action, not the minimal renormalizable45+126 potential, selected coefficient/scale, one-loop-stable vacuum or observed masses. The sextic term is an EFT interaction. Covariant pair Hamiltonian and this elementary126 scalar action are separate models until an effective matching map is built.')


def global_scalar_orbit():
    T,pairs,B,R,C,P10,P126,Sbasis,raw,Praw=spin_pair_data()
    tA=sum(T[pairs.index((2*j,2*j+1))] for j in range(3))
    extreme=np.flatnonzero(np.diag(tA)==-1.5j)
    assert list(extreme)==[14,15]
    for i,j in [(14,14),(14,15),(15,15)]:
        v=np.zeros((16,16),complex);v[i,j]=v[j,i]=1
        c=np.einsum('bij,ij->b',B.conj(),v)
        assert np.linalg.norm(P10@c)<1e-14
        cr=np.array([v[a,b] for a,b in itertools.combinations_with_replacement(range(16),2)])
        assert not np.any(Praw@cr)
    ops=[t[np.ix_(extreme,extreme)] for t,p in zip(T,pairs) if min(p)>=6]
    vectors=np.array([np.concatenate([x.real.ravel(),x.imag.ravel()]) for x in ops])
    ints=np.rint(2*vectors).astype(np.int64)
    assert np.array_equal(ints/2,vectors) and rank_mod(ints)==3
    return dict(status='PASS',
        theorem='All zero minima of the declared positive45/126 action form one Spin10 orbit, at every positive input coefficient and a,b,M. Its connected stabilizer is SU3c x SU2L x U1Y in the standard embedding.',
        proof='A^3+a^2 A=0 and ||A||^2=3a^2 imply exactly three nonzero skew eigenplanes of magnitude a. SO10 conjugates every such rank6 A to a(J01+J23+J45), with sign compensation in the two zero planes. Purity and ||S||^2=b give S=sqrt(b)vv^T, ||v||=1. Alignment implies T_A v=-3ia v/2. This extremal eigenspace is complex dimension2; its whole symmetric square lies in126. The last4-vector Spin4 acts on it as SU2, with all three generators explicitly present. SU2 is transitive on the unit3-sphere, including phase, so all S choices are gauge equivalent.',
        extreme_spinor_indices=[14,15],extreme_complex_dimension=2,Spin4_restricted_algebra_rank=3,
        matter_parity='The Spin10 central element minus1 acts as minusI on16bar and plusI on126bar and45. The vacuum has no16bar VEV, so that gauge transformation is unbroken. It is not in the connected SM stabilizer because the16bar SM singlet is odd under it.',
        boundary='Uniqueness is modulo gauge for this supplied tree cutoff potential. Its input radius/adjoint spectrum and degree6 operator are engineered, not predicted; no quantum stability or effective matching of the composite occupation model is proved.')


def exact_scalar_spectrum(J):
    # J rows: complex alignment512, complex top-left minors450,
    # ten-channel linear constraints272, adjoint cubic100, two norms2.
    assert J.shape==(1336,317)
    H=2*J[-2:].T@J[-2:]+2*J[:512].T@J[:512]+4*J[512:962].T@J[512:962]+J[1234:1334].T@J[1234:1334]
    *_,raw,P10=spin_pair_data()
    metric=np.concatenate([np.ones(45),2*np.sum(abs(raw)**2,axis=(1,2)),2*np.sum(abs(raw)**2,axis=(1,2))])
    P=np.eye(317);P[45:181,45:181]=np.eye(136)-P10;P[181:,181:]=np.eye(136)-P10
    L=P@(H/metric[:,None])@P
    W=np.rint(L*65536).astype(np.int64)
    assert np.array_equal(W/65536,L)
    seen=set();factors={};sizes=[];z=s.Symbol('z')
    for i in range(317):
        if i in seen:continue
        block=[i];seen.add(i)
        for q in block:
            for j in np.flatnonzero((W[q]!=0)|(W[:,q]!=0)):
                j=int(j)
                if j not in seen:seen.add(j);block.append(j)
        sizes.append(len(block))
        A=s.Matrix([[s.Rational(int(W[i,j]),65536) for j in block] for i in block])
        for factor,n in s.factor_list(A.charpoly(z).as_expr())[1]:
            factors[str(factor)]=factors.get(str(factor),0)+n
    expected={'z - 2':5,'z - 8':8,'z**2 - 44*z + 204':1,'z - 6':54,'z':53,'z - 3':24,'z - 4':3,'z - 38':6,'z - 27':24,'z - 18':60,'z - 11':68,'2*z - 19':4,'2*z - 9':6}
    assert factors==expected
    moment=s.Rational(sum(int(W[i,j])*int(W[j,i]) for i,j in zip(*np.nonzero(W))),65536**2)
    assert moment==s.Rational(117157,2)
    return dict(characteristic_factors=factors,blocks=len(sizes),largest_block=max(sizes),
                ambient_zero_count=53,unphysical_ten_zero_count=20,physical_gauge_zero_count=33,
                two_irrational_masses_squared=['22-2sqrt70','22+2sqrt70'],sum_m4=str(moment),
                mass_operator_shape=[317,317],mass_operator_scaled65536_sparse=sparse_pack(W))


def shared_flavor():
    w=-s.Rational(1,2)+s.I*s.sqrt(3)/2
    F=s.Matrix(3,3,lambda i,j:w**(i*j)/s.sqrt(3));P=s.diag(1,1,w)
    RF=s.Matrix([[1,s.sqrt(2)],[s.sqrt(2),-1]])/s.sqrt(3);RP=s.diag(1,w)
    u=s.Matrix(s.symbols('u0:2',real=True));h=s.Matrix(s.symbols('h0:3',real=True))
    def Y(U,H):return yukawa(s.conjugate(U[0])/s.sqrt(3),s.conjugate(U[1])/s.sqrt(6),H)
    errors=[]
    for G,R in [(F,RF),(P,RP)]:
        delta=G.T*Y(R*u,G*h)*G-Y(u,h)
        assert all(s.simplify(z)==0 for z in delta)
        errors.append(True)
    # Source covariant mediators transform in conjugate(R)tensor G.
    rng=np.random.default_rng(11622);uu=rng.normal(size=2)+1j*rng.normal(size=2);hh=rng.normal(size=3)+1j*rng.normal(size=3)
    base=np.array(Y(s.Matrix(uu),s.Matrix(hh)),complex)
    joint=[]
    for g,r in [(np.array(F,complex),np.array(RF,complex)),(np.array(P,complex),np.array(RP,complex))]:
        changed=np.array(Y(s.Matrix(r@uu),s.Matrix(g@hh)),complex)
        joint.append(float(np.max(abs(np.linalg.svd(base,compute_uv=False)-np.linalg.svd(changed,compute_uv=False)))))
        assert joint[-1]<1e-12
    x=s.symbols('x0:4',real=True);z=s.Matrix([x[0]+s.I*x[1],x[2]+s.I*x[3]])
    m=Y(z,s.Matrix([1,2,3]));K=m.H*m
    fixed=s.expand(s.trace(K*K))
    transformed=Y(RF*z,s.Matrix([1,2,3]));defect=s.simplify(s.trace((transformed.H*transformed)**2)-fixed)
    assert s.simplify(defect.subs(dict(zip(x,[1,0,0,0]))))==s.Rational(16,3)
    return dict(status='PASS',joint_covariance='G^T Y(Ru,Gh)G=Y(u,h), exactly for(F,RF) and(P,RP), using11600 normalized tensors. Thus every singular-spectrum threshold is invariant under the simultaneous transformations, for arbitrary complex u,h.',
        mediator_completion='A_j transforms as conjugate(R)_jk G A_k; u transforms as R u; H and matter family triplets transform as G. The positive mediator source M A+conjugate(u)tensor H and the tensor Yukawa interaction are covariant. Channels must share the invariant mediator mass/coupling; independent channel masses generally break the extended symmetry.',
        joint_singular_errors=joint,fixed_alignment_quartic_defect='16/3',
        counterterm='Tr[(YdagY)^2] is a joint invariant and still contains degree4 angular dependence in u after unequal h freezes. Extending symmetry to all fields repairs explicit interaction covariance, not lower-degree angular protection in a broken Higgs background.',
        potential_extension='Any scalar seed polynomial can be orbit-summed over the finite parent to make a joint invariant, but that does not prove the seed minimum survives. No uncalculated orbit-sum is assigned a stable vacuum.',
        boundary='Common finite family action named and checked; no automatic selected simultaneous flavor/Higgs vacuum, protected high-degree hierarchy, anomaly-safe gauging, beta functions or measured Yukawa coefficients.')


def fp_mode(k):
    dim=len(k);slots=list(itertools.combinations_with_replacement(range(dim),2))
    B=[]
    for i,j in slots:
        b=s.zeros(dim);b[i,j]=b[j,i]=1 if i==j else 1/s.sqrt(2);B.append(b)
    k=s.Matrix(k);k2=(k.T*k)[0]
    def E(h):
        return k2*h-k*(k.T*h)-(h*k)*k.T+k*k.T*s.trace(h)-s.eye(dim)*(k2*s.trace(h)-(k.T*h*k)[0])
    K=s.Matrix(len(B),len(B),lambda i,j:s.simplify(s.trace(B[i]*E(B[j]))))
    G=s.Matrix(len(B),dim,lambda i,j:s.simplify(s.trace(B[i]*(k*s.eye(dim)[:,j].T+s.eye(dim)[:,j]*k.T))))
    assert K==K.T and K*G==s.zeros(len(B),dim)
    return K,G,B


def gravitational_block():
    K,G,B=fp_mode([1,2,0,1]);assert K.rank()==6 and G.rank()==4
    # h0mu can be gauged to zero at nonzero k0; spatial six are a complement.
    complement=s.zeros(10,6)
    for j,i in enumerate([4,5,6,7,8,9]):complement[i,j]=1
    T=G.row_join(complement);assert T.det()!=0
    full=s.simplify(T.T*K*T)
    chosen=None
    for elim in itertools.combinations(range(4,10),3):
        if full.extract(elim,elim).det()!=0:chosen=elim;break
    keep=[i for i in range(10) if i not in chosen]
    A=full.extract(keep,keep);D=full.extract(chosen,chosen);C=full.extract(keep,chosen)
    blocked=s.simplify(A-C*D.inv()*C.T)
    assert blocked.rank()==3 and blocked[:4,:]==s.zeros(4,7)
    # Canonical linearized ADM: three momentum and one Hamiltonian constraints.
    k=s.Matrix([1,2,3]);_,_,Bs=fp_mode(list(k));n=6
    q=s.Matrix(s.symbols('q0:6'));p=s.Matrix(s.symbols('p0:6'))
    h=sum((q[i]*Bs[i] for i in range(n)),s.zeros(3));pi=sum((p[i]*Bs[i] for i in range(n)),s.zeros(3))
    Cs=[((k.T*h*k)[0]-(k.T*k)[0]*s.trace(h))]+list(-2*pi*k)
    J=s.Matrix(Cs).jacobian(list(q)+list(p));omega=s.zeros(12)
    omega[:6,6:]=s.eye(6);omega[6:,:6]=-s.eye(6)
    assert J.rank()==4 and s.simplify(J*omega*J.T)==s.zeros(4)
    TT=s.Matrix([[s.trace(b) for b in Bs]]+[[sum(k[a]*b[a,j] for a in range(3)) for b in Bs] for j in range(3)])
    assert len(TT.nullspace())==2
    return dict(status='PASS',
        action='Quadratic Fierz-Pauli action of a supplied flat4D geometry, restricted to finite Fourier modes. E(h)=k^2 h-k(k^T h)-(h k)k^T+kk^T trh-I(k^2 trh-k^T h k). K in the orthonormal symmetric-tensor basis; gauge map Gxi=kxi^T+xik^T.',
        exact_Ward={'K_rank':6,'G_rank':4,'KG':0},
        blocking='Separate four exact gauge directions and six complementary coordinates; eliminate three nondegenerate normal coordinates by stationarity. Kcoarse=Kkk-Kki Kii^-1 Kik retains all four gauge nulls, rank3 on seven retained coordinates. Euclidean conformal directions need not be positive; this is stationary Gaussian elimination.',
        retained_indices=keep,eliminated_indices=list(chosen),coarse_matrix=blocked.tolist(),
        linear_ADM='C0=k_i k_j h_ij-k^2 trh; Ci=-2 k_j pi_ij. The canonical four-constraint matrix has rank4 and exactly zero mutual Poisson brackets. Twelve canonical phase coordinates minus eight gauge/constraint coordinates leave four physical phase coordinates: two polarizations.',
        transverse_traceless_basis=[v.tolist() for v in TT.nullspace()],
        boundary='Exact linearized constraint-preserving coarse action, not a perfect nonlinear W33 gravitational action. Fourier modes and flat4D geometry are supplied; position-space spectral derivatives are nonlocal. Mode-wise Ward closure does not establish the nonlinear hypersurface-deformation algebra, interacting coarse locality, quantum measure or Newton scale. Prior11430 curved Regge slice is not silently upgraded.')


def four_form_response(scalar_result):
    D=s.Matrix(top_boundary());assert D.rank()==2 and D*s.ones(3,1)==s.zeros(D.rows,1)
    betti=[1,82,162,82,1];chi=sum((-1)**i*b for i,b in enumerate(betti));assert chi==0
    K,m,a1,a2=s.symbols('K m a1 a2',positive=True)
    vac=a1*m**6/K+a2*m**8/K**2
    residual=s.factor(-K*s.diff(vac,K)/2)
    assert s.expand(residual-(a1*m**6/(2*K)+a2*m**8/K**2))==0
    lam,c,Q,mu=s.symbols('Lambda C Q mu',real=True)
    linear=s.expand(Q*(lam-c)/mu-Q*lam/mu)
    nonlinear=s.exp(lam-c)-s.exp(lam)
    assert s.diff(linear,lam)==0 and s.diff(nonlinear,lam)!=0
    masses=scalar_result['mass_groups_numeric']
    scalar4=sum(x['multiplicity']*x['mass_squared']**2 for x in masses)
    vector_m2=[(1.,12),(6.,6),(3.,12),(2.,2),(10.,1)]
    vector4=sum(n*z*z for z,n in vector_m2);assert vector4==444
    cw=(sum(n['multiplicity']*n['mass_squared']**2*(np.log(n['mass_squared'])-1.5) for n in masses)+3*sum(n*z*z*(np.log(z)-5/6) for z,n in vector_m2))/(64*np.pi**2)
    return dict(status='PASS',
        history='Reuse11284: M4=(#81 S1xS2)xS1, Betti(1,82,162,82,1), Euler0 and H4=Z. Cellular D4 rank2 on three top cells. No new topology is claimed.',
        prior_Einstein_obstruction='11317 already proves that this particular history has no smooth closed Riemannian Einstein metric: Euler0 would force flatness, contradicting b1=82>4. The GB-flux equation below adds a constraint/measure compatibility test; it does not rediscover or evade that theorem.',
        graviton_remainder=str(residual),
        Euler_flux_obstruction='For closed oriented Riemannian M4, integral GB=32pi^2 chi=0. A Gauss-Bonnet-conjugate four-form equation integralGB+hat_sigma_prime Qhat=0 forces Qhat=0 when hat_sigma_prime is nonzero. The old nonzero curvature-conjugate flux cannot be transplanted unchanged into the GB-conjugate model on this history.',
        quantum_zero_mode='For linear hat_sigma, integrating the rigid theta with a flat Fourier measure gives2pi delta(32pi^2 chi+Qhat). Thus a fixed nonzero Qhat sector has no support on this closed history. This is a finite/global measure constraint, not a gravity path integral construction.',
        compact_topological_measure='A separate declared compact-angle sector has Ztop=(1/2pi) integral_0^2pi dtheta exp[i theta(chi+n)]=Kronecker_delta(chi+n,0), with normalized Euler coupling and integer four-form flux n. The identity-gluing history supports only n=0; a supplied round S4 supports n=-2. This removes the formal infinite theta-volume in the zero sector, but is an added topological measure, not a derived gravitational path integral or the standard real-theta sequester.',
        round_sphere_escape='For the distinct supplied round Euclidean S4, chi=2, integralGB=64pi^2, Vol=8pi^2 r^4/3 and R=12/r^2. If the separate volume-flux constraint sets Vol=Q/mu4, the homogeneous residual obeys DeltaLambda^2=24pi^2 K^2 mu4/Q. Q and its sector remain inputs, so this is not a predicted CC or native Lorentzian universe. Prior11307 already owns a different spherical two-cap membrane saddle.',
        exact_shift_Ward='With linear sigma, a translation-invariant Lambda integration domain/measure lets Lambda->Lambda-C remove a common matter constant, up to the field-independent topological phase exp(-i Q C/mu4). Normalized invariant insertions are unchanged, if the formal integral is consistently defined. Nonlinear sigma has Lambda-dependent shift and lacks this exact fixed-sector identity.',
        linear_shift=str(linear),nonlinear_shift=str(nonlinear),
        actual_stable_scalar_gauge_threshold={'physical_scalars':264,'massive_vectors':33,'massless_vectors':12,'scalar_sum_m4_exact':'117157/2','Str_m4_exact':'119821/2','scalar_sum_m4_numeric':scalar4,'vector_sum_m4_exact':vector4,'Str_m4_numeric':scalar4+3*vector4,'CW_MS_Landau_mu1_numeric':float(cw),'running_mu_dVdmu_exact':'-119821/(64pi^2)','running_mu_dVdmu':float(-(scalar4+3*vector4)/(32*np.pi**2))},
        boundary='Known Gauss-Bonnet sequestering is credited to Kaloper-Padilla. The topology/measure compatibility test and concrete297-field threshold are interfaces, not all-loop native quantum gravity, selected flux/CC, Lorentzian Euler positivity, stable loop-corrected scalar vacuum or a regulator-independent finite mass prediction. Compact theta and integer flux are added global data; instanton/flux-transition protection is not proved. Nonlinear sigma used for standard radiative-stability arguments must not be called the exact linear fixed-flux Ward identity.')


def produce():
    data=dict(status='PASS',passes=list(range(11620,11625)),reservation=RESERVATION)
    for name,fn in [('covariant_pair',covariant_pair),('scalar_vacuum',scalar_vacuum),('shared_flavor',shared_flavor),('gravitational_block',gravitational_block)]:
        data[name]=fn();print(name,'PASS',flush=True)
    data['four_form_response']=four_form_response(data['scalar_vacuum']);print('four_form_response PASS',flush=True)
    files=['analysis/w33_pass11615_11619_parent_pairs_constraints.py','data/w33_pass11615_11619_parent_pairs_constraints.json','analysis/w33_pass11600_dynamical_hesse_flavor.py','analysis/w33_pass11284_closed_history_flux.py','data/w33_pass11284_closed_history_flux.json','data/w33_pass11317_history_einstein_obstruction.json','analysis/w33_pass11306_relational_graph_clock_constraints.py','analysis/PASS11313_11319_PORTAL_BARRIERS_RADIATIVE_SCALE_AND_GEOMETRY.md','analysis/PASS11428_11432_NATIVE_ALIGNMENT_MEASURE_COARSE_FLAGS.md']
    data['source_sha256']={p:ph(ROOT/p) for p in files};data['producer_sha256']=ph(Path(__file__))
    OUT.write_text(json.dumps(data,indent=2,default=str)+'\n')
    return data


if __name__=='__main__':produce()
