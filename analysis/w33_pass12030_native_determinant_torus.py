"""Multi-patch finite chiral determinant topology on a toron/flux family.

Fukui-Hatsugai-Suzuki determinant links are standard; integer mesh output is
not automatically the continuum Chern number. Underresolved controls retained.
"""
import sys,numpy as np,itertools,time
from pathlib import Path
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass12000_native_unitary_clock import native_paths
from w33_pass11991_native_four_period_cover import gamma4

def magnetic(L,charge):
 cells=list(itertools.product(range(L),repeat=2));index={c:i for i,c in enumerate(cells)};n=L*L;B=2*np.pi*charge/n;S=[]
 for mu in range(2):
  A=np.zeros((n,n),complex)
  for i,(x,y) in enumerate(cells):
   d=[x,y];d[mu]=(d[mu]+1)%L;j=index[tuple(d)];phase=np.exp(-1j*B*y) if mu==0 else (np.exp(1j*B*L*x) if y==L-1 else 1)
   A[i,j]=phase
  S.append(A)
 return S

@lru_cache(None)
def chern(L,charge,N,native=False):
 gamma,g5=gamma4();n=L*L;offset=np.zeros(4)
 if native:offset=np.angle(native_compile(L)[0][0,0,:]) * charge
 Id=np.eye(4*n);G=np.kron(g5,np.eye(n));S=magnetic(L,charge)
 if native:S=[np.exp(1j*offset[mu+2])*z for mu,z in enumerate(S)]
 base=3*Id.astype(complex)
 for g,a in zip(gamma[2:],S):base-=.5*(np.kron(np.eye(4)-g,a)+np.kron(np.eye(4)+g,a.conj().T))
 frames={};gap=1e9;minsv=1.;start=time.time()
 for i,j in itertools.product(range(N),repeat=2):
  x,y=2*np.pi*np.array([i,j])/N+offset[:2];D=base-(np.cos(x)+np.cos(y))*Id+1j*(np.kron(gamma[0],np.eye(n))*np.sin(x)+np.kron(gamma[1],np.eye(n))*np.sin(y));val,V=np.linalg.eigh(G@D);gap=min(gap,min(abs(val)));frames[i,j]=V[:,val>0]
 links={}
 for i,j in itertools.product(range(N),repeat=2):
  for mu,d in enumerate([(1,0),(0,1)]):
   ov=frames[i,j].conj().T@frames[(i+d[0])%N,(j+d[1])%N];sign,ld=np.linalg.slogdet(ov);links[i,j,mu]=sign;minsv=min(minsv,np.linalg.svd(ov,compute_uv=False)[-1])
 angles=[]
 for i,j in itertools.product(range(N),repeat=2):angles.append(np.angle(links[i,j,0]*links[(i+1)%N,j,1]/links[i,(j+1)%N,0]/links[i,j,1]))
 return dict(L=L,charge=charge,N=N,Chern=sum(angles)/(2*np.pi),gap=gap,continuous_gap_bound=gap-2*np.pi/N,maxplaquette=max(abs(np.array(angles))),min_overlap=minsv,native_compiled=bool(native))


def native_compile(L=6):
    edges,V,paths,tree,T,words=native_paths();v=np.rint(V@np.linalg.inv(np.array(T,int)).T).astype(int)
    assert all(np.array_equal(sum((sign*v[e] for e,sign in word),np.zeros(4,int)),np.eye(4,dtype=int)[mu]) for mu,word in enumerate(words))
    def link(n,mu):
        if mu==0 or mu==1:return 1.+0j
        if mu==2:return np.exp(-2j*np.pi*(n[3]%L)/(L*L))
        return np.exp(2j*np.pi*(n[2]%L)/L) if n[3]%L==L-1 else 1.+0j
    def edge(n,e,sign):
        if sign<0:
            shifted=n-v[e];phase,end=edge(shifted,e,1);return phase.conjugate(),shifted
        current=n.copy();phase=1.+0j
        for mu,num in enumerate(v[e]):
            for _ in range(abs(int(num))):
                if num>0:phase*=link(current,mu);current[mu]+=1
                else:current[mu]-=1;phase*=link(current,mu).conjugate()
        return phase,current
    ratios=np.ones((L,L,4),complex)
    for x,y in itertools.product(range(L),repeat=2):
        n=np.array([0,0,x,y])
        for mu,word in enumerate(words):
            phase=1.+0j;current=n.copy()
            for e,sign in word:
                z,current=edge(current,e,sign);phase*=z
            assert np.array_equal(current,n+np.eye(4,dtype=int)[mu]);ratios[x,y,mu]=phase/link(n,mu)
    error=float(np.max(abs(ratios-ratios[0,0])));assert error<1e-11
    return ratios,error

def payload():
    charges={1:6,2:3,-3:2,-4:3,6:1};rows=[]
    for N in [8,16,24]:
        sectors=[chern(6,c,N,True) for c in charges];total=sum(charges[z['charge']]*z['charge']**2*z['Chern'] for z in sectors)
        rows.append(dict(mesh=N,sectors=sectors,physical_toron_Chern_total=float(total)))
    ratios,error=native_compile();expected=sum(m*c**3 for c,m in charges.items());assert expected==0
    assert max(abs(z['Chern']+z['charge']) for z in rows[-1]['sectors'])<1e-10
    return dict(status='PASS',charges_multiplicities=charges,meshes=rows,native_compile_constant_phase_errors=error,native_period_phase_offsets=np.angle(ratios[0,0]).tolist(),anomaly_sum_q3=expected,
        family='Four-dimensional Wilson kernel: two one-cell directions carry torons alpha,beta; a6x6 magnetic plane carries flux1. Each chargeq has fluxq. Native12000 period words are compiled in the actual unimodular clock marking; their links differ from straight magnetic links by tested constant phases. Positive-projector determinant links use arbitrary local eigenframes across the whole parameter torus, not one fixed reference frame.',
        topology='On the effective-charge torus, resolved mesh Chern=-q. Physical torons map(alpha,beta)=(q theta0,q theta1) with degreeq^2, so contribution=-multiplicity*q^3. For10+bar5 underinteger6Y this sums to zero. Standard anomaly cancellation is prior art; this is an actual finite native-path-compatible family test, not a new anomaly formula.',
        gap_control='Each toron partial derivative of the Hermitian Wilson kernel has operator norm1. A mesh minimum gap minus2pi/N is a whole-torus Lipschitz lower bound up to matrix-eigensolver rounding; positive margins are recorded. This controls gaps, not the correctness of an underresolved Chern mesh. Integer plaquette output alone and max sampled phase<pi do not certify resolution.',
        scope='Multi-patch determinant topology on one declared finite Abelian subgroup family. Stable integer mesh results and native word compilation are numerical controls; no interval-certified general family-index theorem or full nonAbelian/allvolume measure construction. Coarse-loop null Chern is necessary, not sufficient, for the global current. Added flux/periods do not derive families or select physicalconstants.',
        prior=['12025 contractible frame current','12002 coarse factor plus Kato-trivial optical lines','12015 SM10+bar5 charge embedding','prior pump scripts already useFHS','cond-mat/0503172 determinant-link method','hep-lat/9904009 anomaly/determinant geometry'])

if __name__=='__main__':
    import json
    out=payload();(ROOT/'data/w33_pass12030_native_determinant_torus.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS determinant torus',[(r['mesh'],r['physical_toron_Chern_total']) for r in out['meshes']],flush=True)
