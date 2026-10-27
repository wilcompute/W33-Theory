"""Named native operators and explicit limitations, after e674c9a82.

Owners: Oct27 microscopic_response_and_lifts; Round12 classical Albert maps;
Round13 anomalies; TOE68/Pass11984 overlap controls; Pass12330 running inputs.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from functools import lru_cache
import hashlib,json,re,sys
import numpy as np
import sympy as s
from scipy.linalg import eigh, expm
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).resolve().parent))
import w33_20261027_microscopic_response_and_lifts as old
from w33_20261014_toe68_overlap_control import GAMMA,G5
ROOT=Path(__file__).resolve().parents[1]


@lru_cache(None)
def geometry():
    B,V,edges,*_=old.prior.inputs()
    b=B[:,1:];h=V-b@np.linalg.solve(b.T@b,b.T@V)
    return B,V,edges,h


def reflection_selection_probe():
    B,V,edges,h=geometry();r=old.reflection_lift();emap=r['edge_map']
    e=next(i for i,(j,sg) in enumerate(emap)if j!=i);f=emap[e][0]
    K=np.zeros((27,27));X=np.zeros_like(K)
    for a,b in edges:K[a,b]=K[b,a]=-1
    for j,weight in ((e,1),(f,-1)):
        a,b=edges[j];X[a,b]=X[b,a]=weight
    perm=r['vertex_permutation'];assert np.array_equal(K[np.ix_(perm,perm)],K)
    assert np.array_equal(X[np.ix_(perm,perm)],-X)
    L=s.Matrix(K.astype(int))+10*s.eye(27);J=s.ones(27)/27
    inverse=(L+J).inv()-J;v=s.Matrix(X.astype(int))*s.ones(27,1)
    curvature=-s.Rational(2,27)*(v.T*inverse*v)[0]
    assert curvature<0
    ev,U=eigh(K);vertex=U.T@X@U;gap=ev[:,None]-ev[None,:];samples=[]
    for T in (.25,1.,2.):
        occ=1/(1+np.exp(ev/T));diff=occ[:,None]-occ[None,:]
        mask=abs(gap)>1e-10;w=np.zeros_like(gap);w[mask]=diff[mask]/gap[mask]
        deg=-(occ*(1-occ))[:,None]/T;w[~mask]=np.broadcast_to(deg,w.shape)[~mask]
        second=float(np.sum(w*abs(vertex)**2))
        assert second<0
        samples.append(dict(T=T,fermion_free_energy_second_derivative=second,
                            required_bare_positive_stiffness_greater_than=-second))
    # A scale-free circle Casimir potential per3D spatial volume is C/R^4.
    R,C=s.symbols('R C',positive=True)
    assert s.diff(C/R**4,R)==-4*C/R**5
    return dict(odd_edge_pair=[e,f],exact_one_particle_ground_curvature=str(curvature),
                thermal_samples=samples,
                reason='Free energy is concave in a linear Hermitian hopping deformation. The reflection-odd deformation makes the symmetric point stationary, but the tested determinant has negative curvature there.',
                radius_result='A massless scale-free circle Casimir term is C/R^4: no finite stationary radius for nonzero C, and a flat radius if C=0. Imposing reflection changes coefficients, not this homogeneity.',
                scope='Specific selection mechanisms fail. A positive bare stiffness or new massive/dynamical sector could change this; neither its sign nor a physical scale is derived. Casimir homogeneity is standard continuum prior art, not a native quantum-gravity result.')


def interacting_native_cell(U=2.):
    """Exact sector with one up and one down fermion on ALL27 native sites.

    Interaction is supplied U sum_v n_up(v)n_down(v). All135 current vertices
    are retained. This is an external-gauge-field response, not dynamic gauge ED.
    """
    B,V,edges,h=geometry();K=np.zeros((27,27))
    for a,b in edges:K[a,b]=K[b,a]=-1
    I=np.eye(27);H=np.kron(K,I)+np.kron(I,K)
    H[np.arange(0,729,28),np.arange(0,729,28)]+=U
    ev,Q=eigh(H);psi=Q[:,0];delta=ev[1:]-ev[0]
    assert delta[0]>1
    Jpsi=[];diamag=[]
    for a,b in edges:
        j=np.zeros((27,27),complex);j[b,a]=-1j;j[a,b]=1j
        d=np.zeros((27,27));d[a,b]=d[b,a]=1
        # Avoid constructing135 large tensor matrices: act on a27x27 wavefunction.
        P=psi.reshape(27,27)
        Jpsi.append((j@P+P@j.T).ravel())
        diamag.append(float(np.vdot(psi,(d@P+P@d.T).ravel()).real))
    Jpsi=np.array(Jpsi).T;Jexc=Q[:,1:].T@Jpsi
    curvature=np.diag(diamag)-2*(Jexc.conj().T@(Jexc/delta[:,None])).real
    electric=2*(Jexc.conj().T@(Jexc/delta[:,None]**3)).real
    ward=float(np.max(abs(curvature@B)))
    assert ward<1e-10 and np.min(np.linalg.eigvalsh(electric))>-1e-10
    # An arbitrary finite vertex gauge transformation is implemented independently.
    chi=np.random.default_rng(27027).normal(size=27)
    Kg=K*np.exp(1j*(chi[:,None]-chi[None,:]))
    Hg=np.kron(Kg,I)+np.kron(I,Kg)
    Hg[np.arange(0,729,28),np.arange(0,729,28)]+=U
    gauge=np.exp(1j*(chi[:,None]+chi[None,:])).ravel()
    covariance=float(np.max(abs(Hg-gauge[:,None]*H*gauge[None,:].conjugate())))
    assert covariance<1e-12
    # The second derivative is also checked by a finite perturbation on one real link.
    a,b=edges[0];eps=.002
    def energy(t):
        kt=K.astype(complex).copy();kt[b,a]=-np.exp(1j*t);kt[a,b]=kt[b,a].conjugate()
        ht=np.kron(kt,I)+np.kron(I,kt);ht[np.arange(0,729,28),np.arange(0,729,28)]+=U
        return float(eigh(ht,subset_by_index=(0,0),eigvals_only=True)[0])
    fd=(energy(eps)+energy(-eps)-2*ev[0])/eps**2
    assert abs(fd-curvature[0,0])<1e-6
    compressed=h.T@curvature@h
    return dict(U=U,sites=27,links=135,particles='one up plus one down',dimension=729,
                ground_energy=float(ev[0]),gap=float(delta[0]),
                double_occupancy=float(np.sum(psi[np.arange(0,729,28)]**2)),
                static_link_kernel=curvature.tolist(),regular_electric_link_kernel=electric.tolist(),
                static_Ward_max_error=ward,gauge_covariance_max_error=covariance,
                independent_edge_finite_difference_error=float(abs(fd-curvature[0,0])),
                period_twist_stiffness=compressed.tolist(),
                static_kernel_smallest_eigenvalue=float(np.linalg.eigvalsh(curvature)[0]),
                scope='Interacting finite-cell ground-state response in a fixed two-particle sector. The cell has periodic boundary identification; arbitrary infinite-cover matter modes, all Fock sectors, continuum Maxwell dynamics and Qpsi/chiral matter are not included. The period-twist stiffness is not the six commutator metric.')


def su5_terms():
    pairs=list(combinations(range(5),2));ti={p:i for i,p in enumerate(pairs)};terms=[]
    # target order: antisymmetric t10, p_bar5, z1, u5, v_bar5, S1.
    for i in range(5):
        terms.extend([((26,16+i,21+i),1),((15,10+i,16+i),1)])
    for i,j in pairs:
        terms.extend([((ti[i,j],10+i,21+j),1),((ti[i,j],10+j,21+i),-1)])
    for i in range(5):
        a,b,c,d=[j for j in range(5)if j!=i]
        for j,k,l,m,sg in ((a,b,c,d,1),(a,c,b,d,-1),(a,d,b,c,1)):
            terms.append(((ti[j,k],ti[l,m],16+i),(-1)**i*sg))
    return {tuple(sorted(t)):sg for t,sg in terms}


def su5_lie(X):
    pairs=list(combinations(range(5),2));T=np.zeros((27,27),int)
    for col,(a,b) in enumerate(pairs):
        for j in range(5):
            for term,coef in (((j,b),X[j,a]),((a,j),X[j,b])):
                if term[0]==term[1]or not coef:continue
                sign=1 if term[0]<term[1]else -1
                T[pairs.index(tuple(sorted(term))),col]+=sign*coef
    T[10:15,10:15]=-X.T;T[16:21,16:21]=X;T[21:26,21:26]=-X.T
    return T


@lru_cache(None)
def canonical_cubic_intertwiner():
    path=ROOT/'artifacts/canonical_su3_gauge_and_cubic.json';raw=path.read_bytes()
    src={tuple(x['triple']):int(x['sign'])for x in json.loads(raw)['solution']['d_triples']}
    target=su5_terms()
    perm=[26,0,6,5,12,4,13,14,10,15,3,2,9,1,8,7,11,17,23,24,25,21,16,20,19,18,22]
    bits=[0,0,1,1,0,1,1,1,0,1,1,0,1,1,0,0,0,1,0,1,0,1,0,0,0,0,0]
    S=np.zeros((27,27),int)
    for i,j in enumerate(perm):S[j,i]=(-1)**bits[i]
    mapped={tuple(sorted(perm[i]for i in t)):sg*(-1)**sum(bits[i]for i in t)for t,sg in src.items()}
    assert mapped==target and np.array_equal(S.T@S,np.eye(27,dtype=int))
    gens=[]
    for a,b in product(range(5),repeat=2):
        if a==b:continue
        X=np.zeros((5,5),int);X[a,b]=1;gens.append(su5_lie(X))
    for a in range(4):
        X=np.zeros((5,5),int);X[a,a]=1;X[a+1,a+1]=-1;gens.append(su5_lie(X))
    chi=np.array([1]*10+[-3]*5+[5]+[-2]*5+[2]*5+[0]);psi=np.array([1]*16+[-2]*10+[4])
    gens.extend((np.diag(chi),np.diag(psi)))
    for X in gens:
        derivative=Counter()
        for term,coef in target.items():
            for axis,i in enumerate(term):
                for j in np.flatnonzero(X[i]):
                    word=list(term);word[axis]=int(j)
                    derivative[tuple(sorted(word))]+=coef*int(X[i,j])
        assert not any(derivative.values())
    qold=old.prior.matter_interface()['internal_Qpsi']
    assert np.array_equal(np.diag(S.T@np.diag(psi)@S),qold)
    return dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),
                target_coordinate_order='t10,p_bar5,z,u5,v_bar5,S',
                canonical_to_SU5_signed_permutation=S.tolist(),permutation=perm,sign_bits=bits,
                coefficientwise45_term_identity=True,all26_infinitesimal_generators_preserve_cubic=True,
                canonical_Qpsi_matches_previous_anchor0=True,
                target_cubic=[dict(indices=list(t),coefficient=v)for t,v in target.items()],
                scope='An explicit algebraic, unitary signed-permutation bridge from the actual canonical signed cubic to the supplied SU5/two-U1 basis. This removes the previous missing cubic-intertwiner boundary. It does not identify spatial and internal27 carriers or derive a chiral vacuum.')


def wilson_kernel(links,k=None,rho=1.,match_gauge_metric=False):
    B,V,edges,h=geometry();nc=links.shape[1];stride=4*nc
    if match_gauge_metric:
        G=h.T@h/27;ev,frame=eigh(G)
        h=h@(frame@np.diag(ev**-.5)@frame.T)
    DW=5*np.eye(27*stride,dtype=complex)
    for e,(a,b) in enumerate(edges):
        phase=1 if k is None else np.exp(1j*V[e]@k)
        direction=sum(h[e,mu]*GAMMA[mu]for mu in range(4))
        forward=np.kron(-.5*np.eye(4)+.5*direction,links[e]*phase)
        backward=np.kron(-.5*np.eye(4)-.5*direction,links[e].conj().T*phase.conjugate()if isinstance(phase,complex)else links[e].conj().T)
        aa=slice(a*stride,(a+1)*stride);bb=slice(b*stride,(b+1)*stride)
        DW[bb,aa]+=forward;DW[aa,bb]+=backward
    gamma=np.kron(np.eye(27),np.kron(G5,np.eye(nc)))
    HW=gamma@(DW-rho*np.eye(len(DW)))
    assert np.max(abs(HW-HW.conj().T))<1e-11
    return HW,gamma


def overlap_diagnostics(links,k=None,match_gauge_metric=False):
    H,gamma=wilson_kernel(links,k,match_gauge_metric=match_gauge_metric);ev,U=eigh(H);gap=float(min(abs(ev)))
    assert gap>1e-5
    sign=(U*np.sign(ev))@U.conj().T;D=np.eye(len(H))+gamma@sign
    hat=-sign;P=(np.eye(len(H))-hat)/2;Pbar=(np.eye(len(H))+gamma)/2
    GW=gamma@D+D@gamma-D@gamma@D
    intertwine=D@P-Pbar@D
    return dict(dimension=len(H),hermitian_kernel_gap=gap,index=int(round(-np.sign(ev).sum()/2)),
                GW_error=float(np.max(abs(GW))),projector_error=float(np.max(abs(P@P-P))),
                Weyl_intertwining_error=float(np.max(abs(intertwine))),
                near_zero_D_singular_values=int(np.count_nonzero(np.linalg.svd(D,compute_uv=False)<1e-8)))


def native_overlap_regulator():
    free=np.ones((135,1,1),complex)
    runs=[dict(k=k,diagnostics=overlap_diagnostics(free,np.array(k)))for k in ([0,0,0,0],[.07,.11,-.13,.17])]
    assert runs[0]['diagnostics']['near_zero_D_singular_values']==4
    corners=[]
    for binary in product((0,1),repeat=4):
        k=np.pi*np.array(binary);rec=overlap_diagnostics(free,k)
        corners.append(dict(binary_corner=list(binary),diagnostics=rec))
        assert rec['near_zero_D_singular_values']==(4 if not any(binary)else 0)
    random_gaps=[]
    for k in np.random.default_rng(827).uniform(-np.pi,np.pi,(48,4)):
        H,_=wilson_kernel(free,k);ev=eigh(H,eigvals_only=True)
        random_gaps.append(dict(k=k.tolist(),gap=float(min(abs(ev)))))
    # h^T V/27=G. The raw delta_ab Clifford frame gives G^2, not G.
    G=s.Matrix(old.prior.inputs()[-1])/27
    coframe_controls=[]
    for matched in (False,True):
        for eps in (.002,.001):
            k=eps*np.array([1.,0,0,0]);H,gamma=wilson_kernel(free,k,match_gauge_metric=matched)
            ev,U=eigh(H);D=np.eye(108)+gamma@((U*np.sign(ev))@U.conj().T)
            low=np.sort(np.linalg.svd(D,compute_uv=False))[:4]/eps
            target=float(s.sqrt(G[0,0]if matched else (G*G)[0,0]))
            coframe_controls.append(dict(metric_matched=matched,eps=eps,four_low_singular_values_over_eps=low.tolist(),target=target))
    rng=np.random.default_rng(271028);links=[]
    for e in range(135):
        X=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5));X+=X.conj().T;X-=np.trace(X)*np.eye(5)/5
        links.append(expm(.015j*X))
    links=np.array(links)
    irreps={
        '5':links,'bar5':links.conj(),
        '10':np.array([old.wedge2(U)for U in links]),
    }
    irrep_runs={name:overlap_diagnostics(U)for name,U in irreps.items()}
    for rec in irrep_runs.values():
        assert rec['GW_error']<1e-10 and rec['Weyl_intertwining_error']<1e-10
    # Rebuild a kernel from independently transformed nonabelian links.
    frames=[]
    for v in range(27):
        X=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5));X+=X.conj().T;X-=np.trace(X)*np.eye(5)/5
        frames.append(expm(.11j*X))
    frames=np.array(frames);edges=geometry()[2]
    transformed=np.array([frames[b]@links[e]@frames[a].conj().T for e,(a,b)in enumerate(edges)])
    H,_=wilson_kernel(links);Hg,_=wilson_kernel(transformed)
    G=np.zeros_like(H)
    for v in range(27):G[20*v:20*(v+1),20*v:20*(v+1)]=np.kron(np.eye(4),frames[v])
    covariance=float(np.max(abs(Hg-G@H@G.conj().T)));assert covariance<1e-11
    return dict(spin_choice='Supply four Euclidean Clifford gamma matrices; h is the harmonic representative of the actual four deck voltages.',
                kernel='DW=one_half graph_Laplacian + gamma dot antisymmetric harmonic-edge derivative; HW=gamma5(DW-1); Dov=1+gamma5 sign(HW)',
                free_controls=runs,corner_controls=corners,random_momentum_kernel_gaps=random_gaps,
                bare_Clifford_principal_cometric=[[str(x)for x in row]for row in (G*G).tolist()],
                matched_Clifford_frame='Supply gamma^a with anticommutator2(G^-1)^ab, equivalently h -> h G^-1/2. Then the leading Dirac square has cometricG, matching the earlier engineered gauge symbol.',
                coframe_controls=coframe_controls,
                nonabelian_irrep_controls=irrep_runs,kernel_gauge_covariance_error=covariance,
                canonical_internal_representation='Transport10+bar5+1+5+bar5+1 block operators by the exact cubic signed permutation.',
                scope='An actual finite native-cell gauge-covariant overlap operator and Weyl projectors, with a supplied Euclidean spin structure. All tested backgrounds are topologically trivial. No uniform locality/gap theorem, full Brillouin-zone species count, globally integrable fermion measure, interacting chiral gauge dynamics, reflection compactification or physical3+1 spacetime has been derived.')


def split_thresholds():
    # Exact contributions recovered from the same full field ledger as Pass12330.
    path=ROOT/'analysis/search_drivers_12281/bro/Z6II_60_SM_20260917_810_v9__w6odd.nsoq'
    sys.path.insert(0,str(ROOT/'analysis/search_drivers_12286'))
    from lr_hypercharge import solve,fermions
    c,eq,sol=solve(fermions(path));ss=sol[0]
    free=sorted((set(c)-set(ss))|{z for v in ss.values()for z in s.sympify(v).free_symbols},key=str)
    cv=[s.sympify(ss.get(ci,ci)).subs(free[0],s.Rational(-1,148))for ci in c]
    totals={19:s.zeros(3,1),15:s.zeros(3,1),16:s.zeros(3,1)}
    for line in path.read_text().splitlines():
        m=re.match(r'FIELD \d+ m=(\S+) k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*) q=(\S*)',line)
        if not m or int(m[1])not in totals:continue
        kind=int(m[1]);d=[abs(int(re.match(r'-?\d+',x)[0]))for x in m[2].split(',')]
        q=[s.nsimplify(float(x),tolerance=1e-9,rational=True)for x in m[3].split(',')if x]
        y=sum(a*b for a,b in zip(cv,q));d3,dl,dr,dh=d
        t3={1:0,3:s.Rational(1,2),8:3}[d3];t2={1:0,2:s.Rational(1,2),3:2}[dl]
        tr=[s.Rational(1,2),-s.Rational(1,2)]if dr==2 else[0]
        totals[kind]+=s.Matrix([t3*dl*dr*dh,t2*d3*dr*dh,sum((y+z)**2 for z in tr)*d3*dl*dh])
    W=s.Rational(2,3)*totals[19];Sc=(totals[15]+totals[16])/6
    dw=W-s.Matrix([4,4,s.Rational(20,3)]);ds=Sc-s.Matrix([0,s.Rational(1,6),s.Rational(1,6)])
    full=s.Matrix([-11,-s.Rational(22,3),0])+W+Sc
    assert full==s.Matrix([7,16,s.Rational(148,3)])
    A=s.Matrix([1/s.Rational('.1180'),s.Rational('127.95')*s.Rational('.2312'),s.Rational('127.95')*(1-s.Rational('.2312'))])
    # variables y=log(Mcross/MZ)/2pi, f=log(MF/MZ)/2pi, t=log(MS/MZ)/2pi
    y,f,t=s.symbols('y f t');inv=A-full*y+dw*f+ds*t;k=s.Rational(8,3)
    mat,rhs=s.linear_eq_to_matrix([inv[1]-inv[0],inv[2]-k*inv[1]],(y,f,t))
    lower=np.log(1e3/91.1876)/(2*np.pi);upper=np.log(1e16/91.1876)/(2*np.pi);yc=np.log(1e19/91.1876)/(2*np.pi)
    aub=np.array([[-1,1,0],[-1,0,1]],float);bub=np.zeros(2)
    # alpha2^-1>=1 is an explicit perturbative-domain control.
    coeff=np.array([inv[1].coeff(z)for z in (y,f,t)],float)
    aub=np.vstack((aub,-coeff));bub=np.r_[bub,float(A[1]-1)]
    result=linprog(np.zeros(3),A_ub=aub,b_ub=bub,A_eq=np.array(mat,float),b_eq=np.array(rhs,float).ravel(),
                   bounds=[(lower,yc),(lower,upper),(lower,upper)],method='highs')
    record=dict(feasible=bool(result.success),solver_message=result.message,
                full_Weyl_contributions=list(map(str,W)),full_scalar_contributions=list(map(str,Sc)),
                excess_Weyl=list(map(str,dw)),excess_scalar=list(map(str,ds)),
                threshold_range_GeV=[1e3,1e16],maximum_crossing_GeV=1e19,
                source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    # Independent analytic exclusion: tauF=y-f>=0 is the amount of running
    # above the excess-Weyl threshold. Solve both matching equations exactly.
    tau=s.Symbol('tauF',nonnegative=True)
    exact_solution=s.solve([v.subs(f,y-tau)for v in (inv[1]-inv[0],inv[2]-k*inv[1])],(y,t),dict=True)[0]
    yy=s.expand(exact_solution[y]);tt=s.expand(exact_solution[t])
    assert yy.coeff(tau)==-s.Rational(62,1801) and tt.coeff(tau)==s.Rational(152,1801)
    # MF>=MZ means f=y-tau>=0, bounding tau with exact rational inputs.
    taumax=s.solve(yy-tau,tau)[0];tmax=tt.subs(tau,taumax)
    exponent_upper=2*s.Rational(22,7)*tmax # pi<22/7
    N=40
    exp_upper=sum(exponent_upper**j/s.factorial(j)for j in range(N+1))
    exp_upper+=exponent_upper**(N+1)/s.factorial(N+1)/(1-exponent_upper/(N+2))
    mass_upper=s.Rational('91.1876')*exp_upper
    assert exponent_upper<N+2 and mass_upper<1000
    record['exact_analytic_exclusion']=dict(
        variable='tauF=log(Mcross/MF)/(2pi)>=0',crossing_log_y=str(yy),scalar_threshold_log_t=str(tt),
        tauF_upper_if_MF_at_least_MZ=str(taumax),scalar_threshold_log_upper=str(tmax),
        exact_rational_scalar_mass_upper=str(mass_upper),scalar_mass_upper_GeV=float(mass_upper),
        proof='MF>=MZ bounds tauF by y. The exact affine matching solution bounds tS. Using pi<22/7 and a40-term Taylor sum with geometric remainder bounds MS strictly below1TeV. Thus both excess-category thresholds cannot be above1TeV under this running model, independently of the LP.')
    if result.success:
        # Keep one exact rational free parameter, then solve both matches exactly.
        ff=s.Rational(str(float(result.x[1]))).limit_denominator(10**6)
        solution=s.solve([inv[1]-inv[0],inv[2]-k*inv[1],f-ff],(y,f,t),dict=True)[0]
        exact=[solution[z]for z in (y,f,t)];aval=[s.simplify(v.subs(solution))for v in inv]
        assert aval[0]==aval[1]and aval[2]==k*aval[1]and aval[1]>1
        vals=np.array(list(map(float,exact)))
        assert np.max(aub@vals-bub)<1e-7 and vals[0]>=max(vals[1:])-1e-7
        record.update(exact_log_variables=list(map(str,exact)),exact_inverse_couplings=list(map(str,aval)),
                      scales_GeV=(91.1876*np.exp(2*np.pi*vals)).tolist())
    record['scope']='Supplied two-category split-threshold one-loop fit using the frozen candidate spectrum, keeping the SM baseline light and splitting excess Weyl/scalar masses. No mass mechanism, full left-right matching or two-loop string threshold derived; feasibility does not rescue the physical vacuum.'
    return record


def run():
    return dict(reflection_selection=reflection_selection_probe(),
                interacting_cell=[interacting_native_cell(U)for U in (0.,2.,8.)],
                canonical_cubic_intertwiner=canonical_cubic_intertwiner(),
                native_overlap=native_overlap_regulator(),split_thresholds=split_thresholds())


if __name__=='__main__':
    result=run();out=ROOT/'data/w33_20261027_native_operator_closure.json'
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:'computed'for k in result}))
