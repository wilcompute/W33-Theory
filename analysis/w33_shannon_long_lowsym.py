"""Pass 12668: long CP-SAT runs for codes in W(3,3) strong-square invariant under LOW-order cyclic groups, where the solver bound was
far from the incumbent (order 2: 56 / bound 84; order 3 with 13 fixed points: 58 / bound 94), hinted with the best code of the class
found so far; the target is a code of size >= 61 (which would raise Theta(W(3,3)) above sqrt 60).  Any improvement is re-verified
pairwise.  usage: py -3 analysis/w33_shannon_long_lowsym.py [seconds_per_class] [workers]"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_shannon_symmetric_codes.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_shannon_symmetric_codes.py")}
argv = sys.argv; sys.argv = ["x", "30", "4"]; exec(src[: src.index("results = []; best")], g); sys.argv = argv
sec = float(sys.argv[1]) if len(sys.argv) > 1 else 1800; wk = int(sys.argv[2]) if len(sys.argv) > 2 else 6
adj = g["adj"]; out = []
for key in [k for k in g["elems"] if k in ((2, 0), (3, 13), (3, 4), (4, 0))]:
    gp = g["elems"][key]
    orbs = g["orbits_of"](40, [lambda q, gp=gp: (gp[q[0]], gp[q[1]])])
    t0 = time.time(); size, bd, st, S, ngood = g["solve_orbits"](40, adj, orbs, sec, wk)
    rec = dict(order=key[0], fixed=key[1], size=size, bound=bd, status=st, seconds=round(time.time() - t0), beats_60=size > 60, set=S)
    out.append(rec); print({k: v for k, v in rec.items() if k != "set"}, flush=True)
    json.dump(out, open(os.path.join(ROOT, "data", "w33_shannon_long_lowsym.json"), "w"), indent=1, default=int)
