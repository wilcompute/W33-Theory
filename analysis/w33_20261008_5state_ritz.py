"""Pass 20261008: exact orbit-reduced five-state W33 current Ritz calculation."""
from pathlib import Path
from collections import Counter
import hashlib, json, math, sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as prior
OUT=ROOT/'data/w33_20261008_collective_hermite2_4_ritz.json'
def herm(n,y):return np.polynomial.hermite_e.hermeval(y,[0]*n+[1])
def geometry():
    edges=prior.actual_edges()
    N=np.zeros((40,40),dtype=int)
    for p,l in edges:N[p,l-40]=1
    assert len(edges)==160 and np.all(N.sum(axis=0)==4) and np.all(N.sum(axis=1)==4)
    A=(N@N.T==1).astype(int);B=(N.T@N==1).astype(int)
    np.fill_diagonal(A,0);np.fill_diagonal(B,0)
    assert np.all(A.sum(axis=0)==12) and np.all(B.sum(axis=0)==12)
    Wp=np.where(np.eye(40,dtype=bool),9,np.where(A,-3,1))
    Wl=np.where(np.eye(40,dtype=bool),9,np.where(B,-3,1))
    assert np.all(N.T@Wp.T==0) and np.all(N@Wl.T==0)
    return edges,N,A,B,Wp,Wl
def orbit_guard(g):
    edges,N,A,B,Wp,Wl=g;seen={}
    for s,W in [('p',Wp),('l',Wl)]:
        for u,Q in ([('p',Wp),('l',Wl)] if s=='p' else [('l',Wl)]):
            for i in range(40):
                for j in range(40):
                    typ=('self' if i==j else 'adj' if (A if s=='p' else B)[i,j] else 'far') if s==u else ('incident' if N[i,j] else 'not')
                    counts=tuple(sorted(Counter((int(W[i,p if s=='p' else l-40]),int(Q[j,p if u=='p' else l-40])) for p,l in edges).items()))
                    key=(s,u,typ)
                    if key in seen:assert seen[key]==counts
                    else:seen[key]=counts
    assert len(seen)==8
    return len(seen)
def pair(edges,wi,wj,si,sj,tr,order):
    xh,wh=np.polynomial.hermite_e.hermegauss(order);wh/=np.sqrt(2*np.pi)
    eta=np.array(np.meshgrid(xh,xh,xh,xh,indexing='ij')).reshape(4,-1)
    weights=np.prod(np.array(np.meshgrid(wh,wh,wh,wh,indexing='ij')),axis=0).ravel()
    m,t,f=(tr[k] for k in ('m','t','f'))
    sigma=np.sqrt(108*t);vx,vz=t*m,m/t
    a,b=(1 if s=='p' else -1 for s in (si,sj))
    rho=float(wi@wj/216) if si==sj else 0.
    counts=Counter((int(wi[p if si=='p' else l-40]),int(wj[p if sj=='p' else l-40])) for p,l in edges)
    result=np.zeros((2,2),complex)
    for (r,s),count in counts.items():
        c1,d1=a*t*r/(2*sigma),a*r/(2*sigma)
        c2,d2=b*t*s/(2*sigma),b*s/(2*sigma)
        cov=np.array([[vx,0,c1,c2],[0,vz,d1,d2],[c1,d1,1,rho],[c2,d2,rho,1]])
        eig,rot=np.linalg.eigh(cov);assert eig.min()>-2e-12
        x,z,y1,y2=(rot*np.sqrt(np.maximum(eig,0)))@eta
        rows=[]
        for y,r0,sgn in ((y1,r,a),(y2,s,b)):
            stack=[]
            for n in (2,4):
                hn=herm(n,y);der=n*herm(n-1,y)
                stack.append((x+np.sqrt(.05))*((f*x+np.sqrt(.05)+1j*z)*hn-1j*sgn*r0/sigma*der)/np.sqrt(math.factorial(n)))
            rows.append(np.array(stack))
        result+=count*(rows[0].conj()*weights)@rows[1].T
    return result
def build_matrix(g,tr,order):
    edges,N,A,B,Wp,Wl=g
    def same(side,adj,W):
        ix=[0,int(np.flatnonzero(adj[0])[0]),int(np.flatnonzero((adj[0]==0)&(np.arange(40)!=0))[0])]
        block=sum(mul*pair(edges,W[0],W[j],side,side,tr,order) for mul,j in zip((40,480,1080),ix))
        return block
    pp=same('p',A,Wp);ll=same('l',B,Wl)
    inc=int(np.flatnonzero(N[0])[0]);far=int(np.flatnonzero(N[0]==0)[0])
    pl=160*pair(edges,Wp[0],Wl[inc],'p','l',tr,order)+1440*pair(edges,Wp[0],Wl[far],'p','l',tr,order)
    norms=np.array([320/3,11200/243]);den=np.sqrt(np.outer(norms,norms))
    h=np.zeros((5,5),complex);h[0,0]=tr['energy']
    k=35*np.sqrt(6)*(tr['f']*tr['t']+1j)**2/108
    h[0,3]=40*k.conjugate()/np.sqrt(norms[1])
    h[0,4]=40*k/np.sqrt(norms[1])
    h[3,0]=h[0,3].conjugate();h[4,0]=h[0,4].conjugate()
    h[np.ix_([1,3],[1,3])]=pp/den
    h[np.ix_([2,4],[2,4])]=ll/den
    h[np.ix_([1,3],[2,4])]=pl/den
    h[np.ix_([2,4],[1,3])]=(pl/den).conj().T
    assert np.max(np.abs(h-h.conj().T))<1e-8
    return h
def payload():
    geo=geometry()
    return geo
def run():
    geo=geometry()
    orbit_guard(geo)
    tr=prior.exact_trial()
    low=build_matrix(geo,tr,7)
    high=build_matrix(geo,tr,8)
    err=float(np.max(np.abs(low-high)))
    assert err<2e-9
    vals,vec=np.linalg.eigh(low)
    old=float(np.linalg.eigvalsh(low[np.ix_([0,3,4],[0,3,4])])[0])
    assert abs(old-127.61950907272602)<1e-8
    assert vals[0]<old-0.0001
    result={'status':'PASS','upper_bound':float(vals[0]),'old_bound':old,'improvement':float(old-vals[0]),'quadrature_error':err,'orbit_classes':8}
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(result)
if __name__=='__main__':run()
