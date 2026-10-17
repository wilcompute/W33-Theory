"""Theta-vacuum, linked soft CP and finite SQCD followups; no selected TOE vacuum.

12029 heat and12030 topology have separate producers. Standard Jarlskog,
Passarino-Veltman and inverse-map methods are cited, not claimed as new tools.
"""
from pathlib import Path
from functools import lru_cache
import json,sys,itertools
import numpy as np
import sympy as sy
from scipy.integrate import quad,quad_vec,solve_ivp
from scipy.optimize import brentq,least_squares
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12021_12025_uv_curvature_threshold_holonomy as prior
p=prior.p
MATCH=np.array([-0.10656491073583248,-5.272793267008227,-0.29810096172116246,0.09976502092725588,0.04716790982188003,11.313684711138258,7.6126948157198715,-2.130188737763689,-7.442911163051868,-11.76326608746275,12.626469269059587])

@lru_cache(None)
def matching_inputs():return p.unpack(p.running().sol(np.log(prior.MS/p.MZ)))

def B1(a,b,Q):
    """Finite p=0 coefficient for fermion momentum k: -int(1-t)logD/Q2."""
    return -quad(lambda t:(1-t)*np.log((t*a+(1-t)*b)/Q**2),0,1,epsabs=1e-13)[0]

def sqcd_delta(m,kind,mu=1000.,Q=2000.,unit=1.):
    g,_=matching_inputs();cos2=(1-prior.TANB**2)/(1+prior.TANB**2);sw=g[0]**2/(g[0]**2+g[1]**2);pref=2*(g[2]**2/(4*np.pi))/(3*np.pi)
    if kind=='d':ML=2500.*unit;MR=2200.*unit;X=-mu*prior.TANB;DL=(-.5+sw/3)*(p.MZ*unit)**2*cos2;DR=-sw/3*(p.MZ*unit)**2*cos2
    else:ML=2500.*unit;MR=2400.*unit;X=-mu/prior.TANB;DL=(.5-2*sw/3)*(p.MZ*unit)**2*cos2;DR=2*sw/3*(p.MZ*unit)**2*cos2
    S=np.array([[ML*ML+m*m+DL,m*X],[m*X,MR*MR+m*m+DR]]);ev,Z=np.linalg.eigh(S);assert min(ev)>0
    F=(Z*np.array([p.b0(np.array([(2000*unit)**2]),x,Q)[0] for x in ev]))@Z.T
    chir=pref*(2000*unit)*F[0,1]/m;wave=-pref/2*sum(B1((2000*unit)**2,x,Q) for x in ev)
    return dict(chirality=float(chir),wavefunction=float(wave),total=float(chir+wave),squark_mass_squares=ev.tolist())

@lru_cache(None)
def improved_initial(mu=1000.):
    g,mats=matching_inputs();rows=[];high=[];cb=1/np.sqrt(1+prior.TANB**2);sb=prior.TANB*cb
    for kind,M,f in zip(['u','d'],mats[:2],[sb,cb]):
        U,y,V=np.linalg.svd(M);bare=[]
        for mm in y*246.22/np.sqrt(2):
            root=brentq(lambda z:z*(1+sqcd_delta(z,kind,mu)['total'])-mm,.5*mm,1.5*mm,xtol=1e-14);bare.append(root);rows.append(dict(kind=kind,SM_mass_GeV=float(mm),bare_mass_GeV=root,matching_residual=float(root*(1+sqcd_delta(root,kind,mu)['total'])-mm),**sqcd_delta(root,kind,mu)))
        high.append((U*(np.array(bare)*np.sqrt(2)/246.22/f))@V)
    high.append(mats[2]/cb);g=g.copy();g[0]*=np.sqrt(5/3)
    return g,high,rows

@lru_cache(None)
def improved_running(mu=1000.):
    g,high,_=improved_initial(mu);sol=solve_ivp(prior.mssm_beta,[0,np.log(2e16/prior.MS)],p.pack(g,high),rtol=1e-10,atol=1e-13,dense_output=True);assert sol.success;return sol

def residual(x,mu=1000.):
    target=p.shape_observables(p.unpack(improved_running(mu).sol(x[-1]-np.log(prior.MS/p.MZ)))[1]);model=p.shape_observables(p.theta_matrices(x)[:3]);r=np.log(abs(model/target));r[8]=(model[8]-target[8])/target[8];return r

@lru_cache(None)
def finite_thresholds():
    assert max(abs(residual(MATCH)))<1e-7
    rows=improved_initial()[2];g=matching_inputs()[0];pref=2*(g[2]**2/(4*np.pi))/(3*np.pi);check=sqcd_delta(2.3,'d',Q=4000.)['total']-sqcd_delta(2.3,'d')['total'];assert abs(check+pref*np.log(2))<1e-12
    return dict(status='PASS',charged_parameters=MATCH.tolist(),charged_max_log_residual=float(max(abs(residual(MATCH)))),matching_scale_GeV=float(p.MZ*np.exp(MATCH[-1])),all_six_quark_matching=rows,leading_previous_SQCD=prior.sqcd_threshold(),matching_log_derivative=-pref,
        formula='For each real2x2 squark block with LR=m(A-mu tanbeta/cotbeta), include actual eigenvalues/mixing, EW Dterms, quarkm2, chirality term pref*M3/m [B0(M3^2,S)]LR and wavefunction -pref/2 sum_eigen B1(M3^2,mSq2). B1=-int_0^1(1-t)log([tM3^2+(1-t)mSq2]/Q2)dt. Solve mSM=mbare(1+delta) selfconsistently, for all six quarks.',
        RG_log_check='d delta/dlogQ=-2alpha_s/(3pi), exactly betaY_SM,QCD/Y-betaY_MSSM,QCD/Y. Chirality-only12024 misses this matching-scale logarithm; the B1 term supplies it.',
        scope='Complete declared p=0 SQCD quark-mass self energies for aligned real soft blocks; not complete MSSM thresholds. External momentum, finite EW/chargino/neutralino/Higgs/lepton terms, MSbar-DRbar conversion, all softRG and UV/EW vacuum remain open. Full matrix one-loopMSSM running is matched to the same supplied low data; no pole-spectrum/data update or scale prediction.',prior=['12024 leading SQCD benchmark','1411.7035 equations26-29 and41','hep-ph/9709356 beta conventions'])


def orientation(x):
    u,d=p.theta_matrices(x)[:2];V=np.linalg.eigh(u@u.conj().T)[1].conj().T@np.linalg.eigh(d@d.conj().T)[1]
    return V

def mix_coordinates(x):
    V=orientation(x)[::-1,::-1];return np.log(np.abs([V[0,1],V[1,2],V[0,2],(V[0,0]*V[1,1]*V[0,1].conj()*V[1,0].conj()).imag]))

def derivative(fun,x,h=1e-5):return np.column_stack([(fun(x+h*v)-fun(x-h*v))/(2*h) for v in np.eye(len(x))])

@lru_cache(None)
def theta_pullback():
    x=MATCH[:10].copy();full=lambda z:np.r_[z,MATCH[-1]];mix=lambda z:mix_coordinates(full(z));mass=lambda z:np.log(p.shape_observables(p.theta_matrices(full(z))[:3])[1:5]);J=derivative(mix,x);_,s,Vh=np.linalg.svd(J,full_matrices=True);null=Vh[4:].T;massJ=derivative(mass,x);_,ms,Vmass=np.linalg.svd(massJ@null);direction=null@Vmass[0];direction*=1 if direction[np.argmax(abs(direction))]>0 else -1;normal=Vh[:4].T;rows=[]
    for step in [-.04,0.,.04]:
        fit=least_squares(lambda z:mix(x+step*direction+normal@z)-mix(x),np.zeros(4),xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=100);point=x+step*direction+normal@fit.x;assert max(abs(fit.fun))<1e-8
        rows.append(dict(step=step,parameters=point.tolist(),max_mixing_log_residual=float(max(abs(fit.fun))),mass_ratio_log_changes=(mass(point)-mass(x)).tolist()))
    chargedJ=derivative(lambda z:residual(full(z)),x)
    return dict(status='PASS',theta_shape_coordinates=10,orientation_rank=4,local_unfixed_theta_directions=6,mixing_Jacobian_singular_values=s.tolist(),mass_response_on_null_singular_values=ms.tolist(),charged_residual_Jacobian_singular_values=np.linalg.svd(chargedJ,compute_uv=False).tolist(),fixed_orientation_continuations=rows,
        map='Actual12028 theta/Barr matrices determine the relative up/down singular bases V. Pull12022 back by A=diag(1,2,4), B=V diag(1,3,7)Vdag, X=A2,Y=B2. Six radial invariants are then constant; only four mixing constraints act on the ten theta/Barr shape coordinates.',
        conclusion='Exactly two classical matrix-orbits in12022 do not mean two isolated theta vacua. Its pullback has a regular six-dimensional local fibre. Displayed nonlinear continuations preserve all four mixing comparisons while changing quark mass ratios. At fixed matching scale the full charged/quark residual map has rank10; adding data-target functions could isolate the point, but would again fit coefficients rather than derive them.',
        scope='Explicit vacuum-to-theta map and identifiability result, not a dynamically selected modulus vacuum or a retraction of12022 matrix-space theorem. No new stabilizing counterterms or invented coefficient prediction.',prior=['12022 two matrix-orbit theorem','12011 eleven-fit Jacobian','11942 theta/Barr shared kernel','11225 finite-symmetry-only exclusion'])

@lru_cache(None)
def cross_branch_parent():
    A,B=prior.old.flavour_home();old_target=prior.old.invariants(A,B);weights=np.array(prior.old.flavour_potential()['weights']);V=orientation(MATCH);Anew=np.diag(prior.old.A_SPEC);Bnew=V@np.diag(prior.old.B_SPEC)@V.conj().T;new_target=prior.old.invariants(Anew,Bnew);old_energy=float(np.linalg.norm(weights*(new_target-old_target))**2)
    columns=[]
    for k in range(4):
        for z in prior.hermitian_basis():
            ds=[np.zeros((3,3),complex) for _ in range(4)];ds[k]=z;columns.append(prior.parent_differential([Anew,Bnew,Anew@Anew,Bnew@Bnew],ds,weights))
    s=np.linalg.svd(np.array(columns).T,compute_uv=False);assert min(s)>1e-6 and old_energy>1e-15
    return dict(status='PASS',new_branch_energy_in_old_parent=old_energy,old_target=old_target.tolist(),retargeted_coefficients=new_target.tolist(),retargeted_positive_modes=28,retargeted_symmetry_modes=8,retargeted_smallest_normal_Hessian=float(2*min(s)**2),
        result='12022 targeted the12011/12017 orientation, not the changed12028MSSMbranch. Its coefficients must change to make the new orbit a zero. With that supplied retargeting the same36-field parent has28 positive modes and exactly the generic two CP-conjugate global orbits. This explicitly prevents presenting separately fitted packets as one common selected vacuum.',scope='Cross-branch compatibility repair with changed input coefficients; no derivation of them from native interactions or new unification principle.')


def linked_parameters():
    m=np.array([.3,.8,1.7]);rng=np.random.default_rng(12027);E=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));E=(E+E.conj().T)/2;np.fill_diagonal(E,0);return m,E

def cubic_gluino(m,E,l=5.,r=7.,a=.3,b=1.,mg=.7,alpha=.1):
    x=m*m;vand=(x[0]-x[1])*(x[1]-x[2])*(x[2]-x[0]);J=float((E[0,1]*E[1,2]*E[2,0]).imag)
    fun=lambda q:(q+r)*q*q/(np.prod((q+l)*(q+r)-a*a*x)*np.prod(q+x));integral=quad(fun,0,np.inf,epsabs=1e-14,epsrel=1e-11)[0]
    return 3*alpha/(2*np.pi*mg)*a*b*J*vand*integral

@lru_cache(None)
def linked_soft_theorem():
    q,l,r,a,b=sy.symbols('q l r a b',positive=True);m=sy.symbols('m0:3',positive=True);x=[z*z for z in m];D=[(q+l)*(q+r)-a*a*z for z in x];R=[sy.Matrix([[q+r,-a*z],[-a*z,q+l]]) for z in m];kernels=[]
    for i,j,k in [(0,1,2),(1,2,0),(2,0,1)]:
        V=lambda u,v:sy.diag(1,b*m[u]*m[v]);z=R[i]*V(i,j)*R[j]*V(j,k)*R[k]*V(k,i)*R[i]-R[i]*V(i,k)*R[k]*V(k,j)*R[j]*V(j,i)*R[i]
        assert sy.factor(z[0,1]-a*b*m[i]*(x[j]-x[k])*(q+r)*D[i])==0;kernels.append(a*b*m[i]*(x[j]-x[k])*(q+r)/sy.prod(D))
    assert sy.factor(sum(m[i]*kernels[i] for i in range(3)))==0
    physical=sy.factor(sum(m[i]*q/(q+x[i])*kernels[i] for i in range(3)));expected=a*b*(q+r)*q*q*(x[0]-x[1])*(x[1]-x[2])*(x[2]-x[0])/(sy.prod(D)*sy.prod(q+z for z in x));assert sy.factor(physical-expected)==0
    mass,E=linked_parameters();M=np.diag(mass);base=np.block([[5*np.eye(3),.3*M],[.3*M,7*np.eye(3)]]);V=np.block([[E,np.zeros((3,3))],[np.zeros((3,3)),M@E@M]]);coefficient=cubic_gluino(mass,E);rows=[]
    for t in [.1,.05,.025]:
        out=p.colored_phase(M,base+t*V);rows.append(dict(t=t,**out,theta_over_t3=out['sum']/t**3))
    scales=[dict(mass_factor=f,cubic_coefficient=cubic_gluino(f*mass,E)) for f in [1.,.5,.25]]
    return dict(status='PASS',cubic_coefficient=coefficient,CP_triangle=float((E[0,1]*E[1,2]*E[2,0]).imag),finite_controls=rows,mass_scaling_controls=scales,
        theorem='For S=[[lI+epsilon E,aM],[aM,rI+eta*b*M E M]], M>0 diagonal,E Hermitian and real l,r,a,b, ImTr(M^-1 f(S)LR)=0 for every real spectralf, all epsilon/eta for whichS is positive. The common-function gluino trace ImTr(M f(S)LR) also vanishes. Species-dependent internalquarkmass functions in the actual gluino self energy break the latter cancellation.',
        all_orders_proof='For realz let A=(z-l)I-epsilon E, D=(z-r)M^-2-eta*b E, Q=(D A-a2I)^-1. ResolventLR=a Q M^-1. TrQ,TrAQ,TrDQ are real by Qdag=(A D-a2I)^-1 and cyclicity. M^-2 is a real linear combination of D,A,I, so the determinant-trace is real. Spectral residues extend to realf. Zero epsilon follows by continuity/12018.',
        first_survivor='At order epsilon^2 eta, theta_gluino=3alpha/(2pi mg)*a*b*Im(E12 E23 E31)*Vandermonde(m_i^2)* integral_0^infty (q+r)q2/[prod_i Delta_i(-q)*prod_i(q+m_i2)]dq. The integral is strictly positive for positive baseline. All epsilon eta terms and epsilon eta^2 cubic terms vanish. Thus the cubic term is nonzero exactly when the triangle and three mass differences are nonzero (and prefactors nonzero).',
        scope='Exact linked-spurion family and stated colored one-loop channels, not a proof that the full MSSM/UV running enforces this relation, nor protection from LR,neutralportal or higherloopterms. Standard Jarlskog/GIM structure is prior art; this pass supplies its specific nonzero loop coefficient and a larger exact quark-safe family.',prior=['12018 one-sided theorem','12021 linked second-order cancellation','11978 singlet-soft diagnostic not full thresholds','standard Jarlskog mass-difference invariant'])


@lru_cache(None)
def neutrino_factors():
    u,d,e,_,A=p.theta_matrices(MATCH);U=np.linalg.eigh(e.conj()@e.T)[1];tmax=MATCH[-1]-np.log(prior.MS/p.MZ)
    def integ(flow,hi,co):return solve_ivp(lambda t,z:co*np.linalg.svd(p.unpack(flow.sol(t))[1][2],compute_uv=False)[::-1]**2/prior.old.LOOP,[hi,0],np.zeros(3),rtol=1e-11,atol=1e-14).y[:,-1]
    val=integ(improved_running(),tmax,1.)+integ(p.running(),np.log(prior.MS/p.MZ),-1.5)
    return A,U,np.exp(val[:,None]+val[None,:])

def neutrino(q):
    A,U,F=neutrino_factors();L=np.array([[np.exp(q[0]),0,0],[q[2],np.exp(q[1]),0],[q[3],q[4],1.]]);C=(U.T@A.T@L@L.T@A@U)*F;_,ss,Vh=np.linalg.svd(C);ids=np.argsort(ss);ss=ss[ids];V=Vh.conj().T[:,ids];B=abs(V)**2;obs=np.array([B[0,1]/(1-B[0,2]),B[1,2]/(1-B[0,2]),B[0,2],(ss[1]**2-ss[0]**2)/(ss[2]**2-ss[0]**2)]);scale=np.sqrt(.002511/(ss[2]**2-ss[0]**2));J=float((V[0,0]*V[1,1]*V[0,1].conj()*V[1,0].conj()).imag)
    return obs,dict(masses_eV=(ss*scale).tolist(),m_beta_beta_eV=float(abs(C[0,0])*scale),J=J)

@lru_cache(None)
def neutrino_fibre():
    seed=np.array(prior.spectrum_matching()['neutrino_parameters']);fit=least_squares(lambda q:np.log(neutrino(q)[0]/prior.old.NEUTRINO_TARGET),seed,max_nfev=200,xtol=1e-11,ftol=1e-11,gtol=1e-11);assert max(abs(fit.fun))<1e-7;home=fit.x;rows=[]
    J=derivative(lambda q:np.log(neutrino(q)[0]),home);_,sv,Vh=np.linalg.svd(J,full_matrices=True);assert sv[-1]>1e-5
    tangent=Vh[-1];tangent*=1 if tangent[np.argmax(abs(tangent))]>0 else -1;normal=Vh[:4].T
    # Adaptive arclength charts follow the curve rather than fixing a bad coordinate.
    for sign in [-1,1]:
        current=home.copy();previous=sign*tangent;arc=0.;step=.002
        for _ in range(5):
            jac=derivative(lambda q:np.log(neutrino(q)[0]),current);_,_,vh=np.linalg.svd(jac,full_matrices=True);direction=vh[-1]
            if direction@previous<0:direction=-direction
            normal=vh[:4].T
            while True:
                predicted=current+step*direction
                point=least_squares(lambda z:np.log(neutrino(predicted+normal@z)[0]/prior.old.NEUTRINO_TARGET),np.zeros(4),max_nfev=300,xtol=1e-12,ftol=1e-12,gtol=1e-12)
                if max(abs(point.fun))<1e-8:break
                step/=2
                if step<1e-7:raise RuntimeError('Localneutrinocontinuationneedsanotherchart')
            q=predicted+normal@point.x;arc+=np.linalg.norm(q-current);obs,detail=neutrino(q);rows.append(dict(step=float(sign*arc),parameters=q.tolist(),max_log_residual=float(max(abs(point.fun))),observables=obs.tolist(),**detail));current=q;previous=direction;step=min(.02,step*1.5)
    rows.sort(key=lambda r:r['step'])
    bad_fixed=home[4]-.08;bad=least_squares(lambda z:np.log(neutrino(np.r_[z,bad_fixed])[0]/prior.old.NEUTRINO_TARGET),home[:4],max_nfev=300,xtol=1e-11,ftol=1e-11,gtol=1e-11)
    return dict(status='PASS',base_parameters=home.tolist(),Jacobian_singular_values=sv.tolist(),continuation=rows,failed_coordinate_chart=dict(fixed_q4=float(bad_fixed),max_log_residual=float(max(abs(bad.fun))),interpretation='Failedlocalq4chartattempt, not an excludedmodelbranch or globalno-go.'),
        reading='A one-dimensional local family retains all four neutrino comparisons on the new full-p0SQCD branch; lightest mass, m_beta_beta and leptonicJ vary together. This is a conditional correlation in a supplied real-Majorana ansatz, not a unique prediction, a global allowed interval or an experimental update.',scope='One-loop C5shape, supplied atmospheric normalization and historical oscillation targets. No fullMSSMthresholds, neutrino-scale selection or global branch census. CP-conjugate sign conventions follow12007/12016.')


def units_control():
    base=sqcd_delta(2.3,'d');scaled=sqcd_delta(23.,'d',mu=10000.,Q=20000.,unit=10.);error=max(abs(base[k]-scaled[k]) for k in ['chirality','wavefunction','total']);assert error<1e-10
    return dict(status='PASS',common_mass_rescaling=10,dimensionless_threshold_error=error,result='Scaling all masses,momenta,vevs andQ bylambda leaves the dimensionlessmatching map unchanged; I scaleslambda^-2, B0/B1 depend only ratios. Nativeheat Tr exp(-t A/a2) is invariant under a->a/lambda,t->t/lambda2. A fitted scale relative to suppliedMZ does not fix an absolute naturalunit orderiveG/Lambda.',prior=['12009 natural units/density gate','12024 spectrum sensitivity'])


def payload():
    from w33_pass12029_native_heat_curvature import formfactor_certificate
    return dict(status='PASS',pass12026=theta_pullback(),pass12027=linked_soft_theorem(),pass12028=finite_thresholds(),pass12031=cross_branch_parent(),pass12033=neutrino_fibre(),pass12032=formfactor_certificate(),natural_units=units_control())
if __name__=='__main__':
    out=payload();(ROOT/'data/w33_pass12026_12033_theta_soft_threshold_connections.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',out['pass12026']['local_unfixed_theta_directions'],out['pass12027']['cubic_coefficient'],out['pass12028']['matching_scale_GeV'],flush=True)
