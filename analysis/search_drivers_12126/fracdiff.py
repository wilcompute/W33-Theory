import sys, json, itertools
from fractions import Fraction as Fr
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import hyper as H
res = {}
for m in sys.argv[1:]:
    fac, u1, fields = H.parse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    r = H.analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    col, L = [i for i, (n, _) in enumerate(fac) if n == 'A2'][0], r['L']
    aL = fac[L][1][0]
    allf = [f for f in fields if f['m'] in (19, 15, 16)]
    W = {w for f in allf for w in f['W']}
    ff = []
    for s in r['sols']:
        if not H.is_sm(s['net']):
            continue
        y = s['y']
        ok = True
        for f in allf:
            dc = abs(H.dsgn(f['dim'][col]))
            for w in f['W']:
                Q = H.dot(aL, w) / 2 + H.dot(y, w)
                if (dc == 1 and Q.denominator != 1) or (dc == 3 and ((3 * Q).denominator != 1 or Q.denominator == 1)):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            ff.append(y)
    ints = norms = 0
    for a, b in itertools.combinations(ff, 2):
        d = [x - z for x, z in zip(a, b)]
        ints += all(H.dot(d, w).denominator == 1 for w in W)
        norms += (H.dot(d, d) % 2 == 0)
    res[m] = dict(n_fraction_free=len(ff), pairs=len(ff) * (len(ff) - 1) // 2, integral_differences=ints, even_norm_differences=norms,
                  y2=sorted({str(H.dot(y, y)) for y in ff}, key=Fr))
    print(m, res[m], flush=True)
json.dump(res, open(r'C:\tmp\toe_round\stype\fracdiff.json', 'w'), indent=1)
