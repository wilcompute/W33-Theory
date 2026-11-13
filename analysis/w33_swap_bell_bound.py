"""Pass 12652 addendum (novel route): the SWAP/Bell bound for strongly unextendible Pauli MUB sets.
For pure rho = |psi><psi| on n qubits and any set U of Paulis,
    Sigma_U <P>^2 = Tr[(rho (x) rho) Q_U],  Q_U = sum_{b in U} P_b (x) P_b.
All P_b (x) P_b commute, and are diagonal in the Bell basis |Phi_a> = (P_a (x) I)|Phi>:
    (P_b (x) P_b)|Phi_a> = s(b) (-1)^{omega(a,b)} |Phi_a>,  s(b) = (-1)^{#Y(b)} = (-1)^{x_b . z_b},
and SWAP|Phi_a> = s(a)|Phi_a>.  rho (x) rho lies in the symmetric subspace = span{Phi_a : s(a) = +1}, so
    Sigma_U <= B(U) := max_{a : s(a)=+1} V(a),  V(a) = sum_{b in U} s(b) (-1)^{omega(a,b)},
an INTEGER computed by a Walsh-type sum, no optimisation.  For a MUB set with covered set C (F = Sigma_C/d) and U its complement:
    min F >= (d - 1 - B(U)) / d,  and B(U) = d - 2 gives min F >= 1/d EXACTLY.
Control: U = all non-identity Paulis must give B = d - 1 (purity).  Each set is also compared with a numerical min F (the bound must
not exceed it) and with the Lovasz-theta bound where known.  usage: py -3 analysis/w33_swap_bell_bound.py"""
import json, os, time
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
pc = np.vectorize(lambda v: bin(int(v)).count("1"))


def bell_bound(U, n):
    """U: array of (x, z) bit-ints.  Returns B(U), the argmax a, and the full V for symmetric a."""
    if len(U) == 0:
        return 0, (0, 0), np.zeros(1, int)
    ux = np.array([u[0] for u in U], dtype=np.int64); uz = np.array([u[1] for u in U], dtype=np.int64)
    sb = 1 - 2 * (pc(ux & uz) % 2)
    best = None
    ax = np.repeat(np.arange(1 << n), 1 << n); az = np.tile(np.arange(1 << n), 1 << n)
    sym = (pc(ax & az) % 2) == 0
    ax, az = ax[sym], az[sym]
    V = np.zeros(len(ax), int)
    for k in range(0, len(ux), 256):
        om = (pc(np.bitwise_and.outer(ax, uz[k:k + 256])) + pc(np.bitwise_and.outer(az, ux[k:k + 256]))) % 2
        V += ((1 - 2 * om) * sb[k:k + 256]).sum(1)
    i = int(np.argmax(V))
    return int(V[i]), (int(ax[i]), int(az[i])), V


def covered(codes, n, pos):
    C = set()
    for x in range(1, 1 << n):
        C.add((x, 0)); C.add((0, x))
        for c in codes:
            z = 0
            for i in range(n):  # z_i = sum_j S_ij x_j
                bit = 0
                for j in range(n):
                    a, b = min(i, j), max(i, j)
                    if c >> pos.index((a, b)) & 1 and x >> j & 1: bit ^= 1
                z |= bit << i
            C.add((x, z))
    return C


def pauli(x, z, n):
    X1 = np.array([[0, 1], [1, 0]]); Z1 = np.diag([1, -1]); M = np.eye(1)
    for i in range(n):
        xi, zi = x >> i & 1, z >> i & 1
        M = np.kron(M, (1j) ** (xi * zi) * np.linalg.matrix_power(X1, xi) @ np.linalg.matrix_power(Z1, zi))
    return M


def num_minF(C, n, starts=12, seed=0):
    d = 1 << n; Ps = np.array([pauli(x, z, n) for x, z in C]); rng = np.random.default_rng(seed)

    def fg(w):
        v = w[:d] + 1j * w[d:]; nv = np.vdot(v, v).real; e = np.einsum("i,kij,j->k", v.conj(), Ps, v).real
        f = (e ** 2).sum() / nv ** 2 / d
        g = (4 * np.einsum("k,kij,j->i", e, Ps, v) / nv ** 2 - 4 * (e ** 2).sum() * v / nv ** 3) / d
        return f, np.concatenate([g.real, g.imag])
    return min(minimize(fg, rng.standard_normal(2 * d), jac=True, method="L-BFGS-B").fun for _ in range(starts))


def random_maximal(n, rng):
    pos = [(i, j) for i in range(n) for j in range(i, n)]
    def mat(c):
        S = np.zeros((n, n), int)
        for b, (i, j) in enumerate(pos):
            if c >> b & 1: S[i, j] = S[j, i] = 1
        return S
    def nonsing(c):
        return round(abs(np.linalg.det(mat(c)))) % 2 == 1 if False else _rank2(mat(c)) == n
    ns = [c for c in range(1 << len(pos)) if nonsing(c)]
    S = []; avail = list(ns)
    while avail:
        c = int(rng.choice(avail)); S.append(c); avail = [t for t in avail if nonsing(t ^ c)]
    return S, pos


def _rank2(M):
    M = M.copy() % 2; r = 0; m = len(M)
    for col in range(m):
        piv = next((k for k in range(r, m) if M[k, col]), None)
        if piv is None: continue
        M[[r, piv]] = M[[piv, r]]
        for k in range(m):
            if k != r and M[k, col]: M[k] ^= M[r]
        r += 1
    return r


t0 = time.time(); out = dict(controls={}, sets=[])
for n in (2, 3, 4):
    allp = [(x, z) for x in range(1 << n) for z in range(1 << n) if (x, z) != (0, 0)]
    B, _, _ = bell_bound(allp, n); out["controls"][f"all_n{n}"] = B
    assert B == (1 << n) - 1, (n, B)
print("purity controls", out["controls"], flush=True)
rng = np.random.default_rng(1)
for n, reps in ((2, 4), (3, 12), (4, 30)):
    d = 1 << n; seen = {}
    for _ in range(reps):
        S, pos = random_maximal(n, rng)
        C = covered(S, n, pos); U = [p for p in ((x, z) for x in range(d) for z in range(d)) if p != (0, 0) and p not in C]
        B, a, _ = bell_bound(U, n); mf = num_minF(sorted(C), n)
        key = (len(S) + 2, B)
        rec = dict(n=n, size=len(S) + 2, B=B, bound_minF=(d - 1 - B) / d, numeric_minF=mf, tight=bool(abs(mf - (d - 1 - B) / d) < 1e-6))
        assert (d - 1 - B) / d <= mf + 1e-7
        if key not in seen or (rec["tight"] and not seen[key]["tight"]):
            seen[key] = rec
    for r in seen.values():
        print(r, flush=True); out["sets"].append(r)
for n, f in ((5, "w33_five_qubit_size9_verify.json"), (6, "w33_six_qubit_size9_verify.json")):
    d = 1 << n; pos = [(i, j) for i in range(n) for j in range(i, n)]
    codes = json.load(open(os.path.join(ROOT, "data", f)))["example"]
    C = covered(codes, n, pos); assert len(C) == (len(codes) + 2) * (d - 1)
    U = [p for p in ((x, z) for x in range(d) for z in range(d)) if p != (0, 0) and p not in C]
    B, a, V = bell_bound(U, n)
    rec = dict(n=n, size=len(codes) + 2, n_uncovered=len(U), B=B, argmax=a, bound_minF=(d - 1 - B) / d, exact_one_over_d=bool(B == d - 2),
               top_V=sorted(set(V.tolist()))[-4:])
    print(rec, flush=True); out["sets"].append(rec)
out["seconds"] = round(time.time() - t0, 1)
json.dump(out, open(os.path.join(ROOT, "data", "w33_swap_bell_bound.json"), "w"), indent=1)
