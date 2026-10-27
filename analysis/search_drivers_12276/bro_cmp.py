"""12276 (verdicts read from the .sd content via sdclass, not from shell exit codes): compare every brother with its own unshifted control (trivial class) under the strict SUSY engine."""
import json, re, collections, os
idx = json.load(open('brothers_index.json'))
from sdclass import sdclass
CODE = {'SM': 0, 'noSM': 3, 'load failure': 2}
rc = {}
for o in idx:
    p = o['file'][:-4] + '.sd'
    if os.path.exists(p):
        rc[os.path.basename(o['file'])] = CODE[sdclass(p)]
def spec(path):
    t = open(path).read().split('\n')
    full = collections.Counter(); inv = collections.Counter()
    for l in t:
        m = re.match(r'S (\S+?)_\d+ k=(\S+) susy=(\S+) dim=(\S*) q=(\S*)', l)
        if m:
            q = ','.join(f'{round(float(x), 6) + 0.0:.6f}' for x in m.group(5).split(',') if x)
            full[(m.group(1), m.group(2), m.group(3), m.group(4), q)] += 1
            inv[(m.group(2), m.group(3), m.group(4))] += 1
    return full, inv
tab = collections.Counter(); per = collections.defaultdict(lambda: collections.Counter()); newSM = []
ctrl = {}
for o in idx:
    if o['trivial']:
        ctrl[(o['model'], o['line'])] = o
for o in idx:
    b = os.path.basename(o['file'])
    r = rc.get(b)
    if r is None:
        tab['missing'] += 1; continue
    c = ctrl[(o['model'], o['line'])]
    rcc = rc.get(os.path.basename(c['file']))
    if o['trivial']:
        tab[('control', r)] += 1; continue
    if r == 2:
        v = 'inconsistent'
    elif r == 3:
        v = 'consistent, not an SM'
    elif r == 0 and rcc == 0:
        a = spec(o['file'][:-4] + '.sd'); z = spec(c['file'][:-4] + '.sd')
        v = 'SM, identical' if a[0] == z[0] else ('SM, same sectors+reps, charges differ' if a[1] == z[1] else 'SM, different spectrum')
        if v == 'SM, different spectrum':
            newSM.append(o['file'])
    else:
        v = f'rc={r}'
    tab[v] += 1; per[o['model']][v] += 1
for k, v in sorted(tab.items(), key=str): print(k, v)
print('models with a non-identical SM brother:', sum(1 for m in per if per[m]['SM, different spectrum'] or per[m]['SM, same sectors+reps, charges differ']))
json.dump(dict(table={str(k): v for k, v in tab.items()}, per_model={m: dict(c) for m, c in per.items()}, new_SM_brothers=newSM), open('bro_cmp.json', 'w'), indent=1)
