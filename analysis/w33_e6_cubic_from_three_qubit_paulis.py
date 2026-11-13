"""Pass 12656: the E6(6) cubic as Tr X^3 over the 27 three-qubit Paulis of an elliptic quadric, and pure states as charge vectors.
Setup: Q0(v) = x.z (parity of the number of Y's), a antisymmetric Pauli (Q0(a) = 1), Q(v) = Q0(v) + omega(v, a): an elliptic quadric
Q^-(5,2) with 27 singular points (GQ(2,4): 45 totally singular lines = commuting triples {u, v, u+v}).
Claims tested:
 (a) N_P(x) = Tr[(sum_{Q(v)=0} x_v P_v)^3]/48 = sum over the 45 lines of s_uvw x_u x_v x_w, s = Tr(P_u P_v P_w)/8 = +-1;
 (b) this signed cubic satisfies the adjoint identity and has a 78-dimensional stabiliser: it IS the E6 cubic (by Pass 12655 the
     E6 sign class is unique, so it is the repository's cubic up to relabelling and coordinate signs);
     [prior art: Levay-Saniga-Vrana-Pracna PRD 79, 084036 (2009) label GQ(2,4) with three-qubit Paulis for the D=5 entropy formula;
      Ferrara-Gunaydin: I3 = Tr (Omega Z)^3 in the USp(8) basis.  Here: an executable check on the repository's conventions.]
 (c) every three-qubit stabiliser state has charge vector Z_v = <P_v> supported on exactly one line of the quadric (a triad), hence
     rank 3 with N(Z) = +-1; the sign of N splits the 1080 stabiliser states;
 (d) numerical range of |Z|^2 = sum_27 <P_v>^2 and of N(Z(psi)) over pure states.
Negative recorded: the uncovered set of a minimal three-qubit MUB five-set is NOT 'a point + an elliptic quadric' (no quadratic form
fits U - {p} for any p; neither C nor U is a quadric), although Lemmas A, B of Pass 12649 have the same local counts.
usage: py -3 analysis/w33_e6_cubic_from_three_qubit_paulis.py"""
import itertools, json, os
from collections import Counter
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
n = 3
om = lambda a, b: (bin((a & 7) & (b >> 3)).count("1") + bin((a >> 3) & (b & 7)).count("1")) % 2
Q0 = lambda v: bin((v & 7) & (v >> 3)).count("1") % 2
a0 = 1 | 8  # Y on qubit 0
Q = lambda v: (Q0(v) + om(v, a0)) % 2
quad = [v for v in range(1, 64) if Q(v) == 0]; assert len(quad) == 27
assert all((Q(u ^ v) + Q(u) + Q(v)) % 2 == om(u, v) for u in range(1, 64) for v in range(1, 64))
lines = sorted({tuple(sorted((u, v, u ^ v))) for u, v in itertools.combinations(quad, 2) if (u ^ v) in quad}); assert len(lines) == 45
X1 = np.array([[0, 1], [1, 0]], complex); Z1 = np.diag([1, -1]).astype(complex)
def P(v):
    M = np.eye(1)
    for i in range(n):
        xi, zi = v >> i & 1, v >> (n + i) & 1
        M = np.kron(M, (1j) ** (xi * zi) * np.linalg.matrix_power(X1, xi) @ np.linalg.matrix_power(Z1, zi))
    return M
Ps = {v: P(v) for v in range(1, 64)}; idx = {v: i for i, v in enumerate(quad)}
T = np.zeros((27, 27, 27)); signs = {}
for (u, v, w) in lines:
    s = np.trace(Ps[u] @ Ps[v] @ Ps[w]) / 8; assert abs(s.imag) < 1e-12 and abs(abs(s.real) - 1) < 1e-12
    signs[(idx[u], idx[v], idx[w])] = int(round(s.real))
    for p in set(itertools.permutations((idx[u], idx[v], idx[w]))): T[p] = s.real / 6
rng = np.random.default_rng(0); x = rng.standard_normal(27)
Xm = sum(x[idx[v]] * Ps[v] for v in quad); N = lambda y: float(np.einsum("ijk,i,j,k->", T, y, y, y))
sharp = lambda y: 3 * np.einsum("ijk,j,k->i", T, y, y)
res = dict(n_points=27, n_lines=45, TrX3_over_48_equals_N=bool(abs(np.trace(Xm @ Xm @ Xm).real / 48 - N(x)) < 1e-9),
           adjoint_identity=bool(np.allclose(sharp(sharp(x)), N(x) * x, atol=1e-9)),
           sign_counts=dict(Counter(signs.values())))
src2 = open(os.path.join(HERE, "w33_e6_cubic_skew_stabilizer_projection.py"), encoding="utf-8").read()
g2 = {"__name__": "x", "__file__": os.path.join(HERE, "w33_e6_cubic_skew_stabilizer_projection.py")}
exec(src2[: src2.index("T = tensor(signs)")], g2)
res["stabiliser_dim"] = int(g2["stabilizer"](T).shape[1])
# control: hyperbolic-type set (Q0 = 0: 35 symmetric Paulis) is not this structure; and dropping signs kills E6
T1 = np.abs(T); res["control_unsigned_adjoint_identity"] = bool(np.allclose(3 * np.einsum("ijk,j,k->i", T1, 3 * np.einsum("ijk,j,k->i", T1, x, x), 3 * np.einsum("ijk,j,k->i", T1, x, x)), np.einsum("ijk,i,j,k->", T1, x, x, x) * x, atol=1e-9))
print({k: v for k, v in res.items()}, flush=True)
# (c) stabiliser states
PQ = np.array([Ps[v] for v in quad])
charges = lambda psi: np.einsum("i,kij,j->k", psi.conj(), PQ, psi).real
Ls = set()
for a, b, c in itertools.combinations(range(1, 64), 3):
    if om(a, b) or om(a, c) or om(b, c) or (a ^ b) == c: continue
    Ls.add(frozenset({a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c}))
assert len(Ls) == 135
stab = Counter(); nstates = 0
for L in Ls:
    Ll = sorted(L); a = Ll[0]; b = Ll[1]; c = next(v for v in Ll if v not in (a, b, a ^ b))
    for sa, sb, sc in itertools.product((1, -1), repeat=3):
        proj = (np.eye(8) + sa * Ps[a]) @ (np.eye(8) + sb * Ps[b]) @ (np.eye(8) + sc * Ps[c]) / 8
        w, V = np.linalg.eigh((proj + proj.conj().T) / 2); psi = V[:, -1]; nstates += 1
        z = charges(psi); supp = tuple(sorted(i for i in range(27) if abs(z[i]) > 1e-9))
        stab[(len(supp), supp in signs, round(N(z)))] += 1
res["n_stabiliser_states"] = nstates
res["stabiliser_states_(support,is_line,N)"] = [dict(support=k[0], is_line=bool(k[1]), N=int(k[2]), count=v) for k, v in sorted(stab.items())]
print(res["stabiliser_states_(support,is_line,N)"], flush=True)
# (d) ranges over pure states
def opt(f, sgn, starts=40):
    best = None
    for _ in range(starts):
        r = minimize(lambda w: sgn * f((w[:8] + 1j * w[8:]) / np.linalg.norm(w)), rng.standard_normal(16), method="L-BFGS-B")
        best = r.fun if best is None else min(best, r.fun)
    return sgn * best
Z2 = lambda psi: float((charges(psi) ** 2).sum()); NZ = lambda psi: N(charges(psi))
res["Z2_min"] = opt(Z2, 1); res["Z2_max"] = opt(Z2, -1); res["N_min"] = opt(NZ, 1); res["N_max"] = opt(NZ, -1)
print({k: round(res[k], 6) for k in ("Z2_min", "Z2_max", "N_min", "N_max")}, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_e6_cubic_from_three_qubit_paulis.json"), "w"), indent=1, default=int)
