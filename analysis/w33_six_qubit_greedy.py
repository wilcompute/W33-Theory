"""Pass 12651 item 2: six qubits (W(11,2)).  Greedy rank codes (random and coverage-biased) for the size distribution of maximal partial
spreads; the pattern 2^ceil(n/2)+1 (= Grassl's q^{n/2}+1 for even n) predicts minimum 9.  Grassl gave examples of size q^{n/2}+1 for all
even n and q (Kantor 2017), so size 9 should exist; whether greedy reaches it, and nothing smaller, is the test (smaller sizes found would
refute the pattern; not finding them proves nothing).  usage: py -3 analysis/w33_six_qubit_greedy.py"""
import json, os, time
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_rank_code_greedy_sizes.py")}
src = open(os.path.join(HERE, "w33_rank_code_greedy_sizes.py"), encoding="utf-8").read()
exec(src[: src.index("res = {}")], g)
t0 = time.time(); res = {}
for biased, runs, tl in ((True, 300, 2400), (False, 300, 1200)):
    r = g["greedy"](6, runs, biased, 66, tl); res["n6_" + ("biased" if biased else "random")] = r
    print({k: v for k, v in r.items() if k != "example"}, "(%.0fs)" % (time.time() - t0), flush=True)
    json.dump(res, open(os.path.join(ROOT, "data", "w33_six_qubit_greedy.json"), "w"), indent=1)
