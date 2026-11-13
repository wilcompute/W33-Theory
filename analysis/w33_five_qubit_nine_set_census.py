"""Pass 12660: strength census of five-qubit maximal 9-sets.  Sources: (a) Pass 12650 set; (b) two regulus-quotient types (Pass 12658);
(c) the ten 9-sets of data/w33_five_qubit_floor24.json (annealed 6-matrix state + its isolated extendible T; Pass 12652);
(d) the 9-sets returned by the exact-cover search in forward and reversed order.  For each: maximality re-check, invariants
(vanishing quadrics, number of simple eigenvalues and top multiplicities of the uncovered graph), numerical min F * 32 (analytic gradient).
usage: py -3 analysis/w33_five_qubit_nine_set_census.py [starts]"""
import json, os, sys
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
s1 = open(os.path.join(HERE, "w33_regulus_f8_and_quotient.py"), encoding="utf-8").read(); g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_f8_and_quotient.py")}
exec(s1[: s1.index("rng = np.random.default_rng(0); res = {}; t0")], g)
exec(s1[s1.index("pos5, sing5"): s1.index("def span(")], g)
exec(s1[s1.index("def invariants5"): s1.index("def quotient(p)")], g)
s2 = open(os.path.join(HERE, "w33_five_qubit_quotient_sets_minF.py"), encoding="utf-8").read(); h = {"__name__": "x", "__file__": os.path.join(HERE, "w33_five_qubit_quotient_sets_minF.py")}
exec(s2[: s2.index("q = json.load")], h)
starts = int(sys.argv[1]) if len(sys.argv) > 1 else 16
ns5, sing5 = g["ns5"], g["sing5"]
def maximal(codes):
    comp = np.ones(len(ns5), bool)
    for c in codes: comp &= ~sing5[ns5 ^ c]
    comp &= ~np.isin(ns5, codes)
    pair = all(not sing5[a ^ b] for i, a in enumerate(codes) for b in codes[i + 1:])
    return bool(comp.sum() == 0 and pair and all(not sing5[c] for c in codes))
L = lambda f: json.load(open(os.path.join(ROOT, "data", f)))
sets = {"pass12650": L("w33_five_qubit_size9_verify.json")["example"]}
qm = L("w33_five_qubit_quotient_sets_minF.json"); sets["quotient27"] = qm["quotient_type27"]["codes"]; sets["quotient17"] = qm["quotient_type17"]["codes"]
for i, s in enumerate(L("w33_five_qubit_floor24.json")["states"]):
    E = s["E"]; iso = [t for t in E if all(sing5[t ^ u] for u in E if u != t)]
    for t in iso[:1]: sets[f"floor24_{i}"] = list(s["S"]) + [t]
for f, nm in (("w33_five_qubit_size9_dlx.json", "dlx_forward"), ("w33_five_qubit_size9_dlx_reverse.json", "dlx_reverse")):
    ex = L(f)["control_n5_size9"]["example"]; sets[nm] = ex
I5 = sum(1 << b for b, (i, j) in enumerate(g["pos5"]) if i == j)
out = []
for name, codes in sets.items():
    codes = [int(c) for c in codes]
    if len(codes) != 7 or not maximal(codes): print(name, "skipped (size", len(codes), "maximal", maximal(codes) if len(codes) == 7 else None, ")", flush=True); continue
    cov = set().union(*g["lags_from_codes"](5, codes)) - {0}
    inv = g["invariants5"](cov); mf = h["minF"](codes, starts=starts)
    rec = dict(name=name, vanishing_quadrics=inv["vanishing_quadrics"], n_simple_eigs=inv["n_simple_eigs"], top=inv["top_multiplicities"][:3], c=mf["times_32"], levels=mf["levels_times_32"][:4])
    out.append(rec); print(rec, flush=True)
    json.dump(out, open(os.path.join(ROOT, "data", "w33_five_qubit_nine_set_census.json"), "w"), indent=1, default=float)
