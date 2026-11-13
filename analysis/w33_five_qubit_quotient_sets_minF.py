"""Pass 12658: numerical min F for the two five-qubit 9-sets obtained as quotients of the F_8 regulus (w33_regulus_f8_and_quotient.py;
spectral types '27' and '17'), compared with the Pass 12650 set (1/32).  Also stabiliser data: the distribution of |M cap C| is not
enumerated; the optimiser levels are reported in units of 1/32.  usage: py -3 analysis/w33_five_qubit_quotient_sets_minF.py"""
import json, os, numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_selfdual_pauli_lp.py"), encoding="utf-8").read(); g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_selfdual_pauli_lp.py")}
exec(src[: src.index("t0 = time.time()")], g)
n = 5; d = 32
X1 = np.array([[0, 1], [1, 0]], complex); Z1 = np.diag([1, -1]).astype(complex)
def P(v):
    M = np.eye(1)
    for i in range(n):
        xi, zi = v >> i & 1, v >> (n + i) & 1
        M = np.kron(M, (1j) ** (xi * zi) * np.linalg.matrix_power(X1, xi) @ np.linalg.matrix_power(Z1, zi))
    return M
def minF(codes, starts=40, seed=0):
    C = sorted(set().union(*g["lags_from_codes"](5, codes)) - {0}); Ps = np.array([P(v) for v in C]); rng = np.random.default_rng(seed)
    def fg(w):
        v = w[:d] + 1j * w[d:]; nv = np.vdot(v, v).real; e = np.einsum("i,kij,j->k", v.conj(), Ps, v).real
        f = (e ** 2).sum() / nv ** 2 / d
        gr = (4 * np.einsum("k,kij,j->i", e, Ps, v) / nv ** 2 - 4 * (e ** 2).sum() * v / nv ** 3) / d
        return f, np.concatenate([gr.real, gr.imag])
    vals = sorted(minimize(fg, rng.standard_normal(2 * d), jac=True, method="L-BFGS-B", options=dict(maxiter=5000, gtol=1e-12, ftol=1e-15)).fun for _ in range(starts))
    return dict(min_F=vals[0], times_32=vals[0] * 32, levels_times_32=sorted({round(v * 32, 3) for v in vals})[:8])
q = json.load(open(os.path.join(ROOT, "data", "w33_regulus_f8_and_quotient.json")))["quotients"]
t27 = next(r for r in q if r["top_multiplicities"][2][1] == 27); t17 = next(r for r in q if r["top_multiplicities"][2][1] == 17)
out = dict(pass12650=minF(json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_size9_verify.json")))["example"]),
           quotient_type27=dict(codes=t27["codes"], **minF(t27["codes"])), quotient_type17=dict(codes=t17["codes"], **minF(t17["codes"])))
for k, v in out.items(): print(k, {a: b for a, b in v.items() if a != "codes"}, flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "w33_five_qubit_quotient_sets_minF.json"), "w"), indent=1)
