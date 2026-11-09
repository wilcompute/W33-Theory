"""Item 4: a stronger certificate for three qubits.  Hermitian SOS (charge +-2 terms |q(v)|^2, q in Sym^2) fails (-5/8, and -0.164 at degrees
6 and 8).  For a U(1)-invariant quartic, a general real SOS averaged over the phase splits by charge: charge +-2 terms (Hermitian SOS) PLUS
charge-0 terms (v^dag C v)^2 with C Hermitian.  As (2,2)-forms on Sym^2:
    H_F - delta P = H2 + P (sum_ab Q_ab B_a (x) B_b) P,   H2 >= 0 (on Sym^2),  Q >= 0 (real, on the d^2-dim space of Hermitian matrices, basis B_a)
Maximise delta (cvxpy / Clarabel).  delta > 0 certifies F > 0 for v != 0 (strong unextendibility).
Controls: the two-qutrit pentad (expect >= 1/9); 4 bases of a complete spread (must be <= 0).
usage: py -3 analysis/w33_real_sos_threequbit.py"""
import itertools, json, os
import numpy as np, cvxpy as cp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
exec(_src[: _src.index("\nres = {}")], cs)
geometry, bases_for, maximal_partial_spreads = cs["geometry"], cs["bases_for"], cs["maximal_partial_spreads"]
def herm_basis(d):
    B = []
    for i in range(d):
        M = np.zeros((d, d), complex); M[i, i] = 1; B.append(M)
    for i in range(d):
        for j in range(i + 1, d):
            M = np.zeros((d, d), complex); M[i, j] = M[j, i] = 1 / np.sqrt(2); B.append(M)
            M = np.zeros((d, d), complex); M[i, j] = -1j / np.sqrt(2); M[j, i] = 1j / np.sqrt(2); B.append(M)
    return B
def sym2(d):
    cols = []
    for i in range(d):
        for j in range(i, d):
            v = np.zeros(d * d)
            if i == j: v[i * d + i] = 1
            else: v[i * d + j] = v[j * d + i] = 1 / np.sqrt(2)
            cols.append(v)
    return np.array(cols).T
def real_sos_delta(E, d):
    S = sym2(d); m = S.shape[1]
    HF = np.zeros((m, m), complex)
    for e in E:
        A = np.outer(e, e.conj()) - np.eye(d) / d
        HF += S.T @ np.kron(A, A) @ S
    HF = (HF + HF.conj().T) / 2
    Bh = herm_basis(d); nb = len(Bh)
    # T[a,b] = S^T (B_a (x) B_b) S, symmetrised in (a,b) since Q symmetric
    Tab = {}
    for a in range(nb):
        for b in range(a, nb):
            T = S.T @ (np.kron(Bh[a], Bh[b]) + np.kron(Bh[b], Bh[a])) @ S / (2 if a != b else 2)
            Tab[(a, b)] = (T + T.conj().T) / 2
    Q = cp.Variable((nb, nb), symmetric=True)
    H2r = cp.Variable((m, m), symmetric=True); H2i = cp.Variable((m, m))
    delta = cp.Variable()
    # complex Hermitian PSD via real embedding [[Re, -Im], [Im, Re]]
    cons = [Q >> 0, cp.bmat([[H2r, -H2i], [H2i, H2r]]) >> 0, H2i == -H2i.T]
    expr_r = 0; expr_i = 0
    for (a, b), T in Tab.items():
        coef = Q[a, b] * (1 if a == b else 2)
        expr_r = expr_r + coef * T.real
        expr_i = expr_i + coef * T.imag
    cons += [HF.real - delta * np.eye(m) == H2r + expr_r, HF.imag == H2i + expr_i]
    prob = cp.Problem(cp.Maximize(delta), cons)
    prob.solve(solver=cp.CLARABEL)
    return float(delta.value), prob.status
res = {}
pts9, lag9, w9 = geometry(3, 2); B9 = bases_for(3, 2, pts9, lag9)
mps9, _ = maximal_partial_spreads(lag9)
pent = sorted(next(S for S in mps9 if len(S) == 5)); spread = sorted(next(S for S in mps9 if len(S) == 10))
res["control_d9_pentad"] = real_sos_delta([b for L in pent for b in B9[L].T], 9)
print("control two-qutrit pentad: real-SOS delta = %.6f (Hermitian 1/9)" % res["control_d9_pentad"][0], res["control_d9_pentad"][1], flush=True)
res["control_d9_spread4"] = real_sos_delta([b for L in spread[:4] for b in B9[L].T], 9)
print("control 4 spread bases: delta = %.6f" % res["control_d9_spread4"][0], flush=True)
pts8, lag8, w8 = geometry(2, 3); B8 = bases_for(2, 3, pts8, lag8)
mps8, _ = maximal_partial_spreads(lag8)
five = sorted(next(S for S in mps8 if len(S) == 5))
res["three_qubit_size5"] = real_sos_delta([b for L in five for b in B8[L].T], 8)
print("three qubits size 5: real-SOS delta = %.6f  (numerical sphere min 1/8; Hermitian -5/8)" % res["three_qubit_size5"][0], res["three_qubit_size5"][1], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_real_sos_threequbit.json"), "w"), indent=1)
