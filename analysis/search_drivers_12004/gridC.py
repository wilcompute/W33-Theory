import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
"""Pass 12004: accurate full-range grid for the bare CP-real down sector at the up-required tau (centred theta evaluator)."""
import json
import sys

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, _HERE)
import deep  # noqa: E402
import downonly as D  # noqa: E402

sign, rtd = int(sys.argv[1]), int(sys.argv[2])
Uu = D.up_left(sign)
YD = np.logspace(-4, 1, 36)
U = np.concatenate([-np.logspace(-3.5, np.log10(0.97), 12)[::-1], np.logspace(-3.5, np.log10(0.97), 12)])
W = np.concatenate([-np.logspace(-1.5, np.log10(60), 18)[::-1], np.logspace(-1.5, np.log10(60), 18)])
out = []
for kz in range(6):
    pts = []
    for yd in YD:
        for u in U:
            ed = u * np.sqrt(D.Y_UP * yd)
            for w in W:
                p = [yd, ed, w * yd]
                pts.append((float(np.sum(deep.resid(p, rtd, kz, Uu) ** 2)), p))
    pts.sort(key=lambda t: t[0])
    pol = []
    for c, p in pts[:20]:
        r = least_squares(deep.resid, p, args=(rtd, kz, Uu), method='trf', max_nfev=600, x_scale=[p[0], np.sqrt(p[0]), p[0]])
        pol.append((float(2 * r.cost), r.x.tolist()))
    pol.sort(key=lambda t: t[0])
    o = deep.obs_deep(pol[0][1], rtd, kz, Uu)
    rec = dict(sign=sign, rtd=rtd, kz=kz, grid_points=len(pts), grid_min_chi2=pts[0][0], polished_min_chi2=pol[0][0], x=pol[0][1],
               obs={k: float(v) for k, v in o.items()} if o else None)
    out.append(rec)
    print(json.dumps({k: rec[k] for k in ('sign', 'rtd', 'kz', 'grid_min_chi2', 'polished_min_chi2')}), [float('%.4g' % v) for v in rec['x']],
          {k: round(v, 5) for k, v in (o or {}).items()}, flush=True)
json.dump(out, open(_os.path.join(_HERE, f'gridC_{sign}_{rtd}.json'), 'w'), indent=1)
