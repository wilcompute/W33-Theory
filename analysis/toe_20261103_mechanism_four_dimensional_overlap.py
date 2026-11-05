"""Actual four-dimensional compact-U(1) flux overlap operator, with Weyl blocks.

Euclidean regulator supplied independently of W33. No chiral measure is claimed.
"""
import hashlib,itertools,json,math,pathlib,time
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]

def gammas():
    I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
    g=[np.kron(X,I),np.kron(Y,I),np.kron(Z,X),np.kron(Z,Y)]
    g5=g[0]@g[1]@g[2]@g[3]
    assert np.max(abs(g5-g5.conj().T))<1e-14
    return g,g5

def links(L,flux12=1,flux34=1):
    xs=list(itertools.product(range(L),repeat=4));U=np.ones((L**4,4),complex)
    for a,b,n in [(0,1,flux12),(2,3,flux34)]:
        for i,x in enumerate(xs):
            U[i,a]*=np.exp(-2j*np.pi*n*x[b]/L**2)
            if x[b]==L-1:U[i,b]*=np.exp(2j*np.pi*n*x[a]/L)
    return U

def plaquettes(U,L):
    xs=list(itertools.product(range(L),repeat=4));ix={x:i for i,x in enumerate(xs)};out=[]
    for mu in range(4):
        for nu in range(mu+1,4):
            z=[]
            for i,x in enumerate(xs):
                a=list(x);a[mu]=(a[mu]+1)%L;b=list(x);b[nu]=(b[nu]+1)%L
                z.append(U[i,mu]*U[ix[tuple(a)],nu]*U[ix[tuple(b)],mu].conjugate()*U[i,nu].conjugate())
            out.append(np.array(z))
    return np.array(out)

def operator(U,L,m0=1.):
    gs,g5=gammas();n=L**4;xs=list(itertools.product(range(L),repeat=4));ix={x:i for i,x in enumerate(xs)}
    W=4*np.eye(4*n,dtype=complex);I=np.eye(4)
    for i,x in enumerate(xs):
        a=slice(4*i,4*i+4)
        for mu in range(4):
            y=list(x);y[mu]=(y[mu]+1)%L;j=ix[tuple(y)];b=slice(4*j,4*j+4)
            W[a,b]-=.5*U[i,mu]*(I-gs[mu]);W[b,a]-=.5*U[i,mu].conjugate()*(I+gs[mu])
    G=np.kron(np.eye(n),g5);H=G@(W-m0*np.eye(4*n))
    assert np.max(abs(H-H.conj().T))<1e-12
    lam,v=np.linalg.eigh(H);gap=float(np.min(abs(lam)));assert gap>1e-8
    sign=(v*np.sign(lam))@v.conj().T
    D=np.eye(4*n)+G@sign;hat=-sign
    return D,G,hat,lam

def summarize(L,n1,n2,perturb=0.):
    start=time.monotonic();U=links(L,n1,n2)
    if perturb:U*=np.exp(1j*perturb*np.random.default_rng(44).normal(size=U.shape))
    D,G,hat,lam=operator(U,L);N=len(D);I=np.eye(N)
    index=int(round(-np.sum(np.sign(lam))/2));P=(I-hat)/2;Q=(I+G)/2
    # D hatPminus = Pplus D: genuine four-dimensional Weyl kinetic map.
    gw=float(np.max(abs(G@D+D@G-D@G@D)));intertwine=float(np.max(abs(D@P-Q@D)))
    singular=np.linalg.svd(D,compute_uv=False);zero=int(np.sum(singular<1e-8))
    top=np.diag(G@(I-D/2)).real;assert abs(sum(top)-index)<1e-8
    ps=plaquettes(U,L)
    return dict(L=L,sites=L**4,spinor_matrix_dimension=N,flux12=n1,flux34=n2,link_perturbation=perturb,
        overlap_index=index,continuum_flux_product=n1*n2,Dirac_zero_modes=zero,
        kernel_spectral_gap=float(np.min(abs(lam))),GW_max_defect=gw,Weyl_intertwiner_max_defect=intertwine,
        Weyl_domain_rank=int(round(np.trace(P).real)),Weyl_codomain_rank=N//2,
        chirality_of_zero_modes_index_formula=float(np.trace(G@(I-D/2)).real),
        maximum_plaquette_angle=float(np.max(abs(np.angle(ps)))),
        Wilson_gauge_action_beta1=float(np.sum(1-ps.real)),
        index_density_range=[float(top.min()),float(top.max())],elapsed_seconds=time.monotonic()-start,
        kernel_eigenvalue_sha256=hashlib.sha256(np.asarray(lam,dtype='<f8').tobytes()).hexdigest())

def build():
    rows=[summarize(3,0,0),summarize(3,1,1),summarize(3,1,-1),summarize(3,1,1,.015),summarize(4,1,1)]
    orientation=rows[1]['overlap_index'];assert abs(orientation)==1
    assert rows[0]['overlap_index']==0 and rows[2]['overlap_index']==-orientation
    assert rows[3]['overlap_index']==rows[4]['overlap_index']==orientation
    assert all(r['GW_max_defect']<1e-10 and r['Weyl_intertwiner_max_defect']<1e-10 for r in rows)
    assert rows[1]['Dirac_zero_modes']==rows[2]['Dirac_zero_modes']==rows[4]['Dirac_zero_modes']==1
    # A second representation: arbitrary on-site U(1) rotation, tested on full D.
    L=3;U=links(L);D,G,hat,lam=operator(U,L);xs=list(itertools.product(range(L),repeat=4));ix={x:i for i,x in enumerate(xs)}
    phase=np.exp(1j*np.random.default_rng(71).normal(size=L**4));Ug=U.copy()
    for i,x in enumerate(xs):
        for mu in range(4):
            y=list(x);y[mu]=(y[mu]+1)%L;Ug[i,mu]*=phase[i]*phase[ix[tuple(y)]].conjugate()
    Dg,*_=operator(Ug,L);s=np.repeat(phase,4);cov=float(np.max(abs(Dg-s[:,None]*D*s.conj()[None,:])))
    assert cov<1e-11
    # Free corners: at m0 in(0,2), only n_pi=0 has negative Wilson mass.
    corners=[dict(pi_components=k,multiplicity=math.comb(4,k),overlap_D_eigenvalue=0 if k==0 else 2)for k in range(5)]
    charges=[-9,-5,-1,7,8];assert sum(charges)==sum(q**3 for q in charges)==0
    return dict(status='PASS_FOUR_DIMENSIONAL_FLUX_INDEX_AND_WEYL_KINETIC_MAP',rows=rows,
        gauge_covariance_max_defect=cov,free_Brillouin_corners=corners,anomaly_free_chiral_U1_example=charges,
        anomaly_linear=0,anomaly_cubic=0,
        declared_geometry='Periodic hypercubic Euclidean four-torus with L=3 and4, four-component complex spinors and compact U(1) links. This geometry and gauge group are supplied; they are not derived from W33, quantum information, or a background-independent action.',
        convention='gamma=(XxI,YxI,ZxX,ZxY), gamma5=gamma0 gamma1 gamma2 gamma3. DW=4I-sum_mu[(1-gamma_mu)U_mu Tplus+(1+gamma_mu)Tminus U_mu^dag]/2. H=gamma5(DW-m0),m0=1. D=I+gamma5 sign(H), in lattice units. Orientation is fixed by these gamma/flux conventions, not silently adjusted to a desired sign.',
        kinetic_map='hat_gamma5=gamma5(1-D)=-sign(H). hatPminus=(1-hat_gamma5)/2, Pplus=(1+gamma5)/2, D hatPminus=Pplus D. In nonzero-index backgrounds the Weyl block is rectangular, with the dimension mismatch and zero modes exported.',
        prior_native_obstruction='analysis/w33_20261010_toe41_w33_overlap_index_nogo.py proves zero index for its paired 40x40 incidence kernel for ALL gauges. The present unpaired spin/Wilson regulator has a nonzero flux index on a DIFFERENT supplied 4D geometry; it neither refutes that theorem nor supplies a W33-to-spacetime map.',
        prior_free_corner_owner='data/PART_4057_4064_ADVANCED_PHYSICS.json:pass4060_gauge_covariant_wilson_matter already owns the supplied4D nearest-neighbor Wilson construction, gauge covariance and16-corner/one-species audit. Those are reused prior controls, not new results here. The present calculation adds actual finite overlap flux matrices, their nonzero index, rectangular Weyl maps and perturbation/second-size tests.',
        locality='Wilson kernel is nearest-neighbor. The overlap sign is not ultralocal. Positive gaps and observed index persistence under one small perturbation are finite numerical tests, not a proof of uniform exponential locality, admissibility for all backgrounds or a continuum limit.',
        missing_dynamics='This implements a 4D gauge-covariant Weyl kinetic operator and Wilson gauge-action evaluation, NOT a full interacting chiral gauge path integral or Hamiltonian. The anomaly-free charge example passes only polynomial anomaly conditions. An integrable gauge-field-dependent Weyl measure, fermion determinant phase, anomaly/ward identities, fermionic backreaction and continuum dynamics remain unimplemented. A vectorlike determinant or a 1+1D mirror gap would not fill that gap.',
        sources=['https://arxiv.org/abs/hep-lat/9707022','https://arxiv.org/abs/hep-lat/9802011','https://arxiv.org/abs/hep-lat/9811032','https://arxiv.org/abs/2505.20419'])

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261103_mechanism_four_dimensional_overlap.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],[(r['L'],r['flux12'],r['flux34'],r['overlap_index'])for r in d['rows']],flush=True)
