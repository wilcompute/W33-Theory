"""Pass 12651 item 4: a longer and more varied search for a five-qubit maximal partial spread of size 8 (6 matrices): annealing with
single and double replacements, adaptive temperature, many restarts, 2400 s.  Control: size 9 (7 matrices) must be found quickly.
Not finding size 8 is evidence only.  usage: py -3 analysis/w33_five_qubit_size8_anneal2.py"""
import json, os, time, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_symmetric_rank_code_spreads.py")}
src = open(os.path.join(HERE, "w33_symmetric_rank_code_spreads.py"), encoding="utf-8").read()
exec(src[: src.index("def code_of")], g)
pos, sing, alt, ns = g["setup"](5)
def run(k, tlimit, seed):
    rng = np.random.default_rng(seed); t0 = time.time(); best = 10 ** 9; restarts = 0; hist = []
    def compat(S):
        m = np.ones(len(ns), bool)
        for s in S: m &= ~sing[ns ^ s]
        return m
    while time.time() - t0 < tlimit:
        restarts += 1; S = []; avail = np.ones(len(ns), bool)
        while len(S) < k and avail.any():
            i = int(rng.choice(np.flatnonzero(avail))); S.append(int(ns[i])); avail &= ~sing[ns ^ ns[i]]
        if len(S) < k: continue
        c = int(compat(S).sum()); T = 3.0
        for step in range(6000):
            drop = list(rng.choice(k, 2 if rng.random() < 0.3 else 1, replace=False)); keep = [S[i] for i in range(k) if i not in drop]
            new = list(keep)
            for _ in drop:
                cand = np.flatnonzero(compat(new))
                if len(cand) == 0: break
                new.append(int(ns[int(rng.choice(cand))]))
            if len(new) < k: continue
            c2 = int(compat(new).sum())
            if c2 <= c or rng.random() < math.exp(-(c2 - c) / max(T, 1e-3)): S, c = new, c2
            T = max(0.05, T * 0.9993)
            if c < best: best = c
            if c == 0: return dict(size=k + 2, found=True, example=S, restarts=restarts, seconds=round(time.time() - t0, 1))
        hist.append(c)
    return dict(size=k + 2, found=False, best_cost=best, restarts=restarts, final_costs_min=min(hist) if hist else None, seconds=round(time.time() - t0, 1))
res = dict(control_size9=run(7, 300, 1)); print(res, flush=True)
res["size8"] = run(6, 2400, 2); print(res["size8"], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_five_qubit_size8_anneal2.json"), "w"), indent=1)
