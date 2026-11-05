"""Is Model A's coincidence chosen after the fact?  Two-loop for every decaying representation set from pq_unification.py with a one-loop solution, wide windows, then all PQ sign assignments.
Conditions for a success, declared here:
  (a) tau(p -> e+ pi0) > 2.4e34 yr at central estimate, tau = 1.6e36 (M_U/1e16)^4 (35 alpha_U)^-2.  Then a factor-3 band is also reported.
  (b) 1/alpha_U > 10, M_X < M_U.
  (c) a PQ sign assignment with N != 0, N_DW = |2N| = 1, so post-inflation PQ is free of domain walls.
  (d) natural: y_Q = M_X / f in [0.03, 1.5] with f = f_a in the post-inflation window 3e10 to 1.4e11 GeV (string simulations, Buschmann et al 2022, as I recall), so M_X in 1e9 to 2e11.
Report how many sets pass each stage, and for those passing all, E/N for every N_DW = 1 sign assignment and g/g_KSVZ.
Chance estimate: of sets satisfying (a) and (b) with colour, what fraction also has M_X in the window; a uniform-in-ln null over the two-loop M_X range of those sets gives the size of the coincidence.
PQ charges: each multiplet has charge +1 or -1 and mass from sigma or sigma*.  N = sum q_i d_W T(C), E = sum q_i d_C d_W (Y^2 + (d_W^2 - 1)/12).
usage: py -3 pq_full_scan.py"""
import itertools
import json
import math
import sys
import numpy as np

src = open("pq_twoloop.py", encoding="utf-8").read().split("out = {}")[0]
g = {}
exec(src, g)
solve2, tau, Tc, Tw = g["solve2"], g["tau"], g["Tc"], g["Tw"]
base = json.load(open("pq_unification.json"))
src1 = open("pq_unification.py", encoding="utf-8").read().split("out = {}")[0]
g1 = {"__name__": "x"}
exec(src1, g1)
REPS, COLORLESS, DECAY, solve1, db = (g1[k] for k in ("REPS", "COLORLESS", "DECAY", "solve", "db"))
Fr = g1["Fr"]
rows = []
for k in (1, 2, 3):
    for combo in itertools.combinations_with_replacement(range(len(REPS)), k):
        for extra in [None] + list(range(len(COLORLESS))):
            rs = [REPS[i] for i in combo] + ([COLORLESS[extra]] if extra is not None else [])
            if not all(r in DECAY for r in rs):
                continue
            so = solve1(np.sum([db(r) for r in rs], axis=0))
            if so is None or so["inv_alpha_U"] <= 10 or so["MU"] < 3e14 or so["MX"] < 1e4:
                continue
            rows.append((rs, so))
print("candidates for two-loop", len(rows), flush=True)
out = dict(n_candidates=len(rows), rows=[])


def en(r):
    c, w, y = r
    return float(c * w * (y * y + Fr(w * w - 1, 12))), float(w * g1["T"][c])


for rs, so in rows:
    fl = [(r[0], r[1], float(r[2])) for r in rs]
    s2 = solve2(fl, x0=[math.log(so["MX"]), math.log(so["MU"])])
    if s2 is None or s2["inv_alpha_U"] <= 10:
        continue
    t = tau(s2["MU"], s2["inv_alpha_U"])
    signs = []
    for q in itertools.product((1, -1), repeat=len(rs)):
        if q[0] != 1:
            continue
        N = sum(a * en(r)[1] for a, r in zip(q, rs))
        E = sum(a * en(r)[0] for a, r in zip(q, rs))
        if abs(N) < 1e-9:
            continue
        signs.append(dict(q=list(q), N=N, NDW=abs(2 * N), EN=E / N, g=abs(E / N - 1.92) / 1.92))
    row = dict(reps=[(r[0], r[1], str(r[2])) for r in rs], **s2, tau=t, one_loop=so, signs=signs, has_ndw1=any(abs(x["NDW"] - 1) < 1e-9 for x in signs))
    out["rows"].append(row)
print("two-loop solved", len(out["rows"]), flush=True)
R = out["rows"]
coloured = [r for r in R if any(int(x[0]) > 1 for x in r["reps"])]
a_ = [r for r in coloured if r["tau"] > 2.4e34]
a3 = [r for r in coloured if r["tau"] > 2.4e34 / 3]
c_ = [r for r in a_ if r["has_ndw1"]]
d_ = [r for r in c_ if 1e9 <= r["MX"] <= 2e11]
out["stages"] = dict(coloured=len(coloured), proton=len(a_), proton_factor3=len(a3), ndw1=len(c_), natural=len(d_))
print(out["stages"], flush=True)
for r in sorted(a_, key=lambda r: -r["tau"])[:25]:
    print([f"{a}{b}{c}" for a, b, c in r["reps"]], "MX %.2g MU %.2g 1/a %.1f tau %.2g ndw1 %s" % (r["MX"], r["MU"], r["inv_alpha_U"], r["tau"], r["has_ndw1"]), flush=True)
print("---passing all", flush=True)
for r in d_:
    print([f"{a}{b}{c}" for a, b, c in r["reps"]], "MX %.3g MU %.3g 1/a %.1f tau %.2g" % (r["MX"], r["MU"], r["inv_alpha_U"], r["tau"]), [(x["q"], round(x["EN"], 3), round(x["g"], 3)) for x in r["signs"] if abs(x["NDW"] - 1) < 1e-9], flush=True)
if a_:
    lm = np.log10([r["MX"] for r in a_])
    out["MX_distribution"] = dict(min=float(lm.min()), max=float(lm.max()), frac_in_window=float(np.mean((lm >= 9) & (lm <= math.log10(2e11)))), uniform_null=(math.log10(2e11) - 9) / max(lm.max() - lm.min(), 1e-9))
    print(out["MX_distribution"], flush=True)
json.dump(out, open("pq_full_scan.json", "w"), indent=1, default=float)
print("done", flush=True)
