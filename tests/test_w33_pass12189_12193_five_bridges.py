"""Independent native-map, noise, E6 and spectral controls for five bridges."""
import hashlib
import json
from itertools import product
from pathlib import Path
import numpy as np
import pytest
import sympy as s
from sympy.matrices.normalforms import hermite_normal_form
from analysis import w33_pass12189_12193_five_bridges as p
ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def cert():
    return json.loads((ROOT/'data/w33_pass12189_12193_five_bridges.json').read_text())


def test_frozen_provenance(cert):
    assert cert['source_sha256']==hashlib.sha256(Path(p.__file__).read_bytes()).hexdigest()
    for name,digest in cert['input_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest


def test_exact_heralded_norms_and_full_rank(cert):
    z=s.Symbol('z');phi=z**6+z**3+1;norms=[]
    for counts in cert['magic']['phase_counts_mod9']:
        f=sum(s.Rational(n,59049)*z**j for j,n in enumerate(counts))
        fc=sum(s.Rational(n,59049)*z**((-j)%9)for j,n in enumerate(counts))
        norms.append(s.rem(s.expand(f*fc),phi,z))
    assert norms==[1,s.Rational(1,27),s.Rational(1,27)]
    assert sum(norms)/3==s.Rational(29,81)
    assert cert['magic']['kraus_rank_on_declared_logical_qutrit']==3


def test_magic_is_not_one_of_twelve_qutrit_stabilizers(cert):
    z=np.exp(2j*np.pi/9)
    amplitudes=np.array([sum(n*z**j for j,n in enumerate(c))/59049 for c in cert['magic']['phase_counts_mod9']])
    psi=amplitudes/np.linalg.norm(amplitudes)
    stabilizers=list(np.eye(3,dtype=complex))
    omega=z**3
    for a,b in product(range(3),repeat=2):
        stabilizers.append(np.array([omega**(a*t*t+b*t)for t in range(3)])/np.sqrt(3))
    assert max(abs(np.vdot(v,psi))**2 for v in stabilizers)<.99
    assert min(cert['magic']['wigner_q_then_p'])<-.1
    assert np.isclose(sum(cert['magic']['wigner_q_then_p']),1)


def test_single_fault_is_accepted_and_not_corrected(cert):
    noisy=cert['magic']['single_Z_after_gate_controls']
    assert len(noisy)==40
    accepted=[r for r in noisy if r['success']>1e-8]
    assert accepted
    assert all(np.isclose(r['success'],2/81)for r in accepted)
    assert all(r['fidelity_to_ideal']<.1 for r in accepted)


def test_discriminant_covariance_on_actual_three_level_operators(cert):
    omega=np.exp(2j*np.pi/3);X=np.roll(np.eye(3),1,axis=0);Z=np.diag(omega**np.arange(3))
    for rec in cert['discriminant']['actions']:
        U=np.diag(omega**np.array(rec['Weil_diagonal_exponents']));A=np.array(rec['matrix2_mod3'])
        assert round(np.linalg.det(A))%3==1
        for a,b in product(range(3),repeat=2):
            c,d=A@np.array([a,b])%3
            D=omega**(a*b)*np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,(-b)%3)
            target=omega**(c*d)*np.linalg.matrix_power(X,int(c))@np.linalg.matrix_power(Z,int(-d)%3)
            assert np.allclose(U@D@U.conj().T,target,atol=1e-13)
    assert cert['discriminant']['image_order']==3
    assert len(cert['discriminant']['kernel'])==9


def test_discriminant_uses_dual_action_negative_control():
    _,R=p.native.native();F=p.native.alternating([-3,-1,-2,2,1,0]);u=s.Matrix([1,0,0,0])
    M=R[(1,0,0)]
    assert any(x.q!=1 for x in F.inv()*(M*u-M.inv().T*u))


def test_complete_normalizer_candidates_and_lattice_bases(cert):
    P,S,groups=p.native_normalizers()
    assert abs(P.det())==3 and abs((S.inv()*P).det())==1
    assert [len(g)for g in groups]==[144,288]
    for g in groups:
        keys={tuple(M)for M in g}
        # Closure from generators is stronger than counting candidate orders.
        seen={tuple(s.eye(4))};todo=[s.eye(4)]
        generators=[]
        for M in g:
            if tuple(M)in seen:continue
            generators.append(M);seen={tuple(s.eye(4))};todo=[s.eye(4)]
            while todo:
                A=todo.pop()
                for B in generators:
                    C=A*B;k=tuple(C)
                    assert k in keys
                    if k not in seen:seen.add(k);todo.append(C)
            if len(seen)==len(g):break
        assert seen==keys


def test_binary_ternary_action_mismatch(cert):
    for g in cert['normalizer']['groups']:
        assert g['binary_matrix_image_order']==72
        assert g['binary_kernel_orbits']==[[0,1,2,3,4,5]]
        assert g['ternary_polarity_orbits']==[[0,3],[1,2,4,5]]
        for perm in g['binary_permutations']+g['ternary_permutations']:
            assert sorted(perm)==list(range(6))


def test_integral_polarity_exchange_has_actual_antiunitary_lift(cert):
    rec=cert['yukawa']['polarity_exchange'];K=np.array(rec['original_matrix']);Kr=s.Matrix(rec['repaired_matrix'])
    F0=p.native.alternating([-3,-1,-2,2,1,0]);F1=p.native.alternating([-3,-1,-2,2,1,-2])
    assert s.Matrix(K).T*F0*s.Matrix(K)==F1
    assert Kr*Kr==s.eye(4) and Kr.det()==-1
    w=np.exp(2j*np.pi/3);X=np.roll(np.eye(3),1,axis=0);Z=np.diag(w**np.arange(3));U=Z@Z
    la=np.array([0,0,-w.conjugate(),1]);lb=np.array([-1-2*w,2+w,-w,1])
    def Y(x):
        a,b=la@x,lb@x
        return a*X+a.conjugate()*X.T+b*Z+b.conjugate()*Z.conj()
    rng=np.random.default_rng(12193)
    for _ in range(20):
        x=rng.normal(size=4);A=Y(x);B=Y(K@x)
        assert np.allclose(B,U@A.conj()@U.conj().T)
        assert np.allclose(np.linalg.eigvalsh(A),np.linalg.eigvalsh(B))
        assert np.allclose(np.linalg.det(A),np.linalg.det(B))
    for a,b,c in product(range(3),repeat=3):
        W=w**c*np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,(-b)%3)
        target=w**((-c+2*a)%3)*np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b)
        assert np.allclose(U@W.conj()@U.conj().T,target)


def test_native_yukawa_intertwiner_and_cubic_equivariance():
    _,R=p.native.native();w=np.exp(2j*np.pi/3)
    la=np.array([0,0,-w.conjugate(),1]);lb=np.array([-1-2*w,2+w,-w,1])
    X=np.roll(np.eye(3),1,axis=0);Z=np.diag(w**np.arange(3));rng=np.random.default_rng(12191)
    def Y(x):
        a,b=la@x,lb@x
        return a*X+a.conjugate()*X.T+b*Z+b.conjugate()*Z.conj()
    def cubic(A,B,C):return np.linalg.det(A)+np.linalg.det(B)+np.linalg.det(C)-np.trace(A@B@C)
    A,B,C=[rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))for _ in range(3)]
    for (a,b,c),M in R.items():
        W=w**c*np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,(-b)%3);x=rng.normal(size=4)
        assert np.allclose(Y(np.array(M,dtype=float)@x),W@Y(x)@W.conj().T)
        assert np.allclose(cubic(W@A@W.conj().T,W@B,C@W.conj().T),cubic(A,B,C))


def test_radial_F_D_terms_and_soft_cubic_pair_degeneracy():
    rng=np.random.default_rng(12191);w=np.exp(2j*np.pi/3);X=np.roll(np.eye(3),1,axis=0);Z=np.diag(w**np.arange(3))
    for _ in range(20):
        a,b=rng.normal(size=2)+1j*rng.normal(size=2);Y=a*X+a.conjugate()*X.T+b*Z+b.conjugate()*Z.conj()
        t=np.trace(Y@Y).real
        adj=Y@Y-t/2*np.eye(3)
        assert np.allclose(np.trace(adj.conj().T@adj),t*t/4)
        assert np.allclose(np.trace(Y@Y@Y@Y)-t*t/3,t*t/6)
        assert abs(np.linalg.det(Y))<=2*(abs(a)**2+abs(b)**2)**1.5+1e-10
    Y=X+X.T
    assert np.allclose(np.linalg.svd(Y,compute_uv=False),[2,1,1])
    # Direct mixed derivatives of -Tr(A B C) in the declared k-grouped basis.
    mixed=np.empty((9,9),complex)
    for k,j in product(range(3),repeat=2):
        B=np.zeros((3,3));B[j,k]=1
        for ell,i in product(range(3),repeat=2):
            C=np.zeros((3,3));C[ell,i]=1
            mixed[3*k+j,3*ell+i]=-np.trace(Y@B@C)
    assert np.allclose(mixed,-np.kron(np.eye(3),Y.T))
    assert np.allclose(np.linalg.svd(mixed,compute_uv=False),[2,2,2,1,1,1,1,1,1])


def test_native_period_primitivity_and_optical_gap():
    _,B,V,G,aa,bb=p.graph_inputs()
    assert hermite_normal_form(s.Matrix(V.astype(int)).T)==s.eye(4)
    eig=np.linalg.eigvalsh(B.T@B)
    assert abs(eig[0])<1e-12 and eig[1]>6.9
    # An independent incidence assembly checks the Bloch orientation/signs.
    k=np.array([.17,-.21,.08,.14]);D=B.astype(complex).copy()
    D[np.arange(135),bb]=np.exp(1j*(V@k))
    L=D.conj().T@D
    assert np.linalg.eigvalsh(L)[0]>0
    assert np.allclose(L,L.conj().T)


def test_nonlinear_density_and_native_refinement(cert):
    rows=cert['continuum']['Bloch_controls']
    assert [r['N']for r in rows]==[8,16,32,64]
    assert all(r['tested_nonzero_modes']==624 for r in rows)
    assert rows[-1]['max_relative_dispersion_error']<.0071
    for r in cert['continuum']['nonlinear_controls']:
        K=np.array(r['conductivity']);g=np.array(r['metric']);rho=r['capacity_density']
        assert np.allclose(rho*np.linalg.inv(g),K)
        assert np.allclose(np.linalg.det(g),rho*rho)
        assert r['internal_gauge_error']<1e-12
        assert r['Hessian_fd_error']<1e-8


def test_complete_regeneration_matches_certificate(cert):
    actual=p.build()
    def equal(a,b,path=()):
        if isinstance(a,dict):
            assert a.keys()==b.keys()
            for k in a:equal(a[k],b[k],path+(k,))
        elif isinstance(a,list):
            assert len(a)==len(b)
            for x,y in zip(a,b):equal(x,y,path)
        elif path and path[-1]=='Hessian_fd_error':assert a<1e-8 and b<1e-8
        elif isinstance(a,float):assert np.isclose(a,b,rtol=1e-10,atol=2e-12),path
        else:assert a==b
    equal(actual,cert)
