"""12533: the Fox colourings of 6 points are the zero-charge monomials of 6 Z_3 parafermions.  Fradkin-Kadanoff: g_{2j-1} = s_j prod_{k<j} t_k, g_{2j} = (phase) s_j prod_{k<=j} t_k on 3 qutrits (27 dims), g_i g_j = w^e g_j g_i for i < j with one constant e.  With u_i = (-1)^i c_i,
M_u = prod g_i^{u_i}.  Tests: (1) the closed form omega(c, c') = sum_{i<j} (u_i u'_j - u_j u'_i) is invariant under Fox and is the unique form of fox_w33.py up to scale; (2) the g relations; (3) zero-charge monomials commute with Q = prod t_k; (4) M_u M_u' = w^{e omega} M_u' M_u for all colourings;
(5) the constant colouring acts as a scalar on each Q sector, so 'mod constants' is 'fixed total charge'; (6) on a Q sector (9 dims) the 81 classes are trace-orthogonal, a two-qutrit Pauli group; (7) the triangle: the TL6 braid generator built from an eigenprojector of the neighbouring bilinear M(a_i) acts on monomials by the Fox rule.  usage: py -3 parafermion_w33.py"""
import itertools
import json
import numpy as np

w3 = np.exp(2j * np.pi / 3)
S = np.roll(np.eye(3), 1, axis=0).astype(complex)
T = np.diag([1, w3, w3 ** 2])
I3 = np.eye(3, dtype=complex)


def op(*fs):
    M = np.eye(1, dtype=complex)
    for f in fs:
        M = np.kron(M, f)
    return M


s = [op(S, I3, I3), op(I3, S, I3), op(I3, I3, S)]
t = [op(T, I3, I3), op(I3, T, I3), op(I3, I3, T)]
g = []
for j in range(3):
    st = s[j]
    for k in range(j):
        st = st @ t[k]
    g.append(st)
    g.append(st @ t[j])
out = {}
rel = set()
for i, j in itertools.combinations(range(6), 2):
    A = g[i] @ g[j]
    B = g[j] @ g[i]
    k = np.trace(B.conj().T @ A) / 27
    assert np.allclose(A, k * B), (i, j)
    rel.add(round(float(np.angle(k) / (2 * np.pi / 3))) % 3)
out["g_i_g_j_constant_exponent_for_i_lt_j"] = sorted(rel)
e = sorted(rel)[0]
Q = t[0] @ t[1] @ t[2]
alt = lambda c: sum((-1) ** i * x for i, x in enumerate(c)) % 3
sign = lambda c: tuple(((-1) ** i * x) % 3 for i, x in enumerate(c))


def M(c):
    u = sign(c)
    R = np.eye(27, dtype=complex)
    for i in range(6):
        R = R @ np.linalg.matrix_power(g[i], u[i])
    return R


def omega(c, d):
    u, v = sign(c), sign(d)
    return sum(u[i] * v[j] - u[j] * v[i] for i in range(6) for j in range(i + 1, 6)) % 3


def fox(c, s_):
    c = list(c)
    i = s_ - 1
    a, b = c[i], c[i + 1]
    c[i], c[i + 1] = b, (2 * b - a) % 3
    return tuple(c)


ALL = [c for c in itertools.product(range(3), repeat=6) if alt(c) == 0]
one = (1, 1, 1, 1, 1, 1)
out["closed_form_fox_invariant"] = all(omega(fox(c, s_), fox(d, s_)) == omega(c, d) for s_ in range(1, 6) for c in ALL[::7] for d in ALL[::11])
out["constants_in_radical"] = all(omega(one, c) == 0 for c in ALL)
known = json.load(open("fox_w33.json"))["a_vectors_as_colourings"]
a = {int(k): tuple(v) for k, v in known.items()}
out["closed_form_chain_pattern"] = {f"{s_},{t_}": omega(a[s_], a[t_]) for s_, t_ in itertools.combinations(sorted(a), 2)}
out["zero_charge_monomials_commute_with_Q"] = all(np.allclose(M(c) @ Q, Q @ M(c)) for c in ALL[::3])
cc = True
for c in ALL[::9]:
    for d in ALL[::13]:
        cc &= np.allclose(M(c) @ M(d), w3 ** (e * omega(c, d)) * M(d) @ M(c))
out["commutators_match_closed_form"] = bool(cc)
vals, vecs = np.linalg.eig(Q)
sec = {}
for lam in (1, w3, w3 ** 2):
    Pi = sum(np.linalg.matrix_power(Q / lam, k) for k in range(3)) / 3
    u_, sv, _ = np.linalg.svd(Pi)
    sec[lam] = u_[:, :int(round(np.trace(Pi).real))]
out["sector_dims"] = sorted(v.shape[1] for v in sec.values())
B0 = sec[1]
Mc = B0.conj().T @ M(one) @ B0
out["constant_colouring_is_scalar_on_a_sector"] = bool(np.allclose(Mc, Mc[0, 0] * np.eye(9))) and bool(all(np.allclose((v.conj().T @ M(one) @ v), (v.conj().T @ M(one) @ v)[0, 0] * np.eye(9)) for v in sec.values()))
canon = lambda c: tuple((x - c[0]) % 3 for x in c)
cls = sorted({canon(c) for c in ALL})
assert len(cls) == 81
mats = [B0.conj().T @ M(c) @ B0 for c in cls]
Gm = np.abs(np.array([[np.trace(a_.conj().T @ b_) for b_ in mats] for a_ in mats])) / 9
out["81_classes_trace_orthonormal"] = bool(np.allclose(Gm, np.eye(81), atol=1e-9))
out["each_is_unitary_on_sector"] = all(np.allclose(m.conj().T @ m, np.eye(9)) for m in mats)
# the triangle: the TL generator R_i = A + (sqrt 3 / A) Pi_i, with Pi_i an eigenprojector of the neighbouring bilinear M(a_i), acts on monomials by the Fox rule
A_ = np.exp(5j * np.pi / 12)
def fox_inv(c, s_):
    c = list(c); i = s_ - 1; a_, b_ = c[i], c[i + 1]; c[i], c[i + 1] = (2 * a_ - b_) % 3, a_; return tuple(c)
tri = {}
Rs = {}
for s_ in range(1, 6):
    h = B0.conj().T @ M(a[s_]) @ B0
    assert np.allclose(np.linalg.matrix_power(h, 3), np.linalg.matrix_power(h, 3)[0, 0] * np.eye(9))
    root = np.linalg.matrix_power(h, 3)[0, 0] ** (1 / 3)
    results = []
    for k in range(3):
        lam = root * w3 ** k; Pi = sum(np.linalg.matrix_power(h / lam, m) for m in range(3)) / 3
        assert np.allclose(Pi @ Pi, Pi) and abs(np.trace(Pi) - 3) < 1e-8
        R = A_ * np.eye(9) + (np.sqrt(3) / A_) * Pi; Rs[(s_, k)] = (R, Pi)
        def agrees(rule):
            for c in cls[::2]:
                x = R @ (B0.conj().T @ M(c) @ B0) @ R.conj().T; y = B0.conj().T @ M(rule(c, s_)) @ B0
                if abs(abs(np.trace(y.conj().T @ x)) / 9 - 1) > 1e-9: return False
            return True
        results.append(("fox" if agrees(fox) else "") + ("inverse" if agrees(fox_inv) else ""))
    tri[s_] = results
out["TL_generator_acts_on_monomials_by"] = tri
tl_ok = all(np.allclose(Rs[(s_, 0)][1] @ Rs[(s_ + 1, 0)][1] @ Rs[(s_, 0)][1], Rs[(s_, 0)][1] / 3) for s_ in range(1, 5))
out["neighbouring_bilinear_eigenprojectors_satisfy_TL"] = bool(tl_ok)
print(json.dumps(out, default=str))
json.dump(out, open("parafermion_w33.json", "w"), indent=1, default=str)
