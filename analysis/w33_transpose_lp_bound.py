"""Pass 12656: LP bound for Sigma_U with BOTH families of exact linear relations on m_b = <P_b>^2 of a pure n-qubit state:
 (i)  unitary (self-duality, Pass 12653):   sum_b (-1)^{omega(a,b)} m_b = d m_a                      for all a;
 (ii) antiunitary (new here): with Q0(b) = x.z,   t_a := (1/d) sum_b (-1)^{Q0(b)+omega(a,b)} m_b = |<psi| P_a |psi*>|^2,
      so t_a = 0 for every ANTISYMMETRIC Pauli a (Q0(a) = 1; P_a K is a quaternionic structure, <psi|J psi> = 0),
      and 0 <= t_a <= 1 for symmetric a (including a = 0).
 Equivalent form of (ii): for each of the 2^(n-1)(2^n - 1) elliptic quadrics E_a, sum_{b in E_a} m_b = d/2 - 1 (n = 3: the 27 lines, 3).
Both are verified on random states first.  LP: max sum_U m_b s.t. m >= 0, m_0 = 1, (i), (ii).  Cases as in w33_selfdual_pauli_lp.py.
usage: py -3 analysis/w33_transpose_lp_bound.py"""
import json, os, time
import numpy as np
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_selfdual_pauli_lp.py")}
src = open(os.path.join(HERE, "w33_selfdual_pauli_lp.py"), encoding="utf-8").read()
exec(src[: src.index("t0 = time.time()")], g)
omega_matrix, lags_from_codes = g["omega_matrix"], g["lags_from_codes"]
pc = np.vectorize(lambda v: bin(int(v)).count("1"))


def mats(n):
    d = 1 << n; N = d * d; Om = omega_matrix(n); v = np.arange(N)
    q0 = pc((v & (d - 1)) & (v >> n)) % 2
    H = 1 - 2 * Om                       # (-1)^omega
    Tm = H * (1 - 2 * q0)[None, :]       # (-1)^{Q0(b) + omega(a,b)}
    return d, N, Om, q0, H, Tm


def check_identities(n, trials=3):
    d, N, Om, q0, H, Tm = mats(n); X1 = np.array([[0, 1], [1, 0]], complex); Z1 = np.diag([1, -1]).astype(complex)
    def P(v):
        M = np.eye(1)
        for i in range(n):
            xi, zi = v >> i & 1, v >> (n + i) & 1
            M = np.kron(M, (1j) ** (xi * zi) * np.linalg.matrix_power(X1, xi) @ np.linalg.matrix_power(Z1, zi))
        return M
    Ps = [P(v) for v in range(N)]; rng = np.random.default_rng(0); w1 = w2 = 0
    for _ in range(trials):
        psi = rng.standard_normal(d) + 1j * rng.standard_normal(d); psi /= np.linalg.norm(psi)
        m = np.array([np.vdot(psi, Q @ psi).real ** 2 for Q in Ps])
        w1 = max(w1, np.abs(H @ m - d * m).max())
        t = Tm @ m / d; tt = np.array([abs(np.vdot(psi, Q @ psi.conj())) ** 2 for Q in Ps])
        w2 = max(w2, np.abs(t - tt).max(), np.abs(t[q0 == 1]).max())
    return float(w1), float(w2)


def lp(n, U):
    d, N, Om, q0, H, Tm = mats(n)
    A_eq = [H - d * np.eye(N), np.eye(N)[:1], Tm[q0 == 1] / d]
    b_eq = [np.zeros(N), np.ones(1), np.zeros(int((q0 == 1).sum()))]
    S = Tm[q0 == 0] / d
    A_ub = np.vstack([-S, S]); b_ub = np.concatenate([np.zeros(len(S)), np.ones(len(S))])
    c = np.zeros(N); c[list(U)] = -1
    r = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=np.vstack(A_eq), b_eq=np.concatenate(b_eq), bounds=(0, 1), method="highs")
    return -r.fun, r


t0 = time.time(); res = dict(identity_residuals={}, cases=[])
for n in (2, 3, 4):
    res["identity_residuals"][n] = check_identities(n); assert max(res["identity_residuals"][n]) < 1e-9
print("identities (unitary, antiunitary) verified:", res["identity_residuals"], flush=True)
cases = [(3, "three-qubit five-set", lags_from_codes(3, [41, 14, 53]), 6.0)]
ex4 = {"__name__": "x", "__file__": os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py")}
src4 = open(os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py"), encoding="utf-8").read()
exec(src4[: src4.index("def decide")], ex4)
lags4, _ = ex4["lagrangians"](4)
census = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_size5_census.json")))
for name, t, truth in zip(("four-qubit type A", "four-qubit type B"), census["types"], (14.16220, 14.0)):
    cases.append((4, name, [frozenset(lags4[i]) for i in t["example"]], truth))
cases.append((5, "five-qubit 9-set", lags_from_codes(5, json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_size9_verify.json")))["example"]), 30.0))
for n, name, lags, truth in cases:
    d = 1 << n; C = set().union(*lags) - {0}; U = set(range(1, d * d)) - C
    val, r = lp(n, U)
    rec = dict(n=n, name=name, truth=truth, LP=val, trivial=d - 1, exact_target=d - 2, status=int(r.status), closes=bool(abs(val - truth) < 1e-6))
    assert val >= truth - 1e-6, rec
    res["cases"].append(rec); print(rec, round(time.time() - t0), "s", flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_transpose_lp_bound.json"), "w"), indent=1)
