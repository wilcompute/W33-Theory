"""12150: the beta-theta obstruction as a lattice congruence. For a k_Y = 5/3 candidate v (a root, q = v -+ lambda), a colour-singlet
state of weight w = pi + U_f (pi in E8 x E8, U_f = V0 + V1 + sum c_i W_i the local shift of the beta-theta fixed point f) has
Q = v.w = v.pi + v.U_f, so it is integral iff v.U_f in Z. Check (a) that the congruence reproduces the kyroot failures exactly and
(b) the residues v.V0, v.V1, v.W_i mod 1 that drive it."""
import sys
import os
import glob
import json
import itertools
from fractions import Fraction as Fr
from collections import Counter
from multiprocessing import Pool
sys.path.insert(0, r'C:\tmp\toe_round\stype')
os.environ['NMAX'] = '2'
import latff as LF
import hyper_a8 as H
import oneloop as O


def shifts(path):
    (V0, V, W), block = O.load_any(path)
    rows = block if block else None
    if rows is None:
        t = open(path).read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
        rows = [','.join(r.split()) for r in [t[0], t[1]] + t[3:9]]
    vec = [[Fr(x.strip()) for x in r.split(',')] for r in rows]
    return vec[0], vec[1], [vec[2], vec[4], vec[6]]


def analyse(qpath, mpath, col, L):
    LF.E8 = LF.e8_upto(2)
    fac, u1, fields = H.parse(qpath)
    V0, V1, Ws = shifts(mpath)
    a, b = fac[col][1][0], fac[col][1][1]
    aL = fac[L][1][0]
    lam1 = [(2 * x + z) / 3 for x, z in zip(a, b)]
    roots = [r for _, rts in fac for r in rts]
    # beta-theta colour-singlet states and their fixed points (lattice labels -> c_i)
    bt = [f for f in fields if f['m'] in (19, 15, 16) and f['n'] == 1 and f['mm'] == 1 and abs(H.dsgn(f['dim'][col])) == 1]
    out = []
    seen = set()
    for sg in (1, -1):
        p = [sg * l + x / 2 for l, x in zip(lam1, aL)]
        for v8 in LF.E8:
            for h in (0, 1):
                v = [Fr(0)] * 16
                for k in range(8):
                    v[8 * h + k] = Fr(int(v8[k]), 2)
                if sum(x * x for x in v) != 2 or any(H.dot(v, r) != H.dot(p, r) for r in roots):
                    continue
                y = tuple(x - z for x, z in zip(v, p))
                if y in seen:
                    continue
                seen.add(y)
                # direct test on beta-theta colour singlets
                direct = any((H.dot(aL, w) / 2 + H.dot(list(y), w)).denominator != 1 for f in bt for w in f['W'])
                # congruence test: v.w mod 1 for the same states (equal to v.U_f mod 1)
                cong = any((H.dot(v, w)).denominator != 1 for f in bt for w in f['W'])
                res = dict(direct=direct, congruence=cong, vV0=str(H.dot(v, V0) % 1), vV1=str(H.dot(v, V1) % 1),
                           vW=[str(H.dot(v, W) % 1) for W in Ws])
                out.append(res)
    return out


def run_a8(lab):
    import a8ff
    import a8down as A
    base = r'C:\tmp\toe_round\stype\a8\%s' % lab
    fac, u1, fields = H.parse(base + '.q')
    c, l = a8ff.slots(fac, [f for f in fields if f['m'] == 19], A.ydir(base + '.sm'))
    return lab, analyse(base + '.q', base + '.txt', c, l)


if __name__ == '__main__':
    labs = sorted(os.path.basename(p)[:-2] for p in glob.glob(r'C:\tmp\toe_round\stype\a8\*.q'))
    allc = []
    with Pool(4) as p:
        for lab, c in p.imap_unordered(run_a8, labs):
            allc += c
    import hyper
    for m, path in [('N004_F1_03_S002', r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt'),
                    ('N008_F1_04_S037_T115', r'C:\tmp\toe_wt\analysis\search_drivers_12121\smwl3\N008_F1_04_S037_T115.txt')]:
        fac, u1, fields = H.parse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
        r = hyper.analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
        col = [i for i, (n, _) in enumerate(fac) if n == 'A2'][0]
        allc += analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m, path, col, r['L'])
    allint = sum(1 for c in allc if (Fr(c['vV0']) + Fr(c['vV1'])) % 1 == 0 and all(Fr(x) == 0 for x in c['vW']))
    zeroVW = Counter(tuple(c['vW']) for c in allc if (Fr(c['vV0']) + Fr(c['vV1'])) % 1 == 0)
    summary = dict(all_integral=allint, vW_when_V0V1_integral=Counter(str(k) for k in zeroVW.elements()), n=len(allc), direct_fails=sum(c['direct'] for c in allc), congruence_fails=sum(c['congruence'] for c in allc),
                   agree=sum(c['direct'] == c['congruence'] for c in allc),
                   vV0V1=Counter(str((Fr(c['vV0']) + Fr(c['vV1'])) % 1) for c in allc),
                   vV0=Counter(c['vV0'] for c in allc), vV1=Counter(c['vV1'] for c in allc))
    print({k: (dict(v) if isinstance(v, Counter) else v) for k, v in summary.items()})
    json.dump(dict(summary={k: (dict(v) if isinstance(v, Counter) else v) for k, v in summary.items()}), open(r'C:\tmp\toe_round\stype\congr.json', 'w'), indent=1)
    print('DONE')
