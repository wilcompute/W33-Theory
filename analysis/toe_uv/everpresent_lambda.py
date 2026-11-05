"""Everpresent Lambda (Sorkin 1987; Ahmed, Dodelson, Greene, Sorkin 2004; Zwane, Afshordi, Sorkin 2017) against DESI DR2 + SN + compressed CMB.  The only framework that predicted the size of Lambda in advance: discrete spacetime gives Lambda fluctuations ~ 1/sqrt(V), V the past 4-volume, with no fields.
Model (the ADGS stochastic form): Lambda_n = alpha S_n / V_n, S_(n+1) = S_n + xi_n sqrt(V_(n+1) - V_n), xi standard normal.  V = integral a^3 (4 pi/3) chi^3 dt.  alpha is the one parameter, of order 1 in natural units if the discreteness is at the Planck scale times an order-one number.  Units: H^2 in omega units, (100 km/s/Mpc)^2, rho_Lambda in omega units is Lambda / 3.
omega_b, omega_m and omega_r are held at their Planck values.  H0 is not chosen: it emerges from each history as sqrt(H^2 at a = 1).  So a history has no free parameter.  H^2 < 0 in the past means a crunch, and the history has zero likelihood.  (Energy is not conserved by this form; the Friedmann constraint is used and Barrow's objection, gr-qc/0612128, is about this amplitude.)
Marginal: ln Z(alpha) = ln < exp(-chi2/2) > over histories, all drawn, so rarity is counted.  Compared with LCDM at the same omega_b, omega_m with h fitted: chi2_L; a flat prior for Lambda would add an Occam cost to LCDM, which is reported separately as a tuning factor, the fraction of the natural prior range that lands within the data's h window.
Control: alpha = 0 with Lambda fixed by hand reproduces LCDM from L.chi2.  Also rms Lambda scales as alpha/sqrt(V).  Also early dark energy fraction at z = 1090 is reported, the Barrow test.
Perturbations are ignored: compressed CMB distances only, and the CMB is compressed assuming standard physics, so an early fraction above about 1 percent makes this test too generous.
usage: python3 everpresent_lambda.py dataset"""
import json
import math
import os
import sys
import numpy as np
import dark_like as L

ds = sys.argv[1]
FORM = os.environ.get("FORM", "cone")  # cone: past light cone volume; comoving: V = integral a^3 dt, the Ahmed et al / Zwane et al form, with an arbitrary comoving unit absorbed in alpha
AL = [float(x) for x in os.environ.get("ALPHAS", "0.003,0.01,0.03,0.1,0.3,1.0,3.0").split(",")]
SND = os.path.expanduser(os.environ.get("SND", "~/cosmo/snsdata"))
sn = L.load_sn(ds, SND)
WB, WBC = 0.02223, 0.14208  # the compressed CMB centre
WR = 4.18e-5
WM = WBC + L.OMEGA_NU_H2
AI = math.log(1 / 8000.0)
NG = np.linspace(AI, 0.0, 700)
A = np.exp(NG)
dN = NG[1] - NG[0]
rng = np.random.default_rng(int(os.environ.get("SEED", 11)))
ZINT = 1 / A[::-1] - 1


def run(alpha, M):
    H2b = WM * A ** -3 + WR * A ** -4
    # start: radiation era with analytic volume
    H0i = math.sqrt(H2b[0])
    t_i = 0.5 / H0i
    chi_i = 2 * t_i / A[0]  # conformal, radiation
    V = np.full(M, A[0] ** 3 * t_i / 2.5 if FORM == "comoving" else (4 * math.pi / 3) * A[0] ** 3 * chi_i ** 3 * t_i / 5.0)
    chi = np.full(M, chi_i)
    S = rng.standard_normal(M) * np.sqrt(V)
    H2 = np.zeros((M, len(NG)))
    alive = np.ones(M, bool)
    for j, a in enumerate(A):
        lam = alpha * S / V
        h2 = H2b[j] + lam / 3.0
        alive &= h2 > 0
        h2 = np.where(h2 > 0, h2, H2b[j])
        H2[:, j] = h2
        Hh = np.sqrt(h2)
        dV = a ** 3 * dN / Hh if FORM == "comoving" else a ** 3 * (4 * math.pi / 3) * chi ** 3 * dN / Hh
        chi = chi + dN / (a * Hh)
        V = V + dV
        S = S + rng.standard_normal(M) * np.sqrt(dV)
    return H2, alive


def chi2_of(H2row):
    h = math.sqrt(H2row[-1])
    z = 1 / A[::-1] - 1
    E = np.sqrt(H2row[::-1]) / h
    Eg = np.exp(np.interp(np.log1p(L.ZGRID), np.log1p(z), np.log(E), right=np.nan))
    # beyond the start of the grid use standard matter + radiation
    bad = ~np.isfinite(Eg)
    Eg[bad] = np.sqrt(WM * (1 + L.ZGRID[bad]) ** 3 + WR * (1 + L.ZGRID[bad]) ** 4) / h
    return L.chi2(Eg, h, WB, WBC, sn), h


# LCDM reference with the same omega values
bestL = None
for h in np.linspace(0.62, 0.74, 241):
    E = np.sqrt(WM * (1 + L.ZGRID) ** 3 + WR * (1 + L.ZGRID) ** 4 + (h * h - WM - WR)) / h
    c = L.chi2(E, h, WB, WBC, sn)
    if bestL is None or c < bestL[0]:
        bestL = (float(c), float(h))
out = dict(dataset=ds, LCDM_chi2=bestL[0], LCDM_h=bestL[1], rows={})
print("LCDM", bestL, flush=True)
# control: compare a history with alpha tiny and constant Lambda path
ctrl_rows = {}
for alpha in AL:
    tot = 0.0
    n_all = 0
    n_chi = 0
    lnw = []
    best = None
    ede = []
    win = 0
    surv = 0
    hs = []
    for b in range(int(os.environ.get("BATCHES", 8))):
        M = 40000
        H2, alive = run(alpha, M)
        n_all += M
        surv += int(alive.sum())
        h = np.sqrt(H2[:, -1])
        keep = alive & (h > 0.60) & (h < 0.76)
        win += int(keep.sum())
        i1090 = np.argmin(np.abs(ZINT[::-1] - 1090.0))
        bg = WM * A[i1090] ** -3 + WR * A[i1090] ** -4
        ede.append(float(np.std((H2[alive, i1090] - bg) / H2[alive, i1090])) if alive.any() else float("nan"))
        ogl = (H2[alive, -1] - (WM + WR))
        om_rms = float(np.std(ogl)) if alive.any() else float("nan")
        hs.extend(h[alive][:200].tolist())
        for r in H2[keep][:int(os.environ.get("NCHI", 600))]:
            c, hh = chi2_of(r)
            n_chi += 1
            lnw.append(-0.5 * c)
            if best is None or c < best[0]:
                best = (float(c), float(hh))
    # thinned chi2: scale by keep fraction
    frac = win / n_all
    if lnw:
        lnw = np.array(lnw)
        lnZ = float(np.logaddexp.reduce(lnw) - math.log(len(lnw)) + math.log(max(frac, 1e-300)))
    else:
        lnZ = None
    row = dict(alpha=alpha, n=n_all, survive=surv / n_all, h_window=frac, n_chi2=n_chi, lnZ=lnZ, lnZ_minus_LCDM=None if lnZ is None else lnZ + 0.5 * bestL[0], best_chi2=None if best is None else best[0], best_delta=None if best is None else best[0] - bestL[0], best_h=None if best is None else best[1], early_fraction_rms=float(np.nanmean(ede)), h_q=[float(q) for q in np.quantile(hs, [.16, .5, .84])] if hs else None, omega_lambda_today_rms=om_rms)
    out["rows"][str(alpha)] = row
    print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()}, flush=True)
    json.dump(out, open(f"everpresent_lambda_{ds}_{FORM}.json", "w"), indent=1, default=float)
print("everdone", flush=True)
