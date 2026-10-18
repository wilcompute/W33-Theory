"""Pass 12045 driver: propagate the quark-input uncertainties through solution C to its lepton prediction.
Each trial: perturb the 8 quark targets (log-normal, errors of Pass 12004/12044), re-solve the up home (y, eps_u on the
CP locus) and the 6 geometric-row down parameters starting from C, record (m_mu/m_tau, m_e/m_mu).
Run: py -3 mcC.py <trials> <seed>
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import least_squares

import barrfit as B
from jointlep import leptons
from w33_pass11942_hypercharge_wilson_leptons import DATA as D0, LEPTONS, theta

HERE = os.path.dirname(os.path.abspath(__file__))
ERR = dict(mc_mt=.05, mu_mc=.20, ms_mb=.08, md_ms=.10, Vus=.003, Vcb=.025, Vub=.05, J=.04)
XC = np.load(os.path.join(HERE, 'solC.npy'))


def set_up(y, e):
    B.TAU = 1 + 1j * y
    Ou = np.array([[B.TAU, 1j * e], [1j * e, B.TAU]])
    u = B.PH.conj()[:, None] * theta(Ou) * B.PH.conj()[None, :]
    u = u.real / np.linalg.norm(u)
    B.U = u @ np.diag([np.sign(np.linalg.det(u)), 1, 1])
    B.UU, B.SU, _ = np.linalg.svd(B.U)


def up_resid(p, tgt):
    Ou = np.array([[1 + 1j * p[0], 1j * p[1]], [1j * p[1], 1 + 1j * p[0]]])
    s = np.linalg.svd(theta(Ou), compute_uv=False)
    return [np.log(s[1] / s[0] / tgt['mc_mt']), np.log(s[2] / s[1] / tgt['mu_mc'])]


if __name__ == '__main__':
    n, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = np.random.default_rng(seed)
    rows = []
    for t in range(n):
        tgt = {k: D0[k] * np.exp(ERR[k] * rng.normal()) for k in D0}
        pu, xd, ok, jump = np.array([B.Y_UP, B.EU]), XC.copy(), True, 0.0
        for s in np.linspace(0.05, 1, 20):          # homotopy: follow the branch of C continuously
            ts = {k: D0[k] ** (1 - s) * tgt[k] ** s for k in D0}
            ru = least_squares(up_resid, pu, args=(ts,), xtol=1e-15, ftol=1e-15)
            set_up(*ru.x)
            B.DATA = ts
            rd = least_squares(B.resid, xd, args=('shared',), xtol=1e-15, ftol=1e-15, gtol=1e-15)
            if np.abs(ru.fun).max() > 1e-8 or np.abs(rd.fun).max() > 1e-8:
                ok = False
                break
            jump = max(jump, float(np.abs(rd.x - xd).max()))
            pu, xd = ru.x, rd.x
        if not ok:
            continue
        a, b = leptons(xd)
        rows.append([float(a), float(b), float(np.abs(xd - XC).max()), jump])
    rows = np.array(rows)
    json.dump(dict(seed=seed, trials=n, kept=len(rows), rows=rows.tolist()), open(os.path.join(HERE, f'mcC_{seed}.json'), 'w'))
    for k, name in enumerate(('mmu_mtau', 'me_mmu')):
        q = np.percentile(rows[:, k], [2.5, 16, 50, 84, 97.5])
        print(name, 'data %.6f' % LEPTONS[name], 'band 2.5/16/50/84/97.5:', np.round(q, 6).tolist(), flush=True)
    print('kept', len(rows), 'of', n, flush=True)
