"""Rational outward-rounded Wick audit of the actual nine-state trial.

The trial space belongs to the parallel October 9 nine-state calculation.
Here no quadrature, fitted covariance eigensystem or floating eigenvalue
is used as a proof. A rational trial vector has an enclosed Rayleigh quotient.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from math import factorial, isqrt
from pathlib import Path
import hashlib, json, sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261008_5state_ritz as prior
SCALE=10**36
OUT=ROOT/'data/w33_pass11786_certified_spectral_transitions.json'

def floor_grid(x): return F((x.numerator*SCALE)//x.denominator,SCALE)
def ceil_grid(x): return -floor_grid(-x)

@dataclass(frozen=True)
class I:
    lo:F
    hi:F
    def __init__(self,lo=0,hi=None):
        object.__setattr__(self,'lo',F(lo));object.__setattr__(self,'hi',F(lo if hi is None else hi))
        assert self.lo<=self.hi
    @staticmethod
    def cast(x):return x if isinstance(x,I) else I(x)
    @staticmethod
    def rounded(lo,hi):return I(floor_grid(lo),ceil_grid(hi))
    def __add__(self,other):
        o=I.cast(other);return I.rounded(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,o):return self+-I.cast(o)
    def __rsub__(self,o):return I.cast(o)+-self
    def __mul__(self,other):
        o=I.cast(other);v=[a*b for a in (self.lo,self.hi) for b in (o.lo,o.hi)]
        return I.rounded(min(v),max(v))
    __rmul__=__mul__
    def reciprocal(self):
        assert self.lo*self.hi>0
        return I.rounded(1/self.hi,1/self.lo)
    def __truediv__(self,o):return self*I.cast(o).reciprocal()
    def __rtruediv__(self,o):return I.cast(o)*self.reciprocal()
    def __pow__(self,n):
        assert n>=0 and isinstance(n,int)
        z=I(1)
        for _ in range(n):z=z*self
        return z
    def sqrt(self):
        assert self.lo>=0
        def low(x):return F(isqrt((x.numerator*SCALE*SCALE)//x.denominator),SCALE)
        l,h=low(self.lo),low(self.hi)
        return I(l,h if h*h==self.hi else h+F(1,SCALE))
    def data(self):return [str(self.lo),str(self.hi)]
    def mid(self):return float((self.lo+self.hi)/2)

def parameters():
    m=(6*I(10).sqrt()+15)/40;b=F(1,20)
    def poly(t,m0):return (t*t-1)*(3*m0*t+b)**2-4*b*b*t*t
    lo,hi=F(1),F(2)
    for _ in range(110):
        mid=(lo+hi)/2
        if poly(mid,m.hi)<0:lo=mid
        elif poly(mid,m.lo)>0:hi=mid
        else:break
    assert poly(lo,m.hi)<0<poly(hi,m.lo)
    t=I(lo,hi);f=-2*b/(3*m*t+b)
    e=160*(m*m+b*m*(t+1/t)+b*b-4*b*b*t*m/(3*m*t+b))
    return m,t,f,e

def hermite(n):
    return {n-2*k: F((-1)**k*factorial(n),2**k*factorial(k)*factorial(n-2*k))
            for k in range(n//2+1)}

def current_polynomial(n,yindex,derivative,a,f):
    # J(He_n psi)/psi = R+iZ; common 1/sqrt(n!) applied later.
    real={};imag={}
    def add(p,exp,c):p[exp]=p.get(exp,I(0))+c
    for power,h in hermite(n).items():
        for xp,c in [(2,f),(1,a*(1+f)),(0,a*a)]:
            ex=[0]*4;ex[0]=xp;ex[yindex]=power;add(real,tuple(ex),h*c)
        for xp,c in [(1,I(1)),(0,a)]:
            ex=[0]*4;ex[0]=xp;ex[1]=1;ex[yindex]=power;add(imag,tuple(ex),h*c)
        if power:
            for xp,c in [(1,I(1)),(0,a)]:
                ex=[0]*4;ex[0]=xp;ex[yindex]=power-1
                add(imag,tuple(ex),-derivative*power*h*c)
    return real,imag

def wick(cov):
    @lru_cache(None)
    def moment(ex):
        if sum(ex)%2:return I(0)
        if not any(ex):return I(1)
        i=next(j for j,x in enumerate(ex) if x);rest=list(ex);rest[i]-=1
        out=I(0)
        for j,count in enumerate(rest):
            if count:
                smaller=rest.copy();smaller[j]-=1
                out+=count*cov[i][j]*moment(tuple(smaller))
        return out
    def pair(p,q):
        return sum((c*d*moment(tuple(a+b for a,b in zip(x,y)))
                    for x,c in p.items() for y,d in q.items()),I(0))
    return pair

DEGREES=(2,4,6,8)
def block(edges,wa,wb,sa,sb,m,t,f,left=DEGREES,right=DEGREES):
    sigma=(108*t).sqrt();a=I(F(1,20)).sqrt()
    rho=F(int(wa@wb),216) if sa==sb else F(0)
    pa,pb=(1 if side=='p' else -1 for side in (sa,sb))
    groups=Counter((int(wa[p if sa=='p' else l-40]),int(wb[p if sb=='p' else l-40])) for p,l in edges)
    out=[[(I(0),I(0)) for _ in right] for _ in left]
    for (r,s),count in groups.items():
        # X=Vq has the point/line sign. Z=U*C0^-1*q/t and
        # U.grad(Y) have NO line-side sign. Check against the80D covariance.
        c1,d1=pa*t*r/(2*sigma),r/(2*sigma)
        c2,d2=pb*t*s/(2*sigma),s/(2*sigma)
        cov=[[t*m,I(0),c1,c2],[I(0),m/t,d1,d2],
             [c1,d1,I(1),I(rho)],[c2,d2,I(rho),I(1)]]
        expect=wick(cov)
        ls=[current_polynomial(n,2,r/sigma,a,f) for n in left]
        rs=[current_polynomial(n,3,s/sigma,a,f) for n in right]
        for i,(lr,li) in enumerate(ls):
            for j,(rr,ri) in enumerate(rs):
                den=I(factorial(left[i])*factorial(right[j])).sqrt()
                x,y=out[i][j]
                out[i][j]=(x+count*(expect(lr,rr)+expect(li,ri))/den,
                           y+count*(expect(lr,ri)-expect(li,rr))/den)
    return out

def matrix():
    edges,n,adj,adjl,wp,wl=prior.geometry();prior.orbit_guard((edges,n,adj,adjl,wp,wl))
    m,t,f,e=parameters();norm=[F(40)*(1+F(12,3**k)+F(27,9**k)) for k in DEGREES]
    h=[[(I(0),I(0)) for _ in range(9)] for _ in range(9)];h[0][0]=(e,I(0))
    def collect(wa,W,indices,weights,sa,sb):
        blocks=[block(edges,wa,W[j],sa,sb,m,t,f) for j in indices]
        return [[tuple(sum((weight*b[i][j][part] for weight,b in zip(weights,blocks)),I(0))
                       for part in range(2)) for j in range(4)] for i in range(4)]
    ips=[1,3,5,7];ils=[2,4,6,8]
    for side,adj0,W,ix in [('p',adj,wp,ips),('l',adjl,wl,ils)]:
        js=[0,int(np.flatnonzero(adj0[0])[0]),int(np.flatnonzero((adj0[0]==0)&(np.arange(40)!=0))[0])]
        b=collect(W[0],W,js,[40,480,1080],side,side)
        for i in range(4):
            for j in range(4):h[ix[i]][ix[j]]=tuple(x/I(norm[i]*norm[j]).sqrt() for x in b[i][j])
        # All vacuum couplings computed, including the previously set-zero He2/6/8 entries.
        c=block(edges,W[0],W[0],side,side,m,t,f,left=(0,))[0]
        for j,k in enumerate(ix):
            re,im=(40*x/I(norm[j]).sqrt() for x in c[j])
            h[0][k]=(re,im);h[k][0]=(re,-im)
    js=[int(np.flatnonzero(n[0])[0]),int(np.flatnonzero(n[0]==0)[0])]
    b=collect(wp[0],wl,js,[160,1440],'p','l')
    for i in range(4):
        for j in range(4):
            re,im=(x/I(norm[i]*norm[j]).sqrt() for x in b[i][j])
            h[ips[i]][ils[j]]=(re,im);h[ils[j]][ips[i]]=(re,-im)
    return h

def rayleigh(h,vector):
    # Re(conj(c_i) H_ij c_j), with rational real and imaginary trial coefficients.
    num=I(0);den=sum(x*x+y*y for x,y in vector)
    for i,(a,b) in enumerate(vector):
        for j,(c,d) in enumerate(vector):
            re,im=h[i][j];num+=re*(a*c+b*d)-im*(a*d-b*c)
    return num/den

def certificate():
    h=matrix();mid=np.array([[complex(re.mid(),im.mid()) for re,im in row] for row in h])
    _,vec=np.linalg.eigh(mid)
    vector=[(F(f'{z.real:.13f}'),F(f'{z.imag:.13f}')) for z in vec[:,0]]
    energy=rayleigh(h,vector)
    assert energy.hi<F('127.595533')
    # Analytic 11769 two-state span certifies an ordered second-energy upper bound.
    m,t,f,e=parameters();b=F(1,20)
    d=(21600*f*f*m*m*t**3+4320*f*f*m*t**3+360*f*f*m*t*t+
       525*f*f*t**3+36*f*f*t*t+1440*f*m*t*t+144*f*t*t+
       7200*m*m*t+360*m*t*t+1440*m*t+360*m+36*t*t+193*t+36)/(45*t)
    k2=F(35**2*6,108**2)*(1+f*f*t*t)**2
    ordered_second=(e+d+((d-e)**2+4*k2).sqrt())/2
    couplings={str(k):[x.data() for x in h[0][k]] for k in range(1,9)}
    return dict(schema='w33.pass11786.v1',status='PASS',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        method='Exact Wick recurrence; rational outward rounding on grid10^-36 after every operation; isqrt square-root enclosure; rational endpoint root signs. Floating eigenvectors only choose a rational witness.',
        prior='analysis/w33_20261009_9state_ritz.py owns the nine-state trial; analysis/w33_pass11769_quantized_current_vacuum.py owns the analytic two-state span.',
        m_interval=m.data(),t_interval=t.data(),f_interval=f.data(),
        trial_coefficients=[[str(x),str(y)] for x,y in vector],
        rayleigh_interval=energy.data(),ground_energy_upper_bound='127.595533',
        coordinate_sign_audit='For side parity s=+1 point,-1 line: Cov(X,Y)=s*t*r/(2*sigma), Cov(Z,Y)=r/(2*sigma), U.grad(Y)=r/sigma. The earlier5/7/9-state block used s on all three quantities. The old floating9-state value127.595518296517 is superseded as a certified claim; the corrected rational witness is enclosed here.',
        ordered_second_energy_upper_interval=ordered_second.data(),
        matrix_intervals=[[[re.data(),im.data()] for re,im in row] for row in h],
        all_vacuum_couplings=couplings,
        transition_observables='For T-real exact eigenvectors g,e with E_e>E0, S+=|e><g|, S-=S+*, A=S++S-, B=i(S+-S-); [H,S+]=(E_e-E0)S+ and -i<g|[A,B]|g>=2. These are bounded observables, not named current polynomials.',
        boundaries='Only an upper bound on E0. The Rayleigh lower endpoint does NOT lower-bound E0. Ordered second energy need not be the first distinct excitation if the ground is degenerate. No numerical ground lower bound or numerical gap is established.')

if __name__=='__main__':
    out=certificate();OUT.write_text(json.dumps(out,indent=2)+'\n')
    print('11786 PASS rational nine-state upper bound',out['ground_energy_upper_bound'],flush=True)
