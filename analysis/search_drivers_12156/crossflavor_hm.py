"""12147 + 12148: in the 16 crossed models (fraction-free k_Y = 17/3 Y with a single heavy up quark):
(12147) |V_tb| = overlap of the heavy up and heavy down directions in the light-Q space; up-Yukawa rank after adding quartic
Q u H <s> terms (gauge + space group; upper bound) -- does a charm mass appear at next order?
(12148) Witten-parity protection: if every SM-singlet scalar has mm = 0, masses cannot cross Witten-parity sectors; count the
vector-like pairs that stay exactly massless in each SM class."""
import sys
import os
import json
import itertools
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
from exomass4 import sg_ok_n, hm_mod3


def run(item):
    lab, ys = item
    base = r'C:\tmp\toe_round\stype\a8\%s' % lab
    fac, u1, fields = Y.parse(base + '.q')
    y0 = A.ydir(base + '.sm')
    left = [f for f in fields if f['m'] == 19]
    scal = [f for f in fields if f['m'] in (15, 16)]
    c, l = a8ff.slots(fac, left, y0)
    y = [Fr(x) for x in ys]
    dc = lambda f: H.dsgn(f['dim'][c])  # noqa: E731
    Yv = lambda w: H.dot(y, w)  # noqa: E731
    best = None
    for cq in (3, -3):
        for yq in (Fr(1, 6), Fr(-1, 6)):
            net = sum((1 if (dc(f) == cq and Yv(w) == yq) else -1 if (dc(f) == -cq and Yv(w) == -yq) else 0)
                      for f in left if f['dim'][l] == '2' for w in f['W']) // 6
            if best is None or net > best[0]:
                best = (net, cq, yq)
    net, cq, yq = best

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
    rng = np.random.default_rng(13)
    vev = defaultdict(lambda: rng.normal() + 1j * rng.normal())
    hs, ss = defaultdict(list), defaultdict(list)
    sing = []
    for s in scal:
        if abs(dc(s)) == 1 and s['dim'][l] == '2':
            for w in s['W']:
                hs[w].append(s)
        if abs(dc(s)) == 1 and s['dim'][l] == '1':
            for w in s['W']:
                if Yv(w) == 0:
                    ss[w].append(s)
                    sing.append((s, w))

    def coup(Aa, Bb, idx, quartic=False):
        tot, seen = 0, set()
        for wa in Aa[1]:
            for wb in Bb[1]:
                need = tuple(-(x + z) for x, z in zip(wa, wb))
                for S in idx.get(need, []):
                    if S['i'] in seen:
                        continue
                    seen.add(S['i'])
                    fs = [Aa[0], Bb[0], S]
                    if Y.sg_ok(fs) and Y.hm_ok(fs, [False] * 3) and A.local(fs):
                        tot += rng.normal() * vev[S['i']]
                if quartic:
                    for s, ws in sing:
                        need2 = tuple(x - z for x, z in zip(need, ws))
                        for S in idx.get(need2, []):
                            if sg_ok_n([Aa[0], Bb[0], S, s]) and hm_mod3([Aa[0], Bb[0], S, s]):
                                tot += 0.1 * rng.normal() * vev[S['i']] * vev[s['i']]
        return tot

    def light(Xs, Xbs):
        if not Xbs:
            return np.eye(len(Xs))
        M = np.array([[coup(a, b, ss) for b in Xs] for a in Xbs], complex).reshape(len(Xbs), len(Xs))
        u, s, vh = np.linalg.svd(M)
        r = int((s > 1e-8 * max(1, s.max() if s.size else 1)).sum())
        return vh[r:].conj().T
    Q, Qb = comps(left, cq, 2, yq), comps(left, -cq, 2, -yq)
    NQ = light(Q, Qb)
    res = dict(netQ=net)
    heavy = {}
    for kind, ycc in (('up', -4 * yq), ('down', 2 * yq)):
        D, Db = comps(left, -cq, 1, ycc), comps(left, cq, 1, -ycc)
        ND = light(D, Db)
        Y3 = np.array([[coup(q, d, hs) for d in D] for q in Q], complex).reshape(len(Q), len(D))
        L3 = NQ.conj().T @ Y3 @ ND
        u, s, vh = np.linalg.svd(L3)
        r3 = int((s > 1e-8 * max(1, s.max())).sum())
        heavy[kind] = u[:, 0]
        res[kind] = dict(rank3=r3, sv3=[float(x) for x in s])
        if kind == 'up':
            Y4 = np.array([[coup(q, d, hs, quartic=True) for d in D] for q in Q], complex).reshape(len(Q), len(D))
            L4 = NQ.conj().T @ Y4 @ ND
            s4 = np.linalg.svd(L4, compute_uv=False)
            res[kind].update(rank_with_quartic=int((s4 > 1e-8 * max(1, s4.max())).sum()), sv4=[float(x) for x in s4])
    res['Vtb'] = float(abs(np.vdot(heavy['up'], heavy['down'])))
    # 12148 Witten-parity protection
    smm = sorted({s['mm'] for s, _ in sing})
    prot = {}
    if smm == [0]:
        cls = defaultdict(Counter)
        for f in left:
            g = defaultdict(int)
            for w in f['W']:
                g[Yv(w)] += 1
            for yy, k in g.items():
                key = (dc(f), int(f['dim'][l]) if f['dim'][l].isdigit() else 0, yy)
                cls[key][f['mm']] += k // max(1, abs(dc(f)) * (int(f['dim'][l]) if f['dim'][l].isdigit() else 1))
        done = set()
        for key in list(cls):
            if key in done:
                continue
            d_, l_, yy = key
            conj = ((-d_ if abs(d_) == 3 else d_), l_, -yy)
            done |= {key, conj}
            if key == conj or (d_, l_, yy) == (1, 1, 0):
                continue
            per = [cls[key][m] - cls.get(conj, Counter())[m] for m in (0, 1)]
            p_ = (sum(abs(x) for x in per) - abs(sum(per))) // 2
            if p_:
                prot[str((d_, l_, str(yy)))] = p_
    res['singlet_mm'] = smm
    res['witten_protected_pairs'] = prot
    return lab, res


if __name__ == '__main__':
    d = json.load(open(r'C:\tmp\toe_round\stype\a8cross.json'))
    lat = json.load(open(r'C:\tmp\toe_round\stype\latff_a8.json'))
    items = []
    for lab, r in sorted(d.items()):
        ys = [y for y in lat[lab]['ys'] if 2 * sum(Fr(x) ** 2 for x in y) == Fr(17, 3)][:4]
        for x, yv in zip(r, ys):
            if x['up']['rank'] == 1:
                items.append((lab, yv))
                break
    out = {}
    with Pool(6) as p:
        for lab, res in p.imap_unordered(run, items):
            out[lab] = res
            print(lab, 'Vtb %.3f' % res['Vtb'], 'up', res['up']['rank3'], '->', res['up']['rank_with_quartic'], 'down', res['down']['rank3'],
                  'singlet mm', res['singlet_mm'], 'protected', res['witten_protected_pairs'], flush=True)
    json.dump(out, open(r'C:\tmp\toe_round\stype\crossflavor_hm.json', 'w'), indent=1, default=str)
    print('DONE')
