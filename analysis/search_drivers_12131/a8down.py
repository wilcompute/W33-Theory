"""12134: down-sector vector-like mixing in the 104 A8 models of Pass 11095. Hypercharge = the nsosm SM-config U(1) (rescaled
so Q has 1/6); D-class mass matrix from singlet couplings psi psi <s> and Q D H Yukawas, all tree-level rules with the exact
H-momentum rule; O(1) = every twisted field at the same fixed point (as in 11098). Light down Yukawa = Yuk x null(M)."""
import sys
import os
import re
import glob
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


def local(fs):
    """all twisted fields sit at one geometric fixed point (theta label l, theta^2 label -l) in every torus"""
    tw = [f for f in fs if f['n']]
    for t in range(3):
        pts = {int((f['lat'][2 * t] + f['lat'][2 * t + 1]) * (1 if f['n'] == 1 else -1)) % 3 for f in tw}
        if len(pts) > 1:
            return False
    return True


def ydir(smfile):
    t = open(smfile).read()
    u1 = [[float(x) for x in l.split('|')[1].split()] for l in t.split('\n') if l.startswith('U1 ')]
    raw = [(m.group(1), [float(x) for x in m.group(3).split(',')]) for m in re.finditer(r'^L (\S+) dim=(\S+) q=(\S+)', t, re.M)]
    qf = [q for lab, q in raw if lab == 'q']
    yi = next(i for i in range(len(qf[0])) if all(abs(abs(q[i]) - 1 / 6) < 1e-9 for q in qf))
    return [H.F(x) for x in u1[yi]]


def run(lab):
    base = r'C:\tmp\toe_round\stype\a8\%s' % lab
    fac, u1, fields = Y.parse(base + '.q')
    y = ydir(base + '.sm')
    left = [f for f in fields if f['m'] == 19]
    scal = [f for f in fields if f['m'] in (15, 16)]
    a2 = [i for i, (n, _) in enumerate(fac) if n == 'A2' and all(H.dot(y, rt) == 0 for rt in fac[i][1])]
    a1 = [i for i, (n, _) in enumerate(fac) if n == 'A1' and all(H.dot(y, rt) == 0 for rt in fac[i][1])]
    best = None
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
                    net //= 6
                    if best is None or net > best[0]:
                        best = (net, c, l, cq, yq)
    net, c, l, cq, yq = best
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
    D = comps(left, -cq, 1, 2 * yq)
    Db = comps(left, cq, 1, -2 * yq)
    hs = defaultdict(list)
    for s in scal:
        if abs(dc(s)) == 1 and s['dim'][l] == '2':
            for w in s['W']:
                hs[w].append(s)
    ss = defaultdict(list)
    for s in scal:
        if abs(dc(s)) == 1 and s['dim'][l] == '1':
            for w in s['W']:
                if Yv(w) == 0:
                    ss[w].append(s)
    rng = np.random.default_rng(5)
    vev = defaultdict(lambda: rng.normal() + 1j * rng.normal())

    def coupling(A, B, idx, strict_local):
        tot, seen = 0, set()
        for wa in A[1]:
            for wb in B[1]:
                for S in idx.get(tuple(-(x + z) for x, z in zip(wa, wb)), []):
                    if S['i'] in seen:
                        continue
                    seen.add(S['i'])
                    fs = [A[0], B[0], S]
                    if Y.sg_ok(fs) and Y.hm_ok(fs, [False] * 3) and (local(fs) or not strict_local):
                        tot += rng.normal() * vev[S['i']]
        return tot
    out = dict(netQ=net, nQ=len(Q), nD=len(D), nDb=len(Db))
    for strict in (True,):
        M = np.array([[coupling(a, b, ss, strict) for b in D] for a in Db], complex).reshape(len(Db), len(D))
        Yk = np.array([[coupling(q, d, hs, strict) for d in D] for q in Q], complex).reshape(len(Q), len(D))
        if len(Db):
            u, s, vh = np.linalg.svd(M)
            rM = int((s > 1e-8 * max(1, s.max())).sum())
            N = vh[rM:].conj().T
        else:
            rM, N = 0, np.eye(len(D))
        light = Yk @ N
        out.update(rank_M=rM, n_light_d=N.shape[1], rank_Yuk_all_D=int(np.linalg.matrix_rank(Yk, tol=1e-8 * max(1, np.abs(Yk).max()))) if Yk.size else 0,
                   rank_light=int(np.linalg.matrix_rank(light, tol=1e-8 * max(1, np.abs(light).max()))) if light.size else 0)
    return lab, out


if __name__ == '__main__':
    labs = sorted(os.path.basename(p)[:-2] for p in glob.glob(r'C:\tmp\toe_round\stype\a8\*.q'))
    if len(sys.argv) > 1:
        labs = labs[:int(sys.argv[1])]
    with Pool(10) as p:
        res = dict(p.map(run, labs))
    json.dump(res, open(r'C:\tmp\toe_round\stype\a8down.json', 'w'), indent=1)
    print(len(res), 'nQ', Counter(v['nQ'] for v in res.values()))
    print('n_light_d', Counter(v['n_light_d'] for v in res.values()))
    print('rank light down Yukawa', Counter(v['rank_light'] for v in res.values()))
    print('rank with all D (no mass matrix)', Counter(v['rank_Yuk_all_D'] for v in res.values()))
    print('vector-like D present & rank_light>0', sum(1 for v in res.values() if v['nDb'] and v['rank_light']))
