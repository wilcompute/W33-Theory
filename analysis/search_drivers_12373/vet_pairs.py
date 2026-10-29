"""12374d: every (SU(3), SU(2)) factor pairing with |net (3,2)| = 3 (not only the first found), base hypercharge search, for the 59
exotic-free large-radius-safe candidates; the Y-independent exotic test is re-run per pairing."""
import json, os, re, subprocess, sys, collections, itertools, glob
v = json.load(open('vet.json'))
todo = [b for b, r in v.items() if not r['y_independent_exotics']]
out = {}
for b in todo:
    L = open(f'spec/{b}.nsoq', errors='ignore').read().split('\n')
    fac = [l.split()[2] for l in L if l.startswith('FACTOR')]
    c = collections.Counter()
    for l in L:
        m = re.match(r'FIELD \d+ m=19 k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*)', l)
        if m: c[tuple(int(re.match(r'-?\d+', x).group(0)) for x in m.group(1).split(','))] += 1
    cj = lambda d: tuple(-x if abs(x) > 2 else x for x in d)
    res = []
    for i3, i2 in itertools.product([i for i, f in enumerate(fac) if f == 'A2'], [i for i, f in enumerate(fac) if f == 'A1']):
        net = sum(n * (1 if d[i3] > 0 else -1) * int(__import__('math').prod(abs(x) for j, x in enumerate(d) if j not in (i3, i2)))
                  for d, n in c.items() if abs(d[i3]) == 3 and abs(d[i2]) == 2)
        if abs(net) != 3: continue
        ex = any((n - c.get(cj(d), 0)) for d, n in c.items() if cj(d) != d and (abs(d[i3]) > 1 or abs(d[i2]) > 1)
                 and any(abs(x) > 1 for j, x in enumerate(d) if j not in (i3, i2)))
        k = None
        if not ex:
            env = dict(os.environ, YS_NSOQ=f'../search_drivers_12373/spec/{b}.nsoq')
            subprocess.run([sys.executable, 'ysearch.py', b, str(i3), str(i2), '1'], cwd='../search_drivers_12364', env=env, capture_output=True, text=True, timeout=3000)
            k = [s['kY'] for s in json.load(open(f'../search_drivers_12364/ysearch_{b}.json'))['solutions']]
        res.append(dict(su3=i3, su2=i2, exotics=bool(ex), hypercharges=k))
    out[b] = res
    print(b, res, flush=True)
json.dump(out, open('vet_pairs.json', 'w'), indent=1)
print('any pairing with a hypercharge:', [b for b, r in out.items() if any(x['hypercharges'] for x in r)])
