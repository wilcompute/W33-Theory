"""Pass 12653: a linear-programming bound for min F of Pauli MUB sets from the SELF-DUALITY of pure-state Pauli spectra.
For pure psi on n qubits, m_b = <P_b>^2 satisfies (exact identity, Sum_b Tr[P_b rho] Tr[P_b P_a rho P_a] = d Tr[rho P_a rho P_a]):
    m_0 = 1,  m_b >= 0,  sum_b (-1)^{omega(a,b)} m_b = d m_a  for all a       (self-dual under the symplectic Fourier transform).
Relaxation (Delsarte / Rains style):  Sigma_U <= LP(U) := max sum_{b in U} m_b subject to the above (+ optional clique cuts
m_a + m_b + m_c <= 1 on anticommuting triples).  min F >= (d - 1 - LP)/d.  LP = d - 2 certifies min F = 1/d EXACTLY (rational LP).
Cases: n = 3 five-set (truth 6), n = 4 types A (truth 14.162) / B (truth 14) and nine-sets (14), n = 5 size-9 (numerical 30),
n = 6 size-9 (numerical 62).  Controls: (i) random pure states satisfy the constraints (identity check); (ii) LP >= the numerical
maximum in every case (a valid relaxation can never be below it).  usage: py -3 analysis/w33_selfdual_pauli_lp.py"""
import json, os, time, itertools
import numpy as np
import scipy.sparse as sps
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
pc = np.vectorize(lambda v: bin(int(v)).count("1"))


def omega_matrix(n):
    N = 1 << (2 * n); v = np.arange(N); lo = (1 << n) - 1
    return (pc(np.bitwise_and.outer(v & lo, v >> n)) + pc(np.bitwise_and.outer(v >> n, v & lo))) % 2


def lp_bound(n, Uset, cliques=False, Om=None):
    d = 1 << n; N = d * d
    Om = omega_matrix(n) if Om is None else Om
    H = 1 - 2 * Om  # (+-1) Fourier kernel
    A_eq = H - d * np.eye(N)
    A_eq = np.vstack([A_eq, np.eye(N)[0]]); b_eq = np.zeros(N + 1); b_eq[-1] = 1
    c = np.zeros(N); c[list(Uset)] = -1
    A_ub = None; b_ub = None
    if cliques:
        rows = []
        Ul = sorted(Uset)
        for a, b in itertools.combinations(Ul, 2):
            if Om[a, b]:
                cc = a ^ b  # a, b, a+b: a and b anticommute -> a+b anticommutes with both
                if cc > b and cc in Uset:
                    r = np.zeros(N); r[[a, b, cc]] = 1; rows.append(r)
        if rows:
            A_ub = np.array(rows); b_ub = np.ones(len(rows))
    r = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, 1), method="highs")
    return -r.fun, r


def lags_from_codes(n, codes):
    pos = [(i, j) for i in range(n) for j in range(i, n)]
    def zof(M, x):
        return sum((sum(M[i][j] * (x >> j & 1) for j in range(n)) % 2) << i for i in range(n))
    L = [frozenset(x for x in range(1 << n)), frozenset(x << n for x in range(1 << n))]
    for c in codes:
        M = [[0] * n for _ in range(n)]
        for b, (i, j) in enumerate(pos):
            if c >> b & 1: M[i][j] = M[j][i] = 1
        L.append(frozenset(x | (zof(M, x) << n) for x in range(1 << n)))
    return L


def check_identity(n, Om, trials=3):
    d = 1 << n; X1 = np.array([[0, 1], [1, 0]], complex); Z1 = np.diag([1, -1]).astype(complex)
    def P(v):
        M = np.eye(1)
        for i in range(n):
            xi, zi = v >> i & 1, v >> (n + i) & 1
            M = np.kron(M, (1j) ** (xi * zi) * np.linalg.matrix_power(X1, xi) @ np.linalg.matrix_power(Z1, zi))
        return M
    Ps = [P(v) for v in range(d * d)]; rng = np.random.default_rng(0); worst = 0
    for _ in range(trials):
        psi = rng.standard_normal(d) + 1j * rng.standard_normal(d); psi /= np.linalg.norm(psi)
        m = np.array([np.vdot(psi, Q @ psi).real ** 2 for Q in Ps])
        worst = max(worst, np.abs((1 - 2 * Om) @ m - d * m).max())
    return float(worst)


t0 = time.time(); res = dict(identity_check={}, cases=[])
for n in (2, 3, 4):
    res["identity_check"][n] = check_identity(n, omega_matrix(n)); assert res["identity_check"][n] < 1e-9
print("self-duality identity verified n=2,3,4", res["identity_check"], flush=True)
# n = 3 five-set: example codes from the size-7 control [41, 14, 53]
cases = [(3, "three-qubit five-set", lags_from_codes(3, [41, 14, 53]), 6.0)]
ex4 = {"__name__": "x", "__file__": os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py")}
src4 = open(os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py"), encoding="utf-8").read()
exec(src4[: src4.index("def decide")], ex4)
lags4, _ = ex4["lagrangians"](4)
census = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_size5_census.json")))
for name, t, truth in zip(("four-qubit type A (genuine five-set)", "four-qubit type B (lifted five-set)"), census["types"], (14.16220, 14.0)):
    cases.append((4, name, [frozenset(lags4[i]) for i in t["example"]], truth))
nine4 = [53, 508, 753, 1027, 1092, 1602, 1876, 2024, 2095]  # Pass 12645 indexing (w33_four_qubit_theta_exact.py) -- may differ; checked below
cases.append((5, "five-qubit size-9", lags_from_codes(5, json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_size9_verify.json")))["example"]), 30.0))
Oms = {}
for n, name, lags, truth in cases:
    d = 1 << n
    C = set().union(*lags) - {0}
    assert all(len(L - {0}) == d - 1 for L in lags) and len(C) == len(lags) * (d - 1), name
    U = set(range(1, d * d)) - C
    Om = Oms.setdefault(n, omega_matrix(n))
    lp0, _ = lp_bound(n, U, Om=Om)
    lp1, _ = lp_bound(n, U, cliques=True, Om=Om)
    rec = dict(n=n, name=name, n_U=len(U), truth_SigmaU_max=truth, LP=lp0, LP_with_clique_cuts=lp1,
               minF_bound=(d - 1 - min(lp0, lp1)) / d, exact_one_over_d=bool(abs(min(lp0, lp1) - (d - 2)) < 1e-7))
    assert min(lp0, lp1) >= truth - 1e-6, rec
    res["cases"].append(rec); print(rec, round(time.time() - t0), "s", flush=True)
res["seconds"] = round(time.time() - t0, 1)
json.dump(res, open(os.path.join(ROOT, "data", "w33_selfdual_pauli_lp.json"), "w"), indent=1)
