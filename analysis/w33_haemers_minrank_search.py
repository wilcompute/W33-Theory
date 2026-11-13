"""Pass 12653 audit: local search for a Haemers matrix of the W(3,3) collinearity graph G with rank <= 9 over F_2 or F_3
(M_ii != 0, M_ij = 0 whenever i != j are NON-adjacent, edge entries free, not necessarily symmetric).  rank_F(M) bounds
Theta(G) from above, so rank <= 9 would prove Theta(G) < theta(G) = 10.  Control: on C5 (Theta = sqrt5, minrank 3) the search must
reach 3.  Not finding <= 9 is NOT evidence of anything beyond this search.  usage: py -3 analysis/w33_haemers_minrank_search.py [seconds]"""
import json, os, sys, time, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_shannon_capacity_audit.py")}
exec(open(os.path.join(HERE, "w33_shannon_capacity_audit.py"), encoding="utf-8").read().split("t0 = time.time(); res = {}")[0], g)
def rank_p(M, p):
    M = M.copy() % p; n, m = M.shape; r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i, c]), None)
        if piv is None: continue
        M[[r, piv]] = M[[piv, r]]; M[r] = (M[r] * pow(int(M[r, c]), -1, p)) % p
        nz = np.nonzero(M[:, c])[0]
        for i in nz:
            if i != r: M[i] = (M[i] - M[i, c] * M[r]) % p
        r += 1
    return r
def search(A, p, seconds, seed):
    n = len(A); rng = np.random.default_rng(seed); E = list(zip(*np.nonzero(A)))
    M = np.eye(n, dtype=np.int64) * rng.integers(1, p, n)
    for (i, j) in E: M[i, j] = rng.integers(0, p)
    cur = rank_p(M, p); best = cur; T = 1.0; t0 = time.time()
    while time.time() - t0 < seconds:
        if rng.random() < 0.9:
            i, j = E[rng.integers(len(E))]; old = M[i, j]; M[i, j] = (old + rng.integers(1, p)) % p
        else:
            i = j = int(rng.integers(n)); old = M[i, i]; M[i, i] = rng.integers(1, p) if p > 2 else 1
        r = rank_p(M, p)
        if r <= cur or rng.random() < np.exp(-(r - cur) / T): cur = r
        else: M[i, j] = old
        best = min(best, cur); T = max(0.05, T * 0.9995)
    return best
sec = float(sys.argv[1]) if len(sys.argv) > 1 else 240
C5 = np.array([[int((i - j) % 5 in (1, 4)) for j in range(5)] for i in range(5)])
ctrl = {p: search(C5, p, 5, 0) for p in (2, 3)}
print("control C5 best ranks", ctrl, flush=True); assert min(ctrl.values()) == 3
A = g["w33"](); out = dict(control_C5=ctrl, runs=[])
for p in (2, 3):
    for seed in range(2):
        b = search(A, p, sec, seed); out["runs"].append(dict(p=p, seed=seed, best_rank=b)); print(p, seed, b, flush=True)
out["best"] = min(r["best_rank"] for r in out["runs"])
json.dump(out, open(os.path.join(ROOT, "data", "w33_haemers_minrank_search.json"), "w"), indent=1)
