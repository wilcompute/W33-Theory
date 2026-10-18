"""Pass 12045 driver: linear sensitivity d ln(lepton ratio) / d ln(quark target) at each isolated solution,
by re-solving after a small log-shift of one target (up targets re-solve the up home first)."""
import numpy as np
from scipy.optimize import least_squares

import barrfit as B
import mcC as M
from jointlep import leptons
from w33_pass11942_hypercharge_wilson_leptons import DATA as D0, LEPTONS

SOLS = {'A': np.load('shared_sol.npy'), 'B': np.array([1.139142, -1.15415, -0.238268, 5.502257, 0.403614, -0.99549]),
        'C': np.load('solC.npy')}
H = 1e-3


def solve(tgt, x0):
    ru = least_squares(M.up_resid, [B.Y_UP, B.EU], args=(tgt,), xtol=1e-15, ftol=1e-15)
    M.set_up(*ru.x)
    B.DATA = tgt
    rd = least_squares(B.resid, x0, args=('shared',), xtol=1e-15, ftol=1e-15, gtol=1e-15)
    assert np.abs(rd.fun).max() < 1e-9 and np.abs(ru.fun).max() < 1e-9
    return rd.x


for name, x0 in SOLS.items():
    x0 = solve(dict(D0), x0)
    l0 = np.log(leptons(x0))
    S = {}
    for k in D0:
        tp, tm = dict(D0), dict(D0)
        tp[k] *= np.exp(H)
        tm[k] *= np.exp(-H)
        S[k] = (np.log(leptons(solve(tp, x0))) - np.log(leptons(solve(tm, x0)))) / (2 * H)
    sig = np.sqrt(sum((S[k] * M.ERR[k]) ** 2 for k in D0))
    pred = np.exp(l0)
    print(name, 'prediction', np.round(pred, 6), 'data', np.round([LEPTONS['mmu_mtau'], LEPTONS['me_mmu']], 6),
          'pull (log units / sigma):', np.round((np.log([LEPTONS['mmu_mtau'], LEPTONS['me_mmu']]) - l0) / sig, 2), 'sigma_ln', np.round(sig, 3))
    print('   sensitivities', {k: np.round(v, 2).tolist() for k, v in S.items()})
