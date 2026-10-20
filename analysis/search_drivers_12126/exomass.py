"""12128: can every vector-like exotic of a model get a mass psi psi <s> from SM-singlet scalar vevs (trilinear, all selection
rules)? Numerical rank of each SM-class mass matrix at random couplings and vevs."""
import sys
import json
import random
import itertools
from fractions import Fraction as Fr
from collections import Counter, defaultdict
import numpy as np
import sympy as sp

sys.path.insert(0, r'C:\tmp\toe_round\stype')
import hyper as H
import yuk as Y

rng = np.random.default_rng(11)


def units(fields, Bc, y, col, L, scalar=False):
    out = []
    for f in fields:
        dc, dl = H.dsgn(f['dim'][col]), int(f['dim'][L])
        g = defaultdict(list)
        for w in f['W']:
            g[tuple(H.dot(b, w) for b in Bc)].append(w)
        for t, ws in g.items():
            out.append(dict(f=f, t=t, Y=H.dot(y, ws[0]), dc=dc, dl=dl, n=len(ws)))
    return out


def run(m, yv):
    fac, u1, fields = Y.parse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    r = H.analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    col, L = [i for i, (n, _) in enumerate(fac) if n == 'A2'][0], r['L']
    roots = [fac[col][1][0], fac[col][1][1], fac[L][1][0]]
    M = sp.Matrix([[sp.Rational(str(x)) for x in rt] for rt in roots])
    Bc = [[Fr(str(x)) for x in v] for v in M.nullspace()]  # 13 Cartan directions commuting with SU(3)c x SU(2)L
    y = [Fr(x) for x in yv]
    left = [f for f in fields if f['m'] == 19]
    scal = [f for f in fields if f['m'] in (15, 16)]
    fu = units(left, Bc, y, col, L)
    su = [u for u in units(scal, Bc, y, col, L) if u['dc'] == 1 and u['dl'] == 1 and u['Y'] == 0]
    sidx = defaultdict(list)
    for u in su:
        sidx[u['t']].append(u)
    cls = defaultdict(list)
    for u in fu:
        cls[(u['dc'], u['dl'], u['Y'])].append(u)
    report = {}
    vev = defaultdict(lambda: rng.normal() + 1j * rng.normal())
    done = set()
    for key in list(cls):
        if key in done:
            continue
        dc, dl, Yv = key
        conj = ((-dc if abs(dc) == 3 else dc), dl, -Yv)
        done |= {key, conj}
        A, B = cls.get(key, []), cls.get(conj, [])
        if key == (1, 1, 0):
            continue
        selfc = key == conj
        if selfc:
            B = A
        if not A or not B:
            report[str(key)] = dict(nR=len(A), nRbar=len(B), rank=0, need=0, ok=True)
            continue
        Mm = np.zeros((len(A), len(B)), complex)
        for i, a in enumerate(A):
            for j, b in enumerate(B):
                if selfc and j < i:
                    continue
                need = tuple(-(x + z) for x, z in zip(a['t'], b['t']))
                for s in sidx.get(need, []):
                    if Y.sg_ok([a['f'], b['f'], s['f']]) and Y.hm_ok([a['f'], b['f'], s['f']], [False] * 3):
                        Mm[i, j] += (rng.normal() + 1j * rng.normal()) * vev[s['f']['i']]
                if selfc:
                    Mm[j, i] = Mm[i, j]
        rk = int(np.linalg.matrix_rank(Mm, tol=1e-8 * max(1, np.abs(Mm).max())))
        needr = len(A) if selfc else min(len(A), len(B))
        report[str(key)] = dict(nR=len(A), nRbar=len(B) if not selfc else len(A), rank=rk, need=needr, ok=rk == needr)
    return report


if __name__ == '__main__':
    hy = json.load(open(r'C:\tmp\toe_round\stype\hyper3_4.json'))
    res = {}
    for m in sys.argv[1:]:
        rep = run(m, hy[m]['y_good'])
        bad = {k: v for k, v in rep.items() if not v['ok']}
        light = sum(v['need'] - v['rank'] for v in rep.values())
        res[m] = dict(classes=rep, n_classes=len(rep), n_bad=len(bad), unlifted_pairs=light)
        print(m, 'classes', len(rep), 'not fully lifted', len(bad), 'unlifted', light, flush=True)
        for k, v in sorted(bad.items()):
            print('   ', k, v)
    json.dump(res, open(r'C:\tmp\toe_round\stype\exomass.json', 'w'), indent=1)
