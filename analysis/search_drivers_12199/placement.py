"""12200: generation placement of the 128 Z6-II W(3,3) Standard Models.  For each parent: net quark doublets per sector k
(dimension weighted, .sp spectra) and which order-2 directions are Wilson-line trivial (W5, W6, W5 + W6 in Gamma).
Prediction (pairing): if some direction is WL-trivial, the odd-sector net is even."""
import json, re, subprocess
from collections import Counter, defaultdict
from fractions import Fraction as F


def in_e8(v):
    ints = all(x.denominator == 1 for x in v)
    halves = all(x.denominator == 2 for x in v)
    return (ints or halves) and sum(v) % 2 == 0


def in_gamma(w):
    return in_e8(w[:8]) and in_e8(w[8:])


sh = ("cd ~/orb/scan/cp2/sp && for f in *.sp; do echo \"FILE $f\"; grep -hE '^S b?q_' $f | cut -d' ' -f2-5; done; "
      "cd ~/orb/scan/sm && for f in Z6II_*.txt; do echo \"BASE ${f%.txt}\"; cat $f; done")
o = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
spec, cur = {}, None
for l in o.splitlines():
    if l.startswith('FILE '):
        cur = l[5:-3]; spec[cur] = defaultdict(int); continue
    m = re.match(r'(b?)q_\d+ k=(\d+) susy=\d+ dim=(\S+)', l)
    if m and cur:
        tot = 1
        for x in m.group(3).split(','):
            tot *= abs(int(re.match(r'-?\d+', x).group(0)))
        spec[cur][int(m.group(2))] += (-1 if m.group(1) else 1) * tot // 6
wl = {}
labs_seen = Counter()
for part in o.split('BASE ')[1:]:
  base = part.split()[0]
  for blk in part.split('begin model')[1:]:
    lab = base + '__' + re.search(r'Label:(\S+)', blk).group(1)
    labs_seen[re.search(r'Label:(\S+)', blk).group(1)] += 1
    rows = blk.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().splitlines()
    rows = [[F(x.strip(',')) for x in r.replace(',', ' ').split()] for r in rows]
    W5, W6 = rows[6], rows[7]
    wl[lab] = dict(W5=in_gamma(W5), W6=in_gamma(W6), W56=in_gamma([a + b for a, b in zip(W5, W6)]))
res = {}
for k, v in spec.items():
    lab = k
    odd = sum(n for s, n in v.items() if s % 2)
    res[k] = dict(sectors=dict(v), even=sum(n for s, n in v.items() if s % 2 == 0), odd=odd, wl=wl.get(lab))
tab = Counter((r['even'], r['odd'], any(r['wl'].values()) if r['wl'] else None) for r in res.values())
print('duplicate labels across bases:', sum(1 for v in labs_seen.values() if v > 1), 'missing wl:', sum(1 for k in spec if k not in wl))
print('(even, odd, some WL-trivial direction):', sorted(tab.items()))
print('sector patterns:', Counter(tuple(sorted((s, n) for s, n in r['sectors'].items() if n)) for r in res.values()).most_common(8))
viol = [k for k, r in res.items() if r['wl'] and any(r['wl'].values()) and r['odd'] % 2]
print('parity-prediction violations:', viol)
json.dump(res, open('placement.json', 'w'), indent=1)
