"""12143: why no fraction-free hypercharge has k_Y = 5/3. Every admissible k_Y = 5/3 candidate is a root v (q +- lambda = v, v.r fixed
for every nonabelian root). For each: does it give the SM net spectrum, and in which orbifold sectors does it leave fractionally
charged massless states?"""
import sys
import os
import glob
import json
from fractions import Fraction as Fr
from collections import Counter
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, r'C:\tmp\toe_round\stype')
os.environ['NMAX'] = '2'
import latff as LF
import hyper_a8 as H


def analyse(qpath, col, L):
    LF.E8 = LF.e8_upto(2)
    fac, u1, fields = H.parse(qpath)
    left = [f for f in fields if f['m'] == 19]
    a, b = fac[col][1][0], fac[col][1][1]
    aL = fac[L][1][0]
    lam1 = [(2 * x + z) / 3 for x, z in zip(a, b)]
    roots = [r for _, rts in fac for r in rts]
    cands = []
    seen = set()
    for sg in (1, -1):
        p = [sg * l + x / 2 for l, x in zip(lam1, aL)]
        for v8 in LF.E8:
            for h in (0, 1):
                v = [Fr(0)] * 16
                for k in range(8):
                    v[8 * h + k] = Fr(int(v8[k]), 2)
                if sum(x * x for x in v) != 2:
                    continue
                if any(H.dot(v, r) != H.dot(p, r) for r in roots):
                    continue
                y = [x - z for x, z in zip(v, p)]
                if tuple(y) in seen:
                    continue
                seen.add(tuple(y))
                sm = H.is_sm(LF.net_of(left, y, col, L))
                frac = Counter()
                for f in fields:
                    if f['m'] not in (19, 15, 16):
                        continue
                    dc = abs(H.dsgn(f['dim'][col]))
                    for w in f['W']:
                        Q = H.dot(aL, w) / 2 + H.dot(y, w)
                        if (dc == 1 and Q.denominator != 1) or (dc == 3 and ((3 * Q).denominator != 1 or Q.denominator == 1)):
                            frac[('U' if f['n'] == 0 and f['mm'] == 0 else 'W' if f['n'] == 0 else 'T%d%s' % (f['n'], 'b' if f['mm'] else ''))] += 1
                cands.append(dict(sm=sm, frac_sectors=dict(frac)))
    return cands


def run_a8(lab):
    import a8ff
    import a8down as A
    base = r'C:\tmp\toe_round\stype\a8\%s' % lab
    fac, u1, fields = H.parse(base + '.q')
    y0 = A.ydir(base + '.sm')
    c, l = a8ff.slots(fac, [f for f in fields if f['m'] == 19], y0)
    return lab, analyse(base + '.q', c, l)


def summarize(cands):
    return dict(n=len(cands), sm=sum(c['sm'] for c in cands), fraction_free=sum(1 for c in cands if not c['frac_sectors']),
                untwisted_fractional=sum(1 for c in cands if c['frac_sectors'].get('U')),
                sectors=dict(Counter(s for c in cands for s in c['frac_sectors'])))


if __name__ == '__main__':
    out = {}
    for m in ['N004_F1_03_S002', 'N008_F1_03_S033', 'N008_F1_04_S037', 'N008_F1_02_S053', 'N008_F1_04_S037_T115']:
        fac, u1, fields = H.parse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
        import hyper
        r = hyper.analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
        col = [i for i, (n, _) in enumerate(fac) if n == 'A2'][0]
        out[m] = summarize(analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m, col, r['L']))
        print(m, out[m], flush=True)
    labs = sorted(os.path.basename(p)[:-2] for p in glob.glob(r'C:\tmp\toe_round\stype\a8\*.q'))
    with Pool(6) as pool:
        for lab, c in pool.imap_unordered(run_a8, labs):
            out[lab] = summarize(c)
    tot = Counter()
    for k, v in out.items():
        if k.startswith('A8'):
            tot['n'] += v['n']; tot['sm'] += v['sm']; tot['ff'] += v['fraction_free']; tot['untw_frac'] += v['untwisted_fractional']
    print('A8 totals', dict(tot))
    print('A8 sectors', Counter(s for k, v in out.items() if k.startswith('A8') for s in v['sectors']))
    json.dump(out, open(r'C:\tmp\toe_round\stype\kyroot.json', 'w'), indent=1)
    print('DONE')
