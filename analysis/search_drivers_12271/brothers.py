"""12272: distinct consistent spectra per even-order input among {repair s0, repair s1, two harmless-looking relabellings of s0} --
a lower bound on the number of torsion brothers sharing the input's Wilson-line classes mod the lattice."""
import sys, json, collections
sys.path.insert(0, '../search_drivers_12267')
from cmp_census import load
dist = collections.Counter(); per = []
for i in range(40):
    sp = [load(f'even/{i:03d}_s0.nsoq'), load(f'even/{i:03d}_s1.nsoq'), load(f'relabel/ctrl{i:03d}_r0.nsoq'), load(f'relabel/ctrl{i:03d}_r1.nsoq')]
    keys = {(x[0], frozenset(x[1].items())) for x in sp}
    counts = sorted({sum(x[2].values()) for x in sp})
    dist[len(keys)] += 1; per.append(dict(i=i, distinct=len(keys), field_counts=counts))
print('distinct consistent spectra per input (of 4 lifts):', dict(sorted(dist.items())))
json.dump(dict(distribution=dist, per=per), open('brothers.json', 'w'), indent=1)
