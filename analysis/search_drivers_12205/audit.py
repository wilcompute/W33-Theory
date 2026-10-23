"""12205: audit of the Z6-II directions with the refined criterion of 12199b: W_2t in Gamma AND every product of W_2t with
V and W1..W6 (and W_2t^2/2) even.  Per parent and direction (W5, W6, W5+W6): refined-trivial or not; paired-sector parity
(12200 placement.json) must be even exactly when some direction is refined-trivial."""
import json, re
from collections import Counter
from fractions import Fraction as F

pl = json.load(open('../search_drivers_12199/placement.json'))
dot = lambda a, b: sum(x * y for x, y in zip(a, b))


def in_e8(v):
    return (all(x.denominator == 1 for x in v) or all(x.denominator == 2 for x in v)) and sum(v) % 2 == 0


res = {}
txt = open('z6ii_sm_all.txt').read()
for part in txt.split('BASE ')[1:]:
    base = part.split()[0]
    for blk in part.split('begin model')[1:]:
        lab = base + '__' + re.search(r'Label:(\S+)', blk).group(1)
        rows = [[F(x.strip(',')) for x in s.replace(',', ' ').split()] for s in blk.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().splitlines()]
        V, Ws = rows[0], rows[2:8]
        dirs = {}
        for name, w in (('W5', Ws[4]), ('W6', Ws[5]), ('W5+W6', [a + b for a, b in zip(Ws[4], Ws[5])])):
            if not (in_e8(w[:8]) and in_e8(w[8:])):
                continue
            prods = [dot(w, V)] + [dot(w, x) for x in Ws] + [dot(w, w) / 2]
            dirs[name] = all(p.denominator == 1 and p % 2 == 0 for p in prods)
        r = pl[lab]
        res[lab] = dict(gamma_dirs=sorted(dirs), refined_dirs=sorted(k for k, v in dirs.items() if v), even=r['even'], odd=r['odd'])
gam = [r for r in res.values() if r['gamma_dirs']]
ref = [r for r in res.values() if r['refined_dirs']]
print('parents', len(res), 'Gamma-valued direction', len(gam), 'refined-trivial direction', len(ref))
print('refined-trivial generations:', Counter((r['even'], r['odd']) for r in ref))
print('Gamma-only (not refined) generations:', Counter((r['even'], r['odd']) for r in gam if not r['refined_dirs']))
viol = [k for k, r in res.items() if r['refined_dirs'] and r['odd'] % 2]
print('refined-trivial with odd paired net (violations):', viol)
json.dump(res, open('audit.json', 'w'), indent=1)
