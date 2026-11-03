"""The other half of dark_premium.py: under LCDM truth, how often does the same 13-bin fit gain as much as the real data, with w >= -1 and with w free?  Both tests are one-sided mixtures, so the p values come from linear mocks.
Together with the premium this separates three statements: LCDM rejected by a w >= -1 history, LCDM rejected by any history, and w >= -1 rejected in favour of crossing.  Control: with the bound removed the gain must average n bins.
usage: py -3 dark_premium2.py dataset data_dir n"""
import json
import sys
import numpy as np
from scipy.optimize import lsq_linear

ds_, dd_, n_ = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.argv = ["x", ds_, dd_, "0", "0"]
exec(open("dark_premium.py", encoding="utf-8").read().split("start = np.r_[0.02223")[0])
prev = json.load(open(f"dark_premium_{ds_}.json"))
HI_save = HI.copy()
HI[3:] = -1.0 + 1e-9
x0, c0 = solve(lambda x: resid(x), np.r_[0.02223, 0.1405, 0.675, np.full(nb, -1.0)], LO)
HI[:] = HI_save
rt = resid(x0)
J = jac(lambda x: resid(x), x0, rt)
# the first three columns are the LCDM nuisance directions; project them out for a clean gain
Q, R = np.linalg.qr(J)
rng = np.random.default_rng(23)
gc, gf = np.zeros(n_), np.zeros(n_)
for i in range(n_):
    z = rng.normal(size=R.shape[0])
    base = lsq_linear(R[:, :3], z, method="bvls", tol=1e-10)
    a = lsq_linear(R, z, bounds=(LO - x0, HI - x0), method="bvls", tol=1e-10)
    b = lsq_linear(R, z, bounds=(LOF - x0, HI - x0), method="bvls", tol=1e-10)
    gc[i] = 2 * base.cost - 2 * a.cost
    gf[i] = 2 * base.cost - 2 * b.cost
real_c, real_f = -prev["ceiling"], -prev["free"]
out = dict(dataset=ds_, n=n_, real_ceiling_gain=real_c, real_free_gain=real_f, p_ceiling=float((gc >= real_c).mean()), p_free=float((gf >= real_f).mean()), mean_ceiling=float(gc.mean()), mean_free=float(gf.mean()), q99_ceiling=float(np.quantile(gc, 0.99)), n_bins=nb)
print(out, flush=True)
json.dump(out, open(f"dark_premium2_{ds_}.json", "w"), indent=1, default=float)
