"""12373 (WSL): a targeted Witten-shift search.  For the SUSY Z6-II parents of the three-doublet lineages (SM_2913, SM_2618, SM_2503,
SM_574, SM_1105; W6 = 0), enumerate ALL admissible V0 = (a; b) in (1/2){norm-4 E8 vectors}^2 with V0 . V, V0 . W_i integral (the 12180
construction, which sampled only <= 400 per parent), take a seeded random sample, and for each candidate: strict consistency
(nsocheck_strict), then the verbose dump (zero-mode tachyons T_NFIELDS, gauge group, field list).  Records the best net (3,2) count over
A2 x A1 choices (Weyl fermions m = 19, hidden multiplicity included).  usage: python3 newv0.py WORKER NWORKERS NSAMPLE"""
import os, re, sys, json, random, subprocess, itertools
from fractions import Fraction as F
sys.path.insert(0, '/mnt/c/tmp/toe_wt/analysis/orbifolder_n0_drivers')
import so16_bases as SB
WK, NW, NS = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/orb/libfix') + ':' + os.path.expanduser('~/orb/sysroot/usr/lib/x86_64-linux-gnu'))
OUT = os.path.expanduser('~/orb/newv0'); os.makedirs(OUT, exist_ok=True)
D = '/mnt/c/tmp/toe_wt/analysis/search_drivers_12373'
WANT = ('SM_20260917_2913', 'SM_20260917_2618', 'SM_20260917_2503', 'SM_20260917_574', 'SM_20260917_1105')
models = []
for f in sorted(x for x in os.listdir(os.path.expanduser('~/orb/scan/sm')) if x.startswith('Z6II_')):
    t = open(os.path.expanduser('~/orb/scan/sm/' + f)).read()
    for blk in t.split('begin model')[1:]:
        lab = re.search(r'Label:(\S+)', blk).group(1)
        if lab not in WANT: continue
        rows = blk.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().splitlines()
        rows = [[F(x.strip(',')) for x in r.replace(',', ' ').split()] for r in rows]
        if all(x == 0 for x in rows[7]):
            models.append((f[:-4] + '_' + lab, rows))
dot = lambda u, v: sum(a * b for a, b in zip(u, v))
def all_candidates(shifts):
    ra = {}
    for a in SB.HALF:
        ra.setdefault(tuple(dot(a, V[:8]) % 1 for V in shifts), []).append(a)
    out = []
    for b in SB.HALF:
        need = tuple((-dot(b, V[8:])) % 1 for V in shifts)
        for a in ra.get(need, []):
            out.append(a + b)
    return out
def best32(dump):
    g = re.search(r'GAUGE (.*)', dump)
    fac = []
    for l in dump.splitlines():
        if l.startswith('FACTOR') or l.startswith('GAUGE'):
            pass
    flds = []
    for l in dump.splitlines():
        m = re.match(r'F m=(\d+) k=\d+ m=\d+ n=\d+ dim=(\S+) x(\d+)', l)
        if m and m.group(1) == '19':
            flds.append(([int(re.match(r'-?\d+', x).group(0)) for x in m.group(2).split(',')], int(m.group(3))))
    if not flds: return None, None
    n = len(flds[0][0]); best = 0; arg = None
    for i3, i2 in itertools.permutations(range(n), 2):
        tot = 0; seen = False
        for d, x in flds:
            if abs(d[i3]) == 3 and abs(d[i2]) == 2:
                seen = True
                mult = 1
                for j, y in enumerate(d):
                    if j not in (i3, i2): mult *= abs(y)
                tot += (1 if d[i3] > 0 else -1) * x * mult
        if seen and abs(tot) > best: best, arg = abs(tot), (i3, i2)
    return best, arg
log = open(f'{D}/scan_{WK}.jsonl', 'a')
for lab, rows in models:
    V, W = rows[0], rows[2:8]
    cands = all_candidates([V] + W)
    cands = [c for c in cands if all(dot(c, s).denominator == 1 for s in [V] + W)]
    random.Random(12373).shuffle(cands)
    if WK == 0: print(lab, 'admissible V0:', len(cands), flush=True)
    for i, V0 in enumerate(cands[:NS]):
        if i % NW != WK: continue
        nrows = [list(V0), V, [F(0)] * 16] + W
        path = f'{OUT}/{lab}_c{i}.txt'
        open(path, 'w').write(SB.model_text(f'{lab}_c{i}', 'Geometry_Z6-II_1_1.txt', nrows))
        chk = subprocess.run(['./nsocheck_strict', path], cwd=os.path.expanduser('~/orb/nsostrict'), capture_output=True, text=True, env=env, timeout=600).stdout
        okc = re.search(r'^FILE \S+ \S+ (\S+)', chk, re.M)
        rec = dict(parent=lab, i=i, V0=SB.fmt(V0), strict=okc.group(1) if okc else None)
        if rec['strict'] == '1':
            try:
                d = subprocess.run(['./nsodump_verbose', path], cwd=os.path.expanduser('~/orb/nsoverb'), capture_output=True, text=True, env=env, timeout=1800).stdout
            except subprocess.TimeoutExpired:
                d = ''
            t = re.search(r'T_NFIELDS (\d+)', d); g = re.search(r'GAUGE (.*)', d)
            b, arg = best32(d)
            rec.update(T=int(t.group(1)) if t else None, gauge=g.group(1).strip() if g else None, best32=b, su3su2=arg)
        log.write(json.dumps(rec) + '\n'); log.flush()
print('DONE', WK)
