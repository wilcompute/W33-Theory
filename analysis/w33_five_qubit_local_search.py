"""Pass 12650: local search for five-qubit maximal partial spreads of size 8 and 9 (rank-code form, k = size - 2 matrices).
State: k pairwise-compatible nonsingular symmetric S_i (S_i + S_j nonsingular).  Cost: number of nonsingular symmetric T compatible with
all S_i (an extension exists iff cost > 0).  Moves: replace one S_i by a random compatible matrix; simulated annealing with restarts.
Cost 0 with k matrices => maximal partial spread of size k + 2.  Control: n = 4 with k = 3 must reach cost 0 (size 5 exists).
usage: py -3 analysis/w33_five_qubit_local_search.py"""
import json, os, time, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_symmetric_rank_code_spreads.py")}
src = open(os.path.join(HERE, "w33_symmetric_rank_code_spreads.py"), encoding="utf-8").read()
exec(src[: src.index("def code_of")], g)
setup = g["setup"]
def anneal(n, k, tlimit, seed):
    pos, sing, alt, ns = setup(n); rng = np.random.default_rng(seed); t0 = time.time(); best = None; restarts = 0
    while time.time() - t0 < tlimit:
        restarts += 1
        S = []; avail = np.ones(len(ns), bool)
        while len(S) < k and avail.any():
            i = int(rng.choice(np.flatnonzero(avail))); S.append(int(ns[i])); avail &= ~sing[ns ^ ns[i]]
        if len(S) < k: continue
        def cost(S_):
            m = np.ones(len(ns), bool)
            for s in S_: m &= ~sing[ns ^ s]
            return int(m.sum())
        c = cost(S); T = 2.0
        for step in range(4000):
            j = int(rng.integers(k)); others = S[:j] + S[j + 1:]
            ok = np.ones(len(ns), bool)
            for s in others: ok &= ~sing[ns ^ s]
            cand = np.flatnonzero(ok)
            if len(cand) == 0: continue
            new = int(ns[int(rng.choice(cand))]); S2 = others + [new]; c2 = cost(S2)
            if c2 <= c or rng.random() < math.exp(-(c2 - c) / max(T, 1e-3)):
                S, c = S2, c2
            T *= 0.999
            if best is None or c < best[0]: best = (c, list(S))
            if c == 0: return dict(n=n, size=k + 2, found=True, example=S, restarts=restarts, seconds=round(time.time() - t0, 1))
    return dict(n=n, size=k + 2, found=False, best_cost=best[0] if best else None, restarts=restarts, seconds=round(time.time() - t0, 1))
res = dict(control_n4_size5=anneal(4, 3, 300, 1)); print(res, flush=True)
res["n5_size9"] = anneal(5, 7, 1500, 2); print(res["n5_size9"], flush=True)
res["n5_size8"] = anneal(5, 6, 1500, 3); print(res["n5_size8"], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_five_qubit_local_search.json"), "w"), indent=1)
