"""12145: crossing the routes -- for each A8 model and each fraction-free hypercharge at the minimal k_Y = 17/3 (12139),
recompute the quark sector under THAT Y: vector-like Q / u^c / d^c pairs, and the light up- and down-type Yukawa ranks after
vector-like mixing (local tree-level couplings, exact H-momentum, as 11098/12134)."""
import sys
import os
import json
import numpy as np
from fractions import Fraction as Fr
from collections import defaultdict, Counter
from multiprocessing import Pool
sys.path.insert(0, r'C:\tmp\toe_round\stype')
os.environ['EXACT'] = '1'
import hyper as H
import yuk as Y
import a8down as A
import a8ff


def sector_rank(left, scal, y, c, l, cq, yq, kind, rng):
    dc = lambda f: H.dsgn(f['dim'][c])  # noqa: E731
    Yv = lambda w: H.dot(y, w)  # noqa: E731

    def comps(fs, want_dc, want_dl, want_Y):
        out = []
        for f in fs:
            if dc(f) != want_dc or f['dim'][l] != str(want_dl):
                continue
            g = defaultdict(list)
            for w in f['W']:
                g[Yv(w)].append(w)
            for yy, ws in g.items():
                if yy == want_Y:
                    out.append((f, ws))
        return out
    Q = comps(left, cq, 2, yq)
    Qb = comps(left, -cq, 2, -yq)
    yc = 2 * yq if kind == 'down' else -4 * yq
    D = comps(left, -cq, 1, yc)
    Db = comps(left, cq, 1, -yc)
    hs, ss = defaultdict(list), defaultdict(list)
    for s in scal:
        if abs(dc(s)) == 1 and s['dim'][l] == '2':
            for w in s['W']:
                hs[w].append(s)
        if abs(dc(s)) == 1 and s['dim'][l] == '1':
            for w in s['W']:
                if Yv(w) == 0:
                    ss[w].append(s)
    vev = defaultdict(lambda: rng.normal() + 1j * rng.normal())

    def coup(Aa, Bb, idx):
        tot, seen = 0, set()
        for wa in Aa[1]:
            for wb in Bb[1]:
                for S in idx.get(tuple(-(x + z) for x, z in zip(wa, wb)), []):
                    if S['i'] in seen:
                        continue
                    seen.add(S['i'])
                    fs = [Aa[0], Bb[0], S]
                    if Y.sg_ok(fs) and Y.hm_ok(fs, [False] * 3) and A.local(fs):
                        tot += rng.normal() * vev[S['i']]
        return tot

    def light(Xs, Xbs):
        if not Xbs:
            return np.eye(len(Xs))
        M = np.array([[coup(a, b, ss) for b in Xs] for a in Xbs], complex).reshape(len(Xbs), len(Xs))
        u, s, vh = np.linalg.svd(M)
        r = int((s > 1e-8 * max(1, s.max() if s.size else 1)).sum())
        return vh[r:].conj().T
    NQ, ND = light(Q, Qb), light(D, Db)
    Yk = np.array([[coup(q, d, hs) for d in D] for q in Q], complex).reshape(len(Q), len(D))
    L = NQ.conj().T @ Yk @ ND if Yk.size else np.zeros((0, 0))
    rank = int(np.linalg.matrix_rank(L, tol=1e-8 * max(1, np.abs(L).max()))) if L.size else 0
    sv = np.linalg.svd(L, compute_uv=False) if L.size else []
    return dict(nQ=len(Q), nQb=len(Qb), nD=len(D), nDb=len(Db), light_Q=NQ.shape[1], light_D=ND.shape[1], rank=rank,
                sv=[float(x) for x in sv])


def run(item):
    lab, ys = item
    base = r'C:\tmp\toe_round\stype\a8\%s' % lab
    fac, u1, fields = Y.parse(base + '.q')
    y0 = A.ydir(base + '.sm')
    left = [f for f in fields if f['m'] == 19]
    scal = [f for f in fields if f['m'] in (15, 16)]
    c, l = a8ff.slots(fac, left, y0)
    res = []
    for ys_ in ys:
        y = [Fr(x) for x in ys_]
        best = None
        for cq in (3, -3):
            for yq in (Fr(1, 6), Fr(-1, 6)):
                net = sum((1 if (H.dsgn(f['dim'][c]) == cq and H.dot(y, w) == yq) else -1 if (H.dsgn(f['dim'][c]) == -cq and H.dot(y, w) == -yq) else 0)
                          for f in left if f['dim'][l] == '2' for w in f['W']) // 6
                if best is None or net > best[0]:
                    best = (net, cq, yq)
        net, cq, yq = best
        rng = np.random.default_rng(7)
        up = sector_rank(left, scal, y, c, l, cq, yq, 'up', rng)
        dn = sector_rank(left, scal, y, c, l, cq, yq, 'down', rng)
        res.append(dict(netQ=net, up=up, down=dn))
    return lab, res


if __name__ == '__main__':
    lat = json.load(open(r'C:\tmp\toe_round\stype\latff_a8.json'))
    items = []
    for lab, v in sorted(lat.items()):
        ys = [y for y in v['ys'] if 2 * sum(Fr(x) ** 2 for x in y) == Fr(17, 3)][:4]
        if ys:
            items.append((lab, ys))
    out = {}
    with Pool(6) as p:
        for lab, r in p.imap_unordered(run, items):
            out[lab] = r
            print(lab, [(x['netQ'], x['up']['rank'], x['down']['rank'], x['up']['nQb'], x['up']['nDb']) for x in r], flush=True)
    json.dump(out, open(r'C:\tmp\toe_round\stype\a8cross.json', 'w'), indent=1)
    allr = [x for r in out.values() for x in r]
    print('hypercharges', len(allr), 'models', len(out))
    print('(up rank, down rank)', Counter((x['up']['rank'], x['down']['rank']) for x in allr))
    print('single heavy up (rank 1):', sorted({lab for lab, r in out.items() if any(x['up']['rank'] == 1 for x in r)}))
    print('DONE')
