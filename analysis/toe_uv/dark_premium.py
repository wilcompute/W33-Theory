"""How significant is crossing w = -1?  The premium is P = chi2(best w >= -1) - chi2(best free w) on 13 bins.  Under w >= -1 truth it is not chi2(n): many bins sit on the boundary, so it follows a chi-bar-squared mixture, which is what a p value must use.
Method: whiten the residual vector (SN with M projected out, BAO, compressed CMB) and solve the constrained fit by sequential bound-constrained least squares (scipy lsq_linear) with a trust region.  Convex in each step, so no starts to scatter, and it is an independent check of the differential evolution ceiling (dark_refine.py) and gives a global ceiling on Pantheon+, which only had a local one.
Mocks: truth = best w >= -1 fit of the real data, noise N(0,1) in whitened residuals.  Linear mocks (Jacobian at truth) and a smaller nonlinear set as a check on the linearisation.
Control: LCDM mocks with the 2 parameter CPL gain were already done in dark_mocks; here truth = LCDM must give a premium distribution no larger than truth = ceiling, and with bound removed the free fit gain must be chi2(n).
usage: py -3 dark_premium.py dataset data_dir n_linear n_nonlinear"""
import json
import sys
import numpy as np
from scipy.optimize import lsq_linear
from scipy.integrate import cumulative_trapezoid
import dark_like as L

ds, ddir, NL, NN = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
sn = L.load_sn(ds, ddir)
EDGES = json.load(open(f"dark_lowz_{ds}_0.0.json"))["edges"]
nb = len(EDGES) - 1
U = np.linalg.cholesky(sn["IC"]).T
ONES, SUM = sn["ones"], sn["sum"]
LC = np.linalg.cholesky(L.IC_CMB).T
LO = np.array([0.0215, 0.135, 0.62] + [-1.0] * nb)
LOF = np.array([0.0215, 0.135, 0.62] + [-6.0] * nb)
HI = np.array([0.023, 0.150, 0.74] + [1.0] * nb)
SC = np.array([2e-4, 1.5e-3, 5e-3] + [0.15] * nb)
STEP = np.array([2e-5, 2e-4, 5e-4] + [2e-3] * nb)


def model(x):
    E = L.E_binned(x[1], x[2], EDGES, x[3:])
    wb, wbc, h = x[:3]
    Dc = cumulative_trapezoid(1 / E, L.ZGRID, initial=0) * L.C / (100 * h)
    rd = 147.05 * (wb / 0.02236) ** -0.13 * (wbc / 0.1432) ** -0.23
    bao = []
    for d in L.DATA:
        z = d[0]
        DM = float(np.interp(z, L.ZGRID, Dc)) / rd
        DH = L.C / (100 * h * float(np.interp(z, L.ZGRID, E))) / rd
        if d[1] == "V":
            bao.append(((z * DM ** 2 * DH) ** (1 / 3) - d[2]) / d[3])
        else:
            a, b, r = (DM - d[2]) / d[3], (DH - d[4]) / d[5], d[6]
            bao += [a, (b - r * a) / np.sqrt(1 - r * r)]
    wm = wbc + L.OMEGA_NU_H2
    zs = L.zstar(wb, wm)
    th = L.CAL * L.rs_analytic(wb, wm, zs) / float(np.interp(zs, L.ZGRID, Dc))
    cmb = LC @ (np.array([th, wb, wbc]) - L.X_CMB)
    return Dc, np.array(bao), cmb


def resid(x, mu=None, xb=0.0):
    """whitened residual; mu overrides the observed SN vector, xb is an added noise vector on BAO and CMB"""
    Dc, bao, cmb = model(x)
    r = (sn["MU"] if mu is None else mu) - 5 * np.log10((1 + sn["ZH"]) * np.interp(sn["ZC"], L.ZGRID, Dc))
    return np.r_[U @ (r - (ONES @ r) / SUM), bao, cmb] + xb


def jac(f, x, r0):
    J = np.zeros((len(r0), len(x)))
    for i in range(len(x)):
        x2 = x.copy()
        x2[i] += STEP[i] if x[i] + STEP[i] < HI[i] else -STEP[i]
        J[:, i] = (f(x2) - r0) / (x2[i] - x[i])
    return J


def solve(f, x0, lo, iters=25, tr0=1.0):
    x = np.clip(x0, lo, HI)
    r = f(x)
    c = r @ r
    tr = tr0
    for it in range(iters):
        J = jac(f, x, r)
        for _ in range(8):
            l_ = np.maximum(lo, x - tr * SC)
            h_ = np.minimum(HI, x + tr * SC)
            s = lsq_linear(J, -r, bounds=(l_ - x, h_ - x), method="bvls" if J.shape[1] < 40 else "trf", tol=1e-10)
            x2 = x + s.x
            r2 = f(x2)
            c2 = r2 @ r2
            if c2 < c:
                break
            tr *= 0.5
        if not c2 < c:
            break
        gain = c - c2
        x, r, c = x2, r2, c2
        tr = min(tr * 1.5, 3.0)
        if gain < 1e-3:
            break
    return x, c


start = np.r_[0.02223, 0.1405, 0.675, np.full(nb, -0.95)]
real = lambda x: resid(x)
# LCDM: bins held at -1 by a tight bound
HI_save = HI.copy()
HI[3:] = -1.0 + 1e-9
lcdm_x, lcdm_chi = solve(real, np.r_[0.02223, 0.1405, 0.675, np.full(nb, -1.0)], LO)
HI[:] = HI_save
assert abs(lcdm_chi - L.chi2(L.E_binned(lcdm_x[1], lcdm_x[2], EDGES, lcdm_x[3:]), lcdm_x[2], lcdm_x[0], lcdm_x[1], sn)) < 1e-6
xc, cc = solve(real, np.r_[lcdm_x[:3], np.full(nb, -0.97)], LO)
# multistart, to test convexity in practice
rng = np.random.default_rng(3)
starts = [cc]
for i in range(8):
    x_, c_ = solve(real, np.r_[lcdm_x[:3], np.clip(rng.normal(-0.9, 0.12, nb), -1, 0.5)], LO)
    starts.append(c_)
    if c_ < cc:
        xc, cc = x_, c_
xf, cf = solve(real, np.r_[xc[:3], xc[3:] - 0.05], LOF)
for i in range(8):
    x_, c_ = solve(real, np.r_[lcdm_x[:3], rng.normal(-1.1, 0.4, nb)], LOF)
    if c_ < cf:
        xf, cf = x_, c_
prem = cc - cf
out = dict(dataset=ds, edges=EDGES, lcdm=lcdm_chi, ceiling=cc - lcdm_chi, free=cf - lcdm_chi, premium=prem, ceiling_starts=[s - lcdm_chi for s in starts], w_ceiling=list(xc[3:]), w_free=list(xf[3:]))
print({k: v for k, v in out.items() if k not in ("edges",)}, flush=True)
fn = f"dark_premium_{ds}.json"
json.dump(out, open(fn, "w"), indent=1, default=float)

# linear mocks: 16 dimensional after QR
rt = resid(xc)
J = jac(real, xc, rt)
Q, R = np.linalg.qr(J)
rng = np.random.default_rng(11)
n_ = len(rt)


def linear_premium(z):
    """z is the noise projected on Q; truth exact, so r0 = -z in the reduced space (free fit gain is relative to truth)."""
    a = lsq_linear(R, z, bounds=(LO - xc, HI - xc), method="bvls", tol=1e-10)
    b = lsq_linear(R, z, bounds=(LOF - xc, HI - xc), method="bvls", tol=1e-10)
    return 2 * a.cost - 2 * b.cost, -2 * a.cost + z @ z


P = np.zeros(NL)
G = np.zeros(NL)
for i in range(NL):
    P[i], G[i] = linear_premium(rng.normal(size=R.shape[0]))
# unbounded control: gain must be chi2(n params)
gfree = []
for i in range(2000):
    z = rng.normal(size=R.shape[0])
    gfree.append(z @ z)
out["linear"] = dict(n=NL, mean=float(P.mean()), q50=float(np.median(P)), q90=float(np.quantile(P, 0.9)), q99=float(np.quantile(P, 0.99)), frac_zero=float((P < 1e-6).mean()), p_real=float((P >= prem).mean()), mean_ceiling_gain_over_truth=float(G.mean()), control_unbounded_mean=float(np.mean(gfree)), n_params=int(R.shape[0]))
print(out["linear"], flush=True)
json.dump(out, open(fn, "w"), indent=1, default=float)

# nonlinear mocks
rows = []
# a mock replaces the residual at truth on real data with pure noise, in whitened space
for i in range(NN):
    noise = rng.normal(size=n_)
    f = lambda x: resid(x) - rt + noise  # residual of a mock whose truth is xc
    a, ca = solve(f, xc, LO, iters=8)
    b, cb = solve(f, np.r_[a[:3], a[3:]], LOF, iters=8)
    rows.append((ca, cb, ca - cb))
    if (i + 1) % 20 == 0:
        r_ = np.array(rows)
        out["nonlinear"] = dict(n=i + 1, mean=float(r_[:, 2].mean()), q50=float(np.median(r_[:, 2])), q90=float(np.quantile(r_[:, 2], 0.9)), p_real=float((r_[:, 2] >= prem).mean()), rows=rows)
        json.dump(out, open(fn, "w"), indent=1, default=float)
        print(i + 1, out["nonlinear"]["mean"], out["nonlinear"]["p_real"], flush=True)
print("done", flush=True)
