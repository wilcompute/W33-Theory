"""12374b: for each large-radius-safe candidate, (i) hypercharge-independent chiral exotics: net chirality of states charged under the
SM SU(3) or SU(2) AND a hidden non-abelian factor (fatal for every Y); (ii) the exact hypercharge search of 12364 (YS_NSOQ path)."""
import json, glob, re, os, subprocess, collections, sys
F = {json.loads(l)['base']: json.loads(l) for f in glob.glob('filt_*.jsonl') for l in open(f)}
safe = [l.strip() for l in open('large_safe.txt') if l.strip()]
out = {}
for b in safe:
    r = F[b]; i3, i2 = r['su3su2']
    c = collections.Counter()
    for l in open(f'spec/{b}.nsoq', errors='ignore'):
        m = re.match(r'FIELD \d+ m=19 k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*)', l)
        if m: c[tuple(int(re.match(r'-?\d+', x).group(0)) for x in m.group(1).split(','))] += 1
    cj = lambda d: tuple(-x if abs(x) > 2 else x for x in d)
    ex = {}
    for d, n in c.items():
        hid = any(abs(x) > 1 for j, x in enumerate(d) if j not in (i3, i2)); sm = abs(d[i3]) > 1 or abs(d[i2]) > 1
        if hid and sm and cj(d) != d:
            net = n - c.get(cj(d), 0)
            if net and str(cj(d)) not in ex: ex[str(d)] = net
    rec = dict(all_radius=(r['e5'] + r['e3a'] + r['e3b'] == 0), y_independent_exotics=ex)
    if not ex:
        env = dict(os.environ, YS_NSOQ=f'../search_drivers_12373/spec/{b}.nsoq')
        p = subprocess.run([sys.executable, 'ysearch.py', b, str(i3), str(i2), '2'], cwd='../search_drivers_12364', env=env, capture_output=True, text=True, timeout=3000)
        sols = json.load(open(f'../search_drivers_12364/ysearch_{b}.json'))['solutions']
        rec['hypercharges'] = [s['kY'] for s in sols]
    out[b] = rec
    print(b, 'all-radius' if rec['all_radius'] else 'large-R', 'exotics' if ex else '', rec.get('hypercharges'), flush=True)
json.dump(out, open('vet.json', 'w'), indent=1)
s = collections.Counter((v['all_radius'], bool(v['y_independent_exotics']), bool(v.get('hypercharges'))) for v in out.values())
print('(all-radius, Y-indep exotics, hypercharge found):', dict(s))
