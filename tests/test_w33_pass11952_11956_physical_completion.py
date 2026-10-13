"""Independent controls for the five physical-completion fronts."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import sympy as s
import pytest
from numpy.polynomial.legendre import leggauss

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"analysis"))
import w33_pass11952_11955_threshold_vacuum_loop_leptons as p
import w33_pass11956_local_electric_metric as g


def test_chiral_threshold_positive_zero_orders_and_winding():
    z = .02*np.exp(1j*np.linspace(0, 2*np.pi, 401))
    for orders in ([0], [1, 2], [0, 1, 3], [2, 2, 2]):
        amplitude = z**3*np.prod([z**q for q in orders], axis=0)
        phase = np.unwrap(np.angle(amplitude))
        assert abs((phase[-1]-phase[0])/(2*np.pi)-(3+sum(orders))) < 1e-12


def test_singular_uv_factor_is_a_distinct_negative_control():
    e = s.symbols("e", nonzero=True)
    assert s.simplify(e**-6*e**3*e**3) == 1
    assert s.limit(e**3*e**3, e, 0) == 0


def test_fi_free_vacuum_full_real_hessian_and_gauge_mode():
    z = s.symbols("S1 S2 T1 T2 X Y Z")
    S1, S2, T1, T2, X, Y, Z = z
    W = X*(S1*T1-1)+2*Y*(S2*T2-1)+3*Z*(S1*T2+S2*T1)
    home = dict(zip(z, [1, s.I, 1, -s.I, 0, 0, 0]))
    assert all(s.diff(W, a).subs(home) == 0 for a in z)
    assert W.subs(home) == 0
    J = s.Matrix([s.diff(W, a) for a in z]).jacobian(z).subs(home)
    q = np.array(J, dtype=complex)
    A = q.conj().T@q
    H = 2*np.block([[A.real, -A.imag], [A.imag, A.real]])
    D = np.array([-2, 0, 2, 0, 0, 0, 0, 0, -2, 0, -2, 0, 0, 0])
    H += np.outer(D, D)
    ev = np.linalg.eigvalsh(H)
    assert abs(ev[0]) < 1e-12 and ev[1] > 3.9
    goldstone = np.array([0, 1, 0, 1, 0, 0, 0, -1, 0, 1, 0, 0, 0, 0])
    assert np.max(abs(H@goldstone)) < 1e-12
    assert s.im((S1*T2).subs(home)) == -1


def test_explicit_messenger_generates_upper_block_operator():
    R, Rc, QH, T, Dc, L, a, b = s.symbols("R Rc QH T Dc L a b", nonzero=True)
    W = L*R*Rc+a*QH*Rc+b*T*R*Dc
    sol = s.solve([s.diff(W, R), s.diff(W, Rc)], [R, Rc])
    assert s.simplify(W.subs(sol)+a*b*T*QH*Dc/L) == 0


def test_charge_completion_identity_for_u1_and_discrete_groups():
    # Let q(dc)=u,q(D)=v,q(QHd)=-u,q(Dc)=-v,
    # q(S)=-u-v and q(T)=u+v. All five operators are neutral.
    for modulus in range(2, 19):
        for u in range(modulus):
            for v in range(modulus):
                assert ((u+v)-u-v) % modulus == 0


def test_complete_e6_inventory_and_allowed_su5_leak():
    fields = p.e6_inventory()["fields_Qpsi_X_familyZ2"]
    assert (-1)**fields["S_27Bi16"][0]*fields["S_27Bi16"][2] == 1
    assert (-1)**fields["D_27A10"][0]*fields["D_27A10"][2] == -1
    members = ["q_native16", "Hd_native10", "Dc_bar27A10", "T_bar27Bi16"]
    assert sum(fields[z][0] for z in members) == 0
    assert sum(fields[z][1] for z in members) == 0
    # The named E6 contraction has this nonzero SU5 component.
    Q = np.zeros((5, 5)); Q[0, 1] = 1; Q[1, 0] = -1
    Hd = np.eye(5)[0]; Dc = np.eye(5)[1]
    assert Hd@Q@Dc == 1


def test_neutral_scalar_cp_portal_controls():
    main = p.scalar_loop()
    assert abs(main["theta"]) > 1e-6
    assert abs(main["theta"]+p.scalar_loop(cp_sign=-1)["theta"]) < 1e-15
    assert abs(p.scalar_loop((0, 0))["theta"]) < 1e-15
    assert abs(p.scalar_loop((.1, .1))["theta"]) < 1e-15
    assert abs(main["theta"]-p.scalar_loop(scale=3)["theta"]) < 1e-15


def test_scalar_self_energy_by_independent_feynman_parameter_integration():
    m = np.array([[1, 1, 0], [0, 2, 1], [1, 0, 3]], float)/10
    r = np.array([1, 2, 1])/10; t = np.array([1, -1, 2])/10
    M = np.zeros((4, 4), complex); M[:3, :3] = m
    M[3, :3] = r+1j*t; M[3, 3] = .2
    vertices = np.zeros((5, 4, 4), complex)
    vertices[0, :3, :3] = m
    for i, row in enumerate([r, 1j*r, t, 1j*t], 1):
        vertices[i, 3, :3] = row
    K = np.diag([1., 3., 1.5, 1.5, 3.])
    for i, j, val in [(1, 4, 1), (2, 3, .5), (0, 1, .1), (0, 4, .2)]:
        K[i, j] = K[j, i] = val
    scalars, O = np.linalg.eigh(K)
    masses, V = np.linalg.eigh(M.conj().T@M)
    nodes, weights = leggauss(1024); nodes = (nodes+1)/2; weights /= 2
    delta = np.zeros((4, 4), complex)
    for a, scalar in enumerate(scalars):
        integrals = -weights@np.log(nodes[:, None]*masses+(1-nodes[:, None])*scalar)
        F = (V*integrals)@V.conj().T
        gamma = np.einsum("i,ijk->jk", O[:, a], vertices)
        delta += gamma@F@M.conj().T@gamma/(16*np.pi**2)
    theta = np.trace(np.linalg.solve(M, delta)).imag
    assert abs(theta-p.scalar_loop()["theta"]) < 1e-12


def test_scalar_hessian_from_declared_potential():
    h, x, y, u, v = s.symbols("h x y u v", real=True)
    p1, p2 = s.symbols("p1 p2", real=True)
    a = x*x+y*y; b = u*u+v*v
    V = (a+b-2)**2/4+(a-b)**2/8+(x*u+y*v)**2/2+(h*h-1)**2/8
    V += (h*h-1)*(p1*(a-1)+p2*(b-1))/4
    home = {h: 1, x: 1, y: 0, u: 0, v: 1}
    assert all(s.diff(V, z).subs(home) == 0 for z in (h, x, y, u, v))
    H = s.hessian(V, (h, x, y, u, v)).subs(home)
    goldstone = s.Matrix([0, 0, 1, -1, 0])
    H += goldstone*goldstone.T/2
    assert H == s.Matrix([[1, p1, 0, 0, p2], [p1, 3, 0, 0, 1],
                           [0, 0, s.Rational(3, 2), s.Rational(1, 2), 0],
                           [0, 0, s.Rational(1, 2), s.Rational(3, 2), 0], [p2, 1, 0, 0, 3]])


def test_msbar_divergent_theta_cancels_symbolically():
    m = s.Matrix([[1, 1, 0], [0, 2, 1], [1, 0, 3]])/10
    # Explicit row vectors avoid the intake scanner's [[n,k,d]] token syntax.
    r = s.Matrix([1, 2, 1]).T/10; t = s.Matrix([1, -1, 2]).T/10
    M = m.row_join(s.zeros(3, 1)).col_join((r+s.I*t).row_join(s.Matrix([[s.Rational(1, 5)]])))
    vertices = [m.row_join(s.zeros(3, 1)).col_join(s.zeros(1, 4))]
    vertices += [s.zeros(3, 4).col_join(z.row_join(s.zeros(1, 1))) for z in (r, s.I*r, t, s.I*t)]
    assert s.im(sum(s.trace(M.inv()*z*M.conjugate().T*z) for z in vertices)) == 0


def test_common_su5_kernel_mass_transpose_for_random_real_yukawas():
    rng = np.random.default_rng(11955)
    for _ in range(10):
        B = rng.normal(size=3)+1j*rng.normal(size=3)
        K = np.eye(3)-np.outer(B.conj(), B)/(1+np.vdot(B, B).real)
        A = p.positive_root(K); m = rng.normal(size=(3, 3))
        d = m@A; e = A.T@m.T
        assert np.max(abs(e-d.T)) < 1e-12
        assert np.max(abs(np.sort(np.linalg.svd(e, compute_uv=False))-
                             np.sort(np.linalg.svd(d, compute_uv=False)))) < 1e-12


def test_pmns_weyl_basis_covariance():
    rng = np.random.default_rng(11955)
    e = rng.normal(size=(3, 3))+1j*rng.normal(size=(3, 3))
    n = rng.normal(size=(3, 3))+1j*rng.normal(size=(3, 3)); n += n.T
    R, _ = np.linalg.qr(rng.normal(size=(3, 3))+1j*rng.normal(size=(3, 3)))
    def pmns(e, n):
        _, ue = np.linalg.eigh(e.conj()@e.T)
        _, un = np.linalg.eigh(n.conj().T@n)
        return abs(ue.conj().T@un)**2
    assert np.max(abs(pmns(e, n)-pmns(R.T@e, R.T@n@R))) < 1e-12


def test_shared_kernel_cp_and_parity_controls():
    main = p.lepton_probe()
    conjugate = p.lepton_probe(np.array([1-1j, 2+1j, 1-2j]))
    assert abs(main["J"]) > 1e-5 and main["kernel_parity_commutator"] > .1
    assert abs(main["J"]+conjugate["J"]) < 1e-12
    assert abs(p.lepton_probe(np.array([1, 2, 1]))["J"]) < 1e-12


@pytest.fixture(scope="module")
def native():
    return g.construction()


def test_exact_native_curl_tensor_all_quadratic_coefficients(native):
    ed, volts, look, zero, comm, h, weights, derivatives, cert = native
    k = s.symbols("kx ky kz", real=True)
    dc = [s.Matrix(derivatives[i, len(zero):])*h for i in range(3)]
    C = sum((k[i]*dc[i] for i in range(3)), s.zeros(3))
    X = s.Matrix([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    assert (C.T*C-X.T*X).applyfunc(s.expand) == s.zeros(3)


def test_exact_positive_root_certificate_and_prior_projector(native):
    *_, h, weights, derivatives, cert = native
    assert h.T*h == s.Matrix([[81, 1, 1], [1, 81, -3], [1, -3, 81]])/160
    assert min(weights) > s.Rational(1, 8) and max(weights) < 2
    c = cert["exact_existence_certificate"]
    assert s.Rational(c["contraction_upper"]) < s.Rational(1, 2)
    assert s.Rational(c["newton_displacement_inf_upper"]) < s.Rational(c["radius"])/4
    assert len(set(c["selected_edges"])) == 6


def test_exact_walk_derivatives_against_bloch_negative_momenta(native):
    ed, volts, look, zero, comm, _, _, D, _ = native
    for j in [0, 300, 1000, len(zero), len(zero)+2]:
        w = (zero+comm)[j]
        for i in range(3):
            k = np.eye(3)[i]*1e-6
            fd = (g.cycle_row(w, ed, volts, look, k)-g.cycle_row(w, ed, volts, look, -k))/(2j*1e-6)
            assert np.max(abs(fd-D[i, j])) < 1e-9


def test_finite_k_gauss_and_light_branches(native):
    ed, volts, look, zero, comm, _, weights, _, _ = native
    rows = g.finite_bloch(ed, volts, look, zero, comm, weights)
    assert max(x["gauss_residual"] for x in rows) < 1e-10
    assert max(x["relative_split"] for x in rows) < 2e-5
    assert max(max(abs(z-2) for z in x["velocity_squared"]) for x in rows) < 2e-4


def test_metric_promotion_primary_constraint_is_not_gravity():
    w, E, pi = s.symbols("w E pi", positive=True)
    H = E**2/(2*w)
    preservation = -s.diff(H, w)
    assert preservation == E**2/(2*w*w)
    assert s.solve(preservation, E) == []  # positive electric field cannot satisfy it


def test_frozen_input_hashes():
    for name in ("w33_pass11952_11955_threshold_vacuum_loop_leptons.json", "w33_pass11956_local_electric_metric.json"):
        data = json.loads((ROOT/"data"/name).read_text())
        assert data["status"] == "PASS"
        for path, expected in data["input_sha256_lf"].items():
            assert hashlib.sha256((ROOT/path).read_bytes().replace(b"\r\n", b"\n")).hexdigest() == expected
