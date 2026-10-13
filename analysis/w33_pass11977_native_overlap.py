"""Native11970 spinor kernel promoted to Euclidean overlap/GW fermions.

TOE41 owns zero-index pairing of a different80-band bipartite kernel.
Here the320-band Clifford kernel has actual3D acoustic Dirac low modes.
Euclidean time, Wilson mass and spinor factor are supplied. No3families.
"""
from pathlib import Path
import json
import sys
import numpy as np
from scipy.linalg import eigh,svdvals
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass11970_native_wilson_dirac import construction


def clifford():
    _,_,_,alpha,beta,_=construction()
    gamma=[-1j*beta@a for a in alpha]+[beta]
    g5=gamma[0]@gamma[1]@gamma[2]@gamma[3]
    for i in range(4):
        for j in range(4):assert np.max(abs(gamma[i]@gamma[j]+gamma[j]@gamma[i]-2*(i==j)*np.eye(4)))<1e-14
    return gamma,g5


def kernel(k,omega=0.,phases=None,m0=.5,r=10.,rt=1.):
    ed,volts,J,*_=construction();gamma,g5=clifford()
    phase=np.exp(1j*(volts@np.asarray(k)+(np.zeros(160) if phases is None else phases)))
    B=np.zeros((160,80),complex);C=np.zeros_like(B)
    for e,(a,b) in enumerate(ed):B[e,a]=-1;B[e,b]=phase[e];C[e,a]=.5;C[e,b]=.5*phase[e]
    L=B.conj().T@B;K=[-1j*C.conj().T@(J[:,i,None]*B) for i in range(3)]
    DW=1j*sum(np.kron(g,K) for g,K in zip(gamma,K))+1j*np.sin(omega)*np.kron(gamma[3],np.eye(80))
    DW+=np.kron(np.eye(4),r*L+(rt*(1-np.cos(omega))-m0)*np.eye(80))
    G5=np.kron(g5,np.eye(80));Q=G5@DW
    assert np.max(abs(Q-Q.conj().T))<1e-11
    return Q,G5


def overlap(k,omega=0.,phases=None):
    Q,G5=kernel(k,omega,phases);ev,U=eigh(Q)
    assert min(abs(ev))>1e-8
    sign=(U*np.sign(ev))@U.conj().T;D=np.eye(320)+G5@sign
    defect=float(np.max(abs(D@G5+G5@D-D@G5@D)))
    return D,Q,G5,ev,dict(gap=float(min(abs(ev))),index=int(round(-.5*sum(np.sign(ev)))),GW_max=defect)


def payload():
    D,Q,G5,ev,origin=overlap([0,0,0])
    assert sum(svdvals(D)<1e-9)==4 and origin['index']==0
    gamma,g5=clifford();pair=np.kron(1j*gamma[3]@g5,np.eye(80))
    assert np.max(abs(pair@Q+Q@pair))<1e-11
    rows=[];p=np.array([2.,-1,3]);p*=.8/np.linalg.norm(p)
    for a in (.02,.01,.005):
        d,*_,record=overlap(a*p,.6*a)
        low=np.sort(svdvals(d))[:4]*.5/a
        record.update(spacing=a,scaled_singular_values=low.tolist(),error=float(max(abs(low-1))))
        rows.append(record)
    assert rows[-1]['error']<rows[0]['error']/2
    rng=np.random.default_rng(11977);ph=rng.uniform(-.15,.15,160)
    dr,qr,_,er,random=overlap([0,0,0],phases=ph)
    assert random['index']==0 and np.max(abs(pair@qr+qr@pair))<1e-11
    # Gauge/rechart covariance is checked without assuming special vertex labels.
    theta=rng.uniform(-2,2,80);ed,*_=construction()
    pg=ph+np.array([theta[b]-theta[a] for a,b in ed])
    dg,*_=overlap([0,0,0],phases=pg)
    U=np.kron(np.eye(4),np.diag(np.exp(1j*theta)))
    cov=float(np.max(abs(dg-U.conj().T@dr@U)));assert cov<1e-10
    timecorner,*_=overlap([0,0,0],np.pi)
    assert min(svdvals(timecorner))>1e-3
    norm=1.01*max(abs(ev));wall=[]
    for n in (16,64,256,1024):
        epsilon=np.tanh(n*np.arctanh(ev/norm))
        wall.append(dict(wall_layers=n,sign_error_max=float(max(abs(epsilon-np.sign(ev)))),
                         GW_spectral_defect=float(max(abs(1-epsilon**2))),
                         gap_bound=float(2*np.exp(-2*n*np.arctanh(min(abs(ev))/norm)))))
    return dict(status='PASS',kernel_bands=320,origin=origin,origin_massless_spinors=4,
        Euclidean_kernel='DW=i gamma4 sin(omega)+i sum_i gamma_i K_i(k)+r L(k)+rt(1-cos omega)-m0; Q=gamma5 DW; Dov=I+gamma5 sign(Q). r10,rt1,m0.5.',
        exact_relation='D gamma5+gamma5 D=D gamma5 D, whenever Q is gapped. hat_gamma5=gamma5(I-D)=-sign Q squares toI; modified chiral projectors are defined exactly.',
        low_momentum_checks=rows,static_random_gauge=random,gauge_covariance_max=cov,
        static_pairing='At omega0 orpi, R=i gamma4 gamma5 anticommutes with Q for EVERY static link phase. Hence signQ trace and overlap index are0 when gapped. At general omega, R Q(k,omega) R=-Q(k,-omega), so time-reflected free/static sectors also pair. This is a new kernel application of the prior paired-spectrum obstruction, not an all4D-topology no-go.',
        finite_domain_wall=wall,
        scope='Exact GW construction with demonstrated native low Dirac modes and approximate finite-wall error, on supplied Euclidean-time extension. Free/static gauge index0; no topological charge3, anomaly-free chiral gauge measure, three-family count, uniform gap for all fields, interacting continuum or locality proof for signQ.',
        prior=['11970 native harmonic Wilson kernel','TOE41 different graph-only overlap pairing','11423-11427 and11582 external4D overlap index controls'],
        primary='https://arxiv.org/abs/hep-lat/9801031')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11977_native_overlap.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS',d['origin'],d['gauge_covariance_max'],d['finite_domain_wall'][-1])
