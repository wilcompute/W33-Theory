"""12199 (WSL): Scherk-Schwarz census of the 29 Z2xZ6-I W(3,3) Standard Models.  The SS translations live on plane 1 (SO4,
rotated only by the Z2 generator, Pass 12177 kernel); a translation t needs W_2t in Gamma (12180c lemma; W1, W2 = rows 2, 3).
The sectors with odd Z2 power k rotate plane 1, so the translation pairs and halves them.  Per model: SUSY spectrum (specdump),
net quark doublets (dimension weighted) at even / odd k, and which plane-1 directions are Wilson-line trivial."""
import json, os, re, subprocess, sys
from fractions import Fraction as F
os.environ['LD_LIBRARY_PATH'] = os.path.expanduser('~/orb/sysroot/usr/lib/x86_64-linux-gnu') + ':/tmp/su9/lib'


def in_e8(v):
    ints = all(x.denominator == 1 for x in v)
    halves = all(x.denominator == 2 for x in v)
    return (ints or halves) and sum(v) % 2 == 0


def in_gamma(w):
    return in_e8(w[:8]) and in_e8(w[8:])


D = os.path.expanduser('~/orb/scan/z2z6/sm')
res = {}
for f in sorted(os.listdir(D)):
    for i, blk in enumerate(open(f'{D}/{f}').read().split('begin model')[1:]):
        lab = f[:-4] + '__' + re.search(r'Label:(\S+)', blk).group(1)
        rows = [[F(x.strip(',')) for x in r.replace(',', ' ').split()] for r in blk.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().splitlines()]
        W1, W2 = rows[2], rows[3]
        path = '/tmp/z26_one.txt'
        open(path, 'w').write('begin model' + blk.split('end model')[0] + 'end model\n')
        o = subprocess.run(['./specdump', path], cwd=os.path.expanduser('~/orb/build'), capture_output=True, text=True, timeout=1800)
        sec = {}
        for l in o.stdout.splitlines():
            m = re.match(r'S (b?)q_\d+ k=(\d+) susy=\d+ dim=(\S+)', l)
            if m:
                tot = 1
                for x in m.group(3).split(','):
                    tot *= abs(int(re.match(r'-?\d+', x).group(0)))
                sec[int(m.group(2))] = sec.get(int(m.group(2)), 0) + (-1 if m.group(1) else 1) * tot // 6
        rec = dict(rc=o.returncode, sectors=sec, even=sum(v for k, v in sec.items() if k % 2 == 0), odd=sum(v for k, v in sec.items() if k % 2),
                   wl_trivial=dict(W1=in_gamma(W1), W2=in_gamma(W2), W12=in_gamma([a + b for a, b in zip(W1, W2)])))
        res[lab] = rec
        print(lab, rec, flush=True)
json.dump(res, open('z2z6census.json', 'w'), indent=1)
print('DONE')
