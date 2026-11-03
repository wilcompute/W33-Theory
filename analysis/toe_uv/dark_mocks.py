"""Control for the low-z cut.  Removing supernovae removes leverage, so a smaller CPL gain is expected even if CPL is true.  Mocks: truth = CPL best fit of the real data; SN, BAO and compressed CMB all redrawn from their covariances; the gain of CPL over LCDM is fitted with all SNe and with z > zmin, on the same mock.
Reported: the distribution of gain_cut, and how often gain_cut is as weak as the real one among mocks whose full gain is at least as strong as the real one.
Validity control: mocks drawn from the LCDM best fit must give a mean gain near 2 (two extra parameters).  usage: py -3 dark_mocks.py dataset data_dir zmin truth(cpl|lcdm) nmocks seed"""
import json
import sys
import numpy as np
from scipy.optimize import minimize
import dark_like as L

ds, ddir, zmin, truth, nm_, seed = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], int(sys.argv[5]), int(sys.argv[6])
sn = L.load_sn(ds, ddir)
Cv = np.linalg.inv(sn["IC"])
chol = np.linalg.cholesky(Cv)
keep = sn["ZC"] > zmin
IC2 = np.linalg.inv(Cv[keep][:, keep])
base = dict(ZC=sn["ZC"], ZH=sn["ZH"], IC=sn["IC"], sum=sn["sum"], ones=sn["ones"], n=sn["n"])
cut = dict(ZC=sn["ZC"][keep], ZH=sn["ZH"][keep], IC=IC2, sum=IC2.sum(), ones=IC2.sum(1), n=int(keep.sum()))
S = np.array([1e-4, 1e-3, 3e-3])
OPT = dict(xatol=2e-5, fatol=2e-3)


def nm(fn, x0, steps, maxiter):
    x0 = np.asarray(x0, float)
    return minimize(fn, x0, method="Nelder-Mead", options=dict(OPT, maxiter=maxiter, maxfev=maxiter, initial_simplex=np.vstack([x0] + [x0 + np.eye(len(x0))[i] * steps[i] for i in range(len(x0))])))


def fit_pair(s, x_l, x_c):
    a = nm(lambda p: L.chi2(L.E_lcdm(p[1], p[2]), p[2], p[0], p[1], s), x_l, S, 500)
    f = lambda p: L.chi2(L.E_cpl(p[1], p[2], p[3], p[4]), p[2], p[0], p[1], s) if p[3] + p[4] < 0 else 1e8
    b = min((nm(f, x0, np.r_[S, 0.05, 0.2], 1100) for x0 in (x_c, np.r_[a.x, -0.95, -0.2])), key=lambda r: r.fun)
    return b.fun - a.fun, b.x


real = dict(base, MU=sn["MU"])
rc = dict(cut, MU=sn["MU"][keep])
x_l = [0.02223, 0.1405, 0.68]
g_full, x_c = fit_pair(real, x_l, [0.02223, 0.1405, 0.675, -0.85, -0.5])
g_cut, _ = fit_pair(rc, x_l, x_c)
print("real", g_full, g_cut, x_c, flush=True)
if truth == "cpl":
    E = L.E_cpl(x_c[1], x_c[2], x_c[3], x_c[4])
    wb, wbc, h = x_c[:3]
else:
    r0 = nm(lambda p: L.chi2(L.E_lcdm(p[1], p[2]), p[2], p[0], p[1], real), x_l, S, 500)
    wb, wbc, h = r0.x
    E = L.E_lcdm(wbc, h)
chi = np.cumsum(np.r_[0, 0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(L.ZGRID)]) * L.C / (100 * h)
mu0 = 5 * np.log10((1 + sn["ZH"]) * np.interp(sn["ZC"], L.ZGRID, chi))
rd = 147.05 * (wb / 0.02236) ** -0.13 * (wbc / 0.1432) ** -0.23
D0 = list(L.DATA)
X0 = L.X_CMB.copy()
wm = wbc + L.OMEGA_NU_H2
zs = L.zstar(wb, wm)
xt = np.array([L.CAL * L.rs_analytic(wb, wm, zs) / float(np.interp(zs, L.ZGRID, chi)), wb, wbc])
LC = np.linalg.cholesky(L.C_CMB)
rng = np.random.default_rng(seed)
rows = []
for i in range(nm_):
    mock_mu = mu0 + chol @ rng.normal(size=sn["n"])
    nd = []
    for d in D0:
        z = d[0]
        DM = float(np.interp(z, L.ZGRID, chi)) / rd
        DH = L.C / (100 * h * float(np.interp(z, L.ZGRID, E))) / rd
        if d[1] == "V":
            nd.append((z, "V", (z * DM ** 2 * DH) ** (1 / 3) + d[3] * rng.normal(), d[3]))
        else:
            r = d[6]
            n1, n2 = rng.normal(size=2)
            nd.append((z, "MH", DM + d[3] * n1, d[3], DH + d[5] * (r * n1 + np.sqrt(1 - r * r) * n2), d[5], r))
    L.DATA[:] = nd
    L.X_CMB[:] = xt + LC @ rng.normal(size=3)
    gf, xf = fit_pair(dict(base, MU=mock_mu), x_l, x_c)
    gc, _ = fit_pair(dict(cut, MU=mock_mu[keep]), x_l, xf)
    rows.append((gf, gc))
    if (i + 1) % 10 == 0:
        json.dump(dict(dataset=ds, zmin=zmin, truth=truth, real_full=g_full, real_cut=g_cut, x_cpl=list(x_c), rows=rows), open(f"dark_mocks_{ds}_{truth}_{seed}.json", "w"))
        print(i + 1, flush=True)
json.dump(dict(dataset=ds, zmin=zmin, truth=truth, real_full=g_full, real_cut=g_cut, x_cpl=list(x_c), rows=rows), open(f"dark_mocks_{ds}_{truth}_{seed}.json", "w"))
print("done", flush=True)
