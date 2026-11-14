"""Pass 12663: an EXACT certificate for  F(v) >= (11/250) |v|^4  for the F_4 regulus set (type B, four qubits).
Input: the interior floating solution of w33_typeB_degree6_margin.py (Gram blocks K0 51x51, G0 136x136, delta0 = 0.044 = 11/250).
Structure used: the coefficient equations of the Pauli-reduced degree-6 SOS (w33_typeB_degree6_sos.py) split the 51^2 + 136^2 Gram
entries into 2,601 DISJOINT groups, each constrained only through the sum of its entries (every column of the constraint matrix has
16 identical-support rows; verified here).  Hence:
 1. round K0, G0 to Gaussian rationals with denominator 2^40 (Hermitian);
 2. for each group add (exact deficit)/(group size) to every entry -> all 41,616 coefficient equations hold EXACTLY (checked in
    Fraction arithmetic, real and imaginary parts);  the right-hand side is exact: 256 cF is an integer vector, delta0 = 11/250;
 3. positivity in exact integer arithmetic without LDL growth: with R ~ L^{-1} (floating Cholesky inverse, rounded to denominator
    2^30), verify that E = R G R^* - I has every absolute row sum < 1 (using |z| <= |Re z| + |Im z|), so R G R^* is Hermitian,
    strictly diagonally dominant with positive diagonal, hence positive definite, hence G is positive definite.
Output: data/w33_typeB_exact_certificate.json (hashes, margins) and the exact Gram matrices as integer numerators (npz).
usage: py -3 analysis/w33_typeB_exact_certificate.py"""
import hashlib, json, os, time
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_typeB_degree6_sos.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_typeB_degree6_sos.py")}
exec(src[: src.index("def solve(")], g)
MK, MG, cN, nK, nG = g["MK"].tocsr(), g["MG"].tocsr(), g["cN"], g["nK"], g["nG"]
t0 = time.time()
cF = g["coefF"](g["bases"]([0, 1, 2, 3]))
c256 = np.round(cF * 256).astype(np.int64); assert np.abs(cF * 256 - c256).max() < 1e-7
cNi = np.round(cN).astype(np.int64); assert np.abs(cN - cNi).max() < 1e-12
DELTA = Fr(11, 250)
rhs = [Fr(int(a), 256) - DELTA * int(b) for a, b in zip(c256, cNi)]
# groups: rows -> support (columns of K block then G block)
nrow = MK.shape[0]; groups = {}; row_group = []
for r in range(nrow):
    key = (tuple(MK.indices[MK.indptr[r]: MK.indptr[r + 1]]), tuple(MG.indices[MG.indptr[r]: MG.indptr[r + 1]]))
    if key not in groups: groups[key] = [r]
    else: groups[key].append(r)
assert len(groups) == nK * nK
seenK = np.zeros(nK * nK, int); seenG = np.zeros(nG * nG, int)
for (ck, cg), rows in groups.items():
    seenK[list(ck)] += 1; seenG[list(cg)] += 1
    assert len({rhs[r] for r in rows}) == 1  # the identical-support rows carry identical right-hand sides
assert (seenK == 1).all() and (seenG == 1).all()
assert (MK.data == 1).all() and (MG.data == 1).all()
sol = np.load(os.path.join(ROOT, "data", "w33_typeB_degree6_margin_solution.npz")); K = sol["K0"]; G = sol["G0"]
D = 1 << 40
def rnd(M):
    M = (M + M.conj().T) / 2
    re = [[Fr(int(round(M[i, j].real * D)), D) for j in range(len(M))] for i in range(len(M))]
    im = [[Fr(int(round(M[i, j].imag * D)), D) for j in range(len(M))] for i in range(len(M))]
    n = len(M)
    for i in range(n):
        im[i][i] = Fr(0)
        for j in range(i):
            re[i][j] = re[j][i]; im[i][j] = -im[j][i]
    return re, im
Kre, Kim = rnd(K); Gre, Gim = rnd(G)
get = lambda M, n, c: M[c // n][c % n]
max_def = Fr(0)
for (ck, cg), rows in groups.items():
    size = len(ck) + len(cg)
    sr = sum(get(Kre, nK, c) for c in ck) + sum(get(Gre, nG, c) for c in cg)
    si = sum(get(Kim, nK, c) for c in ck) + sum(get(Gim, nG, c) for c in cg)
    dr = (rhs[rows[0]] - sr) / size; di = (Fr(0) - si) / size
    max_def = max(max_def, abs(dr), abs(di))
    for c in ck: Kre[c // nK][c % nK] += dr; Kim[c // nK][c % nK] += di
    for c in cg: Gre[c // nG][c % nG] += dr; Gim[c // nG][c % nG] += di
# exact verification of every equation and of Hermitian symmetry
for (ck, cg), rows in groups.items():
    sr = sum(get(Kre, nK, c) for c in ck) + sum(get(Gre, nG, c) for c in cg)
    si = sum(get(Kim, nK, c) for c in ck) + sum(get(Gim, nG, c) for c in cg)
    assert sr == rhs[rows[0]] and si == 0
herm = all(Kre[i][j] == Kre[j][i] and Kim[i][j] == -Kim[j][i] for i in range(nK) for j in range(nK)) and \
       all(Gre[i][j] == Gre[j][i] and Gim[i][j] == -Gim[j][i] for i in range(nG) for j in range(nG))
print("equations exact:", True, "| Hermitian exact:", herm, "| max correction", float(max_def), round(time.time() - t0), "s", flush=True)
assert herm
# exact positivity by preconditioned diagonal dominance
def posdef(re, im, n):
    A = np.array([[float(re[i][j]) + 1j * float(im[i][j]) for j in range(n)] for i in range(n)])
    L = np.linalg.cholesky(A); Rf = np.linalg.inv(L)
    S = 1 << 30
    Rr = [[int(round(Rf[i, j].real * S)) for j in range(n)] for i in range(n)]; Ri = [[int(round(Rf[i, j].imag * S)) for j in range(n)] for i in range(n)]
    den = max(x.denominator for row in re for x in row); den = max(den, max(x.denominator for row in im for x in row))
    # common denominator: lcm of all denominators (they are of the form 2^a * small); use lcm
    from math import lcm
    den = 1
    for row in re + im:
        for x in row: den = lcm(den, x.denominator)
    Ar = np.array([[int(x * den) for x in row] for row in re], dtype=object); Ai = np.array([[int(x * den) for x in row] for row in im], dtype=object)
    Rr = np.array(Rr, dtype=object); Ri = np.array(Ri, dtype=object)
    # T = R A  (complex) ; P = T R^*   ;  R^* = (Rr^T - i Ri^T)
    Tr_ = Rr.dot(Ar) - Ri.dot(Ai); Ti = Rr.dot(Ai) + Ri.dot(Ar)
    Pr = Tr_.dot(Rr.T) + Ti.dot(Ri.T); Pi = Ti.dot(Rr.T) - Tr_.dot(Ri.T)
    scale = den * S * S  # P / scale = R A R^*
    worst = Fr(0)
    for i in range(n):
        s = Fr(0)
        for j in range(n):
            er = Fr(int(Pr[i, j]), scale) - (1 if i == j else 0); ei = Fr(int(Pi[i, j]), scale)
            s += abs(er) + abs(ei)
        worst = max(worst, s)
    return worst, float(np.linalg.eigvalsh(A)[0]), den
wK, eK, denK = posdef(Kre, Kim, nK); print("K block: max abs row sum of R K R^* - I =", float(wK), "min eig (float)", eK, round(time.time() - t0), "s", flush=True)
wG, eG, denG = posdef(Gre, Gim, nG); print("G block: max abs row sum of R G R^* - I =", float(wG), "min eig (float)", eG, round(time.time() - t0), "s", flush=True)
h = hashlib.sha256()
for M in (Kre, Kim, Gre, Gim):
    for row in M:
        for x in row: h.update(f"{x.numerator}/{x.denominator};".encode())
res = dict(delta="11/250", n_groups=len(groups), n_equations=int(nrow), equations_exact=True, hermitian_exact=bool(herm),
           max_group_correction=float(max_def), K_row_sum_bound=float(wK), G_row_sum_bound=float(wG), K_min_eig_float=eK, G_min_eig_float=eG,
           positive_definite_exact=bool(wK < 1 and wG < 1), certificate_sha256=h.hexdigest(), common_denominators=[str(denK), str(denG)],
           seconds=round(time.time() - t0, 1))
print(res, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_typeB_exact_certificate.json"), "w"), indent=1)
from math import lcm
np.savez_compressed(os.path.join(ROOT, "data", "w33_typeB_exact_certificate_gram.npz"),
                    K_re=np.array([[str(x) for x in r] for r in Kre]), K_im=np.array([[str(x) for x in r] for r in Kim]),
                    G_re=np.array([[str(x) for x in r] for r in Gre]), G_im=np.array([[str(x) for x in r] for r in Gim]))
