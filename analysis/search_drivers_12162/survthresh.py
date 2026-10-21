"""12162: intermediate-scale exotic thresholds of the 12 survivors of Passes 11101/11106. One-loop b_a of the full massless spectrum
(nsosm SM configuration: left Weyl fermions L and scalars SC, the model's own hypercharge), Delta b_a = b_a(total) - b_a(SM with one Higgs
doublet); all non-SM states at one scale M_X. Solve exactly (linear) for 1/alpha_U, L_s = ln(M_s/M_Z), L_X = ln(M_s/M_X) from the measured
alpha_s, alpha_2, alpha_Y at M_Z with string boundary conditions k_3 = k_2 = 1, k_Y = 5/3; compare M_s with the heterotic scale
g_U * 5.27e17 GeV and require 0 <= L_X <= L_s."""
import re
import json
import math
from fractions import Fraction as Fr
import numpy as np

MZ, aem, a3, s2 = 91.1876, 1 / 127.951, 0.1180, 0.23122
ia = {'3': 1 / a3, '2': s2 / aem, 'Y': (1 - s2) / aem}
TSU3 = {1: 0, 3: Fr(1, 2), 6: Fr(5, 2), 8: Fr(3)}
TSU2 = {1: 0, 2: Fr(1, 2), 3: Fr(2)}
bSM = {'3': Fr(-7), '2': Fr(-19, 6), 'Y': Fr(41, 6)}
kk = {'3': 1, '2': 1, 'Y': Fr(5, 3)}


def parse(path):
    t = open(path).read()
    facs = re.findall(r'^FACTOR (\d+) (\w+)', t, re.M)
    raw = []
    for m in re.finditer(r'^(L|SC) (\S+) dim=(\S+) q=(\S+)', t, re.M):
        raw.append((m.group(1), m.group(2), m.group(3).split(','), [float(x) for x in m.group(4).split(',')]))
    qf = [r for r in raw if r[0] == 'L' and r[1] == 'q']
    yi = next(i for i in range(len(qf[0][3])) if all(abs(abs(r[3][i]) - 1 / 6) < 1e-9 for r in qf))
    d0 = qf[0][2]
    c = next(i for i, e in enumerate(d0) if e.lstrip('-') == '3')
    l = next(i for i, e in enumerate(d0) if e == '2')
    return raw, yi, c, l


def bcoef(raw, yi, c, l):
    b = {'3': Fr(0), '2': Fr(0), 'Y': Fr(0)}
    nf = ns = 0
    for kind, lab, dims, q in raw:
        dc = abs(int(re.match(r'-?\d+', dims[c]).group(0)))
        dl = abs(int(re.match(r'-?\d+', dims[l]).group(0)))
        mult = 1
        for i, e in enumerate(dims):
            if i not in (c, l):
                mult *= abs(int(re.match(r'-?\d+', e).group(0)))
        Y = Fr(q[yi]).limit_denominator(36)
        w = Fr(2, 3) if kind == 'L' else Fr(1, 3)
        b['3'] += w * mult * dl * TSU3[dc]
        b['2'] += w * mult * dc * TSU2[dl]
        b['Y'] += w * mult * dc * dl * Y * Y
        if kind == 'L':
            nf += 1
        else:
            ns += 1
    # gauge bosons
    b['3'] += Fr(-11)
    b['2'] += Fr(-22, 3)
    return b, nf, ns


def solve(db):
    # 1/alpha_a = k_a x + bSM_a Ls/2pi + db_a LX/2pi ; unknowns x = 1/alpha_U, Ls, LX
    A = np.array([[float(kk[a]), float(bSM[a]) / (2 * math.pi), float(db[a]) / (2 * math.pi)] for a in ('3', '2', 'Y')])
    rhs = np.array([ia[a] for a in ('3', '2', 'Y')])
    x, Ls, LX = np.linalg.solve(A, rhs)
    aU = 1 / x
    Ms = MZ * math.exp(Ls)
    return dict(alphaU=aU, Ms_GeV=Ms, MX_GeV=Ms * math.exp(-LX), LX=LX, Ls=Ls, consistent=bool(0 <= LX <= Ls and aU > 0),
                Ms_heterotic_GeV=math.sqrt(4 * math.pi * aU) * 5.27e17 if aU > 0 else None)


if __name__ == '__main__':
    labs = json.load(open(r'C:\tmp\toe_wt\data\w33_pass11106_survivor_shifts.json'))['models']
    out = {}
    for k, v in labs.items():
        raw, yi, c, l = parse(r'C:\tmp\toe_round\stype\a8\%s.sm' % v['label'])
        b, nf, ns = bcoef(raw, yi, c, l)
        db = {a: b[a] - bSM[a] for a in b}
        sol = solve(db)
        out[k] = dict(label=v['label'], b_total={a: str(x) for a, x in b.items()}, delta_b={a: str(x) for a, x in db.items()}, n_L=nf, n_SC=ns, fit=sol)
        print(k, v['label'], {a: str(x) for a, x in db.items()}, {kk_: (round(x, 3) if isinstance(x, float) else x) for kk_, x in sol.items()}, flush=True)
    # control: SM alone (db = 0) cannot be solved -> report the two-coupling prediction instead
    json.dump(out, open(r'C:\tmp\toe_round\stype\survthresh.json', 'w'), indent=1, default=str)
