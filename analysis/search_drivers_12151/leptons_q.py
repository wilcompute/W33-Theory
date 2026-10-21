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
from exomass4 import sg_ok_n


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
                            if sg_ok_n([Aa[0], Bb[0], S, s]):
                                tot += 0.1 * rng.normal() * vev[S['i']] * vev[s['i']]
        return tot

    def light(Xs, Xbs):
        if not Xbs:
            return np.eye(len(Xs))
        M = np.array([[coup(a, b, ss) for b in Xs] for a in Xbs], complex).reshape(len(Xbs), len(Xs))
        u, s, vh = np.linalg.svd(M)
        r = int((s > 1e-8 * max(1, s.max() if s.size else 1)).sum())
        return vh[r:].conj().T
    Lp, Lb = comps(left, 1, 2, -3 * yq), comps(left, 1, 2, 3 * yq)
    E_, Eb = comps(left, 1, 1, 6 * yq), comps(left, 1, 1, -6 * yq)
    N = comps(left, 1, 1, Fr(0))
    NL, NE = light(Lp, Lb), light(E_, Eb)
    Ye = np.array([[coup(a, e, hs) for e in E_] for a in Lp], complex).reshape(len(Lp), len(E_))
    Le = NL.conj().T @ Ye @ NE
    se = np.linalg.svd(Le, compute_uv=False) if Le.size else np.zeros(0)
    Yn = np.array([[coup(a, n, hs) for n in N] for a in Lp], complex).reshape(len(Lp), len(N))
    Ln = NL.conj().T @ Yn
    sn = np.linalg.svd(Ln, compute_uv=False) if Ln.size else np.zeros(0)
    Mm = np.zeros((len(N), len(N)), complex)
    for i1 in range(len(N)):
        for j1 in range(i1, len(N)):
            Mm[i1, j1] = Mm[j1, i1] = coup(N[i1], N[j1], ss)
    rM = int(np.linalg.matrix_rank(Mm, tol=1e-8 * max(1, np.abs(Mm).max()))) if Mm.size else 0
    dirN = [k for k in range(len(N)) if np.abs(Ln[:, k]).max() > 1e-12] if Ln.size else []
    sub = Mm[np.ix_(dirN, dirN)] if dirN else np.zeros((0, 0))
    rSub = int(np.linalg.matrix_rank(sub, tol=1e-8 * max(1, np.abs(sub).max()))) if sub.size else 0
    import exomass4 as X4
    singl = [(sv, w) for sv, w in sing]
    two = defaultdict(list)
    for a_i in range(len(singl)):
        for b_i in range(a_i, len(singl)):
            two[tuple(x + z for x, z in zip(singl[a_i][1], singl[b_i][1]))].append((singl[a_i][0], singl[b_i][0]))
    M4 = np.zeros((len(dirN), len(dirN)), complex)
    for a_ in range(len(dirN)):
        for b_ in range(a_, len(dirN)):
            na, nb = N[dirN[a_]], N[dirN[b_]]
            tot = 0
            for wa in na[1]:
                for wb in nb[1]:
                    need = tuple(-(x + z) for x, z in zip(wa, wb))
                    for s1, s2 in two.get(need, []):
                        fs = [na[0], nb[0], s1, s2]
                        if X4.sg_ok_n(fs) and X4.hm_mod3(fs):
                            tot += rng.normal() * vev[s1['i']] * vev[s2['i']]
            M4[a_, b_] = M4[b_, a_] = tot
    rq = int(np.linalg.matrix_rank(M4, tol=1e-8 * max(1, np.abs(M4).max()))) if M4.size and np.abs(M4).max() > 0 else 0
    res = dict(majorana_quartic_rank_on_dirac_N=rq, netQ=net, nL=len(Lp), nLb=len(Lb), light_L=NL.shape[1], nE=len(E_), nEb=len(Eb), light_E=NE.shape[1],
               lepton_rank=int((se > 1e-8 * max(1, se.max() if se.size else 1)).sum()),
               nN=len(N), dirac_rank=int((sn > 1e-8 * max(1, sn.max() if sn.size else 1)).sum()), n_N_with_dirac=len(dirN),
               majorana_rank=rM, majorana_rank_on_dirac_N=rSub)
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
    items = [it for it in items if it[0] in ('A8SM_20260928_16222_TF',)]
    with Pool(2) as p:
        for lab, res in p.imap_unordered(run, items):
            out[lab] = res
            print(lab, res, flush=True)
    json.dump(out, open(r'C:\tmp\toe_round\stype\leptons_q.json', 'w'), indent=1, default=str)
    print('DONE')
