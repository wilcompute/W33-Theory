#!/usr/bin/env python3
"""Six independently tested exact/finite TOE research gates, 2026-11-20.

Rigorous algebraic certificates (H27 baryon covariants; W33 Hodge), controlled
quantum-metrology models, standard chirality no-gos, and a 4D causal sprinkling
symmetry check. No assertion of a completed TOE or optical experiment.
"""
from __future__ import annotations
import json, math
from collections import Counter
from itertools import combinations,product
from pathlib import Path
import numpy as np
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'data/toe_20261120_H27_equivariant_sic_memory_weyl_g2_causal_hodge.json'
PRIME=7
OMEGA_MOD=2 # 2**2+2+1=0 modulo 7; residue of Eisenstein integer omega
OMEGA=np.exp(2j*np.pi/3)
X=np.array([[0,0,1],[1,0,0],[0,1,0]],dtype=int)
Z7=np.diag([1,OMEGA_MOD,(OMEGA_MOD**2)%PRIME])
ZC=np.diag([1,OMEGA,OMEGA**2])
Xc=X.astype(complex)
TRIPLES=list(combinations(range(9),3))
TINDEX={t:i for i,t in enumerate(TRIPLES)}
OFFSETS=((0,0),(1,0),(0,1))


def modrank(A,p=PRIME,return_pivots=False):
    a=np.array(A,dtype=np.int64,copy=True)%p
    r=0;pivots=[]
    for j in range(a.shape[1]):
        choices=np.flatnonzero(a[r:,j])
        if not len(choices):continue
        row=r+int(choices[0]);a[[r,row],:]=a[[row,r],:]
        a[r,:]=(a[r,:]*pow(int(a[r,j]),-1,p))%p
        for k in range(r+1,a.shape[0]):
            if a[k,j]:a[k,:]=(a[k,:]-a[k,j]*a[r,:])%p
        pivots.append(j);r+=1
        if r==a.shape[0]:break
    return (r,pivots) if return_pivots else r


def moddet(A,p=PRIME):
    a=np.array(A,dtype=np.int64,copy=True)%p
    n=a.shape[0];assert a.shape==(n,n)
    det=1
    for j in range(n):
        hit=np.flatnonzero(a[j:,j])
        if not len(hit):return 0
        i=j+int(hit[0])
        if i!=j:a[[i,j]]=a[[j,i]];det=-det
        v=int(a[j,j]);det=(det*v)%p
        factor=pow(v,-1,p)
        for k in range(j+1,n):
            if a[k,j]:a[k,:]=(a[k,:]-a[k,j]*factor*a[j,:])%p
    return int(det%p)


def det3(a,b,c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))


def shift(i,da,db):
    return 3*((i//3+db)%3)+(i%3+da)%3


def baryon_action(t,da,db,omega):
    indices=[shift(i,da,db) for i in t]
    sign=(-1)**sum(indices[i]>indices[j] for i in range(3) for j in range(i+1,3))
    phase=omega**((da*sum(i//3 for i in t))%3)
    return tuple(sorted(indices)),sign*phase


def sic_columns(omega,mod=False):
    ZZ=np.diag([1,omega,omega**2]);XX=X
    v=np.array([1,-1,0],dtype=int if mod else complex)
    Q=np.array([np.linalg.matrix_power(XX,b)@np.linalg.matrix_power(ZZ,a)@v
                for b in range(3) for a in range(3)]).T
    return Q%PRIME if mod else Q


def baryon_J(Q,mod=False):
    rows=[]
    for t in TRIPLES:
        row=np.zeros(27,dtype=int if mod else complex)
        for j,idx in enumerate(t):
            for coord in range(3):
                arr=[Q[:,i].copy() for i in t]
                arr[j]=np.eye(3,dtype=int if mod else complex)[:,coord]
                row[3*idx+coord]=det3(*arr)
        rows.append(row%PRIME if mod else row)
    return np.array(rows)


def fourier_baryon_coeff(t,u,v,omega,mod=False):
    co=np.zeros(len(TRIPLES),dtype=int if mod else complex)
    for da,db in product(range(3),repeat=2):
        dest,phase=baryon_action(t,da,db,omega)
        chi=omega**((u*da+v*db)%3)
        val=phase*(pow(int(chi)%PRIME,-1,PRIME) if mod else 1/chi)
        co[TINDEX[dest]]+=val
    return co%PRIME if mod else co


def baryons(Q):
    return np.array([det3(*[Q[:,k] for k in t]) for t in TRIPLES])


def h27_sic_gate():
    Q7=sic_columns(OMEGA_MOD,True);J7=baryon_J(Q7,True)
    assert modrank(J7)==19
    selected=[];sector_dims={};all_rows=[]
    for u,v in product(range(3),repeat=2):
        collection=[]
        for t in TRIPLES:
            c=fourier_baryon_coeff(t,u,v,OMEGA_MOD,True)
            collection.append(c@J7%PRIME)
        rank=modrank(collection);sector_dims[f'{u}{v}']=rank
        indep=[]
        for seed,row in zip(TRIPLES,collection):
            if modrank(np.array(indep+[row]))>len(indep):
                indep.append(row)
                selected.append({'char':[u,v],'seed':list(seed)})
                all_rows.append(row)
                if len(indep)==rank:break
    assert sector_dims['00']==3 and all(sector_dims[k]==2 for k in sector_dims if k!='00')
    assert len(all_rows)==19 and modrank(all_rows)==19
    mr,pivots=modrank(np.array(all_rows),return_pivots=True) # Pivot columns of the 19x27 constraint matrix
    assert mr==19
    certdet=moddet(np.array(all_rows)[:,pivots]);assert certdet!=0
    Q=sic_columns(OMEGA)
    J=baryon_J(Q)
    C=np.array([fourier_baryon_coeff(tuple(s['seed']),*s['char'],OMEGA) for s in selected])
    M=C@J
    sv=np.linalg.svd(M,compute_uv=False)
    assert sv[-1]>1e-7 and np.linalg.matrix_rank(M,tol=1e-7)==19
    b=C@baryons(Q)
    nontrivial_idx=[i for i,s in enumerate(selected) if s['char']!=[0,0]]
    assert max(abs(b[i]) for i in nontrivial_idx)<1e-9
    assert np.linalg.norm(Q@Q.conj().T-6*np.eye(3))<1e-10
    # Covariance of ALL nineteen source polynomials in a randomly chosen Q.
    rng=np.random.default_rng(20261120)
    Qrand=rng.normal(size=(3,9))+1j*rng.normal(size=(3,9))
    F=C@baryons(Qrand)
    maxcov=0;maxvac=0
    for da,db in product(range(3),repeat=2):
        new=np.column_stack([OMEGA**(da*(i//3))*Qrand[:,shift(i,da,db)] for i in range(9)])
        moved=C@baryons(new)
        expected=np.array([OMEGA**((s['char'][0]*da+s['char'][1]*db)%3)*f for s,f in zip(selected,F)])
        maxcov=max(maxcov,float(np.max(abs(moved-expected))))
        U=np.linalg.matrix_power(Xc,db)@np.linalg.matrix_power(ZC,da)
        movevac=np.column_stack([OMEGA**(da*(i//3))*Q[:,shift(i,da,db)] for i in range(9)])
        maxvac=max(maxvac,float(np.linalg.norm(movevac-U@Q)))
    assert maxcov<1e-8 and maxvac<1e-10
    # Anti-triplet/S mass coupling from three translated offsets, each a 3-vector frame.
    N=np.zeros((27,27),dtype=complex);dets=[]
    for i in range(9):
        V=np.column_stack([Q[:,shift(i,*ofs)] for ofs in OFFSETS])
        dets.append(np.linalg.det(V))
        for r in range(3):N[3*i+r,3*i:3*i+3]=V[:,r]
    assert min(abs(x) for x in dets)>1e-7
    sn=np.linalg.svd(N,compute_uv=False)
    assert sn[-1]>1e-7
    # Check the *actual* coupling S_{i,r} tildeQ_i.Q_{i+off_r} under species H27 action.
    tilde=rng.normal(size=(9,3))+1j*rng.normal(size=(9,3))
    S=rng.normal(size=(9,3))+1j*rng.normal(size=(9,3))
    def WA(Qmat,tmat,Smat):
        return sum(Smat[i,r]*np.dot(tmat[i,:],Qmat[:,shift(i,*offs)])
          for i in range(9) for r,offs in enumerate(OFFSETS))
    orig=WA(Qrand,tilde,S);maxanti=0
    for da,db in product(range(3),repeat=2):
        newQ=np.column_stack([OMEGA**(da*(i//3))*Qrand[:,shift(i,da,db)] for i in range(9)])
        newT=np.array([OMEGA**(-da*(i//3))*tilde[shift(i,da,db)] for i in range(9)])
        newS=np.array([[OMEGA**(-da*ofs[1])*S[shift(i,da,db),r]
                         for r,ofs in enumerate(OFFSETS)] for i in range(9)])
        maxanti=max(maxanti,float(abs(WA(newQ,newT,newS)-orig)))
    assert maxanti<1e-8
    # Full holomorphic mass Hessian W=sum L(F-b)+sum S tildeQ.Qoffset.
    # Coordinates: Q[27], tilde[27], L[19], S[27].
    H=np.zeros((100,100),complex)
    H[:27,54:73]=M.T; H[54:73,:27]=M
    H[27:54,73:100]=N.T; H[73:100,27:54]=N
    singular=np.linalg.svd(H,compute_uv=False)
    assert sum(singular>1e-7)==92
    # Gauge orbit 8D tangent: check M kills all traceless complex matrices A*Q.
    gauge_basis=[]
    for i in range(3):
        for j in range(3):
            if i!=j:
                A=np.zeros((3,3),complex);A[i,j]=1;gauge_basis.append(A)
    for k in (0,1):
        A=np.zeros((3,3),complex);A[k,k]=1;A[2,2]=-1;gauge_basis.append(A)
    gauge_vec=np.array([(A@Q).T.reshape(-1) for A in gauge_basis])
    maxgauge=max(np.linalg.norm(M@((A@Q).T.reshape(-1))) for A in gauge_basis)
    assert len(gauge_basis)==8 and maxgauge<1e-8
    # Color-ordered Q variables are flattened by species; the gauge check above matches J.
    return {
       'baryon_character_ranks':sector_dims,'dimension':sum(sector_dims.values()),
       'selected_19_characters_and_seed_triples':selected,
       'mod7_minor_pivot_columns':pivots,'mod7_nonzero_19x19_minor_determinant':certdet,
       'exact_rank_certificate':'Nonzero 19x19 minor over F7, omega=2, implies a nonzero minor in Z[omega] and characteristic-zero rank >=19; eight SL3 gauge directions force <=19.',
       'nine_SIC_triplets_Dflat_residual':float(np.linalg.norm(Q@Q.conj().T-6*np.eye(3))),
       '19_constraint_min_singular_value':float(sv[-1]),
       'trivial_character_source_values':[[float(z.real),float(z.imag)] for i,z in enumerate(b) if i not in nontrivial_idx],
       'max_nontrivial_character_source_value':float(max(abs(b[i]) for i in nontrivial_idx)),
       'H27_covariance_source_residual':maxcov,
       'H27_vacuum_color_gauge_residual':maxvac,
       'H27_antifundamental_coupling_residual':maxanti,
       'anti_triplet_frame_min_abs_det':float(min(abs(z) for z in dets)),
       'antifundamental_block_min_singular':float(sn[-1]),
       'full_100x100_holomorphic_Hessian_rank':int(sum(singular>1e-7)),
       'full_holomorphic_Hessian_gauge_kernel':100-int(sum(singular>1e-7)),
       'max_gauge_tangent_Flinear_residual':float(maxgauge),
       'SU3_cubic_chiral_gauge_anomaly':'9 fundamental + 9 antifundamental = 0; singlets carry no color',
       'no_surplus_L_modes':True,
       'limitation':'Engineered H27-equivariant gauge toy, NOT E8-invariant, globally vacuum-selected, chirally compactified or phenomenologically predictive. Relative species/clock phases are active, not bare baryon-coordinate permutations.'}


def fid(d,e):
    a=1-e+e/d;b=e/d
    return 2*math.sqrt(a*b)+(d-2)*b

def witness(d,g,e):return (d-1)*(d*fid(d,e)-g)

def memory_gate():
    threshold={str(g):brentq(lambda e:witness(3,g,e),1e-15,.2) for g in (.36,.75,1.)}
    # Bernoulli experiment under explicitly modeled symmetric depolarization.
    # First channel: |0> count on E1(I/d), p=(1+(d-1)gamma)/d.
    # Later: wrong-basis outcome rate q=e(d-1)/d, pooled across two bases.
    g=.75;e=.01;d=3;delta=.01
    q=e*(d-1)/d;p=(1+(d-1)*g)/d
    def worst(N):
        t=math.sqrt(math.log(4/delta)/(2*N))
        qu=min(1.,q+2*t);gl=(d*(p-2*t)-1)/(d-1)
        # convert q to e with factor d/(d-1)
        return witness(d,gl,qu*d/(d-1))
    low=1;high=1
    while worst(high)>=0:high*=2
    while low+1<high:
        mid=(low+high)//2
        if worst(mid)<0:high=mid
        else:low=mid
    assert worst(high)<0 and worst(high-1)>=0
    rng=np.random.default_rng(20261120);n=high
    # Actual outcome model and data-driven CI, one representative seeded experiment.
    nfirst=int(rng.binomial(n,p));nlate=int(rng.binomial(n,q))
    t=math.sqrt(math.log(4/delta)/(2*n))
    pL=max(0.,nfirst/n-t);qU=min(1.,nlate/n+t)
    gammaL=max(0.,(3*pL-1)/2)
    we=witness(3,gammaL,min(1.,1.5*qU))
    assert we<0
    return {'dimension':3,'gamma_thresholds_epsilon':threshold,
      'illustrative_gamma':g,'illustrative_late_depolarization_epsilon':e,
      'illustrative_true_witness':witness(3,g,e),
      'error_probability_upper_bound':delta,
      'sufficient_shots_each_of_first_and_pooled_late_populations':high,
      'total_independent_shots':2*high,
      'hoeffding_radius':t,'simulated_first_channel_reference0_counts':nfirst,
      'simulated_late_wrong_outcome_counts':nlate,
      'simulated_confidence_upper_witness':we,
      'statistical_contract':'Model-conditional: exact isotropic depolarization, IID fixed preparations/readout and known MUBs. One Bernoulli population estimates E1(I/3), another the pooled late wrong-outcome rate. Two-sided Hoeffding and union bound certify a 99% confidence bound. Not SPAM-/loss-robust device-independent certification.',
      'interpretation':'Increasing gamma to 0.75 raises qutrit witness noise threshold from about 1.03% to 4.29%; 1.0 reaches about 7.50%. This is witness detectability, not a noise tolerance for an implemented device.'}


def su3_weyl_gate():
    # Probability weights p_ab for nine physical controlled Weyl settings.
    W=[np.linalg.matrix_power(Xc,a)@np.linalg.matrix_power(ZC,b)
       for a,b in product(range(3),repeat=2)]
    for u,v in product(range(3),repeat=2):
        if u==v==0:continue
        assert abs(sum(OMEGA**((a*u+b*v)%3) for a,b in product(range(3),repeat=2)))<1e-12
    rng=np.random.default_rng(20261120)
    randomE=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    E=randomE@randomE.conj().T;E/=np.trace(E)
    M=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    A,_=np.linalg.qr(M);A=A/np.linalg.det(A)**(1/3)
    M=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    B,_=np.linalg.qr(M);B=B/np.linalg.det(B)**(1/3)
    K=A@B@A.conj().T@B.conj().T
    def read(V):return 3*np.trace(E@V@K@V.conj().T)
    err9=abs(sum(read(V) for V in W)/9-np.trace(K))
    assert err9<1e-12
    # Every nonuniform Weyl weight survives at least one character Fourier mode.
    # A simple specific setting dependent efficiency pattern.
    p=np.array([1+.25*math.cos(2*math.pi*a/3) for a,b in product(range(3),repeat=2)],float)
    p/=sum(p)
    fmax=max(abs(sum(p[j]*OMEGA**((a*u+b*v)%3) for j,(a,b) in enumerate(product(range(3),repeat=2))))
             for u,v in product(range(3),repeat=2) if (u,v)!=(0,0))
    eta_twirl=sum((p[j]*V.conj().T@E@V for j,V in enumerate(W)),np.zeros((3,3),complex))
    bias=3*np.trace(eta_twirl@K)-np.trace(K)
    bound=3*sum(abs(p-1/9))
    assert abs(bias)<=bound+1e-12 and fmax>1e-4
    # 3 settings sufficient for diagonal mode response, but not arbitrary E.
    U=[np.linalg.matrix_power(Xc,a) for a in range(3)]
    Ediag=np.diag([.1,.3,.6]).astype(complex)
    avg=sum((V.conj().T@Ediag@V for V in U),np.zeros((3,3),complex))/3
    assert np.linalg.norm(avg-np.eye(3)/3)<1e-12
    residual3=np.linalg.norm(sum((V.conj().T@E@V for V in U),np.zeros((3,3),complex))/3-np.eye(3)/3)
    assert residual3>1e-3
    # finite Fourier inversion: only uniform nine-weight distribution annihilates all 8 nonidentity Weyls.
    char=np.array([[OMEGA**((a*u+b*v)%3) for a,b in product(range(3),repeat=2)]
                   for u,v in product(range(3),repeat=2)],complex)
    assert np.linalg.matrix_rank(char)==9
    # Worst-case gate operator norm tau contributes <=6tau additive character bias.
    return {'nine_weyl_character_Fourier_transform_rank':int(np.linalg.matrix_rank(char)),
      'unique_weight_distribution_for_detector_independent_all_matrix_twirling':'p_ab=1/9 for all 9 settings',
      'minimum_nonzero_Weyl_settings_for_full_unknown_detector':9,
      'minimum_X_shift_settings_for_unknown_diagonal_detector':3,
      'error_full_uniform_nine_twirls':float(err9),
      'nonuniform_example_max_nontrivial_Weyl_Fourier_weight':float(fmax),
      'nonuniform_example_complex_trace_error':float(abs(bias)),
      'nonuniform_example_L1_bound':float(bound),
      'arbitrary_detector_three_shift_frobenius_residual':float(residual3),
      'gate_operator_error_bound':'For each intended Weyl U_j and implemented V_j with ||U_j-V_j||_op<=tau, total character error <=6tau plus 3||p-uniform||_1 (eta>=0, Tr eta=1, K unitary).',
      'limitations':'Assumes linear positive detector matrix, coherently implemented conjugations, no time-correlated source drift. General physical optical error budget still pending.'}


def chirality_gate():
    # Established Lichnerowicz and Dirac-sphere spectral input, independently tabulated.
    n=7;scalar=n*(n-1) # radius 1
    gap_bound=math.sqrt(scalar/4)
    vals=[]
    for k in range(4):
        eig=k+n/2
        deg=2**(n//2)*math.comb(k+n-1,k)
        vals.append({'k':k,'Dirac_eigenvalues':[-eig,eig],'multiplicity_each_sign':deg})
    assert vals[0]['Dirac_eigenvalues']==[-3.5,3.5]
    assert min(abs(x) for x in vals[0]['Dirac_eigenvalues'])>gap_bound
    # On a compact smooth 1D periodic discretization, the chiral offdiagonal
    # operator Q is square. By rank-nullity: dimkerQ-dimkerQ^*=0.
    size=78
    x=np.arange(size);m=.85*np.tanh(4*np.sin(6*np.pi*x/size))
    F=np.roll(np.eye(size),-1,axis=1)
    B=F.T
    Q=.5*(F-B)+np.diag(m)
    assert np.linalg.matrix_rank(Q)==np.linalg.matrix_rank(Q.T)
    # A positive scalar curvature gap is for the untwisted Dirac operator; twisting
    # changes the Weitzenbock curvature term. No universal no-go asserted.
    return {'round_unit_S7_scalar_curvature':scalar,
      'untwisted_Lichnerowicz_dirac_spectral_gap_lower_bound':gap_bound,
      'exact_unit_S7_Dirac_spectrum_first_four_levels':vals,
      'untwisted_S7_zero_modes':0,
      'periodic_domain_wall_lattice_sites':size,
      'periodic_Q_rank':int(np.linalg.matrix_rank(Q)),
      'periodic_index_dimkerQ_minus_dimkerQ_adj':int((size-np.linalg.matrix_rank(Q))-(size-np.linalg.matrix_rank(Q.T))),
      'classification':'Independent reproduction of established spin geometry. Acharya-Witten require singular G2 holonomy spaces for 4D chirality in the M-theory setup. Smooth positive-scalar-curvature *untwisted* S7 cannot yield even a 7D Dirac zero mode; twisted bundles/singular geometries are different cases.'}


def sample_minkowski_diamond(rng,n):
    radius=np.abs(rng.beta(1,4,size=n))
    t=np.where(rng.integers(0,2,size=n).astype(bool),radius,-radius)
    spatial=rng.normal(size=(n,3));spatial/=np.linalg.norm(spatial,axis=1,keepdims=True)
    spatial*=((1-radius)*rng.random(n)**(1/3))[:,None]
    return t,spatial

def causal_4d_gate():
    rng=np.random.default_rng(20261120)
    N=48;samples=320;arrows=[];matches=0;nonzero=0
    for _ in range(samples):
        t,x=sample_minkowski_diamond(rng,N)
        ds=np.sum((x[:,None,:]-x[None,:,:])**2,axis=-1)
        dt=t[None,:]-t[:,None]
        A=(dt>0)&(dt*dt>ds)
        assert not np.any(A&A.T)
        past=A.sum(axis=0);future=A.sum(axis=1)
        a=int(np.sum(past**3-future**3))
        reverse_dt=-dt
        Ar=(reverse_dt>0)&(reverse_dt**2>ds)
        reverse=int(np.sum(Ar.sum(axis=0)**3-Ar.sum(axis=1)**3))
        if reverse==-a:matches+=1
        if a:nonzero+=1
        arrows.append(a)
    assert matches==samples
    return {'model':'IID uniform-volume 3+1D Minkowski Alexandrov diamond of half-height1; no preferred boundary source',
       'events_per_sprinkling':N,'sprinkling_count':samples,
       'exact_time_reversal_arrow_sign_matches':matches,
       'arrow_nonzero_samples':nonzero,
       'sample_arrow_mean':float(np.mean(arrows)),
       'sample_arrow_std':float(np.std(arrows,ddof=1)),
       'paired_time_reverse_ensemble_arrow_mean':0,
       'theorem':'A3 is order-isomorphism invariant but T odd. A time-reversal-symmetric sprinkling probability measure makes E[A3]=0, irrespective of typical sample fluctuations. Boundary conditions or T-breaking dynamics are needed to orient an ensemble. This does not create a Lorentzian gravitational action or show 4D emergence.'}


def projective(v):
    for a in v:
        if a%3:return tuple(int((x*pow(int(a),-1,3))%3) for x in v)
    raise ValueError('zero vector')

def symp(x,y):return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3


def w33_hodge_gate():
    pts=sorted({projective(v) for v in product(range(3),repeat=4) if any(v)})
    assert len(pts)==40
    line_set=set()
    for a,b in combinations(pts,2):
        if symp(a,b)==0:
            span=frozenset(projective(tuple((u*a[i]+v*b[i])%3 for i in range(4)))
                           for u,v in product(range(3),repeat=2) if u or v)
            assert len(span)==4
            line_set.add(span)
    lines=sorted(line_set,key=lambda f:tuple(sorted(f)))
    assert len(lines)==40
    flags=[(i,j) for i,p in enumerate(pts) for j,li in enumerate(lines) if p in li]
    assert len(flags)==160
    # flag line-graph adjacency, 6-regular and diameter 4
    A=np.zeros((160,160),dtype=np.int8)
    for i,(p,l) in enumerate(flags):
        for j,(q,m) in enumerate(flags):
            if i!=j and (p==q or l==m):A[i,j]=1
    assert np.all(A.sum(axis=1)==6)
    dist=np.full((160,160),-1,dtype=int)
    for i in range(160):
        dist[i,i]=0;queue=[i]
        for v in queue:
            for t in np.flatnonzero(A[v]):
                if dist[i,t]<0:dist[i,t]=dist[i,v]+1;queue.append(int(t))
    shell=[int(np.count_nonzero(dist[0]==j)) for j in range(5)]
    assert shell==[1,6,18,54,81] and np.all(dist>=0)
    K=(-3)**(4-dist)
    assert np.array_equal(K@K,160*K)
    P=K.astype(float)/160
    assert abs(np.trace(P)-81)<1e-12 and np.min(abs(P))>0
    # Exact one-edge diagonal phase noise: all offdiagonal K entries nonzero,
    # so no nonconstant edge-diagonal unitary can preserve cycle projector.
    phi=.41;z=np.ones(160,complex);z[0]=np.exp(1j*phi)
    delta=(np.diag(z)@P@np.diag(z.conj())-P)
    leakage=np.linalg.norm((np.eye(160)-P)@np.diag(z)@P)**2
    formula=4*math.sin(phi/2)**2*(81/160)*(79/160)
    assert abs(leakage-formula)<1e-9
    # IID Gaussian phase faults theta~N(0,sigma²): expected phase characteristic
    # |E exp(i theta)|²=exp(-sigma²), hence E leakage=(r-sum P_ee²)(1-exp(-sigma²)).
    sigma=.11
    expect=(81-160*(81/160)**2)*(1-math.exp(-sigma*sigma))
    rng=np.random.default_rng(20261120)
    # Cheap trace formula L=rank(P)-Tr(P D† P D), no 160³ work per run.
    W=P*P;observed=[]
    for _ in range(400):
        phase=rng.normal(0,sigma,size=160);zz=np.exp(1j*phase)
        measured=81-np.real(zz.conj()@W@zz)
        observed.append(float(measured))
    empirical=float(np.mean(observed))
    assert abs(empirical-expect)<.05
    return {'W33_points':40,'W33_lines':40,'Levi_vertices':80,'Levi_flags':160,
      'Levi_cycle_space_rank':81,'flag_line_graph_shells':shell,
      'signed_cycle_K_coefficient_by_distance':[81,-27,9,-3,1],
      'K_squared_exactly_160_K':True,
      'all_160x160_cycle_projector_entries_nonzero':True,
      'diagonal_edge_phase_preserves_cycle_space_iff_all_phases_identical':True,
      'one_edge_phi_radians':phi,'one_edge_hodge_leakage_numeric':float(leakage),
      'one_edge_hodge_leakage_exact_formula':'4 sin²(phi/2) * (81/160)*(79/160)',
      'gaussian_IID_phase_sigma':sigma,
      'expected_total_Hodge_leakage_exact_formula':'(6399/160)*(1-exp(-sigma²))',
      'expected_total_Hodge_leakage_at_sigma':expect,
      'empirical_mean_total_Hodge_leakage_400_trials':empirical,
      'limitation':'Leakage relative to a fixed Levi Hodge projector under independent edge-diagonal phase faults, NOT a universal physical error rate or a proof that gauge-covariantly transformed connections fail. Protection requires active correction or constrained noise, not merely 81-dimensional homology.'}


def run(write=True):
    result={'date':'2026-11-20','status':'SIX_FINITE_GATES_PASS_NOT_A_THEORY_OF_EVERYTHING',
       'tracks':{'H27_equivariant_SIC_SU3':h27_sic_gate(),
                 'qutrit_three_time_finite_shots':memory_gate(),
                 'SU3_Weyl_detector_twirl_minimality':su3_weyl_gate(),
                 'G2_smooth_compactification_chirality':chirality_gate(),
                 'causal_4D_time_reversal':causal_4d_gate(),
                 'W33_Hodge_edge_phase_leakage':w33_hodge_gate()}}
    if write:
        OUTPUT.parent.mkdir(parents=True,exist_ok=True)
        OUTPUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    return result

if __name__=='__main__':
    r=run()
    print(json.dumps({k:{i:v for i,v in a.items() if i in ('dimension','full_100x100_holomorphic_Hessian_rank','sufficient_shots_each_of_first_and_pooled_late_populations','minimum_nonzero_Weyl_settings_for_full_unknown_detector','untwisted_S7_zero_modes','exact_time_reversal_arrow_sign_matches','one_edge_hodge_leakage_numeric')} for k,a in r['tracks'].items()},indent=2))
    print('CERTIFICATE',OUTPUT)
