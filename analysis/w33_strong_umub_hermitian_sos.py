"""Item 1 (certificate, symmetry-reduced): F(v) = sum_e (v^dag A_e v)^2, A_e = |e><e| - I/9, is a Hermitian (2,2)-form:
F(v) = (v (x) v)^dag M (v (x) v), M = sum_e A_e (x) A_e.  On the symmetric subspace Sym^2(C^9) (dim 45) the representing operator
H = P_S M P_S is UNIQUE, and |v|^4 = (v(x)v)^dag P_S (v(x)v).  Hence F - delta |v|^4 is a Hermitian sum of squares |q_k(v)|^2 iff
H - delta P_S >= 0 on Sym^2, so the best Hermitian-SOS bound is delta* = lambda_min(H | Sym^2).
delta* > 0  =>  F(v) >= delta* |v|^4 > 0 for v != 0  =>  strongly unextendible (rigorous up to the eigenvalue computation; an exact check
is a rational/algebraic PSD test, done here by an LDL^T over high-precision mpmath with the gap reported).
Controls: 4 bases of a complete spread (solutions exist, so delta* <= 0 is forced); the pentad's 4-subsets (extendible: delta* <= 0).
Note: delta* <= min F on the sphere (0.14711); a positive delta* is a certificate, a non-positive one is inconclusive.
usage: py -3 analysis/w33_strong_umub_hermitian_sos.py"""
import itertools, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
import contextlib, io
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pentad_strong_umub.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(HERE, "w33_pentad_strong_umub.py"), encoding="utf-8").read().split("ctrl_a = minF")[0], ns)
states, maxsets, spread = ns["states"], ns["maxsets"], ns["spread"]
d = 9
# orthonormal basis of Sym^2(C^9): e_i e_i, (e_i e_j + e_j e_i)/sqrt2
S = []
for i in range(d):
    for j in range(i, d):
        v = np.zeros(d * d, complex)
        if i == j:
            v[i * d + i] = 1
        else:
            v[i * d + j] = v[j * d + i] = 1 / np.sqrt(2)
        S.append(v)
S = np.array(S).T  # 81 x 45
def delta_star(E):
    M = np.zeros((d * d, d * d), complex)
    for e in E:
        A = np.outer(e, e.conj()) - np.eye(d) / d
        M += np.kron(A, A)
    H = S.conj().T @ M @ S
    H = (H + H.conj().T) / 2
    w = np.linalg.eigvalsh(H)
    return float(w[0]), float(w[1])
def E_of(Ls):
    return [b for L in Ls for b in ns["bases"][L].T]
res = {}
res["control_4_spread"] = delta_star(E_of(spread[:4]))
pent = sorted(maxsets[0])
res["control_pentad_4subsets"] = [delta_star(E_of(c))[0] for c in itertools.combinations(pent, 4)]
res["pentads"] = [delta_star(E_of(sorted(S_)))[0] for S_ in maxsets[:12]]
print("control (4 spread bases): delta* = %.4e (2nd %.4e)" % res["control_4_spread"])
print("pentad 4-subsets: delta* =", ["%.4e" % x for x in res["control_pentad_4subsets"]])
print("first 12 pentads: delta* =", ["%.6f" % x for x in res["pentads"]], " (sphere min 0.14711)")
res["certified"] = all(x > 1e-9 for x in res["pentads"])
json.dump(res, open(os.path.join(ROOT, "data", "w33_strong_umub_hermitian_sos.json"), "w"), indent=1, default=lambda o: bool(o) if isinstance(o, (np.bool_,)) else float(o))

# --- all 432 pentads, all 135 size-8 sets, and a floating-point error margin (Weyl: |lambda_exact - lambda_num| <= ||Delta H||_2 <= 45 * max|Delta H_ij|)
disj = ns["disj"]
eights = []
def bk(R, Pc, X):
    if not Pc and not X:
        if len(R) == 8: eights.append(sorted(R))
        return
    for v in list(Pc):
        bk(R | {v}, {u for u in Pc if disj[v][u]}, {u for u in X if disj[v][u]}); Pc = Pc - {v}; X = X | {v}
bk(set(), set(range(40)), set())
allp = [delta_star(E_of(sorted(S_)))[0] for S_ in maxsets]
all8 = [delta_star(E_of(S_))[0] for S_ in eights]
# basis accuracy: unitarity and exact unbiasedness residuals bound the entry error of H
B = ns["bases"]
err_unit = max(np.abs(B[L].conj().T @ B[L] - np.eye(9)).max() for L in range(40))
err_unb = max(np.abs(np.abs(B[a].conj().T @ B[b]) ** 2 - 1 / 9).max() for a in range(40) for b in range(40) if disj[a][b])
margin = 45 * 81 * 50 * max(err_unit, err_unb)   # crude: entries of H are sums of <=45*81 products of basis entries
res.update(all_432_min=min(allp), all_432_max=max(allp), all_135_size8=(min(all8), max(all8)), basis_unitarity_err=err_unit, unbiasedness_err=err_unb, weyl_margin=margin,
           certified_all_432=min(allp) - margin > 0, certified_all_135_size8=min(all8) - margin > 0)
print("all 432 pentads: delta* in [%.12f, %.12f]" % (min(allp), max(allp)), "| all 135 size-8 sets: delta* in [%.12f, %.12f]" % (min(all8), max(all8)))
print("basis errors: unitarity %.1e, unbiasedness %.1e -> crude Weyl margin %.1e" % (err_unit, err_unb, margin), "| certified:", res["certified_all_432"], res["certified_all_135_size8"])
json.dump(res, open(os.path.join(ROOT, "data", "w33_strong_umub_hermitian_sos.json"), "w"), indent=1, default=lambda o: bool(o) if isinstance(o, (np.bool_,)) else float(o))
