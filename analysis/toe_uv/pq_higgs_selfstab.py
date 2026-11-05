"""Outside idea: do Model A's (or trinification's) heavy quarks stabilise the Higgs by themselves?
Above M_X the extra coloured states make b3 less negative, so g3 stays larger, y_t falls faster, and the -6 y_t^4 term that drives lambda negative weakens.  My one-loop lambda is not accurate (it crosses near 1e8 instead of the NNLO 2.7e10), so only the DIFFERENCE is used:
   Delta lambda(mu) = lambda_model(mu) - lambda_SM(mu), both run at one loop from the same values at M_Z with two-loop gauge running for g3, then added to an NNLO-like baseline lambda_0(mu).
Baseline: lambda_0 = lambda_SM,1loop(mu) shifted by a constant so that it crosses zero at 2 Lambda_V = 2.7e10 GeV (Pass 12612), an approximation to the NNLO curve's shape, flagged.
Report: does lambda_0 + Delta lambda stay positive up to M_P?  The minimum value and where.  Models: Model A at M_X = 2.7e10 (4D two-loop), trinification 3 pairs at M_X = 2.85e11, and a control with no new states (Delta lambda = 0).
usage: py -3 pq_higgs_selfstab.py"""
import json
import math
import numpy as np
from scipy.integrate import solve_ivp

K = 1 / (16 * math.pi ** 2)
MT = 173.1
Y0 = [0.3587, 0.6478, 1.1666, 0.9369, 0.12604]  # g1 (non-GUT), g2, g3, yt, lambda at M_t


def run(dB3, dB2, dB1, MX, mu_max=2.4e18):
    def r(t, y):
        g1, g2, g3, yt, lam = y
        above = t > math.log(MX / MT)
        b1 = 41 / 6 + (dB1 * 5 / 3 if above else 0)  # non-GUT normalisation: Db1(GUT) x 5/3
        b2 = -19 / 6 + (dB2 if above else 0)
        b3 = -7 + (dB3 if above else 0)
        return [K * b1 * g1 ** 3, K * b2 * g2 ** 3, K * b3 * g3 ** 3, K * yt * (4.5 * yt ** 2 - 8 * g3 ** 2 - 2.25 * g2 ** 2 - 17 / 12 * g1 ** 2), K * (24 * lam ** 2 - 6 * yt ** 4 + 0.375 * (2 * g2 ** 4 + (g2 ** 2 + g1 ** 2) ** 2) + lam * (12 * yt ** 2 - 9 * g2 ** 2 - 3 * g1 ** 2))]
    ts = np.linspace(0, math.log(mu_max / MT), 400)
    s = solve_ivp(r, (0, ts[-1]), Y0, t_eval=ts, rtol=1e-9, atol=1e-11)
    return MT * np.exp(s.t), s.y[4], s.y[3], s.y[2]


def db(reps):
    T3 = {1: 0, 3: 0.5}
    T2 = {1: 0, 2: 0.5}
    d3 = sum(4 / 3 * T3[c] * w for c, w, y in reps)
    d2 = sum(4 / 3 * T2[w] * c for c, w, y in reps)
    d1 = sum(4 / 3 * 0.6 * y * y * c * w for c, w, y in reps)
    return d3, d2, d1


mu, lam_sm, yt_sm, g3_sm = run(0, 0, 0, 1e30)
# baseline shift: make lambda_SM cross zero at 2.7e10
i0 = np.argmin(np.abs(np.log(mu / 2.7e10)))
shift = -lam_sm[i0]
base = lam_sm + shift
out = dict(shift=float(shift), note="baseline = one-loop SM lambda shifted to cross zero at 2.7e10 GeV")
models = dict(control_none=([], 1e30), model_A=([(3, 1, -1 / 3), (3, 2, 1 / 6), (3, 2, 1 / 6)], 2.73e10), trinification_3=([(3, 2, 1 / 6), (3, 1, -1 / 3)] * 3, 2.85e11), model_A_low_MX=([(3, 1, -1 / 3), (3, 2, 1 / 6), (3, 2, 1 / 6)], 1e9))
for name, (reps, MX) in models.items():
    d3, d2, d1 = db(reps) if reps else (0, 0, 0)
    _, lam_m, yt_m, g3_m = run(d3, d2, d1, MX)
    dl = lam_m - lam_sm
    tot = base + dl
    k = np.argmin(tot)
    stable = bool(tot.min() > 0) or bool(np.all(tot[mu > 2.7e10] >= -1e-4))
    out[name] = dict(MX=MX, dB3=d3, delta_lambda_MP=float(dl[-1]), yt_MP=float(yt_m[-1]), yt_MP_SM=float(yt_sm[-1]), min_lambda=float(tot.min()), mu_at_min=float(mu[k]), stays_positive=bool(tot.min() > 0))
    print(name, "dB3 %.2f  Delta lambda(M_P) %+.4f  y_t(M_P) %.3f (SM %.3f)  min lambda %+.4f at %.2g GeV  positive: %s" % (d3, dl[-1], yt_m[-1], yt_sm[-1], tot.min(), mu[k], tot.min() > 0), flush=True)
json.dump(out, open("pq_higgs_selfstab.json", "w"), indent=1, default=float)
