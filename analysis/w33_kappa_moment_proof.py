"""Pass 12652 item 1: an exact proof of kappa <= 3, hence min F = 1/8 exactly for all 24,192 three-qubit size-5 sets.

kappa = max over unit x, y in C^4 of sum_{j=1}^6 |<x|M_j|y>|^2 (Lemma B of Pass 12649; M_j unitary 4x4 blocks).
For fixed y put V = [M_1 y, ..., M_6 y] (4 x 6).  max_x sum_j |<x|M_j y>|^2 = lambda_max(V V^H) = lambda_max(G), G = V^H V,
G_jk = <y|M_j^H M_k|y>.  G is PSD, rank <= 4, Tr G = 6 (M_j unitary).
KEY FACT (checked exactly below): the 15 products M_j^H M_k (j < k) are, up to phase, the 15 non-identity elements of an orthogonal
unitary basis of M_4 (with I they are pairwise Hilbert-Schmidt orthogonal).  For any orthogonal unitary basis {U_g} of M_d,
sum_g |<y|U_g|y>|^2 = d|y|^4, so sum_{j<k} |G_jk|^2 = 4 - 1 = 3 and Tr G^2 = 6 + 2*3 = 12, for EVERY unit y.
Moment bound: nonzero eigenvalues l_1 >= ... >= l_4 >= 0 with sum 6 and sum of squares 12.  Cauchy-Schwarz on l_2..l_4:
(6 - l_1)^2 <= 3 (12 - l_1^2)  <=>  4 l_1 (l_1 - 3) <= 0  <=>  l_1 <= 3.  QED; equality iff spectrum (3, 1, 1, 1, 0, 0).
Combinatorially: {0, a_1, ..., a_5} is a 6-subset of F_2^4 whose 15 pairwise sums are the 15 non-zero vectors (a hyperoval-type /
Sidon set); a pentagon anticommutation graph forces this (the only linear relation is sum a_i = 0).
usage: py -3 analysis/w33_kappa_moment_proof.py"""
import json, os, contextlib, io, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_threequbit_analytic_one_eighth.py")}
src = open(os.path.join(HERE, "w33_threequbit_analytic_one_eighth.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("# kappa numerically")], g)
Ms, nu, lemA, lemB = g["Ms"], g["nu"], g["res"]["lemmaA_bijection"], g["res"]["lemmaB_six_pairs"]
res = dict(lemmaA_bijection=bool(lemA), lemmaB_six_pairs=bool(lemB), nu=int(nu))
# exact arithmetic: Ms are Gaussian-integer matrices with M M^H = nu^2 I (Mo = M / nu unitary)
def gi(M):
    R = np.round(M.real).astype(np.int64); I_ = np.round(M.imag).astype(np.int64)
    assert np.abs(M - (R + 1j * I_)).max() < 1e-9; return R, I_
E = [gi(M) for M in Ms]
def mul(A, B):  # (Ar + i Ai)(Br + i Bi), exact int64
    return A[0] @ B[0] - A[1] @ B[1], A[0] @ B[1] + A[1] @ B[0]
def adj(A): return A[0].T, -A[1].T
def tr(A): return int(np.trace(A[0])), int(np.trace(A[1]))
unitary = all(np.array_equal(mul(A, adj(A))[0], nu * nu * np.eye(4, dtype=np.int64)) and not mul(A, adj(A))[1].any() for A in E)
prods = [((-1, -1), (nu * nu * np.eye(4, dtype=np.int64), np.zeros((4, 4), dtype=np.int64)))]  # nu^2 * identity
prods += [((j, k), mul(adj(E[j]), E[k])) for j, k in itertools.combinations(range(6), 2)]
# every product is nu^2 * (unitary): check P P^H = nu^4 I exactly
prod_unitary = all(np.array_equal(mul(P, adj(P))[0], nu ** 4 * np.eye(4, dtype=np.int64)) and not mul(P, adj(P))[1].any() for _, P in prods)
gram = [[tr(mul(adj(P), Q)) for _, Q in prods] for _, P in prods]  # Tr(P^H Q), exact Gaussian integers
offdiag_zero = all(gram[a][b] == (0, 0) for a in range(16) for b in range(16) if a != b)
diag = sorted({gram[a][a] for a in range(16)})
res.update(blocks_unitary=bool(unitary), products_unitary=bool(prod_unitary), sixteen_products_HS_orthogonal=bool(offdiag_zero),
           HS_norms=[list(d) for d in diag])
# sanity: Tr G = 6 and Tr G^2 = 12 for random y; lambda_max <= 3 with equality approached by the optimiser
Mo = [M / nu for M in Ms]
rng = np.random.default_rng(7); tg, tg2, lmax = [], [], []
for _ in range(2000):
    y = rng.standard_normal(4) + 1j * rng.standard_normal(4); y /= np.linalg.norm(y)
    V = np.array([M @ y for M in Mo]).T; G = V.conj().T @ V
    tg.append(np.trace(G).real); tg2.append(np.trace(G @ G).real); lmax.append(np.linalg.eigvalsh(G)[-1])
res.update(trG_range=[float(min(tg)), float(max(tg))], trG2_range=[float(min(tg2)), float(max(tg2))], random_lambda_max=float(max(lmax)))
# equality spectrum at a maximiser: alternate x <- top eigvec, y <- top eigvec
best = 0
for s in range(50):
    y = rng.standard_normal(4) + 1j * rng.standard_normal(4); y /= np.linalg.norm(y)
    for _ in range(400):
        A = sum(np.outer(M @ y, (M @ y).conj()) for M in Mo); x = np.linalg.eigh(A)[1][:, -1]
        B = sum(np.outer(M.conj().T @ x, (M.conj().T @ x).conj()) for M in Mo); y = np.linalg.eigh(B)[1][:, -1]
    V = np.array([M @ y for M in Mo]).T; ev = np.linalg.eigvalsh(V.conj().T @ V)
    if ev[-1] > best: best, spec = ev[-1], ev
res.update(kappa_alternating=float(best), spectrum_at_max=[round(float(v), 9) for v in spec[::-1]])
# the moment bound as a function: general r = rank bound, s = trace, q = Tr G^2
r, s, q = 4, 6, 12
res["moment_bound"] = (s + np.sqrt((r - 1) * (r * q - s * s))) / r
res["proved"] = bool(unitary and prod_unitary and offdiag_zero and lemA and lemB)
print(json.dumps(res, indent=1))
json.dump(res, open(os.path.join(ROOT, "data", "w33_kappa_moment_proof.json"), "w"), indent=1)
