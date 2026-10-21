"""12139: fraction-free hypercharges in the 104 A8 models of 11095. Strict exact search (12121 method) with colour / SU(2)_L
fixed by the corpus (nsosm) hypercharge, Y in the U(1) span; then the fraction-free test on every massless state.
Control: the corpus hypercharge itself must be found among the exact SM solutions."""
import sys
import os
import glob
import json
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import hyper_a8 as H
import a8down as A


def slots(fac, left, y):
    best = None
    a2 = [i for i, (n, _) in enumerate(fac) if n == 'A2' and all(H.dot(y, rt) == 0 for rt in fac[i][1])]
    a1 = [i for i, (n, _) in enumerate(fac) if n == 'A1' and all(H.dot(y, rt) == 0 for rt in fac[i][1])]
    for c in a2:
        for l in a1:
            for cq in (3, -3):
                for yq in (Fr(1, 6), Fr(-1, 6)):
                    net = 0
                    for f in left:
                        if f['dim'][l] != '2':
                            continue
                        d = H.dsgn(f['dim'][c])
                        for w in f['W']:
                            if d == cq and H.dot(y, w) == yq:
                                net += 1
                            elif d == -cq and H.dot(y, w) == -yq:
                                net -= 1
                    if best is None or net > best[0]:
                        best = (net, c, l)
    return best[1], best[2]


def fractional(fields, col, aL, y):
    n = 0
    for f in fields:
        if f['m'] not in (19, 15, 16):
            continue
        dc = abs(H.dsgn(f['dim'][col]))
        for w in f['W']:
            Q = H.dot(aL, w) / 2 + H.dot(y, w)
            if (dc == 1 and Q.denominator != 1) or (dc == 3 and ((3 * Q).denominator != 1 or Q.denominator == 1)):
                n += 1
    return n


def run(lab):
    base = r'C:\tmp\toe_round\stype\a8\%s' % lab
    fac, u1, fields = H.parse(base + '.q')
    y0 = A.ydir(base + '.sm')
    left = [f for f in fields if f['m'] == 19]
    c, l = slots(fac, left, y0)
    aL = fac[l][1][0]
    r = H.analyse(base + '.q', c, l, cap=3000)
    exact = [s for s in r['sols'] if H.is_sm(s['net'])]
    ff = []
    found_corpus = False
    for s in exact:
        y = s['y']
        if all(a == b or a == -b for a, b in zip(y, y0)) and (y == y0 or y == [-v for v in y0]):
            found_corpus = True
        if fractional(fields, c, aL, y) == 0:
            ff.append(str(2 * H.dot(y, y)))
    return lab, dict(nsol=r['nsol'], n_exact=len(exact), corpus_Y_found=found_corpus, corpus_Y_fractional=fractional(fields, c, aL, y0),
                     corpus_kY=str(2 * H.dot(y0, y0)), n_fraction_free=len(ff), kY_fraction_free=sorted(set(ff), key=Fr), capped=r['nsol'] > 3000)


if __name__ == '__main__':
    labs = sorted(os.path.basename(p)[:-2] for p in glob.glob(r'C:\tmp\toe_round\stype\a8\*.q'))
    if len(sys.argv) > 1:
        labs = labs[:int(sys.argv[1])]
    with Pool(4) as p:
        res = {}
        for lab, v in p.imap_unordered(run, labs):
            res[lab] = v
            print(lab, v, flush=True)
    json.dump(res, open(r'C:\tmp\toe_round\stype\a8ff.json', 'w'), indent=1)
    print('DONE')
