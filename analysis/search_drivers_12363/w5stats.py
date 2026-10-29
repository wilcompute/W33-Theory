"""12367: the order-2 Wilson line W5 on the theta^2-fixed torus versus three generations and radius-dependent tachyons (99 parents)."""
import json, os, collections
from fractions import Fraction as F
rows = json.load(open('combine.json'))['rows']
hits = {h[:-6] for h in json.load(open('../search_drivers_12338/gen3.json'))['hits']}
tab = collections.Counter(); out = {}
for m, r in rows.items():
    p = f'../search_drivers_12281/bro/{m}__ctrl.txt'
    if not os.path.exists(p): p = f'../search_drivers_12302/bro/{m}__ctrl.txt'
    L = open(p).read().split('\n'); i = L.index('Shifts and Wilsonlines:')
    W5 = [F(x) for x in L[i + 8].split()]; W3 = [F(x) for x in L[i + 6].split()]
    key = (any(W5), any(W3), m in hits, r['large_e5e6'] > 0, r['small_e5'] > 0)
    tab[key] += 1; out[m] = dict(W5=any(W5), W3=any(W3), three_doublets=m in hits, **r)
for k, v in sorted(tab.items()): print('W5', k[0], 'W3', k[1], '3-doublet', k[2], 'large-R tach', k[3], 'small-R tach', k[4], ':', v)
json.dump(dict(table={str(k): v for k, v in tab.items()}, rows=out), open('w5stats.json', 'w'), indent=1)
