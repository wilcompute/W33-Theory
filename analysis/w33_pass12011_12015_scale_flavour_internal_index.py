"""Five conditional physics constructions after12006-12010.

Standard RG, spurion alignment, heat kernels and magnetic translations are
prior art. Fits and external internal geometry do not establish a TOE.
"""
from pathlib import Path
from collections import deque
from functools import lru_cache
import itertools,json,sys
import numpy as np
from scipy.integrate import solve_ivp,quad
from scipy.optimize import brentq
from scipy.special import expn
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass12007_shared_theta_leptons import inputs
from w33_pass11942_hypercharge_wilson_leptons import theta,normalised
from w33_pass12000_native_unitary_clock import native_paths
from w33_pass11952_11955_threshold_vacuum_loop_leptons import b0
MZ=91.1876
RG_FIT=np.array([-0.12113734813242999,-5.234395562960745,-0.13362993217135702,0.11291225431755648,0.04531505175636371,11.578209908337737,8.301819053990371,-2.6160682472868846,-9.88089638985497,-7.0309278582387895,10.73846537904411])
NAMES=['yb_ytau','mc_mt','mu_mc','ms_mb','md_ms','Vus','Vcb','Vub','J','mmu_mtau','me_mmu']
def pack(g,ms):return np.r_[g,np.array(ms).ravel()]
def unpack(x):return x[:3].real,x[3:].reshape(3,3,3)
def beta(t,x):
 g,ms=unpack(x);u,d,e=ms;hu=u@u.conj().T;hd=d@d.conj().T;he=e@e.conj().T;tr=np.trace(3*hu+3*hd+he).real;g1,g2,g3=g
 gu=17/12*g1*g1+9/4*g2*g2+8*g3*g3;gd=5/12*g1*g1+9/4*g2*g2+8*g3*g3;ge=15/4*g1*g1+9/4*g2*g2
 return pack(np.array([41/6,-19/6,-7])*g**3,[(1.5*(hu-hd)+(tr-gu)*np.eye(3))@u,(1.5*(hd-hu)+(tr-gd)*np.eye(3))@d,(1.5*he+(tr-ge)*np.eye(3))@e])/(16*np.pi**2)
phase=np.exp(1j*np.pi*np.arange(3)**2/3)
def theta_matrices(x):
 yy,eu=np.exp(x[:2]);p=x[2:10];tau=1+1j*yy;Ou=np.array([[tau,1j*eu],[1j*eu,tau]]);Od=np.array([[tau,1j*p[1]],[1j*p[1],1j*np.exp(p[0])]])
 u=(phase.conj()[:,None]*theta(Ou)*phase.conj()[None,:]).real
 d=(phase.conj()[:,None]*normalised(Od,(0,1j*p[2]))).real;e=(phase.conj()[:,None]*normalised(Od,(0,6j*p[2]))).real
 b=np.array([p[3],p[4]+1j*p[5],p[6]+1j*p[7]]);ee,O=np.linalg.eigh(np.eye(3)-np.outer(b.conj(),b)/(1+np.vdot(b,b).real));A=(O*np.sqrt(ee))@O.conj().T
 d=d@A;e=A.T@e.T
 return u,d,e,b,A

def shape_observables(mats):
    u,d,e=mats
    su=np.linalg.svd(u,compute_uv=False);sd=np.linalg.svd(d,compute_uv=False);se=np.linalg.svd(e,compute_uv=False)
    V=(np.linalg.svd(u)[0].conj().T@np.linalg.svd(d)[0])[::-1,::-1]
    return np.r_[sd[0]/se[0],su[1]/su[0],su[2]/su[1],sd[1]/sd[0],sd[2]/sd[1],abs(V[0,1]),abs(V[1,2]),abs(V[0,2]),(V[0,0]*V[1,1]*V[0,1].conj()*V[1,0].conj()).imag,se[1]/se[0],se[2]/se[1]]

@lru_cache(None)
def running():
    u,d,e,b,A=inputs();d=d@A;e=A.T@e.T;v=246.22
    mats=[m*np.sqrt(2)*mass/v/np.linalg.svd(m,compute_uv=False)[0] for m,mass in zip([u,d,e],[168.26,2.86,1.74624])]
    sol=solve_ivp(beta,[0,np.log(2e16/MZ)],pack([.3575,.6518,1.2177],mats),rtol=1e-10,atol=1e-13,dense_output=True)
    assert sol.success
    return sol

def rg_residual(x):
    target=shape_observables(unpack(running().sol(x[-1]))[1]);model=shape_observables(theta_matrices(x)[:3])
    residual=np.log(abs(model/target));residual[8]=(model[8]-target[8])/target[8]
    return residual

def rg_matching():
    sol=running();target=shape_observables(unpack(sol.sol(RG_FIT[-1]))[1]);model=shape_observables(theta_matrices(RG_FIT)[:3]);res=rg_residual(RG_FIT)
    assert max(abs(res))<1e-7
    initial=shape_observables(unpack(sol.sol(0))[1]);old=shape_observables([inputs()[0],inputs()[1]@inputs()[4],inputs()[4].T@inputs()[2].T])
    crossing=brentq(lambda t:shape_observables(unpack(sol.sol(t))[1])[0]-old[0],0,sol.t[-1])
    # Independent inverse flow from the matched spectrum/orbit at the scale.
    high=list(theta_matrices(RG_FIT)[:3]);high[0]*=np.linalg.svd(unpack(sol.sol(RG_FIT[-1]))[1][0],compute_uv=False)[0]/np.linalg.svd(high[0],compute_uv=False)[0]
    common=np.linalg.svd(unpack(sol.sol(RG_FIT[-1]))[1][1],compute_uv=False)[0]/np.linalg.svd(high[1],compute_uv=False)[0];high[1]*=common;high[2]*=common
    back=solve_ivp(beta,[RG_FIT[-1],0],pack(unpack(sol.sol(RG_FIT[-1]))[0],high),rtol=1e-10,atol=1e-13)
    backobs=shape_observables(unpack(back.y[:,-1])[1]);assert max(abs(backobs/initial-1))<1e-7
    jac=np.column_stack([(rg_residual(RG_FIT+1e-5*v)-rg_residual(RG_FIT-1e-5*v))/(2e-5) for v in np.eye(11)])
    return dict(status='PASS',names=NAMES,fitted_coordinates=RG_FIT.tolist(),matching_scale_GeV=float(MZ*np.exp(RG_FIT[-1])),log_matching_scale=float(RG_FIT[-1]),running_target=target.tolist(),theta_match=model.tolist(),residual=res.tolist(),back_to_MZ_max_relative_error=float(max(abs(backobs/initial-1))),local_Jacobian_singular_values=np.linalg.svd(jac,compute_uv=False).tolist(),old_texture_crossing_GeV=float(MZ*np.exp(crossing)),old_texture_shape_drift_at_crossing=(shape_observables(unpack(sol.sol(crossing))[1])/initial-1).tolist(),gauge_at_matching=unpack(sol.sol(RG_FIT[-1]))[0].tolist(),beta_convention='Yu,Yd share left Q index; betaYu=[3/2(Hu-Hd)+T-gu]Yu/(16pi2), betaYd=[3/2(Hd-Hu)+T-gd]Yd/(16pi2), betaYe=[3/2He+T-ge]Ye/(16pi2); hypercharge gprime, b=(41/6,-19/6,-7); T=Tr(3Hu+3Hd+He).',inputs='Prior12007 dimensionless MZ comparators; supplied MZ=91.1876,v=246.22,top=168.26,bottom=2.86,tau=1.74624GeV; gprime=.3575,g2=.6518,g3=1.2177. SM one-loop below freely fitted matching scale. No SUSY or vectorlike finite matching thresholds; heavy species integrated out.',boundary='Eleven fitted shape/scale coordinates match eleven comparisons: NOT a prediction of the matching scale or constants. Updated experimental inputs, two-loop running, thresholds and unified gauge breaking remain uncomputed. Matching scale is not a GUT claim. The previous four neutrino comparators must be rematched on this new branch, including Weinberg running; they are not inherited.',prior=['11942 charge6 theta family','12005/12007 CP-real theta/Barr matching','11298 actual distinct E6 mediator running','0712.1419,hep-ph/0207271 standard SM running','2510.01312 updated data available but not substituted silently'])

def hermitian_basis(n,traceless=False):
    out=[]
    for i in range(n):
        for j in range(i):
            a=np.zeros((n,n),complex);a[i,j]=a[j,i]=1;out.append(a)
            a=np.zeros((n,n),complex);a[i,j]=1j;a[j,i]=-1j;out.append(a)
    for i in range(n-1 if traceless else n):
        a=np.zeros((n,n),complex);a[i,i]=1
        if traceless:a[-1,-1]=-1
        out.append(a)
    return out

def stabilizer(mats=None):
    if mats is None:mats=theta_matrices(RG_FIT)[:3]
    u,d,_=mats;H=[m@m.conj().T/np.linalg.norm(m@m.conj().T) for m in (u,d)]
    cols=[]
    for a in hermitian_basis(3):
        z=np.concatenate([(a@h-h@a).ravel() for h in H]);cols.append(np.r_[z.real,z.imag])
    sv=np.linalg.svd(np.array(cols).T,compute_uv=False)
    val,V=np.linalg.eigh(H[0]);D=V.conj().T@H[1]@V;off=[float(abs(D[i,j])) for i,j in itertools.combinations(range(3),2)]
    assert min(np.diff(val))>1e-8 and min(off)>1e-7
    assert sv[-2]>1e-6 and sv[-1]<1e-12
    comm=H[0]@H[1]-H[1]@H[0];cp=float(np.trace(comm@comm@comm).imag)
    return dict(status='PASS',U3_commutant_real_dimension=1,SU3_continuous_stabilizer_dimension=0,SU3_stabilizer='Z3 center',commutator_map_singular_values=sv.tolist(),up_Gram_eigenvalues=val.tolist(),down_offdiagonal_in_up_basis=off,normalized_CP_odd_cubic=cp,proof='Distinct up eigenvalues force every commuting unitary to be diagonal in that eigenbasis. Connected nonzero offdiagonal down support forces all three phases equal. U3 common stabilizer=U1; intersect SU3 gives Z3 center. This proof covers the displayed generic pair; numerical margins verify its hypotheses.',selection_boundary='A generic realistic pair has no enhanced continuous common flavour stabilizer to pin its fitted coordinates. This does not rule out spontaneous breaking to the center, generalized CP/modular combined actions or a potential with generic minima. No vacuum potential or modulus stabilization is derived. Full gauge representations and right flavour rotations must be specified separately.',prior=['11921 magnetic flavour qutrit','11923 stabilizer Higgs lock','11927 geometric local-adjoint spurions','11321/11326 explicit CP vacua do not select observed CKM'])

def spectral_soft(M):
    left=M@M.conj().T;right=M.conj().T@M;scale=np.linalg.norm(left,2)
    L=left+4*np.eye(len(M))+.2*left@left/scale
    R=right+5*np.eye(len(M))+.3*right@right/scale
    LR=(.3*np.eye(len(M))+.07*left/scale+.02*left@left/scale**2)@M
    return np.block([[L,LR],[LR.conj().T,R]])

def colored_phase(M,Sq,mg=.7,alpha=.1):
    n=len(M);ev,Z=np.linalg.eigh(Sq);assert min(ev)>0
    F=(Z*np.array([b0(np.array([mg*mg]),v)[0] for v in ev]))@Z.conj().T;delta=2*alpha/(3*np.pi)*mg*F[:n,n:];quark=float(np.trace(np.linalg.solve(M,delta)).imag)
    U,sv,Vh=np.linalg.svd(M);ZL=U.conj().T@Z[:n];ZR=Vh@Z[n:];dg=0j
    for i,m in enumerate(sv):dg+=alpha/(2*np.pi)*m*np.sum(ZL[i]*ZR[i].conj()*np.array([b0(np.array([m*m]),v)[0] for v in ev]))
    return dict(quark=quark,gluino=float(-3*dg.imag/mg),sum=float(quark-3*dg.imag/mg),minimum_soft_eigenvalue=float(min(ev)))

def spurion_alignment():
    u,d,e,b,A=theta_matrices(RG_FIT);bare=d@np.linalg.inv(A);bare/=np.linalg.norm(bare)
    M=np.zeros((4,4),complex);M[:3,:3]=bare;M[3,:3]=b;M[3,3]=1
    safe=colored_phase(M,spectral_soft(M));assert abs(safe['sum'])<1e-10
    # Negative control: another noncommuting spurion with allowed real coefficient.
    Sq=spectral_soft(M);pattern=np.arange(16).reshape(4,4)/7-1;leak=.01*pattern*M;Sq[:4,4:]+=leak;Sq[4:,:4]+=leak.conj().T;bad=colored_phase(M,Sq)
    return dict(status='PASS',nonuniversal_spectral_alignment=safe,misaligned_control=bad,exact_theorem='For a single invertible complex spurion M, LL=f(MMdag), RR=g(MdagM), LR=h(MMdag)M, all real functions on positive spectra, become independent real2x2 blocks in the singular basis. All real loop spectral functions give real determinant-trace and gluino channels. Universality is sufficient but not necessary.',group_action='The mass-sector statement is equivariant under U(n)L x U(n)R spurion transformations M->UL M URdag. For full4x4 Barr block the heavy singlet and light weak-doublet left fields have different unbroken electroweak representations: this enlarged mass-basis covariance is NOT automatically an ultraviolet flavour symmetry.',boundary='Conditional protection of the specified colored one-loop mass phases. Gauge mediation, multi-spurion running, neutral portal, forbidden operators and SUSY breaking still need a single gauge-invariant UV action. No total theta bound or all-orders MFV claim.',prior=['12008 universal special case','11978 F/VEV phase shielding','2002.04204 and0807.0801 MFV/mediation literature'])

def tree_eigenvalues():
    edges,V,paths,tree,T,words=native_paths();L=np.zeros((27,27))
    for e in tree:
        a,b=edges[e];L[a,a]+=1;L[b,b]+=1;L[a,b]-=1;L[b,a]-=1
    ev=np.linalg.eigvalsh(L);ev[0]=0;return ev

def induced_scale():
    ev=tree_eigenvalues();rows=[]
    for kappa in [0.,.1,1.,4*27**2]:
        x=kappa*ev;F2=float(sum(expn(2,x)));F4=float(sum(expn(3,x)))
        assert 0<F2<=27.00001 and 0<F4<=13.50001
        rows.append(dict(kappa=kappa,dimensionless_optical_masses_squared=x.tolist(),curvature_effective_species=F2,vacuum_effective_moment=F4,G_times_cutoff_squared=12*np.pi/F2,absolute_vacuum_over_reduced_Planck_fourth=288*np.pi**2*F4/F2**2))
    return dict(status='PASS',native_tree_eigenvalues=ev.tolist(),rows=rows,action='Conditional27 real minimally coupled scalar tower Pj=-Delta_g+kappa*lambda_j/a2 with all modes sharing the12009 capacity-completed continuum metric. Lambda=1/a; frozen internal tree spectrum, no varying eigenvector/Berry terms. This is a supplied scalar extension, not the fermionic Wilson optical spectrum or full physical SM inventory.',proper_time='Gamma=-1/2 integral_(a2)^infinity ds/s Tr exp(-sP). F2(x)=E2(x),F4(x)=E3(x). Gamma_R=-Lambda2 sumF2 R/(192pi2); compare Euclidean EH -R/(16piG) gives G Lambda2=12pi/sumF2. Gamma0=-Lambda4 sumF4/(32pi2). Nonminimal xi multiplies each curvature term by(1-6xi).',scope='Native27 sites do not mean27 light gravitational species. Actual12002 optical coefficient2916 leaves only the acoustic mode below cutoff in this scalar diagnostic. Conformal xi=1/6 removes scalar induced EH term. Regulator moments, bare counterterms, field inventory and physical a remain supplied; no predicted Newton constant, observed cosmological constant, Lorentzian dynamics or constraint algebra.',prior=['11601 heat/metric warning','11604/11615 actual inventory and proper-time integrals','12002 native tree optical regulator','12009 capacity density map'])

def internal_flux(length=6,charge=3):
    n=length**2;B=2*np.pi*charge/n;cells=list(itertools.product(range(length),repeat=2));idx={x:i for i,x in enumerate(cells)};U=np.ones((n,2),complex)
    for i,(x,y) in enumerate(cells):
        U[i,0]=np.exp(-1j*B*y)
        if y==length-1:U[i,1]=np.exp(1j*B*length*x)
    S=[]
    for mu in range(2):
        a=np.zeros((n,n),complex)
        for i,c in enumerate(cells):
            d=list(c);d[mu]=(d[mu]+1)%length;a[i,idx[tuple(d)]]=U[i,mu]
        S.append(a)
    sx=np.array([[0,1],[1,0]]);sy=np.array([[0,-1j],[1j,0]]);g5=np.kron(np.diag([1,-1]),np.eye(n));D=np.eye(2*n,dtype=complex)
    for g,a in zip([sx,sy],S):D-=.5*(np.kron(np.eye(2)-g,a)+np.kron(np.eye(2)+g,a.conj().T))
    ev,V=np.linalg.eigh(g5@D);sign=(V*np.sign(ev))@V.conj().T;Do=np.eye(2*n)+g5@sign;z,W=np.linalg.eigh(Do.conj().T@Do);K=W[:,z<1e-10]
    return cells,idx,U,S,g5,D,ev,Do,z,K

def magnetic_translation(cells,idx,U,step):
    n=len(cells);length=round(np.sqrt(n));r=np.full(n,np.nan+0j);r[0]=1;queue=deque([0])
    while queue:
        i=queue.popleft();c=cells[i];ci=idx[tuple((c[k]+step[k])%length for k in range(2))]
        for mu in range(2):
            d=list(c);d[mu]=(d[mu]+1)%length;j=idx[tuple(d)];want=r[i]*U[ci,mu]/U[i,mu]
            if np.isnan(r[j]):r[j]=want;queue.append(j)
            else:assert abs(r[j]-want)<1e-10
    P=np.zeros((n,n),complex)
    for i,c in enumerate(cells):P[i,idx[tuple((c[k]+step[k])%length for k in range(2))]]=r[i]
    return P

def sm_embedding(g3,g2,z):
    """Standard integer-6Y embedding, not a new unification mechanism."""
    V=np.zeros((5,5),complex);V[:3,:3]=z**-2*g3;V[3:,3:]=z**3*g2
    return V

def wedge2(V):
    pairs=list(itertools.combinations(range(len(V)),2))
    return np.array([[V[i,k]*V[j,l]-V[i,l]*V[j,k] for k,l in pairs] for i,j in pairs])

def measure_restriction():
    from scipy.linalg import expm
    rng=np.random.default_rng(12015)
    def group(n):
        A=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));A=(A+A.conj().T)/2;A-=np.trace(A)*np.eye(n)/n
        return expm(.03j*A)
    a3,b3=group(3),group(3);a2,b2=group(2),group(2);z,w=np.exp(.02j),np.exp(-.03j)
    A=sm_embedding(a3,a2,z);B=sm_embedding(b3,b2,w)
    assert np.linalg.norm(A@B-sm_embedding(a3@b3,a2@b2,z*w))<1e-12
    assert np.linalg.norm(wedge2(A@B)-wedge2(A)@wedge2(B))<1e-12
    center=sm_embedding(np.exp(2j*np.pi/3)*np.eye(3),-np.eye(2),np.exp(1j*np.pi/3))
    assert np.linalg.norm(center-np.eye(5))<1e-12
    fundamental=[-2]*3+[3]*2
    charges10=[fundamental[i]+fundamental[j] for i,j in itertools.combinations(range(5),2)]
    assert sorted(charges10)==[-4]*3+[1]*6+[6]
    delta=np.linalg.norm(A-np.eye(5),2)
    assert np.linalg.norm(wedge2(A)-np.eye(10),2)<=2*delta+1e-12
    return dict(embedding='diag(z^-2 g3,z^3 g2)',kernel='Z6 generated by(exp(2pi i/3)I3,-I2,exp(pi i/3))',ten_integer_6Y_charges=charges10,bar5_integer_6Y_charges=[-q for q in fundamental],homomorphism_error=float(np.linalg.norm(A@B-sm_embedding(a3@b3,a2@b2,z*w))),wedge_homomorphism_error=float(np.linalg.norm(wedge2(A@B)-wedge2(A)@wedge2(B))),admissibility_bound='For an SU5 plaquette P, ||wedge2(P)-I||<=2||P-I||. Sufficient SM lifted bounds are ||P3-I||+|zP^-2-1|<delta and ||P2-I||+|zP^3-1|<delta. Numerical flux backgrounds here are NOT asserted to meet the much stronger uniform bounds of a global measure theorem.',scope='Standard restriction map independently tested. Not an implementation or independent proof of Craig2610.09093, its current, refinement maps, locality or global integrability. Native path/tree transfer remains conditional on those hypotheses and bounded gauge-covariant conjugation.')

def internal_family():
    cells,idx,U,S,g5,D,ev,Do,z,K=internal_flux();n=len(cells);assert K.shape[1]==3
    X=magnetic_translation(cells,idx,U,(2,0));Y=magnetic_translation(cells,idx,U,(0,2));omega=np.exp(-2j*np.pi/3)
    Xs=np.kron(np.eye(2),X);Ys=np.kron(np.eye(2),Y);x=K.conj().T@Xs@K;y=K.conj().T@Ys@K
    assert max(np.max(abs(T@D-D@T)) for T in (Xs,Ys))<1e-11
    assert np.linalg.norm(x@y-omega*y@x)<1e-11
    assert max(np.linalg.norm(np.linalg.matrix_power(T,3)-np.eye(3)) for T in (x,y))<1e-11
    chars=[abs(np.trace(np.linalg.matrix_power(x,a)@np.linalg.matrix_power(y,b))) for a,b in itertools.product(range(3),repeat=2) if (a,b)!=(0,0)]
    assert max(chars)<1e-11
    # Fourier multiplier gives a genuine, generally non-scalar family operator.
    F=np.diag(np.exp(2j*np.pi*np.array([c[0] for c in cells])/6));proj=K.conj().T@np.kron(np.eye(2),F)@K
    gap=float(min(abs(ev)));index=int(-sum(np.sign(ev))/2)
    return dict(status='PASS',internal_lattice=[6,6],supplied_flux=3,overlap_index=index,zero_modes=K.shape[1],kernel_gap=gap,first_nonzero_DdagD=float(z[3]),zero_mode_chiralities=np.linalg.eigvalsh(K.conj().T@g5@K).tolist(),Heisenberg_phase_real_imag=[float(omega.real),float(omega.imag)],restricted_commutator_error=float(np.linalg.norm(x@y-omega*y@x)),noncentral_character_max=float(max(chars)),projected_fourier_singular_values=np.linalg.svd(proj,compute_uv=False).tolist(),X_real=x.real.tolist(),X_imag=x.imag.tolist(),Y_real=y.real.tolist(),Y_imag=y.imag.tolist(),group_statement='Translations by2 sites, with solved gauge compensators, commute with the finite2D overlap kernel. Their action on its3 zero modes has X3=Y3=I,XY=omega YX; noncentral characters vanish. This is the irreducible3D H27 module with nontrivial central character. Any Hermitian operator commuting with both is scalar (Schur), so nondegenerate masses need symmetry breaking.',family_reading='An EXTERNAL internal2D compactification with flux3 supplies3 chiral zero modes. It is different from4D spacetime instanton index, which does NOT count independent generations. Product compactification, flux/size stabilization, SM embedding, all unwanted modes and interactions remain supplied/open. Original native4D W33 model alone does not contain this added torus.',measure_frontier='New external preprint Craig2610.09093v1 (2026-10-06) CLAIMS nonperturbative nonAbelian overlap measure, including SM via10+bar5 SU5 restriction. Its hypotheses/current/global proof are not independently certified here; repository native pullback/admissibility/current implementation remain open. Do not describe the literature as simply lacking any proposed construction.',prior=['11921 flux-selected two flavour qutrits','11927 Fourier-mode Pauli spurions','11588 external/internal tensor index distinction','12010 native SU3 spacetime index, not family count','0812.1426 magnetic translation prior art','1001.1788 magnetized flavour prior art'])

def payload():
    family=internal_family();family['measure_restriction']=measure_restriction()
    return dict(status='PASS',pass12011=rg_matching(),pass12012=stabilizer(),pass12013=spurion_alignment(),pass12014=induced_scale(),pass12015=family)

if __name__=='__main__':
    out=payload();path=ROOT/'data/w33_pass12011_12015_scale_flavour_internal_index.json';path.write_text(json.dumps(out,indent=2)+'\n');print('PASS',out['pass12011']['matching_scale_GeV'],out['pass12015']['overlap_index'])
