"""Item 2: unified groups in which the PQ quarks are COMPLETE multiplets, so no splitting is needed.
Trinification SU(3)_C x SU(3)_L x SU(3)_R: (3, 3bar, 1) = (3,2,1/6) + (3,1,-1/3).  Flipped SU(5): 10 = (3,2,1/6) + (3bar,1,1/3) + (1,1,0), so a vectorlike 10 + 10bar = Dirac (3,2,1/6) + Dirac (3,1,-1/3) + a singlet.
Candidate A' = 2 x [(3,2,1/6) + (3,1,-1/3)]: Model A plus one more (3,1,-1/3).  My scan of Pass 12605 stopped at three coloured multiplets, so A' was never tested.  Also 1 x and 3 x the pair.
Two-loop crossing exactly as pq_twoloop.py (all three couplings meet, as in trinification with the standard k1 = 5/3 embedding; flipped SU(5) needs only alpha_2 = alpha_3 and is reported separately as the scale where those two meet).
Then the same chain: proton tau and SU(5)-type threshold spread are not applied here, since the heavy states of trinification differ; the central tau estimate is reported, with the 4D formula.  PQ charges: all sign choices; N_DW, E/N, g/g_KSVZ.  M_X window and y_Q for post-inflation f.
usage: py -3 pq_complete_multiplets.py"""
import itertools
import json
import math
import numpy as np

src = open("pq_twoloop.py", encoding="utf-8").read().split("out = {}")[0]
g = {}
exec(src, g)
solve2, tau, run = g["solve2"], g["tau"], g["run"]
PAIR = [(3, 2, 1 / 6), (3, 1, -1 / 3)]
out = {}
for n in (1, 2, 3):
    reps = PAIR * n
    s = solve2(reps, x0=[math.log(1e10), math.log(5e15)])
    row = dict(reps=reps, two_loop=s)
    if s:
        row["tau"] = tau(s["MU"], s["inv_alpha_U"])
        # charges: each multiplet +-1, first fixed +1
        Ti = {(3, 2): (1.0, 3 * 2 * (1 / 36 + 3 / 12)), (3, 1): (0.5, 3 * (1 / 9))}  # (N, E) per multiplet
        signs = []
        for q in itertools.product((1, -1), repeat=len(reps)):
            if q[0] != 1:
                continue
            N = sum(a * Ti[(r[0], r[1])][0] for a, r in zip(q, reps))
            E = sum(a * Ti[(r[0], r[1])][1] for a, r in zip(q, reps))
            if abs(N) < 1e-9:
                continue
            signs.append(dict(q=list(q), NDW=abs(2 * N), EN=E / N, g=abs(E / N - 1.92) / 1.92))
        ndw1 = [x for x in signs if abs(x["NDW"] - 1) < 1e-9]
        row["ndw1"] = ndw1
        row["EN_set_ndw1"] = sorted({round(x["EN"], 4) for x in ndw1})
        row["EN_set_all"] = sorted({round(x["EN"], 4) for x in signs})
    out[f"{n}_pairs"] = row
    print(n, "pairs:", None if not s else "MX %.3g MU %.3g 1/a %.2f tau %.2g" % (s["MX"], s["MU"], s["inv_alpha_U"], row["tau"]), "E/N with N_DW=1:", row.get("EN_set_ndw1"), "all:", row.get("EN_set_all"), flush=True)
# flipped SU(5): only alpha2 = alpha3, scan threshold
fl = {}
for MX in (1e8, 1e9, 1e10, 1e11, 1e12):
    for n in (1, 2):
        reps = PAIR * n
        def f(lnMU):
            a = run(reps, [1.0] * len(reps), math.log(MX), lnMU)
            return a[1] - a[2]
        from scipy.optimize import brentq
        try:
            lnMU = brentq(f, math.log(MX * 1.01), math.log(1e19))
            a = run(reps, [1.0] * len(reps), math.log(MX), lnMU)
            fl[f"{n}_{MX:.0e}"] = dict(MU=math.exp(lnMU), inv_a23=float(a[2]), inv_a1=float(a[0]), tau=tau(math.exp(lnMU), float(a[2])))
        except ValueError:
            fl[f"{n}_{MX:.0e}"] = None
out["flipped_23"] = fl
print("flipped alpha2 = alpha3:", {k: (None if v is None else ("%.2g" % v["MU"], "%.2g" % v["tau"])) for k, v in fl.items()}, flush=True)
json.dump(out, open("pq_complete_multiplets.json", "w"), indent=1, default=float)
