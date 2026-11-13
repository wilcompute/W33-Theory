"""Pass 12655: the k-copy (symmetric-extension / de Finetti) hierarchy for Sigma_U = sum_{P in U} <P>^2.
For pure psi, Sigma_U = <psi^{(x)k}| Q_12 (x) 1 |psi^{(x)k}> with Q = sum_U P (x) P, and psi^{(x)k} lies in Sym^k(C^d).  Hence
    Sigma_U <= B_k := lambda_max( Pi_k (Q_12 (x) 1) Pi_k )   on Sym^k,       B_2 >= B_3 >= ... -> max Sigma_U  (k -> infinity).
B_2 is the swap/Bell bound of Pass 12652 (12 at n = 3, 40 at n = 5: useless).  This computes B_k by Lanczos on (C^d)^{(x)k} with an
explicit symmetriser (Paulis act as signed permutations).  B_k is exactly the degree-2k SOS bound with multiplier |psi|^{2(k-2)}.
Cases: three-qubit five-set (truth 6), k = 2..5; four-qubit types A (14.162), B (14), k = 2, 3; five-qubit 9-set (30), k = 2, 3.
Control: U = all Paulis gives d - 1 at every k (purity); B_2 must reproduce Pass 12652 (12, 40).
usage: py -3 analysis/w33_kcopy_symmetric_bound.py"""
import itertools, json, os, time
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_selfdual_pauli_lp.py")}
src = open(os.path.join(HERE, "w33_selfdual_pauli_lp.py"), encoding="utf-8").read()
exec(src[: src.index("t0 = time.time()")], g)
lags_from_codes = g["lags_from_codes"]


def pauli_action(n, v):
    """P_v |b> = phase(b) |b xor x>, with P = prod_i i^{x_i z_i} X^{x_i} Z^{z_i} (qubit i = bit i)."""
    x, z = v & ((1 << n) - 1), v >> n
    b = np.arange(1 << n)
    ph = (1j) ** bin(x & z).count("1") * (1 - 2 * (np.array([bin(int(t)).count("1") for t in (b & z)]) % 2))
    return b ^ x, ph  # new index for each b, and the amplitude: (P psi)[b ^ x] = ph[b] psi[b]


def bound(n, U, k, tol=1e-9):
    d = 1 << n; acts = [pauli_action(n, v) for v in U]
    perms = list(itertools.permutations(range(k)))
    shape = (d,) * k

    def sym(T):
        out = np.zeros_like(T)
        for p in perms: out += T.transpose(p)
        return out / len(perms)

    def Q12(T):
        out = np.zeros_like(T)
        for tgt, ph in acts:
            inv = np.empty(d, dtype=np.int64); inv[tgt] = np.arange(d)  # (P psi)[c] = ph[inv[c]] psi[inv[c]]
            A = T[inv] * ph[inv].reshape((d,) + (1,) * (k - 1))
            A = A[:, inv] * ph[inv].reshape((1, d) + (1,) * (k - 2))
            out += A
        return out

    def mv(vv):
        T = sym(vv.reshape(shape).astype(complex))
        return sym(Q12(T)).reshape(-1)
    L = LinearOperator((d ** k, d ** k), matvec=mv, dtype=complex)
    rng = np.random.default_rng(0); v0 = sym((rng.standard_normal(shape) + 1j * rng.standard_normal(shape))).reshape(-1)
    val = eigsh(L, k=1, which="LA", v0=v0, tol=tol, maxiter=4000)[0][0]
    return float(val)


def uncovered(n, lags):
    d = 1 << n; C = set().union(*lags) - {0}
    return sorted(set(range(1, d * d)) - C)


t0 = time.time(); res = dict(controls={}, cases=[])
for n, k in ((2, 2), (2, 3), (3, 3)):
    res["controls"][f"all_n{n}_k{k}"] = bound(n, list(range(1, 4 ** n)), k)
    assert abs(res["controls"][f"all_n{n}_k{k}"] - (2 ** n - 1)) < 1e-6
print("purity controls", res["controls"], flush=True)
U3 = uncovered(3, lags_from_codes(3, [41, 14, 53]))
for k in (2, 3, 4, 5):
    b = bound(3, U3, k); res["cases"].append(dict(n=3, name="three-qubit five-set", truth=6.0, k=k, B=b)); print(res["cases"][-1], round(time.time() - t0), "s", flush=True)
assert abs(res["cases"][0]["B"] - 12) < 1e-6
ex4 = {"__name__": "x", "__file__": os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py")}
src4 = open(os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py"), encoding="utf-8").read()
exec(src4[: src4.index("def decide")], ex4)
lags4, _ = ex4["lagrangians"](4)
census = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_size5_census.json")))
for name, t, truth in zip(("four-qubit type A", "four-qubit type B"), census["types"], (14.1622, 14.0)):
    U = uncovered(4, [frozenset(lags4[i]) | {0} for i in t["example"]])
    for k in (2, 3):
        b = bound(4, U, k); res["cases"].append(dict(n=4, name=name, truth=truth, k=k, B=b)); print(res["cases"][-1], round(time.time() - t0), "s", flush=True)
U5 = uncovered(5, lags_from_codes(5, json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_size9_verify.json")))["example"]))
for k in (2, 3):
    b = bound(5, U5, k, tol=1e-7); res["cases"].append(dict(n=5, name="five-qubit 9-set", truth=30.0, k=k, B=b)); print(res["cases"][-1], round(time.time() - t0), "s", flush=True)
for c in res["cases"]: assert c["B"] >= c["truth"] - 1e-5
res["seconds"] = round(time.time() - t0, 1)
json.dump(res, open(os.path.join(ROOT, "data", "w33_kcopy_symmetric_bound.json"), "w"), indent=1)
