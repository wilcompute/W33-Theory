"""12374 (WSL): radius filters for the new candidates (T = 0 at the orbifold point, best net (3,2) = 3): large radius -- 6D theories of
both fixed tori (theta^2 sub-orbifold with W5 = W6 = 0; theta^3 with W3 = W4 = 0); small radius -- odd e5 winding, e3 winding classes 1, 2
(geometries of 12359 / 12366).  Writes filt.jsonl with T_NFIELDS for each test.  usage: python3 filt.py WORKER NWORKERS"""
import os, re, sys, json, subprocess, glob
from fractions import Fraction as F
WK, NW = int(sys.argv[1]), int(sys.argv[2])
env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/orb/libfix') + ':' + os.path.expanduser('~/orb/sysroot/usr/lib/x86_64-linux-gnu'))
D = '/mnt/c/tmp/toe_wt/analysis/search_drivers_12373'; OUT = os.path.expanduser('~/orb/newv0')
recs = [json.loads(l) for f in sorted(glob.glob(f'{D}/scan_*.jsonl')) for l in open(f)]
cand = [r for r in recs if r.get('T') == 0 and r.get('best32') == 3]
TESTS = dict(t3=(2, 'Geometry_Z6-II_sub2.txt', (7, 8)), t2=(3, 'Geometry_Z6-II_sub3.txt', (5, 6)), e5=(2, 'Geometry_Z6-II_win_e5.txt', ()),
             e3a=(3, 'Geometry_Z6-II_win_e3a.txt', ()), e3b=(3, 'Geometry_Z6-II_win_e3b.txt', ()))
log = open(f'{D}/filt_{WK}.jsonl', 'a')
for n, r in enumerate(cand):
    if n % NW != WK: continue
    base = f"{r['parent']}_c{r['i']}"
    L = open(f'{OUT}/{base}.txt').read().split('\n'); i = L.index('Shifts and Wilsonlines:')
    rows = [x.split() for x in L[i + 1:i + 10]]
    res = dict(base=base, V0=r['V0'], gauge=r['gauge'], su3su2=r['su3su2'])
    for tag, (s, geo, zero) in TESTS.items():
        rr = [list(x) for x in rows]; rr[1] = [str(F(x) * s) for x in rr[1]]
        for z in zero: rr[z] = ['0'] * 16
        out = list(L); out[i + 1:i + 10] = [' '.join(x) for x in rr]
        out = [l if not l.startswith('SpaceGroup') else f'SpaceGroup:Geometry/{geo}' for l in out]
        p = f'{OUT}/{base}__{tag}.txt'; open(p, 'w').write('\n'.join(out))
        try:
            d = subprocess.run(['./nsodump_verbose', p], cwd=os.path.expanduser('~/orb/nsoverb'), capture_output=True, text=True, env=env, timeout=1800).stdout
        except subprocess.TimeoutExpired:
            d = ''
        t = re.search(r'T_NFIELDS (\d+)', d); res[tag] = int(t.group(1)) if t else None
    log.write(json.dumps(res) + '\n'); log.flush()
print('DONE', WK)
