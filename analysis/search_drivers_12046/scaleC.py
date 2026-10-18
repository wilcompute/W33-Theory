"""Pass 12046 driver: follow 12045 branches in the MATCHING SCALE, using Codex 12011's SM one-loop running of the full
Yukawa matrices (its `running()` / `shape_observables`). At each scale the up home and the 6 geometric-row parameters
are re-solved against the running quark targets, and the parameter-free charged-lepton prediction is compared with the
running lepton targets. Run: py -3 scaleC.py <A|B|C> <npts>
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'search_drivers_12045'))
sys.path.insert(0, os.path.dirname(HERE))
import barrfit as B  # noqa: E402
import mcC as M  # noqa: E402
from jointlep import leptons  # noqa: E402
import w33_pass12011_12015_scale_flavour_internal_index as R  # noqa: E402
from curve import SOLS  # noqa: E402
import glob as _g
for _f in _g.glob(os.path.join(HERE, 'recover_*.json')):
    _d = json.load(open(_f))
    if _d['x']:
        SOLS[_d['label']] = _d['x']
from w33_pass11942_hypercharge_wilson_leptons import normalised  # noqa: E402


def bare_leptons(x):
    Od = np.array([[B.TAU, 1j * x[1]], [1j * x[1], 1j * np.exp(x[0])]])
    s = np.linalg.svd(B.PH.conj()[:, None] * normalised(Od, (0, 6j * x[2])), compute_uv=False)
    return s[1] / s[0], s[2] / s[1]

NAMES = R.NAMES          # yb_ytau, mc_mt, mu_mc, ms_mb, md_ms, Vus, Vcb, Vub, J, mmu_mtau, me_mmu
MZ = R.MZ


def targets(t):
    o = R.shape_observables(R.unpack(R.running().sol(t))[1])
    return dict(zip(NAMES, o))


if __name__ == '__main__':
    name, npts = sys.argv[1], int(sys.argv[2])
    tmax = np.log(2e16 / MZ)
    x = np.array(SOLS[name])
    pu = np.array([B.Y_UP, B.EU])
    rows = []
    for t in np.linspace(0, tmax, npts):
        tg = targets(t)
        q = {k: tg[k] for k in ('mc_mt', 'mu_mc', 'ms_mb', 'md_ms', 'Vus', 'Vcb', 'Vub', 'J')}
        ru = least_squares(M.up_resid, pu, args=(q,), xtol=1e-15, ftol=1e-15)
        M.set_up(*ru.x)
        B.DATA = q
        ok = False
        for sub in range(4):
            rd = least_squares(B.resid, x, args=('shared',), xtol=1e-15, ftol=1e-15, gtol=1e-15)
            if np.abs(rd.fun).max() < 1e-9 and np.abs(rd.x - x).max() < 0.3:
                ok = True
                break
        if not ok or np.abs(ru.fun).max() > 1e-9:
            print(name, 'lost the branch at mu = %.3g GeV' % (MZ * np.exp(t)), flush=True)
            break
        x, pu = rd.x, ru.x
        a, b = leptons(x)
        ba, bb = bare_leptons(x)
        comb_pred, comb_tgt = b * a * a, tg['me_mmu'] * tg['mmu_mtau'] ** 2
        rows.append(dict(mu=float(MZ * np.exp(t)), x=x.tolist(), up=pu.tolist(), mmu_mtau=[float(a), float(tg['mmu_mtau'])],
                         me_mmu=[float(b), float(tg['me_mmu'])], comb_ratio=float(comb_pred / comb_tgt), ms_mb_target=float(tg['ms_mb']), bare=[float(ba), float(bb)]))
        print(name, 'mu=%.3g GeV  m_mu/m_tau %.5f (tgt %.5f)  m_e/m_mu %.6f (tgt %.6f)  m_e m_mu/m_tau^2 ratio %.3f   bare (%.5f, %.6f)'
              % (MZ * np.exp(t), a, tg['mmu_mtau'], b, tg['me_mmu'], comb_pred / comb_tgt, ba, bb), flush=True)
    json.dump(dict(branch=name, rows=rows), open(os.path.join(HERE, f'scale_{name}.json'), 'w'), indent=1)
