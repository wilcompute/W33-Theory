import sys, json
import sympy as sp
from fractions import Fraction as Fr
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import hyper as H


def netof(r, c):
    from collections import Counter
    cnt = Counter()
    for cc in r['comps']:
        Y = H.dot(c, cc['t'])
        cnt[(cc['dc'], cc['dl'], Y)] += cc['k'] // (abs(cc['dc']) * cc['dl'])
    net, done = {}, set()
    for key in cnt:
        if key in done:
            continue
        dc, dl, Y = key
        conj = ((-dc if abs(dc) == 3 else dc), dl, -Y)
        done |= {key, conj}
        if key == conj:
            continue
        d = cnt.get(key, 0) - cnt.get(conj, 0)
        if d:
            net[key if d > 0 else conj] = abs(d)
    return net


res = {}
for m in sys.argv[1:]:
    r = H.analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    B = r['basis']
    # trace anomalies of each basis direction over left fermions (all weights)
    tr = [sum(H.dot(b, w) for f in r['left'] for w in f['W']) for b in B]
    anom = [i for i, t in enumerate(tr) if t != 0]
    # anomalous direction: vector of traces in y-space -> y_anom = sum tr_i * (dual)... use condition Tr Y = 0 automatically; GS needs y . t_A = 0
    tA = [sum(tr[i] * B[i][x] for i in range(len(B))) for x in range(16)]
    best = []
    for s in r['sols']:
        if not H.is_sm(s['net']):
            continue
        aff = s['aff']
        n = len(B)
        piv = [p for p, _, _ in aff.rows]
        freev = [i for i in range(n) if i not in piv]
        # c = c0 + sum t_j d_j ; d_j: free var j = 1, pivots from rows
        c0 = aff.particular()
        dirs = []
        for j in freev:
            d = [Fr(0)] * n
            d[j] = Fr(1)
            for p, w, _ in aff.rows:
                d[p] = -w[j]
            dirs.append(d)
        Bm = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in b] for b in B])
        G = Bm * Bm.T
        c0m = sp.Matrix([sp.Rational(x.numerator, x.denominator) for x in c0])
        if dirs:
            D = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in d] for d in dirs]).T
            tt = sp.symbols('t0:%d' % len(dirs))
            cm = c0m + D * sp.Matrix(tt)
            f = (cm.T * G * cm)[0]
            sol = sp.solve([sp.diff(f, t) for t in tt], tt, dict=True)[0]
            cmin = cm.subs(sol)
        else:
            cmin = c0m
        c = [Fr(int(sp.fraction(x)[0]), int(sp.fraction(x)[1])) for x in cmin]
        y = [sum(ci * b[x] for ci, b in zip(c, B)) for x in range(16)]
        ok = H.is_sm(netof(r, c))
        yA = H.dot(y, tA)
        best.append((H.dot(y, y), ok, yA == 0, [str(v) for v in y]))
    best.sort(key=lambda t: t[0])
    good = [b for b in best if b[1] and b[2]]
    res[m] = dict(n_exact=len(best), n_exact_orth_anomalous=len(good), min_y2_exact=str(best[0][0]) if best else None,
                  min_y2_good=str(good[0][0]) if good else None, y_good=good[0][3] if good else None,
                  k_Y_min_good=str(2 * good[0][0]) if good else None, anomalous_basis=anom)
    print(m, {k: v for k, v in res[m].items() if k != 'y_good'}, flush=True)
json.dump(res, open(r'C:\tmp\toe_round\stype\hyper3_4.json', 'w'), indent=1)
