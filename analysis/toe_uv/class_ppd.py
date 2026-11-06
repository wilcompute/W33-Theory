"""Posterior-predictive cross-validation: the proper score behind Pass 12597's point estimates.
For each model and held-out probe: start at the lowest-training-chi2 fit of class_holdout_dovekie_{hold}_neutral.json, build the Fisher matrix of the TRAINING residuals (held probe masked), draw parameters from that Gaussian posterior, and score each draw on the held probe only.  Report
   elpd = ln < exp(-chi2_held/2) >  over draws (expected log predictive density, up to the probe's constant),
   and the mean and spread of chi2_held.
Higher elpd is better.  Differences between models are the cross-validation evidence; the Gaussian posterior is an approximation, most of all for c, c' (Pass 12597 found the Fisher too narrow along c' by about 2, so a variant with the extra-parameter block inflated by 2 is also run).
Not blind: these data were seen when the models were chosen.
usage: python3 class_ppd.py hold(sn|bao) models ndraw"""
import json
import math
import os
import sys
import numpy as np

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
HOLD, models, ND = sys.argv[1], sys.argv[2].split(","), int(sys.argv[3])
DS = os.environ.get("DS", "dovekie")
sys.argv = ["x", DS, HOLD]
src = open("class_holdout.py", encoding="utf-8").read().split('if HOLD == "evidence":')[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_holdout.py"))
exec(src, g)
F, C, BMASK, SN, FREE, kind_of = g["F"], g["C"], g["BMASK"], g["SN"], g["FREE"], g["kind_of"]
neu = json.load(open(f"class_holdout_{DS}_{HOLD}_neutral.json"))
path = f"class_ppd_{DS}_{HOLD}{'_trunc' if os.environ.get('TRUNC', '1') == '1' else ''}.json"
out = json.load(open(path)) if os.path.exists(path) else dict(hold=HOLD, rows={})
rng = np.random.default_rng(20261105)
TRUNC = os.environ.get("TRUNC", "1") == "1"  # default on since Pass 12626: draws outside the flat priors are resampled, rejections and CLASS failures are recorded per row
BOUNDS = dict(c=(-3.0, 3.0), cp=(0.0, 0.2), w0=(-3.0, 1.0), wa=(-5.0, 3.0), tau=(0.01, 0.2))
n_rej = [0]


def in_prior(q):
    """flat-prior support used by the fits; CPL also needs w0 + wa < 0 (matter era)."""
    if any(n in q and not (lo <= q[n] <= hi) for n, (lo, hi) in BOUNDS.items()):
        return False
    return not ("w0" in q and "wa" in q and q["w0"] + q["wa"] >= 0)


def train_resid(p, k):
    F.sn = None if HOLD == "sn" else SN
    BMASK["on"] = True
    r = F.resid(p, k)[0]
    F.sn = SN
    BMASK["on"] = False
    return r


def held(p, k):
    F.sn = SN
    BMASK["on"] = False
    parts = F.resid(p, k)[1]
    return parts["sn" if HOLD == "sn" else "bao"]


for m in models:
    for infl in (1.0, 2.0):
        key = f"{m}_infl{infl:g}"
        if key in out["rows"] or (m == "LCDM" and infl > 1):
            continue
        best = min(neu["rows"][m], key=lambda r: r["train_chi2"])
        p0 = dict(best["p"])
        k = kind_of(m)
        free = C.NAMES + FREE[m]
        r0 = train_resid(p0, k)
        J = []
        for n in free:
            st = C.STEP[n]
            pu, pd = dict(p0), dict(p0)
            pu[n] += st
            pd[n] -= st
            J.append((train_resid(pu, k) - train_resid(pd, k)) / (2 * st))
        J = np.array(J).T
        cov = np.linalg.inv(J.T @ J)
        for i, n in enumerate(free):
            if n in FREE[m]:
                cov[i, :] *= infl
                cov[:, i] *= infl
        L = np.linalg.cholesky(cov + 1e-14 * np.eye(len(free)))
        hs = []
        for _ in range(ND):
            for _try in range(200):
                x = L @ rng.standard_normal(len(free))
                q = dict(p0)
                for i, n in enumerate(free):
                    q[n] = p0[n] + x[i]
                if not TRUNC or in_prior(q):
                    break
                n_rej[0] += 1
            q["tau"] = max(q["tau"], 0.01)
            try:
                hs.append(held(q, k))
            except Exception as e:
                print("draw failed", str(e)[-80:], flush=True)
        hs = np.array(hs)
        elpd = float(np.logaddexp.reduce(-0.5 * hs) - math.log(len(hs)))
        out["rows"][key] = dict(n=len(hs), elpd=elpd, chi2_best=best["held_chi2"], chi2_mean=float(hs.mean()), chi2_q=[float(v) for v in np.quantile(hs, [0.16, 0.5, 0.84])], sd={n: float(math.sqrt(cov[i, i])) for i, n in enumerate(free) if n in FREE[m]}, rejected_outside_prior=n_rej[0], failed=ND - len(hs))
        n_rej[0] = 0
        print(key, "elpd %.2f  held chi2 best %.2f mean %.2f q %s" % (elpd, best["held_chi2"], hs.mean(), np.round(np.quantile(hs, [0.16, 0.5, 0.84]), 1)), flush=True)
        json.dump(out, open(path, "w"), indent=1, default=float)
print("ppddone", flush=True)
