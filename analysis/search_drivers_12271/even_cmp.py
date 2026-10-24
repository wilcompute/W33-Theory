"""compare stock-engine spectrum of each even-order input with the strict engine's spectra of its two repairs"""
import sys, json, collections
sys.path.insert(0, '../search_drivers_12267')
from cmp_census import load
res = collections.Counter(); rows = []
def same(x, y):
    if x[0] == y[0] and x[1] == y[1]: return 'identical'
    if x[2] == y[2]: return 'same sectors+dims, charges differ'
    return 'different spectrum'
def summary(x):
    gauge = [l for l in x[0] if l.startswith('GAUGE')][0]
    return gauge, sum(x[2].values())
for i in range(40):
    o, a, b = (load(f'even/{i:03d}_{s}.nsoq') for s in ('o', 's0', 's1'))
    r = dict(i=i, o_s0=same(o, a), o_s1=same(o, b), s0_s1=same(a, b), o=summary(o), s0=summary(a), s1=summary(b))
    rows.append(r); res[(r['o_s0'], r['o_s1'], r['s0_s1'])] += 1
for k, v in res.most_common(): print(v, k)
for r in rows:
    if 'different' in r['o_s0'] + r['o_s1'] + r['s0_s1']: print(r)
json.dump(dict(summary={str(k): v for k, v in res.items()}, rows=rows), open('even_cmp.json', 'w'), indent=1)
