"""Five explicit followups to12016-12020. Supplied EFT inputs are not predictions.

General mass insertions, auxiliary-field parents, unistochastic reconstruction,
conformal geometry, MSSM matching and Kato transport are prior art.
"""
from pathlib import Path
from functools import lru_cache
import itertools,json,sys
import numpy as np
import sympy as sy
from scipy.integrate import quad,solve_ivp
from scipy.optimize import least_squares
from scipy.linalg import expm,polar
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12016_12020_neutrino_vacuum_native_measure as old
p=old.prior

def hermitian_basis():
    out=[]
    for i in range(3):
        z=np.zeros((3,3),complex);z[i,i]=1;out.append(z)
    for i in range(3):
        for j in range(i):
            z=np.zeros((3,3),complex);z[i,j]=z[j,i]=1/np.sqrt(2);out.append(z)
            z=np.zeros((3,3),complex);z[i,j]=1j/np.sqrt(2);z[j,i]=-1j/np.sqrt(2);out.append(z)
    return out

def mixed_data():
    m=np.array([.3,.8,1.7]);ell=.3*m;l=np.array([4.,5.,6.]);r=np.array([6.,7.,8.]);rng=np.random.default_rng(12021)
    def herm():
        z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));z=(z+z.conj().T)/2;np.fill_diagonal(z,0);return z
    return m,ell,l,r,herm(),herm()

def mixed_loop_response(x,ell,l,r,E,F):
    """Exact coefficient of eps*eta Im B0(x,S)_{Li,Ri} at real species blocks."""
    out=np.zeros(len(ell))
    for i in range(len(ell)):
        for j in range(len(ell)):
            if i==j:continue
            fun=lambda q:q/(q+x)/(((q+l[i])*(q+r[i])-ell[i]**2)*((q+l[j])*(q+r[j])-ell[j]**2))
            out[i]-=ell[j]*(E[i,j]*F[j,i]).imag*quad(fun,0,np.inf,epsabs=1e-13,epsrel=1e-11)[0]
    return out

def mixed_soft():
    z,l1,l2,r1,r2,a1,a2=sy.symbols('z l1 l2 r1 r2 a1 a2',real=True)
    base=sy.Matrix([[l1,0,a1,0],[0,l2,0,a2],[a1,0,r1,0],[0,a2,0,r2]])
    E=sy.zeros(4);F=sy.zeros(4);E[0,1]=1+sy.I;E[1,0]=1-sy.I;F[2,3]=2-sy.I;F[3,2]=2+sy.I
    R=(z*sy.eye(4)-base).inv();mixed=R*E*R*F*R+R*F*R*E*R
    delta1=(z-l1)*(z-r1)-a1*a1;delta2=(z-l2)*(z-r2)-a2*a2
    assert sy.factor(sy.im(mixed[0,2])-3*a2/delta1/delta2)==0
    m,ell,l,r,E,F=mixed_data();M=np.diag(m);base=np.block([[np.diag(l),np.diag(ell)],[np.diag(ell),np.diag(r)]])
    quark=2*.1*.7/(3*np.pi)*sum(mixed_loop_response(.7**2,ell,l,r,E,F)/m)
    gluino=-3*.1/(2*np.pi*.7)*sum(m[i]*mixed_loop_response(m[i]**2,ell,l,r,E,F)[i] for i in range(3));rows=[]
    for h in [.04,.02,.01,.005]:
        def phase(a,b):return p.colored_phase(M,base+np.block([[a*E,np.zeros((3,3))],[np.zeros((3,3)),b*F]]))['sum']
        value=sum(a*b*phase(a*h,b*h) for a in [-1,1] for b in [-1,1])/(4*h*h)
        rows.append(dict(h=h,mixed_coefficient=value,error=value-quark-gluino))
    linked=M@E@M;mfv_error=float(max(abs((E*linked.T).imag).ravel()));assert mfv_error<1e-14
    return dict(status='PASS',quark_coefficient=quark,gluino_coefficient=gluino,total_mixed_coefficient=quark+gluino,finite_difference_controls=rows,linked_spurion_imaginary_pair_max=mfv_error,
        exact_resolvent='For Delta_i(z)=(z-l_i)(z-r_i)-ell_i^2 and E=deltaLL,F=deltaRR Hermitian, Im[coeff_eps_eta (z-S)^-1_LRii]=sum_j ell_j Im(Eij Fji)/(Delta_i Delta_j). Single-sided terms vanish by12018.',
        exact_loop_kernel='Im coeff_eps_eta B0(x,S)_LRii=-sum_j ell_j Im(Eij Fji) integral_0^infty dq q/[(q+x)Delta_i(-q)Delta_j(-q)]. Positive massive baseline assumed. This is a convergent mass-insertion kernel, not a finite-difference estimate.',
        radiative_reading='If the leading right spurion is F=Mdag E M in the real mass basis, every Im(Eij Fji)=0. Thus merely seeing both sides generated does not imply this leading mixed CP channel survives. Independent spurions or higher insertions/LR channels are required.',
        scope='Exact second mixed coefficient in specified colored one-loop channels. No complete MSSM soft RG, LR/neutral/Higgs portals, UV threshold or total strong-CP bound; standard mass-insertion mechanism cited to2002.04204/9303296.')


def parent_invariants(fields):
    A,B,X,Y=fields
    def Q(A,X,ev,i):
        others=np.delete(ev,i);return (X-sum(others)*A+np.prod(others)*np.eye(3))/np.prod(ev[i]-others)
    out=[np.trace(A).real,np.trace(X).real,np.trace(A@X).real,np.trace(B).real,np.trace(Y).real,np.trace(B@Y).real]
    out.extend(np.trace(Q(A,X,old.A_SPEC,i)@Q(B,Y,old.B_SPEC,j)).real for i in range(2) for j in range(2))
    return np.array(out)

def parent_residual(fields,target,weights):
    A,B,X,Y=fields;basis=hermitian_basis()
    return np.r_[weights*(parent_invariants(fields)-target),[np.trace(z@(X-A@A)).real for z in basis],[np.trace(z@(Y-B@B)).real for z in basis]]

def parent_differential(fields,dfields,weights):
    A,B,X,Y=fields;dA,dB,dX,dY=dfields
    def Q(A,X,dA,dX,ev,i):
        others=np.delete(ev,i);den=np.prod(ev[i]-others)
        return (X-sum(others)*A+np.prod(others)*np.eye(3))/den,(dX-sum(others)*dA)/den
    out=[np.trace(dA).real,np.trace(dX).real,np.trace(dA@X+A@dX).real,np.trace(dB).real,np.trace(dY).real,np.trace(dB@Y+B@dY).real]
    for i in range(2):
        for j in range(2):
            a,da=Q(A,X,dA,dX,old.A_SPEC,i);b,db=Q(B,Y,dB,dY,old.B_SPEC,j);out.append(np.trace(da@b+a@db).real)
    return np.r_[weights*np.array(out),[np.trace(z@(dX-A@dA-dA@A)).real for z in hermitian_basis()],[np.trace(z@(dY-B@dB-dB@B)).real for z in hermitian_basis()]]

def unitary_from_moduli(B,sign=1):
    lengths=np.sqrt(B[0]*B[1]);c=(lengths[2]**2-lengths[0]**2-lengths[1]**2)/(2*lengths[0]*lengths[1]);assert -1<c<1
    phase1=c+sign*1j*np.sqrt(1-c*c);phase2=-(lengths[0]+lengths[1]*phase1)/lengths[2]
    rows=[np.sqrt(B[0]).astype(complex),np.sqrt(B[1])*np.array([1,phase1,phase2])];rows.append(np.cross(rows[0].conj(),rows[1].conj()));return np.array(rows)

@lru_cache(None)
def parent_vacuum():
    A,B=old.flavour_home();fields=[A,B,A@A,B@B];target=old.invariants(A,B);weights=np.array(old.flavour_potential()['weights']);columns=[]
    for k in range(4):
        for z in hermitian_basis():
            ds=[np.zeros((3,3),complex) for _ in range(4)];ds[k]=z;columns.append(parent_differential(fields,ds,weights))
    J=np.array(columns).T;sv=np.linalg.svd(J,compute_uv=False);H=2*J.T@J;relaxed=H[:18,:18]-H[:18,18:]@np.linalg.solve(H[18:,18:],H[18:,:18]);ev=np.linalg.eigvalsh(relaxed)
    assert sv[-1]>1e-5 and np.max(abs(parent_residual(fields,target,weights)))<1e-12
    _,U=np.linalg.eigh(A);_,V=np.linalg.eigh(B);moduli=abs(U.conj().T@V)**2;U1=unitary_from_moduli(moduli);U2=unitary_from_moduli(moduli,-1)
    error=max(np.linalg.norm(U1@U1.conj().T-np.eye(3)),np.max(abs(abs(U1)**2-moduli)))
    js=[float((u[0,0]*u[1,1]*u[0,1].conj()*u[1,0].conj()).imag) for u in [U1,U2]];assert error<1e-10 and js[0]*js[1]<0
    return dict(status='PASS',real_fields=36,constraint_rank=28,positive_normal_modes=28,symmetry_zero_modes=8,normal_Hessian_eigenvalues=(2*sv**2).tolist(),relaxed_light_Hessian_eigenvalues=ev.tolist(),heavy_Hessian_min=float(np.linalg.eigvalsh(H[18:,18:])[0]),unitary_moduli_reconstruction_error=float(error),CP_partner_J=js,
        potential='V/f^4=sum_r w_r^2 (Itilde_r(A,B,X,Y)-c_r)^2+||X-A^2||F^2+||Y-B^2||F^2. All four fields are dimensionless Hermitian3 matrices; physical canonically dimension-one fields are f times them. Itilde uses TrA,TrX,TrAX and B,Y analogues; projectors replace A^2 byX and B^2 byY. Every residual has degree<=2, so parent is renormalizable degree<=4.',
        global_vacuum_proof='Nonnegative terms force X=A^2,Y=B^2 and the ten12017 invariant targets. Three power traces fix each simple spectrum by Newton identities. Four overlaps fix the whole3x3 bistochastic matrix. Orthogonality of the first two unitary rows is a triangle with nonzero area |J|/2, hence has exactly two orientations up to row/column phases. The third row is then fixed up to phase. Thus exactly two simultaneous-U3 vacuum orbits, exchanged by CP, for the displayed nonzero-J target. Radial trace2 bounds the zero set. No additional zero-energy orbits are missed.',
        relaxation='Finite auxiliary masses preserve the exact zero set but do NOT reproduce the entire old off-shell degree8 potential. The correctly relaxed light Hessian is its Schur complement, not the frozen-auxiliary Hessian; both are explicitly stored.',
        scope='A supplied renormalizable bosonic parent and a global classical vacuum classification, not a derivation of target coefficients c_r,w_r,f from W33, theta-modulus stabilization, physical matter couplings or radiative naturalness. GlobalSU3 gives8 Goldstones; gauging/fermion anomalies require separate completion.',prior=['11665 positive auxiliary-chain parent and relaxed-Hessian warning','12017 observed-orientation invariant target','11967 single mixed trace alignment obstruction','0909.0116 standard3x3 unistochastic triangle'])


def sigma(x):return .12*np.cos(x)+.04*np.sin(2*x)
def sigma_prime(x):return -.12*np.sin(x)+.08*np.cos(2*x)
def test_field(x):return np.sin(x)+.2*np.cos(2*x)
def test_field_prime(x):return np.cos(x)-.4*np.sin(2*x)

def conformal_native(N,marking=None,wrong_capacity=False):
    b,v,_,H=old.metric_inputs();H=np.array(H,float);M=float(np.sqrt(np.linalg.det(H)));chi=np.r_[0,-np.linalg.solve(b.T@b,b.T@v[:,0])];bf=np.c_[-b.sum(1),b].astype(int)
    if marking is not None:v=v.copy();v[:,0]+=bf@marking;chi-=marking
    ends=[(np.flatnonzero(e<0)[0],np.flatnonzero(e>0)[0]) for e in bf];a=2*np.pi/N;n=np.arange(N);energy=curvature=0.
    for e,(i,j) in enumerate(ends):
        x=a*(n+chi[i]);y=a*(n+v[e,0]+chi[j]);w=np.exp(2*sigma((x+y)/2))
        energy+=np.mean(w*(test_field(y)-test_field(x))**2)/27/a**2;curvature+=6*np.mean(w*(sigma(y)-sigma(x))**2)/27/a**2
    mass=np.mean([M*(np.ones(N) if wrong_capacity else np.exp(4*sigma(a*(n+c))))*test_field(a*(n+c))**2 for c in chi])
    return dict(N=N,energy=float(energy),mass=float(mass),rayleigh=float(energy/mass),curvature_functional=float(curvature))

@lru_cache(None)
def curved_native():
    _,_,_,H=old.metric_inputs();H=np.array(H,float);M=float(np.sqrt(np.linalg.det(H)));mean=lambda f:quad(f,0,2*np.pi,epsabs=1e-12)[0]/(2*np.pi)
    energy=H[0,0]*mean(lambda x:np.exp(2*sigma(x))*test_field_prime(x)**2);mass=M*mean(lambda x:np.exp(4*sigma(x))*test_field(x)**2);R=6*H[0,0]*mean(lambda x:np.exp(2*sigma(x))*sigma_prime(x)**2)
    rows=[]
    for N in [16,32,64,128,256]:
        row=conformal_native(N);row.update(rayleigh_error=row['rayleigh']-energy/mass,curvature_error=row['curvature_functional']-R);rows.append(row)
    drawing=conformal_native(64,np.arange(27)%3-1);basis_error=max(abs(drawing[k]-rows[2][k]) for k in ['energy','mass','rayleigh','curvature_functional']);assert basis_error<1e-11
    return dict(status='PASS',continuum_rayleigh=energy/mass,continuum_integrated_R_per_coordinate_volume=R,refinement=rows,cell_relabelling_error=basis_error,fixed_capacity_rayleigh=conformal_native(256,wrong_capacity=True)['rayleigh'],
        construction='Use harmonic vertex positions x=a(n+chi_i), h_e=v_e+chi_j-chi_i. Supply edge conductance exp(2sigma(bond midpoint)) and vertex capacity M0 exp(4sigma(x)); all135native edges retained. H(x)=exp(2sigma)H0, M(x)=exp(4sigma)M0, g(x)=exp(2sigma)g0.',
        recovery_proof='For smooth periodic fields on4D, centered bond difference is a h_e.grad f+O(a^3). Riemann sums give native energy -> integral exp(2sigma) gradf.H0.gradf and mass -> integral M0 exp(4sigma)|f|^2. Harmonicity minimizes the frozen cell energy. The displayed one-coordinate periodic recovery sequence has O(a^2) energy error. This is a genuine inhomogeneous native consistency/recovery calculation, not a proved full spectral/heat-trace convergence theorem.',
        curvature_identity='In4D, R[g]=exp(-2sigma)(-6 Delta_g0 sigma-6|grad sigma|g0^2). Periodic integration yields integral sqrt(g)R=6 integral exp(2sigma) grad sigma.H0.grad sigma. The native6E[sigma] converges to this conformal curvature functional.',
        Einstein_boundary='Choosing this particular conductance-gradient functional is extra dynamics. Euclidean Einstein action -integral sqrt(g)R/(16piG) is NEGATIVE along the conformal mode; positive native6E is not automatically the Einstein sign. No quantum determinant derivation, general10metric action, constraint closure, Lorentz signature, Newton/Lambda or selected spacinga follows.',prior=['11995 harmonic10weight chart','12009 required capacity and fixed-capacity counterexample','12019 constant native dispersion','11601 heat/metric density audit'])

MS=2000.;TANB=10.;MU=1000.;M3=2000.;ML=2500.;MR=2200.
MATCH=np.array([-0.10622740839975005,-5.273670380805942,-0.2970894096517852,0.09981283193449943,0.047304516697719255,11.311933268217096,7.5998672172559365,-2.134212736256183,-7.4594211092695595,-11.772460308016756,12.707248708341723])

def three_mass_I(a,b,c):
    scale=max(a,b,c);return quad(lambda q:q/((q+a/scale)*(q+b/scale)*(q+c/scale)),0,np.inf,epsabs=1e-13)[0]/scale

def sqcd_threshold(mu=MU):
    g,_=p.unpack(p.running().sol(np.log(MS/p.MZ)));I=three_mass_I(ML**2,MR**2,M3**2)
    return 2*(g[2]**2/(4*np.pi))/(3*np.pi)*M3*mu*TANB*I

def mssm_beta(t,x):
    g,ms=p.unpack(x);u,d,e=ms;hu=u@u.conj().T;hd=d@d.conj().T;he=e@e.conj().T;tu=np.trace(hu).real;td=np.trace(hd).real;te=np.trace(he).real;g1,g2,g3=g
    gu=13/15*g1*g1+3*g2*g2+16/3*g3*g3;gd=7/15*g1*g1+3*g2*g2+16/3*g3*g3;ge=9/5*g1*g1+3*g2*g2
    return p.pack(np.array([33/5,1,-3])*g**3,[(3*hu+hd+(3*tu-gu)*np.eye(3))@u,(3*hd+hu+(3*td+te-gd)*np.eye(3))@d,(3*he+(3*td+te-ge)*np.eye(3))@e])/old.LOOP

@lru_cache(None)
def matched_running(mu=MU):
    g,m=p.unpack(p.running().sol(np.log(MS/p.MZ)));g=g.copy();g[0]*=np.sqrt(5/3);cb=1/np.sqrt(1+TANB*TANB);sb=TANB*cb
    sol=solve_ivp(mssm_beta,[0,np.log(2e16/MS)],p.pack(g,[m[0]/sb,m[1]/cb/(1+sqcd_threshold(mu)),m[2]/cb]),rtol=1e-10,atol=1e-13,dense_output=True);assert sol.success;return sol

def matched_residual(x,mu=MU):
    target=p.shape_observables(p.unpack(matched_running(mu).sol(x[-1]-np.log(MS/p.MZ)))[1]);model=p.shape_observables(p.theta_matrices(x)[:3]);r=np.log(abs(model/target));r[8]=(model[8]-target[8])/target[8];return r

@lru_cache(None)
def matching_neutrino_factors():
    sol=matched_running();tmax=MATCH[-1]-np.log(MS/p.MZ);A=p.theta_matrices(MATCH)[4];e=p.theta_matrices(MATCH)[2];ue=np.linalg.eigh(e.conj()@e.T)[1]
    def integral(flow,lo,hi,coefficient):
        return solve_ivp(lambda t,z:coefficient*np.linalg.svd(p.unpack(flow.sol(t))[1][2],compute_uv=False)[::-1]**2/old.LOOP,[hi,lo],np.zeros(3),rtol=1e-11,atol=1e-14).y[:,-1]
    val=integral(sol,0,tmax,1.)+integral(p.running(),0,np.log(MS/p.MZ),-1.5)
    return A,ue,np.exp(val[:,None]+val[None,:])

def matched_neutrino(q):
    A,U,F=matching_neutrino_factors();L=np.array([[np.exp(q[0]),0,0],[q[2],np.exp(q[1]),0],[q[3],q[4],1.]])
    C=(U.T@A.T@L@L.T@A@U)*F;_,s,vh=np.linalg.svd(C);ids=np.argsort(s);s=s[ids];V=vh.conj().T[:,ids];B=abs(V)**2
    return np.array([B[0,1]/(1-B[0,2]),B[1,2]/(1-B[0,2]),B[0,2],(s[1]**2-s[0]**2)/(s[2]**2-s[0]**2)])

@lru_cache(None)
def spectrum_matching():
    assert max(abs(matched_residual(MATCH)))<1e-7
    rows=[]
    for mu in [-MU,0.,MU]:
        fit=least_squares(lambda x:matched_residual(x,mu),MATCH,max_nfev=150,xtol=1e-10,ftol=1e-10,gtol=1e-10,diff_step=1e-5,bounds=(np.r_[np.full(10,-np.inf),np.log(MS/p.MZ)],np.r_[np.full(10,np.inf),np.log(2e16/p.MZ)]));assert max(abs(fit.fun))<1e-6
        rows.append(dict(mu_GeV=mu,leading_SQCD_delta=sqcd_threshold(mu),scale_GeV=float(p.MZ*np.exp(fit.x[-1])),max_log_residual=float(max(abs(fit.fun))),parameters=fit.x.tolist()))
    nu=least_squares(lambda q:np.log(matched_neutrino(q)/old.NEUTRINO_TARGET),old.NU_FIT,max_nfev=300,xtol=1e-11,ftol=1e-11,gtol=1e-11);assert max(abs(nu.fun))<1e-7
    return dict(status='PASS',charged_parameters=MATCH.tolist(),charged_max_log_residual=float(max(abs(matched_residual(MATCH)))),neutrino_parameters=nu.x.tolist(),neutrino_observables=matched_neutrino(nu.x).tolist(),neutrino_max_log_residual=float(max(abs(nu.fun))),threshold_refits=rows,
        inventory='SM below Ms=2TeV; MSSM above. Supplied DR-like soft benchmark: allQ2.5TeV, alluR2.4TeV, alldR2.2TeV, allL/eR2TeV, M1=1.5TeV,M2=1.6TeV,M3=2TeV, mu=1TeV, heavyHiggs2TeV, tanbeta10, A=0 at matching. These are running input masses, not a solved SUSY/EW vacuum or measured pole spectrum.',
        matching='At Ms: Yu_MSSM=Yu_SM/sinbeta, Yd_MSSM=Yd_SM/[cosbeta(1+Delta_g)], Ye_MSSM=Ye_SM/cosbeta; Delta_g=2alpha_s/(3pi)M3 mu tanbeta I(mQ2,mdR2,M32). I(a,b,c)=integral_0^infty q dq/[(q+a)(q+b)(q+c)]. Included leading tanbeta-enhancedSQCD term is calculated from this spectrum, not an arbitrarydelta.',
        neutrino='One-loop C5 shape in charged eigenbasis: q_i=+y_i^2/(16pi2) aboveMs and -3y_i^2/(32pi2) belowMs. Universal factor and sinbeta^2 matching absorbed into suppliedDelta31. Four oscillation comparisons rematched; five real shapes remain underdetermined.',
        scope='Fifteen fitted comparisons in a declared piecewise one-loop SM/MSSM benchmark with a calculated dominant finite SQCD correction. Omitted finite EW/Higgs/top/lepton and scheme conversion terms, higher loops and full nonuniversal thresholds prevent calling this complete precision MSSM matching. mu=0 row is an algebraic zero-threshold control, not a physical heavy-Higgsino benchmark. Full softRG, Higgs potential, messenger-to-low spectrum, UV unification and vacuum/scale selection remain open.',prior=['12011 SM branch','12016 arbitrary threshold sensitivity and C5 shape','hep-ph/9709356 MSSM beta functions','1411.7035 complete thresholds and limitations of dominant approximation'])

class NativeChiralPatch:
    """Actual native period words; finite one-cell10+bar5 chiral projector."""
    def __init__(self):
        rng=np.random.default_rng(12020);_,_,_,_,_,self.words=p.native_paths();self.gamma,g5=old.gamma4();self.G=np.kron(g5,np.eye(15));ev,E=np.linalg.eigh(-self.G);self.E=E[:,ev>0]
        def gen():
            a=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5));a=(a-a.conj().T)/2;a-=np.trace(a)*np.eye(5)/5;return a/np.linalg.norm(a)
        self.links=[expm(.25*gen()) for _ in range(135)];self.A=gen();self.B=gen();self.edges=[self.words[0][0][0],self.words[1][0][0]];self.pairs=list(itertools.combinations(range(5),2))
    def wedge_derivative(self,c,d):
        return np.array([[d[i,k]*c[j,l]+c[i,k]*d[j,l]-d[i,l]*c[j,k]-c[i,l]*d[j,k] for k,l in self.pairs] for i,j in self.pairs])
    def evaluate(self,s,t,ds=0,dt=0,conjugator=None):
        ls=list(self.links);ls[self.edges[0]]=expm(s*self.A)@ls[self.edges[0]];ls[self.edges[1]]=expm(t*self.B)@ls[self.edges[1]];D=3*np.eye(60,dtype=complex);dD=np.zeros_like(D)
        for gm,w in zip(self.gamma,self.words):
            c=old.word_product(w,ls);d=ds*old.word_derivative(w,ls,self.edges[0],self.A)+dt*old.word_derivative(w,ls,self.edges[1],self.B)
            if conjugator is not None:c=conjugator@c@conjugator.conj().T;d=conjugator@d@conjugator.conj().T
            R=np.zeros((15,15),complex);R[:10,:10]=p.wedge2(c);R[10:,10:]=c.conj();dR=np.zeros_like(R);dR[:10,:10]=self.wedge_derivative(c,d);dR[10:,10:]=d.conj()
            D-=.5*(np.kron(np.eye(4)-gm,R)+np.kron(np.eye(4)+gm,R.conj().T));dD-=.5*(np.kron(np.eye(4)-gm,dR)+np.kron(np.eye(4)+gm,dR.conj().T))
        ev,V=np.linalg.eigh(self.G@D);pp=(ev>0).astype(float);P=(V*pp)@V.conj().T;C=self.E.conj().T@P@self.E;cc,Z=np.linalg.eigh(C);assert min(cc)>1e-8
        frame=P@self.E@(Z/np.sqrt(cc))@Z.conj().T
        delta=ev[:,None]-ev[None,:];numer=pp[:,None]-pp[None,:];ratio=np.divide(numer,delta,out=np.zeros_like(delta),where=abs(delta)>1e-10);dP=V@(ratio*(V.conj().T@self.G@dD@V))@V.conj().T
        current=float((.5j*np.trace(np.linalg.solve(C,self.E.conj().T@(P@dP-dP@P)@self.E))).real)
        return P,frame,current,float(min(abs(ev))),float(min(cc)),dP

CORNERS=[(-.12,-.1),(.12,-.1),(.12,.1),(-.12,.1),(-.12,-.1)]
def transport_loop(patch,N,reverse=False):
    corners=CORNERS[::-1] if reverse else CORNERS;P0,F0,*_=patch.evaluate(*corners[0]);last=P0;Q=np.eye(60,dtype=complex);gap=overlap=1e100
    for c,d in zip(corners,corners[1:]):
        for u in np.arange(1,N+1)/N:
            P,_,_,g,o,_=patch.evaluate(*(np.array(c)+u*(np.array(d)-c)));gap=min(gap,g);overlap=min(overlap,o)
            K=P@last+(np.eye(60)-P)@(np.eye(60)-last);Q=polar(K)[0]@Q;last=P
    return dict(segments_per_side=N,phase=float(np.angle(np.linalg.det(F0.conj().T@Q@F0))),unitarity_error=float(np.linalg.norm(Q.conj().T@Q-np.eye(60))),projector_intertwining_error=float(np.linalg.norm(P0@Q-Q@P0)),sampled_min_kernel_gap=gap,sampled_min_reference_overlap=overlap)

@lru_cache(None)
def closed_measure():
    patch=NativeChiralPatch();integral=0.
    for c,d in zip(CORNERS,CORNERS[1:]):
        ds,dt=np.array(d)-c;integral+=quad(lambda u:patch.evaluate(*(np.array(c)+u*np.array([ds,dt])),ds,dt)[2],0,1,epsabs=1e-11)[0]
    rows=[]
    for N in [8,16,32]:
        row=transport_loop(patch,N);row['phase_error']=row['phase']-integral;rows.append(row)
    reverse=transport_loop(patch,16,True);assert abs(reverse['phase']+rows[1]['phase'])<1e-11
    G=expm(.1*(patch.A+patch.B));rep=np.zeros((15,15),complex);rep[:10,:10]=p.wedge2(G);rep[10:,10:]=G.conj();U=np.kron(np.eye(4),rep)
    P,F,*_=patch.evaluate(.03,-.02);Pg,Fg,*_=patch.evaluate(.03,-.02,conjugator=G);Ur=patch.E.conj().T@U@patch.E
    cov=float(np.linalg.norm(Fg-U@F@Ur.conj().T));assert cov<1e-11
    return dict(status='PASS',closed_native_loop=CORNERS,connection_integral=integral,transport=rows,reverse_phase=reverse['phase'],frame_gauge_equivariance_error=cov,reference_representation_determinant_real_imag=[float(np.linalg.det(Ur).real),float(np.linalg.det(Ur).imag)],
        current='L_eta=(i/2)Tr[(E dag P E)^-1 E dag [P,delta_eta P] E]. deltaP uses the exact spectral Frechet divided difference of the sign/projector, with deltaWilson built by actual ordered native-word derivatives and wedge2 product differentiation. This implements the local current, not only its curvature.',
        loop_identity='For the displayed closed native-edge rectangle, exp(i integral L) agrees under refinement with det(1-P0+P0 Q_Kato). Q_Kato is approximated independently by products of full60D polar direct rotations between successive projectors. Loop reversal inverts the phase.',
        equivariance='On this one-cell simultaneous-root-conjugation domain, F(Ug)=R(g)F(U)R_E(g)dag and detR_E(g)=1. This is finite-patch equivariance, not an allvolume locality proof or a complete gauge Ward identity.',
        native_pullback='For any admissible coarse current Lc, Phi*Lc acts on native links by the full ordered-word differential. Bounded words preserve finite support up to their bounded graph paths; the tree/Kato terms of12002 are still required for the enlarged native regulator.',
        scope='Actual finite-patch current and closed-loop reconstruction check. The loop is contractible and remains inside one reference-frame patch. No assertion about noncontractible loops, all topological components, uniform volume/admissibility/locality bounds or implemented Craig refinement series. Thus a global native chiral measure remains open.',prior=['12020 local curvature and native differential','12002 bounded tree/heavy-sector determinant lines','2610.09093v1 equations51-54 andAppendixE finite-truncation caveat'])

def payload():return dict(status='PASS',pass12021=mixed_soft(),pass12022=parent_vacuum(),pass12023=curved_native(),pass12024=spectrum_matching(),pass12025=closed_measure())
if __name__=='__main__':
    out=payload();(ROOT/'data/w33_pass12021_12025_uv_curvature_threshold_holonomy.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',out['pass12021']['total_mixed_coefficient'],out['pass12022']['positive_normal_modes'],out['pass12024']['threshold_refits'][-1]['scale_GeV'],out['pass12025']['connection_integral'])
