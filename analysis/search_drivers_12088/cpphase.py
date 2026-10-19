import sys, itertools
import numpy as np
from scipy.optimize import least_squares, root
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
n=np.arange(-10,11);n1,n2=np.meshgrid(n,n,indexing='ij');v1=n1[None,None,:,:]+np.arange(3)[:,None,None,None]/3;v2=n2[None,None,:,:]+np.arange(3)[None,:,None,None]/3
D=np.exp(1j*np.pi*np.arange(3)**2/3)
def theta(y,eu,yd,ed,z,up=False):
    O11=1+1j*y;O22=O11 if up else 1j*yd;e=1j*(eu if up else ed)
    A=np.exp(3j*np.pi*(O11*v1*v1+2*e*v1*v2+O22*v2*v2)+6j*np.pi*v2*(0 if up else 1j*z)).sum(axis=(-2,-1))
    A=D.conj()[:,None]*A
    if up: A=A*D.conj()[None,:]
    return A.real/np.linalg.norm(A)
Utarget=np.array([.620/168.26,1.23e-3/.620])
r=root(lambda p: np.log(np.array((lambda a:[a[1]/a[0],a[2]/a[1]])(np.linalg.svd(theta(p[0],p[1],0,0,0,True),compute_uv=False)))/Utarget),[.8745,.00552])
y,eu=r.x; Uu=np.linalg.svd(theta(y,eu,0,0,0,True))[0]
target=np.array([.053/2.86,2.67e-3/.053,.225,.0411,.00382,3.08e-5])
def obs(yd,ed,zi,b):
    m=theta(y,eu,yd,ed,zi)
    K=np.eye(3)-np.outer(b.conj(),b)/(1+np.vdot(b,b).real)
    ev,O=np.linalg.eigh(K);A=(O*np.sqrt(ev))@O.conj().T
    Ud,sd,_=np.linalg.svd(m@A);V=(Uu.conj().T@Ud)[::-1,::-1]
    J=np.imag(V[0,0]*V[1,1]*V[0,1].conj()*V[1,0].conj())
    return np.array([sd[1]/sd[0],sd[2]/sd[1],abs(V[0,1]),abs(V[1,2]),abs(V[0,2]),J])
def res(o): return np.r_[np.log(np.maximum(o[:5],1e-30)/target[:5]),(o[5]-target[5])/target[5]]
def fit(make, npar, starts=40, seed=0):
    rng=np.random.default_rng(seed); best=None
    for _ in range(starts):
        p0=np.r_[rng.uniform(-3,.2),rng.uniform(.005,.07),rng.uniform(-.06,.06),rng.normal(0,3,npar-3)]
        def F(p):
            try:
                if y*np.exp(p[0])-p[1]**2<.005: return np.ones(6)*100
                return res(obs(np.exp(p[0]),p[1],p[2],make(p)))
            except Exception: return np.ones(6)*100
        f=least_squares(F,p0,max_nfev=800)
        if best is None or np.linalg.norm(f.fun)<np.linalg.norm(best.fun): best=f
    return best
# control: equal magnitudes, continuous phases (6 params)
c=fit(lambda p: p[3]*np.array([1,np.exp(1j*p[4]),np.exp(1j*p[5])]),6)
print('control equal-|b|, continuous phases: |res| =', np.linalg.norm(c.fun), ' phases/(pi/3) =', (np.array(c.x[4:6])/(np.pi/3))%6)
out=[]
for k,l in itertools.product(range(6),repeat=2):
    f=fit(lambda p,k=k,l=l: p[3]*np.array([1,np.exp(1j*k*np.pi/3),np.exp(1j*l*np.pi/3)]),4,starts=12,seed=k*6+l)
    out.append((np.linalg.norm(f.fun),k,l))
out.sort()
print('best quantised (k,l):', [(round(a,4),k,l) for a,k,l in out[:6]])
# also unequal magnitudes with quantised phases (6 params): fits?
q=min((fit(lambda p,k=k,l=l: np.array([p[3],p[4]*np.exp(1j*k*np.pi/3),p[5]*np.exp(1j*l*np.pi/3)]),6,starts=8,seed=100+k*6+l),k,l) for k,l in [(1,2),(2,1),(1,1),(2,4)]) if False else None
