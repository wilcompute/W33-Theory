"""12296: compare every Z4 brother's full field list (multiplet, sector, representation, U(1) charges) with its unshifted control."""
import json, collections
idx = json.load(open('z4_index.json'))
def load(p):
    t = open(p[:-4] + '.dump', errors='ignore').read().split('\n')
    if any(l.startswith('LOADFAIL') for l in t) or not any(l.startswith('END') for l in t):
        return None
    head = [l for l in t if l.startswith('GAUGE')]
    rnd = lambda s: ','.join(f'{round(float(x), 6) + 0.0:.6f}' for x in s.split(',') if x)
    f = collections.Counter()
    for l in t:
        if l.startswith('FIELD'):
            a, b = l.split(' q=')
            f[(a, rnd(b))] += 1
    return head, f
tab = collections.Counter(); per = []
for m in idx:
    ctrl = [b for b in m['brothers'] if b['trivial']][0]
    c = load(ctrl['file'])
    for b in m['brothers']:
        if b['trivial']:
            tab['control ' + ('loaded' if c else 'LOADFAIL')] += 1; continue
        x = load(b['file'])
        v = 'load failure' if x is None else ('identical' if x == c else 'changed')
        tab[v] += 1; per.append(dict(model=m['model'], j=b['j'], cls=b['cls'], verdict=v))
print(dict(tab))
json.dump(dict(table=dict(tab), rows=per), open('z4cmp.json', 'w'), indent=1)
