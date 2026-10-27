"""12281: compare control / even / odd / w6odd brothers of the non-SUSY Z6-II models (strict engine nsoq dumps), and record for each
the tachyon-type and fermion/boson component counts -- a brother that removes all tachyons would be a new candidate."""
import json, sys, os, collections
sys.path.insert(0, '../search_drivers_12267'); sys.path.insert(0, '../search_drivers_12277')
from cmp_census import load
from bf_count import count
idx = json.load(open('census_index.json'))
tab = collections.Counter(); rows = []
done = lambda p: os.path.exists(p) and open(p, errors='ignore').read().rstrip().endswith('END')
for e in idx:
    f = {k: v[:-4] + '.nsoq' for k, v in e['files'].items()}
    if not done(f['ctrl']):
        continue
    c = load(f['ctrl']); cc = count(f['ctrl'])
    r = dict(model=e['model'], ctrl=dict(tach=cc['tachyon'] + cc['excited tachyon'], nF=cc['fermion']))
    for tag in ('even', 'odd', 'w6odd'):
        if tag not in f or not done(f[tag]):
            continue
        x = load(f[tag]); xc = count(f[tag])
        v = 'identical' if (x[0] == c[0] and x[1] == c[1]) else 'changed'
        tab[(tag, v)] += 1
        r[tag] = dict(verdict=v, tach=xc['tachyon'] + xc['excited tachyon'], nF=xc['fermion'])
        if v == 'changed' and r[tag]['tach'] == 0:
            tab[(tag, 'changed and tachyon-free')] += 1
    tab['ctrl tachyon-free'] += r['ctrl']['tach'] == 0
    rows.append(r)
for k, v in sorted(tab.items(), key=str):
    print(k, v)
json.dump(dict(table={str(k): v for k, v in tab.items()}, rows=rows), open('census_cmp.json', 'w'), indent=1)
