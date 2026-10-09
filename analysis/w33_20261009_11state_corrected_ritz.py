"""Sign-corrected eleven-state: Gaussian plus collective point/line He2,4,6,8,10.
Proof boundary: Ritz upper bound ONLY. Uses W33 incidence orbit reduction.
"""
from pathlib import Path
from collections import Counter
import numpy as np, math, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as vacuum
import w33_20261008_5state_ritz as first
OUT=ROOT/'data/w33_20261009_11state_corrected_ritz.json'
DEGREES=(2,4,6,8,10)
def block(edges,wa,wb,sa,sb,tr,order=9,left=DEGREES,right=DEGREES):
    nodes,weights=np.polynomial.hermite_e.hermegauss(order);weights/=np.sqrt(2*np.pi)
    xi=np.array(np.meshgrid(nodes,nodes,nodes,nodes,indexing='ij')).reshape(4,-1)
    prob=np.prod(np.array(np.meshgrid(weights,weights,weights,weights,indexing='ij')),axis=0).ravel()
    m,t,f=(tr[k] for k in ('m','t','f'))
    h=np.zeros((len(left),len(right)),complex)
    sig=np.sqrt(108*t)
    rho=float(wa@wb/216) if sa==sb else 0.
    parity1=1 if sa=='p' else -1;parity2=1 if sb=='p' else -1
    groups=Counter((int(wa[p if sa=='p' else l-40]),int(wb[p if sb=='p' else l-40])) for p,l in edges)
    for (r,s),count in groups.items():
        c1=parity1*t*r/(2*sig);d1=r/(2*sig)
        c2=parity2*t*s/(2*sig);d2=s/(2*sig)
        cov=np.array([[t*m,0,c1,c2],[0,m/t,d1,d2],[c1,d1,1,rho],[c2,d2,rho,1]])
        ev,rot=np.linalg.eigh(cov)
        assert min(ev)>-2e-12
        x,z,y1,y2=(rot*np.sqrt(np.maximum(ev,0)))@xi
        rows=[]
        for y,endpoint,degs in ((y1,r,left),(y2,s,right)):
            js=[]
            for n in degs:
                hn=first.herm(n,y);deriv=n*first.herm(n-1,y)
                js.append((x+np.sqrt(.05))*((f*x+np.sqrt(.05)+1j*z)*hn-1j*endpoint/sig*deriv)/np.sqrt(math.factorial(n)))
            rows.append(np.array(js))
        h+=count*(rows[0].conj()*prob)@rows[1].T
    return h
def ritz(order):
    geo=first.geometry();first.orbit_guard(geo)
    edges,N,A,B,Wp,Wl=geo;tr=vacuum.exact_trial()
    def same(side,adj,W):
        indices=[0,int(np.flatnonzero(adj[0])[0]),int(np.flatnonzero((adj[0]==0)&(np.arange(40)!=0))[0])]
        return sum(k*block(edges,W[0],W[j],side,side,tr,order) for k,j in zip((40,480,1080),indices))
    pp=same('p',A,Wp);ll=same('l',B,Wl)
    inc=int(np.flatnonzero(N[0])[0]);non=int(np.flatnonzero(N[0]==0)[0])
    pl=160*block(edges,Wp[0],Wl[inc],'p','l',tr,order)+1440*block(edges,Wp[0],Wl[non],'p','l',tr,order)
    norm=np.array([40*(1+12/(3**n)+27/(9**n)) for n in DEGREES])
    z=np.sqrt(np.outer(norm,norm))
    h=np.zeros((11,11),complex);h[0,0]=tr['energy']
    # Independent vacuum coupling for every Hermite degree, point and line.
    ixp=[1,3,5,7,9];ixl=[2,4,6,8,10]
    for side,W,ix in [('p',Wp,ixp),('l',Wl,ixl)]:
        c=40*block(edges,W[0],W[0],side,side,tr,order,left=(0,),right=DEGREES)
        for j,k in enumerate(ix):
            h[0,k]=c[0,j]/np.sqrt(norm[j]);h[k,0]=h[0,k].conjugate()
    h[np.ix_(ixp,ixp)]=pp/z;h[np.ix_(ixl,ixl)]=ll/z
    h[np.ix_(ixp,ixl)]=pl/z;h[np.ix_(ixl,ixp)]=(pl/z).conj().T
    assert np.max(np.abs(h-h.conj().T))<1e-8
    return h
def main():
    h9=ritz(13);h10=ritz(14)
    diff=float(np.max(np.abs(h9-h10)))
    assert diff<1e-7
    ev,vec=np.linalg.eigh(h9)
    old=float(np.linalg.eigvalsh(h9[:9,:9])[0])
    assert old<127.596
    result=dict(status='PASS',ritz11=float(ev[0]),ritz9=old,
                improvement=float(old-ev[0]),quadrature13_14_error=diff,
                eigenvalues=list(map(float,ev)))
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(result)
if __name__=='__main__':main()
