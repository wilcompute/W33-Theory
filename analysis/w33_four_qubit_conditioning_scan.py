"""Pass 12653: the conditioning route (w33_five_qubit_conditioning_scan.py) at EVERY uncovered point of the four-qubit types A and B
of Pass 12648.  Best route bound 21 > 14 for both, so conditioning alone cannot give type B's exact 1/16.  usage: py -3 analysis/w33_four_qubit_conditioning_scan.py"""
import json, os, sys, numpy as np
sys.argv = ['x', '0']
src = open('analysis/w33_five_qubit_conditioning_scan.py', encoding='utf-8').read()
g = {'__name__': 'y', '__file__': os.path.abspath('analysis/w33_five_qubit_conditioning_scan.py')}
exec(src[: src.index('rng = np.random.default_rng(0); t0')], g)
ex4 = {"__name__": "x", "__file__": os.path.abspath("analysis/w33_exhaustive_small_maximal_spreads.py")}
s4 = open("analysis/w33_exhaustive_small_maximal_spreads.py", encoding="utf-8").read(); exec(s4[: s4.index("def decide")], ex4)
lags4, _ = ex4["lagrangians"](4)
census = json.load(open("data/w33_four_qubit_size5_census.json"))
rng = np.random.default_rng(0); out = {}
for name, t in zip(("A", "B"), census["types"]):
    lags = [frozenset(lags4[i]) for i in t["example"]]; C = set().union(*lags) - {0}
    rows = [g['analyse'](4, lags, p, rng, starts=6) for p in range(1, 256) if p not in C]
    best = min(rows, key=lambda r: r['route_bound'])
    from collections import Counter
    prof = Counter((tuple(sorted(r['coset_multiplicities'].items())), round(r['lam_B'], 3), round(r['kappa_A'], 3), round(r['route_bound'], 3)) for r in rows)
    out[name] = dict(best=best, profiles=[dict(mult=str(k[0]), lam_B=k[1], kappa_A=k[2], route=k[3], count=v) for k, v in prof.items()])
    print(name, 'best', round(best['route_bound'], 4)); [print('  ', p) for p in out[name]['profiles']]
json.dump(out, open('data/w33_four_qubit_conditioning_scan.json', 'w'), indent=1, default=float)
