"""Local hybrid T4 x native80fiber Wilson regulator with optical decoupling.

Nonzero topology comes from the supplied T4 flux, not from the W33 fiber.
No native4D manifold or chiral Standard Model is claimed.
"""
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh
from w33_20261014_toe68_overlap_control import GAMMA,G5
from w33_pass1081_1086_core import build_w33
from w33_pass11980_heisenberg_fixed_holonomies import DIRECTIONS
from w33_20261015_toe82_native_H27_h1_character import mul

ROOT=Path(__file__).resolve().parents[1]


def su5_chiral_anomaly():
    fundamental=[]
    for a,b in itertools.combinations(range(5),2):
        x=np.zeros((5,5),complex);x[a,b]=x[b,a]=.5;fundamental.append(x)
        x=np.zeros((5,5),complex);x[a,b]=-.5j;x[b,a]=.5j;fundamental.append(x)
    for k in range(1,5):
        diag=np.r_[np.ones(k),-k,np.zeros(4-k)]/np.sqrt(2*k*(k+1))
        fundamental.append(np.diag(diag))
    wedge=np.zeros((25,10))
    for c,(a,b) in enumerate(itertools.combinations(range(5),2)):
        wedge[5*a+b,c]=1/np.sqrt(2);wedge[5*b+a,c]=-1/np.sqrt(2)
    generators=[]
    for t in fundamental:
        ten=wedge.T@(np.kron(t,np.eye(5))+np.kron(np.eye(5),t))@wedge
        matrix=np.zeros((15,15),complex);matrix[:10,:10]=ten;matrix[10:,10:]=-t.conj();generators.append(matrix)
    generators=np.array(generators)
    triple=np.einsum('aij,bjk,cki->abc',generators,generators,generators,optimize=True)
    anomaly=triple+triple.swapaxes(1,2)
    maximum=float(np.max(abs(anomaly)));assert maximum<1e-13
    H=np.diag([1,-1,0,0,0]);ten=wedge.T@(np.kron(H,np.eye(5))+np.kron(np.eye(5),H))@wedge
    charges=np.r_[np.rint(np.diag(ten)).astype(int),-np.diag(H)]
    assert Counter(charges)==Counter({-1:4,0:7,1:4})
    return dict(representation='Standard chiral SU5 10 + conjugate5; an explicit additional matter choice, not selected by W33.',
                generators=24,all_ordered_cubic_anomaly_entries_checked=24**3,
                max_Tr_Ta_anticommutator_Tb_Tc=maximum,
                selected_Cartan_charge_histogram={str(k):int(v) for k,v in sorted(Counter(charges).items())},
                selected_background_total_Weyl_overlap_index=8,
                chiral_boundary='The fullSU5 representation is chiral and perturbatively anomalyfree; its selectedU1 restriction is vectorlike. GW Weyl projectors are defined by the kernel. A global non-Abelian Weyl measure, interacting gauge dynamics, vacuum selection and threefamilies are not built.')


def torus_kernel(m,n,mass=1.):
    sites=list(itertools.product(range(3),repeat=4));sid={x:i for i,x in enumerate(sites)}
    links=np.ones((81,4),complex)
    for j,x in enumerate(sites):
        for a,b,q in ((0,1,m),(2,3,n)):
            links[j,a]=np.exp(-2j*np.pi*q*x[b]/9)
            if x[b]==2:links[j,b]=np.exp(2j*np.pi*q*x[a]/3)
    Q=np.kron(np.eye(81),(4-mass)*G5).astype(complex)
    for k,x in enumerate(sites):
        for a in range(4):
            y=list(x);y[a]=(y[a]+1)%3;j=sid[tuple(y)]
            block=-.5*G5@(np.eye(4)-GAMMA[a])*links[k,a]
            Q[4*k:4*k+4,4*j:4*j+4]+=block
            Q[4*j:4*j+4,4*k:4*k+4]+=block.conj().T
    assert np.max(abs(Q-Q.conj().T))<1e-12
    return Q


def payload():
    pts,_,lines,*_=build_w33();inc=np.array([[int(v in line) for line in lines] for v in range(40)])
    Lap=np.block([[4*np.eye(40),-inc],[-inc.T,4*np.eye(40)]])
    lam,U=np.linalg.eigh(Lap);assert abs(lam[0])<1e-12 and lam[1]>1.55
    G=np.kron(np.eye(81),G5);Q=torus_kernel(1,1)
    multiplicities=[(0.,1),(4-np.sqrt(6),24),(4.,30),(4+np.sqrt(6),24),(8.,1)]
    sectors=[];index=0
    for shift,mult in multiplicities:
        ev=eigvalsh(Q+shift*G)
        idx=int(round(-sum(np.sign(ev))/2));index+=mult*idx
        assert min(abs(ev))>1e-6
        sectors.append(dict(native_L_eigenvalue=shift,multiplicity=mult,index_per_sector=idx,gap=float(min(abs(ev)))))
    assert index==1 and all(s['index_per_sector']==0 for s in sectors[1:])
    rng=np.random.default_rng(11984);z=rng.normal(size=(80,324))+1j*rng.normal(size=(80,324))
    local=z@Q.T+Lap@z@G.T
    spectral=U@((U.T@z)@Q.T+lam[:,None]*(U.T@z)@G.T)
    error=float(np.max(abs(local-spectral)));assert error<1e-10
    # Primitive E6 root charges on the prior27 minuscule address carrier.
    H=list(itertools.product(range(3),repeat=3));hi={h:i for i,h in enumerate(H)}
    F={tuple(sorted(hi[mul(g,t)] for t in ((0,0,0),d,mul(d,d)))) for g in H for d in DIRECTIONS}
    A=np.zeros((27,27),dtype=int)
    for f in F:
        for a,b in itertools.combinations(f,2):A[a,b]=A[b,a]=1
    P=3*np.eye(27,dtype=int)-3*A+np.ones((27,27),dtype=int)
    a,b=next((a,b) for a,b in itertools.combinations(range(27),2) if not A[a,b])
    numerator=P[:,a]-P[:,b];assert not (numerator%3).any();charges=numerator//3
    assert Counter(charges)==Counter({-1:6,0:15,1:6})
    assert sum(charges)==sum(charges**3)==sum(charges**5)==0
    # Actual charge-conjugate flux signatures, not large-charge aliasing.
    evminus=eigvalsh(torus_kernel(-1,-1));iminus=int(round(-sum(np.sign(evminus))/2));assert iminus==1
    return dict(status='PASS',full_hybrid_spinor_dimension=80*324,
        actual_local_kernel='Q_total=I80 tensor Q_T4 + L_W33_Levi tensor gamma5. Optical Laplacian mass coefficient1. Equivalently DW_total=I tensor DW_T4+L tensor I.',
        locality='Nearest-neighbor T4 spacetime edges plus actual160 native internal Levi links, onsite otherwise. This is a hybrid product with an externally supplied4D base.',
        native_optical_sectors=sectors,total_charge1_overlap_index=index,local_spectral_tensor_action_error=error,
        exact_optical_gap_bound='For lambda>0, Re DW_total >= lambda-m0 >0 since lambda_min_positive=4-sqrt6>1=m0. Thus optical blocks stay gapped through kinetic-to-zero homotopy and have zero index.',
        primitive_E6_root_charge_histogram={str(k):int(v) for k,v in sorted(Counter(charges).items())},
        mixed_gravity_anomaly=int(sum(charges)),cubic_U1_anomaly=int(sum(charges**3)),charge_minus1_index=iminus,
        charged_index_multiplicities={'q=-1':6,'q=+1':6},
        explicit_chiral_SU5_extension=su5_chiral_anomaly(),
        scope='Nonzero hybrid probe index and selectedU1 anomaly cancellation, with native optical decoupling. The chargedU1 content is vectorlike, not chiralSM. No fullE6 anomaly-free lattice measure or threefamilies. CoarseT4 plaquettes violate a standard sufficient overlap-locality bound; no uniform locality theorem or native4D continuum is inferred.',
        prior=['TOE68 conventionalT4 indexpositivecontrol','TOE69 largecharge aliasing correction','11970/11977 different nativecover Dirac/overlap kernel','TOE80 E6 minuscule weights'],
        primary='https://arxiv.org/abs/hep-lat/9801031')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11984_native_fiber_overlap.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['total_charge1_overlap_index'],d['primitive_E6_root_charge_histogram'])
