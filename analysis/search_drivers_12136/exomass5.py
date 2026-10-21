"""12133: exotic masses up to quartic order in T115 (and S002): psi psi <s> (all rules) + psi psi <s1><s2> (gauge + space
group only; H-momentum not imposed, so a 'lift' is an upper bound and a remaining light pair is robust)."""
import sys
import json
import itertools
import numpy as np
from collections import defaultdict
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import hyper as H
import yuk as Y
import sympy as sp
import os
QUINTIC = os.environ.get('QUINTIC') == '1'
from fractions import Fraction as Fr
from exomass import units

rng = np.random.default_rng(23)


def sg_ok_n(fs):
    if sum(f['n'] for f in fs) % 3 or sum(f['mm'] for f in fs) % 2:
        return False
    if any(f['n'] for f in fs):
        return all(sum(f['lat'][2 * t] + f['lat'][2 * t + 1] for f in fs) % 3 == 0 for t in range(3))
    for ks in itertools.product(range(3), repeat=len(fs)):
        s = [sum(x) for x in zip(*[Y.rot(f['lat'], k) for f, k in zip(fs, ks)])]
        if all(x == 0 for x in s):
            return True
    return False


def run(m, yv):
    fac, u1, fields = Y.parse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    r = H.analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    col, L = [i for i, (n, _) in enumerate(fac) if n == 'A2'][0], r['L']
    M = sp.Matrix([[sp.Rational(str(x)) for x in rt] for rt in [fac[col][1][0], fac[col][1][1], fac[L][1][0]]])
    Bc = [[Fr(str(x)) for x in v] for v in M.nullspace()]
    y = [Fr(x) for x in yv]
    left = [f for f in fields if f['m'] == 19]
    scal = [f for f in fields if f['m'] in (15, 16)]
    fu = units(left, Bc, y, col, L)
    su = [u for u in units(scal, Bc, y, col, L) if u['dc'] == 1 and u['dl'] == 1 and u['Y'] == 0]
    one = defaultdict(list)
    for u in su:
        one[u['t']].append(u)
    two = defaultdict(list)
    for i, u in enumerate(su):
        for v in su[i:]:
            two[tuple(x + z for x, z in zip(u['t'], v['t']))].append((u, v))
    vev = {u['f']['i']: rng.normal() + 1j * rng.normal() for u in su}
    cls = defaultdict(list)
    for u in fu:
        cls[(u['dc'], u['dl'], u['Y'])].append(u)
    rep, done = {}, set()
    for key in list(cls):
        if key in done:
            continue
        dc, dl, Yv = key
        conj = ((-dc if abs(dc) == 3 else dc), dl, -Yv)
        done |= {key, conj}
        if key == (1, 1, 0) or key == conj:
            continue
        A, B = cls.get(key, []), cls.get(conj, [])
        if not A or not B:
            continue
        M3 = np.zeros((len(A), len(B)), complex)
        M4 = np.zeros((len(A), len(B)), complex)
        M5 = np.zeros((len(A), len(B)), complex)
        for i, a in enumerate(A):
            for j, b in enumerate(B):
                need = tuple(-(x + z) for x, z in zip(a['t'], b['t']))
                for s in one.get(need, []):
                    if Y.sg_ok([a['f'], b['f'], s['f']]) and Y.hm_ok([a['f'], b['f'], s['f']], [False] * 3):
                        M3[i, j] += rng.normal() * vev[s['f']['i']]
                for s1, s2 in two.get(need, []):
                    if sg_ok_n([a['f'], b['f'], s1['f'], s2['f']]):
                        M4[i, j] += rng.normal() * vev[s1['f']['i']] * vev[s2['f']['i']]
                if QUINTIC and key[1] == 2:
                    for s0 in su:
                        rest = tuple(x - z for x, z in zip(need, s0['t']))
                        for s1, s2 in two.get(rest, []):
                            if sg_ok_n([a['f'], b['f'], s0['f'], s1['f'], s2['f']]):
                                M5[i, j] += rng.normal() * vev[s0['f']['i']] * vev[s1['f']['i']] * vev[s2['f']['i']]
        need_r = min(len(A), len(B))
        r3 = int(np.linalg.matrix_rank(M3, tol=1e-8 * max(1, np.abs(M3).max())))
        Mt = M3 + 0.1 * M4
        r34 = int(np.linalg.matrix_rank(Mt, tol=1e-9 * max(1, np.abs(Mt).max())))
        M5t = M3 + 0.1 * M4 + 0.01 * M5
        r345 = int(np.linalg.matrix_rank(M5t, tol=1e-10 * max(1, np.abs(M5t).max())))
        rep[str(key)] = dict(nR=len(A), nRbar=len(B), need=need_r, rank_trilinear=r3, rank_up_to_quartic=r34, rank_up_to_quintic=r345,
                             n_quintic_entries=int((np.abs(M5) > 0).sum()))
    return rep


if __name__ == '__main__':
    hy = json.load(open(r'C:\tmp\toe_round\stype\hyper3_4.json'))
    out = {}
    for m in sys.argv[1:]:
        rep = run(m, hy[m]['y_good'])
        out[m] = dict(classes=rep, light_trilinear=sum(v['need'] - v['rank_trilinear'] for v in rep.values()),
                      light_up_to_quartic=sum(v['need'] - v['rank_up_to_quartic'] for v in rep.values()), light_up_to_quintic=sum(v['need'] - v['rank_up_to_quintic'] for v in rep.values()))
        print(m, out[m]['light_trilinear'], '->', out[m]['light_up_to_quartic'], flush=True)
        for k, v in rep.items():
            print('   ', k, v)
    json.dump(out, open(r'C:\tmp\toe_round\stype\exomass5.json', 'w'), indent=1)
