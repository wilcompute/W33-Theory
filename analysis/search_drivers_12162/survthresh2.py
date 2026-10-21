"""12162b: two exotic scales (coloured M_c, colourless M_l), M_s fixed at the heterotic value g_U * 5.27e17 GeV (self-consistent);
solve the three measured couplings exactly for 1/alpha_U, L_c = ln(M_s/M_c), L_l = ln(M_s/M_l); require 0 <= L_c, L_l <= L_s."""
import re, json, math
from fractions import Fraction as Fr
import numpy as np
import survthresh as S


def split_b(raw, yi, c, l):
    out = {}
    for part in ('col', 'nocol'):
        b = {'3': Fr(0), '2': Fr(0), 'Y': Fr(0)}
        for kind, lab, dims, q in raw:
            dc = abs(int(re.match(r'-?\d+', dims[c]).group(0)))
            if (dc > 1) != (part == 'col'):
                continue
            dl = abs(int(re.match(r'-?\d+', dims[l]).group(0)))
            mult = 1
            for i, e in enumerate(dims):
                if i not in (c, l):
                    mult *= abs(int(re.match(r'-?\d+', e).group(0)))
            Y = Fr(q[yi]).limit_denominator(36)
            w = Fr(2, 3) if kind == 'L' else Fr(1, 3)
            b['3'] += w * mult * dl * S.TSU3[dc]
            b['2'] += w * mult * dc * S.TSU2[dl]
            b['Y'] += w * mult * dc * dl * Y * Y
        out[part] = b
    return out


# SM pieces split the same way: coloured SM (Q, u, d) and colourless SM (L, e, one Higgs) + gauge
def sm_split():
    col = {'3': Fr(2, 3) * 3 * (2 * Fr(1, 2) + Fr(1, 2) + Fr(1, 2)), '2': Fr(2, 3) * 3 * 3 * Fr(1, 2),
           'Y': Fr(2, 3) * 3 * (6 * Fr(1, 36) + 3 * Fr(4, 9) + 3 * Fr(1, 9))}
    noc = {'3': Fr(0), '2': Fr(2, 3) * 3 * Fr(1, 2) + Fr(1, 3) * Fr(1, 2), 'Y': Fr(2, 3) * 3 * (2 * Fr(1, 4) + 1) + Fr(1, 3) * 2 * Fr(1, 4)}
    return col, noc


if __name__ == '__main__':
    smc, smn = sm_split()
    chk = {a: smc[a] + smn[a] + {'3': Fr(-11), '2': Fr(-22, 3), 'Y': 0}[a] for a in smc}
    assert chk == S.bSM, chk
    labs = json.load(open(r'C:\tmp\toe_wt\data\w33_pass11106_survivor_shifts.json'))['models']
    out = {}
    for k, v in labs.items():
        raw, yi, c, l = S.parse(r'C:\tmp\toe_round\stype\a8\%s.sm' % v['label'])
        sb = split_b(raw, yi, c, l)
        dbc = {a: sb['col'][a] - smc[a] for a in smc}
        dbl = {a: sb['nocol'][a] - smn[a] for a in smn}
        Ls = math.log(5e17 / S.MZ)
        for _ in range(200):
            A = np.array([[float(S.kk[a]), float(dbc[a]) / (2 * math.pi), float(dbl[a]) / (2 * math.pi)] for a in ('3', '2', 'Y')])
            rhs = np.array([S.ia[a] - float(S.bSM[a]) * Ls / (2 * math.pi) for a in ('3', '2', 'Y')])
            x, Lc, Ll = np.linalg.solve(A, rhs)
            if x <= 0:
                break
            Ls_new = math.log(math.sqrt(4 * math.pi / x) * 5.27e17 / S.MZ)
            if abs(Ls_new - Ls) < 1e-12:
                break
            Ls = Ls_new
        Ms = S.MZ * math.exp(Ls)
        ok = bool(x > 0 and 0 <= Lc <= Ls and 0 <= Ll <= Ls)
        out[k] = dict(label=v['label'], db_col={a: str(x_) for a, x_ in dbc.items()}, db_nocol={a: str(x_) for a, x_ in dbl.items()},
                      alphaU=1 / x if x > 0 else None, Ms_GeV=Ms, Mc_GeV=Ms * math.exp(-Lc), Ml_GeV=Ms * math.exp(-Ll), consistent=ok)
        print(k, v['label'], 'aU %.4f' % (1 / x) if x > 0 else 'aU<0', 'Ms %.2e Mc %.2e Ml %.2e' % (Ms, Ms * math.exp(-Lc), Ms * math.exp(-Ll)), 'OK' if ok else '--', flush=True)
    json.dump(out, open(r'C:\tmp\toe_round\stype\survthresh2.json', 'w'), indent=1, default=str)
