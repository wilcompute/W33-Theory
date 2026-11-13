"""Pass 12656: the uncovered Paulis of a minimal three-qubit unextendible Pauli MUB set and the E6(6) cubic.
Conjecture tested here (suggested by Lemmas A, B of Pass 12649: 15 cosets {b, b+p0} with exactly one uncovered member, 6 uncovered
pairs {a, a+p0}): for a three-qubit maximal five-set with covered set C (35 points) and uncovered set U (28 points),
  (1) there is a point p0 in U such that U \ {p0} is an ELLIPTIC QUADRIC Q^-(5,2) of the symplectic space F_2^6 (27 points; its
      totally singular lines form GQ(2,4) = the 27 lines / 45 tritangent planes), equivalently C = (non-singular points) \ {p0}:
      the five Lagrangians partition 35 of the 36 non-singular points;
  (2) with Hermitian Paulis P_v, the cubic  N_P(x) = Tr[(sum_{v in quadric} x_v P_v)^3] / 48  has exactly the 45 line monomials
      with signs s = P_u P_v P_{u+v} = +-1, and this sign class is THE E6 class (adjoint identity (x#)# = N x; 78-dim stabiliser).
      [Physics: the 27 quadric Paulis span the traceless quaternionic-Hermitian 8x8 matrices, the 27 of USp(8); Tr Z^3 is the
      Ferrara-Gunaydin form of the E6(6) cubic in the central-charge basis.  Levay-Saniga-Vrana-Pracna, PRD 79 084036 (2009), label
      GQ(2,4) by three-qubit Paulis for the same entropy formula; cited as prior art for the labelling.]
  (3) consequently Sigma_U(psi) = <P0>^2 + sum_{27} <P_v>^2 = <P0>^2 + |Z(psi)|^2, Z = (<P_v>) in the 27.
Checks: fit a quadratic form over F_2 for every p0 in U; elliptic type by point count; exact signs; adjoint identity numerically;
stabiliser dimension; rank/N of the charge vector Z(psi) at the stabiliser minimisers of F and at random states.
Control: for a COMPLETE-type choice (random 28-subset) no quadric fit exists.  usage: py -3 analysis/w33_umub_uncovered_is_e6_cubic.py"""
import itertools, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_selfdual_pauli_lp.py")}
src = open(os.path.join(HERE, "w33_selfdual_pauli_lp.py"), encoding="utf-8").read()
exec(src[: src.index("t0 = time.time()")], g)
n = 3; lags = g["lags_from_codes"](3, [41, 14, 53])
C = set().union(*lags) - {0}; U = sorted(set(range(1, 64)) - C); assert len(C) == 35 and len(U) == 28
bits = lambda v: [(v >> i) & 1 for i in range(6)]
om = lambda a, b: (bin((a & 7) & (b >> 3)).count("1") + bin((a >> 3) & (b & 7)).count("1")) % 2
mons = [(i, j) for i in range(6) for j in range(i, 6)]


def fit_quadric(zero_set):
    """quadratic form Q (no constant/linear beyond x_i^2 = x_i) with Q = 0 exactly on zero_set among the 63 nonzero points"""
    A = np.array([[bits(v)[i] * bits(v)[j] for (i, j) in mons] + [1 if v in zero_set else 0] for v in range(1, 64)], dtype=np.int64)
    # solve A[:, :21] c = 1 - indicator(zero) i.e. Q(v) = 0 on zero_set, 1 elsewhere
    M = A[:, :21].copy(); b = 1 - A[:, 21]
    aug = np.concatenate([M, b.reshape(-1, 1)], 1); r = 0; piv = []
    for c in range(21):
        p = next((i for i in range(r, 63) if aug[i, c]), None)
        if p is None: continue
        aug[[r, p]] = aug[[p, r]]
        for i in range(63):
            if i != r and aug[i, c]: aug[i] ^= aug[r]
        piv.append(c); r += 1
    if aug[r:, -1].any(): return None
    sol = np.zeros(21, dtype=np.int64); sol[piv] = aug[:r, -1]
    return sol


fits = {p: fit_quadric(set(U) - {p}) for p in U}
good = [p for p, f in fits.items() if f is not None]
rng = np.random.default_rng(0)
ctrl = sum(fit_quadric(set(rng.choice(63, 27, replace=False) + 1)) is not None for _ in range(200))
res = dict(n_uncovered=28, p0_candidates=good, control_random_27_subsets_that_are_quadrics=int(ctrl))
print("p0 with U - {p0} a quadric:", good, "| control random fits:", ctrl, flush=True)
assert len(good) == 1
p0 = good[0]; Qc = fits[p0]
Q = lambda v: int(sum(Qc[k] * bits(v)[i] * bits(v)[j] for k, (i, j) in enumerate(mons)) % 2)
quad = sorted(set(U) - {p0}); assert all(Q(v) == 0 for v in quad) and sum(Q(v) == 0 for v in range(1, 64)) == 27
polar_ok = all((Q(u ^ v) + Q(u) + Q(v)) % 2 == om(u, v) for u in range(1, 64) for v in range(1, 64))
res.update(p0=p0, Q_polarises_to_symplectic_form=bool(polar_ok), singular_points=27, Q_of_p0=Q(p0),
           covered_equals_nonsingular_minus_p0=bool(C == {v for v in range(1, 64) if Q(v) == 1} - {p0}))
lines = sorted({tuple(sorted((u, v, u ^ v))) for u, v in itertools.combinations(quad, 2) if (u ^ v) in quad})
res["quadric_lines"] = len(lines); res["all_lines_commuting"] = bool(all(om(u, v) == 0 for (u, v, w) in lines))
print({k: res[k] for k in ("p0", "Q_polarises_to_symplectic_form", "Q_of_p0", "covered_equals_nonsingular_minus_p0", "quadric_lines", "all_lines_commuting")}, flush=True)
# Pauli operators
X1 = np.array([[0, 1], [1, 0]], complex); Z1 = np.diag([1, -1]).astype(complex)
def P(v):
    M = np.eye(1)
    for i in range(n):
        xi, zi = v >> i & 1, v >> (n + i) & 1
        M = np.kron(M, (1j) ** (xi * zi) * np.linalg.matrix_power(X1, xi) @ np.linalg.matrix_power(Z1, zi))
    return M
Ps = {v: P(v) for v in range(1, 64)}
idx = {v: i for i, v in enumerate(quad)}
T = np.zeros((27, 27, 27)); signs = {}
for (u, v, w) in lines:
    s = np.trace(Ps[u] @ Ps[v] @ Ps[w]) / 8; assert abs(s.imag) < 1e-12 and abs(abs(s.real) - 1) < 1e-12
    signs[(idx[u], idx[v], idx[w])] = int(round(s.real))
    for p in set(itertools.permutations((idx[u], idx[v], idx[w]))): T[p] = s.real / 6
# Tr X^3 / 48 equals N
x = rng.standard_normal(27); Xm = sum(x[idx[v]] * Ps[v] for v in quad)
N = np.einsum("ijk,i,j,k->", T, x, x, x)
res["TrX3_over_48_equals_N"] = bool(abs(np.trace(Xm @ Xm @ Xm).real / 48 - N) < 1e-9)
sharp = lambda y: 3 * np.einsum("ijk,j,k->i", T, y, y)
res["adjoint_identity_holds"] = bool(np.allclose(sharp(sharp(x)), N * x, atol=1e-9))
src2 = open(os.path.join(HERE, "w33_e6_cubic_skew_stabilizer_projection.py"), encoding="utf-8").read()
g2 = {"__name__": "x", "__file__": os.path.join(HERE, "w33_e6_cubic_skew_stabilizer_projection.py")}
exec(src2[: src2.index("T = tensor(signs)")], g2)
res["stabiliser_dim"] = int(g2["stabilizer"](T).shape[1])
res["sign_counts"] = {"+1": sum(1 for s in signs.values() if s == 1), "-1": sum(1 for s in signs.values() if s == -1)}
print({k: res[k] for k in ("TrX3_over_48_equals_N", "adjoint_identity_holds", "stabiliser_dim", "sign_counts")}, flush=True)
# charge vector of pure states: Z(psi)_v = <P_v>
def charges(psi): return np.array([np.vdot(psi, Ps[v] @ psi).real for v in quad])
def rank_of(z):
    Nz = np.einsum("ijk,i,j,k->", T, z, z, z); sh = sharp(z)
    return (3 if abs(Nz) > 1e-8 else (2 if np.abs(sh).max() > 1e-8 else (1 if np.abs(z).max() > 1e-8 else 0))), float(Nz), float(z @ z)
rows = []
for _ in range(5):
    psi = rng.standard_normal(8) + 1j * rng.standard_normal(8); psi /= np.linalg.norm(psi)
    r, Nz, z2 = rank_of(charges(psi)); t = np.vdot(psi, Ps[p0] @ psi).real
    rows.append(dict(kind="random", rank=r, N=Nz, Z2=z2, P0=t, SigmaU=z2 + t * t))
# stabiliser minimisers: Lagrangians (as joint eigenstates) meeting C in exactly one point
from numpy.linalg import eigh
allL = []
vs = list(range(1, 64))
for a, b, c in itertools.combinations(vs, 3):
    if om(a, b) or om(a, c) or om(b, c) or (a ^ b) == c: continue
    L = frozenset({a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c}); allL.append(L)
allL = list(set(allL)); assert len(allL) == 135
mstats = {}
for L in allL:
    m = len(L & C)
    gens = sorted(L)[:1]
    # joint eigenstate: project with (1 + P)/2 for three independent generators
    a, b = sorted(L)[0], sorted(L)[1]; c = next(v for v in sorted(L) if v not in (a, b, a ^ b))
    proj = np.eye(8, dtype=complex)
    for v in (a, b, c):
        Pm = Ps[v] if abs(np.trace(Ps[v])) < 1e-9 else Ps[v]
        proj = proj @ (np.eye(8) + Pm) / 2
    w, V = eigh((proj + proj.conj().T) / 2); psi = V[:, -1]
    if abs(np.vdot(psi, proj @ psi)) < 0.5: continue
    z = charges(psi); r, Nz, z2 = rank_of(z); t = np.vdot(psi, Ps[p0] @ psi).real
    key = (m, p0 in L, r, round(Nz, 6), round(z2, 6), round(t * t, 6))
    mstats[key] = mstats.get(key, 0) + 1
res["random_states"] = rows
res["stabiliser_states_by_(meetC,contains_p0,rank,N,Z2,P0sq)"] = [dict(key=list(k), count=v) for k, v in sorted(mstats.items())]
for k, v in sorted(mstats.items()): print("stabiliser:", k, v, flush=True)
print("random:", [(r["rank"], round(r["N"], 4), round(r["SigmaU"], 4)) for r in rows], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_umub_uncovered_is_e6_cubic.json"), "w"), indent=1)
