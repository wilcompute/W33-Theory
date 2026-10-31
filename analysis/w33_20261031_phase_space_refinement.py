"""Distinguish fundamental and full-matrix Pauli refinement modules.

The adjoint module has an exact flat4D Fourier Wilson refinement with zero
index. Fundamental charged indices have a numerical resolution gate. Neither
is a derived physical spacetime or a completed chiral gauge measure.
"""
import pathlib,sys,json,itertools,math,time
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261031_native_phase_space_overlap import operators,kernel

def translations(N,charge=1):
    X=np.roll(np.eye(N),1,axis=0).astype(complex);Z=np.diag(np.exp(2j*np.pi*charge*np.arange(N)/N));I=np.eye(N)
    return [np.kron(X,I),np.kron(Z,I),np.kron(I,X),np.kron(I,Z)]

def fundamental_index(N,charge,mass,gammas,chirality):
    H,_=kernel(gammas,chirality,translations(N,charge),mass);e=np.linalg.eigvalsh(H)
    assert min(abs(e))>1e-8
    return dict(N=N,charge=charge,mass=mass,dimension=len(H),numerical_index=int(round(-np.sign(e).sum()/2)),numerical_gap=float(min(abs(e))))

def flat_symbol(p,mass=1.):
    p=np.asarray(p,dtype=float);W=np.sum(1-np.cos(p));sin2=float(np.sum(np.sin(p)**2));radius=math.sqrt((W-mass)**2+sin2)
    return W,sin2,radius

def build():
    gs,c,_=operators();g=[np.array(G,dtype=complex)for G in gs];c=np.array(c,dtype=complex)
    family=[fundamental_index(N,1,1.4,g,c)for N in (3,5,7,11,15)]
    charged=[]
    for N in (15,23):
        rows=[fundamental_index(N,q,1.4,g,c)for q in (1,-2,4)]
        value=sum(n*r['charge']*r['numerical_index']for n,r in zip((16,10,1),rows))
        charged.append(dict(N=N,rows=rows,weighted_index_sum=value,expected_continuum_indices=[-1,-4,-16],
            expected_cubic_charge_sum=16-80+64))
        print('CHARGED',N,value,[(r['charge'],r['numerical_index'])for r in rows],flush=True)
    assert charged[0]['weighted_index_sum']==60 and charged[1]['weighted_index_sum']==0
    T=translations(3);adjoint=[np.kron(U.conj(),U)for U in T]
    assert all(np.linalg.norm(A@B-B@A)<1e-12 for A,B in itertools.combinations(adjoint,2))
    H,Gamma=kernel(g,c,adjoint,1.);ev=np.linalg.eigvalsh(H)
    expected=[]
    for labels in itertools.product(range(3),repeat=4):
        W,sin2,r=flat_symbol(2*np.pi*np.array(labels)/3)
        expected.extend([-r,-r,r,r])
    assert np.max(abs(ev-sorted(expected)))<1e-12 and round(-np.sign(ev).sum()/2)==0
    # The exact identity at m=1 is H(p)^2=1+2 sum_(mu<nu)u_mu u_nu,
    # u_mu=1-cos(p_mu) in[0,2], giving 1<=H^2<=49 at every N.
    for labels in itertools.product(range(3),repeat=4):
        p=2*np.pi*np.array(labels)/3;u=1-np.cos(p);W,sin2,r=flat_symbol(p)
        assert abs(r*r-(1+2*sum(u[i]*u[j]for i,j in itertools.combinations(range(4),2))))<1e-12
    # Numerical positive control for the exact small-momentum expansion.
    k=np.array([.2,-.1,.3,.15]);rows=[]
    for N in (31,63,127,255):
        a=2*np.pi/N;p=a*k;W,sin2,r=flat_symbol(p)
        scalar=(1+(W-1)/r)/a;vector=np.sin(p)/(a*r)
        error=math.sqrt(float(scalar*scalar+np.sum((vector-k)**2)))
        rows.append(dict(N=N,lattice_spacing=a,continuum_symbol_error=error))
    assert all(rows[i+1]['continuum_symbol_error']<rows[i]['continuum_symbol_error']for i in range(len(rows)-1))
    return dict(status='PASS_REFINEMENT_MODULE_DISTINCTION_AND_CHARGED_RESOLUTION_GATE',
        fundamental_refinement_samples=family,charged_index_resolution=charged,
        charged_scope='Numerical Hermitian spectral signatures, not interval certificates. The16_1+10_-2+1_4 ledger tests the necessary weighted-index sum, not a local anomaly-free measure. At N15 charge4 is in a wrong finite-resolution phase, so cancellation fails; at N23 the expected index ledger cancels. Physical charge assignments and a common chiral measure remain inputs.',
        exact_adjoint_result='On Mat_(N^2), Ad(T_mu) commute because the fundamental commutators are central. The N^4 Pauli monomials diagonalize them with every Fourier momentum in(Z/N)^4 once. Each Wilson block has paired eigenvalues +/-sqrt(sum sin^2 p+(sum(1-cos p)-m)^2), each twice. Hence its index is exactly0 at every noncritical mass for every N.',
        adjoint_N3_control=dict(dimension=len(H),index=0,gap=float(min(abs(ev))),maximum_symbol_spectrum_error=float(np.max(abs(ev-sorted(expected))))),
        exact_uniform_gap='At m=1, H(p)^2=1+2 sum_(mu<nu)(1-cos p_mu)(1-cos p_nu), so1<=H^2<=49 at every N.',
        locality='With ||H||<=7 and gap>=1, sign H=(H/7) sum_k c_k (I-H^2/49)^k, c_k=binom(2k,k)/4^k<=1. Truncating at K has operator error<=49*(48/49)^(K+1). In the Fourier-dual position basis the polynomial has range<=2K+1, giving a uniform exponential distance bound.',
        continuum='For p=a k at m=1, Dov(p)/a -> i sum gamma_mu k_mu, with O(a) scalar Wilson correction. This is a flat Euclidean4D free-Dirac refinement on a supplied operator module/Fourier interpretation, not derived Lorentzian space.',
        continuum_symbol_controls=rows,
        prior='The preceding36D fundamental kernel owns its exact N3 index certificates. Pass5709 owns central-flux invisibility in an adjoint representation; October19 owns the native80-character Pauli module. Pass11592 already shows charge-dependent Wilson resolution on external tori. Here the two refinement modules are compared explicitly and the same finite phase-space charged ledger is replayed.',
        literature=['https://arxiv.org/abs/hep-lat/9808010','https://arxiv.org/abs/0810.5234','https://arxiv.org/abs/hep-lat/9811032'],
        boundary='Fundamental and full-matrix carriers differ (N^2 versus N^4). Their indices cannot be identified. Finite nonzero index and a flat adjoint continuum control do not combine into a derived chiral4D universe. No local anomaly primitive, non-Abelian measure, dynamical geometry or physical generation prediction constructed.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261031_phase_space_refinement.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'])
