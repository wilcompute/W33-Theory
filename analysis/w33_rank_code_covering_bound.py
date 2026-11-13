"""Pass 12655: the elementary covering lower bound for maximal partial spreads in rank-code form, n = 3..6.
A maximal set {S_1..S_k} (plus the X- and Z-Lagrangians) must kill every other nonsingular symmetric T (T + S_i singular for some i).
K(S) = #{T nonsingular : T + S singular} depends only on the congruence class of S (two classes for even n: alternating or not;
one for odd n).  Hence size >= 2 + ceil(N / (K_max + 1)).  For comparison: true minima 5, 5, 9 (n = 3, 4, 5; Passes 12643-12654) and
the Grassl/Kantor value q^k + 1 = 9 at n = 6 (Kantor, Adv. Geom. 2017, Thm 5.2, dims 4k and 4k-2).
usage: py -3 analysis/w33_rank_code_covering_bound.py"""
import json, os, math, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_symmetric_rank_code_spreads.py")}
src = open(os.path.join(HERE, "w33_symmetric_rank_code_spreads.py"), encoding="utf-8").read()
exec(src[: src.index("def code_of")], g)
out = {}
for n in (3, 4, 5, 6):
    t0 = time.time(); pos, sing, alt, ns = g["setup"](n); N = len(ns)
    reps = {}
    for c in ns.tolist():
        key = bool(alt[c]) if hasattr(alt, "__getitem__") else False
        if key not in reps: reps[key] = c
        if len(reps) == 2: break
    K = {str(k): int(sing[ns ^ c].sum()) for k, c in reps.items()}
    Kmax = max(K.values())
    out[n] = dict(N_nonsingular=int(N), kills_by_class=K, covering_lower_bound_on_size=2 + math.ceil(N / (Kmax + 1)), seconds=round(time.time() - t0, 1))
    print(n, out[n], flush=True)
out["known_minima"] = {"3": 5, "4": 5, "5": 9, "6": "<= 9 (Grassl/Kantor value; exact minimum open)"}
json.dump(out, open(os.path.join(ROOT, "data", "w33_rank_code_covering_bound.json"), "w"), indent=1)
