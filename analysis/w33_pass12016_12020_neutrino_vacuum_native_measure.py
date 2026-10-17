"""Five explicit followups; conditional EFT and native operator results.

No fitted potential coefficients, messenger/flux inputs or cutoff units are
asserted to be predictions. General RGE, invariant and overlap methods are prior art.
"""
from pathlib import Path
from functools import lru_cache
import sys,json,itertools,math
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12011_12015_scale_flavour_internal_index as prior
from w33_pass12007_shared_theta_leptons import NEUTRINO_TARGET
from w33_pass11995_native_metric_gr_lift import inputs as metric_inputs,homogenize
from w33_pass11991_native_four_period_cover import gamma4
LOOP=16*np.pi**2
NU_FIT=np.array([0.17949509395694016, -0.4295888152402716, 0.9583199350202315, -1.0661365699775118, -0.37716229548993896])

@lru_cache(None)
def lepton_running():
    u,d,e,b,A=prior.theta_matrices(prior.RG_FIT);high=prior.unpack(prior.running().sol(prior.RG_FIT[-1]))[1]
    e=e*np.linalg.svd(high[1],compute_uv=False)[0]/np.linalg.svd(d,compute_uv=False)[0]
    ue=np.linalg.eigh(e.conj()@e.T)[1]
    # Remove universal C5 factor: it does not affect angles/ratios and is fixed by Delta31.
    def rhs(t,x):
        g,m=prior.unpack(prior.running().sol(t));ell=np.linalg.svd(m[2],compute_uv=False)[::-1]**2
        T=sum(np.trace(k@k.conj().T).real*c for k,c in zip(m,[3,3,1]));P=ell/LOOP
        q1=-1.5*P;q2=-(57/16*g[0]**2-33/16*g[1]**2-5*T/4)*P/LOOP+19/4*P**2
        return np.r_[(q1[:,None]+q1[None,:]).ravel(),(q1[:,None]+q1[None,:]+q2[:,None]+q2[None,:]+2*np.outer(P,P)).ravel()]
    val=solve_ivp(rhs,[prior.RG_FIT[-1],0],np.zeros(18),rtol=1e-11,atol=1e-14).y[:,-1]
    return A,ue,np.exp(val[:9].reshape(3,3)),np.exp(val[9:].reshape(3,3))

def neutrino_observables(parameters=NU_FIT,two_loop=True):
    A,ue,F1,F2=lepton_running();L=np.array([[np.exp(parameters[0]),0,0],[parameters[2],np.exp(parameters[1]),0],[parameters[3],parameters[4],1.]])
    C=ue.T@(A.T@(L@L.T)@A)@ue;C=C*(F2 if two_loop else F1)
    _,ss,vh=np.linalg.svd(C);ids=np.argsort(ss);ss=ss[ids];U=vh.conj().T[:,ids];Q=abs(U)**2;s13=Q[0,2]
    out=np.array([Q[0,1]/(1-s13),Q[1,2]/(1-s13),s13,(ss[1]**2-ss[0]**2)/(ss[2]**2-ss[0]**2)])
    J=float((U[0,0]*U[1,1]*U[0,1].conj()*U[1,0].conj()).imag);scale=np.sqrt(.002511/(ss[2]**2-ss[0]**2))
    return out,dict(J=J,masses_eV=(ss*scale).tolist(),PMNS_abs_squared=Q.tolist())

def threshold_residual(x,delta):
    out=prior.rg_residual(x);out[0]+=np.log1p(delta);return out

def neutrino_thresholds():
    o,details=neutrino_observables();one,_=neutrino_observables(two_loop=False)
    assert max(abs(o/NEUTRINO_TARGET-1))<1e-6
    rows=[]
    for delta in [-.01,.01]:
        fit=least_squares(lambda x:threshold_residual(x,delta),prior.RG_FIT,max_nfev=200,xtol=1e-10,ftol=1e-10,gtol=1e-10,diff_step=1e-5)
        assert max(abs(fit.fun))<1e-6
        rows.append(dict(universal_down_threshold=delta,scale_GeV=float(prior.MZ*np.exp(fit.x[-1])),parameters=fit.x.tolist(),max_log_residual=float(max(abs(fit.fun)))))
    return dict(status='PASS',neutrino_parameters=NU_FIT.tolist(),oscillation_targets=NEUTRINO_TARGET.tolist(),matched=o.tolist(),details=details,two_loop_minus_one_loop=(o-one).tolist(),threshold_refits=rows,
        shape_RGE='C5 universal scalar factor removed. In charged eigenbasis P_i=y_i^2/(16pi2), q_i=-3P_i/2-[57gprime2/16-33g2^2/16-5T/4]P_i/(16pi2)+19P_i^2/4. Entrywise dCij/dlnmu=(qi+qj+2PiPj)Cij. Exact two-loop flavour-dependent C5 terms from2411.08011 eq24, evaluated on ONE-LOOP SM background.',
        scope='Fifteen fitted comparisons on common12011 branch:11 charged/quark plus4 neutrino. Five real Majorana shapes fit4 constraints, so masses/J are witness values, not predictions. Universal C5 running absorbed into supplied Delta31 normalization. This is NOT a complete two-loop SM+BSM matching fit. Threshold deltas are supplied matching deformations, not computed heavy-particle threshold coefficients.',prior=['12007 real Majorana construction','12011 shared running branch','2411.08011 equations20-24'])

A_SPEC=np.array([1.,2.,4.]);B_SPEC=np.array([1.,3.,7.])
def projection(X,values,i):
    j,k=[j for j in range(3) if j!=i]
    return (X-values[j]*np.eye(3))@(X-values[k]*np.eye(3))/((values[i]-values[j])*(values[i]-values[k]))
def dprojection(X,dX,values,i):
    j,k=[j for j in range(3) if j!=i]
    return (dX@(X-values[k]*np.eye(3))+(X-values[j]*np.eye(3))@dX)/((values[i]-values[j])*(values[i]-values[k]))
def invariants(A,B):
    return np.r_[[np.trace(np.linalg.matrix_power(A,k)).real for k in (1,2,3)],[np.trace(np.linalg.matrix_power(B,k)).real for k in (1,2,3)],[np.trace(projection(A,A_SPEC,i)@projection(B,B_SPEC,j)).real for i in (0,1) for j in (0,1)]]
def invariant_derivative(A,B,dA,dB):
    return np.r_[[k*np.trace(np.linalg.matrix_power(A,k-1)@dA).real for k in (1,2,3)],[k*np.trace(np.linalg.matrix_power(B,k-1)@dB).real for k in (1,2,3)],[np.trace(dprojection(A,dA,A_SPEC,i)@projection(B,B_SPEC,j)+projection(A,A_SPEC,i)@dprojection(B,dB,B_SPEC,j)).real for i in (0,1) for j in (0,1)]]
def flavour_home():
    u,d,*_=prior.theta_matrices(prior.RG_FIT);Ua=np.linalg.eigh(u@u.conj().T)[1];Ub=np.linalg.eigh(d@d.conj().T)[1];V=Ua.conj().T@Ub
    return np.diag(A_SPEC),(V*B_SPEC)@V.conj().T

def flavour_potential():
    A,B=flavour_home();basis=[z/np.linalg.norm(z) for z in prior.hermitian_basis(3)];zero=np.zeros((3,3));target=invariants(A,B)
    J=np.column_stack([invariant_derivative(A,B,z,zero) for z in basis]+[invariant_derivative(A,B,zero,z) for z in basis]);weights=1/np.linalg.norm(J,axis=1);J=weights[:,None]*J;sv=np.linalg.svd(J,compute_uv=False)
    assert sv[-1]>1e-5
    gauge=[]
    for T in prior.hermitian_basis(3,True):
        da=1j*(T@A-A@T);db=1j*(T@B-B@T);gauge.append([np.trace(z@da).real for z in basis]+[np.trace(z@db).real for z in basis])
    orbit=np.array(gauge).T;assert np.linalg.matrix_rank(orbit)==8 and np.linalg.norm(J@orbit)<1e-10
    assert max(abs(invariants(A.conj(),B.conj())-target))<1e-12
    return dict(status='PASS',target_invariants=target.tolist(),weights=weights.tolist(),normal_Hessian_eigenvalues=(2*sv**2).tolist(),positive_normal_modes=10,symmetry_zero_modes=8,orbit_annihilation_error=float(np.linalg.norm(J@orbit)),potential='V=mu0^4 sum_r w_r^2 (I_r(A,B)-c_r)^2; I=TrA^k,TrB^k k1..3 andTr(Pi(A)Qj(B)) i,j0,1 with Lagrange spectral polynomials degree2. CP-even, simultaneousU3 invariant, positive degree8 polynomial. c_r andw_r are supplied.',scope='Explicit stable local orientation-flavon vacuum with observed CKM orbit and its conjugate at engineered target invariants. Auxiliary Hermitian spectra(1,2,4),(1,3,7) are supplied, not physical masses. Full18-field Hessian has10 positive normal directions and8 symmetry tangents. This does not dynamically derive coefficients, choose CP sign, stabilize theta moduli or construct a renormalizable UV potential. Prior11967 mixed-trace alignment obstruction is evaded by multiple higher-degree invariants, not contradicted.',prior=['11967 spectral-potential/alignment obstruction','11321/11326 explicit CP-breaking flavour potentials','12012 generic stabilizer'])

def gauge_mediation():
    messenger=1e6;Lambda=2e5;softscale=2e3
    g,_=prior.unpack(prior.running().sol(np.log(messenger/prior.MZ)));g=g.copy();g[0]*=np.sqrt(5/3)
    # Leading small-F/M^2 messenger formula; exact finite-x functions omitted.
    gaugino=Lambda*g*g/LOOP
    qmass2=2*Lambda**2*np.dot([1/60,3/4,4/3],g**4)/LOOP**2
    dmass2=2*Lambda**2*np.dot([1/15,0,4/3],g**4)/LOOP**2
    a=-np.log(messenger/softscale)*np.dot([14/15,6,32/3],g*g*gaugino)/LOOP
    _,d,*_=prior.theta_matrices(prior.RG_FIT);d=d*2.86/np.linalg.svd(d,compute_uv=False)[0]
    LR=a*d;Sq=np.block([[d@d.conj().T+qmass2*np.eye(3),LR],[LR.conj().T,d.conj().T@d+dmass2*np.eye(3)]])
    theta=prior.colored_phase(d,Sq,mg=gaugino[2],alpha=g[2]**2/(4*np.pi));assert abs(theta['sum'])<1e-10
    # Leading cross-spurion LL insertion; Hermitian but not spectral in down mass.
    u=prior.theta_matrices(prior.RG_FIT)[0];u=u/np.linalg.norm(u);Hu=u@u.conj().T
    eps=1e-5
    def phase(eps):
        trial=Sq.copy();trial[:3,:3]+=eps*qmass2*Hu
        return prior.colored_phase(d,trial,mg=gaugino[2],alpha=g[2]**2/(4*np.pi))['sum']
    derivative=(phase(eps)-phase(-eps))/(2*eps) # noise diagnostic only; exact one-sided theorem below applies
    return dict(status='PASS',messenger_GeV=messenger,F_over_M_GeV=Lambda,F_over_M2=Lambda/messenger,gluino_and_EW_gaugino_GeV=gaugino.tolist(),Q_soft_mass_GeV=float(np.sqrt(qmass2)),dc_soft_mass_GeV=float(np.sqrt(dmass2)),leading_log_Ad_GeV=float(a),colored_threshold=theta,cross_spurion_finite_difference_noise=float(derivative),one_sided_exact_result='The single LL Hermitian perturbation with RR/LR diagonal in mass basis has zero colored phase exactly; finite-difference derivative is cancellation noise, not a physical susceptibility.',messenger_superpotential='W=X Phi Phibar withPhi+Phibar=5+bar5, X=M+theta2 F real, no direct matter/CP-sector couplings. Canonical light fields and CP/heavy thresholds integrated out ABOVE messenger.',scope='Gauge-invariant post-heavy minimal gauge-mediation boundary, A=0 at messenger and gauge-only leading-log real Ad. Two-loop scalar/one-loop gaugino leading small-x formulas; finite x=.2 corrections, messenger stability/global SUSY vacuum, Yukawa running, neutralportal and fullradiative theta uncomputed. SUSYbenchmark is NOT silently spliced into priorSM-only runningfit; SM-MSSM thresholds and allphysicalcouplings require rematching.',prior=['11965/11973 mediation framework','11978 actual soft phase shielding','12013 spectral safe class','hep-ph/9801271 standard gauge mediation'])

def one_sided_alignment():
    rng=np.random.default_rng(12018);M=np.diag([.2,.7,1.4]);z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));L=5*np.eye(3)+.15*(z+z.conj().T);R=np.diag([6.,7.,8.]);LR=.3*M;Sq=np.block([[L,LR],[LR,R]])
    one=prior.colored_phase(M,Sq);assert abs(one['sum'])<1e-12
    z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));Sq[3:,3:]+=.15*(z+z.conj().T);two=prior.colored_phase(M,Sq);cp=prior.colored_phase(M,Sq.conj())
    assert abs(two['sum'])>1e-8 and abs(two['sum']+cp['sum'])<1e-12
    return dict(status='PASS',one_sided=one,both_sides=two,CP_partner=cp,proof='In mass SVD basis, RR=diag(r), LR=diag(ell) real, LL arbitrary Hermitian. For realz outside spectrum, resolventLR=[z-LL-ell(z-RR)^-1ell]^-1 ell(z-RR)^-1 has REAL diagonal entries. Its spectral residues on each degenerate eigenspace are real. Thus every real spectral loop function has real LRii. Both ImTr(M^-1deltaM) and each species-weighted gluino phase vanish. SwappingL/R gives the partner theorem.',scope='Specified colored one-loop self-energy phases only. A leading top-Yukawa LL insertion alone cannot defeat this safe class; simultaneous opposite-side or LR misalignment, neutral portals and higher loops still need calculation. Mass-basis covariance does not assert a new UVgauge/flavour symmetry.',prior=['12008 universal alignment','12013 spectral-function sufficient class'])

@lru_cache(None)
def exact_native_dispersion():
    b,v,_,H=metric_inputs();b=s.Matrix(np.c_[-b.sum(1),b].astype(int));v=s.Matrix(v.astype(int));M=s.sqrt(H.det());n=27;p=s.symbols('p0:4',real=True);cs=v*s.Matrix(p);C=[b.T*b/M]
    for r in range(1,5):
        L=s.zeros(n)
        for e in range(135):
            a=next(i for i in range(n) if b[e,i]==-1);z=next(i for i in range(n) if b[e,i]==1)
            L[a,z]-=(s.I*cs[e])**r/s.factorial(r)/M;L[z,a]-=(-s.I*cs[e])**r/s.factorial(r)/M
        C.append(L)
    Inv=(C[0]+s.ones(n)/n).inv();U=[s.ones(n,1)];lam=[s.Integer(0)]
    for r in range(1,5):
        rhs=sum((C[j]*U[r-j] for j in range(1,r+1)),s.zeros(n,1));val=s.expand(sum(rhs)/n);lam.append(val)
        if r<4:
            rhs=-rhs+sum((lam[j]*U[r-j] for j in range(1,r+1)),s.zeros(n,1));U.append((Inv*rhs).applyfunc(s.expand))
    assert lam[1]==lam[3]==0 and s.expand(lam[2]-(s.Matrix(p).T*(H/M)*s.Matrix(p))[0])==0
    return b,v,M,p,lam

def native_continuum():
    b,v,M,p,lam=exact_native_dispersion();direction=s.Matrix([s.Rational(7,10),-s.Rational(3,10),s.Rational(1,5),s.Rational(1,2)]);sub=dict(zip(p,direction));quadratic=float(lam[2].subs(sub));quartic=lam[4].subs(sub);rows=[]
    bf=np.array(b,float);vf=np.array(v,float);q=np.array(direction,float).ravel()
    for a in [.16,.08,.04,.02]:
        B=bf.astype(complex).copy()
        for e in range(135):B[e,np.flatnonzero(bf[e]>0)[0]]*=np.exp(1j*a*(vf[e]@q))
        ev=np.linalg.eigvalsh(B.conj().T@B/float(M));value=ev[0]/a**2;rows.append(dict(a=a,physical_eigenvalue=float(value),quadratic_error=float(value-quadratic),quartic_estimate=float((value-quadratic)/a**2)))
    ratio=s.expand(lam[4]).coeff(p[0],4)/s.expand(lam[2]**2).coeff(p[0],4);anisotropic=s.expand(lam[4]-ratio*lam[2]**2);assert anisotropic!=0
    return dict(status='PASS',native_capacity=str(M),exact_quadratic=str(lam[2]),exact_quartic=s.factor(lam[4]).__str__(),quartic_monomials=len(s.Poly(lam[4],*p).terms()),direction_quartic=str(quartic),refinement=rows,derivation='Expand actual135-edge27siteBloch operator B(k)dagB(k)/M to fourthorder. Solve mean-zero eigenvector correctors with (L0+11T/27)^-1. Fredholm solvability gives everylambda_n exactly;lambda1=lambda3=0. Physicallambda(a p)/a2=q2(p)+a2 q4(p)+O(a4).',scope='Exact flat native acoustic effective operator and explicit anisotropic higherderivative lattice correction. q4 is not proportionalq2^2. This establishes a flatlongwavelength/principalmetric refinement test, not curved homogenization, spinconnection, renormalizedEH/Newton/Lambda, Lorentzsignature or nonlinearconstraintclosure. Spacinga remains supplied in hbar=c=1 units.',prior=['11991 native4periodcover','11995 harmonicmetric','12009 capacitycompletion','12014 conditional scalarheat tower'])

def word_product(word,links):
    out=np.eye(links[0].shape[0],dtype=complex)
    for e,sign in word:out=out@(links[e] if sign==1 else links[e].conj().T)
    return out

def word_derivative(word,links,edge,A):
    n=links[0].shape[0];factors=[links[e] if sign==1 else links[e].conj().T for e,sign in word];out=np.zeros((n,n),complex)
    for j,(e,sign) in enumerate(word):
        if e!=edge:continue
        d=A@links[e] if sign==1 else -links[e].conj().T@A
        left=np.eye(n,dtype=complex);right=left.copy()
        for factor in factors[:j]:left=left@factor
        for factor in factors[j+1:]:right=right@factor
        out+=left@d@right
    return out

def local_measure():
    rng=np.random.default_rng(12020);_,_,_,_,_,words=prior.native_paths()
    def gen():
        a=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5));a=(a-a.conj().T)/2;a-=np.trace(a)*np.eye(5)/5;return a/np.linalg.norm(a)
    links=[expm(.25*gen()) for _ in range(135)];A=gen();B=gen();chosen=[words[0][0][0],words[1][0][0]];gamma,g5=gamma4();G5=np.kron(g5,np.eye(15));ev,E=np.linalg.eigh(-G5);E=E[:,ev>0]
    def field(s0,t0):
        ls=list(links);ls[chosen[0]]=expm(s0*A)@ls[chosen[0]];ls[chosen[1]]=expm(t0*B)@ls[chosen[1]];return ls
    def projector(s0,t0,frame=False):
        C=[word_product(w,field(s0,t0)) for w in words];D=3*np.eye(60,dtype=complex)
        for gm,c in zip(gamma,C):
            R=np.zeros((15,15),complex);R[:10,:10]=prior.wedge2(c);R[10:,10:]=c.conj();D-=.5*(np.kron(np.eye(4)-gm,R)+np.kron(np.eye(4)+gm,R.conj().T))
        val,V=np.linalg.eigh(G5@D);P=V[:,val>0]@V[:,val>0].conj().T
        if not frame:return P,float(min(abs(val)))
        gram=E.conj().T@P@E;val,V=np.linalg.eigh(gram);assert min(val)>1e-8
        return P@E@(V/np.sqrt(val))@V.conj().T,float(min(val))
    minimum_reference_overlap=projector(0,0,True)[1]
    h=1e-4;P,gap=projector(0,0);Fs=(projector(h,0,True)[0]-projector(-h,0,True)[0])/(2*h);Ft=(projector(0,h,True)[0]-projector(0,-h,True)[0])/(2*h)
    Ps=(projector(h,0)[0]-projector(-h,0)[0])/(2*h);Pt=(projector(0,h)[0]-projector(0,-h)[0])/(2*h)
    curvature=float((1j*np.trace(P@(Ps@Pt-Pt@Ps))).real);frame_curv=float((1j*np.trace(Fs.conj().T@Ft-Ft.conj().T@Fs)).real);assert abs(curvature-frame_curv)<1e-7 and abs(curvature)>1e-4
    err=0.
    for word in words:
        exact=word_derivative(word,links,chosen[0],A);fd=(word_product(word,field(h,0))-word_product(word,field(-h,0)))/(2*h);err=max(err,float(np.linalg.norm(exact-fd)))
    assert err<1e-7
    cells,idx,Ui,Si,g5i,Di,evi,Doi,zi,K=prior.internal_flux();X=prior.magnetic_translation(cells,idx,Ui,(2,0));Xs=np.kron(np.eye(2),X);small=K.conj().T@Xs@K
    S=np.array([[1,.2j,.3],[-.2j,2,.1j],[.3,-.1j,3]]);lifted=K@S@K.conj().T;interface_error=float(np.linalg.norm(Xs@lifted@Xs.conj().T-K@small@S@small.conj().T@K.conj().T));assert interface_error<1e-10
    return dict(status='PASS',minimum_reference_overlap=minimum_reference_overlap,internal_operator_intertwining_error=interface_error,period_word_lengths=list(map(len,words)),native_varied_edges=chosen,projector_rank=int(round(np.trace(P).real)),Wilson_kernel_gap=gap,projector_Berry_curvature=curvature,frame_connection_curvature=frame_curv,native_path_derivative_error=err,local_measure='On the displayed one-cell, topologically trivial patch F=P E(E dag P E)^-1/2 gives an explicit determinant-line frame and L=iTr(Fdag dF). The nonzero curvature iTrP[dP,dP] is not erased by10+bar5 anomaly cancellation.',conditional_native_current='If a coarse global current Lc exists on admissible Phi(U), native determinant line is its pullback tensor26 Kato-trivial optical determinant lines. Lnative=Phi*Lc+Lheavy+iTr[(Pfactor-Pplus)T dTdag], with bounded cell-tree unitaryT. Nativepath derivative is the ordered product-rule sum including inverse edges. This names a conditional local interface; it doesnot implementthecoarseglobalcurrent.',internal_carrier='Prior12015 K3 embeds an internalfamily matrixS as K3 S K3dag in the72D internaloverlap space. It intertwines the computed H27 action. Tensoring three identical SM copies multiplies localmeasurecurvature by3 but doesnotselectflux3 orderive the4Dfamilyinventory.',scope='Concrete finite localframe and native-word differential, not a globally gaugeinvariant/allvolume localmeasure. Coarseglobalcurrent, admissibilitydomain, refinement estimates, globalholonomies and nativefamily/fluxembedding remainopen. Craig2610.09093v1 is an externalcandidate requiring these hypotheses, not independentlycertifiedhere.',prior=['12000 nativewords','12002 heavyKatoandboundedtreefactorization','12010 nonAbeliannativepaths','12015 internalH27andSMrestriction','2610.09093 sections4,9,10'])

def payload():return dict(status='PASS',pass12016=neutrino_thresholds(),pass12017=flavour_potential(),pass12018=dict(gauge_mediation=gauge_mediation(),one_sided_alignment=one_sided_alignment()),pass12019=native_continuum(),pass12020=local_measure())
if __name__=='__main__':
    out=payload();(ROOT/'data/w33_pass12016_12020_neutrino_vacuum_native_measure.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',out['pass12016']['matched'],out['pass12019']['quartic_monomials'],out['pass12020']['projector_Berry_curvature'])
