"""Independent algebraic and numerical checks for the continuation packet."""
from pathlib import Path
import sys
import json
import numpy as np
import mpmath as mp
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import w33_pass12377_12381_continuation as p

def test_weber_against_jacobi_theta_and_eta_identity():
    mp.mp.dps=75
    tau=1+1j*mp.sqrt(3)/2
    q=mp.exp(mp.pi*1j*tau)
    eta=mp.exp(mp.pi*1j*tau/12)*mp.fprod(1-q**(2*n) for n in range(1,150))
    # f^2=theta3/eta, independently using the Jacobi-theta implementation.
    value=abs(mp.jtheta(3,0,q)/eta)**8/4
    cert=p.weber()
    assert abs(value-mp.mpf(cert['values'][-1]['ratio']))<mp.mpf('1e-65')

def test_full_link_curl_from_gauge_variation_and_random_transverse_basis():
    a,b,V,faces,loops=p.geometry();k=np.array([.19,-.28,.35,.21])
    A=p.curl(faces+loops,V,k);D=p.gradient(a,b,V,k)
    phi=np.random.default_rng(12377).normal(size=27)
    assert np.max(abs(A@(D@phi)))<1e-12
    U,sv,_=np.linalg.svd(D,full_matrices=True);T=U[:,27:]
    rotate=np.linalg.qr(np.random.default_rng(9).normal(size=(108,108)))[0]
    x=A@T;y=A@T@rotate
    assert np.allclose(np.linalg.eigvalsh(x.conj().T@x),np.linalg.eigvalsh(y.conj().T@y),atol=1e-12)

def test_saved_torsion_roots_by_exact_symbolic_substitution():
    record=json.loads((p.ROOT/'data/w33_pass12377_12381_continuation.json').read_text())
    x=s.Symbol('x')
    for row in record['torsion']['cases']:
        n=row['n'];phi=s.cyclotomic_poly(n,x)
        for v in row['h_exponents_of_zeros']:
            delta=s.Matrix([x**j-1 for j in v]);poly=s.expand((delta.T*p.N*delta)[0]/2)
            assert s.rem(poly,phi,x)==0

def test_native_intertwiner_kills_exactly_central_nontrivial_subspace():
    r=p.hamming();J=s.Matrix(r['native_regular_to_codes_integer_intertwiner'])
    # Independent exact rational rank, rather than the producer's SVD.
    assert J.rank()==9 and len(J.nullspace())==18
    # Each sum over the three central translates maps to three times a code basis vector.
    assert sorted(set(map(sum,J.tolist())))==[0,3]

def test_modular_negative_control_uses_both_generators():
    r=p.string_control();assert r['exact_S_invariance']
    A=np.array(r['character_coefficient_matrix']);assert np.count_nonzero(A)==8
    # A wrong T weight on just the O8 sector breaks level matching of its terms.
    tr=[-3,8,8,8];tl=[-8,4,16,16]
    residues=[(tr[i]-tl[j]-tl[k])%24 for i,j,k in np.ndindex(4,4,4) if A[i,4*j+k]]
    assert set(residues)=={0,1}
