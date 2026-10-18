import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
_sys.path.insert(0, _HERE)
import json, sys
import numpy as np
sys.path.insert(0, '.')
import cwhess as C
from cwct import make_ct
out = {}
for name, x0 in C.POINTS.items():
    Hc = C.hess(make_ct(x0), x0, C.T)
    for s in (0.1, 1.0, 10.0):
        for Q in (0.5, 1.0, 2.0):
            V = C.make_V(x0, s, Q)
            H = C.hess(V, x0, C.T); gT = C.grad(V, x0, C.T); gL = C.grad(V, x0, C.L)
            cs = np.concatenate([-np.logspace(-4, 4, 400)[::-1], [0], np.logspace(-4, 4, 400)])
            m = [np.linalg.eigvalsh(H + c * Hc).min() for c in cs]; i = int(np.argmax(m))
            # relative measure: min eigenvalue over the largest |eigenvalue| at the best c
            ev = np.linalg.eigvalsh(H + cs[i] * Hc)
            out[f'{name}|s={s}|Q={Q}'] = dict(gradT=float(np.abs(gT).max()), gradL=float(np.abs(gL).max()), eigH=np.linalg.eigvalsh(H).tolist(),
                                            best_c=float(cs[i]), best_min_eig=float(m[i]), rel=float(m[i] / np.abs(ev).max()))
            print(name, s, Q, '%.1e %.2e' % (out[f'{name}|s={s}|Q={Q}']['gradT'], out[f'{name}|s={s}|Q={Q}']['gradL']),
                  'best min eig %.3e (rel %.3f) at c=%.3g' % (m[i], m[i] / np.abs(ev).max(), cs[i]), flush=True)
json.dump(out, open('cwfull.json', 'w'), indent=1)
