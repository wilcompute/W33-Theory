import sys, json
from fractions import Fraction as Fr
from collections import Counter
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import hyper as H
res = {}
for m in sys.argv[1:]:
    fac, u1, fields = H.parse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    r = H.analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    col, L = [i for i, (n, _) in enumerate(fac) if n == 'A2'][0], r['L']
    aL = fac[L][1][0]
    allf = [f for f in fields if f['m'] in (19, 15, 16)]
    stats = []
    for s in r['sols']:
        if not H.is_sm(s['net']):
            continue
        y = s['y']
        frac = 0
        for f in allf:
            dc = abs(H.dsgn(f['dim'][col]))
            for w in f['W']:
                Q = H.dot(aL, w) / 2 + H.dot(y, w)
                if (dc == 1 and Q.denominator != 1) or (dc == 3 and (3 * Q).denominator != 1) or (dc == 3 and Q.denominator == 1):
                    frac += 1
        stats.append((frac, str(2 * s['y2'])))
    stats.sort()
    res[m] = dict(n_exact=len(stats), n_no_fractional=sum(1 for f, _ in stats if f == 0), kY_of_fraction_free=sorted({k for f, k in stats if f == 0}, key=Fr))
    print(m, res[m], flush=True)
json.dump(res, open(r'C:\tmp\toe_round\stype\fraccheck.json', 'w'), indent=1)
