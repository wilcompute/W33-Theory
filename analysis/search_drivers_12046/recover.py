"""Pass 12046 driver: recover full coordinates of 12045 catalogue branches from their invariant keys
(Im tau_d, |eps_d|, |Im z_d|, lambda, m_mu/m_tau, m_e/m_mu) by solving from seeds over sign choices and a w grid.
Run: py -3 recover.py <label> <Im tau_d> <|eps|> <|z|> <lambda> <mmu_mtau> <me_mmu>
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
from jointlep import leptons  # noqa: E402

lab = sys.argv[1]
yd, ae, az, lam, l1, l2 = map(float, sys.argv[2:8])
found = None
for se in (1, -1):
    for sz in (1, -1):
        for rw in np.linspace(-0.5, 0.45, 20):
            for iw in np.linspace(-10, 10, 41):
                x0 = np.array([np.log(yd), se * ae, sz * az, np.log(lam), rw, iw])
                if np.abs(B.resid(x0, 'shared')).max() > 3:
                    continue
                r = least_squares(B.resid, x0, args=('shared',), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=400)
                if np.abs(r.fun).max() > 1e-9:
                    continue
                a, b = leptons(r.x)
                if abs(np.exp(r.x[0]) / yd - 1) < 1e-3 and abs(a / l1 - 1) < 1e-3 and abs(b / l2 - 1) < 1e-3:
                    found = r.x.tolist()
                    break
            if found:
                break
        if found:
            break
    if found:
        break
print(lab, 'recovered' if found else 'NOT recovered', found, flush=True)
json.dump(dict(label=lab, x=found), open(os.path.join(HERE, f'recover_{lab}.json'), 'w'))
