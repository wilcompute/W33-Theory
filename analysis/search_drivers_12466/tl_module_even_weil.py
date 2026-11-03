"""12533 follow-up: the TL6 vacuum module is the even Weil sector.  Start from the cap state of knots_overlap.py; apply the TL projectors Pi_i (with the eigenprojector choice that keeps the cap on the module) to generate the module.  Tests: its dimension is 5 = Catalan C_3; the two-qutrit parity is +1 on it; so it equals the even sector, the C^5 of the Burkhardt quartic of 12530; the five non-crossing cap states have the TL Gram matrix delta^(loops - 3); the five non-crossing lines are pairwise in which relation, and are they a half of a crown (a pentad) in the 2 codewords that contain them?  usage: py -3 tl_module_even_weil.py"""
import collections
import itertools
import json
import numpy as np

ks = open("knots_overlap.py", encoding="utf-8").read().split("rng = random.Random(11)")[0]
exec(ks)
out = dict(cap_rank=out["rank_Pi0_Pi2"], cap_in_P4=out["cap_is_P4_eigenstate"])
Pc = pauli(pts[path[4]])
P = list(Pis)
P[4] = Pi4
vs = [cap]
basis = [cap]
for _ in range(8):
    new = []
    for v in basis:
        for pr in P:
            u = pr @ v
            n = np.linalg.norm(u)
            if n < 1e-9:
                continue
            u = u / n
            r = np.array(basis + new).T
            res = u - r @ (r.conj().T @ u) if False else u
            A_ = np.array(basis + new).T
            q, _ = np.linalg.qr(A_)
            if np.linalg.norm(u - q @ (q.conj().T @ u)) > 1e-8:
                new.append(u)
    if not new:
        break
    basis += new
M = np.array(basis).T
out["module_dimension"] = int(np.linalg.matrix_rank(M, tol=1e-8))
Par = np.zeros((9, 9), dtype=complex)
for a, b in itertools.product(range(3), repeat=2):
    Par[3 * ((-a) % 3) + ((-b) % 3), 3 * a + b] = 1
q, _ = np.linalg.qr(M)
q = q[:, :out["module_dimension"]]
out["module_invariant_under_all_R"] = all(np.linalg.norm(R[i] @ q - q @ (q.conj().T @ R[i] @ q)) < 1e-8 for i in range(5))
out["parity_on_module_values"] = sorted({complex(np.round(x, 6)) for x in np.linalg.eigvals(q.conj().T @ Par @ q)}, key=lambda z: z.real)
out["parity_commutes_with_Pi"] = [bool(np.allclose(Par @ pr, pr @ Par)) for pr in P]
# some displaced parity D_x Par D_x^dag may be the right one: search all 81 centres
tau = np.exp(4j * np.pi / 3)
X_ = np.roll(np.eye(3), 1, axis=0).astype(complex); Z_ = np.diag([1, np.exp(2j * np.pi / 3), np.exp(4j * np.pi / 3)])
D1 = lambda a, b: tau ** (a * b % 3) * np.linalg.matrix_power(X_, a) @ np.linalg.matrix_power(Z_, b)
Dx = lambda v: np.kron(D1(v[0], v[2]), D1(v[1], v[3]))
hits = []
for v in itertools.product(range(3), repeat=4):
    A_x = Dx(v) @ Par @ Dx(v).conj().T
    if np.allclose(A_x @ q, q, atol=1e-8):
        hits.append(v)
        comm = [bool(np.allclose(A_x @ pr, pr @ A_x)) for pr in P]
        out["centre_commutes_with_all_Pi"] = comm
        ev = np.linalg.eigvalsh((A_x + A_x.conj().T) / 2)
        out["centre_parity_plus_one_dimension"] = int(np.sum(np.isclose(ev, 1)))
out["displaced_parities_acting_as_plus_one_on_module"] = hits
# the 5 TL basis states from words in the e_i: cap, and the images, with their Gram matrix
e = [np.sqrt(3) * pr for pr in P]
words = {"123456_cap": [], "e2": [1], "e4": [3], "e2e4": [1, 3], "e3e2e4": [2, 1, 3]}
tb = {}
for k, w_ in words.items():
    v = cap
    for i in w_:
        v = e[i] @ v
    tb[k] = v
keys = list(tb)
G = np.array([[np.vdot(tb[a], tb[b]) for b in keys] for a in keys])
out["TL_words_gram_abs_rounded"] = np.round(np.abs(G), 4).tolist()
out["TL_words_rank"] = int(np.linalg.matrix_rank(np.array([tb[k] for k in keys]).T, tol=1e-8))
out["TL_gram_powers_of_sqrt3"] = sorted({round(float(np.log(abs(x)) / np.log(np.sqrt(3))), 4) for x in G.flatten() if abs(x) > 1e-9})
out = {k: (str(v) if k == "parity_on_module_values" else v) for k, v in out.items()}
print(json.dumps(out, default=str))
json.dump(out, open("tl_module_even_weil.json", "w"), indent=1, default=str)
