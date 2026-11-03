"""Multiple-point criticality (Froggatt-Nielsen; Buttazzo et al.): lambda(k) = 0 and beta_lambda(k) = 0 at one scale k are two conditions on (M_t, M_H), with no free parameter once k is fixed.  Scan k from 1e16 to 1e21 GeV: solve for (M_t, M_H), compare with measurement.  Also: the single-condition lines, lambda(M_Pl) = 0.  Fair null for 'how special is the measured point': the fraction of the plane (M_t in 150-200, M_H in 100-160) lying within the observed distance of the critical point, and the look-elsewhere factor from the choice of k.
usage: py -3 criticality.py"""
import json
import math
from scipy.optimize import fsolve
from sm_rge import beta_sm, matching, run

A3, MW = 0.1180, 80.369
MT_OBS, MT_ERR = 172.57, 0.29
MH_OBS, MH_ERR = 125.20, 0.11
# theory ambiguity of the pole-mass extraction, as usually quoted, and two-loop truncation here (about 8e-4 in lambda(M_Pl) against Buttazzo, i.e. 0.28 GeV in M_H, 0.12 GeV in M_t)
MT_THEORY = 0.5


def at_k(mt, mh, k):
    m = matching(mt, mh, A3, MW)
    return run([m["gY"], m["g2"], m["g3"], m["yt"], m["lam"], 0.0155, 0.0100], mt, k)


out = dict(scan=[])
for k in (1e16, 1e17, 1e18, 1e19, 1.22e19, 2.4e18, 1e20, 1e21):
    def eqs(v):
        y = at_k(v[0], v[1], k)
        return [y[4] * 100, beta_sm(y, 2)[4] * 1e3]
    sol, info, ok, msg = fsolve(eqs, [171.0, 127.0], full_output=True, xtol=1e-6)
    mt, mh = float(sol[0]), float(sol[1])
    y = at_k(mt, mh, k)
    out["scan"].append(dict(k=k, converged=ok == 1, Mt=mt, MH=mh, dMt=mt - MT_OBS, dMH=mh - MH_OBS, pull_Mt=(mt - MT_OBS) / math.hypot(MT_ERR, MT_THEORY), pull_MH=(mh - MH_OBS) / MH_ERR, residual=[y[4], beta_sm(y, 2)[4]]))
    print({a: (round(b, 3) if isinstance(b, float) else b) for a, b in out["scan"][-1].items() if a != "residual"}, flush=True)
y = at_k(MT_OBS, MH_OBS, 1e19)
out["measured_at_1e19"] = dict(lam=y[4], beta_lam=beta_sm(y, 2)[4])
best = None
import numpy as np
for lk in np.linspace(9, 21, 241):
    yy = at_k(MT_OBS, MH_OBS, 10 ** lk)
    b = abs(beta_sm(yy, 2)[4])
    if best is None or b < best[0]:
        best = (b, float(lk), float(yy[4]))
out["measured_beta_lam_min"] = dict(abs_beta=best[0], log10k=best[1], lam_there=best[2])
print(out["measured_at_1e19"], out["measured_beta_lam_min"])
json.dump(out, open("criticality.json", "w"), indent=1, default=float)
