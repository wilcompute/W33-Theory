"""the scale where the critical point reproduces the measured M_H, and the M_t it then requires, with the sensitivity to alpha_s.  usage: py -3 mpp_k.py"""
import json
from scipy.optimize import brentq, fsolve
from sm_rge import beta_sm, matching, run
def sol(k, a3=0.1180):
    def at(mt, mh):
        m = matching(mt, mh, a3, 80.369); return run([m["gY"], m["g2"], m["g3"], m["yt"], m["lam"], 0.0155, 0.0100], mt, k)
    def eq(v):
        y = at(v[0], v[1]); return [y[4] * 100, beta_sm(y, 2)[4] * 1e3]
    return fsolve(eq, [171.0, 126.0], xtol=1e-6)
out = {}
for a3 in (0.1171, 0.1180, 0.1189):
    k = brentq(lambda lk: sol(10 ** lk, a3)[1] - 125.20, 16.5, 18.5, xtol=1e-3)
    s = sol(10 ** k, a3); out[a3] = dict(k=10 ** k, Mt=float(s[0]), MH=float(s[1]), dMt=float(s[0]) - 172.57)
s = sol(5.27e17); out["heterotic_5.27e17"] = dict(Mt=float(s[0]), MH=float(s[1]), dMt=float(s[0]) - 172.57, dMH=float(s[1]) - 125.20)
print(out); json.dump(out, open("mpp_k.json", "w"), indent=1, default=float)
