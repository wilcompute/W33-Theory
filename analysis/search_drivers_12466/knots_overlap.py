"""12528: the plat-closure amplitude is a stabiliser overlap.  In the TL6 two-qutrit braid rep, take the cap = the rank-1 joint eigenstate of the commuting p0, p2, p4 (the line L0).  Test the COMPLEX identity
bracket(plat closure) = 3 <cap| U_beta |cap>, and |..| = sqrt(3)^d / 3 with d = dim(L0 meet beta L0), against the independent state sum.  Then equidistribution of long words on the rank-3 relation of the lines, (1, 12, 27)/40, which predicts the mod-3 homology
distribution of random 3-bridge closures.  usage: py -3 knots_overlap.py"""
import collections, json, math, random, runpy
import numpy as np
ks = open("knots_w33.py", encoding="utf-8").read().split("# plat\n")[0]
g = {}; exec(ks, g)
bracket, rep, L0, rand_word, path, pts, lines = (g[k] for k in ("bracket", "rep", "L0", "rand_word", "path", "pts", "lines"))
tlsrc = open("tl_braid_iso.py", encoding="utf-8").read().split("U4 = generate(R[:3])")[0]
t = {}; exec(tlsrc, t)
Pis, A, Rm, pauli = t["Pis"], t["A"], t["R"], t["pauli"]
out = dict(tl_ok=bool(t["tl_ok"]), braid_ok=bool(t["braid_ok"]))
P02 = Pis[0] @ Pis[2]; out["rank_Pi0_Pi2"] = int(np.linalg.matrix_rank(P02, tol=1e-8))
vals, vecs = np.linalg.eigh((P02 + P02.conj().T) / 2); cap = vecs[:, -1]
out["Pi4_on_cap"] = float(np.linalg.norm(Pis[4] @ cap))
# Pi_4 is an arbitrary eigenprojector: use the eigenspace of P(p4) containing the cap, as the caps require
Pc = pauli(pts[path[4]]); lam = np.vdot(cap, Pc @ cap); out["cap_is_P4_eigenstate"] = bool(abs(abs(lam) - 1) < 1e-9)
Pi4 = sum(np.linalg.matrix_power(Pc / lam, k) for k in range(3)) / 3
R = list(Rm); R[4] = A * np.eye(9) + (1 / A) * np.sqrt(3) * Pi4
out["braid_relations_with_chosen_Pi4"] = bool(np.allclose(R[3] @ R[4] @ R[3], R[4] @ R[3] @ R[4]))
rng = random.Random(11); agree = abs_agree = 0; tests = 0; worst = 0.0
for _ in range(160):
    wd = g["rand_word"](6, rng.randint(2, 12))
    U = np.eye(9, dtype=complex)
    for s in wd:
        M = R[abs(s) - 1] if s > 0 else R[abs(s) - 1].conj().T
        U = U @ M
    amp = 3 * np.vdot(cap, U @ cap); b = bracket(wd, 6, "plat"); worst = max(worst, abs(amp - b)); tests += 1
    agree += abs(amp - b) < 1e-8
    gg = rep(wd); m = len(L0 & frozenset(gg[p] for p in L0)); abs_agree += abs(abs(amp) - math.sqrt(3) ** {4: 2, 1: 1, 0: 0}[m]) < 1e-8
out.update(tests=tests, complex_identity_agree=agree, abs_vs_line_agree=abs_agree, worst_error=worst)
rng = random.Random(3); cnt = collections.Counter(); N = 20000
for _ in range(N):
    wd = rand_word(6, 60); gg = rep(wd); cnt[{4: 2, 1: 1, 0: 0}[len(L0 & frozenset(gg[p] for p in L0))]] += 1
out["long_word_dim_frequencies"] = {k: round(v / N, 4) for k, v in sorted(cnt.items())}; out["predicted"] = {0: 27 / 40, 1: 12 / 40, 2: 1 / 40}
print(json.dumps(out, default=str)); json.dump(out, open("knots_overlap.json", "w"), indent=1, default=str)
