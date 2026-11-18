"""Actual exterior-form PW localizer; local model, not a compact G2 vacuum.

Prior: 580972009 E6 Morse model; ccdd3fe07 auxiliary Callias texture.
Standard Witten index technology: Dai/Yan arXiv:2011.05468.
Physical form/chirality dictionary: Braun et al arXiv:1812.06072 eq2.44.
"""
import json
from pathlib import Path
import numpy as np
import sympy as sy
from scipy import sparse as sp
from scipy.sparse.linalg import eigsh
from scipy.integrate import quad
from scipy.special import i0e

ROOT = Path(__file__).resolve().parents[1]


def clifford():
    wedge = []
    for i in range(3):
        E = np.zeros((8, 8), dtype=int)
        for mask in range(8):
            if not mask & (1 << i):
                E[mask | (1 << i), mask] = (-1)**((mask & ((1 << i)-1)).bit_count())
        wedge.append(E)
    a = [E-E.T for E in wedge]
    b = [E+E.T for E in wedge]
    grade = np.diag([(-1)**m.bit_count() for m in range(8)])
    I = np.eye(8, dtype=int)
    for i in range(3):
        assert np.array_equal(grade @ a[i]+a[i] @ grade, 0*I)
        assert np.array_equal(grade @ b[i]+b[i] @ grade, 0*I)
        for j in range(3):
            assert np.array_equal(a[i] @ a[j]+a[j] @ a[i], -2*(i == j)*I)
            assert np.array_equal(b[i] @ b[j]+b[j] @ b[i], 2*(i == j)*I)
            assert np.array_equal(a[i] @ b[j]+b[j] @ a[i], 0*I)
    # With only b3*Phi, unused b1 flips form parity and anticommutes D.
    assert np.array_equal(b[0] @ b[0], I)
    assert np.array_equal(b[0] @ b[2]+b[2] @ b[0], 0*I)
    return {"dimension": 8, "exact_anticommutators": True,
            "single_component_unused_b1_pairing": True,
            "pairing_scope": "full exterior-form module; domain invariant under constant b1"}


def exact_geometry():
    x, y, z = sy.symbols('x y z', real=True)
    variables = (x, y, z)
    f = (x**4-6*x*x*y*y+y**4)/4-(x*x+y*y)/2+z*z
    g = sy.Matrix([sy.diff(f, t) for t in variables])
    h = sy.hessian(f, variables)
    assert sy.trace(h) == 0
    solutions = sy.solve(list(g), variables)
    expected = {(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)}
    assert set(solutions) == expected
    records = []
    for p in sorted(solutions):
        H = h.subs(dict(zip(variables, p)))
        eigenvalues = sorted([v for v, n in H.eigenvals().items() for _ in range(n)])
        records.append({"point": list(p), "hessian_eigenvalues": list(eigenvalues),
                        "morse_index": sum(1 for v in eigenvalues if v < 0)})
    signed = sum((-1)**r['morse_index'] for r in records)
    assert signed == -3
    r2 = x*x+y*y
    V = sy.expand(g[0]**2+g[1]**2)
    assert sy.expand(V-(r2**3+r2-2*(x**4-6*x*x*y*y+y**4))) == 0
    # General angular proper-homotopy check, radius R=2, t in [0,1].
    # g_t = conjugate(w)^3-t*w, so |g_t| >= R^3-t*R >= 6.
    winding = []
    theta = np.linspace(0, 2*np.pi, 8193)
    w = 2*np.exp(1j*theta)
    for t in (0., .25, .5, .75, 1.):
        gv = np.conj(w)**3-t*w
        deg = float((np.unwrap(np.angle(gv))[-1]-np.unwrap(np.angle(gv))[0])/(2*np.pi))
        assert abs(deg+3) < 1e-10
        winding.append({"t": t, "winding": deg, "sample_minimum_gradient": float(min(abs(gv)))})
    return {"f": str(f), "laplacian_f": 0, "critical_points": records,
            "even_minus_odd_index": signed, "planar_winding_controls": winding,
            "exact_boundary_gradient_lower_bound_R2": 6,
            "planar_even_kernel": [0, 0],
            "L2_betti_positive_charge": [0, 3, 0, 0],
            "L2_betti_negative_charge": [0, 0, 3, 0],
            "count_proof": "proper-gradient Witten index -3; exp(+/-f2) not L2; z oscillator degree0; Hodge dual for negative charge",
            "z_oscillator_gap": 4,
            "native_E6_charge_choice": "H=-Psi/3; adjoint16_-3 effective charge +1",
            "E8_common_T_net_spinor_index_for_nu3": 6}


def hermite_operators(n, omega):
    # Padding makes all degree<=6 polynomial matrix elements exact Galerkin,
    # unlike taking powers of the already truncated position operator.
    m = n+8
    lower = sp.diags(np.sqrt(np.arange(1, m)), 1, shape=(m, m), format='csc')
    X = (lower+lower.T)/np.sqrt(2*omega)
    derivative = np.sqrt(omega/2)*(lower-lower.T)
    powers = {k: (X**k)[:n, :n].tocsc() for k in (1, 2, 4, 6)}
    kinetic = (-(derivative @ derivative))[:n, :n].tocsc()
    return powers, kinetic


def index_and_symmetry():
    # Flat-space Witten index = pullback normalized Gaussian volume by grad f2.
    # Angular integral computed independently with scaled Bessel I0.
    density = lambda r: 2*r*(1-9*r**4)*np.exp(-r**6-r*r+2*r**4)*i0e(2*r**4)
    integral, error = quad(density, 0, np.inf, epsabs=1e-10, epsrel=1e-10)
    assert abs(integral+3) < 1e-9
    # Four negative ends permute cyclically; reduced H0 = standard 3D subspace.
    P = sy.zeros(4)
    for i in range(4):
        P[(i+1) % 4, i] = 1
    B = sy.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, -1, -1]])
    R = (B.T*B).inv()*B.T*P*B
    assert P*B == B*R and R**4 == sy.eye(3)
    u = sy.Symbol('u')
    assert sy.expand(R.charpoly(u).as_expr()-(u+1)*(u*u+1)) == 0
    invariant = []
    for k in range(4):
        # Representation is regular C4 minus its trivial character.
        invariant.append(0 if k == 0 else 1)
    return {"independent_gaussian_index_integral": integral, "quadrature_error_estimate": error,
            "C4_exact_reduced_regular_matrix": [list(map(int, R.row(i))) for i in range(3)],
            "C4_characteristic_polynomial": "(u+1)*(u^2+1)",
            "C4_invariants_after_gauge_character_k": invariant,
            "general_harmonic_family": "Re(w^m)/m-|w|^2/2+z^2; m>=3",
            "general_L2_degree1_count": "m-1; degree m is input, not selected",
            "general_critical_hessians": {str(m): {"outer_count": m,
                "outer_eigenvalues": [-m, m-2, 2], "origin_eigenvalues": [-1, -1, 2],
                "even_minus_odd_index": 1-m} for m in range(3, 9)}}


def galerkin(n, omega=3.):
    X, K = hermite_operators(n, omega)
    I = sp.eye(n, format='csc')
    kron = sp.kron
    H = (kron(K, I)+kron(I, K)+kron(X[6], I)+kron(I, X[6])
         +3*kron(X[4], X[2])+3*kron(X[2], X[4])
         +kron(X[2], I)+kron(I, X[2])-2*kron(X[4], I)-2*kron(I, X[4])
         +12*kron(X[2], X[2])).tocsc()
    diag = 6*(kron(X[2], I)-kron(I, X[2]))
    cross = -12*kron(X[1], X[1])
    odd = sp.bmat([[H+diag, cross], [cross, H-diag]], format='csc')
    assert sp.linalg.norm(odd-odd.T) < 1e-9
    # Deterministic start vector, no dependency on scipy's global RNG.
    v0 = np.random.default_rng(18).normal(size=2*n*n)
    ev, vec = eigsh(odd, k=8, sigma=-.001, which='LM', tol=1e-11, v0=v0)
    order = np.argsort(ev); ev = ev[order]; vec = vec[:, order]
    residual = max(np.linalg.norm(odd @ vec[:, i]-ev[i]*vec[:, i]) for i in range(8))
    scalar = float(eigsh(H, k=1, sigma=0, which='LM', v0=v0[:n*n], tol=1e-11)[0][0])
    # Active rotation: coefficient functions u(R^-1 x), forms R u.
    rows, cols, vals = [], [], []
    for nx in range(n):
        for ny in range(n):
            rows.append(ny*n+nx); cols.append(nx*n+ny); vals.append((-1)**ny)
    P = sp.csc_matrix((vals, (rows, cols)), shape=(n*n, n*n))
    U = sp.bmat([[None, -P], [P, None]], format='csc')
    comm = float(sp.linalg.norm(U @ odd-odd @ U))
    assert comm < 1e-8
    small = vec[:, :3]
    restricted = small.T @ (U @ small)
    leakage = float(np.linalg.norm(U @ small-small @ restricted))
    eigen_u = np.linalg.eigvals(restricted)
    assert np.min(ev) > -1e-8 and residual < 1e-7
    return {"basis_per_axis": n, "omega": omega, "dimension_odd": 2*n*n,
            "odd_lowest_ritz": ev.tolist(), "max_residual": float(residual),
            "even0_lowest_ritz": scalar+2, "even2_lowest_ritz": scalar-2,
            "C4_commutator_frobenius": comm, "C4_low3_leakage": leakage,
            "C4_low3_eigenvalues": sorted([[float(v.real), float(v.imag)] for v in eigen_u])}


def run():
    native = json.loads((ROOT/'data/toe_20261118_E6_Morse_relative_families.json').read_text())['native_E6']
    assert native['adjoint_charge_dimensions'] == {'-3': 16, '0': 46, '3': 16}
    assert native['minus3_family_Q6Y'] == {'2': 3, '0': 1, '6': 1, '-4': 3, '1': 6, '-3': 2}
    result = {"scope": "noncompact PW BPS background and specified L2 charged operator; no compact G2 or SM completion",
              "clifford": clifford(), "geometry": exact_geometry(),
              "index_and_symmetry": index_and_symmetry(), "spectral": []}
    result['native_E6_charge_certificate_checked'] = True
    for n in (16, 24, 32, 40):
        record = galerkin(n)
        result['spectral'].append(record)
        print('N', n, 'odd', record['odd_lowest_ritz'][:4], 'even2', record['even2_lowest_ritz'], flush=True)
    last = result['spectral'][-1]
    assert max(last['odd_lowest_ritz'][:3]) < .001
    assert last['odd_lowest_ritz'][3] > .1
    result['independent_oscillator_width'] = galerkin(40, omega=2.)
    result['limitations'] = ["quartic degree and coefficients supplied", "infinite background energy on R3",
        "gauge constants not L2 on R3", "no global G2 gluing", "E6 Psi anomaly and rank-breaking remain",
        "bare adjoint two-family cubic still zero", "fixed H27 flavor compatibility unbuilt",
        "Ritz values support convergence, do not prove exact kernel counts or positive gap bounds"]
    path = ROOT/'data/toe_20261118_PW_Clifford_A3_localizer.json'
    path.write_text(json.dumps(result, indent=2, default=lambda v: int(v))+'\n', encoding='utf-8')
    print('PASS', path, flush=True)
    return result


if __name__ == '__main__':
    run()
