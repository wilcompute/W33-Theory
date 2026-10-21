"""12141: the marginal (Delta = 0) Witten-sector states on S002's imaginary Wilson-line axis, with their SM quantum numbers."""
import sys
import json
import functools
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import w33_pass11107_winding_tachyons as T
import w33_so16_one_loop as E
import hyper as H

T.torus_table = functools.partial(T.torus_table, nmax=6, mmax=10)
RHO = 0.5 + 0.8660254037844386j


def levels(rows, Tw, Ts, Nrange=5, cut=1e-9):
    V0, V, W = E.parse_model(rows)
    tori = [0, 2, 4]
    wlt = [i for i in tori if np.any(W[i] != 0)]
    Wt = [W[i] for i in wlt]
    tabs_free = T.torus_table(Ts, np.zeros(2), None)
    found = []
    for N1 in range(-Nrange, Nrange + 1):
        for N2 in range(-Nrange, Nrange + 1):
            w = V0 + N1 * Wt[0] + N2 * Wt[1]
            A = [T.e8_near(w[:8], 2.0), T.e8_near(w[8:], 2.0)]
            for x1 in A[0]:
                for x2 in A[1]:
                    pi = np.concatenate([x1, x2])
                    l = pi + w
                    l2 = l @ l
                    if l2 >= 2 - 1e-9 or abs(np.exp(2j * np.pi * (pi @ V0 + V0 @ V0)) + 1) > 1e-6:
                        continue
                    pp = pi + V0
                    offs = [(pp @ Wv + 0.5 * Wv @ (N1 * Wt[0] + N2 * Wt[1])) % 1.0 for Wv in Wt]
                    t1 = T.torus_table(Tw[0], np.array([offs[0]] * 2), N1)
                    t2 = T.torus_table(Tw[1], np.array([offs[1]] * 2), N2)
                    target = round(1 - l2, 6)
                    best = None
                    for k1, (r1, _) in t1.items():
                        for k2, (r2, _) in t2.items():
                            k3 = round(target - k1 - k2, 6)
                            if k3 in tabs_free:
                                tot = r1 + r2 + tabs_free[k3][0]
                                if tot <= 1 + cut and (best is None or tot < best):
                                    best = tot
                    if best is not None:
                        found.append(dict(Delta=-0.5 + best / 2, l=l))
    return found


if __name__ == '__main__':
    rows = open(r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    block = [','.join(r.strip().split()) for r in [rows[0], rows[1]] + rows[3:9]]
    hy = json.load(open(r'C:\tmp\toe_round\stype\hyper3_4.json'))['N004_F1_03_S002']
    y = np.array([float(Fr(x)) for x in hy['y_good']])
    fac, u1, fields = H.parse(r'C:\tmp\toe_round\stype\q4\N004_F1_03_S002.q')
    col = [i for i, (n, _) in enumerate(fac) if n == 'A2'][0]
    r = H.analyse(r'C:\tmp\toe_round\stype\q4\N004_F1_03_S002.q')
    aL = np.array([float(x) for x in fac[r['L']][1][0]])
    ca = [np.array([float(x) for x in rt]) for rt in fac[col][1]]
    out = {}
    for name, tw in [('0.55i', 0.55j), ('0.9i', 0.9j)]:
        f = levels(block, [tw, tw], RHO)
        marg = [s for s in f if abs(s['Delta']) < 1e-6]
        qn = []
        for s in marg:
            l = s['l']
            colour_singlet = all(abs(l @ a) < 1e-9 for a in ca) and True
            qn.append(dict(Y=round(float(y @ l), 6), T3=round(float(aL @ l / 2), 6), colour_weight=[round(float(l @ a), 6) for a in ca]))
        out[name] = dict(n_marginal=len(marg), n_tachyonic=sum(1 for s in f if s['Delta'] < -1e-6), quantum_numbers=qn)
        print(name, out[name]['n_marginal'], out[name]['n_tachyonic'], qn[:6], flush=True)
    json.dump(out, open(r'C:\tmp\toe_round\stype\marginal.json', 'w'), indent=1)
    print('DONE')
