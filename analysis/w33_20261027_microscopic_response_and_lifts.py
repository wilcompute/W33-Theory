"""Explicit continuations; all supplied model choices are recorded in the report.

Prior owners: Oct27 five_front_followthrough, TOE62 three-loop matter,
Pass11984 native_fiber_overlap and Round13 chiral_anomaly_27. No TOE claim.
"""
from collections import Counter
from itertools import product, combinations
from pathlib import Path
import json
import sys
import numpy as np
import sympy as s
from scipy.linalg import expm, eigvalsh
from scipy.special import expit
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import eigsh
sys.path.insert(0, str(Path(__file__).resolve().parent))
import w33_20261027_five_front_followthrough as prior
ROOT = Path(__file__).resolve().parents[1]


def fermion_vertices(phi, charge=1):
    C, B, keys, endpoints = prior.lifted_patch()
    dual = C.T @ np.linalg.inv(C @ C.T)
    K = np.zeros((B.shape[1], B.shape[1]), complex)
    J = np.zeros((2, *K.shape), complex)
    D = np.zeros((2, 2, *K.shape), complex)
    for e, row in enumerate(B):
        a = int(np.flatnonzero(row < 0)[0]); b = int(np.flatnonzero(row > 0)[0])
        K[b,a] = -np.exp(1j*charge*(dual[e] @ phi)); K[a,b] = K[b,a].conjugate()
        for i in range(2):
            J[i,b,a] = 1j*charge*dual[e,i]*K[b,a]; J[i,a,b] = J[i,b,a].conjugate()
            for j in range(2):
                D[i,j,b,a] = -charge**2*dual[e,i]*dual[e,j]*K[b,a]
                D[i,j,a,b] = D[i,j,b,a].conjugate()
    return K, J, D


def polarization(T=1., nu=0., mu=0.):
    """Real symmetric Euclidean current kernel of ONE microscopic determinant.

    At nu=0 includes thermal degenerate terms. Nonzero nu is the spectral
    continuation of the Matsubara kernel; only nu=2*pi*n*T is thermal data.
    """
    result = np.zeros((2,2))
    for q, mult in ((1,16),(-2,10),(4,1)):
        K,J,D = fermion_vertices(np.array([2*np.pi/3,4*np.pi/3]),q)
        ev,U = np.linalg.eigh(K)
        if T==0:
            assert np.min(abs(ev-mu))>1e-6
            occ=(ev<mu).astype(float)
        else:occ=expit((mu-ev)/T)
        gap = ev[:,None]-ev[None,:]; diff = occ[:,None]-occ[None,:]
        weight = np.zeros_like(gap); mask = abs(gap)>1e-9
        weight[mask] = diff[mask]*gap[mask]/(gap[mask]**2+nu**2)
        if nu == 0 and T>0:
            degenerate = -((occ*(1-occ))[:,None]+(occ*(1-occ))[None,:])/(2*T)
            weight[~mask] = degenerate[~mask]
        vertices = np.array([U.conj().T@x@U for x in J])
        for i,j in product(range(2),repeat=2):
            diamagnetic = np.sum(occ*np.diag(U.conj().T@D[i,j]@U)).real
            bubble = np.sum(weight*vertices[i]*vertices[j].T).real
            result[i,j] += mult*(diamagnetic+bubble)
    return result


def temporal_determinant_control(T=1., slices=24, epsilon=.002):
    """Exact finite time-step covariance; transfer factors from same hopping K.

    Slice temporal link W_t maps frame t to t+1. Factors L_t=W_t exp(-dt K_t)
    transform as G_(t+1) L_t G_t^-1. Their cyclic product is conjugated.
    """
    beta=1/T; dt=beta/slices; nv=19
    rng=np.random.default_rng(20261027)
    frames=np.exp(1j*rng.normal(size=(slices,nv)))
    phi=np.array([2*np.pi/3,4*np.pi/3])
    def determinant(amplitude, direction, gauge=False):
        P=np.eye(nv,dtype=complex)
        for t in range(slices):
            K,_,_=fermion_vertices(phi+amplitude*np.cos(2*np.pi*t/slices)*direction)
            L=expm(-dt*K)
            if gauge:
                # Equivalent to K'_t=G_t K_t G_t^-1 and W'_t=G_(t+1)G_t^-1.
                L=frames[(t+1)%slices,:,None]*L*frames[t,None,:].conjugate()
            P=L@P
        phase,logabs=np.linalg.slogdet(np.eye(nv)+P)
        return -T*logabs, phase
    original,phase=determinant(.07,np.array([1.,-.4]))
    transformed,phase2=determinant(.07,np.array([1.,-.4]),True)
    error=abs(original-transformed)
    assert error<1e-10 and abs(phase-phase2)<1e-10
    base,_=determinant(0,np.array([1.,0.]))
    responses=[]
    for direction in (np.array([1.,0.]),np.array([0.,1.]),np.array([1.,1.])):
        plus,_=determinant(epsilon,direction); minus,_=determinant(-epsilon,direction)
        finite=2*(plus+minus-2*base)/epsilon**2
        # Only q=1 here. Central intertwiners imply sum multiplicity*q^2=72.
        target=float(direction@polarization(T,2*np.pi*T)@direction)/72
        responses.append(dict(direction=direction.tolist(),finite_time_kernel=finite,
                              continuous_time_spectral_kernel=target,error=abs(finite-target)))
    return dict(slices=slices,T=T,gauge_covariance_logdet_error=error,
                probes=responses,scope='Finite time-step determinant; temporal links transform explicitly. No continuum or physical speed inferred.')


def microscopic_response():
    rows=[]
    for T in (.25,1.,2.):
        B=polarization(T,0); samples=[]
        # Distinguish genuine Matsubara samples from a low-frequency analytic probe.
        for nu in (2*np.pi*T,4*np.pi*T,.02,.01):
            K=polarization(T,nu); inertia=(K-B)/nu**2
            samples.append(dict(nu=nu,matsubara=nu>.1,kernel=K.tolist(),
                                effective_inertia=inertia.tolist(),
                                inertia_eigenvalues=np.linalg.eigvalsh(inertia).tolist()))
        jump=np.zeros((2,2)); regular=np.zeros((2,2))
        for q,mult in ((1,16),(-2,10),(4,1)):
            K,J,D=fermion_vertices(np.array([2*np.pi/3,4*np.pi/3]),q)
            ev,U=np.linalg.eigh(K);occ=expit(-ev/T)
            gap=ev[:,None]-ev[None,:];diff=occ[:,None]-occ[None,:]
            mask=abs(gap)>1e-9; weights=np.zeros_like(gap)
            weights[mask]=-diff[mask]/gap[mask]**3
            degenerate=((occ*(1-occ))[:,None]+(occ*(1-occ))[None,:])/(2*T)
            degenerate[mask]=0
            JJ=np.array([U.conj().T@x@U for x in J])
            for i,j in product(range(2),repeat=2):
                jump[i,j]+=mult*np.sum(degenerate*JJ[i]*JJ[j].T).real
                regular[i,j]+=mult*np.sum(weights*JJ[i]*JJ[j].T).real
        rows.append(dict(T=T,static_curvature=B.tolist(),frequency_samples=samples,
                         thermal_zero_frequency_jump=jump.tolist(),
                         jump_eigenvalues=np.linalg.eigvalsh(jump).tolist(),
                         regular_inertia_after_subtracting_jump=regular.tolist()))
    zero_B=polarization(0,0,.1)
    zero_samples=[dict(nu=nu,inertia=((polarization(0,nu,.1)-zero_B)/nu**2).tolist())for nu in (.02,.01,.005)]
    return dict(action='S=sum_q,multiplicity bar(psi)[d_tau+i*q*a0+K_q(A)-mu]psi; Gamma=-sum mult Tr log',
                samples=rows,time_controls=[temporal_determinant_control(slices=n) for n in (24,48)],
                zero_temperature_gapped_filling=dict(mu=.1,static_curvature=zero_B.tolist(),
                                                       inertia_controls=zero_samples,
                                                       choice='Supplied chemical potential inside a finite single-particle spectral gap; this removes the thermal jump, not the metric-shape mismatch or missing continuum.'),
                scope='Electric and magnetic quadratic responses of one supplied spinless thermal hopping model. Small-nu continuation can be singular in a finite thermal degenerate system; it is not assumed to define a local Maxwell action. Spin, chirality, continuum, H0 selection and common limiting speed remain unproved.')


def reflection_lift():
    B,V,edges,loops,periods,comm,H,M=prior.inputs()
    F=np.array([[-1,0,0,0],[1,1,0,0],[-1,0,1,0],[0,0,0,1]],int)
    perm=[18,20,19,23,22,21,25,24,26,9,11,10,14,13,12,16,15,17,0,2,1,5,4,3,7,6,8]
    offsets=np.array([[0,0,0,0]]*3+[[-1,0,1,-1]]*3+[[-1,0,1,0]]*3+
                     [[0,0,0,0]]*3+[[-1,0,0,0]]*3+[[0,0,0,0]]*6+
                     [[0,0,-1,1]]*3+[[0,0,-1,0]]*3,int)
    lookup={edge:i for i,edge in enumerate(edges)}
    edge_map=[(lookup[tuple(sorted((perm[a],perm[b])))],1 if perm[a]<perm[b] else -1)for a,b in edges]
    image_volts=np.array([sg*V[e]for e,sg in edge_map])
    assert np.array_equal(image_volts,V@F+B@offsets)
    assert all(perm[perm[v]]==v for v in range(27)) and not (offsets@F+offsets[perm]).any()
    assert s.Matrix(F).T*M*s.Matrix(F)==M
    def image(face):return [(edge_map[e][0],sg*edge_map[e][1])for e,sg in face]
    payload=json.loads((ROOT/'data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json').read_text())
    faces=[f['boundary']for f in payload['independent_face_basis']]
    # Projected cycle supports distinguish equality of geometric faces from span.
    def key(face):
        row=np.zeros(135,int)
        for e,sg in face:row[e]+=sg
        if next(x for x in row if x)<0:row=-row
        return tuple(row)
    face_keys={key(f)for f in faces}; image_faces=[image(f)for f in faces]
    missing=sum(key(f)not in face_keys for f in image_faces)
    image_comm=[image(f)for f in comm]
    Hroot=np.linalg.cholesky(np.array(H,float)).T
    def operator(k,symmetric):
        fs=prior.prior.curl(faces,V,k);fc=Hroot@prior.prior.curl(comm,V,k)
        if not symmetric:return np.vstack((fs,fc))
        fi=prior.prior.curl(image_faces,V,k);ci=Hroot@prior.prior.curl(image_comm,V,k)
        return np.vstack((fs,fc,fi,ci))/np.sqrt(2)
    controls=[]
    for k in (np.array([.17,.31,-.23,.41]),np.array([.1,0,0,0])):
        record={'k':k.tolist()}
        for symmetric in (False,True):
            spectra=[]
            for momentum in (k,F@k):
                D=prior.prior.gradient(V,edges,momentum)
                _,ev=prior.prior.transverse(operator(momentum,symmetric),D);spectra.append(ev)
            error=float(np.max(abs(spectra[0]-spectra[1])))
            record['averaged_spectrum_error' if symmetric else 'original_spectrum_error']=error
            if symmetric:assert error<1e-10
        controls.append(record)
    acoustic=[]
    for t in (.02,.01,.005):
        direction=np.array([1.,2.,-1.,1.]); k=t*direction
        _,ev=prior.prior.transverse(operator(k,True),prior.prior.gradient(V,edges,k))
        acoustic.append(dict(t=t,three_soft_eigenvalues_over_t2=(ev[:3]/t**2).tolist(),
                             target_speed_squared=float(direction@np.array(M,float)@direction/27)))
    # Loop image closure follows exactly from edge voltage identity; no finite-cover approximation.
    assert all(not sum((sg*V[e]for e,sg in f),np.zeros(4,int)).any()for f in image_faces+image_comm)
    return dict(momentum_reflection=F.tolist(),deck_reflection=F.T.tolist(),
                vertex_permutation=perm,vertex_offsets=offsets.tolist(),
                edge_map=[[int(e),int(sg)]for e,sg in edge_map],
                exact_edge_voltage_identity=True,exact_involution_on_infinite_cover=True,
                selected105_faces_with_image_outside_selected_set=missing,
                repaired_action='Average the old quadratic action and its exact reflected image, with factor1/2. All translated copies are included.',
                spectral_controls=controls,acoustic_controls=acoustic,
                scope='An explicit infinite-cover graph and boundary-loop involution, and a supplied reflection-invariant averaged action. Original selected-face/coupling action is not invariant; averaging changes microscopic interactions. No dynamically chosen compact radius, chiral orbifold, or 3+1 theory derived.')


def lifted_patch(d=3,N=3):
    B,V,edges,loops,periods,comm,H,M=prior.inputs()
    dictionaries=[]
    for face in comm[:d]:
        cell=np.zeros(4,dtype=int); vertex=0; row=Counter()
        for e,sign in face:
            a,b=edges[e] if sign==1 else edges[e][::-1]
            assert vertex==a
            if sign<0:cell-=V[e]
            row[(tuple(map(int,cell%N)),e)]+=sign
            if sign>0:cell+=V[e]
            vertex=b
        assert vertex==0 and not cell.any()
        dictionaries.append({k:v for k,v in row.items() if v})
    keys=sorted(set().union(*dictionaries)); endpoints=[]; vertices=set()
    for cell,e in keys:
        a,b=edges[e];tail=(cell,a);head=(tuple(map(int,(np.array(cell)+V[e])%N)),b)
        endpoints.append((tail,head));vertices.update((tail,head))
    vid={v:i for i,v in enumerate(sorted(vertices))}; B=np.zeros((len(keys),len(vid)),int)
    for e,(a,b) in enumerate(endpoints):B[e,vid[a]]=-1;B[e,vid[b]]=1
    C=np.array([[row.get(k,0)for k in keys]for row in dictionaries],int)
    assert not (C@B).any() and np.linalg.matrix_rank(C)==d
    return C,B,keys


def cycle_lattice_index(C,B):
    order=[0]; tree=set()
    for v in order:
        for e in np.flatnonzero(B[:,v]):
            w=int(next(x for x in np.flatnonzero(B[e])if x!=v))
            if w not in order:order.append(w);tree.add(int(e))
    chords=[e for e in range(B.shape[0])if e not in tree]
    assert len(order)==B.shape[1] and len(chords)==C.shape[0]
    return abs(int(s.Matrix(C[:,chords]).det()))


def rotor(cutoff=3,g=1.,d=3):
    C,B,keys=lifted_patch(d)
    states=np.array(list(product(range(-cutoff,cutoff+1),repeat=d)),int)
    idx={tuple(x):i for i,x in enumerate(states)}; size=len(states)
    # Restrict the previously certified positive27-harmonic potential to f_rest=0.
    old=json.loads((ROOT/'data/w33_20261027_five_front_followthrough.json').read_text())
    harmonics={}
    for rec in old['compact_metric_completion']['harmonics']:
        q=tuple(rec['q'][:d])
        if not any(q):continue
        if next(x for x in q if x)<0:q=tuple(-x for x in q)
        harmonics[q]=harmonics.get(q,s.S.Zero)+s.Rational(rec['weight'])
    hessian=sum((w*s.Matrix(q)*s.Matrix(q).T for q,w in harmonics.items()),s.zeros(d))
    assert hessian==prior.inputs()[-2][:d,:d]
    E=states@C; assert not (E@B).any()
    diag=.5*g*g*np.sum(E*E,axis=1)+float(sum(harmonics.values()))/(g*g)
    rr=[];cc=[];vv=[]
    for q,w in harmonics.items():
        for i,x in enumerate(states):
            j=idx.get(tuple(x+q))
            if j is not None:rr.extend((i,j));cc.extend((j,i));vv.extend((-float(w)/(2*g*g),)*2)
    A=diags(diag)+coo_matrix((vv,(rr,cc)),shape=(size,size)).tocsr()
    ev,vec=eigsh(A,k=2,which='SA',tol=1e-11,v0=np.ones(size)); order=np.argsort(ev)
    psi=vec[:,order[0]]; energy=float(ev[order[0]])
    return dict(loops=d,cutoff=cutoff,g=g,dimension=size,vertices=B.shape[1],links=B.shape[0],
                graph_cycle_rank=B.shape[0]-B.shape[1]+1,retained_cycle_rank=d,
                integral_cycle_lattice_index=cycle_lattice_index(C,B),
                loop_Gram=(C@C.T).tolist(),ground_energy=energy,gap=float(np.diff(ev[order])[0]),
                residual_norm=float(np.linalg.norm(A@psi-energy*psi)),
                boundary_probability=float(np.sum(psi[np.any(abs(states)==cutoff,axis=1)]**2)),
                exact_Gauss=True,restricted_hessian=[[str(x)for x in row]for row in hessian.tolist()])


def compact_expansion():
    rows=[]
    for g in (.5,1.,2.):
        seq=[rotor(L,g) for L in ((2,3,4,5,6,7)if g==.5 else (2,3,4,5))]
        assert all(b['ground_energy']<=a['ground_energy']+1e-9 for a,b in zip(seq,seq[1:]))
        rows.append(dict(g=g,sequence=seq,last_energy_change=abs(seq[-1]['ground_energy']-seq[-2]['ground_energy'])))
    return dict(three_loop_sequences=rows,six_loop_controls=[rotor(L,1.,6)for L in (1,2)],
                prior='TOE62 already quantized three overlapping loops on a different Levi patch. This extends the Oct27 deck-commutator patch and its matched compact potential.',
                scope='Galerkin flux subspace; beta1 of the patch is reported separately from retained rank. No full graph dynamics, rigorous infinite-cutoff error, phase diagram or confinement claim.')


def wedge2(U):
    pairs=list(combinations(range(5),2))
    return np.array([[U[a,c]*U[b,d]-U[a,d]*U[b,c]for c,d in pairs]for a,b in pairs])


def nonabelian_interface():
    # Round13 sign convention for chi: 16=10_(1)+bar5_(-3)+1_(5).
    blocks=[('10',10,1,1),('bar5',5,-3,1),('1',1,5,1),
            ('5',5,-2,-2),('bar5',5,2,-2),('1',1,0,4)]
    x=s.symbols('x0:4'); a,b=s.symbols('a b'); cartan=list(x)+[-sum(x)]
    weights=[]
    for rep,dim,chi,psi in blocks:
        su=( [cartan[i]+cartan[j]for i,j in combinations(range(5),2)] if rep=='10'
            else cartan if rep=='5' else [-z for z in cartan] if rep=='bar5' else [0])
        assert len(su)==dim
        weights.extend(z+a*chi+b*psi for z in su)
    assert s.expand(sum(weights))==0
    cubic=s.Poly(s.expand(sum(z**3 for z in weights)),*x,a,b)
    assert cubic.is_zero
    rng=np.random.default_rng(271027)
    def group():
        z=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5)); H=z+z.conj().T
        H-=np.trace(H)*np.eye(5)/5
        return expm(.2j*H)
    def rep(U,chiangle=0.,psiangle=0.):
        out=np.zeros((27,27),complex);start=0
        for name,dim,chi,psi in blocks:
            A=wedge2(U) if name=='10' else U if name=='5' else U.conj() if name=='bar5' else np.ones((1,1))
            out[start:start+dim,start:start+dim]=A*np.exp(1j*(chi*chiangle+psi*psiangle));start+=dim
        return out
    U,V,Gv,Gw=group(),group(),group(),group()
    hom=float(np.max(abs(rep(U@V)-rep(U)@rep(V))))
    R=rep(U,.17,-.23);gv=rep(Gv,.31,.12);gw=rep(Gw,-.16,.27)
    pv=rng.normal(size=27)+1j*rng.normal(size=27);pw=rng.normal(size=27)+1j*rng.normal(size=27)
    old=np.vdot(pw,R@pv);new=np.vdot(gw@pw,(gw@R@gv.conj().T)@(gv@pv))
    covariance=float(abs(old-new));assert hom<1e-12 and covariance<1e-11
    # A bare Weyl mass requires qpsi_i+qpsi_j=0, absent in this complete27.
    charges=[psi for _,dim,chi,psi in blocks for _ in range(dim)]
    assert all(q+r!=0 for q,r in product(charges,repeat=2))
    subgroup=[int(z.subs(dict(zip(x,(1,-1,0,0)))|{a:0,b:0}))for z in weights]
    assert Counter(subgroup)==Counter({-1:6,0:15,1:6})
    return dict(branches=[dict(SU5=n,dimension=d,Qchi=c,Qpsi=p)for n,d,c,p in blocks],
                exact_Cartan_cubic_anomaly_polynomial=str(cubic.as_expr()),
                anomaly_reason='Every su5 Hermitian element is conjugate to a Cartan element. The identically vanishing trace of (X+a Qchi+b Qpsi)^3 therefore proves all local cubic and mixed gauge anomalies for this representation.',
                representation_homomorphism_error=hom,native_edge_hopping_covariance_error=covariance,
                hopping='-t psi_w^dag R(U_edge,chi_edge,psi_edge) psi_v + h.c., at every native edge',
                bare_Weyl_mass_forbidden_by_Qpsi=True,
                SU2_restriction=dict(doublets=6,singlets=15,half_integer_multiplicity_even=True),
                recent_external_connection='Craig arXiv:2610.09093v1 Proposition11.1 lists anomaly cancellation and even half-integer SU2 multiplicities for a measure on ordinary four-dimensional Euclidean SU(N) lattices. The SU5 restriction passes those representation conditions; this is not an implementation or verification of that preprint, nor does it supply the native spacetime or the two additional U1 measures.',
                prior='Round13 chiral_anomaly_27 owns the anomaly ledger; Pass11984 native_fiber_overlap already checks24^3 SU5 anomaly entries. Here joint SU5 x U1chi x U1psi finite-link matrices and covariance are explicit.',
                scope='Supplied standard27 branching on an independent internal carrier. No intertwiner to the canonical signed45-term cubic, Weyl lattice measure, global anomaly theorem, chiral dynamics, generations or vacuum derived. Ordinary hopping by itself is vectorlike.')


def continuous_threshold_bound():
    """Upgrade the inspected Pass12330 grid to a conditional continuous bound.

    These are frozen repo inputs, not newly measured couplings. Running uses
    exactly its one-loop, single common threshold assumptions.
    """
    source=ROOT/'analysis/search_drivers_12330'
    beta=json.loads((source/'beta.json').read_text())['b_full']
    assert beta==dict(b3='7',b2='16',bY='148/3')
    scan=json.loads((source/'scan.json').read_text())
    A2=s.Rational('127.95')*s.Rational('.2312')
    AY=s.Rational('127.95')*(1-s.Rational('.2312'));A3=1/s.Rational('.1180')
    delta=A2-A3; u=s.Symbol('u') # u=ln(MX/MZ)/(2pi)
    crossing_log=delta/9+s.Rational(31,54)*u # ln(Mcross/MZ)/(2pi)
    a2=s.expand(A2-16*crossing_log-(-s.Rational(19,6)-16)*u)
    ay=s.expand(AY-s.Rational(148,3)*crossing_log-(s.Rational(41,6)-s.Rational(148,3))*u)
    asymptote=s.Rational(2297,1617)
    remainder=s.expand(ay-asymptote*a2)
    assert a2.coeff(u)==s.Rational(539,54) and ay.coeff(u)==s.Rational(2297,162)
    assert remainder.is_Rational and remainder<0 and asymptote<s.Rational(8,3)
    maximum_error=0.
    for row in scan['rows']:
        uv=np.log(10**row['log10MX']/91.1876)/(2*np.pi)
        lcross=float(crossing_log.subs(u,uv))*2*np.pi
        assert lcross>=2*np.pi*uv # full-spectrum branch is applicable at crossing
        kval=float((ay/a2).subs(u,uv))
        maximum_error=max(maximum_error,abs(kval-row['k_needed']))
    assert maximum_error<1e-10
    return dict(prior_owner='Pass12330: analysis/search_drivers_12330/scan.py, beta.py and scan.json; full patch a15185e5c9fa28d820a69df8d1dcfda7fb040544 inspected.',
                variable='u=log(M_X/M_Z)/(2pi)',crossing_log_over_2pi=str(crossing_log),
                inverse_alpha2_at_crossing=str(a2),inverse_alphaY_at_crossing=str(ay),
                exact_remainder_AY_minus_bound_A2=str(remainder),
                universal_positive_A2_upper_bound_kY=str(asymptote),
                target='8/3',original53_grid_rows_max_error=maximum_error,
                scope='Whenever crossing lies above the common threshold and inverse alpha2 is positive, kY <2297/1617 <8/3 for this one-loop model. This proves a continuous conditional exclusion, strengthening the prior sampled exclusion. Nondegenerate thresholds, two-loop effects and other spectra are outside the claim.')


if __name__=='__main__':
    result=dict(microscopic_response=microscopic_response(),reflection_lift=reflection_lift(),compact_expansion=compact_expansion(),
                nonabelian_interface=nonabelian_interface(),continuous_threshold_bound=continuous_threshold_bound())
    out=ROOT/'data/w33_20261027_microscopic_response_and_lifts.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
