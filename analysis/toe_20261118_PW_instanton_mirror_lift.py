"""Explicit PW Morse trajectories and the lifted vectorlike pair.

Prior d7280e023 proves three exact local chiral profiles; here we resolve
the finite positive eigenvalue, not observed particle masses or a G2 vacuum.
"""
import json
from pathlib import Path
from math import lcm
import numpy as np
import sympy as s
from scipy import sparse as sp
from scipy.sparse.linalg import eigsh
from toe_20261118_PW_Clifford_A3_localizer import hermite_operators
import w33_pass10950_clock_albert_lorentz_spinor as native

ROOT = Path(__file__).resolve().parents[1]


def exact_trajectories():
    x, y, z, t = s.symbols('x y z t', real=True)
    f = (x**4-6*x*x*y*y+y**4)/4-(x*x+y*y)/2+z*z
    r = 1/s.sqrt(1+s.exp(-2*t))
    for px, py in [(r, 0), (-r, 0), (0, r), (0, -r)]:
        for variable, coordinate in ((x, px), (y, py), (z, 0)):
            rhs = -s.diff(f, variable).subs({x: px, y: py, z: 0}, simultaneous=True)
            assert s.simplify(s.diff(coordinate, t)-rhs) == 0
    assert s.limit(r, t, -s.oo) == 0 and s.limit(r, t, s.oo) == 1
    assert f.subs({x: 1, y: 0, z: 0}) == -s.Rational(1, 4)
    incidence = s.ones(1, 4)
    projector = s.eye(4)-s.ones(4)/4
    assert incidence*projector == s.zeros(1, 4)
    assert projector**2 == projector and projector.rank() == 3
    # Fourier basis: one invariant lifted direction, three nontrivial C4 chars.
    Fourier = s.Matrix([[s.I**(j*k)/2 for k in range(4)] for j in range(4)])
    assert s.simplify(Fourier.conjugate().T*Fourier) == s.eye(4)
    assert incidence*Fourier == s.Matrix([[2, 0, 0, 0]])
    angles=s.symbols('theta0:4',real=True)
    phase_row=s.Matrix([[s.exp(s.I*a) for a in angles]])
    assert s.simplify((phase_row*phase_row.conjugate().T)[0,0])==4
    return {"trajectory_radius": "(1+exp(-2*t))^(-1/2)", "verified_flows": 4,
            "f_origin_minus_f_outer": "1/4", "negative_gradient_polar_angular_velocity": "r^2*sin(4*theta)",
            "Morse_incidence_row_orientation_choice": [[1, 1, 1, 1]],
            "kernel_projector": [[str(v) for v in projector.row(i)] for i in range(4)],
            "Morse_differential_rank": 1, "Morse_kernel_dimension": 3,
            "arbitrary_unit_phase_row_norm_squared": 4,
            "exact_low_subspace_mass_row": "sqrt(lambda_q)/2 * (1,1,1,1)",
            "basis_scope": "C4 Fourier choice within exact three zero modes plus lowest positive odd partner; not exactly point-supported Gaussian states"}


def scalar_hamiltonian(n, q, omega):
    X, K = hermite_operators(n, omega)
    I = sp.eye(n, format='csc'); kron = sp.kron
    V = (kron(X[6], I)+kron(I, X[6])+3*kron(X[4], X[2])+3*kron(X[2], X[4])
         +kron(X[2], I)+kron(I, X[2])-2*kron(X[4], I)-2*kron(I, X[4])
         +12*kron(X[2], X[2]))
    return (kron(K, I)+kron(I, K)+q*q*V-2*q*sp.eye(n*n)).tocsc()


def native_bilinear():
    # Explicit graded generators from the actual clock-Albert product.
    J=native.build_clock_albert()
    den=lcm(*[v.denominator for v in J['prod'].flat])
    tensor=np.array([[[int(v*den) for v in row] for row in plane]
                     for plane in J['prod']],dtype=np.int64)
    L=np.stack([tensor[i].T for i in range(27)])
    c=J['idx'][J['G'][0]]
    half=[i for i in range(27) if 2*L[c,i,i]==den]
    assert len(half)==16
    D=[L[c]@L[h]-L[h]@L[c] for h in half]
    minus=np.stack([den*L[h]-2*d for h,d in zip(half,D)])
    plus=np.stack([den*L[h]+2*d for h,d in zip(half,D)])
    Psi=6*L[c]-2*den*np.eye(27,dtype=np.int64)
    for sign, block in ((-1,minus),(1,plus)):
        assert all(np.array_equal(Psi@M-M@Psi,sign*3*den*M) for M in block)
    assert all(not np.any(A@B-B@A) for i,A in enumerate(minus) for B in minus[i+1:])
    gram=s.Matrix(np.einsum('aij,bji->ab',plus,minus).tolist())/den**4
    assert gram==12*s.eye(16)
    return {"actual_native_charge_dimensions":[16,16],"trace_pairing_rank":16,
            "trace_pairing_eigenvalues":{str(k):int(v) for k,v in gram.eigenvals().items()},
            "same_charge_pair_brackets_vanish":True,
            "meaning":"Rbar-R bilinear is nondegenerate; R-R adjoint cubic still forbidden; neither fact predicts a light-family Yukawa"}


def rectangular_partner(n, q, omega):
    # True exterior d_f^dagger: N -> N+3 per coordinate, no truncation loss.
    m = n+3; pad = n+8
    lower = sp.diags(np.sqrt(np.arange(1, pad)), 1, shape=(pad, pad), format='csc')
    X = (lower+lower.T)/np.sqrt(2*omega)
    derivative = np.sqrt(omega/2)*(lower-lower.T)
    powers = {k: (X**k)[:m, :n] for k in (1, 2, 3)}
    J = sp.eye(pad, format='csc')[:m, :n]
    deriv = derivative[:m, :n]
    kron = sp.kron
    fx = kron(powers[3], J)-3*kron(powers[1], powers[2])-kron(powers[1], J)
    fy = kron(J, powers[3])-3*kron(powers[2], powers[1])-kron(J, powers[1])
    Cx = kron(deriv, J)-q*fx
    Cy = kron(J, deriv)-q*fy
    return sp.vstack([Cy, -Cx], format='csc')


def spectral_case(n, q, width_ratio=1.):
    omega = max(3., q)*width_ratio
    H = scalar_hamiltonian(n, q, omega)
    B = rectangular_partner(n, q, omega)
    factor_error = float(sp.linalg.norm(B.T @ B-H))
    assert factor_error/(1+sp.linalg.norm(H)) < 1e-12
    v0 = np.random.default_rng(33).normal(size=n*n)
    vals, vec = eigsh(H, k=3, sigma=-1e-6, which='LM', tol=1e-11, v0=v0)
    order = np.argsort(vals); vals=vals[order]; vec=vec[:, order]
    v = vec[:, 0]
    lam = float(vals[0])
    residual = float(np.linalg.norm(H @ v-lam*v))
    # H is degree six: N+6 captures its ENTIRE action on this finite vector.
    # Thus this is an actual L2 residual, not just a projected eigensolver residual.
    N=n+6
    embedded=np.zeros((N,N)); embedded[:n,:n]=v.reshape(n,n)
    full_residual=float(np.linalg.norm(scalar_hamiltonian(N,q,omega)@embedded.ravel()-lam*embedded.ravel()))
    bv = B @ v
    norm2 = float(bv @ bv)
    relative_norm_error = abs(norm2-lam)/max(lam, 1e-14)
    assert lam > 0 and residual < 1e-6
    assert relative_norm_error < 1e-5
    # Ground scalar is invariant under quarter-turn (positivity/simple ground).
    rotated = v.reshape(n,n).T*np.array([(-1)**j for j in range(n)])[:,None]
    rotation_error = np.linalg.norm(rotated.ravel()-v)
    assert rotation_error < 1e-7
    approx = 2*np.sqrt(2)/np.pi*q*np.exp(-q/2)
    return {"q": q, "n": n, "omega": omega, "lowest_lambda": lam,
            "next_two_lambda": vals[1:].tolist(), "projected_eigen_residual": residual,
            "full_space_polynomial_operator_residual":full_residual,
            "exterior_partner_norm_squared": norm2, "partner_relative_norm_error": relative_norm_error,
            "exact_Galerkin_factor_relative_error": factor_error/(1+float(sp.linalg.norm(H))),
            "C4_ground_rotation_error": float(rotation_error),
            "Eyring_Kramers_candidate": float(approx), "lambda_over_candidate": lam/approx,
            "dimensionless_singular_mass": float(np.sqrt(lam)),
            "mirror_to_next_internal_mass_ratio": float(np.sqrt(lam/min(vals[1],4*q))),
            "C4_point_basis_equal_entry": float(np.sqrt(lam)/2)}


def run():
    prior=json.loads((ROOT/'data/toe_20261118_PW_Clifford_A3_localizer.json').read_text())
    assert prior['geometry']['L2_betti_positive_charge'] == [0,3,0,0]
    out={"scope": "local internal PW mirror-pair lift; no global G2/SM or observed mass prediction",
         "exact":exact_trajectories(), "native_bilinear":native_bilinear(), "spectral":[],
         "semiclassical_normalization": "H_q=q^2 Delta_(h), h=1/q; candidate lambda=(2sqrt(2)/pi)q exp(-q/2)",
         "asymptotic_status": "tested leading Eyring-Kramers prediction; whole-space escape-domain theorem not proved here"}
    for q in (1.,2.,4.,6.,8.,12.,16.,20.,24.):
        for n in (32,48):
            row=spectral_case(n,q)
            out['spectral'].append(row)
            print('q',q,'N',n,'lambda',row['lowest_lambda'],'ratio',row['lambda_over_candidate'],flush=True)
    out['independent_width_controls']=[spectral_case(56,q,.75) for q in (8.,16.,24.)]
    out['high_resolution_controls']=[spectral_case(80,8.),spectral_case(96,24.)]
    assert out['high_resolution_controls'][-1]['full_space_polynomial_operator_residual']<1e-8
    # Required convergence before interpreting the smallest finite mass.
    for q in (8.,16.,24.):
        base=next(r for r in out['spectral'] if r['q']==q and r['n']==48)
        check=next(r for r in out['independent_width_controls'] if r['q']==q)
        assert abs(base['lowest_lambda']/check['lowest_lambda']-1)<.002
    out['limitations']=["quartic and q supplied", "C4 Fourier mass row basis choice",
        "Morse incidence is not a normalized finite-q mass matrix", "whole-space Eyring-Kramers asymptotic not certified",
        "no chiral-generation Yukawa from this vectorlike mass", "native adjoint16_-3 pair brackets still vanish",
        "no compactification scale or global inflow/gauge normalization"]
    path=ROOT/'data/toe_20261118_PW_instanton_mirror_lift.json'
    path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('PASS',path,flush=True)
    return out


if __name__=='__main__':
    run()
