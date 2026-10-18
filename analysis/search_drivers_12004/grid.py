import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
"""Pass 12004: dense-grid certificate for the bare CP-real down sector at the up-required tau (frozen), then polish."""
import json
import sys

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, _HERE)
import downonly as D  # noqa: E402

sign, rtd = int(sys.argv[1]), int(sys.argv[2])
Uu = D.up_left(sign)
YD = np.logspace(np.log10(0.004), np.log10(1.5), 30)
ED = np.concatenate([-np.logspace(-4, np.log10(0.3), 15)[::-1], np.logspace(-4, np.log10(0.3), 15)])
out = []
for kz in range(6):
    best = []
    for yd in YD:
        ZI = np.linspace(-min(1.0, 27 * yd), min(1.0, 27 * yd), 30)
        for ed in ED:
            for zi in ZI:
                r = D.resid([yd, ed, zi], 'frozen', rtd, kz, Uu)
                best.append((float(np.sum(r ** 2)), yd, ed, zi))
    best.sort()
    grid_min = best[0][0]
    pol = []
    for c, yd, ed, zi in best[:12]:
        rr = least_squares(D.resid, [yd, ed, zi], args=('frozen', rtd, kz, Uu), method='trf', max_nfev=800)
        pol.append((float(2 * rr.cost), rr.x.tolist()))
    pol.sort(key=lambda t: t[0])
    o = D.obs(pol[0][1], 'frozen', rtd, kz, Uu)
    rec = dict(sign=sign, rtd=rtd, kz=kz, grid_points=len(best), grid_min_chi2=grid_min, polished_min_chi2=pol[0][0],
               x=pol[0][1], obs={k: float(v) for k, v in o.items()} if o else None)
    out.append(rec)
    print(json.dumps({k: rec[k] for k in ('sign', 'rtd', 'kz', 'grid_min_chi2', 'polished_min_chi2')}),
          {k: round(v, 5) for k, v in (o or {}).items()}, flush=True)
json.dump(out, open(_os.path.join(_HERE, f'grid_{sign}_{rtd}.json'), 'w'), indent=1)
