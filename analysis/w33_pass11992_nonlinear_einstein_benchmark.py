"""Nonlinear vacuum GR positive control and the atlas/Lorentz boundary.

Gowdy T3 is imported classical GR, not derived from W33. Independently
differentiate its full4D metric, evolve both polarizations, and test the
constraints. This replaces neither11976's finite no-go nor full ADM closure.
"""
import json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[1]


class Jet:
    """Scalar two-jet in(t,theta), used to differentiate the metric itself."""
    def __init__(self,value,gradient=None,hessian=None):
        self.v=float(value);self.d=np.zeros(2) if gradient is None else np.array(gradient,float)
        self.h=np.zeros((2,2)) if hessian is None else np.array(hessian,float)
    @staticmethod
    def of(x):return x if isinstance(x,Jet) else Jet(x)
    def __add__(self,x):
        x=self.of(x);return Jet(self.v+x.v,self.d+x.d,self.h+x.h)
    __radd__=__add__
    def __neg__(self):return Jet(-self.v,-self.d,-self.h)
    def __sub__(self,x):return self+-self.of(x)
    def __rsub__(self,x):return self.of(x)+-self
    def __mul__(self,x):
        x=self.of(x)
        return Jet(self.v*x.v,self.d*x.v+self.v*x.d,self.h*x.v+self.v*x.h+np.outer(self.d,x.d)+np.outer(x.d,self.d))
    __rmul__=__mul__
    def __pow__(self,p):return Jet(self.v**p,p*self.v**(p-1)*self.d,p*self.v**(p-1)*self.h+p*(p-1)*self.v**(p-2)*np.outer(self.d,self.d))
    def exp(self):
        v=np.exp(self.v);return Jet(v,v*self.d,v*(self.h+np.outer(self.d,self.d)))


def metric_jets(t,P,Q,lam):
    tj=Jet(t,[1,0]);a=(lam*.5).exp()*tj**(-.5);e=P.exp();em=(-P).exp()
    g=[[Jet(0) for _ in range(4)] for _ in range(4)]
    g[0][0]=-a;g[1][1]=a;g[2][2]=tj*e;g[2][3]=g[3][2]=tj*e*Q;g[3][3]=tj*(e*Q*Q+em)
    value=np.array([[x.v for x in row] for row in g]);d=np.zeros((4,4,4));dd=np.zeros((4,4,4,4))
    for i in range(4):
        for j in range(4):d[:2,i,j]=g[i][j].d;dd[:2,:2,i,j]=g[i][j].h
    return value,d,dd


def curvature(g,d,dd):
    inv=np.linalg.inv(g);dinv=np.array([-inv@v@inv for v in d]);Gamma=np.zeros((4,4,4));dGamma=np.zeros((4,4,4,4))
    for a in range(4):
        for b in range(4):
            for c in range(4):
                v=np.array([d[b,k,c]+d[c,k,b]-d[k,b,c] for k in range(4)])
                Gamma[a,b,c]=inv[a]@v/2
                for e in range(4):
                    dv=np.array([dd[e,b,k,c]+dd[e,c,k,b]-dd[e,k,b,c] for k in range(4)])
                    dGamma[e,a,b,c]=(dinv[e,a]@v+inv[a]@dv)/2
    R=np.zeros((4,4,4,4))
    for a,b,c,dindex in np.ndindex(4,4,4,4):
        R[a,b,c,dindex]=dGamma[c,a,dindex,b]-dGamma[dindex,a,c,b]+sum(Gamma[a,c,e]*Gamma[e,dindex,b]-Gamma[a,dindex,e]*Gamma[e,c,b] for e in range(4))
    Ricci=np.einsum('abad->bd',R);lower=np.einsum('ae,ebcd->abcd',g,R)
    kretschmann=np.einsum('abcd,ae,bf,cg,dh,efgh->',lower,inv,inv,inv,inv,lower,optimize=True)
    return Ricci,float(kretschmann)


def completed_jets(t,P,Q,Pt,Px,Qt,Qx,Pxx,Qxx,Ptx,Qtx,lam=.1,remove_nonlinear=False):
    e=np.exp(2*P)
    Ptt=Pxx-Pt/t+(0 if remove_nonlinear else e*(Qt*Qt-Qx*Qx))
    Qtt=Qxx-Qt/t-(0 if remove_nonlinear else 2*(Pt*Qt-Px*Qx))
    energy=Pt*Pt+Px*Px+e*(Qt*Qt+Qx*Qx)
    lt=t*energy;lx=2*t*(Pt*Px+e*Qt*Qx)
    ltt=energy+t*(2*Pt*Ptt+2*Px*Ptx+2*e*Pt*(Qt*Qt+Qx*Qx)+2*e*(Qt*Qtt+Qx*Qtx))
    ltx=t*(2*Pt*Ptx+2*Px*Pxx+2*e*Px*(Qt*Qt+Qx*Qx)+2*e*(Qt*Qtx+Qx*Qxx))
    lxx=2*t*(Ptx*Px+Pt*Pxx+2*e*Px*Qt*Qx+e*(Qtx*Qx+Qt*Qxx))
    return Jet(P,[Pt,Px],[[Ptt,Ptx],[Ptx,Pxx]]),Jet(Q,[Qt,Qx],[[Qtt,Qtx],[Qtx,Qxx]]),Jet(lam,[lt,lx],[[ltt,ltx],[ltx,lxx]])


def exact_constraint_identity():
    t,p,pt,px,qt,qx,pxx,qxx,ptx,qtx=s.symbols('t P Pt Px Qt Qx Pxx Qxx Ptx Qtx',real=True)
    e=s.exp(2*p);ptt=pxx-pt/t+e*(qt**2-qx**2);qtt=qxx-qt/t-2*(pt*qt-px*qx)
    derivative_x=t*(2*pt*ptx+2*px*pxx+2*e*px*(qt**2+qx**2)+2*e*(qt*qtx+qx*qxx))
    derivative_t=2*(pt*px+e*qt*qx)+2*t*(ptt*px+pt*ptx+2*e*pt*qt*qx+e*(qtt*qx+qt*qtx))
    identity=s.simplify(derivative_x-derivative_t);assert identity==0
    return str(identity)


def derivative(f):
    n=len(f);k=np.fft.fftfreq(n,1/n)
    return np.fft.ifft(1j*k*np.fft.fft(f)).real


def primitive(f):
    n=len(f);k=np.fft.fftfreq(n,1/n);ff=np.fft.fft(f);out=np.zeros(n,complex)
    out[1:]=ff[1:]/(1j*k[1:]);return np.fft.ifft(out).real


def rhs(t,y):
    P,Q,pi,rho,lam=y.reshape(5,-1);px=derivative(P);qx=derivative(Q);e=np.exp(2*P)
    h=(pi*pi+rho*rho/e)/(2*t)+t*(px*px+e*qx*qx)/2
    return np.array([pi/t,rho/(t*e),rho*rho/(t*e)+t*derivative(px)-t*e*qx*qx,t*derivative(e*qx),2*h]).ravel()


def evolve(n):
    x=np.arange(n)*2*np.pi/n;P=.2*np.cos(x)+.03*np.cos(2*x);Q=.13*np.cos(x)+.04*np.cos(3*x)
    pi=.1*np.cos(x);rho=.05*np.cos(2*x);j=pi*derivative(P)+rho*derivative(Q)
    lam=primitive(2*j);initial=np.array([P,Q,pi,rho,lam]);times=np.linspace(1,1.4,9)
    sol=solve_ivp(rhs,(1,1.4),initial.ravel(),method='DOP853',t_eval=times,rtol=2e-11,atol=2e-13)
    assert sol.success
    constraints=[]
    for t,y in zip(times,sol.y.T):
        P,Q,pi,rho,lam=y.reshape(5,n);j=pi*derivative(P)+rho*derivative(Q)
        constraints.append(dict(t=float(t),momentum_mean=float(j.mean()),metric_constraint_max=float(max(abs(derivative(lam)-2*j)))))
    final=sol.y[:,-1].reshape(5,n);P,Q,pi,rho,lam=final;t=1.4
    Pt,Qt=rhs(t,sol.y[:,-1]).reshape(5,n)[:2];Px=derivative(P);Qx=derivative(Q)
    Pxx=derivative(Px);Qxx=derivative(Qx);Ptx=derivative(Pt);Qtx=derivative(Qt)
    lx=derivative(lam);lxx=derivative(lx);curves=[]
    for j in range(0,n,n//8):
        a,b,c=completed_jets(t,P[j],Q[j],Pt[j],Px[j],Qt[j],Qx[j],Pxx[j],Qxx[j],Ptx[j],Qtx[j],lam[j])
        # Use the independently evolved lambda and its spatial derivatives.
        c.d[1]=lx[j];c.h[1,1]=lxx[j]
        R,K=curvature(*metric_jets(t,a,b,c))
        curves.append(dict(theta=float(x[j]),Ricci_max=float(np.max(abs(R))),Kretschmann=K))
    return dict(spatial_points=n,constraints=constraints,final_fields=final.tolist(),Ricci_controls=curves,ode_evaluations=sol.nfev)


def payload():
    identity=exact_constraint_identity();rng=np.random.default_rng(11992);random=[];bad=[]
    for _ in range(16):
        numbers=rng.uniform(-.3,.3,10);t=float(rng.uniform(.8,1.5))
        jets=completed_jets(t,*numbers);R,K=curvature(*metric_jets(t,*jets))
        corrupted=completed_jets(t,*numbers,remove_nonlinear=True);wrong,_=curvature(*metric_jets(t,*corrupted))
        random.append(dict(Ricci_max=float(np.max(abs(R))),Kretschmann=K));bad.append(float(np.max(abs(wrong))))
    assert max(r['Ricci_max'] for r in random)<1e-11 and max(bad)>.01
    coarse=evolve(32);fine=evolve(64)
    mismatch=float(np.max(abs(np.array(coarse['final_fields'])-np.array(fine['final_fields'])[:,::2])))
    assert mismatch<1e-7 and max(r['metric_constraint_max'] for r in fine['constraints'])<1e-8
    assert max(r['Ricci_max'] for r in fine['Ricci_controls'])<1e-7
    return dict(status='PASS',known_model='Unpolarized vacuum Gowdy T3 in areal time t>0. A supplied genuine symmetry reduction of Einstein GR, not a W33 derivation.',
        metric='ds2=exp(lambda/2)t^(-1/2)(-dt2+dtheta2)+t[exp(P)(dsigma+Q ddelta)^2+exp(-P)ddelta2]',
        Hamiltonian='H=integral[(piP^2+exp(-2P)piQ^2)/(2t)+t(Ptheta^2+exp(2P)Qtheta^2)/2]dtheta',
        canonical_pairs=['P,piP=t Pt','Q,piQ=t exp(2P)Qt'],local_physical_canonical_pairs=2,
        constraints='lambda_t=t(Pt^2+Ptheta^2+exp(2P)(Qt^2+Qtheta^2)); lambda_theta=2(piP Ptheta+piQ Qtheta). Residual global constraint integral(piP Ptheta+piQ Qtheta)=0 ensures periodiclambda.',
        exact_constraint_integrability_residual=identity,
        metric_twojet_Ricci_checks=random,remove_nonlinear_negative_control_Ricci_max=bad,
        evolution32=coarse,evolution64=fine,refinement_final_field_max=mismatch,
        atlas_to_Lorentz_obstruction='so6 is real simple ofdimension15. A Liehomomorphism toso(1,3) ofdimension6 hasidealkernel; itwouldbezero orinjective, andinjectivityisimpossiblebydimension. Henceeverycontinuoushomomorphism SO6->SO+(1,3) istrivial. The11983 connection cannotbe convertedintoa nontrivial4D Lorentzspinconnection by simplypushingitsstructuregroupthrougha homomorphism. Symmetrybreaking/newfields orchangedconnection are required. Internalcompactgauge interpretations remainpossible.',
        native_carrier_gate='11991 suppliesoneof6nativeZ4coverchoices. Choosingone deckcoordinate aspositivearealtime andthree asperiodicspace, plus theGowdy action above, is anadditionalcontinuum/signature/symmetrybreakingchoice. No graphEinsteinvariation orfinitehypersurfacealgebra is claimed.',
        boundary='This establishes a working nonlinear vacuumEinstein benchmark withtwo interactingpolarizations andactualmetric Ricci/constraintchecks. The equations areclassicalpriorart. It doesnotderiveGRfromW33, repair11976finitepointwiseconstraints, provefullunreducedADMclosure/quantumclosure, fixG/Lambda orcouplethe11989flavourvacuum.',
        prior=['11961 sharedcone ADM necessaryconditions','11976 finitecurvedscalarbracketfailure','11985 clocksretainphysicalpairs butarenotGR','TOE38 differentfiniteorthogonal-versusWeilmodulefirewall'],
        primary=['https://arxiv.org/abs/gr-qc/9710102','https://inspirehep.net/literature/113155'])


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11992_nonlinear_einstein_benchmark.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['refinement_final_field_max'],max(r['Ricci_max'] for r in d['evolution64']['Ricci_controls']))
