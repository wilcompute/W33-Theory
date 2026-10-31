#!/usr/bin/env python3
"""Five independent W33-to-physics followthrough falsifiers; no experimental TOE.

No desktop or network dependencies. Native W(3,3) projective symplectic
geometry and 120 spectral-outcome clock labels are rebuilt from F3^4.
"""
from __future__ import annotations
import itertools, json, math
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.linalg import null_space
from scipy.sparse.linalg import LinearOperator, eigsh

OUT = Path(__file__).resolve().parents[1] / "data" / "w33_20261031_server_five_fronts.json"
P = 3
PTS = [v for v in itertools.product(range(3), repeat=4)
       if any(v) and next(x for x in v if x) == 1]
assert len(PTS) == 40
IDX = {v: i for i, v in enumerate(PTS)}

def canonical(v):
    v = tuple(int(x) % 3 for x in v)
    first = next((x for x in v if x), None)
    if first is None: raise ValueError('zero projective vector')
    return tuple((x * pow(first, -1, 3)) % 3 for x in v)

def pairing(a, b):
    return (a[0]*b[2] + a[1]*b[3] - a[2]*b[0] - a[3]*b[1]) % 3

ADJ = np.array([[int(i != j and pairing(a,b) == 0)
                 for j,b in enumerate(PTS)] for i,a in enumerate(PTS)], dtype=int)
assert np.all(ADJ.sum(axis=1) == 12)

def equivariant_optical():
    """160 point-line rail embedding of the known 81D Steinberg cycle space."""
    lines = set()
    for i, a in enumerate(PTS):
        for j in range(i + 1, 40):
            b = PTS[j]
            if pairing(a,b): continue
            ll = frozenset(IDX[canonical(tuple((t*a[k] + u*b[k]) % 3 for k in range(4)))]
                           for t in range(3) for u in range(3) if t or u)
            assert len(ll) == 4
            lines.add(ll)
    lines = sorted(tuple(sorted(x)) for x in lines)
    assert len(lines) == 40
    flags = [(p,j) for j,l in enumerate(lines) for p in l]
    assert len(flags) == 160
    fidx = {z:i for i,z in enumerate(flags)}
    lidx = {frozenset(line):j for j,line in enumerate(lines)}
    D = np.zeros((80,160), dtype=float)
    for i,(p,l) in enumerate(flags): D[p,i] = -1; D[40+l,i] = 1
    assert np.linalg.matrix_rank(D) == 79
    Q = null_space(D)
    assert Q.shape == (160,81)
    assert np.linalg.norm(D@Q) < 1e-12
    assert np.linalg.norm(Q.T@Q-np.eye(81)) < 1e-12
    proj = Q@Q.T
    generators = [0,1,4,5,13]
    residuals=[]; order=[]; sample=[]
    for gen in generators:
        a=PTS[gen]
        pp=[]
        for v in PTS:
            k=pairing(v,a)
            pp.append(IDX[canonical(tuple((v[t]+k*a[t])%3 for t in range(4)))])
        assert sorted(pp) == list(range(40))
        lp = [lidx[frozenset(pp[p] for p in line)] for line in lines]
        pf = [fidx[(pp[p],lp[j])] for (p,j) in flags]
        assert sorted(pf) == list(range(160))
        Pmat = np.eye(160)[pf].T  # destination row, source col
        assert all(np.argmax(Pmat[:,col]) == pf[col] for col in range(160))
        R = Q.T@Pmat@Q
        cov=np.linalg.norm(Pmat@Q-Q@R)
        un=np.linalg.norm(R.T@R-np.eye(81))
        ord3=np.linalg.norm(R@R@R-np.eye(81))
        projector=np.linalg.norm(Pmat@proj@Pmat.T-proj)
        assert max(cov,un,ord3,projector) < 1e-10
        residuals.append([cov,un,ord3,projector]);order.append(3)
        sample.append({'transvection_point_index':gen,'fixed_physical_flags':int(sum(pf[i]==i for i in range(160))),
                       'tracial_81D_character':float(np.trace(R))})
    return {'status':'PASS_160_FLAG_ISOMETRY_81_STEINBERG_EQUIVARIANCE',
            'physical_rail_count':160,'logical_cycle_dimension':81,'incidence_rank':79,
            'generator_orders':order,'generator_residuals':residuals,'generators':sample,
            'encoding':'One-photon 81 logical complex amplitudes encoded by a real orthonormal 160x81 matrix Q spanning kernel(point-line incidence). W33 transvections are physical rail permutations P, satisfying P Q=Q (Q.T P Q).',
            'boundary':'Already-known Steinberg81 homology; this supplies a concrete passive optical *encoding specification*, not a calibrated 160-port chip, Hamiltonian or identification with 81 Pauli permutation labels.'}

def wigner(rho):
    omega=np.exp(2j*np.pi/3); vals=[]
    for q in range(3):
        for p in range(3):
            A=np.zeros((3,3),complex)
            for y in range(3):A[(q+2*y)%3,(q-2*y)%3]+=omega**(p*y)
            vals.append(float(np.trace(rho@A).real/3))
    return {'min':min(vals),'L1':sum(abs(v) for v in vals)}

def heralding_false_positives():
    S=np.array([0,1,-1],complex)/math.sqrt(2)
    E=np.array([0,1,1],complex)/math.sqrt(2)
    Pm=np.outer(S,S.conj())
    R=np.array([[1,0,0],[0,0,1],[0,1,0]],complex)
    assert np.allclose(Pm,(np.eye(3)-R)/2)
    rates=[]
    for eps in (0.,.01,.05,.1,.25,.4,.5):
        # Classical readout bit flip AFTER ideal projective instrument
        # is a physical noisy-instrument control, not a free Clifford resource.
        out=(1-eps)*Pm + eps*np.outer(E,E.conj())
        assert abs(np.trace(out)-1) < 1e-12
        wig=wigner(out)
        rates.append({'readout_flip':eps,'reported_success_probability_from_input_1':.5,
                      'false_herald_probability_from_input_0':eps,
                      'conditional_Strange_fidelity':1-eps,
                      'conditional_Wigner_min':wig['min'],'conditional_mana':math.log(wig['L1'])})
    assert rates[0]['conditional_mana']>0
    assert abs(rates[-1]['conditional_mana'])<1e-12
    return {'status':'PASS_STRANGE_QND_FALSE_HERALD_AND_MANA_ACCOUNTING',
            'noise_model':'Ideal qutrit parity projective instrument with independent classical flip of ancilla outcome, before conditioning; controlled-R resource already externally supplied.',
            'rates':rates,'noise_free_success':.5,'noisy_magic_zero_at_readout_flip':.5,
            'limitations':'Conditional state fidelity and mana are NOT gate fault-tolerance thresholds; destructive optical detection alone does not provide QND output.'}

def full_120_clock():
    """Full outcomes (40 lines x 3) exact transfer spectrum and quantum 2-site control."""
    J,K=1.,2.; eps=2*J-4*K/3
    pair=np.zeros((120,120),dtype=float)
    for i in range(120):
        a,x=divmod(i,3)
        for j in range(120):
            b,y=divmod(j,3)
            pair[i,j] = (0 if i==j else (3*J if a==b else (2*J if ADJ[a,b] else eps)))
    assert np.array_equal(pair,pair.T)
    rows=[]
    for beta in (.08,.2,.6,1.3,3.):
        a=math.exp(-2*beta*J);b=math.exp(-beta*eps);c=math.exp(-3*beta*J)
        M=np.exp(-beta*pair)
        vals=np.linalg.eigvalsh(M)
        theory=np.sort(np.array([1+2*c+36*a+81*b]
                 +[1+2*c+6*a-9*b]*24
                 +[1+2*c-12*a+9*b]*15
                 +[1-c]*80))
        mismatch=float(np.max(abs(vals-theory)))
        assert mismatch<1e-9
        lam0=float(theory[-1]);rest=sorted(abs(v) for v in theory[:-1])[-1]
        assert lam0>rest
        rows.append({'beta':beta,'Perron_eigenvalue':lam0,'spectral_error':mismatch,
                     'correlation_length':float(1/math.log(lam0/rest))})
    # h>0: on 120 outcomes per site the transverse uniform rank1 mixer is
    # genuinely a quantum off-diagonal Hamiltonian, unlike classical transfer.
    # Two sites: 14,400 dimensional wavefunction, matrix-free eigensolver.
    v=pair.ravel()
    n=120
    def op(h):
        def mv(z):
            t=z.reshape((n,n));z0=v*t.ravel()
            plus=(-h/n)*(np.sum(t,axis=0)[None,:]+np.sum(t,axis=1)[:,None])
            return z0 + plus.ravel()
        return LinearOperator((n*n,n*n),matvec=mv,dtype=float)
    quantum=[]
    for h in (.05,.25):
        eigs=np.sort(eigsh(op(h),k=2,which='SA',tol=5e-7,maxiter=5000,return_eigenvectors=False))
        gap=eigs[1]-eigs[0]
        assert gap>0
        quantum.append({'h':h,'E0':float(eigs[0]),'E1':float(eigs[1]),'gap':float(gap)})
    return {'status':'PASS_120_TICK_FOUR_SECTOR_TRANSFER_AND_TWO_SITE_QUANTUM_GAP',
            'relation_counts_per_label':{'identical':1,'same_direction_other_outcome':2,'different_commuting':36,'noncommuting':81},
            'full_transfer_eigenvalues':{'uniform':'1+2c+36a+81b, mult1','W33_2':'1+2c+6a-9b, mult24',
                          'W33_minus4':'1+2c-12a+9b, mult15','outcome_difference':'1-c, mult80'},
            'parameters':{'J':J,'K':K,'negative_noncommuting_bond':eps},
            'finite_beta':rows,'full_two_site_quantum_hilbert_dimension':n*n,
            'two_site_uniform_transverse_field':quantum,
            'boundary':'One-dimensional classical 120-label transfer solution plus two-site quantum transverse-rank1 Hamiltonian. Finite-size gap is not a bulk phase, and the spatial lattice and couplings are stipulated.'}

def floquet_noisy_channel():
    """Actual number of per-carrier SWAP stages, then calibrated depolarizing channel."""
    runs=[]
    for L in (4,6,8):
        at={(x,y):(x,y) for x in range(L) for y in range(L)}
        used_count=Counter({p:0 for p in at})
        for dx,dy in ((1,0),(0,1),(-1,0),(0,-1)):
            for x in range(L):
                for y in range(L):
                    if (x+y)%2: continue
                    q=(x+dx,y+dy)
                    if q not in at: continue
                    p=(x,y);a,b=at[p],at[q]
                    used_count[a]+=1;used_count[b]+=1
                    at[p],at[q]=b,a
        where={source:destination for destination,source in at.items()}
        moved=[p for p in where if where[p]!=p]
        assert len(moved)==2*L-1
        histogram=dict(sorted(Counter(used_count.values()).items()))
        for err in (0.,.001,.01,.03):
            fid=[]; coh=[]; surv=[]
            for source,stages in used_count.items():
                eta=(1-err)**(13*stages)
                # Standard depolarizing qutrit channel:
                # D_eta(rho)=eta rho+(1-eta) I/3.
                f_e=(1+8*eta)/9
                fixed_pure_f=(1+2*eta)/3
                lam=[f_e]+[(1-eta)/9]*8
                entropy=-sum(q*math.log(q) for q in lam if q>0)
                ic=math.log(3)-entropy
                assert -1e-12 <= f_e <= 1+1e-12
                fid.append(f_e);coh.append(ic);surv.append(fixed_pure_f)
            runs.append({'L':L,'error_per_native_tick':err,'stage_histogram':histogram,
                         'mean_entanglement_fidelity':float(np.mean(fid)),
                         'worst_entanglement_fidelity':float(min(fid)),
                         'mean_fixed_pure_state_fidelity':float(np.mean(surv)),
                         'count_positive_maxmixed_coherent_information':int(sum(x>1e-12 for x in coh))})
    assert all(x['mean_entanglement_fidelity']==1 for x in runs if x['error_per_native_tick']==0)
    return {'status':'PASS_FLOQUET_PER_CARRIER_13_TICK_EXPOSURE_AND_NOISY_FIDELITY',
            'results':runs,'model':'Four-stage open-square native 13-tick SWAP drive; only actual swapped carriers receive 13 local independent qutrit depolarizing channels per stage. Output position routed perfectly; channel fidelity and coherent information computed on that rail.',
            'boundary':'Qutrit depolarizing control, not measured device, correlated noise or a channel GNVW invariant. Positive coherent information at maximally mixed input is only an achievable lower bound for this single-carrier channel, not a fault-tolerance theorem.'}

def lorentz_gauss_and_constraint_gap():
    """3D spatial lattice canonical Lorentz Gauss closure; ADM scalar fails."""
    eta=np.diag([-1.,1.,1.,1.]); generators=[]
    for i in range(1,4):
        k=np.zeros((4,4));k[0,i]=1;k[i,0]=1;generators.append(k)
    for i,j in ((1,2),(1,3),(2,3)):
        k=np.zeros((4,4));k[i,j]=1;k[j,i]=-1;generators.append(k)
    assert all(np.linalg.norm(g.T@eta+eta@g)<1e-12 for g in generators)
    rng=np.random.default_rng(20261031)
    dims=(2,2,2);x=rng.normal(size=dims+(4,));p=rng.normal(size=dims+(4,))
    maxgauss=0.;maxscalar=0.
    for A,B in itertools.product(generators,repeat=2):
        C=A@B-B@A
        for vertex in np.ndindex(dims):
            xx=x[vertex];pp=p[vertex]
            # G_A=p^T A x, {G_A,G_B}= G_[A,B] exactly.
            lhs=(A.T@pp)@(B@xx)-(A@xx)@(B.T@pp)
            rhs=pp@C@xx
            maxgauss=max(maxgauss,abs(lhs-rhs))
        # {G_A, H0} = 0 when H0=.5(pp^T eta pp + xx^T eta xx)
        for vertex in np.ndindex(dims):
            xx=x[vertex];pp=p[vertex]
            gaussgrad_x=A.T@pp;gaussgrad_p=A@xx
            hgrad_x=eta@xx;hgrad_p=eta@pp
            maxscalar=max(maxscalar,abs(gaussgrad_x@hgrad_p-gaussgrad_p@hgrad_x))
    assert maxgauss<1e-12 and maxscalar<1e-12
    # Nonzero shift generator for generic data, but ultralocal H constraints
    # have identically zero bracket for ANY lapse N,M.
    N=rng.normal(size=dims);M=rng.normal(size=dims)
    dif=0.
    for vertex in np.ndindex(dims):
        for mu in range(3):
            plus=list(vertex);plus[mu]=(plus[mu]+1)%dims[mu];plus=tuple(plus)
            dn=N[vertex]*M[plus]-M[vertex]*N[plus]
            dif+=dn*(p[vertex]@(x[plus]-x[vertex]))
    assert abs(dif)>1e-4
    return {'status':'PASS_3PLUS1_LORENTZ_GAUSS_CLOSURE_AND_ULTRALOCAL_ADM_FAILURE',
            'spatial_lattice':list(dims),'internal_metric':'diag(-1,1,1,1)',
            'max_lorentz_Gauss_Poisson_closure_error':maxgauss,
            'max_Gauss_scalar_invariance_error':maxscalar,
            'ultralocal_smeared_scalar_Poisson_bracket':0.,
            'nonzero_generic_discrete_shift_target':float(dif),
            'obstruction':'The local Lorentz Gauss algebra closes, but ultralocal Lorentz-invariant scalar H(x)=.5(p eta p + x eta x) has {H[N],H[M]}=0, not the nonzero spatial-diffeomorphism term of the hypersurface deformation algebra. The candidate is explicitly not 3+1 general relativity.',
            'boundary':'No lattice link curvature, Palatini action, tetrad invertibility, diffeomorphism constraint or first-class ADM closure. This is a stringent negative control, not a completion of the gravity objective.'}

def build():
    fronts={'01_steinberg160_mode_optics':equivariant_optical,
            '02_QND_strange_false_herald':heralding_false_positives,
            '03_full120_tick_classical_and_quantum':full_120_clock,
            '04_noisy_floquet_carrier_channel':floquet_noisy_channel,
            '05_3plus1_lorentz_gauss_and_adm_nogo':lorentz_gauss_and_constraint_gap}
    results={}
    for name,func in fronts.items():
        result=func()
        results[name]=result
        print(name,result['status'],flush=True)
    return {'schema':'w33.server.five_physical_fronts.v1','results':results,
            'provenance':'Reconstructed independent F3 symplectic geometry, existing known Steinberg81, previous native 13-tick SWAP and QND parity protocol. No prior repo result rebranded as discovery.',
            'scope':'Five deterministic mathematical models, bounded extrapolation; not a physical TOE or observed experiment.'}
if __name__=='__main__':
    d=build();OUT.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
    print('CERTIFICATE',OUT)
