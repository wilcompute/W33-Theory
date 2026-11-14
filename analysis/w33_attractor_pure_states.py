"""Pass 12665: attractors of the E6(6) cubic are pure three-qubit states.
Setting (Pass 12656): the 27 three-qubit Paulis commuting with J = (Y (x) I (x) I) K form an elliptic quadric; for a charge vector
Q in R^27 put X(Q) = sum_v Q_v P_v (traceless quaternionic-Hermitian 8x8) and N(Q) = Tr X^3 / 48 (the E6(6) cubic, Pass 12655-12656).
A pure state psi has charge Q_v = <psi|P_v|psi>, with X = 4 Pi - I (Pi = projector on span{psi, J psi}), |Q|^2 = 3, N = 1.
5D maximal supergravity reading (Ferrara-Gunaydin hep-th/0606108): Q are the 27 electric charges; at the origin of moduli space
E6(6)/USp(8) the central charge is Q itself; the black-hole potential V(Q, phi) = |exp(phi.P) Q|^2 over the 42 non-compact
directions P (symmetric part of the stabiliser algebra of N); its minimum is the attractor; the entropy is S ~ sqrt|N|.
Tests:
 (1) stabiliser algebra of N in the Pauli basis: 78 = 36 (skew) + 42 (symmetric); the 36 skew ones are the conjugation action
     of usp(8) (they preserve Tr X^2, Tr X^4);
 (2) for pure-state charges the origin is a critical point of V: <Q, P Q> = 0 for all 42 P;
 (3) for random charges with N > 0: minimise V over phi in R^42; check V_min = 3 N^(2/3) and that the attractor charge Q* has
     quaternionic spectrum N^(1/3) (3, -1, -1, -1), i.e. Q* / N^(1/3) is the charge of a PURE STATE (reconstructed explicitly:
     (X*/N^(1/3) + I)/4 is a rank-2 projector, psi in its range, and charge(psi) = Q*/N^(1/3));
 (4) controls: N < 0 charges flow to -(pure state charge), which is NOT the charge of any state (I + X not >= 0);
     N = 0 charges have inf V = 0 (no attractor: small black holes); mixed states have N in [N_min, 1], N < 0 possible.
usage: py -3 analysis/w33_attractor_pure_states.py"""
import itertools, json, os, time
import numpy as np
from scipy.linalg import expm, null_space
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_e6_cubic_from_three_qubit_paulis.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_e6_cubic_from_three_qubit_paulis.py")}
exec(src[: src.index("rng = np.random.default_rng(0); x = rng.standard_normal(27)")], g)
quad, Ps, T, idx = g["quad"], g["Ps"], g["T"], g["idx"]
s2 = open(os.path.join(HERE, "w33_e6_cubic_skew_stabilizer_projection.py"), encoding="utf-8").read()
h = {"__name__": "x", "__file__": os.path.join(HERE, "w33_e6_cubic_skew_stabilizer_projection.py")}
exec(s2[: s2.index("T = tensor(signs)")], h)
PQ = np.array([Ps[v] for v in quad])
Xof = lambda Q: np.einsum("k,kij->ij", Q, PQ)
Nof = lambda Q: float(np.trace(np.linalg.matrix_power(Xof(Q), 3)).real / 48)
charge = lambda psi: np.einsum("i,kij,j->k", psi.conj(), PQ, psi).real
res = {}; t0 = time.time()
# (1) algebra
B = h["stabilizer"](T); n = 27
Xs = [B[:, a].reshape(n, n) for a in range(B.shape[1])]
Sk = null_space(np.array([(X + X.T).reshape(-1) for X in Xs]).T, rcond=1e-9); Sy = null_space(np.array([(X - X.T).reshape(-1) for X in Xs]).T, rcond=1e-9)
K = [sum(c * X for c, X in zip(Sk[:, i], Xs)) for i in range(Sk.shape[1])]
P = [sum(c * X for c, X in zip(Sy[:, i], Xs)) for i in range(Sy.shape[1])]
P = [p / np.linalg.norm(p) for p in P]
rng = np.random.default_rng(0)
x = rng.standard_normal(27)
inv_dev = max(max(abs(np.trace(np.linalg.matrix_power(Xof(expm(0.3 * k) @ x), m)) - np.trace(np.linalg.matrix_power(Xof(x), m))) for m in (2, 4)) for k in K)
res.update(dim_g=len(Xs), dim_skew=len(K), dim_sym=len(P), skew_preserve_TrX2_TrX4=float(inv_dev))
print("algebra", res, flush=True)
assert (len(Xs), len(K), len(P)) == (78, 36, 42)
# (2) pure-state charges are critical points
crit = 0.0
for _ in range(10):
    psi = rng.standard_normal(8) + 1j * rng.standard_normal(8); psi /= np.linalg.norm(psi)
    Q = charge(psi); crit = max(crit, max(abs(Q @ (p @ Q)) for p in P))
res["pure_state_gradient_max"] = float(crit)
# (3) attractor flow
def flow(Q, starts=4):
    best = None
    for s in range(starts):
        def V(a):
            A = sum(ai * p for ai, p in zip(a, P)); y = expm(A) @ Q; return float(y @ y)
        a0 = 0.05 * rng.standard_normal(42) if s else np.zeros(42)
        r = minimize(V, a0, method="L-BFGS-B", options=dict(maxiter=3000, gtol=1e-12, ftol=1e-15))
        if best is None or r.fun < best.fun: best = r
    A = sum(ai * p for ai, p in zip(best.x, P)); return expm(A) @ Q, best.fun
rows = []
for trial in range(12):
    Q = rng.standard_normal(27) * rng.uniform(0.5, 2.0)
    N = Nof(Q)
    Qs, Vmin = flow(Q)
    Ns = Nof(Qs)
    ev = np.sort(np.linalg.eigvalsh(Xof(Qs)))
    c = np.cbrt(abs(N)); sgn = np.sign(N)
    target = np.sort(sgn * c * np.array([3, 3, -1, -1, -1, -1, -1, -1]))
    rec = dict(N=N, N_after=Ns, V_min=Vmin, three_N23=3 * abs(N) ** (2 / 3), spectrum=[round(float(e), 6) for e in ev],
               spectrum_matches=bool(np.allclose(ev, target, atol=1e-4 * max(1, c))))
    if N > 0:
        Xn = Xof(Qs) / c; Pi = (Xn + np.eye(8)) / 4
        w, V_ = np.linalg.eigh((Pi + Pi.conj().T) / 2); psi = V_[:, -1]
        rec["projector_rank2"] = bool(np.allclose(np.round(w, 4), [0] * 6 + [1, 1], atol=1e-3))
        rec["reconstructed_pure_state_charge_error"] = float(np.abs(charge(psi) - Qs / c).max())
        rec["is_state"] = True
    else:
        rec["I_plus_X_min_eig"] = float(np.linalg.eigvalsh(np.eye(8) + Xof(Qs) / c).min()); rec["is_state"] = False
    rows.append(rec); print({k: (v if k != "spectrum" else v[:3] + ["..."] + v[-2:]) for k, v in rec.items()}, round(time.time() - t0), "s", flush=True)
res["flows"] = rows
# (4) N = 0 charge (a basis-like charge with one Pauli): inf V -> 0
Q0 = np.zeros(27); Q0[0] = 1.0
_, V0 = flow(Q0, starts=2); res["N_zero_charge"] = dict(N=Nof(Q0), V_min_found=V0)
# mixed states: range of N over states with given quaternionic spectrum
ps = [(0.5, 0, 0, 0), (0.25, 0.25, 0, 0), (1 / 6, 1 / 6, 1 / 6, 0), (0.125,) * 4, (0.4, 0.1, 0, 0)]
res["mixed_state_N"] = {str(p): float(sum((8 * pi - 1) ** 3 for pi in p) / 24) for p in ps}
print("N = 0 charge:", res["N_zero_charge"], "| mixed N:", res["mixed_state_N"], flush=True)
res["seconds"] = round(time.time() - t0, 1)
json.dump(res, open(os.path.join(ROOT, "data", "w33_attractor_pure_states.json"), "w"), indent=1)
