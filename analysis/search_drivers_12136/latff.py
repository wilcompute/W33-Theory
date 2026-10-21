"""12139: complete search for fraction-free three-generation hypercharges via the lattice criterion (12131): a fraction-free
Y needs v = q +- lambda in E8 x E8 with v . r = (+-lambda + a_L/2) . r for EVERY nonabelian root r (Y commutes with the whole
unbroken nonabelian group), N = |v|^2 = 7/6 + y^2. Enumerate all such v with N <= NMAX, then test the SM net spectrum and
fractional charges on every massless state. Control: on the e6+a2 models it must return exactly the 12126 fraction-free set
(restricted to N <= NMAX)."""
import sys
import os
import glob
import json
import itertools
from fractions import Fraction as Fr
from collections import Counter
from multiprocessing import Pool
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import hyper_a8 as H

NMAX = int(os.environ.get('NMAX', '12'))


def e8_upto(nmax):
    """all E8 vectors with norm <= nmax, as doubled-coordinate int8 numpy rows (vectorised build)"""
    import numpy as np
    outs = []
    for half in (0, 1):
        vals = np.array([v for v in range(-7, 8) if v % 2 == half and v * v <= 4 * nmax], dtype=np.int16)
        cur = np.zeros((1, 0), dtype=np.int16)
        n2 = np.zeros(1, dtype=np.int32)
        for pos in range(8):
            a = np.repeat(cur, len(vals), axis=0)
            b = np.tile(vals, len(cur))
            nn = np.repeat(n2, len(vals)) + b.astype(np.int32) ** 2
            keep = nn <= 4 * nmax
            cur = np.hstack([a[keep], b[keep, None]])
            n2 = nn[keep]
        cur = cur[(cur.sum(axis=1) % 4) == 0]
        outs.append(cur)
    return np.vstack(outs)


E8 = None


def net_of(left, y, col, L):
    cnt = Counter()
    for f in left:
        dc, dl = H.dsgn(f['dim'][col]), int(f['dim'][L])
        ys = Counter(H.dot(y, w) for w in f['W'])
        for Yv, k in ys.items():
            cnt[(dc, dl, Yv)] += k // (abs(dc) * dl)
    net, done = {}, set()
    for key in cnt:
        if key in done:
            continue
        dc, dl, Yv = key
        conj = ((-dc if abs(dc) == 3 else dc), dl, -Yv)
        done |= {key, conj}
        if key == conj:
            continue
        dd = cnt.get(key, 0) - cnt.get(conj, 0)
        if dd:
            net[key if dd > 0 else conj] = abs(dd)
    return net


def fractional(fields, col, aL, y):
    for f in fields:
        if f['m'] not in (19, 15, 16):
            continue
        dc = abs(H.dsgn(f['dim'][col]))
        for w in f['W']:
            Q = H.dot(aL, w) / 2 + H.dot(y, w)
            if (dc == 1 and Q.denominator != 1) or (dc == 3 and ((3 * Q).denominator != 1 or Q.denominator == 1)):
                return True
    return False


def search(qpath, col, L):
    global E8
    if E8 is None:
        E8 = e8_upto(NMAX)
    fac, u1, fields = H.parse(qpath)
    left = [f for f in fields if f['m'] == 19]
    a, b = fac[col][1][0], fac[col][1][1]
    aL = fac[L][1][0]
    lam1 = [(2 * x + z) / 3 for x, z in zip(a, b)]
    roots = [r for _, rts in fac for r in rts]
    found = []
    for sg in (1, -1):
        p = [sg * l + x / 2 for l, x in zip(lam1, aL)]
        halves = []
        for h in (0, 1):
            rh = [r[8 * h:8 * h + 8] for r in roots if any(r[8 * h:8 * h + 8]) and not any(r[8 * (1 - h):8 * (1 - h) + 8])]
            ph = p[8 * h:8 * h + 8]
            tg = [sum(x * z for x, z in zip(ph, r)) for r in rh]
            import numpy as np
            mask = np.ones(len(E8), bool)
            for r, t in zip(rh, tg):
                t4 = 4 * t
                if t4.denominator != 1:
                    mask[:] = False
                    break
                r2 = np.array([int(2 * x) for x in r], dtype=np.int32)
                mask &= (E8.astype(np.int32) @ r2) == 2 * int(t4) // 1 if False else ((E8.astype(np.int32) @ r2) == int(2 * t * 2))
            ok = E8[mask]
            halves.append([(tuple(Fr(int(x), 2) for x in v), Fr(int((v.astype(np.int32) ** 2).sum()), 4)) for v in ok])
        import numpy as np
        allw = sorted({w for f in fields if f['m'] in (19, 15, 16) for w in f['W']})
        sing = [w for w in allw if any(abs(H.dsgn(f['dim'][col])) == 1 and w in f['W'] for f in fields if f['m'] in (19, 15, 16))]
        sing = sorted(set(sing))[:400]
        c = np.array([float(H.dot(aL, w) / 2 - H.dot(p, w)) for w in sing])
        Wa = np.array([[float(x) for x in w[:8]] for w in sing])
        Wb = np.array([[float(x) for x in w[8:]] for w in sing])
        V1 = np.array([[float(x) for x in v] for v, _ in halves[0]]).reshape(-1, 8)
        V2 = np.array([[float(x) for x in v] for v, _ in halves[1]]).reshape(-1, 8)
        k1 = np.mod(np.round(72 * (V1 @ Wa.T + c)).astype(np.int64), 72)
        k2 = np.mod(np.round(-72 * (V2 @ Wb.T)).astype(np.int64), 72)
        idx = {}
        for jj, row in enumerate(k2):
            idx.setdefault(row.tobytes(), []).append(jj)
        for ii, row in enumerate(k1):
            for jj in idx.get(row.tobytes(), []):
                (v1, n1), (v2, n2) = halves[0][ii], halves[1][jj]
                if n1 + n2 > NMAX:
                    continue
                v = list(v1) + list(v2)
                y = [x - z for x, z in zip(v, p)]
                if fractional(fields, col, aL, y):
                    continue
                if not H.is_sm(net_of(left, y, col, L)):
                    continue
                found.append(str(2 * H.dot(y, y)))
    return sorted(found, key=Fr)


def run_a8(lab):
    import a8ff
    import a8down as A
    base = r'C:\tmp\toe_round\stype\a8\%s' % lab
    fac, u1, fields = H.parse(base + '.q')
    y0 = A.ydir(base + '.sm')
    left = [f for f in fields if f['m'] == 19]
    c, l = a8ff.slots(fac, left, y0)
    ff = search(base + '.q', c, l)
    return lab, dict(n_fraction_free=len(ff), kY=sorted(set(ff), key=Fr))


if __name__ == '__main__':
    if sys.argv[1] == 'control':
        out = {}
        for m in ['N008_F1_03_S033', 'N008_F1_02_S053', 'N008_F1_04_S037_T115', 'N004_F1_03_S002']:
            fac, u1, fields = H.parse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
            r = H.analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
            col = [i for i, (n, _) in enumerate(fac) if n == 'A2'][0]
            ff = search(r'C:\tmp\toe_round\stype\q4\%s.q' % m, col, r['L'])
            out[m] = dict(n=len(ff), kY=sorted(set(ff), key=Fr))
            print(m, out[m], flush=True)
        json.dump(out, open(r'C:\tmp\toe_round\stype\latff_control.json', 'w'), indent=1)
    else:
        labs = sorted(os.path.basename(p)[:-2] for p in glob.glob(r'C:\tmp\toe_round\stype\a8\*.q'))
        if len(sys.argv) > 2:
            labs = labs[:int(sys.argv[2])]
        res = {}
        with Pool(4) as pool:
            for lab, v in pool.imap_unordered(run_a8, labs):
                res[lab] = v
                print(lab, v, flush=True)
        json.dump(res, open(r'C:\tmp\toe_round\stype\latff_a8.json', 'w'), indent=1)
        print('DONE')
