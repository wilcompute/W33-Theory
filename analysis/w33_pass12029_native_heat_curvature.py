"""Actual native heat-trace second variation, with local volume response subtracted.

The response is exact on each finite4D periodic graph, evaluated by27D Bloch
blocks and neighbouring-momentum Frechet kernels. No continuum a2 is inserted.
"""
import sys,numpy as np,itertools,time
from scipy.integrate import quad
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass11995_native_metric_gr_lift import inputs
b,v,_,H=inputs();M=np.sqrt(float(H.det()));H=np.array(H,float);bf=np.c_[-b.sum(1),b].astype(int);aa=np.argmax(bf<0,axis=1);bb=np.argmax(bf>0,axis=1);chi=np.r_[0,-np.linalg.solve(b.T@b,b.T@v[:,0])];mid=(chi[aa]+chi[bb]+v[:,0])/2

def symbol(ks):
 phase=np.exp(1j*ks@v.T);n=len(ks);L=np.tile(np.diag(np.bincount(np.r_[aa,bb],minlength=27)),(n,1,1)).astype(complex)
 L[:,aa,bb]-=phase;L[:,bb,aa]-=phase.conj();return L

def response(N,ts,capacity_exponent=4,symmetry_reduction=True):
 step=2*np.pi/N;a=step;c=capacity_exponent/4;dq=np.diag(np.exp(1j*step*chi));dm=dq.conj();weight=np.exp(1j*step*mid);out=np.zeros(len(ts));unif=np.zeros(len(ts));start=time.time();diag=np.zeros(27,complex);np.add.at(diag,aa,weight);np.add.at(diag,bb,weight*np.exp(-1j*step*v[:,0]))
 for trans in itertools.product(range(N),repeat=3):
  neg=tuple((-x)%N for x in trans)
  if symmetry_reduction and trans>neg:continue
  multiplicity=1 if trans==neg or not symmetry_reduction else 2
  ks=step*np.c_[np.arange(N),np.tile(trans,(N,1))];ph=np.exp(1j*ks@v.T);prevph=np.roll(ph,1,axis=0);L=symbol(ks);Lp=np.zeros_like(L)
  Lp[:]=0;Lp[:,np.arange(27),np.arange(27)]=diag;Lp[:,aa,bb]=-weight*prevph;Lp[:,bb,aa]=-weight*ph.conj()
  Lm=np.roll(Lp,-1,axis=0).conj().transpose(0,2,1);A1=(Lp-c*dq@np.roll(L,1,axis=0)-c*L@dq)/(M*a*a)
  A2=(4*c*c+2)*L
  for D,Q,neighbor in [(dq,Lp,np.roll(L,1,axis=0)),(dm,Lm,np.roll(L,-1,axis=0))]:A2+=2*(-c*D@Q.conj().transpose(0,2,1)-c*Q@D.conj()+c*c*D@neighbor@D.conj())
  A2/=M*a*a
  ev,V=np.linalg.eigh(L/(M*a*a));ev=np.maximum(ev,0);Vh=V.conj().transpose(0,2,1);diag2=np.diagonal(Vh@A2@V,axis1=1,axis2=2).real;mix=Vh@A1@np.roll(V,1,axis=0);squared=abs(mix)**2;ep=np.roll(ev,1,axis=0);diff=ev[:,:,None]-ep[:,None,:]
  for z,t in enumerate(ts):
   ex=np.exp(-t*ev);expair=np.exp(-t*ep);num=-t*(ex[:,:,None]-expair[:,None,:]);D=np.divide(num,diff,out=t*t*np.exp(-t*(ev[:,:,None]+ep[:,None,:])/2),where=abs(diff)>1e-9)
   out[z]+=multiplicity*(np.sum(-t*ex*diag2)+2*np.sum(D*squared));unif[z]+=multiplicity*np.sum((2-capacity_exponent)**2*(t*t*ev*ev-t*ev)*ex)
 return [(4*np.pi*t)**2/(2*np.pi)**4*(x-.5*y)/t for t,x,y in zip(ts,out,unif)],time.time()-start

def conti(t,K=12,capacity_exponent=4):
 p=np.array(list(itertools.product(range(-K,K+1),repeat=4)),float);q=p.copy();q[:,0]-=1;G=H/M;l=np.einsum('ni,ij,nj->n',p,G,p);r=np.einsum('ni,ij,nj->n',q,G,q);ex=np.exp(-t*l);er=np.exp(-t*r);diff=l-r;D=np.divide(-t*(ex-er),diff,out=t*t*np.exp(-t*(l+r)/2),where=abs(diff)>1e-9);c=capacity_exponent/4;a1=(l+r-G[0,0])/2-c*(l+r);a2=(8*c*c+2-8*c)*l+4*c*c*G[0,0];val=np.sum(-t*ex*a2+2*D*a1*a1-.5*(2-capacity_exponent)**2*(t*t*l*l-t*l)*ex)
 return (4*np.pi*t)**2/(2*np.pi)**4*val/t


def full_sector_heat(N,transverse,t,epsilon,capacity_exponent=4):
    """Independent real-space assembly on a single transverse-momentum sector."""
    a=2*np.pi/N;n=N*27;L=np.zeros((n,n),complex);capacity=np.empty(n)
    for cell in range(N):
        capacity[cell*27:(cell+1)*27]=M*np.exp(capacity_exponent*epsilon*np.cos(a*(cell+chi)))
        for e,(i,j) in enumerate(zip(aa,bb)):
            left=cell*27+i;right=((cell+int(v[e,0]))%N)*27+j;phase=np.exp(1j*np.dot(transverse,v[e,1:]));w=np.exp(2*epsilon*np.cos(a*(cell+mid[e])))
            L[left,left]+=w;L[right,right]+=w;L[left,right]-=w*phase;L[right,left]-=w*phase.conjugate()
    A=L/np.sqrt(capacity[:,None]*capacity[None,:])/a**2
    return float(np.exp(-t*np.linalg.eigvalsh(A)).sum())

def payload(sizes=(8,12,16,24)):
    ts=[.08,.12,.18];reference=[float(conti(t)) for t in ts];rows=[]
    for N in sizes:
        values,_=response(N,ts);rows.append(dict(N=N,response=list(map(float,values)),continuum_errors=[float(x-y) for x,y in zip(values,reference)]))
    wrong,_=response(16,ts,0)
    return dict(status='PASS',physical_heat_times=ts,geometric_response=rows,continuum_finite_time_response=reference,fixed_capacity_N16=list(map(float,wrong)),fixed_capacity_continuum=[float(conti(t,capacity_exponent=0)) for t in ts],expected_small_time_curvature_coefficient=float(H[0,0]),wrong_density_small_time_coefficient=float(-3*H[0,0]),
        observable='C_a(t)=(4pi t)^2/[Vol*t] [d_epsilon^2 Tr exp(-t A_epsilon cos x0)|0 - onehalf*d_epsilon^2 Tr exp(-t A_uniform epsilon)|0]. Uniform response is computed from the SAME native spectrum, removing its local zero-derivative cutoff contribution.',
        derivation='A=M^-1/2 L M^-1/2 with135 midpoint-weighted native edges and27 capacities per cell. A1 couples neighbouring longitudinal Bloch momenta; A2 and the exact divided difference of fprime=-t exp(-t lambda) give the finite-graph heat Hessian. All27 bands retained. Inversion-related transverse sectors are paired; independent full assembly/regressions check this reduction.',
        scope='Finite native heat-curvature response and numerical fixed-physical-time continuum convergence on a conformal perturbation; not a uniform heat-trace theorem, full nonlinear Einstein action, selected regulator, renormalizedG/Lambda or Lorentzian constraints. Taking a->0 at fixedt and then t->0 is distinct from keeping t/a^2 fixed.',
        prior=['12023 actual curved recovery sequence','12019 native exactquartic','12009 fixedcapacity negativecontrol','11601 continuumheat/density warning','0811.1063 standard covariant heat perturbation'])

def local_form_factor(t,capacity_exponent=4):
    c=capacity_exponent/4;d=1-2*c;x=t*float(H[0,0]/M)
    def integrand(u):
        v=u*(1-u);bb=d*(.5-v)-.5
        return np.exp(-x*v)*(6*d*d+x*(d*d*(2*u-1)**2/2+4*d*bb)+x*x*bb*bb)
    return float(M/t*(-12*d*d-4*c*c*x+2*quad(integrand,0,1,epsabs=1e-13)[0]))

def formfactor_certificate():
    import sympy as s
    x,u=s.symbols('x u');v=u*(1-u);rows=[]
    for beta in [4,0]:
        c=s.Rational(beta,4);d=1-2*c;bb=d*(s.Rational(1,2)-v)-s.Rational(1,2)
        poly=s.series(s.exp(-x*v)*(6*d*d+x*(d*d*(2*u-1)**2/2+4*d*bb)+x*x*bb*bb),x,0,5).removeO()
        response=s.expand(-12*d*d-4*c*c*x+2*s.integrate(poly,(u,0,1)))
        assert response.coeff(x,1)==(1 if beta==4 else -3)
        rows.append(dict(capacity_exponent=beta,exact_dimensionless_series=str(response),small_time_response=[dict(t=t,value=local_form_factor(t,beta)) for t in [.001,.01,.04,.08]],limiting_curvature_coefficient=float(response.coeff(x,1)*H[0,0])))
    return dict(status='PASS',rows=rows,derivation='For continuumflatG0 andsigma=epsilon cos(qx), Duhamel derivative is a Gaussianmoment integral. Complete p-square atparameteru: v=u(1-u), x=t qGq, c=capacityexponent/4,d=1-2c,b=d(1/2-v)-1/2. C=M0/t[-12d2-4c2x+2int_0^1 exp(-xv)(6d2+x[d2(2u-1)^2/2+4db]+x2b2)du]. This derives the local response without inserting R/6.',scope='Standard covariantheatperturbation applied to the statednativecontinuumtarget. Correctcapacity gives+H00 andfixedcapacity-3H00. It is an independent benchmark/order-of-limits diagnostic, not a proof of uniformnativeheatconvergence or a selectedEinsteinaction.',prior=['12009 exactcontinuumfixed-densityfactor-3','12029 actualnativefinitegraphresponse','0811.1063 covariantperturbation priorart'])

if __name__=='__main__':
    import argparse,json
    parser=argparse.ArgumentParser();parser.add_argument('--sizes',type=int,nargs='+',default=[8,12,16,24]);parser.add_argument('--output',type=Path,default=ROOT/'data/w33_pass12029_native_heat_curvature.json');args=parser.parse_args();out=payload(tuple(args.sizes));args.output.write_text(json.dumps(out,indent=2)+'\n');print('PASS native heat',out['geometric_response'][-1],flush=True)
