"""12283: for every consistent Z2xZ2 relabelling with B != 0, classify the commuting pairs (g, h) with B(g,h) != 0 by the type of g:
'translation' (g = pure lattice translation, which commutes with h only along h's fixed torus), 'witten' (pure Witten element, possibly
with translation) or 'twisted' (g carries a point-group twist).  Hypothesis: the 3 relabellings with an unchanged spectrum have torsion
only on translations (acting on Kaluza-Klein/winding modes along the fixed torus, not on the massless level)."""
import json, sys, collections
import numpy as np
sys.path.insert(0, '../search_drivers_12274')
from torsion_B import table, diff_relabel
R = '../search_drivers_12271/'
d = json.load(open('../search_drivers_12274/correlate.json'))
tab = collections.Counter(); rows = {}
for r in d['rows']:
    if not r['lab'].startswith('ctrl') or not r['nonzeroB']:
        continue
    i = int(r['lab'][4:7])
    r0, S, lam = diff_relabel(R + f'even/{i:03d}_s0.txt', R + f'relabel/{r["lab"]}.txt')
    blocks, _ = table(r0, 'Z2xZ2', S, lam)
    I = np.eye(6, dtype=np.int64)
    types = collections.Counter()
    for hb in blocks:
        if hb['ti'] == 0:
            continue
        for gb in blocks:
            A = gb['labs'] @ (I - hb['M']).T; Bf = hb['labs'] @ (I - gb['M']).T
            keyA = collections.defaultdict(list)
            for k, row in enumerate(map(tuple, A)):
                keyA[row].append(k)
            for j, row in enumerate(map(tuple, Bf)):
                gi = keyA.get(row)
                if not gi:
                    continue
                gi = np.array(gi)
                num = (gb['sig'][gi] * hb['VL'][j] - hb['sig'][j] * gb['VL'][gi]) % 48
                n = int((num != 0).sum())
                if n:
                    t = 'twisted' if gb['ti'] else ('witten' if gb['e'] else 'translation')
                    types[t] += n
    key = tuple(sorted(types))
    tab[(r['spectrum'], key)] += 1
    rows[r['lab']] = dict(spectrum=r['spectrum'], types=dict(types))
for k, v in sorted(tab.items(), key=str):
    print(v, k)
json.dump(dict(table={str(k): v for k, v in tab.items()}, rows=rows), open('gtype.json', 'w'), indent=1)
