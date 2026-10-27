"""12298: score the pre-registered predictions (predictions.json, committed before the engine run) against the strict SUSY engine."""
import json, collections, sys
sys.path.insert(0, '../search_drivers_12296')
pred = json.load(open('predictions.json'))
def load(p):
    t = open(p[:-4] + '.dump', errors='ignore').read().split('\n')
    if any(l.startswith('LOADFAIL') for l in t) or not any(l.startswith('END') for l in t):
        return None
    rnd = lambda s: ','.join(f'{round(float(x), 6) + 0.0:.6f}' for x in s.split(',') if x)
    f = collections.Counter()
    for l in t:
        if l.startswith('FIELD'):
            a, b = l.split(' q='); f[(a, rnd(b))] += 1
    return [l for l in t if l.startswith('GAUGE')], f
ctrl = {p['model']: load(p['file']) for p in pred if p['trivial']}
tab = collections.Counter()
for p in pred:
    if p['trivial']:
        tab[('control', 'loaded' if ctrl[p['model']] else 'LOADFAIL')] += 1; continue
    x = load(p['file'])
    obs = 'load failure' if x is None else ('identical' if x == ctrl[p['model']] else 'changed')
    tab[(p['prediction'], obs)] += 1
for k, v in sorted(tab.items()): print(k, v)
json.dump({str(k): v for k, v in tab.items()}, open('score.json', 'w'), indent=1)
