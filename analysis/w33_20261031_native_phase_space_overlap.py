"""A finite Pauli-phase-space Wilson kernel with a certified nonzero index.

Uses the new two-qubit Clifford axes and native two-qutrit X/Z translations.
It changes the paired incidence kernel. No external spatial torus is added,
but interpreting internal phase space as spacetime is NOT justified here.
"""
import json,pathlib,math
import numpy as np
import sympy as s
from scipy.linalg import expm
ROOT=pathlib.Path(__file__).resolve().parents[1]

def operators():
    d=json.loads((ROOT/'data/w33_20261031_unitary_stabilizer_lift.json').read_text())
    axes=[s.Matrix([[s.sympify(x)for x in row]for row in M])for M in d['gamma_axes']]
    gammas=axes[:4];chirality=gammas[0]*gammas[1]*gammas[2]*gammas[3]
    X=s.Matrix([[0,0,1],[1,0,0],[0,1,0]])
    w=(-1+s.I*s.sqrt(3))/2;Z=s.diag(1,w,s.conjugate(w));I=s.eye(3)
    translations=[s.kronecker_product(X,I),s.kronecker_product(Z,I),s.kronecker_product(I,X),s.kronecker_product(I,Z)]
    return gammas,chirality,translations

def kernel(gammas,chirality,T,mass):
    n=T[0].shape[0];D=(4-mass)*np.eye(4*n,dtype=complex)
    for G,U in zip(gammas,T):D-=(np.kron(np.eye(4)-G,U)+np.kron(np.eye(4)+G,U.conj().T))/2
    Gamma=np.kron(chirality,np.eye(n));H=Gamma@D
    assert np.max(abs(H-H.conj().T))<1e-12
    return H,Gamma

def overlap(H,Gamma):
    ev,V=np.linalg.eigh(H);gap=float(min(abs(ev)));assert gap>1e-9
    sign=(V*np.sign(ev))@V.conj().T;D=np.eye(len(H))+Gamma@sign
    index=int(round(-np.sign(ev).sum()/2));zero=np.linalg.eigh(D.conj().T@D)
    modes=zero[1][:,zero[0]<1e-10];charges=np.linalg.eigvalsh(modes.conj().T@Gamma@modes)
    assert round(charges.sum())==index
    return dict(index=index,Wilson_gap=gap,zero_modes=modes.shape[1],zero_mode_chiralities=charges.tolist(),
        GW_defect=float(np.linalg.norm(Gamma@D+D@Gamma-D@Gamma@D,2)))

def exact_inertia(mass):
    g,c,T=operators()
    D=(4-mass)*s.eye(36)
    for G,U in zip(g,T):D-=(s.kronecker_product(s.eye(4)-G,U)+s.kronecker_product(s.eye(4)+G,U.conjugate().T))/2
    H=s.kronecker_product(c,s.eye(9))*D
    real=H.applyfunc(lambda x:s.expand(s.re(x)));imag=H.applyfunc(lambda x:s.expand(s.im(x)))
    M=real.row_join(-imag).col_join(imag.row_join(real))
    A=M.applyfunc(lambda x:s.expand(x).coeff(s.sqrt(3),0));B=M.applyfunc(lambda x:s.expand(x).coeff(s.sqrt(3)))
    assert A+s.sqrt(3)*B==M
    denominator=int(s.ilcm(*[s.denom(x)for x in list(A)+list(B)]))
    A=np.array(A*denominator,dtype=np.int64);B=np.array(B*denominator,dtype=np.int64)
    _,V=np.linalg.eigh((A+math.sqrt(3)*B)/denominator)
    Q=np.rint(V*10**6).astype(np.int64)
    return dict(denominator=denominator,A=A.tolist(),B=B.tolist(),rational_congruence_numerators=Q.tolist(),
        sqrt3_interval_denominator=10**16,sqrt3_lower_numerator=17320508075688772,
        sqrt3_upper_numerator=17320508075688773)

def verify_inertia(cert):
    """Only integer arithmetic: no eigensolver or square-root evaluation."""
    A=np.array(cert['A'],dtype=object);B=np.array(cert['B'],dtype=object);Q=np.array(cert['rational_congruence_numerators'],dtype=object)
    assert np.array_equal(A.T,A)and np.array_equal(B.T,B)
    D=cert['sqrt3_interval_denominator'];lo=cert['sqrt3_lower_numerator'];hi=cert['sqrt3_upper_numerator']
    assert lo*lo<3*D*D<hi*hi
    gram=Q.T@Q
    # Exact strict diagonal dominance makes Q invertible, so congruence
    # preserves inertia. Gershgorin excludes zero throughout the sqrt interval.
    assert all(int(gram[i,i])>sum(abs(int(gram[i,j]))for j in range(len(Q))if j!=i)for i in range(len(Q)))
    normQ2=max(sum(abs(int(v))for v in row)for row in gram)
    C=Q.T@A@Q;E=Q.T@B@Q;positive=negative=0;margins=[]
    for i in range(len(Q)):
        ends=[int(C[i,i])*D+int(E[i,i])*z for z in (lo,hi)]
        radius=sum(max(abs(int(C[i,j])*D+int(E[i,j])*z)for z in (lo,hi))for j in range(len(Q))if j!=i)
        if min(ends)>radius:positive+=1;margins.append(min(ends)-radius)
        else:
            assert max(ends)<-radius
            negative+=1;margins.append(-max(ends)-radius)
    assert positive%2==negative%2==0
    gap=s.Rational(min(margins),cert['denominator']*D*normQ2)
    return dict(positive_complex_eigenvalues=positive//2,negative_complex_eigenvalues=negative//2,
        index=(negative-positive)//4,rigorous_gap_lower_bound=str(gap),gap_lower_decimal=float(gap),
        method='Exact rational congruence and signed Gershgorin discs for the 72D realification; sqrt3 lies in a rational interval. No floating-point eigensolver is used to verify this certificate.')

def build():
    gs,c,ts=operators();g=[np.array(G,dtype=complex)for G in gs];c=np.array(c,dtype=complex);T=[np.array(U,dtype=complex)for U in ts]
    certificates=[];rows=[]
    for numerator in (7,9):
        mass=s.Rational(numerator,5);cert=exact_inertia(mass);proved=verify_inertia(cert)
        H,Gamma=kernel(g,c,T,float(mass));row=overlap(H,Gamma)
        assert row['index']==proved['index']and proved['gap_lower_decimal']>.1
        certificates.append(dict(mass=str(mass),certificate=cert,verified=proved));rows.append(dict(mass=str(mass),**row))
    H,Gamma=kernel(g,c,T,1.8);controls={}
    rev=T.copy();rev[1]=rev[1].conj().T
    controls['reverse_one_flux_plane']=overlap(kernel(g,c,rev,1.8)[0],Gamma)
    controls['commuting_translations']=overlap(kernel(g,c,[np.eye(9)]*4,1.8)[0],Gamma)
    assert controls['reverse_one_flux_plane']['index']==-rows[-1]['index']and controls['commuting_translations']['index']==0
    rng=np.random.default_rng(20261031);K=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9));K=(K+K.conj().T)/2;U=expm(.001j*K)
    changed=T.copy();changed[0]=U@changed[0];H2,_=kernel(g,c,changed,1.8)
    controls['small_link_perturbation']={**overlap(H2,Gamma),'kernel_norm_change':float(np.linalg.norm(H2-H,2))}
    assert controls['small_link_perturbation']['kernel_norm_change']<certificates[-1]['verified']['gap_lower_decimal']
    assert controls['small_link_perturbation']['index']==rows[-1]['index']
    return dict(status='PASS_NATIVE_FINITE_PHASE_SPACE_NONZERO_INDEX',carrier='C^4 spinor (actual new two-qubit Clifford axes) tensor C^9 native two-qutrit Pauli register',
        dimension=36,mass_samples=rows,exact_inertia_certificates=certificates,controls=controls,
        stability='For Hermitian delta H with ||delta H|| less than the certified gap, Weyl continuity keeps the inertia and overlap index unchanged. At mass9/5 the certified lower gap exceeds0.1.',
        locality='Wilson hopping uses actual qutrit shifts and diagonal clocks. The sign kernel need not be sparse. For a uniformly gapped bounded-range family, the binomial series for H/sqrt(H^2) gives polynomial approximants and exponential graph-distance bounds; such a physical refinement family is not constructed here.',
        prior='TOE41 and the preceding packet exclude the balanced f(MM*) pairing family. Pass11592 and12015 already own external-torus nonzero-index controls; finite noncommutative overlap indices are established literature. This construction instead uses the native 9D Pauli phase-space carrier and the new exact 4D spinor carrier.',
        literature=['https://doi.org/10.1103/PhysRevD.67.085005','https://arxiv.org/abs/hep-th/0602078','https://arxiv.org/abs/0810.5234'],
        boundary='The Wilson form, four phase-space directions and mass are supplied. No external spatial lattice is used, but internal phase space is not derived spacetime. Different masses here even give opposite indices: no unique generation count, continuum chirality, anomaly-free measure, E6-invariant interaction or TOE follows.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261031_native_phase_space_overlap.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['mass_samples'])
