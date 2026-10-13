"""Exact local kinetic repair of the marked TOE38 Maxwell acoustic tensor.

Prior TOE38 owns the plaquette complex; TOE41 owns its canonical-kinetic
birefringence. No gravitational action or physical light speed follows.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import sympy as sp
from sympy.polys.matrices import DomainMatrix
from scipy.linalg import qr, eigh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep, cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient


def cross(k):
    x, y, z = k
    return np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])


def derivative_rows(walks, ed, volts, lookup):
    """Exact integer coefficients of (1/i) dP/dk at zero."""
    out = np.zeros((3, len(walks), len(ed)), dtype=np.int64)
    for r, walk in enumerate(walks):
        acc = np.zeros(3, dtype=np.int64)
        for u, v in zip(walk, walk[1:]):
            e = lookup[tuple(sorted((u, v)))]
            if u == ed[e][0]:
                out[:, r, e] += acc
                acc += volts[e]
            else:
                out[:, r, e] -= acc - volts[e]
                acc -= volts[e]
        assert not np.any(acc)
    return out


def exact_solve(a, b):
    return DomainMatrix.from_Matrix(sp.Matrix(a)).convert_to(sp.QQ).lu_solve(
        DomainMatrix.from_Matrix(sp.Matrix(b)).convert_to(sp.QQ)).to_Matrix()


def construction():
    ed, volts, lookup, zero, comm, picked, _ = prep()
    b = np.rint(gradient(ed, volts, np.zeros(3)).real).astype(np.int64)[:, 1:]
    h = sp.Matrix(volts) - sp.Matrix(b) * exact_solve(b.T @ b, b.T @ volts)
    hi = np.array(160*h, dtype=np.int64)
    assert sp.Matrix(hi) == 160*h
    assert np.max(abs(b.T @ hi)) == 0
    n = np.rint(np.array([cycle_row(w, ed, volts, lookup, np.zeros(3))
                          for w in zero]).real).astype(np.int64)
    assert not np.any(n @ hi)
    # Certify that the first derivative of every native zero-winding
    # plaquette can be cancelled by a static massive-edge correction.
    d = derivative_rows(zero + comm, ed, volts, lookup)
    _, _, cols = qr(n.astype(float), mode="economic", pivoting=True)
    _, _, rows = qr(n[:, cols[:78]].T.astype(float), mode="economic", pivoting=True)
    cols = cols[:78]; rows = rows[:78]
    forcing = np.concatenate([d[i, :len(zero)] @ hi for i in range(3)], axis=1)
    x = exact_solve(n[np.ix_(rows, cols)], -forcing[rows])
    assert sp.Matrix(n[:, cols])*x + sp.Matrix(forcing) == sp.zeros(len(zero), 9)
    # Commutator rows have zero P(0). Their derivative is exactly curl
    # on the three cohomology periods: no numerical fit is used here.
    dc = np.array([d[i, len(zero):] @ hi for i in range(3)])
    # Six directions determine all coefficients of this quadratic tensor.
    for k in ([1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1]):
        c = sp.Matrix(np.einsum("i,irj->rj", k, dc))/160
        assert c.T*c == sp.Matrix(cross(k).T @ cross(k))
    # Gauss reduction matters: the kinetic form is the WEIGHTED harmonic
    # minimum, not h^T diag(w) h in the old unweighted harmonic basis.
    pairs = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    wf = np.ones(160)
    for _ in range(12):
        gh = volts-b@np.linalg.solve(b.T@(wf[:, None]*b), b.T@(wf[:, None]*volts))
        massf = gh.T@(wf[:, None]*gh)
        residual = np.array([massf[i, j]-(.5 if i == j else 0) for i, j in pairs])
        jac = np.array([gh[:, i]*gh[:, j] for i, j in pairs])
        if max(abs(residual)) < 1e-14:
            break
        wf -= jac.T@np.linalg.solve(jac@jac.T, residual)
        assert min(wf) > .1
    # Exact rational center and six active edges. Banach's theorem below
    # proves an EXACT zero in a tiny ball; the stored rational center alone
    # is a highly accurate approximate implementation, not that exact zero.
    _, _, pivots = qr(jac, mode="economic", pivoting=True)
    free = list(map(int, pivots[:6]))
    denominator = 10**12
    wi = np.rint(wf*denominator).astype(np.int64)
    w = sp.Matrix([sp.Rational(int(z), denominator) for z in wi])
    bi = sp.Matrix(b); vi = sp.Matrix(volts)
    lt = bi.T*sp.diag(*map(int, wi))*bi
    rhs = bi.T*sp.diag(*map(int, wi))*vi
    num, den = DomainMatrix.from_Matrix(lt).solve_den(
        DomainMatrix.from_Matrix(rhs), method="rref")
    gh = vi-bi*(num.to_Matrix()/den)
    mass = gh.T*sp.diag(*w)*gh
    F = sp.Matrix([mass[i, j]-(sp.Rational(1, 2) if i == j else 0)
                   for i, j in pairs])
    J = sp.Matrix([[gh[e, i]*gh[e, j] for e in free] for i, j in pairs])
    Ji = J.inv(method="DM")
    invnorm = max(sum(abs(Ji[i, j]) for j in range(6)) for i in range(6))
    eta = max(abs(z) for z in Ji*F)
    radius = sp.Rational(1, 10**8)
    # For weights in[1/8,2], G_ii<=V_i^T W V_i<=2 and leverage
    # |(B L^-1 B^T)_ef|<=8. Thus each second derivative of G_ij is
    # <=2*2/(1/8)^2=256. Six rows x six variables give 36*256*r.
    contraction = invnorm*36*256*radius
    assert all(sp.Rational(1, 8)+radius < z < 2-radius for z in w)
    assert eta < radius/4 and contraction < sp.Rational(1, 2)
    assert bi.T*sp.diag(*w)*gh == sp.zeros(79, 3)
    nonlinear = dict(radius=str(radius), selected_edges=free,
                     inverse_jacobian_inf_upper=1000,
                     newton_displacement_inf_upper="1/1000000000",
                     hessian_entry_upper=256,
                     contraction_upper="1/10",
                     theorem="Fixed-point map x-J0^-1 F(x) is a contraction on the exact rational-centered 6-edge infinity ball; an exact positive weight solution has Gauss-reduced G=I/2.")
    assert invnorm < 1000 and eta < sp.Rational(1, 10**9)
    assert contraction < sp.Rational(1, 10)
    return ed, volts, lookup, zero, comm, h, w, d, {
        "deck_chords": list(map(int, picked)),
        "harmonic_period_basis": [[str(z) for z in row] for row in h.tolist()],
        "canonical_period_gram": [[str(z) for z in row] for row in (h.T*h).tolist()],
        "electric_link_weights": [str(z) for z in w],
        "weight_bounds": ["1/8", "2"], "free_weight_indices": free,
        "center_period_kinetic_form_float": np.array(mass, dtype=float).tolist(),
        "exact_root_kinetic_form": "I/2", "exact_existence_certificate": nonlinear,
        "exact_native_derivative_cancellation": True,
        "exact_commutator_curl_gram": True,
        "native_rank_minor_determinant": str(sp.Matrix(n[np.ix_(rows, cols)]).det()),
    }


def finite_bloch(ed, volts, lookup, zero, comm, weights):
    w = np.array(weights, dtype=float).ravel()
    # C A = omega^2 diag(w) A. Nonzero eigenvectors automatically obey
    # B^dag diag(w) A=0; gauge invariance P B=0 is unchanged.
    out = []
    for direction in ([1, 0, 0], [1, 1, 1], [2, -1, 3]):
        direction = np.array(direction, dtype=float)
        direction /= np.linalg.norm(direction)
        for radius in (.02, .01, .005):
            k = radius*direction
            p = np.array([cycle_row(z, ed, volts, lookup, k) for z in zero+comm])
            b = gradient(ed, volts, k)
            _, _, vh = np.linalg.svd((np.sqrt(w)[:, None]*b).conj().T,
                                     full_matrices=True)
            t = vh.conj().T[:, 80:]/np.sqrt(w)[:, None]
            ev = np.linalg.eigvalsh((p@t).conj().T@(p@t))
            assert ev[0] > 0 and ev[2] > 1
            out.append(dict(direction=direction.tolist(), radius=radius,
                            velocity_squared=(ev[:2]/radius**2).tolist(),
                            relative_split=float((ev[1]-ev[0])/np.mean(ev[:2])),
                            gauss_residual=float(np.max(abs(b.conj().T@(w[:, None]*t)))),
                            third_gap=float(ev[2])))
    return out


def payload():
    ed, volts, look, zero, comm, h, w, d, cert = construction()
    cert["finite_bloch"] = finite_bloch(ed, volts, look, zero, comm, w)
    cert["status"] = "PASS"
    cert["leading_dispersion"] = "At certified exact weight root: omega^2=2 |k|^2, double transverse root, all real directions; stored rational center approximates root."
    cert["local_hamiltonian"] = "H=sum_e E_e^2/(2 w_e)+||P A||^2/2; Gauss B^dag E=0"
    cert["metric_promotion_obstruction"] = "With magnetic term fixed and no w dynamics, primary pi_w=0 has secondary E_e^2/(2 w_e^2)=0: every electric field is forced to zero. Local kinetic matching is not a dynamical gravity action."
    cert["scope"] = "Exact leading acoustic identity on supplied three-deck marking with chosen local positive weights; finite-k/RG, coefficient selection, Lorentz-covariant matter and gravitational closure open."
    cert["prior_owners"] = ["TOE38 local complex", "TOE41 acoustic/birefringence certificates", "analysis/w33_20261009_canonical_triplet_isotropy_theorem.py owns exact cycle-projector denominator160 and entry levels; period Gram is a selected submatrix of that prior projector"]
    paths = ["analysis/w33_20261010_toe38_local_maxwell_2complex.py",
             "analysis/w33_20261010_toe36_incidence_relativistic_walk.py"]
    cert["input_sha256_lf"] = {p: hashlib.sha256((ROOT/p).read_bytes().replace(b"\r\n", b"\n")).hexdigest() for p in paths}
    return cert


if __name__ == "__main__":
    result = payload()
    (ROOT/"data/w33_pass11956_local_electric_metric.json").write_text(json.dumps(result, indent=2)+"\n")
    print(result["status"], result["canonical_period_gram"], flush=True)
    for row in result["finite_bloch"]:
        print(row["radius"], row["velocity_squared"], row["relative_split"], flush=True)
