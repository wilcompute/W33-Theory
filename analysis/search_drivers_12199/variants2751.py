"""12201 (WSL): Wilson-line variants of SM_2751 (all three generations untwisted) with a Wilson-line-trivial order-2 direction,
the necessary condition for a Scherk-Schwarz translation (W_2t in Gamma, V0-independent).  Classes: W6 = W5 + lam (t = (e5+e6)/2),
W6 = lam (t = e6/2), W5 = lam (t = e5/2), lam in {0} + small E8xE8 vectors.  Each variant: SUSY orbifolder SM analysis (specdump),
net quark doublets per sector.  usage: python3 variants2751.py NLAM OUTJSON"""
import itertools, json, os, re, subprocess, sys
from fractions import Fraction as F
sys.path.insert(0, '/mnt/c/tmp/toe_wt/analysis/orbifolder_n0_drivers')
import so16_bases as SB

NL, OUTJ = int(sys.argv[1]), sys.argv[2]
t = open(os.path.expanduser('~/orb/scan/sm/Z6II_24.txt')).read()
blk = [b for b in t.split('begin model')[1:] if 'Label:SM_20260917_2751\n' in b][0]
head = 'begin model' + blk.split('Shifts and Wilsonlines:')[0]
rows = [[F(x.strip(',')) for x in r.replace(',', ' ').split()] for r in blk.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().splitlines()]
W5, W6 = rows[6], rows[7]
roots = SB.e8_norm(2)
lams = [[F(0)] * 16] + [list(r) + [F(0)] * 8 for r in roots[:NL]] + [[F(0)] * 8 + list(r) for r in roots[:NL]]
lams += [[2 * x for x in l] for l in lams[1:NL // 2]]
OUT = os.path.expanduser('~/orb/p1109x/v2751'); os.makedirs(OUT, exist_ok=True)
res = []
for cls in ('W6=W5+lam', 'W6=lam', 'W5=lam'):
    for j, lam in enumerate(lams):
        r = [list(x) for x in rows]
        if cls == 'W6=W5+lam':
            r[7] = [a + b for a, b in zip(W5, lam)]
        elif cls == 'W6=lam':
            r[7] = lam
        else:
            r[6] = lam
        path = f'{OUT}/v_{cls.replace("=", "").replace("+", "p")}_{j}.txt'
        open(path, 'w').write(head.replace('Label:SM_20260917_2751', f'Label:v{j}') + 'Shifts and Wilsonlines:\n' + '\n'.join(' '.join(str(x) for x in v) for v in r) + '\nend model\n')
        o = subprocess.run(['./specdump', path], cwd=os.path.expanduser('~/orb/build'), capture_output=True, text=True, timeout=1800)
        rec = dict(cls=cls, j=j, rc=o.returncode)
        if o.returncode == 0:
            sec = {}
            for l in o.stdout.splitlines():
                m = re.match(r'S (b?)q_\d+ k=(\d+) susy=\d+ dim=(\S+)', l)
                if m:
                    tot = 1
                    for x in m.group(3).split(','):
                        tot *= abs(int(re.match(r'-?\d+', x).group(0)))
                    sec[int(m.group(2))] = sec.get(int(m.group(2)), 0) + (-1 if m.group(1) else 1) * tot // 6
            rec.update(SM=True, sectors=sec, even=sum(v for k, v in sec.items() if k % 2 == 0), odd=sum(v for k, v in sec.items() if k % 2))
        else:
            rec.update(SM=False, out=o.stdout.strip()[:40])
        res.append(rec)
        print(rec, flush=True)
        json.dump(res, open(OUTJ, 'w'), indent=1)
print('DONE')
